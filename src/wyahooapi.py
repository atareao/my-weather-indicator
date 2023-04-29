#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A library for access to google weather api
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
import time
import weatherservice
from weatherservice import WeatherService
import geocodeapi
import requests
from requests_oauthlib import OAuth1
from requests.exceptions import SSLError


CODE = {}
CODE[0] = 'tornado'
CODE[1] = 'tropical storm'
CODE[2] = 'hurricane'
CODE[3] = 'severe thunderstorms'
CODE[4] = 'thunderstorms'
CODE[5] = 'mixed rain and snow'
CODE[6] = 'mixed rain and sleet'
CODE[7] = 'mixed snow and sleet'
CODE[8] = 'freezing drizzle'
CODE[9] = 'drizzle'
CODE[10] = 'freezing rain'
CODE[11] = 'showers'
CODE[12] = 'showers'
CODE[13] = 'snow flurries'
CODE[14] = 'light snow showers'
CODE[15] = 'blowing snow'
CODE[16] = 'snow'
CODE[17] = 'hail'
CODE[18] = 'sleet'
CODE[19] = 'dust'
CODE[20] = 'foggy'
CODE[21] = 'haze'
CODE[22] = 'smoky'
CODE[23] = 'blustery'
CODE[24] = 'windy'
CODE[25] = 'cold'
CODE[26] = 'cloudy'
CODE[27] = 'mostly cloudy'
CODE[28] = 'mostly cloudy'
CODE[29] = 'partly cloudy'
CODE[30] = 'partly cloudy'
CODE[31] = 'clear'
CODE[32] = 'sunny'
CODE[33] = 'fair'
CODE[34] = 'fair'
CODE[35] = 'mixed rain and hail'
CODE[36] = 'hot'
CODE[37] = 'isolated thunderstorms'
CODE[38] = 'scattered thunderstorms'
CODE[39] = 'scattered thunderstorms'
CODE[40] = 'scattered showers'
CODE[41] = 'heavy snow'
CODE[42] = 'scattered snow showers'
CODE[43] = 'heavy snow'
CODE[44] = 'partly cloudy'
CODE[45] = 'thundershowers'
CODE[46] = 'snow showers'
CODE[47] = 'isolated thundershowers'
CODE[3200] = 'not available'


