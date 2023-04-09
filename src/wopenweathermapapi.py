#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# A library for access to OpenWeatherMap Weather Service
#
# Copyright (C) 2011 Lorenzo Carbonell
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

import utils as cf
import weatherservice
import time
from datetime import datetime
from weatherservice import WeatherService
from comun import read_json_from_url


APPID = '4516154e5c8a6494e7e13b550408c863'

OWMURL = 'http://api.openweathermap.org/data/2.5'
URL_FIND_CITY = OWMURL + '/find?lat=%s&lon=%s&cnt=1&appid=' + APPID
URL_CURRENT_CITY_ID = OWMURL + '/weather?id=%s&appid=' + APPID
URL_FORECAST_CITY_ID = OWMURL + '/forecast/daily?id=%s&cnt=7&\
mode=json&appid=' + APPID
URL_HOURLY_CITY_ID = OWMURL + '/forecast?id=%s&appid=' + APPID
URL_CURRENT_CITY_LL = OWMURL + '/weather?lat=%s&lon=%s&appid=' + APPID
URL_FORECAST_CITY_LL = OWMURL + '/forecast/daily?lat=%s&lon=%s&appid=' + APPID
URL_HOURLY_CITY_LL = OWMURL + '/forecast?lat=%s&lon=%s&appid=' + APPID


CONDITION = {}
CONDITION[200] = 'thunderstorm with light rain'
CONDITION[201] = 'thunderstorm with rain'
CONDITION[202] = 'thunderstorm with heavy rain'
CONDITION[210] = 'light thunderstorm'
CONDITION[211] = 'thunderstorm'
CONDITION[212] = 'heavy thunderstorm'
CONDITION[221] = 'ragged thunderstorm'
CONDITION[230] = 'thunderstorm with light drizzle'
CONDITION[231] = 'thunderstorm with drizzle'
CONDITION[232] = 'thunderstorm with heavy drizzle'
CONDITION[300] = 'light intensity drizzle'
CONDITION[301] = 'drizzle'
CONDITION[302] = 'heavy intensity drizzle'
CONDITION[310] = 'light intensity drizzle rain'
CONDITION[311] = 'drizzle rain'
CONDITION[312] = 'heavy intensity drizzle rain'
CONDITION[313] = 'shower rain and drizzle'
CONDITION[314] = 'heavy shower rain and drizzle'
CONDITION[321] = 'shower drizzle'
CONDITION[500] = 'light rain'
CONDITION[501] = 'moderate rain'
CONDITION[502] = 'heavy intensity rain'
CONDITION[503] = 'very heavy rain'
CONDITION[504] = 'extreme rain'
CONDITION[511] = 'freezing rain'
CONDITION[520] = 'light intensity shower rain'
CONDITION[521] = 'shower rain'
CONDITION[522] = 'heavy intensity shower rain'
CONDITION[531] = 'ragged shower rain'
CONDITION[600] = 'light snow'
CONDITION[601] = 'snow'
CONDITION[602] = 'heavy snow'
CONDITION[611] = 'sleet'
CONDITION[612] = 'light shower sleet'
CONDITION[613] = 'shower sleet'
CONDITION[615] = 'light rain and snow'
CONDITION[616] = 'rain and snow'
CONDITION[620] = 'light shower snow'
CONDITION[621] = 'shower snow'
CONDITION[622] = 'heavy shower snow'
CONDITION[701] = 'mist'
CONDITION[711] = 'smoke'
CONDITION[721] = 'haze'
CONDITION[731] = 'sand / dust whirls'
CONDITION[741] = 'fog'
CONDITION[751] = 'sand'
CONDITION[761] = 'dust'
CONDITION[762] = 'volcanic ash'
CONDITION[771] = 'squalls'
CONDITION[781] = 'tornado'
CONDITION[800] = 'clear'  # sky is clear
CONDITION[801] = 'partly sunny'  # few clouds
CONDITION[802] = 'partly cloudy'  # scattered clouds
CONDITION[803] = 'cloudy'  # broken clouds
CONDITION[804] = 'overcast'  # overcast clouds
CONDITION[900] = 'tornado'
CONDITION[901] = 'tropical storm'
CONDITION[902] = 'hurricane'
CONDITION[903] = 'cold'
CONDITION[904] = 'hot'
CONDITION[905] = 'windy'
CONDITION[906] = 'hail'


def find_city(longitude, latitude):
    url = URL_FIND_CITY % (latitude, longitude)
    parsed_json = read_json_from_url(url)
    if parsed_json:
        elist = parsed_json['list']
        if len(elist) > 0:
            return elist[0]['id']
    return None


