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

import sys
import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
except ValueError as e:
    print(e)
    sys.exit(1)
# pylint: disable=wrong-import-position
from gi.repository import Gdk
from gi.repository import Gtk
import comun


class BaseDialog(Gtk.Dialog):
    """
    A base dialog class for creating custom dialogs in GTK.

    Args:
        title (str): The title of the dialog.
        window (Gtk.Window, optional): The parent window for the dialog.
        Defaults to None.
        ok_button (bool, optional): Whether to include an OK button in the
        dialog. Defaults to True.
        cancel_button (bool, optional): Whether to include a Cancel button in
        the dialog. Defaults to True.

    Attributes:
        headerbar (Gtk.HeaderBar): The header bar widget of the dialog.

    Methods:
        set_content(widget): Sets the content of the dialog.
        init_ui(): Initializes the user interface of the dialog.
        on_realize(*_): Callback function called when the dialog is realized.
    """
    def __init__(self, title, window=None, ok_button=True, cancel_button=True):
        Gtk.Dialog.__init__(self, title, window)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        if ok_button:
            self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        if cancel_button:
            self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.set_default_response(Gtk.ResponseType.ACCEPT)
        self.set_resizable(False)
        self.set_icon_from_file(comun.ICON)
        self.connect('realize', self.on_realize)
        self.init_ui()
        self.show_all()

    def set_content(self, widget):
        """
        Set the content of the dialog.

        Parameters:
        - widget: The widget to be added as the content of the dialog.

        Returns:
        None
        """
        self.get_content_area().add(widget)

    def init_ui(self):
        """
        Initializes the user interface of the dialog.

        This method creates and configures the header bar of the dialog.
        It sets the title, subtitle, and close button visibility.

        Parameters:
        - self: The instance of the dialog.

        Returns:
        - None
        """
        self.headerbar = Gtk.HeaderBar.new()
        self.headerbar.set_title(self.get_title())
        self.headerbar.set_subtitle('-')
        self.headerbar.set_show_close_button(True)
        self.set_titlebar(self.headerbar)

    def on_realize(self, *_):
        """
        This method is called when the widget is realized, meaning it has been
        mapped to the screen and is visible to the user.
        It calculates the position of the widget based on the monitor's
        dimensions and centers it on the screen.
        """
        monitor = Gdk.Display.get_primary_monitor(Gdk.Display.get_default())
        scale = monitor.get_scale_factor()
        monitor_width = monitor.get_geometry().width / scale
        monitor_height = monitor.get_geometry().height / scale
        width = self.get_preferred_width()[0]
        height = self.get_preferred_height()[0]
        self.move((monitor_width - width)/2, (monitor_height - height)/2)


if __name__ == '__main__':
    dialog = BaseDialog('Test')
    dialog.run()