class YahooWeatherService(WeatherService):

    def __init__(self,
                 longitude=-0.418,
                 latitude=39.360,
                 units=weatherservice.Units()):
        WeatherService.__init__(self, longitude, latitude, units)
        self.oauth = OAuth1("", "")
        self.woeid = geocodeapi.get_woeid(latitude, longitude)

    def run_query(self):
        q = 'select * from weather.forecast where woeid=%s' % self.woeid
        url = 'https://query.yahooapis.com/v1/yql?q=%s' % q
        params = {}
        params['format'] = 'json'
        try:
            ans = requests.get(url, auth=self.oauth, params=params)
        except SSLError as e:
            print('wyahooapi.py: Bug #1568774', str(e))
            print('wyahooapi.py: Unable to query https url, switch to http url')
            url = 'http://query.yahooapis.com/v1/yql?q=%s' % q
            ans = requests.get(url, auth=self.oauth, params=params)

        if ans.status_code == 200:
            return ans.json()
        else:
            print('wyahooapi.py: Request status code not 200, status_code = ', str(ans.status_code))
            return None

    def get_weather(self):
        weather_data = self.get_default_values()
        if self.woeid is None:
            self.woeid = geocodeapi.get_woeid(self.latitude, self.longitude)
            if self.woeid is None:
                print('wyahooapi.py: Yahoo Weather Service, not found woeid')
                return weather_data
        try:
            ans = self.run_query()
            if ans is None:
                print('wyahooapi.py: Yahoo Weather Service, query answer is None')
                return weather_data
            if 'query' not in list(ans.keys()):
                print('wyahooapi.py: Yahoo Weather Service, query answer has no element query')
                return weather_data
            if 'results' not in list(ans['query'].keys()):
                print('wyahooapi.py: Yahoo Weather Service, query answer has no element query.results')
                return weather_data
            if ans['query']['results'] is None:
                print('wyahooapi.py: Yahoo Weather Service, query answer query.results is None')
                return weather_data
            if 'channel' not in list(ans['query']['results'].keys()):
                print('wyahooapi.py: Yahoo Weather Service, query answer has no element query.results.channel')
                return weather_data

            weather_data['update_time'] = time.time()
            weather_data['ok'] = True
            data = ans['query']['results']['channel']
            temperature = cf.f2c_print(data['item']['condition']['temp'])
            velocity = cf.f2c_print(data['wind']['speed'])
            direction = cf.f2c_print(data['wind']['direction'])
            pressure = cf.f2c_print(data['atmosphere']['pressure'])
            visibility = cf.f2c_print(data['atmosphere']['visibility'])
            humidity = cf.f2c_print(data['atmosphere']['humidity'])
            condition = CODE[int(data['item']['condition']['code'])]
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
                cf.change_temperature(temperature, self.units.temperature)
            weather_data['current_conditions']['pressure'] =\
                weatherservice.change_pressure(pressure, self.units.pressure)
            weather_data['current_conditions']['humidity'] = '%s %%' %\
                (humidity)
            weather_data['current_conditions']['dew_point'] =\
                weatherservice.get_dew_point(humidity,
                                             temperature,
                                             self.units.temperature)
            wind_direction = weatherservice.degToCompass2(direction)
            weather_data['current_conditions']['wind_condition'] =\
                weatherservice.get_wind_condition2(velocity,
                                                   wind_direction[0],
                                                   self.units.wind)
            weather_data['current_conditions']['wind_icon'] = wind_direction[2]
            #
            weather_data['current_conditions']['heat_index'] =\
                weatherservice.get_heat_index(temperature, humidity)
            weather_data['current_conditions']['windchill'] =\
                weatherservice.get_wind_chill(temperature, velocity)
            #
            weather_data['current_conditions']['feels_like'] =\
                weatherservice.get_feels_like(temperature,
                                              humidity,
                                              velocity,
                                              self.units.temperature)
            #
            weather_data['current_conditions']['visibility'] =\
                weatherservice.change_distance(visibility,
                                               self.units.visibility)
            weather_data['current_conditions']['solarradiation'] = None
            weather_data['current_conditions']['UV'] = None
            weather_data['current_conditions']['precip_1hr'] = None
            weather_data['current_conditions']['precip_today'] = None
            for i, forecast_condition in enumerate(data['item']['forecast']):
                if i < 7:
                    tlow = cf.f2c_print(forecast_condition['low'])
                    thight = cf.f2c_print(forecast_condition['high'])
                    weather_data['forecasts'][i]['low'] =\
                        cf.change_temperature(tlow, self.units.temperature)
                    weather_data['forecasts'][i]['high'] =\
                        cf.change_temperature(thight, self.units.temperature)
                    #
                    weather_data['forecasts'][i]['qpf_allday'] = None
                    weather_data['forecasts'][i]['qpf_day'] = None
                    weather_data['forecasts'][i]['qpf_night'] = None
                    weather_data['forecasts'][i]['snow_allday'] = None
                    weather_data['forecasts'][i]['snow_day'] = None
                    weather_data['forecasts'][i]['snow_night'] = None
                    weather_data['forecasts'][i]['maxwind'] = None
                    weather_data['forecasts'][i]['avewind'] = None
                    weather_data['forecasts'][i]['avehumidity'] = None
                    weather_data['forecasts'][i]['maxhumidity'] = None
                    weather_data['forecasts'][i]['minhumidity'] = None
                    #
                    condition = CODE[int(forecast_condition['code'])]
                    weather_data['forecasts'][i]['condition'] = condition
                    weather_data['forecasts'][i]['condition_text'] =\
                        weatherservice.get_condition(condition, 'text')
                    weather_data['forecasts'][i]['condition_image'] =\
                        weatherservice.get_condition(condition, 'image')
                    weather_data['forecasts'][i]['condition_icon'] =\
                        weatherservice.get_condition(condition, 'icon-light')
        except Exception as e:
            print('wyahooapi.py: error:', str(e))
        return weather_data


if __name__ == "__main__":
    import pprint
    longitude = -0.418
    latitude = 39.360
    yws = YahooWeatherService(longitude=longitude, latitude=latitude)
    print(yws.woeid)
    ans = yws.get_weather()
    pprint.pprint(ans)
    exit(0)