class OWMWeatherService(WeatherService):

    def __init__(self, longitude=-0.418, latitude=39.360,
                 units=weatherservice.Units()):
        super().__init__(longitude, latitude, units)
        self._id = find_city(longitude, latitude)
        print('** OWM **')
        print(self._id, longitude, latitude)

    def get_hourly_weather(self):
        weatherdata = []
        if self._id:
            url = URL_HOURLY_CITY_ID % self._id
        else:
            url = URL_HOURLY_CITY_LL % (self._latitude, self._longitude)
        print('OWMWeatherService Current Weather url:%s' % (url))
        parsed_json = read_json_from_url(url)
        if parsed_json is None:
            return weatherdata
        for data in parsed_json['list']:
            condition = CONDITION[data['weather'][0]['id']]
            temperature = cf.fa2f(data['main']['temp'])
            cloudiness = data['clouds']['all']
            # pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            velocity = data['wind']['speed'] if 'wind' in data.keys() and\
                'speed' in data['wind'].keys() else 0.0
            t1 = cf.fa2f(data['main']['temp_min'])
            t2 = cf.fa2f(data['main']['temp_max'])
            direction = data['wind']['deg'] if 'wind' in data.keys() and\
                'deg' in data['wind'].keys() else 0.0
            if t1 < t2:
                temp_min = str(t1)
                temp_max = str(t2)
            else:
                temp_min = str(t2)
                temp_max = str(t1)
            wind_direction = weatherservice.degToCompass2(direction)

            wdd = {}
            wdd['datetime'] = datetime.fromtimestamp(data['dt'])
            wdd['condition'] = condition
            wdd['condition_text'] = weatherservice.get_condition(
                condition, 'text')
            wdd['condition_image'] = weatherservice.get_condition(
                condition, 'image')
            wdd['condition_icon'] = weatherservice.get_condition(
                condition, 'icon-light')
            wdd['temperature'] = cf.change_temperature(
                temperature, self._units.temperature).split(' ')[0]
            wdd['low'] = cf.change_temperature(
                temp_min, self._units.temperature)
            wdd['high'] = cf.change_temperature(
                temp_max, self._units.temperature)
            wdd['cloudiness'] = '%s' % (cloudiness)
            wdd['avehumidity'] = '%s' % (humidity)
            wdd['avewind'] = weatherservice.get_wind_condition2(
                velocity, wind_direction[0], self._units.wind)
            wdd['wind_icon'] = wind_direction[2]
            weatherdata.append(wdd)
        return weatherdata

    def get_weather(self):
        weather_data = self.get_default_values()
        if self._id is None:
            self._id = find_city(self._longitude, self._latitude)
            print('****', self._id)
        if self._id is not None:
            url = URL_CURRENT_CITY_ID % self._id
        else:
            url = URL_CURRENT_CITY_LL % (self._latitude, self._longitude)
        print('-------------------------------------------------------')
        print('OpenWeatherMap Weather Service url:%s' % (url))
        print('-------------------------------------------------------')
        parsed_json = read_json_from_url(url)
        if parsed_json is None or\
                'weather' not in parsed_json.keys() or\
                'main' not in parsed_json.keys() or\
                'wind' not in parsed_json.keys() or\
                'clouds' not in parsed_json.keys():
            return weather_data
        weather_data['update_time'] = time.time()
        weather_data['ok'] = True
        if parsed_json['weather'][0]['id'] not in CONDITION.keys():
            condition = 'not available'
        else:
            condition = CONDITION[parsed_json['weather'][0]['id']]
        temperature = cf.fa2f(parsed_json['main']['temp'])
        pressure = parsed_json['main']['pressure'] if 'pressure' in\
            parsed_json['main'] else 0
        humidity = parsed_json['main']['humidity'] if 'humidity' in\
            parsed_json['main'] else 0
        velocity = parsed_json['wind']['speed'] if 'speed' in\
            parsed_json['wind'] else 0
        cloudiness = parsed_json['clouds']['all']
        if 'deg' in parsed_json['wind'].keys():
            direction = parsed_json['wind']['deg']
        else:
            direction = 0
        wind_direction = weatherservice.degToCompass2(direction)
        weather_data['current_conditions']['condition'] = condition
        weather_data['current_conditions']['condition_text'] =\
            weatherservice.get_condition(condition, 'text')
        if weather_data['current_conditions']['isday']:
            weather_data['current_conditions']['condition_image'] =\
                weatherservice.get_condition(condition, 'image')
            weather_data['current_conditions']['condition_icon_dark'] =\
                weatherservice.get_condition(condition, 'icon-dark')
            weather_data['current_conditions']['condition_icon_light'] =\
                weatherservice.get_condition(condition, 'icon-light')
        else:
            weather_data['current_conditions']['condition_image'] =\
                weatherservice.get_condition(condition, 'image-night')
            weather_data['current_conditions']['condition_icon_dark'] =\
                weatherservice.get_condition(condition, 'icon-night-dark')
            weather_data['current_conditions']['condition_icon_light'] =\
                weatherservice.get_condition(condition, 'icon-night-light')
        weather_data['current_conditions']['temperature'] =\
            cf.change_temperature(
                temperature, self._units.temperature)
        weather_data['current_conditions']['pressure'] =\
            weatherservice.change_pressure(
                pressure, self._units.pressure)
        weather_data['current_conditions']['humidity'] = '%s %%' % (humidity)
        weather_data['current_conditions']['dew_point'] =\
            weatherservice.get_dew_point(
                humidity, temperature, self._units.temperature)
        weather_data['current_conditions']['wind_condition'] =\
            weatherservice.get_wind_condition2(
                velocity, wind_direction[0], self._units.wind)
        weather_data['current_conditions']['wind_icon'] = wind_direction[2]
        weather_data['current_conditions']['heat_index'] =\
            weatherservice.get_heat_index(temperature, humidity)
        weather_data['current_conditions']['windchill'] =\
            weatherservice.get_wind_chill(temperature, velocity)
        weather_data['current_conditions']['feels_like'] =\
            weatherservice.get_feels_like(
                temperature, humidity, velocity, self._units.temperature)
        weather_data['current_conditions']['visibility'] = None
        weather_data['current_conditions']['cloudiness'] = \
            '%s %%' % (cloudiness)
        weather_data['current_conditions']['solarradiation'] = None
        weather_data['current_conditions']['UV'] = None
        weather_data['current_conditions']['precip_1hr'] = None
        weather_data['current_conditions']['precip_today'] = None
        #

        # try:
        if self._id:
            url = URL_FORECAST_CITY_ID % self._id
        else:
            url = URL_FORECAST_CITY_LL % (self._latitude, self._longitude)
        parsed_json = read_json_from_url(url)
        if parsed_json is None:
            return weather_data
        for contador, data in enumerate(parsed_json['list']):
            if data['weather'][0]['id'] in CONDITION:
                condition = CONDITION[data['weather'][0]['id']]
            else:
                data = data['weather'][0]['description']
            temperature = cf.fa2f(data['temp']['day'])
            cloudiness = data['clouds'] if 'clouds' in data.keys() else 0
            pressure = data['pressure'] if 'pressure' in data.keys() else 0
            humidity = data['humidity'] if 'humidity' in data.keys() else 0
            velocity = data['speed'] if 'speed' in data.keys() else 0
            t1 = cf.fa2f(data['temp']['min'])
            t2 = cf.fa2f(data['temp']['max'])
            direction = data['deg']
            if t1 < t2:
                temp_min = str(t1)
                temp_max = str(t2)
            else:
                temp_min = str(t2)
                temp_max = str(t1)
            wind_direction = weatherservice.degToCompass2(direction)
            weather_data['forecasts'][contador]['condition'] = condition
            weather_data['forecasts'][contador]['condition_text'] =\
                weatherservice.get_condition(condition, 'text')
            weather_data['forecasts'][contador]['condition_image'] =\
                weatherservice.get_condition(condition, 'image')
            weather_data['forecasts'][contador]['condition_icon'] =\
                weatherservice.get_condition(condition, 'icon-light')
            weather_data['forecasts'][contador]['low'] =\
                cf.change_temperature(
                    temp_min, self._units.temperature)
            weather_data['forecasts'][contador]['high'] =\
                cf.change_temperature(
                    temp_max, self._units.temperature)
            weather_data['forecasts'][contador]['cloudiness'] =\
                '%s %%' % (cloudiness)
            weather_data['forecasts'][contador]['avehumidity'] =\
                '%s %%' % (humidity)
            weather_data['forecasts'][contador]['avewind'] =\
                weatherservice.get_wind_condition2(
                    velocity, wind_direction[0], self._units.wind)
            weather_data['forecasts'][contador]['wind_icon'] =\
                wind_direction[2]
            weather_data['forecasts'][contador]['qpf_allday'] = None
            weather_data['forecasts'][contador]['qpf_day'] = None
            weather_data['forecasts'][contador]['qpf_night'] = None
            weather_data['forecasts'][contador]['snow_allday'] = None
            weather_data['forecasts'][contador]['snow_day'] = None
            weather_data['forecasts'][contador]['snow_night'] = None
            weather_data['forecasts'][contador]['maxwind'] = None
            weather_data['forecasts'][contador]['maxhumidity'] = None
            weather_data['forecasts'][contador]['minhumidity'] = None
        # except Exception as e:
        # print(e)
        return weather_data


if __name__ == "__main__":
    import pprint
    longitude = -0.4016816
    latitude = 39.3527902
    owm = OWMWeatherService(longitude=longitude, latitude=latitude)
    pprint.pprint(owm.get_weather())
    '''
    print(owm.get_hourly_weather())
    result = 'Fecha,Temperature,Humidity,Cloudiness\\n'
    for data in owm.get_hourly_weather():
        print(data['datetime'])
        print(data['temperature'])
        print(data['avehumidity'])
        result += str(data['datetime']) + ','
        result += str(data['temperature']) + ','
        result += str(data['avehumidity']) + ','
        result += str(data['cloudiness'])+'\\n'
    print(result)
    from graph import Graph
    graph = Graph(result)
    '''
