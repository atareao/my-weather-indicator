#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
#
# My-Weather-Indicator
# An indicator to show the weather
#
# Adding keybiding
#
# Copyright (C) 2010 -2016 Lorenzo Carbonell
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
#
import os
import gi
from gi.repository import GLib
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Notify
import sys
import time
import preferences
import dbus
import time
import webbrowser
from datetime import datetime
from forecastw import FC
from openweathermap import ForecastMap
from preferences import CM
from configurator import Configuration
import ipaddress
import geocodeapi
import comun
import wyahooapi
import weatherservice
import worldweatheronlineapi
import wopenweathermapapi
import wundergroundapi
import machine_information
from graph import Graph
from comun import _
from comun import internet_on
from weatherwidget import WeatherWidget

try:
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(1)


def add2menu(menu, text=None, icon=None,
             conector_event=None, conector_action=None):
    if text is not None:
        menu_item = Gtk.ImageMenuItem.new_with_label(text)
        if icon:
            image = Gtk.Image.new_from_file(icon)
            menu_item.set_image(image)
            menu_item.set_always_show_image(True)
    else:
        if icon is None:
            menu_item = Gtk.SeparatorMenuItem()
        else:
            menu_item = Gtk.ImageMenuItem.new_from_file(icon)
            menu_item.set_always_show_image(True)
    if conector_event is not None and conector_action is not None:
        menu_item.connect(conector_event, conector_action)
    menu_item.show()
    menu.append(menu_item)
    return menu_item


