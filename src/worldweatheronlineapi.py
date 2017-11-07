#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#
# A library for accessing to gunderground api
#
# Copyright (C) 2012 Lorenzo Carbonell
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
#
#

import sys
import json
import time
import weatherservice
from weatherservice import WeatherService
from comun import _
from comun import read_json_from_url

KEY = '5aa718e771170840121008'
URL = 'http://api.worldweatheronline.com/free/v1/weather.ashx?q=%s,%s\
&format=json&num_of_days=5&key=%s'  # (latitude,longitude)
CODES = {
    '395': 'moderate or heavy snow in area with thunder',
    '392': 'patchy light snow in area with thunder',
    '389': 'moderate or heavy rain in area with thunder',
    '386': 'patchy light rain in area with thunder',
    '377': 'moderate or heavy showers of ice pellets',
    '374': 'light showers of ice pellets',
    '371': 'moderate or heavy snow showers',
    '368': 'light snow showers',
    '365': 'moderate or heavy',
    '362': 'light sleet showers',
    '359': 'torrential rain shower',
    '356': 'moderate or heavy rain shower',
    '353': 'light rain shower',
    '350': 'ice pellets',
    '338': 'heavy snow',
    '335': 'patchy heavy snow',
    '332': 'moderate snow',
    '329': 'patchy moderate snow',
    '326': 'light snow',
    '323': 'patchy light snow',
    '320': 'moderate or heavy sleet',
    '317': 'light sleet',
    '314': 'moderate or heavy freezing rain',
    '311': 'light freezing rain',
    '308': 'heavy rain',
    '305': 'heavy rain at times',
    '302': 'moderate rain',
    '299': 'moderate rain at times',
    '296': 'light rain',
    '293': 'patchy light rain',
    '284': 'heavy freezing drizzle',
    '281': 'freezing drizzle',
    '266': 'light drizzle',
    '263': 'patchy light drizzle',
    '260': 'freezing fog',
    '248': 'fog',
    '230': 'blizzard',
    '227': 'blowing snow',
    '200': 'thundery outbreaks in nearby',
    '185': 'patchy freezing drizzle nearby',
    '182': 'patchy sleet nearby',
    '179': 'patchy snow nearby',
    '176': 'patchy rain nearby',
    '143': 'mist',
    '122': 'overcast',
    '119': 'cloudy',
    '116': 'partly cloudy',
    '113': 'clear'}


def get_condition(code):
    if code in CODES.keys():
        return CODES[code]
    return None


def gvfco(key, tree):
    if 'data' in tree.keys():
        if 'current_condition' in tree['data'].keys():
            if len(tree['data']['current_condition']) > 0:
                if key in tree['data']['current_condition'][0].keys():
                    return tree['data']['current_condition'][0][key]
    return _('N/A')


def gvfi(key, tree):
    if 'request' in tree.keys():
        if 'current_condition' in tree['data'].keys():
            if len(tree['data']['current_condition']) > 0:
                if key in tree['data']['current_condition'][0].keys():
                    return tree['data']['current_condition'][0][key]
    return _('N/A')


def gvff(key, day, tree):
    if 'data' in tree.keys():
        if 'weather' in tree['data'].keys():
            if len(tree['data']['weather']) > 0:
                if key in tree['data']['weather'][day].keys():
                    return tree['data']['weather'][day][key]
    return _('N/A')


