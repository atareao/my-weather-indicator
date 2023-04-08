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
    gi.require_version('GdkPixbuf', '2.0')
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk  # pyright: ignore
from gi.repository import GdkPixbuf  # pyright: ignore
import os
import comun
from moon import Moon


class MoonDayWidget(Gtk.EventBox):

    def __init__(self, adate=None):
        Gtk.EventBox.__init__(self)
        self.set_size_request(100, 70)
        self.box1 = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.add(self.box1)
        self.label = Gtk.Label()
        self.box1.pack_start(self.label, True, True, padding=1)
        self.image = Gtk.Image()
        self.box1.pack_start(self.image, True, True, padding=1)
        if adate is not None:
            self.set_date(adate)
        self.image.show()

    def set_style(self, box_name):
        self.box1.set_name(box_name)

    def set_date(self, adate):
        self.adate = adate
        self.label.set_text(str(adate.day))
        self.moon = Moon(adate)
        self.image.set_from_pixbuf(
            GdkPixbuf.Pixbuf.new_from_file_at_size(
                os.path.join(
                    comun.IMAGESDIR, self.moon.image()), 60, 60))

    def get_date(self):
        return self.adate

    def get_position(self):
        return self.moon.position()

    def get_phase(self):
        return self.moon.phase_int()
