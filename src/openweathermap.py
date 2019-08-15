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
from json import loads as from_json
import comun


class ForecastMap(Gtk.Dialog):
    def __init__(self, lat=39.36873, lon=-2.417274645879):
        self.images = {}
        self.echo = True
        Gtk.Dialog.__init__(self)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_title(comun.APP)
        self.set_default_size(900, 600)
        self.set_icon_from_file(comun.ICON)
        self.connect('destroy', self.close_application)
        #
        vbox = Gtk.VBox(spacing=5)
        self.get_content_area().add(vbox)
        hbox1 = Gtk.HBox()
        vbox.pack_start(hbox1, True, True, 0)
        self.scrolledwindow1 = Gtk.ScrolledWindow()
        self.scrolledwindow1.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolledwindow1.set_shadow_type(Gtk.ShadowType.IN)
        hbox1.pack_start(self.scrolledwindow1, True, True, 0)
        self.viewer = WebKit2.WebView()
        self.scrolledwindow1.add(self.viewer)
        self.scrolledwindow1.set_size_request(900, 600)
        self.viewer.connect('load-changed', self.load_changed)
        self.viewer.load_uri('file://' + comun.HTML)
        self.lat = lat
        self.lon = lon
        self.set_focus(self.viewer)
        self.show_all()
        while Gtk.events_pending():
            Gtk.main_iteration()
        self.show_all()
        self.run()
        self.destroy() 

    def load_changed(self, widget, load_event):
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.web_send('setPosition({}, {})'.format(self.lat, self.lon)) 

    def web_send(self, msg):
        print('send: %s' % (msg))
        self.viewer.run_javascript(msg, None, None, None)
        while Gtk.events_pending():
            Gtk.main_iteration()
 
    def close_application(self, widget):
        self.destroy()


if __name__ == '__main__':
    forecastmap = ForecastMap(39.36873, -2.417274645879)
