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

from gi.repository import Gtk
from gi.repository import WebKit2
from json import loads as from_json
import queue
import comun


class Graph(Gtk.Dialog):
    def __init__(self, title='', subtitle='', temperature='', humidity='',
                 cloudiness=''):
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
        #
        self.scrolledwindow1 = Gtk.ScrolledWindow()
        self.scrolledwindow1.set_policy(Gtk.PolicyType.AUTOMATIC,
                                        Gtk.PolicyType.AUTOMATIC)
        self.scrolledwindow1.set_shadow_type(Gtk.ShadowType.IN)
        hbox1.pack_start(self.scrolledwindow1, True, True, 0)
        #
        self.viewer = WebKit2.WebView()
        self.scrolledwindow1.add(self.viewer)
        self.scrolledwindow1.set_size_request(900, 600)
        self.viewer.connect('load-changed', self.load_changed)
        self.viewer.load_uri('file://' + comun.HTML_GRAPH)
        #
        self.title = title
        self.subtitle = subtitle
        self.humidity = humidity
        self.cloudiness = cloudiness
        self.temperature = temperature
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
        self.web_send('title="%s";subtitle="%s";humidity=%s;cloudiness=%s;temperature=%s;draw_graph(title,subtitle,humidity,cloudiness,temperature);'%(self.title,self.subtitle,self.humidity,self.cloudiness,self.temperature))
        pass
    # ###################################################################
    # ########################BROWSER####################################
    # ###################################################################

    def load_changed(self, widget, load_event):
        print(load_event)
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.web_send('title="%s";subtitle="%s";humidity=%s;\
cloudiness=%s;temperature=%s;draw_graph(title,subtitle,temperature,humidity,\
cloudiness);' % (self.title, self.subtitle, self.humidity, self.cloudiness,
                            self.temperature))
            while Gtk.events_pending():
                Gtk.main_iteration()

    def web_send(self, msg):
        print('send: %s' % (msg))
        self.viewer.run_javascript(msg, None, None, None)

    # ###################################################################
    # ########################ACTIONS####################################
    # ###################################################################
    def close_application(self, widget):
        self.destroy()


if __name__ == '__main__':
    title = 'Titulo'
    subtitle = 'Subtitle'
    temperature = [[1376734856, 10], [1387534856, 12], [1398334856, 15],
                   [1409134856, 16], [1419934856, 20], [1430734856, 30],
                   [1441534856, 25], [1452334856, 20], [1463134856, 12],
                   [1473934856, 12], [1484734856, 12], [1495534856, 20],
                   [1506334856, 25], [1517134856, 30], [1527934856, 33]]
    humidity = [[1376734856, 30], [1387534856, 30], [1398334856, 35],
                [1409134856, 40], [1419934856, 45], [1430734856, 50],
                [1441534856, 45], [1452334856, 40], [1463134856, 35],
                [1473934856, 30], [1484734856, 20], [1495534856, 20],
                [1506334856, 35], [1517134856, 40], [1527934856, 50]]
    cloudiness = [[1376734856, 0], [1387534856, 0], [1398334856, 0],
                  [1409134856, 10], [1419934856, 20], [1430734856, 30],
                  [1441534856, 40], [1452334856, 50], [1463134856, 60],
                  [1473934856, 70], [1484734856, 100], [1495534856, 100],
                  [1506334856, 100], [1517134856, 0], [1527934856, 0]]
    graph = Graph(title, subtitle, temperature, humidity, cloudiness)
