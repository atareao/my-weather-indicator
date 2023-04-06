#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# A library for access to Open-Meteo Service
#
# Copyright (C) 2023 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import logging
import requests
import weatherservice

BASE_URL = "https://api.open-meteo.com"

OMCONDITION = {
    0:  "clear",
    1:  "partly sunny",
    2:  "partly cloudy",
    3:  "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light intensity drizzle",
    52: "drizzle",
    53: "heavy intensity drizzle",
    56: "freezing drizzle",
    57: "heavy freezing drizzle",
    61: "light rain",
    63: "moderate rain",
    65: "heavy intensity rain",
    66: "freezing rain",
    67: "heavy freezing rain",
    71: "light snow",
    73: "snow",
    75: "heavy snow",
    77: "snow grains",
    80: "light intensity shower rain",
    81: "shower rain",
    82: "heavy intensity shower rain",
    85: "light show snow",
    86: "heavy show snow",
    95: "thunderstorm",
    96: "thunderstorm with light hail",
    99: "thunderstorm with heavy hail"
}


class OpenMeteoWeatherService(weatherservice.WeatherService):

    def __init__(self, longitude, latitude, units=weatherservice.Units()):
        self.latitude = latitude
        self.longitude = longitude
        self.units = units

    def _do_get(self, url):
        try:
            response = requests.get(url)
            print(response.status_code)
            if response.status_code == 200:
                return response.json()
            data = {}
            data = response.json()
            msg = f"Error. HTTP Error code: {response.status_code}"
            if "error" in data.keys() and data["error"] and \
                    "reason" in data.keys():
                print(data["reason"])
                msg = f"{msg}. {data['reason']}"
            raise Exception(msg)
        except Exception as exception:
            print(exception)
            logging.error(exception)
        return None

    def get_hourly_weather(self):
        weatherdata = []
        url = (f"{BASE_URL}/v1/forecast?latitude={self.latitude}"
               f"&longitude={self.longitude}&hourly=weathercode,"
               "temperature_2m,relativehumidity_2m,apparent_temperature,"
               "cloudcover,windspeed_10m,winddirection_10m,"
               "precipitation_probability,visibility")
        print(url)
        logging.info(url)
        data = self._do_get(url)
        pprint.pprint(data)
        if data:
            hourly = data["hourly"]
            for i in range(0, len(hourly["time"])):
                condition = OMCONDITION[hourly["weathercode"][i]]
                wind_direction = weatherservice.degToCompass2(
                        hourly["winddirection_10m"][i])
                velocity = hourly["windspeed_10m"][i]
                avewind = weatherservice.get_wind_condition2(
                        velocity, wind_direction[0], self.units.wind)
                wdd = {
                    "datetime": datetime.datetime.strptime(
                        hourly["time"][i],
                        "%Y-%m-%dT%H:%M"),
                    "condition": condition,
                    "condition_text": weatherservice.get_condition(
                        condition, 'text'),
                    "condition_image": weatherservice.get_condition(
                        condition, 'image'),
                    "condition_icon": weatherservice.get_condition(
                        condition, 'icon-light'),
                    "temperature": hourly["temperature_2m"][i],
                    "high": hourly["temperature_2m"][i],
                    "low": hourly["temperature_2m"][i],
                    "cloudiness": hourly["cloudcover"][i],
                    "avehumidity": hourly["relativehumidity_2m"][i],
                    "avewind": avewind,
                    "wind_icon": wind_direction[2]
                }
                weatherdata.append(wdd)
        return weatherdata


if __name__ == "__main__":
    import pprint
    longitude = -0.4016816
    latitude = 39.3527902
    print(longitude)
    omws = OpenMeteoWeatherService(longitude, latitude)
    pprint.pprint(omws.get_hourly_weather())
