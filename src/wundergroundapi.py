#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A library for accessing to gunderground api
#
# Copyright (C) 2012 - 2016 Lorenzo Carbonell
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
import time
import weatherservice
from weatherservice import WeatherService
from comun import read_json_from_url
from comun import _

KEY = 'ea472f3ba2b2b77b'
# KEY = '6563686488165a78'
URL = 'http://api.wunderground.com/api/%s/conditions/forecast/\
lang:EN/pws:1/bestfct:1/q/%s,%s.json'
URL = 'http://api.wunderground.com/api/%s/conditions/forecast/\
lang:EN/pws:1/q/%s,%s.json'
URL2 = 'http://api.wunderground.com/api/%s/conditions/forecast/\
astronomy/satellite/lang:EN/pws:1/bestfct:1/q/%s,%s.json'


def gvfco(key, tree):
    if 'current_observation' in tree.keys():
        if key in tree['current_observation'].keys():
            return tree['current_observation'][key]
    return _('N/A')


def gvfi(key, tree):
    if 'current_observation' in tree.keys():
        if 'display_location' in tree['current_observation'].keys():
            if key in tree['current_observation']['display_location'].keys():
                return tree['current_observation']['display_location'][key]
    return _('N/A')


def gvff(key, day, tree):
    if 'forecast' in tree.keys():
        if 'simpleforecast' in tree['forecast'].keys():
            if 'forecastday' in tree['forecast']['simpleforecast'].keys():
                forecastday = tree['forecast']['simpleforecast']['forecastday']
                if len(forecastday) > day:
                    if key in forecastday[day].keys():
                        return forecastday[day][key]
    return _('N/A')


