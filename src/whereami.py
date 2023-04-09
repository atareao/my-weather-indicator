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

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GLib', '2.0')
    gi.require_version('WebKit2', '4.0')
except ValueError as e:
    print(e)
    exit(-1)
from gi.repository import Gtk  # pyright: ignore
from gi.repository import Gdk  # pyright: ignore
from gi.repository import WebKit2  # pyright: ignore
from asyncf import async_function
import json
import comun
import geocodeapi
from comun import _
from basedialog import BaseDialog
import logging
import sys
import os

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOGLEVEL", "DEBUG"))
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class WhereAmI(BaseDialog):
    def __init__(self, parent=None, location="Silla", latitude=39.36667,
                 longitude=-0.41667, timezone="Europe/Madrid"):
        BaseDialog.__init__(self, 'my-weather-indicator | ' + _('Where Am I'),
                            parent)
        self.set_location(location)
        self.set_timezone(timezone)
        self.set_position(latitude, longitude)

        self.set_wait_cursor()
        if latitude and longitude and (location is None or location == ""):
            self.do_search_location(latitude, longitude)
        else:
            self.do_center()

        logger.info(f"location: {self._location}, latitude: {self._latitude}"
                    ", longitude={self._longitude}")
        self.set_normal_cursor()

    def init_ui(self):
        BaseDialog.init_ui(self)
        #
        self.grid = Gtk.Grid()
        self.set_content(self.grid)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        self.grid.attach(vbox, 0, 0, 1, 1)

        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        vbox.pack_start(hbox, False, False, 0)
        #
        self.entry1 = Gtk.Entry()
        self.entry1.set_width_chars(60)

        self.entry1.set_property('primary_icon_name', 'edit-find-symbolic')
        self.entry1.set_property('secondary_icon_name', 'edit-clear-symbolic')
        self.entry1.set_property('primary_icon_tooltip_text',
                                 _('Search location'))
        self.entry1.set_property('secondary_icon_tooltip_text',
                                 _('Clear location'))
        self.entry1.set_tooltip_text(_('Input the name of your city'))
        self.entry1.connect('icon-press', self.on_icon_press)
        self.entry1.connect('activate', self.on_button1_clicked)
        hbox.pack_start(self.entry1, True, True, 0)
        #
        button1 = Gtk.Button.new_with_label(_('Search'))
        button1.connect('clicked', self.on_button1_clicked)
        hbox.pack_start(button1, False, False, 0)
        #
        button2 = Gtk.Button.new_with_label(_('Find me'))
        button2.connect('clicked', self.on_button2_clicked)
        hbox.pack_start(button2, False, False, 0)
        self.expander = Gtk.Expander(label=_('Locations found'))
        self.expander.set_expanded(False)
        vbox.pack_start(self.expander, False, False, 0)
        #
        frame = Gtk.Frame()
        framebox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 50)
        framebox.add(frame)
        self.expander.add(framebox)
        self.expander.connect("notify::expanded", self.on_expander_expanded)
        #
        scrolledwindow0 = Gtk.ScrolledWindow()
        scrolledwindow0.set_policy(Gtk.PolicyType.AUTOMATIC,
                                   Gtk.PolicyType.AUTOMATIC)
        scrolledwindow0.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        scrolledwindow0.set_size_request(450, 100)
        frame.add(scrolledwindow0)
        # city, county, country, latitude, longitude, timezone
        store = Gtk.ListStore(str, str, str, float, float, str)
        store.set_sort_column_id(2, Gtk.SortType.ASCENDING)
        self.treeview = Gtk.TreeView(model=store)
        self.treeview.set_reorderable(True)
        treeviewcolumn0 = Gtk.TreeViewColumn(_('City'),
                                             Gtk.CellRendererText(), text=0)
        treeviewcolumn0.set_reorderable(True)
        treeviewcolumn0.set_sort_column_id(0)
        treeviewcolumn1 = Gtk.TreeViewColumn(_('State'),
                                             Gtk.CellRendererText(), text=1)
        treeviewcolumn1.set_reorderable(True)
        treeviewcolumn1.set_sort_column_id(1)
        treeviewcolumn2 = Gtk.TreeViewColumn(_('Country'),
                                             Gtk.CellRendererText(), text=2)
        treeviewcolumn2.set_reorderable(True)
        treeviewcolumn2.set_sort_column_id(2)
        self.treeview.append_column(treeviewcolumn0)
        self.treeview.append_column(treeviewcolumn1)
        self.treeview.append_column(treeviewcolumn2)
        self.treeview.connect('cursor-changed',
                              self.ontreeviewcursorchanged)
        scrolledwindow0.add(self.treeview)
        #
        #
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                  Gtk.PolicyType.AUTOMATIC)
        scrolledwindow.set_shadow_type(Gtk.ShadowType.IN)
        vbox.pack_start(scrolledwindow, True, True, 0)
        #
        self.viewer = WebKit2.WebView()
        scrolledwindow.add(self.viewer)
        scrolledwindow.set_size_request(900, 600)
        self.viewer.connect('load-changed', self.load_changed)
        self.viewer.connect('notify::title', self.on_title_changed)
        logger.debug(f"File: {comun.HTML_WAI}")
        self.viewer.load_uri('file://' + comun.HTML_WAI)
        self.set_focus(self.viewer)

    def on_expander_expanded(self, widget, selected):
        logger.info(f"{widget}, {selected}")
        if not self.expander.get_expanded():
            self.resize(450, 350)

    def on_title_changed(self, widget, data):
        logger.debug("on_title_changed")
        logger.debug(data)
        logger.debug(self.viewer.get_title())
        self.expander.set_expanded(False)
        model = self.treeview.get_model()
        model.clear()
        data = json.loads(self.viewer.get_title())
        latitude = data["latitude"] if "latitude" in data.keys() else None
        longitude = data["longitude"] if "longitude" in data.keys() else None
        logger.debug(f"{latitude},{longitude}")
        if latitude and longitude:
            logger.debug(f"{latitude},{longitude}")
            self.do_search_location(latitude, longitude)

    def ontreeviewcursorchanged(self, treeview):
        logger.info("ontreeviewcursorchanged")
        selection = treeview.get_selection()
        if selection is not None:
            model, aiter = treeview.get_selection().get_selected()
            if model is not None and aiter is not None:
                self.set_location(model[aiter][0])
                self.set_position(model[aiter][3], model[aiter][4])
                self.set_timezone(model[aiter][5])

    def on_icon_press(self, widget, icon_pos, event):  # pyright: ignore
        if icon_pos == Gtk.EntryIconPosition.PRIMARY:
            self.on_button1_clicked(None)
        elif icon_pos == Gtk.EntryIconPosition.SECONDARY:
            self.entry1.set_text('')

    def on_permission_request(
            self, widget, frame, geolocationpolicydecision):  # pyright: ignore
        WebKit2.geolocation_policy_allow(geolocationpolicydecision)
        return True

    def on_button2_clicked(self, widget):  # pyright: ignore
        self.do_center()

    def do_center(self):
        def on_center_done(result, error):  # pyright: ignore
            logger.info(result)
            if result is not None:
                model = self.treeview.get_model()
                model.clear()
                self.expander.set_expanded(True)
                self.entry1.set_text("")
                model.append([result['city'], result['regionName'],
                              result['country'], result['lat'],
                              result['lon'], result["timezone"]])
                self.set_location(result["city"])
                self.set_position(result["lat"], result["lon"])
                self.set_timezone(result["timezone"])

                if len(model) > 0:
                    self.treeview.set_cursor(0)
                self.set_normal_cursor()

        @async_function(on_done=on_center_done)
        def do_center_in_thread():
            return geocodeapi.get_latitude_longitude_city()

        self.set_wait_cursor()
        do_center_in_thread()

    def on_button1_clicked(self, widget):  # pyright: ignore
        logger.debug("on_button1_clicked")
        self.set_wait_cursor()
        search_string = self.entry1.get_text()
        model = self.treeview.get_model()
        model.clear()
        self.expander.set_expanded(True)
        self.entry1.set_text("")
        logger.debug(f"Search for {search_string}")
        for direction in geocodeapi.get_directions(search_string):
            logger.debug(direction)
            if 'name' in direction.keys() and direction['name']:
                if "admin1" in direction.keys():
                    admin1 = direction["admin1"]
                else:
                    admin1 = ""
                model.append([direction['name'], admin1,
                              direction['country'], direction['latitude'],
                              direction['longitude'], direction["timezone"]])
                if self.entry1.get_text() == "":
                    self.set_location(direction["name"])
                    self.set_position(direction["latitude"],
                                      direction["longitude"])
                    self.set_timezone(direction["timezone"])

        if len(model) > 0:
            self.treeview.set_cursor(0)

        self.set_normal_cursor()

    def do_search_location(self, latitude, longitude):
        logger.debug("do_search_location")

        def on_search_location_done(result, error):  # pyright: ignore
            logger.debug("on_search_location_done")
            logger.debug(result)
            if result is not None:
                city = result["city"] if result["city"] else result["locality"]
                self.set_location(city)
                self.set_position(result["latitude"], result["longitude"])
            self.set_normal_cursor()

        @async_function(on_done=on_search_location_done)
        def do_search_location_in_thread(latitude, longitude):
            return geocodeapi.get_inv_direction(latitude, longitude)
        self.set_wait_cursor()
        do_search_location_in_thread(latitude, longitude)

    def on_close_application(self, widget):  # pyright: ignore
        self.set_normal_cursor()
        self.hide()

    def get_data(self):
        return self._latitude, self._longitude, self._location, self._timezone

    def set_timezone(self, timezone):
        logger.debug(f"Set timezone: {timezone}")
        self._timezone = timezone

    def set_location(self, location):
        logger.debug(f"Set location: {location}")
        self._location = location
        self.entry1.set_text(location)

    def set_position(self, latitude, longitude):
        logger.debug(f"Set position: {latitude}, {longitude}")
        self._latitude = latitude
        self._longitude = longitude
        self.web_send(f"setPosition({self._latitude}, {self._longitude});")

    def set_wait_cursor(self):
        Gdk.Screen.get_default().get_root_window().set_cursor(
            Gdk.Cursor(Gdk.CursorType.WATCH))
        while Gtk.events_pending():
            Gtk.main_iteration()

    def set_normal_cursor(self):
        Gdk.Screen.get_default().get_root_window().set_cursor(
            Gdk.Cursor(Gdk.CursorType.ARROW))
        while Gtk.events_pending():
            Gtk.main_iteration()

    def load_changed(self, widget, load_event):  # pyright: ignore
        if load_event == WebKit2.LoadEvent.FINISHED:
            logger.debug(f"setPosition({self._latitude}, {self._longitude});")
            self.web_send(f"setPosition({self._latitude}, {self._longitude});")

    def web_send(self, msg):
        logger.debug(msg)
        self.viewer.evaluate_javascript(msg, len(msg), None, "localhost", None)
        while Gtk.events_pending():
            Gtk.main_iteration()


if __name__ == '__main__':
    cm = WhereAmI()
    if cm.run() == Gtk.ResponseType.ACCEPT:
        logger.info(cm.get_data())
    cm.hide()
    cm.destroy()
    exit(0)
