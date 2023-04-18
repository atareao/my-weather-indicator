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
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk  # pyright: ignore
import os
import comun
from comun import _
from utils import load_image
from basedialog import BaseDialog


def get_image_with_text2(text, image=None, impar=False):
    vbox = Gtk.VBox()
    vbox.set_name('forecast' if impar is not False else 'forecasti')
    if image:
        image = load_image(os.path.join(comun.IMAGESDIR, image))
        if image:
            image.set_size_request(40, 40)
            image.set_alignment(0.5, 0.5)
            vbox.pack_start(image, True, True, 0)
    label = Gtk.Label.new(text)
    label.set_size_request(10, 20)
    label.set_alignment(0.5, 0.5)
    vbox.pack_start(label, True, True, 0)
    return vbox


def get_image_with_text(text, image_name="", impar=False):
    hbox = Gtk.HBox()
    hbox.set_name('forecast' if impar is not False else 'forecasti')
    image_file = os.path.join(comun.IMAGESDIR, image_name)
    if image_name:
        image = load_image(image_file)
        if image:
            image.set_alignment(1, 0.5)
            hbox.pack_start(image, True, True, 0)
    label = Gtk.Label.new(text)
    label.set_alignment(0, 0.5)
    hbox.pack_start(label, True, True, 0)
    return hbox


class FC(BaseDialog):
    def __init__(self, location, weather):
        title = comun.APPNAME + ' | ' + _('Forecast')
        self.location = location
        self.weather = weather
        BaseDialog.__init__(self, title, ok_button=False, cancel_button=False)

    def init_ui(self):
        BaseDialog.init_ui(self)
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(0)
        self.grid.set_column_spacing(0)
        self.set_content(self.grid)
        forecast = self.weather['forecasts']
        self.table = Gtk.Table(rows=9, columns=5, homogeneous=False)
        self.table.set_col_spacings(10)
        self.create_labels()
        for i in range(0, 5):
            self.create_forecast_dor_day(forecast, i)

    def close_application(self, widget):  # pyright: ignore
        self.destroy()

    def create_labels(self):
        labels = [_('Day of week'), _('Sunrise'), _('Sunset'), _('Moon Phase'),
                  _('Condition'), _('High temperature'), _('Low temperature')]
        labels.extend([_('Average wind'), _('Average humidity'),
                       _('Cloudiness')])
        for index, name in enumerate(labels):
            label = Gtk.Label.new(name)
            label.set_name('forecasti')
            label.set_alignment(index, 0.5)
            label.set_size_request(10, 20)
            self.grid.attach(label, 0, index, 1, 1)

    def create_forecast_dor_day(self, forecast, day):
        fr = day + 1
        label = Gtk.Label.new(forecast[day]['day_of_week'])
        label.set_name('forecasti')
        label.set_width_chars(20)
        self.grid.attach(label, fr, 0, 1, 1)
        label = get_image_with_text(forecast[day]['sunrise'],
                                    os.path.join(comun.IMAGESDIR,
                                                 'mwig-clear.png'),
                                    fr % 2 == 1)
        self.grid.attach(label, fr, 1, 1, 1)
        label = get_image_with_text(forecast[day]['sunset'],
                                    os.path.join(comun.IMAGESDIR,
                                                 'mwig-clear-night.png'),
                                    fr % 2 == 1)
        self.grid.attach(label, fr, 2, 1, 1)

        label = get_image_with_text2(forecast[day]['moon_phase'],
                                     os.path.join(comun.IMAGESDIR,
                                                  forecast[day]['moon_icon']),
                                     fr % 2 == 1)
        self.grid.attach(label, fr, 3, 1, 1)
        label = get_image_with_text2(
            forecast[day]['condition_text'],
            os.path.join(comun.IMAGESDIR, forecast[day]['condition_image']),
            fr % 2 == 1)
        self.grid.attach(label, fr, 4, 1, 1)
        label = get_image_with_text(
            '{0}{1:c}'.format(forecast[day]['high'], 176),
            os.path.join(comun.IMAGESDIR, 'mwi-arrow-hot.png'), fr % 2 == 1)
        self.grid.attach(label, fr, 5, 1, 1)
        label = get_image_with_text(
            '{0}{1:c}'.format(forecast[day]['low'], 176),
            os.path.join(comun.IMAGESDIR, 'mwi-arrow-cold.png'), fr % 2 == 1)
        self.grid.attach(label, fr, 6, 1, 1)
        label = get_image_with_text2(forecast[day]['avewind'],
                                     forecast[day]['wind_icon'],
                                     fr % 2 == 1)
        self.grid.attach(label, fr, 7, 1, 1)
        label = Gtk.Label.new(forecast[day]['avehumidity'])
        label.set_name('forecast' if fr % 2 == 1 else 'forecasti')
        self.grid.attach(label, fr, 8, 1, 1)
        label = get_image_with_text(
            forecast[day]['cloudiness'],
            os.path.join(comun.IMAGESDIR, 'mwig-cloudy.png'), fr % 2 == 1)
        self.grid.attach(label, fr, 9, 1, 1)
