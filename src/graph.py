#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of my-weather-indicator
#
# Copyright (c) 2012-2019 Lorenzo Carbonell Cerezo <a.k.a. atareao>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
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
    gi.require_version('WebKit2', '4.0')
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import WebKit2
import comun
from basedialog import BaseDialog


class Graph(BaseDialog):
    def __init__(self, title='', subtitle='', temperature='', humidity='',
                 cloudiness=''):
        self.title = title
        self.subtitle = subtitle
        self.humidity = humidity
        self.cloudiness = cloudiness
        self.temperature = temperature
        BaseDialog.__init__(self, title, None, ok_button=False,
            cancel_button=False)

    def init_ui(self):
        BaseDialog.init_ui(self)

        self.scrolledwindow1 = Gtk.ScrolledWindow()
        self.scrolledwindow1.set_policy(Gtk.PolicyType.AUTOMATIC,
                                        Gtk.PolicyType.AUTOMATIC)
        self.grid.attach(self.scrolledwindow1, 0, 0, 1, 1)

        self.viewer = WebKit2.WebView()
        self.scrolledwindow1.add(self.viewer)
        self.scrolledwindow1.set_size_request(900, 600)
        print(comun.HTML_GRAPH)
        self.viewer.load_uri('file://' + comun.HTML_GRAPH)
        self.viewer.connect('load-changed', self.load_changed)
        self.set_focus(self.viewer)

    def update(self):
        self.web_send('title="{}";subtitle="{}";humidity={};cloudiness={};\
            temperature={};draw_graph(title,subtitle,temperature,humidity,\
                cloudiness);'.format(self.title, self.subtitle, self.humidity,
                                  self.cloudiness, self.temperature))

    def load_changed(self, widget, load_event):
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.update()
            while Gtk.events_pending():
                Gtk.main_iteration()

    def web_send(self, msg):
        self.viewer.run_javascript(msg, None, None, None)


if __name__ == '__main__':
    title = 'Titulo'
    subtitle = 'Subtitulo'
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
    graph.run()
