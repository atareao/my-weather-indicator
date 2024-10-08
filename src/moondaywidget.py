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

import os
import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
except ValueError as e:
    print(e)
    exit(1)
# pylint: disable=wrong-import-position
from gi.repository import Gtk  # pyright: ignore
from gi.repository import GdkPixbuf  # pyright: ignore
import comun
from moon import Moon


class MoonDayWidget(Gtk.EventBox):
    """
    A custom widget that displays the moon phase and date.

    Args:
        adate (datetime.date, optional): The date to be displayed. Defaults to
        None.

    Methods:
        set_style(box_name):
            Sets the style of the widget's box.

        set_date(adate):
            Sets the date to be displayed and updates the widget.

        get_date():
            Returns the currently set date.

        get_position():
            Returns the position of the moon.

        get_phase():
            Returns the phase of the moon as an integer.
    """

    def __init__(self, adate=None):
        """
        Initializes the MoonDayWidget.

        Args:
            adate (datetime.date, optional): The date to set for the widget.
            Defaults to None.
        """
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
        """
        Sets the style of the widget's box.

        Parameters:
        - box_name (str): The name of the box to set the style for.

        Returns:
        - None
        """
        self.box1.set_name(box_name)

    def set_date(self, adate):
        """
        Sets the date for the moondaywidget.

        Parameters:
        - adate: The date to be set.

        Returns:
        None
        """
        self.adate = adate
        self.label.set_text(str(adate.day))
        self.moon = Moon(adate)
        self.image.set_from_pixbuf(
            GdkPixbuf.Pixbuf.new_from_file_at_size(
                os.path.join(
                    comun.IMAGESDIR, self.moon.image()), 60, 60))

    def get_date(self):
        """
        Returns the date of the moonday widget.

        :return: The date of the moonday widget.
        :rtype: datetime.date
        """
        return self.adate

    def get_position(self):
        """
        Returns the position of the moon.

        Returns:
            tuple: A tuple containing the x and y coordinates of the moon's
            position.
        """
        return self.moon.position()

    def get_phase(self):
        """
        Returns the phase of the moon as an integer.

        :return: The phase of the moon as an integer.
        :rtype: int
        """
        return self.moon.phase_int()
