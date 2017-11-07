#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
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
#
#
import time
import weatherservice
from weatherservice import WeatherService
from weatherservice import change_temperature
import geocodeapi
from comun import _
import requests
from requests_oauthlib import OAuth1
from requests.exceptions import SSLError

API_KEY = 'dj0yJmk9djNkNk5hRUZNODFCJmQ9WVdrOWVEbFVXRWxITTJVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZW\
NyZXQmeD1jMQ--'
SHARED_SECRET = '27dcb39434d1ee95b90e5f3a7e227d3992ecd573'

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


def s2f(word):
    try:
        return float(word)
    except Exception as e:
        print(e)
    return 0


class YahooWeatherService(WeatherService):

    def __init__(self,
                 longitude=-0.418,
                 latitude=39.360,
                 units=weatherservice.Units()):
        WeatherService.__init__(self, longitude, latitude, units)
        self.oauth = OAuth1(API_KEY, SHARED_SECRET)
        self.woeid = geocodeapi.get_woeid(latitude, longitude)

    def run_query(self):
        q = 'select * from weather.forecast where woeid=%s' % self.woeid
        url = 'https://query.yahooapis.com/v1/yql?q=%s' % q
        params = {}
        params['format'] = 'json'
        try:
            ans = requests.get(url, auth=self.oauth, params=params)
        except SSLError as e:
            '''
            Bug #1568774
            '''
            print('Bug #1568774', str(e))
            url = 'http://query.yahooapis.com/v1/yql?q=%s' % q
            ans = requests.get(url, auth=self.oauth, params=params)
        if ans.status_code == 200:
            return ans.json()
        return None

    def get_weather(self):
        weather_data = self.get_default_values()
        if self.woeid is None:
            self.woeid = geocodeapi.get_woeid(self.latitude, self.longitude)
            if self.woeid is None:
                print('Yahoo Weather Service, not found woeid')
                return weather_data
        try:
            ans = self.run_query()
            if ans is None or\
                    'query' not in ans.keys() or\
                    'results' not in ans['query'].keys() or\
                    'channel' not in ans['query']['results'].keys():
                return weather_data
            weather_data['update_time'] = time.time()
            weather_data['ok'] = True
            data = ans['query']['results']['channel']
            temperature = s2f(data['item']['condition']['temp'])
            velocity = s2f(data['wind']['speed'])
            direction = s2f(data['wind']['direction'])
            pressure = s2f(data['atmosphere']['pressure'])
            visibility = s2f(data['atmosphere']['visibility'])
            humidity = s2f(data['atmosphere']['humidity'])
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
                weatherservice.change_temperature(temperature,
                                                  self.units.temperature)
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
                    tlow = s2f(forecast_condition['low'])
                    thight = s2f(forecast_condition['high'])
                    weather_data['forecasts'][i]['low'] =\
                        change_temperature(tlow,
                                           self.units.temperature)
                    weather_data['forecasts'][i]['high'] =\
                        change_temperature(thight,
                                           self.units.temperature)
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
            print(e)
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
