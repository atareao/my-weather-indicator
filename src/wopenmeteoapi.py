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
import time
import utils
import weatherservice

logger = logging.getLogger(__name__)

BASE_URL = "https://api.open-meteo.com"


def get_value_for_time(hourly, timestamp, key):
    for i, value in enumerate(hourly["time"]):
        if value == timestamp:
            return hourly[key][i]
    return None


class OpenMeteoWeatherService(weatherservice.WeatherService):

    def __init__(self, longitude, latitude, location, timezone,
                 units=weatherservice.Units()):
        super().__init__(longitude, latitude, location, timezone, units)

    def _do_get(self, url):
        try:
            response = requests.get(url)
            logger.debug(response.status_code)
            if response.status_code == 200:
                logger.debug(response.json())
                return response.json()
            data = {}
            data = response.json()
            msg = "Error. HTTP Error code: {}".format(response.status_code)
            if "error" in data.keys() and data["error"] and \
                    "reason" in data.keys():
                logger.debug(data["reason"])
                msg = "{}. {}".format(msg, data['reason'])
            raise Exception(msg)
        except Exception as exception:
            logger.error(exception)
        return None

    def get_weather(self):
        weather_data = self.get_default_values()
        url = ("{}/v1/forecast?latitude={}&longitude={}&current_weather=true&"
               "timezone={}&daily=temperature_2m_max,temperature_2m_min,"
               "apparent_temperature_max,apparent_temperature_min,"
               "precipitation_sum,rain_sum,showers_sum,snowfall_sum,"
               "precipitation_hours,precipitation_probability_max,"
               "precipitation_probability_min,precipitation_probability_mean,"
               "weathercode,sunrise,sunset,windspeed_10m_max,"
               "winddirection_10m_dominant,shortwave_radiation_sum,"
               "uv_index_max,uv_index_clear_sky_max"
               "&hourly=relativehumidity_2m,apparent_temperature,"
               "pressure_msl,dewpoint_2m,cloudcover,visibility,uv_index"
               "&windspeed_unit=mph").format(BASE_URL, self._latitude,
                                             self._longitude, self._timezone)
        logger.debug(url)
        logger.info(url)
        data = self._do_get(url)
        if data:
            current_weather = data["current_weather"]
            daily = data["daily"]
            hourly = data["hourly"]
            timestamp = current_weather["time"]
            weather_data["update_time"] = time.time()
            weather_data["ok"] = True
            condition = current_weather["weathercode"]
            temperature = current_weather["temperature"]
            velocity = current_weather["windspeed"]
            direction = current_weather["winddirection"]
            humidity = \
                get_value_for_time(hourly, timestamp, "relativehumidity_2m")
            wind_direction = weatherservice.degToCompass2(direction)
            weather_data["current_conditions"]["condition_text"] =\
                weatherservice.get_condition_om(condition, "text")
            if weather_data['current_conditions']['isday']:
                weather_data['current_conditions']['condition_image'] =\
                    weatherservice.get_condition_om(condition, 'image')
                weather_data['current_conditions']['condition_icon_dark'] =\
                    weatherservice.get_condition_om(condition, 'icon-dark')
                weather_data['current_conditions']['condition_icon_light'] =\
                    weatherservice.get_condition_om(condition, 'icon-light')
            else:
                weather_data['current_conditions']['condition_image'] =\
                    weatherservice.get_condition_om(condition, 'image-night')
                weather_data['current_conditions']['condition_icon_dark'] =\
                    weatherservice.get_condition_om(condition,
                                                    'icon-night-dark')
                weather_data['current_conditions']['condition_icon_light'] =\
                    weatherservice.get_condition_om(condition,
                                                    'icon-night-light')
            weather_data['current_conditions']['temperature'] =\
                utils.change_temperature(temperature, self._units.temperature)
            weather_data["current_conditions"]["pressure"] = \
                get_value_for_time(hourly, timestamp, "pressure_msl")
            weather_data["current_conditions"]["humidity"] = "{} %".format(
                    humidity)
            weather_data['current_conditions']['heat_index'] =\
                weatherservice.get_heat_index(temperature, humidity)
            weather_data['current_conditions']['windchill'] =\
                weatherservice.get_wind_chill(temperature, velocity)
            weather_data["current_conditions"]["dew_point"] = \
                get_value_for_time(hourly, timestamp, "dewpoint_2m")
            weather_data["current_conditions"]["feels_like"] = \
                utils.change_temperature(get_value_for_time(
                    hourly, timestamp, "apparent_temperature"),
                                         self._units.temperature)
            weather_data["current_conditions"]["cloudiness"] = \
                get_value_for_time(hourly, timestamp, "cloudcover")
            weather_data["current_conditions"]["visibility"] = \
                get_value_for_time(hourly, timestamp, "visibility")
            weather_data["current_conditions"]["UV"] = \
                get_value_for_time(hourly, timestamp, "uv_index")
            weather_data['current_conditions']['wind_condition'] =\
                weatherservice.get_wind_condition2(
                    velocity, wind_direction[0], self._units.wind)
            weather_data['current_conditions']['wind_icon'] = wind_direction[2]
            for i in range(0, len(daily["time"])):
                condition = daily["weathercode"][i]
                temp_max = daily["temperature_2m_max"][i]
                temp_min = daily["temperature_2m_min"][i]
                velocity = daily["windspeed_10m_max"][i]
                direction = daily["winddirection_10m_dominant"][i]
                wind_direction = weatherservice.degToCompass2(direction)
                weather_data['forecasts'][i]["condition"] = condition
                weather_data['forecasts'][i]["condition_text"] =\
                    weatherservice.get_condition_om(condition, 'text')
                weather_data['forecasts'][i]["condition_image"] =\
                    weatherservice.get_condition_om(condition, 'image')
                weather_data['forecasts'][i]["condition_icon"] =\
                    weatherservice.get_condition_om(condition, 'icon-light')
                weather_data['forecasts'][i]["low"] =\
                    utils.change_temperature(temp_min, self._units.temperature)
                weather_data['forecasts'][i]["high"] =\
                    utils.change_temperature(temp_max, self._units.temperature)
                weather_data['forecasts'][i]["cloudiness"] = None
                weather_data['forecasts'][i]["avehumidity"] = None
                weather_data['forecasts'][i]["avewind"] =\
                    weatherservice.get_wind_condition2(
                        velocity, wind_direction[0], self._units.wind)
                weather_data['forecasts'][i]["wind_icon"] = wind_direction[2]
                weather_data['forecasts'][i]["qpf_allday"] = \
                    daily["rain_sum"][i]
                weather_data['forecasts'][i]["qpf_day"] = None
                weather_data['forecasts'][i]["qpf_night"] = None
                weather_data['forecasts'][i]["snow_allday"] = None
                weather_data['forecasts'][i]["snow_day"] = \
                    daily["snowfall_sum"][i]
                weather_data['forecasts'][i]["snow_night"] = None
                weather_data['forecasts'][i]["maxwind"] = None
                weather_data['forecasts'][i]["maxhumidity"] = None
                weather_data['forecasts'][i]['minhumidity'] = None
            return weather_data

    def get_hourly_weather(self):
        weatherdata = []
        url = ("{}/v1/forecast?latitude={}&longitude={}&hourly=weathercode,"
               "temperature_2m,relativehumidity_2m,apparent_temperature,"
               "cloudcover,windspeed_10m,winddirection_10m,"
               "precipitation_probability,visibility"
               "&windspeed_unit=mph").format(BASE_URL, self._latitude,
                                             self._longitude)
        logger.info(url)
        data = self._do_get(url)
        if data:
            hourly = data["hourly"]
            for i in range(0, len(hourly["time"])):
                condition = hourly["weathercode"][i]
                logger.debug(condition)
                wind_direction = weatherservice.degToCompass2(
                        hourly["winddirection_10m"][i])
                velocity = hourly["windspeed_10m"][i]
                avewind = weatherservice.get_wind_condition2(
                        velocity, wind_direction[0], self._units.wind)
                wdd = {
                    "datetime": datetime.datetime.strptime(
                        hourly["time"][i],
                        "%Y-%m-%dT%H:%M"),
                    "condition": condition,
                    "condition_text": weatherservice.get_condition_om(
                        condition, 'text'),
                    "condition_image": weatherservice.get_condition_om(
                        condition, 'image'),
                    "condition_icon": weatherservice.get_condition_om(
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
    from pprint import pprint
    longitude = -0.4016816
    latitude = 39.3527902
    location = "Silla"
    timezone = "Europe/Madrid"
    logger.info(longitude)
    omws = OpenMeteoWeatherService(longitude, latitude, location, timezone)
    pprint(omws.get_weather())
