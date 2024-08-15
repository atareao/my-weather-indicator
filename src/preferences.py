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
import os
import shutil
import logging
import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError as gi_exception:
    print(gi_exception)
    print('Repository version required not present')
    sys.exit(1)
# pylint: disable=wrong-import-position
from gi.repository import Gtk  # pyright: ignore
import comun
import geocodeapi
from whereami import WhereAmI
from configurator import Configuration
from comun import _
from basedialog import BaseDialog

logger = logging.getLogger(__name__)

APPDIR = comun.APPDIR
AUTOSTART_FILE = 'my-weather-indicator-autostart.desktop'


def get_skins():
    """
    Retrieves the available skins for the weather indicator.

    Returns:
        list: A list of skin names and their corresponding file paths.
    """
    skins = []
    personal_dir = os.path.expanduser('~/.config/my-weather-indicator/skins')
    if os.path.exists(personal_dir):
        for dn, dns, _filenames in os.walk(personal_dir):
            for sdn in dns:
                skins.append([sdn, os.path.join(dn, sdn)])
    installation_dir = '/opt/extras.ubuntu.com/my-weather-indicator/share/\
my-weather-indicator/skins'
    if os.path.exists(installation_dir):
        for dn, dns, _filenames in os.walk(installation_dir):
            for sdn in dns:
                skins.append([sdn, os.path.join(dn, sdn)])
    return skins


def select_value_in_combo(combo, value):
    """
    Selects the specified value in the combo box.

    Args:
        combo: The combo box widget.
        value: The value to be selected.

    Returns:
        None
    """
    model = combo.get_model()
    for i, item in enumerate(model):
        if value == item[1]:
            combo.set_active(i)
            return
    combo.set_active(0)


def get_selected_value_in_combo(combo):
    """
    Get the selected value in a combo box.

    Parameters:
    combo (Gtk.ComboBox): The combo box to retrieve the selected value from.

    Returns:
    The selected value from the combo box.

    """
    model = combo.get_model()
    return model.get_value(combo.get_active_iter(), 1)


