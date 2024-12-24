import requests
import json
from statistics import mean


START_DATE = '2024-08-18'
END_DATE = '2024-08-25'


response = requests.get(
    'https://archive-api.open-meteo.com/v1/archive?latitude=52.2298&longitude=21.0118&start_date={start_date}&end_date={end_date}&hourly=temperature_2m&daily=rain_sum&timezone=Europe%2FBerlin'.format(start_date = START_DATE, end_date = END_DATE))
data = response.json()

weather_data = {}

d1 = data['hourly']['time']
d2 = data['hourly']['temperature_2m']
d3 = data['daily'].keys()


def extract_date_time(date_data: str):
    return date_data.split('T')


temperature_index = 0
rain_index = 0
for date in d1:
    if extract_date_time(date)[0] not in weather_data.keys():
        weather_data[extract_date_time(date)[0]] = {"rain": data['daily']['rain_sum'][rain_index],
                                                    "temperature": {}}
        rain_index += 1
    weather_data[extract_date_time(date)[0]]["temperature"][extract_date_time(date)[1]] = d2[temperature_index]
    temperature_index += 1


def five_minutes_forward(given_time: str):
    output = given_time[:3]
    minutes = int(given_time[3:])
    minutes += 5
    new_minutes = f"{minutes:02}"
    return output + new_minutes


def five_minutes_average(temperatures: dict):
    for i in range(len(temperatures) - 1):
        start_time, start_temperature = list(temperatures.keys())[i],  list(temperatures.values())[i]
        end_temperature = list(temperatures.values())[i+1]
        for j in range(10):
            average = ((10 - j) * start_temperature + (j + 1) * end_temperature)/11
            start_time = five_minutes_forward(start_time)
            temperatures[start_time] = round(average, 2)
    return temperatures


weather_data[list(weather_data.keys())[0]]['temperature'] = five_minutes_average(weather_data[list(weather_data.keys())[0]]['temperature'])
myKeys = list(weather_data[list(weather_data.keys())[0]]['temperature'].keys())
myKeys.sort()
weather_data[list(weather_data.keys())[0]]['temperature'] = {i: weather_data[list(weather_data.keys())[0]]['temperature'][i] for i in myKeys}
for date in weather_data.keys():
    weather_data[date]['avg_temperature'] = round(mean(weather_data[date]['temperature'].values()),2)

print(weather_data)
with open("weather_data.json", "w") as outfile:
    json.dump(weather_data, outfile)
