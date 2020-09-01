#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
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

import os
import gi
try:
    gi.require_version('GLib', '2.0')
    gi.require_version('AppIndicator3', '0.1')
    gi.require_version('Gtk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
    gi.require_version('Notify', '0.7')
    gi.require_version('GeocodeGlib', '1.0')
    gi.require_version('WebKit2', '4.0')
except Exception as e:
    print(e)
    print('Repository version required not present')
    exit(1)
from gi.repository import GLib
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Notify
from gi.repository import GObject
import time
import preferences
import dbus
import webbrowser
from datetime import datetime
from forecastw import FC
from openweathermap import ForecastMap
from configurator import Configuration
import ipaddress
import geocodeapi
import comun
import weatherservice
import worldweatheronlineapi
import wopenweathermapapi
import wyahooapi
import wundergroundapi
import machine_information
from graph import Graph
from comun import _
from comun import internet_on
from weatherwidget import WeatherWidget
from mooncalendarwindow import CalendarWindow
from comun import CSS_FILE
from utils import load_css

INDICATORS = 2
TIME_TO_CHECK = 15


class MWI(GObject.Object):
    __gsignals__ = {
        'internet-out': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'internet-in': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'update-weather': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'update-widgets': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        GObject.Object.__init__(self)
        if dbus.SessionBus().request_name('es.atareao.MyWeatherIndicator') !=\
                dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
            print("application already running")
            exit(0)
        #
        self.weather_updater = 0
        self.widgets_updater = 0
        self.internet_updater = 0
        self.internet_connection = False
        self.menus = []
        self.indicators = []
        self.notifications = []
        self.widgets = []
        self.weatherservices = []
        self.weathers = []
        self.current_conditions = []
        self.preferences = []
        self.last_update_time = 0
        # Iniciate variables
        for i in range(INDICATORS):
            self.menus.append(None)
            self.indicators.append(None)
            self.notifications.append(None)
            self.widgets.append(None)
            self.weatherservices.append(None)
            self.weathers.append(None)
            self.current_conditions.append(None)
            self.preferences.append(None)
        #
        status = appindicator.IndicatorCategory.APPLICATION_STATUS
        self.notifications[0] = Notify.Notification.new('', '', None)
        self.indicators[0] = appindicator.Indicator.new(
            'My-Weather-Indicator', 'My-Weather-Indicator', status)
        self.notifications[1] = Notify.Notification.new('', '', None)
        self.indicators[1] = appindicator.Indicator.new(
            'My-Weather-Indicator2', 'My-Weather-Indicator', status)
        for i in range(INDICATORS):
            self.create_menu(i)
        for i in range(INDICATORS):
            self.widgets[i] = None
        self.load_preferences()

    def update_widgets(self):
        update = False
        utcnow = datetime.utcnow()
        for i in range(INDICATORS):
            if self.widgets[i] is not None:
                self.widgets[i].set_datetime(utcnow)
                update = True
        return update

    def update_weather(self):
        print('***** refreshing weather *****')
        for i in range(INDICATORS):
            if self.preferences[i]['show']:
                self.update_menu(i)
                self.indicators[i].set_status(
                    appindicator.IndicatorStatus.ACTIVE)
            else:
                self.indicators[i].set_status(
                    appindicator.IndicatorStatus.PASSIVE)
        return True

    def get_help_menu(self):
        help_menu = Gtk.Menu()
        #
        homepage_item = Gtk.MenuItem(label=_(
            'Homepage'))
        homepage_item.connect('activate',
                              lambda x: webbrowser.open('http://www.atareao.es\
/apps/my-weather-indicator-para-ubuntu/'))
        homepage_item.show()
        help_menu.append(homepage_item)
        #
        help_item = Gtk.MenuItem(label=_(
            'Get help online...'))
        help_item.connect('activate',
                          lambda x: webbrowser.open('http://www.atareao.es\
/apps/my-weather-indicator-para-ubuntu/'))
        help_item.show()
        help_menu.append(help_item)
        #
        translate_item = Gtk.MenuItem(label=_(
            'Translate this application...'))
        translate_item.connect(
            'activate',
            lambda x: webbrowser.open('http://www.atareao.es/apps/\
my-weather-indicator-para-ubuntu/'))
        translate_item.show()
        help_menu.append(translate_item)
        #
        bug_item = Gtk.MenuItem(label=_(
            'Report a bug...'))
        bug_item.connect('activate',
                         lambda x: webbrowser.open('https://github.com/atareao\
/my-weather-indicator/issues'))
        bug_item.show()
        help_menu.append(bug_item)
        #
        separator = Gtk.SeparatorMenuItem()
        separator.show()
        help_menu.append(separator)
        #
        twitter_item = Gtk.MenuItem(label=_(
            'Follow me in Twitter'))
        twitter_item.connect(
            'activate',
            lambda x: webbrowser.open('https://twitter.com/atareao'))
        twitter_item.show()
        help_menu.append(twitter_item)
        #
        googleplus_item = Gtk.MenuItem(label=_(
            'Follow me in Google+'))
        googleplus_item.connect('activate',
                                lambda x: webbrowser.open(
                                    'https://plus.google.com/\
118214486317320563625/posts'))
        googleplus_item.show()
        help_menu.append(googleplus_item)
        #
        facebook_item = Gtk.MenuItem(label=_(
            'Follow me in Facebook'))
        facebook_item.connect(
            'activate',
            lambda x: webbrowser.open('http://www.facebook.com/elatareao'))
        facebook_item.show()
        help_menu.append(facebook_item)
        #
        about_item = Gtk.MenuItem.new_with_label(_('About'))
        about_item.connect('activate', self.menu_about_response)
        about_item.show()
        separator = Gtk.SeparatorMenuItem()
        separator.show()
        help_menu.append(separator)
        help_menu.append(about_item)
        #
        help_menu.show()
        return help_menu

    def load_preferences(self):
        if not os.path.exists(comun.CONFIG_FILE):
            if internet_on():
                configuration = Configuration()
                configuration.reset()
                latitude, longitude = ipaddress.get_current_location()
                city = geocodeapi.get_inv_direction(
                    latitude, longitude)['city']
                if city is None:
                    city = ''
                configuration.set('latitude', latitude)
                configuration.set('longitude', longitude)
                configuration.set('location', city)
                configuration.save()
            cm = preferences.CM()
            if cm.run() == Gtk.ResponseType.ACCEPT:
                cm.save_preferences()
            else:
                exit(0)
            cm.hide()
            cm.destroy()
        configuration = Configuration()
        self.first_time = configuration.get('first-time')
        self.refresh = configuration.get('refresh')
        self.version = configuration.get('version')
        #
        self.preferences[0] = {}
        self.preferences[0]['show'] = configuration.get('main-location')
        self.preferences[0]['autolocation'] = configuration.get('autolocation')
        self.preferences[0]['location'] = configuration.get('location')
        self.preferences[0]['latitude'] = configuration.get('latitude')
        self.preferences[0]['longitude'] = configuration.get('longitude')
        self.preferences[0]['show-temperature'] =\
            configuration.get('show-temperature')
        self.preferences[0]['show-notifications'] =\
            configuration.get('show-notifications')
        self.preferences[0]['widget'] = configuration.get('widget1')
        #
        self.preferences[1] = {}
        self.preferences[1]['show'] = configuration.get('second-location')
        self.preferences[1]['autolocation'] = False
        self.preferences[1]['location'] = configuration.get('location2')
        self.preferences[1]['latitude'] = configuration.get('latitude2')
        self.preferences[1]['longitude'] = configuration.get('longitude2')
        self.preferences[1]['show-temperature'] =\
            configuration.get('show-temperature2')
        self.preferences[1]['show-notifications'] =\
            configuration.get('show-notifications2')
        self.preferences[1]['widget'] = configuration.get('widget2')
        #
        temperature = configuration.get('temperature')
        pressure = configuration.get('pressure')
        visibility = configuration.get('visibility')
        wind = configuration.get('wind')
        snow = configuration.get('snow')
        rain = configuration.get('rain')
        ampm = not configuration.get('24h')
        self.units = weatherservice.Units(temperature=temperature,
                                          wind=wind,
                                          pressure=pressure,
                                          visibility=visibility,
                                          snow=snow,
                                          rain=rain,
                                          ampm=ampm)
        self.ws = configuration.get('weather-service')
        if self.ws == 'yahoo':
            self.key = ''
            for i in range(INDICATORS):
                if self.preferences[i]['show']:
                    self.weatherservices[i] = wyahooapi.YahooWeatherService(
                        longitude=self.preferences[i]['longitude'],
                        latitude=self.preferences[i]['latitude'],
                        units=self.units)
                self.menus[i]['evolution'].hide()
        elif self.ws == 'worldweatheronline':
            self.key = configuration.get('wwo-key')
            for i in range(INDICATORS):
                if self.preferences[i]['show']:
                    self.weatherservices[i] =\
                        worldweatheronlineapi.WorldWeatherOnlineService(
                            longitude=self.preferences[i]['longitude'],
                            latitude=self.preferences[i]['latitude'],
                            units=self.units,
                            key=self.key)
                self.menus[i]['evolution'].hide()
        elif self.ws == 'openweathermap':
            self.key = ''
            for i in range(INDICATORS):
                if self.preferences[i]['show']:
                    self.weatherservices[i] =\
                        wopenweathermapapi.OWMWeatherService(
                            longitude=self.preferences[i]['longitude'],
                            latitude=self.preferences[i]['latitude'],
                            units=self.units)
                self.menus[i]['evolution'].show()
        elif self.ws == 'wunderground':
            self.key = configuration.get('wu-key')
            for i in range(INDICATORS):
                if self.preferences[i]['show']:
                    self.weatherservices[i] =\
                        wundergroundapi.UndergroundWeatherService(
                            longitude=self.preferences[i]['longitude'],
                            latitude=self.preferences[i]['latitude'],
                            units=self.units,
                            key=self.key)
                self.menus[i]['evolution'].hide()

        #
        self.icon_light = configuration.get('icon-light')
        #
        utcnow = datetime.utcnow()
        for i in range(INDICATORS):
            if self.preferences[i]['show'] and\
                    self.preferences[i]['widget']:
                if self.widgets[i] is not None:
                    self.widgets[i].hide()
                    self.widgets[i].destroy()
                    self.widgets[i] = None
                self.widgets[i] = WeatherWidget(self.indicators[i], i)
                self.widgets[i].set_datetime(utcnow)
                self.widgets[i].set_location(self.preferences[i]['location'])
                self.widgets[i].connect('pinit', self.on_pinit, i)
            elif self.widgets[i] is not None:
                self.widgets[i].hide()
                self.widgets[i].destroy()
                self.widgets[i] = None
        print(1)
        self.update_weather()
        self.start_looking_for_internet()

    def start_widgets_updater(self):
        if self.widgets_updater > 0:
            GLib.source_remove(self.widgets_updater)
        self.update_widgets()
        self.widgets_updater = GLib.timeout_add(500,
                                                self.update_widgets)

    def stop_widgets_updater(self):
        if self.widgets_updater > 0:
            GLib.source_remove(self.widgets_updater)
            self.widgets_updater = 0

    def start_weather_updater(self):
        if self.weather_updater > 0:
            GLib.source_remove(self.weather_updater)
        self.update_weather()
        self.weather_updater = GLib.timeout_add_seconds(self.refresh * 3600,
                                                        self.update_weather)

    def stop_weather_updater(self):
        if self.weather_updater > 0:
            GLib.source_remove(self.weather_updater)
            self.weather_updater = 0

    def start_looking_for_internet(self):
        if self.internet_updater > 0:
            GLib.source_remove(self.internet_updater)
        if self.looking_for_internet():
            self.internet_updater = GLib.timeout_add_seconds(
                TIME_TO_CHECK, self.looking_for_internet)

    def stop_looking_for_internet(self):
        if self.internet_updater > 0:
            GLib.source_remove(self.internet_updater)
            self.internet_updater = 0

    def looking_for_internet(self):
        print('*** Looking For Internet ***')
        if internet_on():
            print('*** Internet Found ***')
            self.stop_looking_for_internet()
            self.start_weather_updater()
            self.start_widgets_updater()
            return False
        print('*** Internet Not Found ***')
        self.stop_weather_updater()
        self.stop_widgets_updater()
        return True

    def on_pinit(self, widget, data, index):
        utcnow = datetime.utcnow()
        self.widgets[index].is_above = not self.widgets[index].is_above
        weather = self.widgets[index].weather_data
        self.widgets[index].save_preferences()
        self.widgets[index].hide()
        self.widgets[index].destroy()
        self.widgets[index] = None
        self.widgets[index] = WeatherWidget(self.indicators[index], index)
        self.widgets[index].set_datetime(utcnow)
        self.widgets[index].set_location(self.preferences[index]['location'])
        self.widgets[index].connect('pinit', self.on_pinit, index)
        self.widgets[index].set_weather(weather)

    def create_menu(self, index):
        self.menus[index] = {}
        main_menu = Gtk.Menu()
        #
        self.menus[index]['forecast'] = Gtk.MenuItem(
            label=_('Forecast'))
        self.menus[index]['forecast'].connect(
            'activate', self.menu_forecast_response, index)
        self.menus[index]['forecast'].show()
        main_menu.append(self.menus[index]['forecast'])
        #
        self.menus[index]['evolution'] = Gtk.MenuItem(
            label=_('Evolution'))
        self.menus[index]['evolution'].connect(
            'activate', self.menu_evolution_response, index)
        self.menus[index]['evolution'].show()
        main_menu.append(self.menus[index]['evolution'])
        #
        self.menus[index]['forecastmap'] = Gtk.MenuItem(
            label=_('Forecast Map'))
        self.menus[index]['forecastmap'].connect(
            'activate', self.menu_forecast_map_response, index)
        self.menus[index]['forecastmap'].show()
        main_menu.append(self.menus[index]['forecastmap'])

        self.menus[index]['moon_calendar'] = Gtk.ImageMenuItem(
            label=_('Moon Phase Calendar'))
        self.menus[index]['moon_calendar'].set_image(
            Gtk.Image.new_from_file(
                os.path.join(comun.IMAGESDIR, 'mwig-clear-night.png')))
        self.menus[index]['moon_calendar'].set_always_show_image(True)
        self.menus[index]['moon_calendar'].connect(
            'activate', self.on_moon_clicked)
        self.menus[index]['moon_calendar'].show()
        main_menu.append(self.menus[index]['moon_calendar'])

        self.menus[index]['update'] = Gtk.MenuItem(
            label=_('Update weather'))
        self.menus[index]['update'].connect(
            'activate', self.menu_refresh_weather_response, index)
        self.menus[index]['update'].show()
        main_menu.append(self.menus[index]['update'])
        #
        separator = Gtk.SeparatorMenuItem()
        separator.show()
        main_menu.append(separator)
        #
        self.menus[index]['location'] = Gtk.MenuItem(
            label=_('Location'))
        self.menus[index]['location'].show()
        main_menu.append(self.menus[index]['location'])
        #
        self.menus[index]['temperature'] = Gtk.MenuItem(
            label=_('Temperature'))
        self.menus[index]['temperature'].show()
        main_menu.append(self.menus[index]['temperature'])
        #
        self.menus[index]['pressure'] = Gtk.MenuItem(
            label=_('Pressure'))
        self.menus[index]['pressure'].show()
        main_menu.append(self.menus[index]['pressure'])
        #
        self.menus[index]['humidity'] = Gtk.MenuItem(
            label=_('Humidity'))
        self.menus[index]['humidity'].show()
        main_menu.append(self.menus[index]['humidity'])
        #
        self.menus[index]['feels_like'] = Gtk.MenuItem(
            label=_('Feels like'))
        self.menus[index]['feels_like'].show()
        main_menu.append(self.menus[index]['feels_like'])
        #
        self.menus[index]['dew_point'] = Gtk.MenuItem(
            label=_('Dew Point'))
        self.menus[index]['dew_point'].show()
        main_menu.append(self.menus[index]['dew_point'])
        #
        self.menus[index]['wind'] = Gtk.ImageMenuItem(
            label=_('Wind'))
        self.menus[index]['wind'].set_always_show_image(True)
        self.menus[index]['wind'].show()
        main_menu.append(self.menus[index]['wind'])
        #
        self.menus[index]['visibility'] = Gtk.MenuItem(
            label=_('Visibility'))
        self.menus[index]['visibility'].show()
        main_menu.append(self.menus[index]['visibility'])
        #
        self.menus[index]['cloudiness'] = Gtk.MenuItem(
            label=_('Cloudiness'))
        self.menus[index]['cloudiness'].show()
        main_menu.append(self.menus[index]['cloudiness'])
        #
        self.menus[index]['uv'] = Gtk.MenuItem(
            label=_('UV'))
        self.menus[index]['uv'].show()
        main_menu.append(self.menus[index]['uv'])
        #
        self.menus[index]['precipitation'] = Gtk.MenuItem(
            label=_('Precipitation'))
        self.menus[index]['precipitation'].show()
        main_menu.append(self.menus[index]['precipitation'])
        #
        self.menus[index]['condition'] = Gtk.ImageMenuItem(
            label=_(''))
        self.menus[index]['condition'].set_always_show_image(True)
        self.menus[index]['condition'].show()
        main_menu.append(self.menus[index]['condition'])
        #
        separator = Gtk.SeparatorMenuItem()
        separator.show()
        main_menu.append(separator)
        #
        self.menus[index]['dawn'] = Gtk.ImageMenuItem(
            label=_('Dawn'))
        self.menus[index]['dawn'].set_image(
            Gtk.Image.new_from_file(
                os.path.join(comun.IMAGESDIR, 'mwig-clear.png')))
        self.menus[index]['dawn'].set_always_show_image(True)
        self.menus[index]['dawn'].show()
        main_menu.append(self.menus[index]['dawn'])
        #
        self.menus[index]['sunrise'] = Gtk.ImageMenuItem(
            label=_('Sunrise'))
        self.menus[index]['sunrise'].set_image(
            Gtk.Image.new_from_file(
                os.path.join(comun.IMAGESDIR, 'mwig-clear.png')))
        self.menus[index]['sunrise'].set_always_show_image(True)
        self.menus[index]['sunrise'].show()
        main_menu.append(self.menus[index]['sunrise'])
        #
        self.menus[index]['sunset'] = Gtk.ImageMenuItem(
            label=_('Sunset'))
        self.menus[index]['sunset'].set_image(
            Gtk.Image.new_from_file(
                os.path.join(comun.IMAGESDIR, 'mwig-clear-night.png')))
        self.menus[index]['sunset'].set_always_show_image(True)
        self.menus[index]['sunset'].show()
        main_menu.append(self.menus[index]['sunset'])
        #
        self.menus[index]['dusk'] = Gtk.ImageMenuItem(
            label=_('Dusk'))
        self.menus[index]['dusk'].set_image(
            Gtk.Image.new_from_file(
                os.path.join(comun.IMAGESDIR, 'mwig-clear-night.png')))
        self.menus[index]['dusk'].set_always_show_image(True)
        self.menus[index]['dusk'].show()
        main_menu.append(self.menus[index]['dusk'])
        #
        separator = Gtk.SeparatorMenuItem()
        separator.show()
        main_menu.append(separator)
        #
        self.menus[index]['moon_phase'] = Gtk.ImageMenuItem(
            label=_(''))
        self.menus[index]['moon_phase'].set_image(
            Gtk.Image.new_from_file(
                os.path.join(comun.IMAGESDIR, 'mwig-clear-night.png')))
        self.menus[index]['moon_phase'].set_always_show_image(True)
        self.menus[index]['moon_phase'].connect(
            'activate', self.on_moon_clicked)
        self.menus[index]['moon_phase'].show()
        main_menu.append(self.menus[index]['moon_phase'])
        #
        separator = Gtk.SeparatorMenuItem()
        separator.show()
        main_menu.append(separator)
        #
        self.menus[index]['preferences'] = Gtk.MenuItem(
            label=_('Preferences'))
        self.menus[index]['preferences'].connect(
            'activate', self.menu_set_preferences_response)
        self.menus[index]['preferences'].show()
        main_menu.append(self.menus[index]['preferences'])
        #
        self.menus[index]['help'] = Gtk.MenuItem(
            label=_('Help'))
        self.menus[index]['help'].set_submenu(self.get_help_menu())
        self.menus[index]['help'].show()
        main_menu.append(self.menus[index]['help'])
        #
        self.menus[index]['exit'] = Gtk.MenuItem(
            label=_('Exit'))
        self.menus[index]['exit'].connect(
            'activate', self.menu_exit_response)
        self.menus[index]['exit'].show()
        main_menu.append(self.menus[index]['exit'])
        #
        main_menu.show()
        self.indicators[index].set_menu(main_menu)

    def update_menu(self, index):
        if not internet_on():
            print('--- Not internet connection ---')
            if self.icon_light:
                icon = os.path.join(
                    comun.ICONDIR,
                    weatherservice.CONDITIONS['not available']['icon-light'])
            else:
                icon = os.path.join(
                    comun.ICONDIR,
                    weatherservice.CONDITIONS['not available']['icon-dark'])
            self.indicators[index].set_icon(icon)
            self.indicators[index].set_label('', '')
            msg = weatherservice.CONDITIONS['not available']['text']
            msg += '\n' + _('Not Internet connection')
            image = os.path.join(
                comun.IMAGESDIR,
                weatherservice.CONDITIONS['not available']['image'])
            self.notifications[index].update(
                'My-Weather-Indicator',
                msg,
                image)
            self.notifications[index].show()
            return
        print('--- Updating data in location %s ---' % (index))
        if self.preferences[index]['autolocation']:
            lat, lon = ipaddress.get_current_location()
            location = geocodeapi.get_inv_direction(lat, lon)['city']
            if location is None:
                location = ''
            print(lat, lon, location)
            if self.preferences[index]['latitude'] != lat and\
                    self.preferences[index]['longitude'] != lon:
                self.preferences[index]['latitude'] = lat
                self.preferences[index]['longitude'] = lon
                self.preferences[index]['location'] = location
                if self.ws == 'worldweatheronline':
                    self.weatherservices[index] =\
                        worldweatheronlineapi.WorldWeatherOnlineService(
                            longitude=self.preferences[index]['longitude'],
                            latitude=self.preferences[index]['latitude'],
                            units=self.units,
                            key=self.key)
                    self.menus[index]['evolution'].hide()
                elif self.ws == 'openweathermap':
                    self.weatherservices[index] =\
                        wopenweathermapapi.OWMWeatherService(
                            longitude=self.preferences[index]['longitude'],
                            latitude=self.preferences[index]['latitude'],
                            units=self.units)
                    self.menus[index]['evolution'].show()
                elif self.ws == 'wunderground':
                    self.weatherservices[index] =\
                        wundergroundapi.UndergroundWeatherService(
                            longitude=self.preferences[index]['longitude'],
                            latitude=self.preferences[index]['latitude'],
                            units=self.units,
                            key=self.key)
                    self.menus[index]['evolution'].hide()
        print('****** Updating weather')
        weather = self.weatherservices[index].get_weather()
        print('****** Updated weather')
        print(self.weathers[index])
        if weather is None or (weather['ok'] is False and (
                self.weathers[index] is not None and
                self.weathers[index]['ok'] is True)):
            return
        temporal_current_conditions = weather['current_conditions']
        if len(temporal_current_conditions) != 0:
            self.current_conditions[index] = temporal_current_conditions
            self.weathers[index] = weather
            ########################################################
            if self.preferences[index]['location']:
                self.menus[index]['location'].set_label(
                    _('Location') + ': ' + self.preferences[index]['location'])
            self.menus[index]['temperature'].set_label(_('Temperature') + ': \
{0}{1:c}'.format(self.current_conditions[index]['temperature'], 176))
            self.menus[index]['humidity'].set_label(
                _('Humidity') + ': ' +
                self.current_conditions[index]['humidity'])
            self.menus[index]['feels_like'].set_label(_('Feels like') + ': \
{0}{1:c}'.format(self.current_conditions[index]['feels_like'], 176))
            self.menus[index]['dew_point'].set_label(_('Dew Point') + ': \
{0}{1:c}'.format(self.current_conditions[index]['dew_point'], 176))
            self.menus[index]['wind'].set_label(
                _('Wind') + ': ' +
                self.current_conditions[index]['wind_condition'])
            if self.current_conditions[index]['wind_icon']:
                image = Gtk.Image.new_from_file(
                    os.path.join(comun.IMAGESDIR,
                                 self.current_conditions[index]['wind_icon']))
                self.menus[index]['wind'].set_image(image)
            self.menus[index]['condition'].set_label(
                self.current_conditions[index]['condition_text'])
            self.menus[index]['condition'].set_image(
                Gtk.Image.new_from_file(os.path.join(
                    comun.IMAGESDIR,
                    self.current_conditions[index]['condition_image'])))
            if self.widgets[index] is not None:
                self.widgets[index].set_location(
                    self.preferences[index]['location'])
                self.widgets[index].set_weather(weather)
            self.menus[index]['dawn'].set_label(
                _('Dawn') + ': ' + self.current_conditions[index]['dawn'])
            self.menus[index]['sunrise'].set_label(
                _('Sunrise') + ': ' +
                self.current_conditions[index]['sunrise'])
            self.menus[index]['sunset'].set_label(
                _('Sunset') + ': ' + self.current_conditions[index]['sunset'])
            self.menus[index]['dusk'].set_label(
                _('Dusk') + ': ' + self.current_conditions[index]['dusk'])
            self.menus[index]['moon_phase'].set_label(
                self.current_conditions[index]['moon_phase'])
            self.menus[index]['moon_phase'].set_image(
                Gtk.Image.new_from_file(
                    os.path.join(comun.IMAGESDIR,
                                 self.current_conditions[index]['moon_icon'])))
            self.menus[index]['moon_calendar'].set_image(
                Gtk.Image.new_from_file(
                    os.path.join(comun.IMAGESDIR,
                                 self.current_conditions[index]['moon_icon'])))
            #
            pressure = (
                self.current_conditions[index]['pressure'] is not None)
            visibility = (
                self.current_conditions[index]['visibility'] is not None)
            cloudiness = (
                self.current_conditions[index]['cloudiness'] is not None)
            # solarradiation = (
            #    self.current_conditions[index]['solarradiation'] is not None)
            UV = (
                self.current_conditions[index]['UV'] is not None)
            precip_today = (
                self.current_conditions[index]['precip_today'] is not None)
            self.menus[index]['pressure'].set_visible(pressure)
            self.menus[index]['visibility'].set_visible(visibility)
            self.menus[index]['cloudiness'].set_visible(cloudiness)
            self.menus[index]['uv'].set_visible(UV)
            self.menus[index]['precipitation'].set_visible(precip_today)
            if pressure:
                self.menus[index]['pressure'].set_label(
                    ('%s: %s') % (_('Pressure'),
                                  self.current_conditions[index]['pressure']))
            if visibility:
                value = self.current_conditions[index]['visibility']
                self.menus[index]['visibility'].set_label(
                    ('%s: %s') % (_('Visibility'), value))
            if cloudiness:
                value = self.current_conditions[index]['cloudiness']
                self.menus[index]['cloudiness'].set_label(
                    ('%s: %s') % (_('Cloudiness'), value))
            if UV:
                value = self.current_conditions[index]['UV']
                self.menus[index]['uv'].set_label(
                    ('%s: %s') % (_('UV'), value))
            if precip_today:
                value = self.current_conditions[index]['precip_today']
                self.menus[index]['precipitation'].set_label(
                    ('%s: %s') % (_('Precipitation'), value))
            if self.preferences[index]['show-temperature'] is True:
                value = self.current_conditions[index]['temperature']
                self.indicators[index].set_label(
                    '{0}{1:c}'.format(value, 176), '')
            else:
                self.indicators[index].set_label('', '')
            if self.preferences[index]['show'] is True:
                self.indicators[index].set_status(
                    appindicator.IndicatorStatus.ACTIVE)
            else:
                self.indicators[index].set_status(
                    appindicator.IndicatorStatus.PASSIVE)
            if self.icon_light:
                icon = os.path.join(
                    comun.ICONDIR,
                    self.current_conditions[index]['condition_icon_light'])
            else:
                icon = os.path.join(
                    comun.ICONDIR,
                    self.current_conditions[index]['condition_icon_dark'])
            self.indicators[index].set_icon(icon)
            if self.preferences[index]['show-notifications'] is True:
                msg = _('Conditions in') + ' '
                msg += self.preferences[index]['location'] + '\n'
                msg += _('Temperature') + ': ' +\
                    self.current_conditions[index]['temperature'] + '\n'
                msg += _('Humidity') + ': ' + \
                    self.current_conditions[index]['humidity'] + '\n'
                msg += _('Wind') + ': ' +\
                    self.current_conditions[index]['wind_condition'] + '\n'
                msg += self.current_conditions[index]['condition_text']
                image = os.path.join(
                    comun.IMAGESDIR,
                    self.current_conditions[index]['condition_image'])
                self.notifications[index].update(
                    'My-Weather-Indicator',
                    msg,
                    image)
                self.notifications[index].show()
            while Gtk.events_pending():
                Gtk.main_iteration()
        print('--- End of updating data in location %s ---' % (index))
        self.last_update_time = time.time()

    def on_moon_clicked(self, widget):
        p = CalendarWindow()
        p.show_all()

    def menu_offon(self, ison):
        for i in range(INDICATORS):
            self.menus[i]['forecast'].set_sensitive(ison)
            self.menus[i]['forecastmap'].set_sensitive(ison)
            self.menus[i]['evolution'].set_sensitive(ison)
            self.menus[i]['preferences'].set_sensitive(ison)
            self.menus[i]['moon_calendar'].set_sensitive(ison)
            self.menus[i]['update'].set_sensitive(ison)

    def menu_forecast_map_response(self, widget, index):
        self.menu_offon(False)
        ForecastMap(self.preferences[index]['latitude'],
                    self.preferences[index]['longitude'])
        self.menu_offon(True)

    def menu_evolution_response(self, widget, index):
        self.menu_offon(False)
        temperatures = []
        humidities = []
        cloudinesses = []
        for data in self.weatherservices[index].get_hourly_weather():
            value = time.mktime(
                data['datetime'].timetuple()) * 1000 +\
                data['datetime'].microsecond / 1000
            temperatures.append([value, float(data['temperature'])])
            humidities.append([value, float(data['avehumidity'])])
            cloudinesses.append([value, float(data['cloudiness'])])
        title = _('Forecast for next hours')
        subtitle = _('Weather service') + ': OpenWeatherMap'
        graph = Graph(title, subtitle, temperature=temperatures,
                      humidity=humidities, cloudiness=cloudinesses)
        graph.run()
        self.menu_offon(True)

    def menu_forecast_response(self, widget, index):
        self.menu_offon(False)
        self.preferences[index]['location']
        FC(self.preferences[index]['location'], self.ws, self.weathers[index])
        self.menu_offon(True)

    def menu_set_preferences_response(self, widget):
        self.menu_offon(False)
        cm = preferences.CM()
        if cm.run() == Gtk.ResponseType.ACCEPT:
            cm.hide()
            cm.save_preferences()
            cm.hide()
            cm.destroy()
            self.load_preferences()
        cm.destroy()
        self.menu_offon(True)

    def menu_refresh_weather_response(self, widget, index):
        if self.last_update_time + 600 < time.time():
            self.start_weather_updater()

    def menu_exit_response(self, widget):
        exit(0)

    def menu_about_response(self, widget):
        self.menu_offon(False)
        widget.set_sensitive(False)
        ad = Gtk.AboutDialog()
        ad.set_name(comun.APPNAME)
        ad.set_version(comun.VERSION)
        ad.set_copyright('Copyrignt (c) 2011-2016\nLorenzo Carbonell')
        ad.set_comments(_('A weather indicator'))
        ad.set_license('''
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
''')
        ad.set_website('http://www.atareao.es')
        ad.set_website_label('http://www.atareao.es')
        ad.set_authors([
            'Pascal De Vuyst <pascal.devuyst@gmail.com>',
            'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>',
            'doug <https://launchpad.net/~r-d-vaughan>'])
        ad.set_translator_credits('antisa <https://launchpad.net/~antisa>\n\
António Manuel Dias <https://launchpad.net/~ammdias>\n\
Clicksights <https://launchpad.net/~bj7u6139zdyf2a6nz2ly74oec10f2ln-info>\n\
Cooter <https://launchpad.net/~cooter>\n\
Daniel Nylander <https://launchpad.net/~yeager>\n\
Darian Shalev <https://launchpad.net/~lifusion>\n\
DimmuBoy <https://launchpad.net/~dimmuboy>\n\
Emmanuel Brun <https://launchpad.net/~manu57>\n\
Euthymios Spentzos <https://launchpad.net/~voreas>\n\
Gerhard Radatz <https://launchpad.net/~gerhard-radatz>\n\
Grzelny <https://launchpad.net/~grzelny>\n\
Gyaraki László <https://launchpad.net/~gyarakilaszlo>\n\
Hoàng Ngọc Long <https://launchpad.net/~ngoclong19>\n\
Hu Feifei <https://launchpad.net/~gracegreener>\n\
Ibrahim Saed <https://launchpad.net/~ibraheem5000>\n\
Jack H. Daniels <https://launchpad.net/~jack-3wh>\n\
Joseba Oses <https://launchpad.net/~sdsoldi-gmail>\n\
Kim Allamandola <https://launchpad.net/~spacexplorer>\n\
kingdruid <https://launchpad.net/~kingdruid>\n\
Mantas Kriaučiūnas <https://launchpad.net/~mantas>\n\
Maroje Delibasic <https://launchpad.net/~maroje-delibasic>\n\
nehxby <https://launchpad.net/~nehxby-gmail>\n\
Nikola Petković <https://launchpad.net/~nikolja5-gmail>\n\
pardalinux <https://launchpad.net/~pardalinux>\n\
Praveen Illa <https://launchpad.net/~telugulinux>\n\
Radek Šprta <https://launchpad.net/~radek-sprta>\n\
Ricardo <https://launchpad.net/~ragmster>\n\
rodion <https://launchpad.net/~rodion-samusik>\n\
Sal Inski <https://launchpad.net/~syb3ria>\n\
sfc <https://launchpad.net/~sfc-0>\n\
Sohrab <https://launchpad.net/~sohrab-naushad>\n\
Styrmir Magnússon <https://launchpad.net/~styrmirm>\n\
sylinub <https://launchpad.net/~sylinub>\n\
whochismo <https://launchpad.net/~whochismo>\n')
        ad.set_documenters([
            'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_artists([
            '~mohitg <http://mohitg.deviantart.com/>',
            '~MerlinTheRed <http://merlinthered.deviantart.com/>'])
        ad.set_logo(GdkPixbuf.Pixbuf.new_from_file(comun.ICON))
        ad.set_icon(GdkPixbuf.Pixbuf.new_from_file(comun.ICON))
        ad.set_program_name(comun.APPNAME)
        ad.run()
        ad.destroy()
        widget.set_sensitive(True)
        self.menu_offon(True)


def main():
    print(machine_information.get_information())
    print('My-Weather-Indicator version: %s' % comun.VERSION)
    print('#####################################################')
    load_css(CSS_FILE)
    Notify.init("my-weather-indicator")
    MWI()
    Gtk.main()


if __name__ == "__main__":
    main()
    exit(0)