class CM(BaseDialog):  # needs GTK, Python, Webkit-GTK
    """
    Class representing the Preferences dialog.

    Attributes:
        checkbutton11 (Gtk.CheckButton): Check button for showing the main
            location.
        checkbutton10 (Gtk.CheckButton): Check button for enabling auto
            location.
        entry11 (Gtk.Entry): Entry field for the locality.
        button10 (Gtk.Button): Button for searching the location.
        checkbutton12 (Gtk.CheckButton): Check button for showing the
            temperature.
        checkbutton13 (Gtk.CheckButton): Check button for showing
            notifications.
        checkbutton14 (Gtk.CheckButton): Check button for showing the widget.
        checkbutton15 (Gtk.CheckButton): Check button for hiding the indicator
            when showing the widget.
        checkbutton16 (Gtk.CheckButton): Check button for setting the widget
            on top.
        checkbutton17 (Gtk.CheckButton): Check button for showing the widget
            in the taskbar.
        checkbutton18 (Gtk.CheckButton): Check button for showing the widget
            on all desktops.
        comboboxskin1 (Gtk.ComboBox): ComboBox for selecting the skin.
        checkbutton21 (Gtk.CheckButton): Check button for showing the second
            location.
        entry21 (Gtk.Entry): Entry field for the second locality.
        button20 (Gtk.Button): Button for searching the second location.
        checkbutton22 (Gtk.CheckButton): Check button for showing the
            temperature of the second location.
        checkbutton23 (Gtk.CheckButton): Check button for showing
            notifications for the second location.
        checkbutton24 (Gtk.CheckButton): Check button for showing the widget
            for the second location.
        checkbutton25 (Gtk.CheckButton): Check button for hiding the indicator
            when showing the widget for the second location.
        checkbutton26 (Gtk.CheckButton): Check button for setting the widget
            on top for the second location.
        checkbutton27 (Gtk.CheckButton): Check button for showing the widget
            in the taskbar for the second location.
        checkbutton28 (Gtk.CheckButton): Check button for showing the widget
            on all desktops for the second location.
        skinstore1 (Gtk.ListStore): ListStore for storing the skins.
        skinstore2 (Gtk.ListStore): ListStore for storing the skins for the
        second location.
    """
    def __init__(self):
        """
        Initializes the Preferences class.

        Parameters:
        - None

        Returns:
        - None
        """
        title = _("Preferences")
        BaseDialog.__init__(self, title, None, True, True)
        self._location = None
        self._latitude = None
        self._longitude = None
        self._timezone = None
        self._location2 = None
        self._latitude2 = None
        self._longitude2 = None
        self._timezone2 = None
        self.ok = False

    def init_ui(self):
        BaseDialog.init_ui(self)
        self.set_size_request(850, 410)
        self.connect('destroy', self.close_application)
        self.set_icon_from_file(comun.ICON)
        notebook = Gtk.Notebook.new()
        self.set_content(notebook)
        vbox1 = Gtk.VBox(spacing=0)
        vbox1.set_border_width(0)
        notebook.append_page(vbox1, Gtk.Label.new(_('Main Location')))
        frame11 = Gtk.Frame.new(_('General options'))
        vbox1.pack_start(frame11, True, True, 0)
        table11 = Gtk.Table(n_rows=4, n_columns=3)
        frame11.add(table11)
        self.checkbutton11 = Gtk.CheckButton.new_with_label(_('Show'))
        self.checkbutton11.connect('toggled', self.on_checkbutton11_toggled)
        table11.attach(self.checkbutton11, 0, 1, 0, 1,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton10 = Gtk.CheckButton.new_with_label(
            _('Auto Location'))
        self.checkbutton10.connect('toggled', self.on_checkbutton10_toggled)
        table11.attach(self.checkbutton10, 0, 1, 1, 2,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        label11 = Gtk.Label.new(_('Locality') + ':')
        label11.set_halign(Gtk.Align.START)
        label11.set_valign(Gtk.Align.CENTER)
        table11.attach(label11, 0, 1, 2, 3,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.entry11 = Gtk.Entry()
        self.entry11.set_editable(False)
        table11.attach(self.entry11, 1, 2, 2, 3,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.button10 = Gtk.Button.new_with_label(_('Search Location'))
        self.button10.connect('clicked', self.search_location)
        table11.attach(self.button10, 2, 3, 2, 3,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton12 = Gtk.CheckButton.new_with_label(
            _('Show temperature'))
        table11.attach(self.checkbutton12, 0, 1, 3, 4,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton13 = Gtk.CheckButton.new_with_label(
            _('Show notifications'))
        table11.attach(self.checkbutton13, 1, 2, 3, 4,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        frame12 = Gtk.Frame.new(_('Widget options'))
        vbox1.pack_start(frame12, True, True, 0)
        table12 = Gtk.Table(n_rows=3, n_columns=2)
        frame12.add(table12)
        self.checkbutton14 = Gtk.CheckButton.new_with_label(_('Show widget'))
        self.checkbutton14.connect('toggled', self.on_checkbutton14_toggled)
        table12.attach(self.checkbutton14, 0, 1, 0, 1,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton15 = Gtk.CheckButton.new_with_label(
            _('Hide indicator when show widget'))
        table12.attach(self.checkbutton15, 1, 2, 0, 1,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton16 = Gtk.CheckButton.new_with_label(
            _('Widget on top'))
        table12.attach(self.checkbutton16, 0, 1, 1, 2,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton17 = Gtk.CheckButton.new_with_label(
            _('Show in taskbar'))
        table12.attach(self.checkbutton17, 1, 2, 1, 2,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton18 = Gtk.CheckButton.new_with_label(
            _('On all desktops'))
        table12.attach(self.checkbutton18, 0, 1, 2, 3,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.skinstore1 = Gtk.ListStore(str, str)
        for skin in get_skins():
            self.skinstore1.append(skin)
        self.comboboxskin1 = Gtk.ComboBox.new()
        self.comboboxskin1.set_model(self.skinstore1)
        cell1 = Gtk.CellRendererText()
        self.comboboxskin1.pack_start(cell1, True)
        self.comboboxskin1.add_attribute(cell1, 'text', 0)
        table12.attach(self.comboboxskin1, 1, 2, 2, 3,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        vbox2 = Gtk.VBox(spacing=5)
        vbox2.set_border_width(5)
        notebook.append_page(vbox2, Gtk.Label.new(_('Second Location')))
        self.frame21 = Gtk.Frame.new(_('General options'))
        vbox2.pack_start(self.frame21, False, False, 0)
        table21 = Gtk.Table(n_rows=4, n_columns=3)
        self.frame21.add(table21)
        self.checkbutton21 = Gtk.CheckButton.new_with_label(_('Show'))
        self.checkbutton21.connect('toggled', self.on_checkbutton21_toggled)
        table21.attach(self.checkbutton21, 0, 1, 0, 1,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        label21 = Gtk.Label.new(_('Locality') + ':')
        label21.set_halign(Gtk.Align.START)
        label21.set_valign(Gtk.Align.CENTER)
        table21.attach(label21, 0, 1, 1, 2,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.entry21 = Gtk.Entry()
        self.entry21.set_editable(False)
        table21.attach(self.entry21, 1, 2, 1, 2,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.button20 = Gtk.Button.new_with_label(_('Search Location'))
        self.button20.connect('clicked', self.search_location2)
        table21.attach(self.button20, 2, 3, 1, 2,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton22 = Gtk.CheckButton.new_with_label(
            _('Show temperature'))
        table21.attach(self.checkbutton22, 0, 1, 2, 3,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton23 = Gtk.CheckButton.new_with_label(
            _('Show notifications'))
        table21.attach(self.checkbutton23, 1, 2, 2, 3,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        frame22 = Gtk.Frame.new(_('Widget options'))
        vbox2.pack_start(frame22, False, False, 0)
        table22 = Gtk.Table(n_rows=3, n_columns=2)
        frame22.add(table22)
        self.checkbutton24 = Gtk.CheckButton.new_with_label(_('Show widget'))
        self.checkbutton24.connect('toggled', self.on_checkbutton24_toggled)
        table22.attach(self.checkbutton24, 0, 1, 0, 1,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton25 = Gtk.CheckButton.new_with_label(
            _('Hide indicator when show widget'))
        table22.attach(self.checkbutton25, 1, 2, 0, 1,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton26 = Gtk.CheckButton.new_with_label(
            _('Widget on top'))
        table22.attach(self.checkbutton26, 0, 1, 1, 2,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton27 = Gtk.CheckButton.new_with_label(
            _('Show in taskbar'))
        table22.attach(self.checkbutton27, 1, 2, 1, 2,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.checkbutton28 = Gtk.CheckButton.new_with_label(
            _('On all desktops'))
        table22.attach(self.checkbutton28, 0, 1, 2, 3,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.skinstore2 = Gtk.ListStore(str, str)
        for skin in get_skins():
            self.skinstore2.append(skin)
        self.comboboxskin2 = Gtk.ComboBox.new()
        self.comboboxskin2.set_model(self.skinstore2)
        cell1 = Gtk.CellRendererText()
        self.comboboxskin2.pack_start(cell1, True)
        self.comboboxskin2.add_attribute(cell1, 'text', 0)
        table22.attach(self.comboboxskin2, 1, 2, 2, 3,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)

        vbox2 = Gtk.VBox(spacing=5)
        vbox2.set_border_width(5)
        frame2 = Gtk.Frame()
        vbox2.pack_start(frame2, True, True, 0)
        notebook.append_page(vbox2, Gtk.Label.new(_('Units')))
        table2 = Gtk.Table(n_rows=6, n_columns=2)
        frame2.add(table2)
        label3 = Gtk.Label.new(_('Temperature') + ':')
        label3.set_halign(Gtk.Align.START)
        label3.set_valign(Gtk.Align.CENTER)
        table2.attach(label3, 0, 1, 0, 1,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.liststore3 = Gtk.ListStore(str, str)
        self.liststore3.append([f"{176:c} {_('Celsius')}", 'C'])
        self.liststore3.append([f"{176:c} {_('Fahrenheit')}", 'F'])
        self.liststore3.append([_('Kelvin'), 'K'])
        self.combobox3 = Gtk.ComboBox.new()
        self.combobox3.set_model(self.liststore3)
        cell3 = Gtk.CellRendererText()
        self.combobox3.pack_start(cell3, True)
        self.combobox3.add_attribute(cell3, 'text', 0)
        table2.attach(self.combobox3, 1, 2, 0, 1,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        label32 = Gtk.Label.new(_('Pressure') + ':')
        label32.set_halign(Gtk.Align.START)
        label32.set_valign(Gtk.Align.CENTER)
        table2.attach(label32, 0, 1, 1, 2,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.liststore32 = Gtk.ListStore(str, str)
        self.liststore32.append([_('Millibar'), 'mb'])
        self.liststore32.append([_('Inches of mercury'), 'in'])
        self.liststore32.append([_('Millimeters of mercury'), 'mm'])
        self.combobox32 = Gtk.ComboBox.new()
        self.combobox32.set_model(self.liststore32)
        cell32 = Gtk.CellRendererText()
        self.combobox32.pack_start(cell32, True)
        self.combobox32.add_attribute(cell32, 'text', 0)
        table2.attach(self.combobox32, 1, 2, 1, 2,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        label33 = Gtk.Label.new(_('Visibility') + ':')
        label33.set_halign(Gtk.Align.START)
        label33.set_valign(Gtk.Align.CENTER)
        table2.attach(label33, 0, 1, 2, 3,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.liststore33 = Gtk.ListStore(str, str)
        self.liststore33.append([_('mile'), 'mi'])
        self.liststore33.append([_('kilometer'), 'km'])
        self.combobox33 = Gtk.ComboBox.new()
        self.combobox33.set_model(self.liststore33)
        cell33 = Gtk.CellRendererText()
        self.combobox33.pack_start(cell33, True)
        self.combobox33.add_attribute(cell33, 'text', 0)
        table2.attach(self.combobox33, 1, 2, 2, 3,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        label31 = Gtk.Label.new(_('Wind velocity') + ':')
        label31.set_halign(Gtk.Align.START)
        label31.set_valign(Gtk.Align.CENTER)
        table2.attach(label31, 0, 1, 3, 4,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.liststore31 = Gtk.ListStore(str, str)
        self.liststore31.append([_('Beaufort'), 'Beaufort'])
        self.liststore31.append([_('ft/s'), 'ft/s'])
        self.liststore31.append([_('km/h'), 'km/h'])
        self.liststore31.append([_('knots'), 'knots'])
        self.liststore31.append([_('m/s'), 'm/s'])
        self.liststore31.append([_('mph'), 'mph'])
        self.combobox31 = Gtk.ComboBox.new()
        self.combobox31.set_model(self.liststore31)
        cell31 = Gtk.CellRendererText()
        self.combobox31.pack_start(cell31, True)
        self.combobox31.add_attribute(cell31, 'text', 0)
        table2.attach(self.combobox31, 1, 2, 3, 4,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        label34 = Gtk.Label.new(_('Rain Gauge') + ':')
        label34.set_halign(Gtk.Align.START)
        label34.set_valign(Gtk.Align.CENTER)
        table2.attach(label34, 0, 1, 4, 5,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.liststore34 = Gtk.ListStore(str, str)
        self.liststore34.append([_('Inches'), 'in'])
        self.liststore34.append([_('Centimeters'), 'cm'])
        self.liststore34.append([_('Millimeters'), 'mm'])
        self.combobox34 = Gtk.ComboBox.new()
        self.combobox34.set_model(self.liststore34)
        cell34 = Gtk.CellRendererText()
        self.combobox34.pack_start(cell34, True)
        self.combobox34.add_attribute(cell34, 'text', 0)
        table2.attach(self.combobox34, 1, 2, 4, 5,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        label35 = Gtk.Label.new(_('Snow Gauge') + ':')
        label35.set_halign(Gtk.Align.START)
        label35.set_valign(Gtk.Align.CENTER)
        table2.attach(label35, 0, 1, 5, 6,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.liststore35 = Gtk.ListStore(str, str)
        self.liststore35.append([_('Inches'), 'in'])
        self.liststore35.append([_('Centimeters'), 'cm'])
        self.liststore35.append([_('Millimeters'), 'mm'])
        self.combobox35 = Gtk.ComboBox.new()
        self.combobox35.set_model(self.liststore35)
        cell35 = Gtk.CellRendererText()
        self.combobox35.pack_start(cell35, True)
        self.combobox35.add_attribute(cell35, 'text', 0)
        table2.attach(self.combobox35, 1, 2, 5, 6,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        label36 = Gtk.Label.new(_('Time Format') + ':')
        label36.set_halign(Gtk.Align.START)
        label36.set_valign(Gtk.Align.CENTER)
        table2.attach(label36, 0, 1, 6, 7,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.liststore36 = Gtk.ListStore(str, bool)
        self.liststore36.append([_('24 h'), True])
        self.liststore36.append([_('AM/PM'), False])
        self.combobox36 = Gtk.ComboBox.new()
        self.combobox36.set_model(self.liststore36)
        cell36 = Gtk.CellRendererText()
        self.combobox36.pack_start(cell36, True)
        self.combobox36.add_attribute(cell36, 'text', 0)
        table2.attach(self.combobox36, 1, 2, 6, 7,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        vbox3 = Gtk.VBox(spacing=5)
        vbox3.set_border_width(5)
        frame3 = Gtk.Frame()
        vbox3.pack_start(frame3, True, True, 0)
        notebook.append_page(vbox3, Gtk.Label.new(_('General options')))
        table3 = Gtk.Table(n_rows=4, n_columns=2)
        frame3.add(table3)
        self.checkbutton1 = Gtk.CheckButton.new_with_label(_('Autostart'))
        table3.attach(self.checkbutton1, 0, 2, 0, 1,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        label41 = Gtk.Label.new(_('Refresh frequency') + ':')
        label41.set_halign(Gtk.Align.START)
        label41.set_valign(Gtk.Align.CENTER)
        table3.attach(label41, 0, 1, 1, 2,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.liststore45 = Gtk.ListStore(str, float)
        self.liststore45.append(['15 ' + _('minutes'), 0.25])
        self.liststore45.append(['30 ' + _('minutes'), 0.5])
        self.liststore45.append(['1 ' + _('hour'), 1.0])
        self.liststore45.append(['2 ' + _('hours'), 2.0])
        self.liststore45.append(['4 ' + _('hours'), 4.0])
        self.liststore45.append(['8 ' + _('hours'), 8.0])
        self.liststore45.append(['12 ' + _('hours'), 12.0])
        self.liststore45.append(['24 ' + _('hours'), 24.0])
        self.combobox45 = Gtk.ComboBox.new()
        self.combobox45.set_model(self.liststore45)
        cell45 = Gtk.CellRendererText()
        self.combobox45.pack_start(cell45, True)
        self.combobox45.add_attribute(cell45, 'text', 0)
        table3.attach(self.combobox45, 1, 2, 1, 2,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        label31 = Gtk.Label.new(_('Select icon theme') + ':')
        label31.set_halign(Gtk.Align.START)
        label31.set_valign(Gtk.Align.CENTER)
        table3.attach(label31, 0, 2, 2, 3,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.radiobutton31 = Gtk.RadioButton(group=None)
        image1 = Gtk.Image()
        image1.set_from_file(
            os.path.join(comun.ICONDIR, 'mwil-mostly-sunny.png'))
        self.radiobutton31.add(image1)
        table3.attach(self.radiobutton31, 0, 1, 3, 4,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.radiobutton32 = Gtk.RadioButton(group=self.radiobutton31)
        image2 = Gtk.Image()
        image2.set_from_file(
            os.path.join(comun.ICONDIR, 'mwid-mostly-sunny.png'))
        self.radiobutton32.add(image2)
        table3.attach(self.radiobutton32, 1, 2, 3, 4,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.checkbutton11.set_active(True)
        self.checkbutton21.set_active(True)
        if os.path.exists(
                os.path.expanduser(f"~/.config/autostart/{AUTOSTART_FILE}")):
            self.checkbutton1.set_active(True)
        #
        self.show_all()
        #
        self.load_preferences()

    def set_sensitive_frame1(self, sensitive):
        self.checkbutton10.set_sensitive(sensitive)
        self.entry11.set_sensitive(sensitive)
        self.button10.set_sensitive(sensitive)
        self.checkbutton12.set_sensitive(sensitive)
        self.checkbutton13.set_sensitive(sensitive)
        self.checkbutton14.set_sensitive(sensitive)
        self.checkbutton15.set_sensitive(sensitive)
        if sensitive is False:
            self.checkbutton12.set_active(False)
            self.checkbutton13.set_active(False)
            self.checkbutton14.set_active(False)
            self.checkbutton15.set_active(False)
            self.comboboxskin1.set_active(False)

    def set_sensitive_frame2(self, sensitive):
        self.entry21.set_sensitive(sensitive)
        self.button20.set_sensitive(sensitive)
        self.checkbutton22.set_sensitive(sensitive)
        self.checkbutton23.set_sensitive(sensitive)
        self.checkbutton24.set_sensitive(sensitive)
        self.checkbutton25.set_sensitive(sensitive)
        if sensitive is False:
            self.checkbutton24.set_active(False)
            self.checkbutton25.set_active(False)
            self.comboboxskin2.set_active(False)

    def on_checkbutton10_toggled(self, _widget):
        """
        Toggles the sensitivity of various UI elements based on the state of
        checkbutton10.

        Parameters:
        - self: The instance of the class.

        Returns:
        None
        """
        self.entry11.set_sensitive(not self.checkbutton10.get_active())
        self.button10.set_sensitive(not self.checkbutton10.get_active())
        self.checkbutton12.set_sensitive(not self.checkbutton10.get_active())
        self.checkbutton13.set_sensitive(not self.checkbutton10.get_active())

    def on_checkbutton11_toggled(self, _widget):
        """
        Callback function for the toggled event of checkbutton11.

        Parameters:
        - _widget: The widget that triggered the event.

        Description:
        - This function is called when checkbutton11 is toggled.
        - It sets the sensitivity of frame1 based on the state of
                checkbutton11.
        - If checkbutton11 is not active, it disables checkbutton21.
        - If checkbutton11 is active and checkbutton21 is not active, it
                disables checkbutton11.
        - If checkbutton21 is not sensitive, it enables checkbutton21.
        """
        self.set_sensitive_frame1(self.checkbutton11.get_active())
        if self.checkbutton11.get_active() is False:
            self.checkbutton21.set_sensitive(False)
        elif (self.checkbutton11.get_active() is True and
              self.checkbutton21.get_active() is False):
            self.checkbutton11.set_sensitive(False)
        elif self.checkbutton21.get_sensitive() is False:
            self.checkbutton21.set_sensitive(True)

    def on_checkbutton14_toggled(self, _widget):
        """
        Toggles the sensitivity of various check buttons and a combo box based
        on the state of checkbutton14.

        Parameters:
        - _widget: The widget that triggered the toggled event.

        Returns:
        None
        """
        self.checkbutton15.set_sensitive(self.checkbutton14.get_active())
        self.checkbutton16.set_sensitive(self.checkbutton14.get_active())
        self.checkbutton17.set_sensitive(self.checkbutton14.get_active())
        self.checkbutton18.set_sensitive(self.checkbutton14.get_active())
        self.comboboxskin1.set_sensitive(self.checkbutton14.get_active())

    def on_checkbutton21_toggled(self, _widget):
        """
        Toggles the sensitivity of checkbutton21 and checkbutton11 based on
        the state of checkbutton21.

        Parameters:
        - self: The instance of the class.

        Returns:
        None
        """
        self.set_sensitive_frame2(self.checkbutton21.get_active())
        (self.checkbutton21.get_active())
        if self.checkbutton21.get_active() is False:
            self.checkbutton11.set_sensitive(False)
        elif (self.checkbutton21.get_active() is True and
              self.checkbutton11.get_active() is False):
            self.checkbutton21.set_sensitive(False)
        elif self.checkbutton11.get_sensitive() is False:
            self.checkbutton11.set_sensitive(True)

    def on_checkbutton24_toggled(self, _widget):
        """
        Toggles the sensitivity of several check buttons and a combo box based
        on the state of checkbutton24.

        Parameters:
        - _widget: The widget that triggered the toggled event.

        Returns:
        None
        """
        self.checkbutton25.set_sensitive(self.checkbutton24.get_active())
        self.checkbutton26.set_sensitive(self.checkbutton24.get_active())
        self.checkbutton27.set_sensitive(self.checkbutton24.get_active())
        self.checkbutton28.set_sensitive(self.checkbutton24.get_active())
        self.comboboxskin2.set_sensitive(self.checkbutton24.get_active())

    def close_application(self, _widget):
        """
        Closes the application.

        Parameters:
        - _widget: The widget that triggered the close event.

        Returns:
        None
        """
        self.ok = False
        self.destroy()

    def search_location(self, _widget):
        """
        Search for a location using the WhereAmI class.

        Parameters:
        - _widget: The widget triggering the search.

        Returns:
        None
        """
        cm1 = WhereAmI(self, location=self.entry11.get_text(),
                       latitude=self._latitude, longitude=self._longitude,
                       timezone=self._timezone)
        if cm1.run() == Gtk.ResponseType.ACCEPT:
            self._latitude, self._longitude, self._location, self._timezone = \
                    cm1.get_data()
            self.entry11.set_text(self._location)
        cm1.destroy()

    def search_location2(self, _widget):
        """
        Search for a location using the WhereAmI class.

        Parameters:
        - _widget: The widget triggering the search.

        Returns:
        None
        """
        cm2 = WhereAmI(self, location=self.entry21.get_text(),
                       latitude=self._latitude2, longitude=self._longitude2,
                       timezone=self._timezone2)
        if cm2.run() == Gtk.ResponseType.ACCEPT:
            self._latitude2, self._longitude2, self._location2, \
                    self._timezone2 = cm2.get_data()
            self.entry21.set_text(self._location2)
        cm2.destroy()

    def load_preferences(self):
        """
        Load the preferences from the configuration file and update the UI
        accordingly.

        This method retrieves the preferences from the configuration file and
        sets the corresponding UI elements
        to reflect the saved preferences. It updates the state of various
        check buttons, entry fields, combo boxes,
        and radio buttons based on the values stored in the configuration.

        Parameters:
            None

        Returns:
            None
        """
        configuration = Configuration()
        # first_time = configuration.get('first-time')
        # version = configuration.get('version')
        self.checkbutton11.set_active(configuration.get('main-location'))
        self.checkbutton10.set_active(configuration.get('autolocation'))
        self._location = configuration.get('location')
        self._latitude = configuration.get('latitude')
        self._longitude = configuration.get('longitude')
        self._timezone = configuration.get("timezone")
        if self._location:
            self.entry11.set_text(self._location)
        self.checkbutton12.set_active(configuration.get('show-temperature'))
        self.checkbutton13.set_active(configuration.get('show-notifications'))
        self.checkbutton14.set_active(configuration.get('widget1'))
        self.checkbutton15.set_active(configuration.get('onwidget1hide'))
        self.checkbutton15.set_sensitive(self.checkbutton14.get_active())
        self.checkbutton16.set_active(configuration.get('onwidget1top'))
        self.checkbutton16.set_sensitive(self.checkbutton14.get_active())
        self.checkbutton17.set_active(configuration.get('showintaskbar1'))
        self.checkbutton17.set_sensitive(self.checkbutton14.get_active())
        self.checkbutton18.set_active(configuration.get('onalldesktop1'))
        self.checkbutton18.set_sensitive(self.checkbutton14.get_active())
        select_value_in_combo(self.comboboxskin1, configuration.get('skin1'))
        self.comboboxskin1.set_sensitive(self.checkbutton14.get_active())
        #
        self.checkbutton21.set_active(configuration.get('second-location'))
        self._location2 = configuration.get('location2')
        self._latitude2 = configuration.get('latitude2')
        self._longitude2 = configuration.get('longitude2')
        self._timezone2 = configuration.get("timezone2")
        if self._location2:
            self.entry21.set_text(self._location2)
        self.checkbutton22.set_active(configuration.get('show-temperature2'))
        self.checkbutton23.set_active(configuration.get('show-notifications2'))
        self.checkbutton24.set_active(configuration.get('widget2'))
        self.checkbutton25.set_active(configuration.get('onwidget2hide'))
        self.checkbutton25.set_sensitive(self.checkbutton24.get_active())
        self.checkbutton26.set_active(configuration.get('onwidget2top'))
        self.checkbutton26.set_sensitive(self.checkbutton24.get_active())
        self.checkbutton27.set_active(configuration.get('showintaskbar2'))
        self.checkbutton27.set_sensitive(self.checkbutton24.get_active())
        self.checkbutton28.set_active(configuration.get('onalldesktop2'))
        self.checkbutton28.set_sensitive(self.checkbutton24.get_active())
        select_value_in_combo(self.comboboxskin2, configuration.get('skin2'))
        self.comboboxskin2.set_sensitive(self.checkbutton24.get_active())
        #
        select_value_in_combo(self.combobox3, configuration.get('temperature'))
        select_value_in_combo(self.combobox32, configuration.get('pressure'))
        select_value_in_combo(self.combobox33, configuration.get('visibility'))
        select_value_in_combo(self.combobox31, configuration.get('wind'))
        select_value_in_combo(self.combobox34, configuration.get('rain'))
        select_value_in_combo(self.combobox35, configuration.get('snow'))
        select_value_in_combo(self.combobox36, configuration.get('24h'))
        select_value_in_combo(self.combobox45, configuration.get('refresh'))
        #
        self.radiobutton31.set_active(configuration.get('icon-light'))
        self.radiobutton32.set_active(not configuration.get('icon-light'))

    def save_preferences(self):
        """
        Save the preferences of the weather indicator.

        This method saves the preferences of the weather indicator by updating
        the configuration file.
        It checks the status of various check buttons and entry fields to
        determine which preferences to save.
        If the 'autolocation' check button is active, it retrieves the
        latitude, longitude, city, and timezone using the geocodeapi.
        If the 'main-location' check button is active, it saves the location
        entered in the entry field as the main location.
        It also saves other preferences such as show-temperature,
        show-notifications, widget settings, skin selection, etc.
        Finally, it saves the preferences to the configuration file and
        optionally sets up autostart.

        Returns:
            None
        """
        # code implementation
        configuration = Configuration()
        if self.checkbutton11.get_active() and\
                (not self.entry11.get_text() or self._latitude is None or
                 self._latitude == 0 or self._longitude is None or
                 self._longitude == 0 or not self._timezone):
            data = geocodeapi.get_latitude_longitude_city()
            if data:
                self._location = data["city"]
                self._latitude = data["lat"]
                self._longitude = data["lon"]
                self._timezone = data["timezone"]
        if self.checkbutton21.get_active() and\
                (not self.entry21.get_text() or self._latitude2 is None or
                 self._latitude2 == 0 or self._longitude2 is None or
                 self._longitude2 == 0 or not self._timezone2):
            data = geocodeapi.get_latitude_longitude_city()
            if data:
                self._location2 = data["city"]
                self._latitude2 = data["lat"]
                self._longitude2 = data["lon"]
                self._timezone2 = data["timezone"]
        if self.entry11.get_text():
            self._location = self.entry11.get_text()
        if self.entry21.get_text():
            self._location2 = self.entry21.get_text()
        configuration.set('first-time', False)
        configuration.set('version', comun.VERSION)
        configuration.set('main-location', self.checkbutton11.get_active())
        configuration.set('autolocation', self.checkbutton10.get_active())
        configuration.set('location', self._location)
        configuration.set('latitude', self._latitude)
        configuration.set('longitude', self._longitude)
        configuration.set('timezone', self._timezone)
        configuration.set('show-temperature', self.checkbutton12.get_active())
        configuration.set('show-notifications',
                          self.checkbutton13.get_active())
        configuration.set('widget1', self.checkbutton14.get_active())
        if self.checkbutton14.get_active() is True:
            configuration.set('onwidget1hide', self.checkbutton15.get_active())
            configuration.set('onwidget1top', self.checkbutton16.get_active())
            configuration.set('showintaskbar1',
                              self.checkbutton17.get_active())
            configuration.set('onalldesktop1', self.checkbutton18.get_active())
            configuration.set('skin1',
                              get_selected_value_in_combo(self.comboboxskin1))
        #
        configuration.set('second-location', self.checkbutton21.get_active())
        configuration.set('location2', self._location2)
        configuration.set('latitude2', self._latitude2)
        configuration.set('longitude2', self._longitude2)
        configuration.set('timezone2', self._timezone)
        configuration.set('show-temperature2', self.checkbutton22.get_active())
        configuration.set('show-notifications2',
                          self.checkbutton23.get_active())
        configuration.set('widget2', self.checkbutton24.get_active())
        if self.checkbutton24.get_active() is True:
            configuration.set('onwidget2hide', self.checkbutton25.get_active())
            configuration.set('onwidget2top', self.checkbutton26.get_active())
            configuration.set('showintaskbar2',
                              self.checkbutton27.get_active())
            configuration.set('onalldesktop2', self.checkbutton28.get_active())
            configuration.set('skin2',
                              get_selected_value_in_combo(self.comboboxskin2))
        #
        configuration.set(
            'temperature', get_selected_value_in_combo(self.combobox3))
        configuration.set(
            'pressure', get_selected_value_in_combo(self.combobox32))
        configuration.set(
            'visibility', get_selected_value_in_combo(self.combobox33))
        configuration.set(
            'wind', get_selected_value_in_combo(self.combobox31))
        configuration.set(
            'rain', get_selected_value_in_combo(self.combobox34))
        configuration.set(
            'snow', get_selected_value_in_combo(self.combobox35))
        configuration.set(
            '24h', get_selected_value_in_combo(self.combobox36))
        configuration.set(
            'refresh', get_selected_value_in_combo(self.combobox45))
        configuration.set('icon-light', self.radiobutton31.get_active())
        print('Saving...')
        configuration.save()
        #
        filestart = os.path.expanduser(f"~/.config/autostart/{AUTOSTART_FILE}")
        if self.checkbutton1.get_active():
            if not os.path.exists(os.path.dirname(filestart)):
                os.makedirs(os.path.dirname(filestart))
            shutil.copyfile(comun.AUTOSTART, filestart)
        else:
            if os.path.exists(filestart):
                os.remove(filestart)


if __name__ == "__main__":
    cm = CM()
    if cm.run() == Gtk.ResponseType.ACCEPT:
        cm.save_preferences()
    cm.hide()
    cm.destroy()
    sys.exit(0)
