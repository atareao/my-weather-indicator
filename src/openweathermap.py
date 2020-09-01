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
    gi.require_version('WebKit2', '4.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import WebKit2
from basedialog import BaseDialog
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
