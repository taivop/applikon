import asyncio
import json
import logging
import os

import websockets
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from parse import parse_sensor_data

load_dotenv()  # Take environment variables from .env. See .env.example.

# Setup logging
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger("poll")

INFLUXDB_TOKEN = os.environ["INFLUXDB_TOKEN"]
INFLUXDB_URL = os.environ["INFLUXDB_URL"]
INFLUXDB_ORG = os.environ["INFLUXDB_ORG"]
INFLUXDB_BUCKET = os.environ["INFLUXDB_BUCKET"]

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Load list of reactors we should be polling
reactors_conf = json.load(open("reactors.json"))
hosts = reactors_conf["hosts"]


async def poll_once(host):
    uri = f"ws://{host['address']}"
    logger.info("Connecting to reactor '%s' at '%s'", host["name"], uri)

    async with websockets.connect(uri) as websocket:
        # Ask for all sensor values
        await websocket.send("J1.15S\r")
        message = await websocket.recv()
        sensor_data = parse_sensor_data(message.decode("utf-8"))
        logger.info("Reactor '%s' readings: %s", host["name"], sensor_data)

        # Assemble message for InfluxDB
        sequence = []
        for field in sensor_data:
            sequence.append(f"{field},host={uri} {field}={sensor_data[field]}")

        write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, sequence)
        logger.info("Saved sample for reactor '%s' at '%s'", host["name"], uri)


async def main():
    for host in hosts:
        await poll_once(host)


if __name__ == "__main__":
    asyncio.run(main())
