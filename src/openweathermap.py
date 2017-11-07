#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
#
# OpenWeatherMap
#
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
#
#
from gi.repository import Gtk
from gi.repository import WebKit
from gi.repository import GObject

from json import dumps as to_json
from json import loads as from_json
import sys
import queue
import comun

from comun import _


class ForecastMap(Gtk.Dialog):
    def __init__(self, lat=39.36873, lon=-2.417274645879, units='F'):
        self.images = {}
        self.echo = True
        Gtk.Window.__init__(self)
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
        self.viewer = WebKit.WebView()
        self.scrolledwindow1.add(self.viewer)
        self.scrolledwindow1.set_size_request(900, 600)
        self.viewer.connect('title-changed', self.title_changed)
        self.viewer.open('file://' + comun.HTML)
        self.lat = lat
        self.lon = lon
        self.units = units
        self.set_focus(self.viewer)
        self.show_all()
        self.message_queue = queue.Queue()
        while Gtk.events_pending():
            Gtk.main_iteration()
        self.show_all()
        self.inicialize()
        self.run()
        self.destroy()

    # ###################################################################
    # #########################ENGINE####################################
    # ###################################################################
    def inicialize(self):
        self.web_send('mlat=%s;' % (self.lat))
        self.web_send('mlon=%s;' % (self.lon))
        self.web_send('munits="%s";' % (self.units))

    def work(self):
        while Gtk.events_pending():
            Gtk.main_iteration()
        again = False
        msg = self.web_recv()
        if msg:
            try:
                msg = from_json(msg)
                print('This is the message %s' % (msg))
            except:
                msg = None
            again = True
        if msg == 'exit':
            self.close_application(None)

    # ###################################################################
    # ########################BROWSER####################################
    # ###################################################################

    def title_changed(self, widget, frame, title):
        if title != 'null':
            self.message_queue.put(title)
            self.work()

    def web_recv(self):
        if self.message_queue.empty():
            return None
        else:
            msg = self.message_queue.get()
            print('recivied: %s' % (msg))
            return msg

    def web_send(self, msg):
        print('send: %s' % (msg))
        self.viewer.execute_script(msg)

    # ###################################################################
    # ########################ACTIONS####################################
    # ###################################################################

    def close_application(self, widget):
        self.destroy()


if __name__ == '__main__':
    forecastmap = ForecastMap(39.36873, -2.417274645879)
