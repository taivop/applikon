import asyncio

import websockets
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from parse_data import parse_sensor_data

# You can generate a Token from the "Tokens Tab" in the UI
token = "jqWknvpNYX1jdkBDFlFhvZfObI6oyHkQXcPow0aMoW84hOyI5vl7gsBQ1b0kXEZEvwovoDJa24baQJczYTou-A=="
org = "sq42na@gmail.com"
bucket = "sq42na's Bucket"

client = InfluxDBClient(
    url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token
)
write_api = client.write_api(write_options=SYNCHRONOUS)


async def listen():
    uri = "ws://192.168.1.241"
    async with websockets.connect(uri) as websocket:
        print(f"connected to {uri}")

        await websocket.send("J1.15S\r")  # Update all sensor values
        message = await websocket.recv()
        sensor_data = parse_sensor_data(message.decode("utf-8"))

        sequence = []
        for field in sensor_data:
            sequence.append(f"{field},host={uri} {field}={sensor_data[field]}")

        write_api.write(bucket, org, sequence)

        # async for message in websocket:
        #    await consumer(message)


asyncio.run(listen())