class UndergroundWeatherService(WeatherService):
    def __init__(self, longitude=-0.418, latitude=39.360,
                 units=weatherservice.Units(), key=KEY):
        WeatherService.__init__(self, longitude, latitude, units, key)

    def test_connection(self):
        try:
            parsed_json = read_json_from_url(URL % (self.key,
                                                    self.latitude,
                                                    self.longitude))
            if parsed_json is None:
                print('error found')
                return False
            return True
        except Exception as e:
            print(e)
        return False

    def _get_weather(self):
        weather_data = self.get_default_values()
        print('-------------------------------------------------------')
        print('-------------------------------------------------------')
        print('Underground Weather Service url: %s' % URL % (
            self.key, self.latitude, self.longitude))
        print('-------------------------------------------------------')
        print('-------------------------------------------------------')
        parsed_json = read_json_from_url(
            URL % (self.key, self.latitude, self.longitude))
        if parsed_json is None:
            return weather_data
        weather_data['update_time'] = time.time()
        weather_data['ok'] = True
        condition = gvfco('weather', parsed_json).lower()
        #
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
        temperature = cf.s2f(gvfco('temp_f', parsed_json))
        weather_data['current_conditions']['temperature'] =\
            cf.change_temperature(
                temperature, self.units.temperature)
        pressure = cf.s2f(gvfco('pressure_mb', parsed_json))
        weather_data['current_conditions']['pressure'] =\
            weatherservice.change_pressure(pressure, self.units.pressure)
        humidity = cf.s2f(
            gvfco('relative_humidity', parsed_json)[:-1])
        weather_data['current_conditions']['humidity'] = str(
            int(humidity)) + ' %'
        weather_data['current_conditions']['dew_point'] =\
            weatherservice.get_dew_point(
                humidity, temperature, self.units.temperature)
        wind_velocity = cf.s2f(gvfco('wind_mph', parsed_json))
        wind_direction = gvfco('wind_dir', parsed_json)
        weather_data['current_conditions']['wind_condition'] =\
            weatherservice.get_wind_condition(
                wind_velocity, wind_direction, self.units.wind)
        weather_data['current_conditions']['wind_icon'] =\
            weatherservice.get_wind_icon(wind_direction)
        #
        weather_data['current_conditions']['heat_index'] =\
            weatherservice.get_heat_index(temperature, humidity)
        weather_data['current_conditions']['windchill'] =\
            weatherservice.get_wind_chill(temperature, wind_velocity)
        #
        weather_data['current_conditions']['feels_like'] =\
            weatherservice.get_feels_like(
                temperature, humidity, wind_velocity, self.units.temperature)
        #
        weather_data['current_conditions']['visibility'] =\
            weatherservice.change_distance(
                gvfco('visibility_mi', parsed_json), self.units.visibility)
        weather_data['current_conditions']['solarradiation'] = gvfco(
            'solarradiation', parsed_json)
        weather_data['current_conditions']['UV'] = gvfco('UV', parsed_json)
        weather_data['current_conditions']['precip_1hr'] =\
            weatherservice.change_longitude(
                gvfco('precip_1hr_in', parsed_json), self.units.rain)
        weather_data['current_conditions']['precip_today'] =\
            weatherservice.change_longitude(
                gvfco('precip_today_in', parsed_json), self.units.rain)
        for i in range(0, 4):
            weather_data['forecasts'][i]['low'] =\
                cf.change_temperature(
                    gvff('low', i, parsed_json)['fahrenheit'],
                    self.units.temperature)
            weather_data['forecasts'][i]['high'] =\
                cf.change_temperature(
                    gvff('high', i, parsed_json)['fahrenheit'],
                    self.units.temperature)
            #
            weather_data['forecasts'][i]['qpf_allday'] =\
                weatherservice.change_longitude(
                    gvff('qpf_allday', i, parsed_json)['in'], self.units.rain)
            weather_data['forecasts'][i]['qpf_day'] =\
                weatherservice.change_longitude(
                    gvff('qpf_day', i, parsed_json)['in'], self.units.rain)
            weather_data['forecasts'][i]['qpf_night'] =\
                weatherservice.change_longitude(
                    gvff('qpf_night', i, parsed_json)['in'], self.units.rain)
            weather_data['forecasts'][i]['snow_allday'] =\
                weatherservice.change_longitude(
                    gvff('snow_allday', i, parsed_json)['in'], self.units.snow)
            weather_data['forecasts'][i]['snow_day'] =\
                weatherservice.change_longitude(
                    gvff('snow_day', i, parsed_json)['in'], self.units.snow)
            weather_data['forecasts'][i]['snow_night'] =\
                weatherservice.change_longitude(
                    gvff('snow_night', i, parsed_json)['in'], self.units.snow)
            wind = gvff('maxwind', i, parsed_json)
            weather_data['forecasts'][i]['maxwind'] =\
                weatherservice.get_wind_condition(
                    wind['mph'], wind['dir'], self.units.wind)
            wind = gvff('avewind', i, parsed_json)
            weather_data['forecasts'][i]['avewind'] =\
                weatherservice.get_wind_condition(
                    wind['mph'], wind['dir'], self.units.wind)
            weather_data['forecasts'][i]['avehumidity'] = '%s %%' % gvff(
                'avehumidity', i, parsed_json)
            weather_data['forecasts'][i]['maxhumidity'] = '%s %%' % gvff(
                'maxhumidity', i, parsed_json)
            weather_data['forecasts'][i]['minhumidity'] = '%s %%' % gvff(
                'minhumidity', i, parsed_json)
            #
            condition = gvff('conditions', i, parsed_json).lower()
            weather_data['forecasts'][i]['condition'] = condition
            weather_data['forecasts'][i]['condition_text'] =\
                weatherservice.get_condition(condition, 'text')
            weather_data['forecasts'][i]['condition_image'] =\
                weatherservice.get_condition(condition, 'image')
            weather_data['forecasts'][i]['condition_icon'] =\
                weatherservice.get_condition(condition, 'icon-light')
        weather_data['forecast_information']['city'] =\
            gvfi('city', parsed_json)
        weather_data['forecast_information']['postal_code'] =\
            gvfi('zip', parsed_json)
        weather_data['forecast_information']['latitude_e6'] =\
            gvfi('latitude', parsed_json)
        weather_data['forecast_information']['longitude_e6'] =\
            gvfi('longitude', parsed_json)
        return weather_data

    def get_weather(self):
        weather_data = None
        weather_data = self._get_weather()
        return weather_data


if __name__ == '__main__':
    import pprint
    uws = UndergroundWeatherService(longitude=-0.418, latitude=39.360)
    weather_data = uws.get_weather()
    pprint.pprint(weather_data)
    exit(0)