class MWI():
    def __init__(self):
        if dbus.SessionBus().request_name('es.atareao.MyWeatherIndicator') !=\
                dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
            print("application already running")
            exit(0)
        #
        self.current_conditions = None
        self.current_conditions2 = None
        self.preferences_out = False
        self.forecast_out = False
        self.weather_updater = 0
        self.widgets_updater = 0
        #
        self.notification = Notify.Notification.new('', '', None)
        status = appindicator.IndicatorCategory.APPLICATION_STATUS
        self.indicator = appindicator.Indicator.new('My-Weather-Indicator',
                                                    'My-Weather-Indicator',
                                                    status)
        self.notification2 = Notify.Notification.new('', '', None)
        self.indicator2 = appindicator.Indicator.new('My-Weather-Indicator2',
                                                     'My-Weather-Indicator',
                                                     status)
        #
        self.create_menu()
        self.create_menu2()
        #
        while internet_on() == False:
            print('Waiting for internet')
            time_start = time.time()
            time_end = (time_start + 1)
            while time_end > time.time():
                while Gtk.events_pending():
                    Gtk.main_iteration()
                time.sleep(0.3)
        print(comun.CONFIG_FILE, os.path.exists(comun.CONFIG_FILE))
        if not os.path.exists(comun.CONFIG_FILE):
            configuration = Configuration()
            configuration.reset()
            latitude, longitude = ipaddress.get_current_location()
            city = geocodeapi.get_inv_direction(latitude, longitude)
            configuration.set('latitude', latitude)
            configuration.set('longitude', longitude)
            if city is not None:
                configuration.set('location', city['city'])
            configuration.save()
            cm = preferences.CM()
            if cm.run() == Gtk.ResponseType.ACCEPT:
                cm.save_preferences()
            else:
                exit(0)
            cm.hide()
            cm.destroy()
        self.WW1 = None
        self.WW2 = None
        self.load_preferences()

    def update_widgets(self):
        utcnow = datetime.utcnow()
        secnow = utcnow.second
        if self.WW1 is not None:
            self.WW1.set_datetime(utcnow)
        if self.WW2 is not None:
            self.WW2.set_datetime(utcnow)
        return True

    def work(self):
        print('***** refreshing weather *****')
        self.menu_refresh.set_label(_('Refresh weather'))
        self.menu2_refresh.set_label(_('Refresh weather'))
        if self.main_location:
            self.set_menu()
            self.indicator.set_status(
                appindicator.IndicatorStatus.ACTIVE)
        else:
            self.indicator.set_status(
                appindicator.IndicatorStatus.PASSIVE)
        if self.second_location:
            self.set_menu2()
            self.indicator2.set_status(
                appindicator.IndicatorStatus.ACTIVE)
        else:
            self.indicator2.set_status(
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
        translate_item.connect('activate',
                               lambda x: webbrowser.open('http://www.atareao.es\
/apps/my-weather-indicator-para-ubuntu/'))
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
        twitter_item.connect('activate',
                             lambda x: webbrowser.open(
                                'https://twitter.com/atareao'))
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
        facebook_item.connect('activate',
                              lambda x: webbrowser.open(
                                'http://www.facebook.com/elatareao'))
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
        configuration = Configuration()
        self.first_time = configuration.get('first-time')
        self.refresh = configuration.get('refresh')
        self.version = configuration.get('version')
        #
        self.main_location = configuration.get('main-location')
        self.autolocation = configuration.get('autolocation')
        self.location = configuration.get('location')
        self.latitude = configuration.get('latitude')
        self.longitude = configuration.get('longitude')
        self.show_temperature = configuration.get('show-temperature')
        self.show_notifications = configuration.get('show-notifications')
        self.widget1 = configuration.get('widget1')
        '''
        self.widget1 = configuration.get('widget1')
        self.onwidget1hide = configuration.get('onwidget1hide')
        self.WW1.set_hideindicator(self.onwidget1hide)
        self.WW1.set_ontop('onwidget1top')
        self.WW1.show_intaskbar('showintaskbar1')
        '''
        #
        self.second_location = configuration.get('second-location')
        self.location2 = configuration.get('location2')
        self.latitude2 = configuration.get('latitude2')
        self.longitude2 = configuration.get('longitude2')
        self.show_temperature2 = configuration.get('show-temperature2')
        self.show_notifications2 = configuration.get('show-notifications2')
        self.widget2 = configuration.get('widget2')
        '''
        self.widget2 = configuration.get('widget2')
        self.onwidget2hide = configuration.get('onwidget2hide')
        self.WW2.set_hideindicator(self.onwidget2hide)
        self.WW2.set_ontop('onwidget1top')
        self.WW2.show_intaskbar('showintaskbar1')
        '''
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
            if self.main_location:
                self.weatherservice1 = wyahooapi.YahooWeatherService(
                    longitude=self.longitude,
                    latitude=self.latitude,
                    units=self.units)
            if self.second_location:
                self.weatherservice2 = wyahooapi.YahooWeatherService(
                    longitude=self.longitude2,
                    latitude=self.latitude2,
                    units=self.units)
            self.menu_evolution.hide()
            self.menu_evolution2.hide()
        elif self.ws == 'worldweatheronline':
            self.key = configuration.get('wwo-key')
            if self.main_location:
                self.weatherservice1 =\
                    worldweatheronlineapi.WorldWeatherOnlineService(
                        longitude=self.longitude,
                        latitude=self.latitude,
                        units=self.units,
                        key=self.key)
            if self.second_location:
                self.weatherservice2 =\
                    worldweatheronlineapi.WorldWeatherOnlineService(
                        longitude=self.longitude2,
                        latitude=self.latitude2,
                        units=self.units,
                        key=self.key)
            self.menu_evolution.hide()
            self.menu_evolution2.hide()
        elif self.ws == 'openweathermap':
            self.key = ''
            if self.main_location:
                self.weatherservice1 = wopenweathermapapi.OWMWeatherService(
                    longitude=self.longitude,
                    latitude=self.latitude,
                    units=self.units)
            if self.second_location:
                self.weatherservice2 = wopenweathermapapi.OWMWeatherService(
                    longitude=self.longitude2,
                    latitude=self.latitude2,
                    units=self.units)
            self.menu_evolution.show()
            self.menu_evolution2.show()
        elif self.ws == 'wunderground':
            self.key = configuration.get('wu-key')
            if self.main_location:
                self.weatherservice1 =\
                    wundergroundapi.UndergroundWeatherService(
                        longitude=self.longitude,
                        latitude=self.latitude,
                        units=self.units,
                        key=self.key)
            if self.second_location:
                self.weatherservice2 =\
                    wundergroundapi.UndergroundWeatherService(
                        longitude=self.longitude2,
                        latitude=self.latitude2,
                        units=self.units,
                        key=self.key)
            self.menu_evolution.hide()
            self.menu_evolution2.hide()
        #
        self.icon_light = configuration.get('icon-light')
        #
        utcnow = datetime.utcnow()
        if self.main_location and self.widget1:
            if self.WW1 is not None:
                self.WW1.hide()
                self.WW1.destroy()
                self.WW1 = None
            self.WW1 = WeatherWidget(self.indicator, 1)
            self.WW1.set_datetime(utcnow)
            self.WW1.set_location(self.location)
            self.WW1.connect('pinit', self.on_pinit, 1)
        elif self.WW1 is not None:
            self.WW1.hide()
            self.WW1.destroy()
            self.WW1 = None
        if self.second_location and self.widget2:
            if self.WW2 is not None:
                self.WW2.hide()
                self.WW2.destroy()
                self.WW2 = None
            self.WW2 = WeatherWidget(self.indicator, 2)
            self.WW2.set_datetime(utcnow)
            self.WW2.set_location(self.location2)
            self.WW2.connect('pinit', self.on_pinit, 2)
        elif self.WW2 is not None:
            self.WW2.hide()
            self.WW2.destroy()
            self.WW2 = None
        self.start_weather_updater()
        if self.widget1 or self.widget2:
            self.start_widgets_updater()
        else:
            self.stop_widgets_updater()

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
        self.work()
        self.weather_updater = GLib.timeout_add_seconds(self.refresh * 3600,
                                                        self.work)

    def stop_weather_updater(self):
        if self.weather_updater > 0:
            GLib.source_remove(self.weather_updater)
            self.weather_updater = 0

    def on_pinit(self, widget, data, widget_number):
        utcnow = datetime.utcnow()
        if widget_number == 1:
            self.WW1.is_above = not self.WW1.is_above
            weather1 = self.WW1.weather_data
            self.WW1.save_preferences()
            self.WW1.hide()
            self.WW1.destroy()
            self.WW1 = None
            self.WW1 = WeatherWidget(self.indicator, 1)
            self.WW1.set_datetime(utcnow)
            self.WW1.set_location(self.location)
            self.WW1.connect('pinit', self.on_pinit, 1)
            self.WW1.set_weather(weather1)
        elif widget_number == 2:
            self.WW2.is_above = not self.WW2.is_above
            weather2 = self.WW2.weather_data
            self.WW2.save_preferences()
            self.WW2.hide()
            self.WW2.destroy()
            self.WW2 = None
            self.WW2 = WeatherWidget(self.indicator, 2)
            self.WW2.set_datetime(utcnow)
            self.WW2.set_location(self.location)
            self.WW2.connect('pinit', self.on_pinit, 2)
            self.WW2.set_weather(weather2)

    def create_menu(self):
        self.menu = Gtk.Menu()
        self.menu_forecast = add2menu(
            self.menu, text=_('Forecast'),
            conector_event='activate',
            conector_action=self.menu_forecast_response)
        self.menu_evolution = add2menu(
            self.menu, text=_('Evolution'),
            conector_event='activate',
            conector_action=self.menu_evolution_response)
        self.menu_forecastmap = add2menu(
            self.menu, text=_('Forecast Map'),
            conector_event='activate',
            conector_action=self.menu_forecast_map_response)
        self.menu_refresh = add2menu(
            self.menu, text=_('Last Update'),
            conector_event='activate',
            conector_action=self.menu_refresh_weather_response)
        add2menu(self.menu)
        self.menu_location = add2menu(self.menu, text=_('Location')+': ')
        self.menu_temperature = add2menu(self.menu, text=_('Temperature')+': ')
        self.menu_pressure = add2menu(self.menu, text=_('Pressure')+': ')
        self.menu_humidity = add2menu(self.menu, text=_('Humidity')+': ')
        self.menu_feels_like = add2menu(self.menu, text=_('Feels like')+': ')
        self.menu_dew_point = add2menu(self.menu, text=_('Dew Point')+': ')
        self.menu_wind = add2menu(self.menu, text=_('Wind')+': ',
                                  icon='mwi-wind00')
        self.menu_visibility = add2menu(self.menu, text=_('Visibility')+': ')
        self.menu_cloudiness = add2menu(self.menu, text=_('Cloudiness')+': ')
        self.menu_uv = add2menu(self.menu, text=_('UV')+': ')
        self.menu_precipitation = add2menu(self.menu,
                                           text=_('Precipitation')+': ')
        self.menu_condition = add2menu(self.menu, text='',
                                       icon='mwig-clear')
        add2menu(self.menu)
        self.menu_dawn = add2menu(
            self.menu, text=_('Dawn')+': ',
            icon=os.path.join(comun.IMAGESDIR, 'mwig-clear.png'))
        self.menu_sunrise = add2menu(
            self.menu, text=_('Sunrise')+': ',
            icon=os.path.join(comun.IMAGESDIR, 'mwig-clear.png'))
        self.menu_sunset = add2menu(
            self.menu, text=_('Sunset')+': ',
            icon=os.path.join(comun.IMAGESDIR, 'mwig-clear-night.png'))
        self.menu_dusk = add2menu(
            self.menu, text=_('Dusk')+': ',
            icon=os.path.join(comun.IMAGESDIR, 'mwig-clear-night.png'))
        add2menu(self.menu)
        self.menu_moon_phase = add2menu(
            self.menu, text='',
            icon=os.path.join(comun.IMAGESDIR, 'mwig-clear-night.png'))
        add2menu(self.menu)
        ########################################################
        self.menu_preferences = add2menu(
            self.menu, text=_('Preferences'),
            conector_event='activate',
            conector_action=self.menu_set_preferences_response)
        menu_help = add2menu(self.menu, text=_('Help'))
        menu_help.set_submenu(self.get_help_menu())
        add2menu(self.menu, text=_('Exit'),
                 conector_event='activate',
                 conector_action=self.menu_exit_response)
        self.menu.show()
        self.indicator.set_menu(self.menu)

    def create_menu2(self):
        self.menu2 = Gtk.Menu()
        self.menu_forecast2 = add2menu(
            self.menu2, text=_('Forecast'),
            conector_event='activate',
            conector_action=self.menu_forecast_response2)
        self.menu_evolution2 = add2menu(
            self.menu2, text=_('Evolution'),
            conector_event='activate',
            conector_action=self.menu_evolution_response2)
        self.menu_forecastmap2 = add2menu(
            self.menu2, text=_('Forecast Map'),
            conector_event='activate',
            conector_action=self.menu_forecast_map_response2)
        self.menu2_refresh = add2menu(
            self.menu2, text=_('Last Update'),
            conector_event='activate',
            conector_action=self.menu_refresh_weather_response)
        add2menu(self.menu2)
        self.menu2_location = add2menu(
            self.menu2, text=_('Location')+': ')
        self.menu2_temperature = add2menu(
            self.menu2, text=_('Temperature')+': ')
        self.menu2_pressure = add2menu(self.menu2, text=_('Pressure')+': ')
        self.menu2_humidity = add2menu(self.menu2, text=_('Humidity')+': ')
        self.menu2_feels_like = add2menu(self.menu2, text=_('Feels like')+': ')
        self.menu2_dew_point = add2menu(self.menu2, text=_('Dew Point')+': ')
        self.menu2_wind = add2menu(self.menu2, text=_('Wind')+': ',
                                   icon='mwi-wind00')
        self.menu2_visibility = add2menu(self.menu2, text=_('Visibility')+': ')
        self.menu2_cloudiness = add2menu(self.menu2, text=_('Cloudiness')+': ')
        self.menu2_uv = add2menu(self.menu2, text=_('UV')+': ')
        self.menu2_precipitation = add2menu(
            self.menu2, text=_('Precipitation')+': ')
        self.menu2_condition = add2menu(self.menu2, text='', icon='mwig-clear')
        add2menu(self.menu2)
        self.menu2_dawn = add2menu(
            self.menu2, text=_('Dawn')+': ',
            icon=os.path.join(comun.IMAGESDIR, 'mwig-clear.png'))
        self.menu2_sunrise = add2menu(
            self.menu2, text=_('Sunrise')+': ',
            icon=os.path.join(comun.IMAGESDIR, 'mwig-clear.png'))
        self.menu2_sunset = add2menu(
            self.menu2, text=_('Sunset')+': ',
            icon=os.path.join(comun.IMAGESDIR, 'mwig-clear-night.png'))
        self.menu2_dusk = add2menu(
            self.menu2, text=_('Dusk')+': ',
            icon=os.path.join(comun.IMAGESDIR, 'mwig-clear-night.png'))
        add2menu(self.menu2)
        self.menu2_moon_phase = add2menu(
            self.menu2, text='',
            icon='mwig-clear-night')
        add2menu(self.menu2)
        ########################################################
        self.menu_preferences2 = add2menu(
            self.menu2, text=_('Preferences'),
            conector_event='activate',
            conector_action=self.menu_set_preferences_response)
        menu_help = add2menu(
            self.menu2, text=_('Help'))
        menu_help.set_submenu(self.get_help_menu())
        add2menu(
            self.menu2, text=_('Exit'),
            conector_event='activate',
            conector_action=self.menu_exit_response)
        self.menu2.show()
        self.indicator2.set_menu(self.menu2)

    def set_menu(self):
        print('--- Updating data in location 1 ---')
        if self.autolocation:
            lat, lon = ipaddress.get_current_location()
            self.location = ipaddress.get_address_from_ip()
            if self.latitude != lat and self.longitude != lon:
                self.latitude = lat
                self.longitude = lon
                if self.ws == 'yahoo':
                    self.weatherservice1 = wyahooapi.YahooWeatherService(
                        longitude=self.longitude,
                        latitude=self.latitude,
                        units=self.units)
                    self.menu_evolution.hide()
                elif self.ws == 'worldweatheronline':
                    self.weatherservice1 =\
                        worldweatheronlineapi.WorldWeatherOnlineService(
                            longitude=self.longitude,
                            latitude=self.latitude,
                            units=self.units,
                            key=self.key)
                    self.menu_evolution.hide()
                elif self.ws == 'openweathermap':
                    self.weatherservice1 =\
                        wopenweathermapapi.OWMWeatherService(
                            longitude=self.longitude,
                            latitude=self.latitude,
                            units=self.units)
                    self.menu_evolution.show()
                elif self.ws == 'wunderground':
                    self.weatherservice1 =\
                        wundergroundapi.UndergroundWeatherService(
                            longitude=self.longitude,
                            latitude=self.latitude,
                            units=self.units,
                            key=self.key)
                    self.menu_evolution.hide()
        print('****** Updating weather')
        weather = self.weatherservice1.get_weather()
        print('****** Updated weather')
        if weather is None:
            return
        temporal_current_conditions = weather['current_conditions']
        conditions_changed = False
        if len(temporal_current_conditions) != 0:
            self.current_conditions = temporal_current_conditions
            self.weather1 = weather
            ########################################################
            if self.location:
                self.menu_location.set_label(
                    _('Location') + ': ' + self.location)
            self.menu_temperature.set_label(_('Temperature') + ':\
{0}{1:c}'.format(self.current_conditions['temperature'], 176))
            self.menu_humidity.set_label(
                _('Humidity') + ': ' + self.current_conditions['humidity'])
            self.menu_feels_like.set_label(_('Feels like')+':\
{0}{1:c}'.format(self.current_conditions['feels_like'], 176))
            self.menu_dew_point.set_label(_('Dew Point') + ':\
{0}{1:c}'.format(self.current_conditions['dew_point'], 176))
            self.menu_wind.set_label(
                _('Wind') + ':' + self.current_conditions['wind_condition'])
            if self.current_conditions['wind_icon']:
                image = Gtk.Image.new_from_file(
                    os.path.join(comun.IMAGESDIR,
                                 self.current_conditions['wind_icon']))
                self.menu_wind.set_image(image)
            self.menu_condition.set_label(
                self.current_conditions['condition_text'])
            afile = os.path.join(comun.IMAGESDIR,
                                 self.current_conditions['condition_image'])
            self.menu_condition.set_image(
                Gtk.Image.new_from_file(os.path.join(
                    comun.IMAGESDIR,
                    self.current_conditions['condition_image'])))
            filename = os.path.join(comun.WIMAGESDIR,
                                    self.current_conditions['condition_image'])
            if self.WW1 is not None:
                self.WW1.set_location(self.location)
                self.WW1.set_weather(weather)
            self.menu_dawn.set_label(
                _('Dawn')+': '+self.current_conditions['dawn'])
            self.menu_sunrise.set_label(
                _('Sunrise')+': '+self.current_conditions['sunrise'])
            self.menu_sunset.set_label(
                _('Sunset')+': '+self.current_conditions['sunset'])
            self.menu_dusk.set_label(
                _('Dusk')+': '+self.current_conditions['dusk'])
            self.menu_moon_phase.set_label(
                self.current_conditions['moon_phase'])
            self.menu_moon_phase.set_image(
                Gtk.Image.new_from_file(
                    os.path.join(comun.IMAGESDIR,
                                 self.current_conditions['moon_icon'])))
            #
            pressure = (self.current_conditions['pressure'] is not None)
            visibility = (self.current_conditions['visibility'] is not None)
            cloudiness = (self.current_conditions['cloudiness'] is not None)
            solarradiation = (
                self.current_conditions['solarradiation'] is not None)
            UV = (self.current_conditions['UV'] is not None)
            precip_today = (
                self.current_conditions['precip_today'] is not None)
            self.menu_pressure.set_visible(pressure)
            self.menu_visibility.set_visible(visibility)
            self.menu_cloudiness.set_visible(cloudiness)
            self.menu_uv.set_visible(UV)
            self.menu_precipitation.set_visible(precip_today)
            if pressure:
                self.menu_pressure.set_label(
                    ('%s: %s') % (_('Pressure'),
                                  self.current_conditions['pressure']))
            if visibility:
                self.menu_visibility.set_label(
                    ('%s: %s') % (_('Visibility'),
                                  self.current_conditions['visibility']))
            if cloudiness:
                self.menu_cloudiness.set_label(
                    ('%s: %s') % (_('Cloudiness'),
                                  self.current_conditions['cloudiness']))
            if UV:
                self.menu_uv.set_label(
                    ('%s: %s') % (_('UV'),
                                  self.current_conditions['UV']))
            if precip_today:
                self.menu_precipitation.set_label(
                    ('%s: %s') % (_('Precipitation'),
                                  self.current_conditions['precip_today']))
            if self.show_temperature is True:
                self.indicator.set_label(
                    '{0}{1:c}'.format(self.current_conditions['temperature'],
                                      176), '')
            else:
                self.indicator.set_label('', '')
            if self.main_location is True:
                self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
            else:
                self.indicator.set_status(appindicator.IndicatorStatus.PASSIVE)
            if self.icon_light:
                self.indicator.set_icon(
                    os.path.join(
                        comun.ICONDIR,
                        self.current_conditions['condition_icon_light']))
            else:
                self.indicator.set_icon(
                    os.path.join(
                        comun.ICONDIR,
                        self.current_conditions['condition_icon_dark']))
            if self.show_notifications is True:
                msg = _('Conditions in')+' ' + self.location + '\n'
                msg += _('Temperature')+': ' +\
                    self.current_conditions['temperature'] + '\n'
                msg += _('Humidity') + ': ' + \
                    self.current_conditions['humidity'] + '\n'
                msg += _('Wind') + ': ' +\
                    self.current_conditions['wind_condition']+'\n'
                msg += self.current_conditions['condition_text']
                self.notification.update(
                    'My-Weather-Indicator',
                    msg,
                    os.path.join(comun.IMAGESDIR,
                                 self.current_conditions['condition_image']))
                self.notification.show()
            while Gtk.events_pending():
                Gtk.main_iteration()
        print('--- End of updating data in location 1 ---')

    def set_menu2(self):
        print('--- Updating data in location 2 ---')
        print('****** Updating weather')
        weather = self.weatherservice2.get_weather()
        print('****** Updated weather')
        if weather is None:
            return
        temporal_current_conditions = weather['current_conditions']
        conditions_changed = False
        if len(temporal_current_conditions) != 0:
            self.current_conditions2 = temporal_current_conditions
            self.weather2 = weather
            if self.location2:
                self.menu2_location.set_label(
                    _('Location') + ': ' + self.location2)
            self.menu2_temperature.set_label(
                _('Temperature') + ':\
{0}{1:c}'.format(self.current_conditions2['temperature'], 176))
            self.menu2_humidity.set_label(
                _('Humidity') + ': ' + self.current_conditions2['humidity'])
            self.menu2_feels_like.set_label(
                _('Feels like') + ':\
{0}{1:c}'.format(self.current_conditions2['feels_like'], 176))
            self.menu2_dew_point.set_label(
                _('Dew Point') + ':\
{0}{1:c}'.format(self.current_conditions2['dew_point'], 176))
            self.menu2_wind.set_label(
                _('Wind') + ': ' + self.current_conditions2['wind_condition'])
            if self.current_conditions2['wind_icon']:
                image = Gtk.Image.new_from_file(
                    os.path.join(comun.IMAGESDIR,
                                 self.current_conditions2['wind_icon']))
                self.menu2_wind.set_image(image)
            self.menu2_condition.set_label(
                self.current_conditions2['condition_text'])
            self.menu2_condition.set_image(
                Gtk.Image.new_from_file(
                    os.path.join(comun.IMAGESDIR,
                                 self.current_conditions2['condition_image'])))
            self.menu2_dawn.set_label(
                _('Dawn') + ': ' + self.current_conditions2['dawn'])
            self.menu2_sunrise.set_label(
                _('Sunrise') + ': ' + self.current_conditions2['sunrise'])
            self.menu2_sunset.set_label(
                _('Sunset') + ': ' + self.current_conditions2['sunset'])
            self.menu2_dusk.set_label(
                _('Dusk') + ': ' + self.current_conditions2['dusk'])
            filename = os.path.join(
                comun.WIMAGESDIR, self.current_conditions2['condition_image'])
            if self.WW2 is not None:
                self.WW2.set_location(self.location2)
                self.WW2.set_weather(weather)
            self.menu2_moon_phase.set_label(
                self.current_conditions2['moon_phase'])
            self.menu2_moon_phase.set_image(
                Gtk.Image.new_from_file(
                    os.path.join(comun.IMAGESDIR,
                                 self.current_conditions2['moon_icon'])))
            #
            pressure = (self.current_conditions2['pressure'] is not None)
            visibility = (self.current_conditions2['visibility'] is not None)
            cloudiness = (self.current_conditions2['cloudiness'] is not None)
            solarradiation = (
                self.current_conditions2['solarradiation'] is not None)
            UV = (self.current_conditions2['UV'] is not None)
            precip_today = (
                self.current_conditions2['precip_today'] is not None)
            self.menu2_pressure.set_visible(pressure)
            self.menu2_visibility.set_visible(visibility)
            self.menu2_cloudiness.set_visible(cloudiness)
            self.menu2_uv.set_visible(UV)
            self.menu2_precipitation.set_visible(precip_today)
            if pressure:
                self.menu2_pressure.set_label(
                    ('%s: %s') % (_('Pressure'),
                                  self.current_conditions2['pressure']))
            if visibility:
                self.menu2_visibility.set_label(
                    ('%s: %s') % (_('Visibility'),
                                  self.current_conditions2['visibility']))
            if cloudiness:
                self.menu2_cloudiness.set_label(
                    ('%s: %s') % (_('Cloudiness'),
                                  self.current_conditions2['cloudiness']))
            if UV:
                self.menu2_uv.set_label(
                    ('%s: %s') % (_('UV'), self.current_conditions2['UV']))
            if precip_today:
                self.menu2_precipitation.set_label(
                    ('%s: %s') % (_('Precipitation'),
                                  self.current_conditions2['precip_today']))
            if self.show_temperature2 is True:
                self.indicator2.set_label(
                    '{0} {1:c}'.format(self.current_conditions2['temperature'],
                                       176), '')
            else:
                self.indicator2.set_label('', '')
            if self.second_location is True:
                self.indicator2.set_status(appindicator.IndicatorStatus.ACTIVE)
            else:
                self.indicator2.set_status(
                    appindicator.IndicatorStatus.PASSIVE)
            if self.icon_light:
                self.indicator2.set_icon(
                    os.path.join(
                        comun.ICONDIR,
                        self.current_conditions2['condition_icon_light']))
            else:
                self.indicator2.set_icon(
                    os.path.join(
                        comun.ICONDIR,
                        self.current_conditions2['condition_icon_dark']))
            ########################################################
            if self.show_notifications2 is True:
                msg = _('Conditions in') + ' ' + self.location2 + '\n'
                msg += _('Temperature') + ': ' +\
                    self.current_conditions2['temperature'] + '\n'
                msg += _('Humidity') + ': ' +\
                    self.current_conditions2['humidity']+'\n'
                msg += _('Wind') + ': ' +\
                    self.current_conditions2['wind_condition']+'\n'
                msg += self.current_conditions2['condition_text']
                self.notification2.update(
                    'My-Weather-Indicator',
                    msg,
                    os.path.join(
                        comun.IMAGESDIR,
                        self.current_conditions2['condition_image']))
                self.notification2.show()
            while Gtk.events_pending():
                Gtk.main_iteration()
        print('--- End of updating data in location 2 ---')

    def menu_offon(self, ison):
        self.menu_forecast.set_sensitive(ison)
        self.menu_preferences.set_sensitive(ison)
        self.menu_forecast2.set_sensitive(ison)
        self.menu_preferences2.set_sensitive(ison)
        self.menu_forecastmap.set_sensitive(ison)
        self.menu_forecastmap2.set_sensitive(ison)
        self.menu_evolution.set_sensitive(ison)
        self.menu_evolution2.set_sensitive(ison)
        self.menu_refresh.set_sensitive(ison)
        self.menu2_refresh.set_sensitive(ison)

    def menu_forecast_map_response(self, widget):
        self.menu_offon(False)
        fc = ForecastMap(self.latitude,
                         self.longitude,
                         self.units.temperature)
        self.menu_offon(True)

    def menu_forecast_map_response2(self, widget):
        self.menu_offon(False)
        fc = ForecastMap(self.latitude2,
                         self.longitude2,
                         self.units.temperature)
        self.menu_offon(True)

    def menu_evolution_response2(self, widget):
        self.menu_offon(False)
        temperatures = []
        humidities = []
        cloudinesses = []
        for data in self.weatherservice2.get_hourly_weather():
            value = time.mktime(
                data['datetime'].timetuple()) * 1000 +\
                data['datetime'].microsecond / 1000
            temperatures.append([value, float(data['temperature'])])
            humidities.append([value, float(data['avehumidity'])])
            cloudinesses.append([value, float(data['cloudiness'])])
        title = _('Forecast for next hours')
        subtitle = _('Weather service')+': OpenWeatherMap'
        graph = Graph(title, subtitle, temperature=temperatures,
                      humidity=humidities, cloudiness=cloudinesses)
        self.menu_offon(True)

    def menu_evolution_response(self, widget):
        self.menu_offon(False)
        temperatures = []
        humidities = []
        cloudinesses = []
        for data in self.weatherservice1.get_hourly_weather():
            value = time.mktime(
                data['datetime'].timetuple()) * 1000 +\
                data['datetime'].microsecond / 1000
            temperatures.append([value, float(data['temperature'])])
            humidities.append([value, float(data['avehumidity'])])
            cloudinesses.append([value, float(data['cloudiness'])])
        title = _('Forecast for next hours')
        subtitle = _('Weather service')+': OpenWeatherMap'
        graph = Graph(title, subtitle, temperature=temperatures,
                      humidity=humidities, cloudiness=cloudinesses)
        self.menu_offon(True)

    def menu_forecast_response(self, widget):
        self.menu_offon(False)
        fc = FC(self.location, self.ws, self.weather1)
        self.menu_offon(True)

    def menu_forecast_response2(self, widget):
        self.menu_offon(False)
        fc = FC(self.location2, self.ws, self.weather2)
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

    def menu_refresh_weather_response(self, widget):
        self.work()

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


def redondea(valor):
    valor = valor * 10.0
    return int(valor)/10.0


def cambia(valor, a):
    if len(valor) == 0:
        return ''
    valor = float(valor)
    if a == 'F':
        return str(redondea(valor * 9.0 / 5.0 + 32.0))
    elif a == 'K':
        return str(redondea(valor + 273.15))
    return str(valor)

if __name__ == "__main__":
    print(machine_information.get_information())
    print('My-Weather-Indicator version: %s' % comun.VERSION)
    print('#####################################################')
    Notify.init("my-weather-indicator")
    mwi = MWI()
    Gtk.main()
    exit(0)
