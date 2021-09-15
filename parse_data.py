import re

re_message = re.compile(r"J1\.15\.(\d+)A(.*)")

sensor_map = {0: "pH", 1: "do2", 2: "temperature", 5: "o2", 6: "co2", 13: "stirrer"}

type_map = {13: int}


def parse_sensor_data(data_string):
    messages = [m for m in data_string.split("\r") if len(m)]

    sensor_data = dict()

    for m in messages:
        m_search = re_message.search(m)
        if m_search:
            datapoint_id = int(m_search.group(1))
            datapoint_value = m_search.group(2)

            if datapoint_id in sensor_map:
                # print(f"{datapoint_id:<2} {sensor_map[datapoint_id]:<12} -> {datapoint_value:>5}")
                data_type_convert = type_map.get(datapoint_id, float)
                sensor_data[sensor_map[datapoint_id]] = data_type_convert(
                    datapoint_value
                )
        else:
            print("NO MESSAGE FOUND")

    return sensor_data


if __name__ == "__main__":
    with open("data_example.txt") as f:
        data_string = "".join(f.readlines())

        parse_sensor_data(data_string)
