#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# OpenWeatherMap
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

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('WebKit2', '4.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import WebKit2
from basedialog import BaseDialog
from json import loads as from_json
from comun import _
import comun


class ForecastMap(BaseDialog):
    def __init__(self, lat=39.36873, lon=-2.417274645879):
        self.lat = lat
        self.lon = lon
        BaseDialog.__init__(self, _('Forecast'), ok_button=False,
                            cancel_button=False)


    def init_ui(self):
        BaseDialog.init_ui(self)
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.grid.attach(scrolledwindow, 0, 0, 1, 1)
        self.viewer = WebKit2.WebView()
        scrolledwindow.add(self.viewer)
        scrolledwindow.set_size_request(900, 600)
        self.viewer.connect('load-changed', self.load_changed)
        self.viewer.load_uri('file://' + comun.HTML)
        self.set_focus(self.viewer)

    def load_changed(self, widget, load_event):
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.web_send('setPosition({}, {})'.format(self.lat, self.lon)) 

    def web_send(self, msg):
        self.viewer.run_javascript(msg, None, None, None)
        while Gtk.events_pending():
            Gtk.main_iteration()
 
    def close_application(self, widget):
        self.destroy()


if __name__ == '__main__':
    forecastmap = ForecastMap(39.36873, -2.417274645879)
    forecastmap.run()
