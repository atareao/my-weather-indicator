#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#
# A library for access to noaa weather api
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
from lxml import etree
import weatherservice
from  weatherservice import WeatherService

from comun import _

NOAA_WEATHER_URL  = 'http://forecast.weather.gov/MapClick.php?lat=%s&lon=%s&FcstType=dwml'

def download_xml(url):
	print('URL: %s'%url)
	handler = urllib2.urlopen(urllib2.Request(url, headers={'User-Agent' : 'Magic Browser'}))
	xml_response = handler.read()
	handler.close()
	return xml_response

def get_text(root,path):	
	r = root.xpath(path)
	if len(r)>0:
		return r[0].text
	return None

def get_data(root,path):	
	r = root.xpath(path)
	if len(r)>0:
		return r[0].attrib['data']
	return None
	
class NOAAWeatherService(WeatherService):
	def __init__(self,longitude=-0.418, latitude=39.360, units = weatherservice.Units()):
		WeatherService.__init__(self,longitude,latitude,units)
		self.url = NOAA_WEATHER_URL % (self.latitude,self.longitude)

	def get_weather(self):
		weather_data = self.get_default_values()
		xml_response = download_xml(self.url)		
		root = etree.fromstring(xml_response).xpath('/data/parameters/temperature')
		try:
			#
			xml_response = download_xml(self.url)		
			root = etree.fromstring(xml_response).xpath('/data/parameters/temperature')
			if len(root) == 0:
				raise urllib2.URLError('Root 0')
			temperature = get_data(root[0],'temp_f')
			velocity = get_data(root[0],'wind_condition')
			velocity = weatherservice.s2f(velocity.split(' ')[3])
			humidity = weatherservice.get_humidity(get_data(root[0],'humidity'))
			condition = get_data(root[0],'condition').lower()
			weather_data['current_conditions']['condition'] = condition
			weather_data['current_conditions']['condition_text'] = weatherservice.get_condition(condition,'text')
			if weatherservice.is_day_now(weather_data['current_conditions']['sunrise_time'],weather_data['current_conditions']['sunset_time']):
				weather_data['current_conditions']['condition_image'] = weatherservice.get_condition(condition,'image')
				weather_data['current_conditions']['condition_icon_dark'] = weatherservice.get_condition(condition,'icon-dark')
				weather_data['current_conditions']['condition_icon_light'] = weatherservice.get_condition(condition,'icon-light')
			else:
				weather_data['current_conditions']['condition_image'] = weatherservice.get_condition(condition,'image-night')
				weather_data['current_conditions']['condition_icon_dark'] = weatherservice.get_condition(condition,'icon-night-dark')
				weather_data['current_conditions']['condition_icon_light'] = weatherservice.get_condition(condition,'icon-night-light')
			weather_data['current_conditions']['temperature'] = weatherservice.change_temperature(temperature,self.units.temperature)
			weather_data['current_conditions']['pressure'] = None
			weather_data['current_conditions']['humidity'] = '%s %%'%(humidity)
			weather_data['current_conditions']['dew_point'] = weatherservice.get_dew_point(humidity,temperature,self.units.temperature)
			wind =get_data(root[0],'wind_condition')
			wind_direction = wind.split(' ')[1]
			wind_direction = wind_direction.lower()
			wind_velocity = wind.split(' ')
			weather_data['current_conditions']['wind_condition'] = weatherservice.get_wind_condition(wind_velocity,wind_direction,self.units.wind)
			#
			weather_data['current_conditions']['heat_index'] = weatherservice.get_heat_index(temperature,humidity)
			weather_data['current_conditions']['windchill'] = weatherservice.get_wind_chill(temperature,wind_velocity)
			#
			weather_data['current_conditions']['feels_like'] = weatherservice.get_feels_like(temperature,humidity,velocity,self.units.temperature)
			#
			weather_data['current_conditions']['visibility'] = None
			weather_data['current_conditions']['solarradiation'] = None
			weather_data['current_conditions']['UV'] = None
			weather_data['current_conditions']['precip_1hr'] = None
			weather_data['current_conditions']['precip_today'] = None
			#
			root = etree.fromstring(xml_response).xpath('/xml_api_reply/weather/forecast_conditions')
			for i,el in enumerate(root):
				weather_data['forecasts'][i]['low'] = weatherservice.change_temperature(get_data(el,'low'),self.units.temperature)
				weather_data['forecasts'][i]['high'] = weatherservice.change_temperature(get_data(el,'high'),self.units.temperature)
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
				condition = get_data(el,'condition').lower()
				weather_data['forecasts'][i]['condition'] = condition
				weather_data['forecasts'][i]['condition_text'] = weatherservice.get_condition(condition,'text')
				weather_data['forecasts'][i]['condition_image'] = weatherservice.get_condition(condition,'image')
				weather_data['forecasts'][i]['condition_icon'] = weatherservice.get_condition(condition,'icon-light')				
			#
			root = etree.fromstring(xml_response).xpath('/xml_api_reply/weather/forecast_information')
			forecast_information = {}
			weather_data['forecast_information']['city'] = get_data(root[0],'city')
			weather_data['forecast_information']['postal_code'] = get_data(root[0],'postal_code')
			weather_data['forecast_information']['latitude_e6'] = get_data(root[0],'latitude_e6')
			weather_data['forecast_information']['longitude_e6'] = get_data(root[0],'longitude_e6')
			weather_data['forecast_information']['forecast_date'] = get_data(root[0],'forecast_date')
			weather_data['forecast_information']['current_date_time'] = get_data(root[0],'current_date_time')
			weather_data['forecast_information']['unit_system'] = get_data(root[0],'unit_system')
			return weather_data
		except Exception as e:
			print(e)
		return weather_data
			

if __name__ == "__main__":
	lat,lon = 33.766700, -118.191420
	#lat,lon = 52.229958,21.013653
	#lat,lon = 51.769191,19.434658
	#lat = 49.9026653
	#lon = 18.8278352
	ggw = NOAAWeatherService(longitude=lon,latitude=lat)
	print(ggw.get_weather())
	exit(0)
