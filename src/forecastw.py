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
    gi.require_version('GdkPixbuf', '2.0')
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import os
import comun
import webbrowser
from comun import _
from utils import load_image



def get_image_with_text2(text, image=None):
    vbox = Gtk.VBox()
    if image:
        # image = Gtk.Image.new_from_file(os.path.join(comun.IMAGESDIR,image))
        image = load_image(os.path.join(comun.IMAGESDIR, image))
        image.set_alignment(0.5, 0.5)
        vbox.pack_start(image, True, True, 0)
    label = Gtk.Label.new(text)
    label.set_alignment(0.5, 0.5)
    vbox.pack_start(label, True, True, 0)
    return vbox


def get_image_with_text(text, image=None):
    hbox = Gtk.HBox()
    if image:
        image = load_image(os.path.join(comun.IMAGESDIR, image))
        # image = Gtk.Image.new_from_file(image)
        image.set_alignment(1, 0.5)
        hbox.pack_start(image, True, True, 0)
    label = Gtk.Label.new(text)
    label.set_alignment(0, 0.5)
    hbox.pack_start(label, True, True, 0)
    return hbox


class FC(Gtk.Dialog):
    def __init__(self, location, ws, weather):
        Gtk.Dialog.__init__(self, 'my-weather-indicator | ' + _('Forecast'))
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        self.connect('destroy', self.close_application)
        self.set_icon_from_file(comun.ICON)
        vbox0 = Gtk.VBox(spacing=5)
        vbox0.set_border_width(5)
        self.get_content_area().add(vbox0)
        label11 = Gtk.Label(label='<b>' + location + '</b>')
        label11.set_markup('<b>' + location + '</b>')
        vbox0.pack_start(label11, True, True, 0)
        frame = Gtk.Frame()
        vbox0.add(frame)
        hbox1 = Gtk.HBox(spacing=5)
        hbox1.set_border_width(5)
        frame.add(hbox1)
        self.ws = ws
        forecast = weather['forecasts']
        self.table = Gtk.Table(rows=9, columns=5, homogeneous=False)
        self.table.set_col_spacings(10)
        self.create_labels()
        if self.ws == 'yahoo':
            total = 2
        if self.ws == 'wunderground':
            total = 4
        else:
            total = 5
        for i in range(0, total):
            self.create_forecast_dor_day(forecast, i)
        hbox1.add(self.table)
        #
        if self.ws == 'yahoo':
            filename = comun.YAHOOLOGO
            web = comun.YAHOOWEB
        elif self.ws == 'worldweatheronline':
            filename = comun.WOLRDWEATHERONLINE
            web = comun.WOLRDWEATHERONLINEWEB
        elif self.ws == 'openweathermap':
            filename = comun.OPENWEATHERMAPLOGO
            web = comun.OPENWEATHERMAPWEB
        elif self.ws == 'wunderground':
            filename = comun.UNDERGROUNDLOGO
            web = comun.UNDERGROUNDWEB
        image = load_image(filename, size=64)
        image.set_alignment(0.5, 0.5)
        button = Gtk.Button()
        button.set_image(image)
        button.connect('clicked', (lambda x: webbrowser.open(web)))
        hbox1.pack_start(button, True, True, 0)
        #
        self.show_all()

        while Gtk.events_pending():
            Gtk.main_iteration()
        self.run()
        self.destroy()

    def close_application(self, widget):
        self.destroy()

    def create_labels(self):
        label1 = Gtk.Label.new(_('Day of week'))
        label1.set_alignment(0, 0.5)
        self.table.attach(label1, 0, 1, 0, 1,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.EXPAND,
                          xpadding=0,
                          ypadding=5)
        label6 = Gtk.Label.new(_('Sunrise'))
        label6.set_alignment(0, 0.5)
        self.table.attach(label6, 0, 1, 1, 2,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.EXPAND,
                          xpadding=0,
                          ypadding=5)
        label7 = Gtk.Label.new(_('Sunset'))
        label7.set_alignment(0, 0.5)
        self.table.attach(label7, 0, 1, 2, 3,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.EXPAND,
                          xpadding=0,
                          ypadding=5)
        label8 = Gtk.Label.new(_('Moon Phase'))
        label8.set_alignment(0, 0.5)
        self.table.attach(label8, 0, 1, 3, 5,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.EXPAND,
                          xpadding=0,
                          ypadding=5)
        label2 = Gtk.Label.new(_('Condition'))
        label2.set_alignment(0, 0.5)
        self.table.attach(label2, 0, 1, 5, 7,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.EXPAND,
                          xpadding=0,
                          ypadding=5)
        label4 = Gtk.Label.new(_('High temperature'))
        label4.set_alignment(0, 0.5)
        self.table.attach(label4, 0, 1, 7, 8,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.EXPAND,
                          xpadding=0,
                          ypadding=5)
        label5 = Gtk.Label.new(_('Low temperature'))
        label5.set_alignment(0, 0.5)
        self.table.attach(label5, 0, 1, 8, 9,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.EXPAND,
                          xpadding=0,
                          ypadding=5)
        if self.ws == 'wunderground':
            label = Gtk.Label.new(_('Maximum wind'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 9, 10,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(_('Average wind'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 10, 11,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(_('Maximum humidity'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 11, 12,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(_('Minumum humidity'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 12, 13,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(_('Rain measurement'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 13, 14,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(_('Snow measurement'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 14, 15,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)
        elif self.ws == 'worldweatheronline':
            label = Gtk.Label.new(_('Average wind'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 9, 10,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(_('Rain measurement'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 10, 11,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)
        elif self.ws == 'openweathermap':
            label = Gtk.Label.new(_('Average wind'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 9, 10,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(_('Average humidity'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 10, 11,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(_('Cloudiness'))
            label.set_alignment(0, 0.5)
            self.table.attach(label, 0, 1, 11, 12,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.EXPAND,
                              xpadding=0,
                              ypadding=5)

    def create_forecast_dor_day(self, forecast, day):
        fr = day + 1
        lr = fr + 1
        label1 = Gtk.Label.new(forecast[day]['day_of_week'])
        self.table.attach(label1, fr, lr, 0, 1,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.FILL,
                          xpadding=0,
                          ypadding=5)
        label = get_image_with_text(forecast[day]['sunrise'],
                                    os.path.join(comun.IMAGESDIR,
                                                 'mwig-clear.png'))
        self.table.attach(label, fr, lr, 1, 2,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.FILL,
                          xpadding=0,
                          ypadding=5)
        label = get_image_with_text(forecast[day]['sunset'],
                                    os.path.join(comun.IMAGESDIR,
                                                 'mwig-clear-night.png'))
        self.table.attach(label, fr, lr, 2, 3,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.FILL,
                          xpadding=0,
                          ypadding=5)
        image8 = Gtk.Image.new_from_file(
            os.path.join(comun.IMAGESDIR, forecast[day]['moon_icon']))
        self.table.attach(image8, fr, lr, 3, 4,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.FILL,
                          xpadding=0,
                          ypadding=5)
        label9 = Gtk.Label.new(forecast[day]['moon_phase'])
        self.table.attach(label9, fr, lr, 4, 5,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.FILL,
                          xpadding=0,
                          ypadding=5)
        image2 = load_image(
            os.path.join(comun.WIMAGESDIR,
                         forecast[day]['condition_image']), 64)
        self.table.attach(image2, fr, lr, 5, 6,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.FILL,
                          xpadding=0,
                          ypadding=5)
        label3 = Gtk.Label.new(forecast[day]['condition_text'])
        self.table.attach(label3, fr, lr, 6, 7,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.FILL,
                          xpadding=0,
                          ypadding=5)
        label = get_image_with_text(
            '{0}{1:c}'.format(forecast[day]['high'], 176),
            os.path.join(comun.IMAGESDIR, 'mwi-arrow-hot.png'))
        self.table.attach(label, fr, lr, 7, 8,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.FILL,
                          xpadding=0,
                          ypadding=5)
        label = get_image_with_text(
            '{0}{1:c}'.format(forecast[day]['low'], 176),
            os.path.join(comun.IMAGESDIR, 'mwi-arrow-cold.png'))
        self.table.attach(label, fr, lr, 8, 9,
                          xoptions=Gtk.AttachOptions.FILL,
                          yoptions=Gtk.AttachOptions.FILL,
                          xpadding=0,
                          ypadding=5)

        if self.ws == 'wunderground'	:
            label = Gtk.Label.new(forecast[day]['maxwind'])
            self.table.attach(label, fr, lr, 9, 10,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(forecast[day]['avewind'])
            self.table.attach(label, fr, lr, 10, 11,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)
            label = get_image_with_text(
                forecast[day]['maxhumidity'],
                os.path.join(comun.IMAGESDIR, 'mwi-arrow-hot.png'))
            self.table.attach(label, fr, lr, 11, 12,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)
            label = get_image_with_text(
                forecast[day]['minhumidity'],
                os.path.join(comun.IMAGESDIR, 'mwi-arrow-cold.png'))
            self.table.attach(label, fr, lr, 12, 13,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(forecast[day]['qpf_allday'])
            self.table.attach(label, fr, lr, 13, 14,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(forecast[day]['snow_allday'])
            self.table.attach(label, fr, lr, 14, 15,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)
        elif self.ws == 'worldweatheronline':
            label = get_image_with_text2(forecast[day]['avewind'],
                                         forecast[day]['wind_icon'])
            self.table.attach(label, fr, lr, 9, 10,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(forecast[day]['qpf_allday'])
            self.table.attach(label, fr, lr, 10, 11,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)
        elif self.ws == 'openweathermap':
            label = get_image_with_text2(forecast[day]['avewind'],
                                         forecast[day]['wind_icon'])
            self.table.attach(label, fr, lr, 9, 10,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)
            label = Gtk.Label.new(forecast[day]['avehumidity'])
            self.table.attach(label, fr, lr, 10, 11,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)
            label = get_image_with_text(
                forecast[day]['cloudiness'],
                os.path.join(comun.IMAGESDIR, 'mwig-cloudy.png'))
            self.table.attach(label, fr, lr, 11, 12,
                              xoptions=Gtk.AttachOptions.FILL,
                              yoptions=Gtk.AttachOptions.FILL,
                              xpadding=0,
                              ypadding=5)


if __name__ == "__main__":
    cm = FC()
    exit(0)