class WorldWeatherOnlineService(WeatherService):
    def __init__(self, longitude=-0.418, latitude=39.360,
                 units=weatherservice.Units(), key=''):
        WeatherService.__init__(self, longitude, latitude, units, key)

    def test_connection(self):
        try:
            parsed_json = read_json_from_url(URL % (
                self.latitude, self.longitude, self.key))
            if parsed_json is None:
                print(parsed_json)
                return False
        except Exception as e:
            print(e)
            return False
        return True

    def get_weather(self):
        weather_data = self.get_default_values()
        print('-------------------------------------------------------')
        print('-------------------------------------------------------')
        print('WorldWeatherOnline Weather Service url: %s' % (
            URL % (self.latitude, self.longitude, self.key)))
        print('-------------------------------------------------------')
        print('-------------------------------------------------------')
        try:
            parsed_json = read_json_from_url(URL % (
                self.latitude, self.longitude, self.key))
            if parsed_json is None or\
                    'data' not in parsed_json.keys() or\
                    parsed_json['data'] is None or\
                    'current_condition' not in parsed_json['data'].keys() or\
                    'weather' not in parsed_json['data'].keys():
                return weather_data
            weather_data['update_time'] = time.time()
            weather_data['ok'] = True
            number_condition = gvfco('weatherCode', parsed_json)
            condition = get_condition(number_condition)
            print('*******************')
            print('********11***********')
            print('*******************')
            #
            weather_data['current_conditions']['condition_text'] =\
                weatherservice.get_condition_wwa(condition, 'text')
            if weather_data['current_conditions']['isday']:
                weather_data['current_conditions']['condition_image'] =\
                    weatherservice.get_condition_wwa(condition, 'image')
                weather_data['current_conditions']['condition_icon_dark'] =\
                    weatherservice.get_condition_wwa(condition, 'icon-dark')
                weather_data['current_conditions']['condition_icon_light'] =\
                    weatherservice.get_condition_wwa(condition, 'icon-light')
            else:
                weather_data['current_conditions']['condition_image'] =\
                    weatherservice.get_condition_wwa(condition, 'image-night')
                weather_data['current_conditions']['condition_icon_dark'] =\
                    weatherservice.get_condition_wwa(
                        condition, 'icon-night-dark')
                weather_data['current_conditions']['condition_icon_light'] =\
                    weatherservice.get_condition_wwa(
                        condition, 'icon-night-light')
            temperature = weatherservice.s2f(gvfco('temp_F', parsed_json))
            weather_data['current_conditions']['temperature'] =\
                weatherservice.change_temperature(
                    temperature, self.units.temperature)
            pressure = weatherservice.s2f(gvfco('pressure', parsed_json))
            weather_data['current_conditions']['pressure'] =\
                weatherservice.change_pressure(pressure, self.units.pressure)
            humidity = weatherservice.s2f(gvfco('humidity', parsed_json))
            weather_data['current_conditions']['humidity'] = '%s %%' % (
                int(humidity))
            weather_data['current_conditions']['dew_point'] =\
                weatherservice.get_dew_point(
                    humidity, temperature, self.units.temperature)
            wind_velocity = weatherservice.s2f(
                gvfco('windspeedMiles', parsed_json))
            wind_direction = weatherservice.degToCompass2(
                gvfco('winddirDegree', parsed_json))
            weather_data['current_conditions']['wind_condition'] =\
                weatherservice.get_wind_condition2(
                    wind_velocity, wind_direction[0], self.units.wind)
            weather_data['current_conditions']['wind_icon'] = wind_direction[2]
            #
            weather_data['current_conditions']['heat_index'] =\
                weatherservice.get_heat_index(temperature, humidity)
            weather_data['current_conditions']['windchill'] =\
                weatherservice.get_wind_chill(temperature, wind_velocity)
            #
            weather_data['current_conditions']['feels_like'] =\
                weatherservice.get_feels_like(
                    temperature, humidity, wind_velocity,
                    self.units.temperature)
            #
            weather_data['current_conditions']['visibility'] =\
                weatherservice.change_distance(
                    gvfco('visibility', parsed_json), self.units.visibility)
            weather_data['current_conditions']['solarradiation'] = None
            weather_data['current_conditions']['UV'] = None
            weather_data['current_conditions']['precip_1hr'] = None
            weather_data['current_conditions']['precip_today'] =\
                weatherservice.change_longitude(
                    weatherservice.s2f(
                        gvfco('precipMM', parsed_json))/25.4,
                    self.units.rain)
            for i in range(0, 5):
                t1 = weatherservice.s2f(gvff('tempMinF', i, parsed_json))
                t2 = weatherservice.s2f(gvff('tempMaxF', i, parsed_json))
                if t1 < t2:
                    tmin = str(t1)
                    tmax = str(t2)
                else:
                    tmin = str(t2)
                    tmax = str(t1)
                weather_data['forecasts'][i]['low'] =\
                    weatherservice.change_temperature(
                        tmin, self.units.temperature)
                weather_data['forecasts'][i]['high'] =\
                    weatherservice.change_temperature(
                        tmax, self.units.temperature)
                #
                weather_data['forecasts'][i]['qpf_allday'] =\
                    weatherservice.change_longitude(
                        weatherservice.s2f(
                            gvff('precipMM', i, parsed_json))/25.4,
                        self.units.rain)
                weather_data['forecasts'][i]['qpf_day'] = None
                weather_data['forecasts'][i]['qpf_night'] = None
                weather_data['forecasts'][i]['snow_allday'] = None
                weather_data['forecasts'][i]['snow_day'] = None
                weather_data['forecasts'][i]['snow_night'] = None
                weather_data['forecasts'][i]['maxwind'] = None
                winddir = gvff('winddirDegree', i, parsed_json)
                winsped = gvff('windspeedMiles', i, parsed_json)
                wind_direction = weatherservice.degToCompass2(winddir)
                weather_data['forecasts'][i]['avewind'] =\
                    weatherservice.get_wind_condition2(
                        winsped, wind_direction[0], self.units.wind)
                weather_data['forecasts'][i]['wind_icon'] = wind_direction[2]
                weather_data['forecasts'][i]['avehumidity'] = None
                weather_data['forecasts'][i]['maxhumidity'] = None
                weather_data['forecasts'][i]['minhumidity'] = None
                #
                number_condition = gvff('weatherCode', i, parsed_json).lower()
                condition = get_condition(number_condition)
                weather_data['forecasts'][i]['condition'] = condition
                weather_data['forecasts'][i]['condition_text'] =\
                    weatherservice.get_condition_wwa(condition, 'text')
                weather_data['forecasts'][i]['condition_image'] =\
                    weatherservice.get_condition_wwa(condition, 'image')
                weather_data['forecasts'][i]['condition_icon'] =\
                    weatherservice.get_condition_wwa(condition, 'icon-light')
            weather_data['forecast_information']['city'] = None
            weather_data['forecast_information']['postal_code'] = None
            weather_data['forecast_information']['latitude_e6'] = None
            weather_data['forecast_information']['longitude_e6'] = None
        except Exception as e:
            print(e)
            weather_data['ok'] = False
        return weather_data


if __name__ == '__main__':
    import pprint
    lat = 49.9026653
    lon = 18.8278352
    uws = WorldWeatherOnlineService(
        longitude=lat,
        latitude=lon,
        key='1227f7624fa47506bc0b125184cda68e32f131e2')
    weather_data = uws.get_weather()
    pprint.pprint(weather_data['forecasts'])
    exit(0)
