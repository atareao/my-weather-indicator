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
import time
import webbrowser
from datetime import datetime, timezone
import logging
import socket
import sys
import gi
try:
    gi.require_version('GLib', '2.0')
    gi.require_version('AyatanaAppIndicator3', '0.1')
    gi.require_version('Gtk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
    gi.require_version('Notify', '0.7')
    gi.require_version('WebKit2', '4.1')
except ValueError as e:
    print(e)
    print('Repository version required not present')
    sys.exit(1)
# pylint: disable=wrong-import-position
from gi.repository import GLib
from gi.repository import AyatanaAppIndicator3 as appindicator
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Notify
from gi.repository import GObject
import comun
import geocodeapi
import machine_information
import preferences
import weatherservice
import wopenmeteoapi
from forecastw import FC
from weatherwidget import WeatherWidget
from mooncalendarwindow import CalendarWindow
from graph import Graph
from utils import load_css
from comun import _
from comun import internet_on
from comun import CSS_FILE
from configurator import Configuration


INDICATORS = 2
TIME_TO_CHECK = 15

FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(stream=sys.stdout,
                    format=FORMAT,
                    level=LOG_LEVEL)
logger = logging.getLogger(__name__)


class MWI(GObject.Object):
    """
    MWI class represents the My Weather Indicator application.

    Attributes:
        weather_updater (int): The weather updater.
        widgets_updater (int): The widgets updater.
        internet_updater (int): The internet updater.
        internet_connection (bool): The internet connection status.
        menus (list): The list of menus.
        indicators (list): The list of indicators.
        notifications (list): The list of notifications.
        widgets (list): The list of widgets.
        weatherservices (list): The list of weather services.
        weathers (list): The list of weather data.
        current_conditions (list): The list of current weather conditions.
        preferences (list): The list of user preferences.
        last_update_time (int): The timestamp of the last update.

    Methods:
        __init__(): Initializes the MWI object.
        update_widgets(): Updates the widgets.
        update_weather(): Updates the weather.
        open_in_browser(widget, url): Opens the specified URL in a web browser.
        get_help_menu(): Returns the help menu.
        load_preferences(): Loads the user preferences.
    """
    __gsignals__ = {
        'internet-out': (GObject.SignalFlags.RUN_FIRST,
                         GObject.TYPE_NONE, ()),
        'internet-in': (GObject.SignalFlags.RUN_FIRST,
                        GObject.TYPE_NONE, ()),
        'update-weather': (GObject.SignalFlags.RUN_FIRST,
                           GObject.TYPE_NONE, ()),
        'update-widgets': (GObject.SignalFlags.RUN_FIRST,
                           GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        """
        Initializes the MyWeatherIndicator class.

        This method sets up the initial state of the MyWeatherIndicator object.
        It initializes various attributes such as weather_updater,
        widgets_updater, internet_updater, internet_connection, menus,
        indicators, notifications, widgets, weatherservices, weathers,
        current_conditions, preferences, and last_update_time. It also creates
        appindicator indicators and notifications, and calls the create_menu()
        method to create menus for each indicator.  Finally, it loads the
        preferences using the load_preferences() method.
        """
        # code implementation
        GObject.Object.__init__(self)
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
        """
        Updates the widgets with the current datetime in UTC.

        Returns:
            bool: True if any widget was updated, False otherwise.
        """
        update = False
        utcnow = datetime.now(timezone.utc)
        for i in range(INDICATORS):
            if self.widgets[i] is not None:
                self.widgets[i].set_datetime(utcnow)
                update = True
        return update

    def update_weather(self):
        """
        Updates the weather indicators based on the user preferences.

        This method iterates over the indicators and updates their status
        based on the user preferences.
        If a preference is set to 'show', the corresponding indicator is
        updated and set to active status.
        Otherwise, the indicator is set to passive status.

        Returns:
            bool: True if the weather indicators were successfully updated.
        """
        logger.debug('***** refreshing weather *****')
        for i in range(INDICATORS):
            if self.preferences[i]['show']:
                self.update_menu(i)
                self.indicators[i].set_status(
                    appindicator.IndicatorStatus.ACTIVE)
            else:
                self.indicators[i].set_status(
                    appindicator.IndicatorStatus.PASSIVE)
        return True

    def open_in_browser(self, _widget, url):
        """
        Opens the specified URL in the default web browser.

        Parameters:
            _widget (Widget): The widget associated with the action.
            url (str): The URL to be opened in the web browser.
        """
        webbrowser.open(url)

    def get_help_menu(self):
        """
        Returns a Gtk.Menu object containing various help options for the
        application.

        Returns:
            Gtk.Menu: A menu containing help options.
        """
        help_menu = Gtk.Menu()
        #
        homepage_item = Gtk.MenuItem(label=_(
            'Homepage'))
        homepage_item.connect(
            'activate',
            self.open_in_browser,
            'http://www.atareao.es/apps/my-weather-indicator-para-ubuntu/')
        homepage_item.show()
        help_menu.append(homepage_item)
        #
        help_item = Gtk.MenuItem(label=_(
            'Get help online...'))
        help_item.connect(
            'activate',
            self.open_in_browser,
            'http://www.atareao.es/apps/my-weather-indicator-para-ubuntu/')
        help_item.show()
        help_menu.append(help_item)
        #
        translate_item = Gtk.MenuItem(label=_(
            'Translate this application...'))
        translate_item.connect(
            'activate',
            self.open_in_browser,
            'http://www.atareao.es/apps/my-weather-indicator-para-ubuntu/')
        translate_item.show()
        help_menu.append(translate_item)
        #
        bug_item = Gtk.MenuItem(label=_(
            'Report a bug...'))
        bug_item.connect(
            'activate',
            self.open_in_browser,
            'https://github.com/atareao/my-weather-indicator/issues')
        bug_item.show()
        help_menu.append(bug_item)
        #
        separator = Gtk.SeparatorMenuItem()
        separator.show()
        help_menu.append(separator)
        #
        twitter_item = Gtk.MenuItem(label=_(
            'Contact me at Twitter'))
        twitter_item.connect(
            'activate',
            self.open_in_browser,
            'https://twitter.com/atareao')
        twitter_item.show()
        help_menu.append(twitter_item)
        #
        mastodon_item = Gtk.MenuItem(label=_(
            'Contact me at Mastodon'))
        mastodon_item.connect(
            'activate',
            self.open_in_browser,
            'https://mastodon.social/@atareao')
        mastodon_item.show()
        help_menu.append(mastodon_item)
        #
        telegram_item = Gtk.MenuItem(label=_(
            'Contact me at Telegram'))
        telegram_item.connect(
            'activate',
            self.open_in_browser,
            'https://t.me/atareao')
        telegram_item.show()
        help_menu.append(telegram_item)
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
        """
        Loads the preferences for the weather indicator.

        This method checks if the configuration file exists. If it doesn't,
        it creates a new configuration with default values and saves it. Then,
        it prompts the user to enter their preferences using a preferences
        dialog. If the user accepts, the preferences are saved. If the user
        cancels, the program exits. After loading the configuration, the method
        retrieves the preferences for the main and second locations, and sets
        them in the `self.preferences` dictionary. It also retrieves other
        configuration values such as temperature, pressure, visibility, wind,
        snow, rain, and time format. The method then initializes the weather
        services for each location based on the preferences. Finally, it
        creates and initializes weather widgets for each location if the widget
        is enabled in the preferences.

        Returns:
            None
        """
        if not os.path.exists(comun.CONFIG_FILE):
            if internet_on():
                configuration = Configuration()
                configuration.reset()
                data = geocodeapi.get_latitude_longitude_city()
                if data:
                    configuration.set("latitude", data["lat"])
                    configuration.set("longitude", data["lon"])
                    configuration.set("location", data["city"])
                    configuration.set("timezone", data["timezone"])
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
        self.preferences[0]["show"] = configuration.get("main-location")
        self.preferences[0]["autolocation"] = configuration.get("autolocation")
        self.preferences[0]["location"] = configuration.get("location")
        self.preferences[0]["latitude"] = configuration.get("latitude")
        self.preferences[0]["longitude"] = configuration.get("longitude")
        self.preferences[0]["timezone"] = configuration.get("timezone")
        self.preferences[0]["show-temperature"] =\
            configuration.get("show-temperature")
        self.preferences[0]["show-notifications"] =\
            configuration.get("show-notifications")
        self.preferences[0]["widget"] = configuration.get("widget1")
        #
        self.preferences[1] = {}
        self.preferences[1]["show"] = configuration.get("second-location")
        self.preferences[1]["autolocation"] = False
        self.preferences[1]["location"] = configuration.get("location2")
        self.preferences[1]["latitude"] = configuration.get("latitude2")
        self.preferences[1]["longitude"] = configuration.get("longitude2")
        self.preferences[1]["timezone"] = configuration.get("timezone")
        self.preferences[1]["show-temperature"] =\
            configuration.get("show-temperature2")
        self.preferences[1]["show-notifications"] =\
            configuration.get("show-notifications2")
        self.preferences[1]["widget"] = configuration.get("widget2")
        #
        temperature = configuration.get("temperature")
        pressure = configuration.get("pressure")
        visibility = configuration.get("visibility")
        wind = configuration.get("wind")
        snow = configuration.get("snow")
        rain = configuration.get("rain")
        ampm = not configuration.get("24h")
        self.units = weatherservice.Units(temperature=temperature,
                                          wind=wind,
                                          pressure=pressure,
                                          visibility=visibility,
                                          snow=snow,
                                          rain=rain,
                                          ampm=ampm)
        for i in range(INDICATORS):
            if self.preferences[i]['show']:
                self.weatherservices[i] =\
                    wopenmeteoapi.OpenMeteoWeatherService(
                        longitude=self.preferences[i]["longitude"],
                        latitude=self.preferences[i]["latitude"],
                        timezone=self.preferences[i]["timezone"],
                        location=self.preferences[i]["location"],
                        units=self.units)
            self.menus[i]['evolution'].show()
        #
        self.icon_light = configuration.get('icon-light')
        #
        utcnow = datetime.now(timezone.utc)
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
        self.update_weather()
        self.start_looking_for_internet()

    def start_widgets_updater(self):
        """
        Starts the widgets updater.

        This method removes any existing widgets updater if it is running and
        then starts a new one.  The widgets updater periodically updates the
        widgets by calling the `update_widgets` method.

        Returns:
            None
        """
        if self.widgets_updater > 0:
            GLib.source_remove(self.widgets_updater)
        self.update_widgets()
        self.widgets_updater = GLib.timeout_add(500,
                                                self.update_widgets)

    def stop_widgets_updater(self):
        """
        Stops the updater for the widgets.

        If the updater is currently running, it will be stopped by removing the
        source.
        """
        if self.widgets_updater > 0:
            GLib.source_remove(self.widgets_updater)
            self.widgets_updater = 0

    def start_weather_updater(self):
        """
        Starts the weather updater.

        This method is responsible for starting the weather updater. It first
        checks if the weather updater is already running and if so, it removes
        the existing source. Then, it calls the `update_weather` method to
        immediately update the weather information. Finally, it schedules the
        `update_weather` method to be called periodically based on the
        `refresh` interval.

        Parameters:
        - None

        Returns:
        - None
        """
        if self.weather_updater > 0:
            GLib.source_remove(self.weather_updater)
        self.update_weather()
        self.weather_updater = GLib.timeout_add_seconds(self.refresh * 3600,
                                                        self.update_weather)

    def stop_weather_updater(self):
        """
        Stops the weather updater if it is currently running.

        If the weather updater is running, this method will stop it by
        removing the associated GLib source.
        """
        if self.weather_updater > 0:
            GLib.source_remove(self.weather_updater)
            self.weather_updater = 0

    def start_looking_for_internet(self):
        """
        Starts looking for internet connection periodically.

        If there is an existing internet updater, it is removed before
        starting a new one. The method checks if there is an internet
        connection by calling the `looking_for_internet` method.  If there is
        an internet connection, it schedules a periodic check
        using `GLib.timeout_add_seconds` with the specified time interval.

        Returns:
            None
        """
        if self.internet_updater > 0:
            GLib.source_remove(self.internet_updater)
        if self.looking_for_internet():
            self.internet_updater = GLib.timeout_add_seconds(
                TIME_TO_CHECK, self.looking_for_internet)

    def stop_looking_for_internet(self):
        """
        Stops the process of looking for internet connection.

        If the `internet_updater` is greater than 0, it removes the source
        from the GLib event loop and sets `internet_updater` to 0.

        Parameters:
            self (MyWeatherIndicator): The instance of the MyWeatherIndicator
            class.

        Returns:
            None
        """
        if self.internet_updater > 0:
            GLib.source_remove(self.internet_updater)
            self.internet_updater = 0

    def looking_for_internet(self):
        """
        Checks if there is an internet connection available.

        Returns:
            bool: True if internet is not found, False otherwise.
        """
        # code implementation
        logger.debug('*** Looking For Internet ***')
        if internet_on():
            logger.debug('*** Internet Found ***')
            self.stop_looking_for_internet()
            self.start_weather_updater()
            self.start_widgets_updater()
            return False
        logger.debug('*** Internet Not Found ***')
        self.stop_weather_updater()
        self.stop_widgets_updater()
        return True

    def on_pinit(self, _widget, _data, index):
        """
        Callback function triggered when the 'pinit' event is emitted by a
        widget.

        Args:
            _widget: The widget that emitted the event.
            _data: Additional data associated with the event.
            index: The index of the widget in the list.

        Returns:
            None
        """
        utcnow = datetime.now()
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
        """
        Create a menu for the weather indicator at the given index.

        Parameters:
        - index (int): The index of the weather indicator.

        Returns:
        - None
        """
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
            label='')
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
            label='')
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
        """
        Update the menu for a specific index.

        Parameters:
        - index (int): The index of the menu to update.

        Returns:
        - None

        Raises:
        - None

        """
        if not internet_on():
            logger.error('--- Not internet connection ---')
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
        logger.debug('--- Updating data in location %s ---', index)
        if self.preferences[index]['autolocation']:
            data = geocodeapi.get_latitude_longitude_city()
            if data:
                self.preferences[index]["latitude"] = data["lat"]
                self.preferences[index]["longitude"] = data["lon"]
                self.preferences[index]["location"] = data["city"]
                self.preferences[index]["timezone"] = data["timezone"]
                self.weatherservices[index] = \
                    wopenmeteoapi.OpenMeteoWeatherService(
                        longitude=self.preferences[index]["longitude"],
                        latitude=self.preferences[index]["latitude"],
                        location=self.preferences[index]["location"],
                        timezone=self.preferences[index]["timezone"],
                        units=self.units)
                self.menus[index]['evolution'].show()
        logger.debug('****** Updating weather')
        weather = self.weatherservices[index].get_weather()
        logger.debug('****** Updated weather')
        logger.debug(self.weathers[index])
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
            self.menus[index]['temperature'].set_label(
                f"{_('Temperature')}: "
                f"{self.current_conditions[index]['temperature']}{176:c}")
            self.menus[index]['humidity'].set_label(
                f"{_('Humidity')}: "
                f"{self.current_conditions[index]['humidity']}")
            self.menus[index]['feels_like'].set_label(
                f"{_('Feels like')}: "
                f"{self.current_conditions[index]['feels_like']}{176:c}")
            self.menus[index]['dew_point'].set_label(
                f"{_('Dew Point')}: "
                f"{self.current_conditions[index]['dew_point']}{176:c}")
            self.menus[index]['wind'].set_label(
                f"{_('Wind')}: "
                f"{self.current_conditions[index]['wind_condition']}")
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
                f"{_('Dawn')}: {self.current_conditions[index]['dawn']}")
            self.menus[index]['sunrise'].set_label(
                f"{_('Sunrise')}: {self.current_conditions[index]['sunrise']}")
            self.menus[index]['sunset'].set_label(
                f"{_('Sunset')}: {self.current_conditions[index]['sunset']}")
            self.menus[index]['dusk'].set_label(
                f"{_('Dusk')}: {self.current_conditions[index]['dusk']}")
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
            ultraviolet = (
                self.current_conditions[index]['UV'] is not None)
            precip_today = (
                self.current_conditions[index]['precipitation'] is not None)
            self.menus[index]['pressure'].set_visible(pressure)
            self.menus[index]['visibility'].set_visible(visibility)
            self.menus[index]['cloudiness'].set_visible(cloudiness)
            self.menus[index]['uv'].set_visible(ultraviolet)
            self.menus[index]['precipitation'].set_visible(precip_today)
            if pressure:
                self.menus[index]['pressure'].set_label(
                    f"{_('Pressure')}: "
                    f"{self.current_conditions[index]['pressure']}")
            if visibility:
                value = self.current_conditions[index]['visibility']
                self.menus[index]['visibility'].set_label(
                    f"{_('Visibility')}: {value}")
            if cloudiness:
                value = self.current_conditions[index]['cloudiness']
                self.menus[index]['cloudiness'].set_label(
                    f"{_('Cloudiness')}: {value}")
            if ultraviolet:
                value = self.current_conditions[index]['UV']
                self.menus[index]['uv'].set_label(
                    f"{_('UV')}: {value}")
            if precip_today:
                value = self.current_conditions[index]['precipitation']
                self.menus[index]['precipitation'].set_label(
                    f"{_('Precipitation')}: {value}")
            if self.preferences[index]['show-temperature'] is True:
                value = self.current_conditions[index]['temperature']
                self.indicators[index].set_label(f"{value}{176:c}", "100%")
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
                    str(self.current_conditions[index]['humidity']) + '\n'
                msg += _('Wind') + ': ' +\
                    self.current_conditions[index]['wind_condition'] + '\n'
                msg += self.current_conditions[index]['condition_text']
                image = os.path.join(
                    comun.IMAGESDIR,
                    self.current_conditions[index]['condition_image'])
                try:
                    self.notifications[index].update(
                        'My-Weather-Indicator',
                        msg,
                        image)
                    self.notifications[index].show()
                except Exception as exception:
                    logger.error(exception)
            while Gtk.events_pending():
                Gtk.main_iteration()
        logger.debug('--- End of updating data in location %s ---', index)
        self.last_update_time = time.time()

    def on_moon_clicked(self, _widget):
        """
        Handle the event when the moon button is clicked.

        Parameters:
        - _widget: The widget that triggered the event.

        Returns:
        None
        """
        p = CalendarWindow()
        p.show_all()

    def menu_offon(self, ison):
        """
        Enable or disable the sensitivity of various menu items based on the
        given 'ison' value.

        Parameters:
        - ison (bool): A boolean value indicating whether the menu items
        should be enabled or disabled.

        Returns:
        - None
        """
        for i in range(INDICATORS):
            self.menus[i]['forecast'].set_sensitive(ison)
            self.menus[i]['evolution'].set_sensitive(ison)
            self.menus[i]['preferences'].set_sensitive(ison)
            self.menus[i]['moon_calendar'].set_sensitive(ison)
            self.menus[i]['update'].set_sensitive(ison)

    def menu_evolution_response(self, _widget, index):
        """
        Handle the menu evolution response.

        Parameters:
        - _widget: The widget triggering the event.
        - index: The index of the weather service.

        Returns:
        None
        """
        # Rest of the code...
        configuration = Configuration()
        temperature_unit = configuration.get('temperature')
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
        subtitle = _('Weather service') + ': Open Meteo'
        graph = Graph(title, subtitle, temperature=temperatures,
                      humidity=humidities, cloudiness=cloudinesses,
                      temperature_unit=temperature_unit)
        graph.run()
        self.menu_offon(True)

    def menu_forecast_response(self, _widget, index):
        """
        Handle the menu forecast response.

        Parameters:
        - _widget: The widget triggering the event.
        - index: The index of the forecast in the preferences list.

        Returns:
        None
        """
        self.menu_offon(False)
        FC(self.preferences[index]['location'], self.weathers[index])
        self.menu_offon(True)

    def menu_set_preferences_response(self, _widget):
        """
        Handle the response from the preferences menu.

        Parameters:
        - _widget: The widget that triggered the response.

        Returns:
        None

        Description:
        This method is called when the user responds to the preferences menu.
        It disables the menu, opens the preferences dialog, saves the
        preferences if accepted, and reloads the preferences.
        Finally, it enables the menu again.
        """
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

    def menu_refresh_weather_response(self, _widget, _index):
        """
        Refreshes the weather response in the menu.

        Parameters:
        - _widget: The widget triggering the refresh.
        - _index: The index of the widget.

        Returns:
        None
        """
        if self.last_update_time + 600 < time.time():
            self.start_weather_updater()

    def menu_exit_response(self, _widget):
        """
        Handles the response when the menu exit option is selected.

        Parameters:
        - _widget: The widget that triggered the event.

        Returns:
        None
        """
        sys.exit(0)

    def menu_about_response(self, widget):
        """
        Display the About dialog for the weather indicator.

        Parameters:
        - widget: The widget that triggered the event.

        Returns:
        None
        """
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
    """
    Entry point of the My Weather Indicator application.

    This function initializes the necessary components, checks if the
    application is already running, and starts the main event loop.

    Raises:
        socket.error: If there is an error while binding the socket.
    """
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind('\0_my_weather_indicator_lock')
    except socket.error as socket_exception:
        error_code = socket_exception.args[0]
        error_string = socket_exception.args[1]
        logger.error("My Weather Indicator is already running (%s:%s). Exit",
                     error_code, error_string)
        sys.exit(1)
    logger.info(machine_information.get_information())
    logger.info("My-Weather-Indicator version: %s", comun.VERSION)
    logger.info('#####################################################')
    load_css(CSS_FILE)
    Notify.init("my-weather-indicator")
    MWI()
    Gtk.main()


if __name__ == "__main__":
    main()
    sys.exit(0)
