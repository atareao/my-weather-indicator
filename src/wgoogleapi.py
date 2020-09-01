#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of my-weather-indicator
#
# Copyright (c) 2012 Lorenzo Carbonell Cerezo <a.k.a. atareao>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import utils as cf
import time
from lxml import etree
import geocodeapi
import weatherservice
import html.entities
from weatherservice import WeatherService
from comun import read_from_url

GOOGLE_WEATHER_URL = "http://www.google.com/ig/api?weather=%s&hl=en"
GOOGLE_WEATHER_URL2 = 'http://www.google.com/ig/api?weather=,,,%s,%s&hl=en'


def unicode2html(str):
    """translate any unicode or upper ascii char by its html entity"""
    ret = ""
    for char in str:
        if ord(char) > 127:
            try:
                ret = ret + "&" +\
                    html.entities.codepoint2name[ord(char)] + ";"
            except BaseException:
                ret = ret + '?'
        else:
            ret = ret + char
    return ret


def download_xml(url):
    url = unicode2html(url)
    url = url.replace(" ", "%20")
    print('URL: %s' % url)
    xml_response = read_from_url(url)
    return xml_response


def get_text(root, path):
    r = root.xpath(path)
    if len(r) > 0:
        return r[0].text
    return None


def get_data(root, path):
    r = root.xpath(path)
    if len(r) > 0:
        return r[0].attrib['data']
    return None


class GoogleWeatherService(WeatherService):

    def __init__(self, longitude=-0.418, latitude=39.360,
                 units=weatherservice.Units()):
        WeatherService.__init__(self, longitude, latitude, units)
        self.search_string = geocodeapi.get_inv_direction(
            latitude, longitude)['search_string']
        self.search_string = unicode2html(self.search_string)
        self.latlontrouble = False
        self.url1 = GOOGLE_WEATHER_URL % (self.search_string)
        self.url2 = GOOGLE_WEATHER_URL2 % (
            int(self.latitude * 1000000), int(self.longitude * 1000000))

    def get_weather(self):
        weather_data = self.get_default_values()
        if self.latlontrouble:
            temp = self.url2
            self.url2 = self.url1
            self.url1 = temp
            self.latlontrouble = False
        for i in range(0, 6):
            if i < 3:
                URL = self.url1
                self.latlontrouble = False
            else:
                URL = self.url2
                self.latlontrouble = True
            try:
                #
                xml_response = download_xml(URL)
                root = etree.fromstring(xml_response).xpath(
                    '/xml_api_reply/weather/current_conditions')
                if len(root) == 0:
                    raise Exception('Root 0')
                temperature = get_data(root[0], 'temp_f')
                velocity = get_data(root[0], 'wind_condition')
                velocity = cf.s2f(velocity.split(' ')[3])
                humidity = weatherservice.get_humidity(
                    get_data(root[0], 'humidity'))
                condition = get_data(root[0], 'condition').lower()
                weather_data['current_conditions']['condition'] = condition
                weather_data['current_conditions']['condition_text'] = \
                    weatherservice.get_condition(condition, 'text')
                if weatherservice.is_day_now(
                        weather_data['current_conditions']['sunrise_time'],
                        weather_data['current_conditions']['sunset_time']):
                    weather_data['current_conditions']['condition_image'] = \
                        weatherservice.get_condition(condition, 'image')
                    weather_data['current_conditions']['condition_icon_dark'] = weatherservice.get_condition(condition, 'icon-dark')
                    weather_data['current_conditions']['condition_icon_light'] = weatherservice.get_condition(condition, 'icon-light')
                else:
                    weather_data['current_conditions']['condition_image'] = \
                        weatherservice.get_condition(condition, 'image-night')
                    weather_data['current_conditions']['condition_icon_dark'] = weatherservice.get_condition(condition, 'icon-night-dark')
                    weather_data['current_conditions']['condition_icon_light'] = weatherservice.get_condition(condition, 'icon-night-light')
                weather_data['current_conditions']['temperature'] = \
                    cf.change_temperature(temperature, self.units.temperature)
                weather_data['current_conditions']['pressure'] = None
                weather_data['current_conditions']['humidity'] = '%s %%' % (humidity)
                weather_data['current_conditions']['dew_point'] = weatherservice.get_dew_point(humidity, temperature, self.units.temperature)
                wind = get_data(root[0], 'wind_condition')
                wind_direction = wind.split(' ')[1]
                wind_direction = wind_direction.lower()
                wind_velocity = wind.split(' ')
                weather_data['current_conditions']['wind_condition'] = weatherservice.get_wind_condition(wind_velocity, wind_direction, self.units.wind)
                #
                weather_data['current_conditions']['heat_index'] = weatherservice.get_heat_index(temperature, humidity)
                weather_data['current_conditions']['windchill'] = weatherservice.get_wind_chill(temperature, wind_velocity)
                #
                weather_data['current_conditions']['feels_like'] = weatherservice.get_feels_like(temperature, humidity, velocity, self.units.temperature)
                #
                weather_data['current_conditions']['visibility'] = None
                weather_data['current_conditions']['solarradiation'] = None
                weather_data['current_conditions']['UV'] = None
                weather_data['current_conditions']['precip_1hr'] = None
                weather_data['current_conditions']['precip_today'] = None
                #
                root = etree.fromstring(xml_response).xpath('/xml_api_reply/weather/forecast_conditions')
                for i, el in enumerate(root):
                    weather_data['forecasts'][i]['low'] = cf.change_temperature(get_data(el, 'low'), self.units.temperature)
                    weather_data['forecasts'][i]['high'] = cf.change_temperature(get_data(el, 'high'), self.units.temperature)
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
                    condition = get_data(el, 'condition').lower()
                    weather_data['forecasts'][i]['condition'] = condition
                    weather_data['forecasts'][i]['condition_text'] = weatherservice.get_condition(condition, 'text')
                    weather_data['forecasts'][i]['condition_image'] = weatherservice.get_condition(condition, 'image')
                    weather_data['forecasts'][i]['condition_icon'] = weatherservice.get_condition(condition, 'icon-light')
                #
                root = etree.fromstring(xml_response).xpath('/xml_api_reply/weather/forecast_information')
                weather_data['forecast_information']['city'] = get_data(root[0], 'city')
                weather_data['forecast_information']['postal_code'] = get_data(root[0], 'postal_code')
                weather_data['forecast_information']['latitude_e6'] = get_data(root[0], 'latitude_e6')
                weather_data['forecast_information']['longitude_e6'] = get_data(root[0], 'longitude_e6')
                weather_data['forecast_information']['forecast_date'] = get_data(root[0], 'forecast_date')
                weather_data['forecast_information']['current_date_time'] = get_data(root[0], 'current_date_time')
                weather_data['forecast_information']['unit_system'] = get_data(root[0], 'unit_system')
                return weather_data
            except Exception as e:
                time.sleep(1)
                if i > 3:
                    print(e)
        return weather_data


if __name__ == "__main__":
    lat, lon = 33.766700, -118.191420
    # lat,lon = 52.229958,21.013653
    # lat,lon = 51.769191,19.434658
    ggw = GoogleWeatherService(longitude=lon, latitude=lat)
    print(ggw.get_weather())
    print(ggw.get_weather())
    exit(0)
