#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#
# Copyright (C) 2011 Lorenzo Carbonell
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
#
import os
import sys
import shutil
from gi.repository import Gtk
import locale
import gettext
import comun
import geocodeapi
import ipaddress
import webbrowser
from whereami import WhereAmI
from wundergroundapi import UndergroundWeatherService
from worldweatheronlineapi import WorldWeatherOnlineService
from configurator import Configuration
from comun import _

APPDIR = comun.APPDIR


def get_skins():
    skins = []
    personal_dir = os.path.expanduser('~/.config/my-weather-indicator/skins')
    if os.path.exists(personal_dir):
        for dirname, dirnames, filenames in os.walk(personal_dir):
            for subdirname in dirnames:
                skins.append([subdirname, os.path.join(dirname, subdirname)])
    installation_dir = '/opt/extras.ubuntu.com/my-weather-indicator/share/\
my-weather-indicator/skins'
    if os.path.exists(installation_dir):
        for dirname, dirnames, filenames in os.walk(installation_dir):
            for subdirname in dirnames:
                skins.append([subdirname, os.path.join(dirname, subdirname)])
    return skins


def select_value_in_combo(combo, value):
    model = combo.get_model()
    for i, item in enumerate(model):
        if value == item[1]:
            combo.set_active(i)
            return
    combo.set_active(0)


def get_selected_value_in_combo(combo):
    model = combo.get_model()
    return model.get_value(combo.get_active_iter(), 1)


class CM(Gtk.Dialog):  # needs GTK, Python, Webkit-GTK
    def __init__(self):
        # ***************************************************************
        Gtk.Dialog.__init__(self,
                            'my-weather-indicator | '+_('Preferences'),
                            None,
                            Gtk.DialogFlags.MODAL |
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                             Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_size_request(850, 410)
        self.connect('destroy', self.close_application)
        self.set_icon_from_file(comun.ICON)
        vbox = Gtk.VBox(spacing=5)
        vbox.set_border_width(5)
        self.get_content_area().add(vbox)
        notebook = Gtk.Notebook.new()
        vbox.add(notebook)
        vbox1 = Gtk.VBox(spacing=5)
        vbox1.set_border_width(5)
        notebook.append_page(vbox1, Gtk.Label.new(_('Main Location')))
        frame11 = Gtk.Frame.new(_('General options'))
        vbox1.pack_start(frame11, True, True, 0)
        table11 = Gtk.Table(rows=4, columns=3)
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
        label11 = Gtk.Label.new(_('Locality')+':')
        label11.set_alignment(0, 0.5)
        table11.attach(label11, 0, 1, 2, 3,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.entry11 = Gtk.Entry()
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
        table12 = Gtk.Table(rows=3, columns=2)
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
        table21 = Gtk.Table(rows=4, columns=3)
        self.frame21.add(table21)
        self.checkbutton21 = Gtk.CheckButton.new_with_label(_('Show'))
        self.checkbutton21.connect('toggled', self.on_checkbutton21_toggled)
        table21.attach(self.checkbutton21, 0, 1, 0, 1,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        label21 = Gtk.Label.new(_('Locality')+':')
        label21.set_alignment(0, 0.5)
        table21.attach(label21, 0, 1, 1, 2,
                       xoptions=Gtk.AttachOptions.FILL,
                       yoptions=Gtk.AttachOptions.FILL,
                       xpadding=5, ypadding=5)
        self.entry21 = Gtk.Entry()
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
        table22 = Gtk.Table(rows=3, columns=2)
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
        vbox25 = Gtk.VBox(spacing=5)
        vbox25.set_border_width(5)
        notebook.append_page(vbox25, Gtk.Label.new(_('Weather Services')))
        table25 = Gtk.Table(2, 2, True)
        vbox25.pack_start(table25, True, True, 0)
        owmframe = Gtk.Frame()
        self.radiobutton253 = Gtk.RadioButton(group=None)
        image_wowm = Gtk.Image()
        image_wowm.set_from_file(comun.OPENWEATHERMAPLOGO)
        self.radiobutton253.add(image_wowm)
        owmframe.add(self.radiobutton253)
        table25.attach(owmframe, 0, 1, 0, 1, xpadding=5, ypadding=5)
        yahooframe = Gtk.Frame()
        self.radiobutton251 = Gtk.RadioButton(group=self.radiobutton253)
        image_wyahoo = Gtk.Image()
        image_wyahoo.set_from_file(comun.YAHOOLOGO)
        self.radiobutton251.add(image_wyahoo)
        yahooframe.add(self.radiobutton251)
        table25.attach(yahooframe, 0, 1, 1, 2, xpadding=5, ypadding=5)
        wwoframe = Gtk.Frame()
        table25.attach(wwoframe, 1, 2, 1, 2, xpadding=5, ypadding=5)
        wwobox = Gtk.Table(1, 3)
        wwoframe.add(wwobox)
        self.radiobutton252 = Gtk.RadioButton(group=self.radiobutton253)
        self.radiobutton252.set_sensitive(False)
        image_wworldonline = Gtk.Image()
        image_wworldonline.set_from_file(comun.WOLRDWEATHERONLINE)
        self.radiobutton252.add(image_wworldonline)
        wwobox.attach(self.radiobutton252, 0, 1, 0, 1,
                      xpadding=5, ypadding=5)
        self.wwokey = Gtk.Entry()
        self.wwokey.set_tooltip_text(_('Input World Weather Online key'))
        wwobox.attach(self.wwokey, 1, 2, 0, 1, xpadding=5, ypadding=5)
        buttonwwokey = Gtk.Button(_('Activate'))
        buttonwwokey.set_tooltip_text(
            _('Click to activate World Weather Online'))
        buttonwwokey.connect('clicked', self.on_buttonwwokey_clicked)
        wwobox.attach(buttonwwokey, 2, 3, 0, 1,
                      xoptions=Gtk.AttachOptions.SHRINK,
                      yoptions=Gtk.AttachOptions.SHRINK,
                      xpadding=5, ypadding=5)
        wuframe = Gtk.Frame()
        table25.attach(wuframe, 1, 2, 0, 1, xpadding=5, ypadding=5)
        wubox = Gtk.Table(1, 3)
        wuframe.add(wubox)
        self.radiobutton254 = Gtk.RadioButton(group=self.radiobutton253)
        self.radiobutton254.set_sensitive(False)
        image_wunderground = Gtk.Image()
        image_wunderground.set_from_file(comun.UNDERGROUNDLOGO)
        image_wunderground.connect(
            'button-release-event', self.on_image_wunderground_clicked)
        self.radiobutton254.add(image_wunderground)
        wubox.attach(self.radiobutton254, 0, 1, 0, 1, xpadding=5, ypadding=5)
        self.wukey = Gtk.Entry()
        self.wukey.set_tooltip_text(_('Input Weather Underground key'))
        wubox.attach(self.wukey, 1, 2, 0, 1, xpadding=5, ypadding=5)
        buttonwukey = Gtk.Button(_('Activate'))
        buttonwukey.set_tooltip_text(
            _('Click to activate Weather Underground'))
        buttonwukey.connect('clicked', self.on_buttonwukey_clicked)
        wubox.attach(buttonwukey, 2, 3, 0, 1,
                     xoptions=Gtk.AttachOptions.SHRINK,
                     yoptions=Gtk.AttachOptions.SHRINK,
                     xpadding=5, ypadding=5)
        vbox2 = Gtk.VBox(spacing=5)
        vbox2.set_border_width(5)
        frame2 = Gtk.Frame()
        vbox2.pack_start(frame2, True, True, 0)
        notebook.append_page(vbox2, Gtk.Label.new(_('Units')))
        table2 = Gtk.Table(rows=6, columns=2)
        frame2.add(table2)
        label3 = Gtk.Label.new(_('Temperature')+':')
        label3.set_alignment(0, 0.5)
        table2.attach(label3, 0, 1, 0, 1,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.liststore3 = Gtk.ListStore(str, str)
        self.liststore3.append(['{0:c} '.format(176)+_('Celsius'), 'C'])
        self.liststore3.append(['{0:c} '.format(176)+_('Fahrenheit'), 'F'])
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
        label32 = Gtk.Label.new(_('Pressure')+':')
        label32.set_alignment(0, 0.5)
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
        label33 = Gtk.Label.new(_('Visibility')+':')
        label33.set_alignment(0, 0.5)
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
        label31 = Gtk.Label.new(_('Wind velocity')+':')
        label31.set_alignment(0, 0.5)
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
        label34 = Gtk.Label.new(_('Rain Gauge')+':')
        label34.set_alignment(0, 0.5)
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
        label35 = Gtk.Label.new(_('Snow Gauge')+':')
        label35.set_alignment(0, 0.5)
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
        label36 = Gtk.Label.new(_('Time Format')+':')
        label36.set_alignment(0, 0.5)
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
        table3 = Gtk.Table(rows=4, columns=2)
        frame3.add(table3)
        self.checkbutton1 = Gtk.CheckButton(_('Autostart'))
        table3.attach(self.checkbutton1, 0, 2, 0, 1,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        label41 = Gtk.Label.new(_('Refresh frequency')+':')
        label41.set_alignment(0, 0.5)
        table3.attach(label41, 0, 1, 1, 2,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        self.liststore45 = Gtk.ListStore(str, float)
        self.liststore45.append(['15 '+_('minutes'), 0.25])
        self.liststore45.append(['30 '+_('minutes'), 0.5])
        self.liststore45.append(['1 '+_('hour'), 1.0])
        self.liststore45.append(['2 '+_('hours'), 2.0])
        self.liststore45.append(['4 '+_('hours'), 4.0])
        self.liststore45.append(['8 '+_('hours'), 8.0])
        self.liststore45.append(['12 '+_('hours'), 12.0])
        self.liststore45.append(['24 '+_('hours'), 24.0])
        self.combobox45 = Gtk.ComboBox.new()
        self.combobox45.set_model(self.liststore45)
        cell45 = Gtk.CellRendererText()
        self.combobox45.pack_start(cell45, True)
        self.combobox45.add_attribute(cell45, 'text', 0)
        table3.attach(self.combobox45, 1, 2, 1, 2,
                      xoptions=Gtk.AttachOptions.FILL,
                      yoptions=Gtk.AttachOptions.FILL,
                      xpadding=5, ypadding=5)
        label31 = Gtk.Label.new(_('Select icon theme')+':')
        label31.set_alignment(0, 0.5)
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
        autostart_file = 'my-weather-indicator-autostart.desktop'
        if os.path.exists(os.path.join(
                os.getenv('HOME'), '.config/autostart', autostart_file)):
            self.checkbutton1.set_active(True)
        #
        self.show_all()
        #
        self.load_preferences()

    def on_buttonwukey_clicked(self, widget):
        if len(self.wukey.get_text()) > 0:
            uws = UndergroundWeatherService(key=self.wukey.get_text())
            if uws.test_connection():
                self.radiobutton254.set_sensitive(True)
            else:
                self.radiobutton254.set_sensitive(False)
        else:
            self.radiobutton254.set_sensitive(False)

    def on_buttonwwokey_clicked(self, widget):
        if len(self.wwokey.get_text()) > 0:
            wwo = WorldWeatherOnlineService(key=self.wwokey.get_text())
            if wwo.test_connection():
                self.radiobutton252.set_sensitive(True)
            else:
                self.radiobutton252.set_sensitive(False)
        else:
            self.radiobutton252.set_sensitive(False)

    def on_image_wunderground_clicked(self, widget):
        webbrowser.open('http://www.wunderground.com/?apiref=6563686488165a78')

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

    def on_checkbutton10_toggled(self, widget):
        self.entry11.set_sensitive(not self.checkbutton10.get_active())
        self.button10.set_sensitive(not self.checkbutton10.get_active())
        self.checkbutton12.set_sensitive(not self.checkbutton10.get_active())
        self.checkbutton13.set_sensitive(not self.checkbutton10.get_active())

    def on_checkbutton11_toggled(self, widget):
        self.set_sensitive_frame1(self.checkbutton11.get_active())
        if self.checkbutton11.get_active() is False:
            self.checkbutton21.set_sensitive(False)
        elif (self.checkbutton11.get_active() is True and
              self.checkbutton21.get_active() is False):
            self.checkbutton11.set_sensitive(False)
        elif self.checkbutton21.get_sensitive() is False:
            self.checkbutton21.set_sensitive(True)

    def on_checkbutton14_toggled(self, widget):
        self.checkbutton15.set_sensitive(self.checkbutton14.get_active())
        self.checkbutton16.set_sensitive(self.checkbutton14.get_active())
        self.checkbutton17.set_sensitive(self.checkbutton14.get_active())
        self.checkbutton18.set_sensitive(self.checkbutton14.get_active())
        self.comboboxskin1.set_sensitive(self.checkbutton14.get_active())

    def on_checkbutton21_toggled(self, widget):
        self.set_sensitive_frame2(self.checkbutton21.get_active())
        (self.checkbutton21.get_active())
        if self.checkbutton21.get_active() is False:
            self.checkbutton11.set_sensitive(False)
        elif (self.checkbutton21.get_active() is True and
              self.checkbutton11.get_active() is False):
            self.checkbutton21.set_sensitive(False)
        elif self.checkbutton11.get_sensitive() is False:
            self.checkbutton11.set_sensitive(True)

    def on_checkbutton24_toggled(self, widget):
        self.checkbutton25.set_sensitive(self.checkbutton24.get_active())
        self.checkbutton26.set_sensitive(self.checkbutton24.get_active())
        self.checkbutton27.set_sensitive(self.checkbutton24.get_active())
        self.checkbutton28.set_sensitive(self.checkbutton24.get_active())
        self.comboboxskin2.set_sensitive(self.checkbutton24.get_active())

    def on_optionbutton41_toggled(self, widget):
        self.frame41.set_sensitive(widget.get_active())

    def on_optionbutton42_toggled(self, widget):
        self.frame42.set_sensitive(widget.get_active())

    def close_application(self, widget):
        self.ok = False
        self.destroy()

    def search_location(self, widget):
        cm1 = WhereAmI(self, location=self.entry11.get_text(),
                       latitude=self.latitude, longitude=self.longitude)
        if cm1.run() == Gtk.ResponseType.ACCEPT:
            lat, lon, loc = cm1.get_lat_lon_loc()
            print(lat, lon, loc)
            self.latitude = lat
            self.longitude = lon
            self.location = loc
            if self.location is not None:
                self.entry11.set_text(self.location)
        cm1.destroy()

    def search_location2(self, widget):
        cm2 = WhereAmI(self, location=self.entry21.get_text(),
                       latitude=self.latitude2, longitude=self.longitude2)
        if cm2.run() == Gtk.ResponseType.ACCEPT:
            lat, lon, loc = cm2.get_lat_lon_loc()
            self.latitude2 = lat
            self.longitude2 = lon
            self.location2 = loc
            if self.location2:
                self.entry21.set_text(self.location2)
        cm2.destroy()

    def load_preferences(self):
        configuration = Configuration()
        first_time = configuration.get('first-time')
        version = configuration.get('version')
        weatherservice = configuration.get('weather-service')
        if weatherservice == 'yahoo':
            self.radiobutton251.set_active(True)
        elif weatherservice == 'worldweatheronline':
            self.radiobutton252.set_active(True)
        elif weatherservice == 'openweathermap':
            self.radiobutton253.set_active(True)
        elif weatherservice == 'wunderground':
            self.radiobutton254.set_active(True)
        wwokey = configuration.get('wwo-key')
        if len(wwokey) > 0:
            self.wwokey.set_text(wwokey)
            wwo = WorldWeatherOnlineService(key=wwokey)
            if wwo.test_connection():
                self.radiobutton252.set_sensitive(True)
            else:
                if weatherservice == 'worldweatheronline':
                    self.radiobutton253.set_active(True)
        wukey = configuration.get('wu-key')
        if len(wukey) > 0:
            self.wukey.set_text(wukey)
            uws = UndergroundWeatherService(key=self.wukey.get_text())
            if uws.test_connection():
                self.radiobutton254.set_sensitive(True)
            else:
                if weatherservice == 'wunderground':
                    self.radiobutton253.set_active(True)
        #
        self.checkbutton11.set_active(configuration.get('main-location'))
        self.checkbutton10.set_active(configuration.get('autolocation'))
        self.location = configuration.get('location')
        self.latitude = configuration.get('latitude')
        self.longitude = configuration.get('longitude')
        if self.location:
            self.entry11.set_text(self.location)
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
        self.location2 = configuration.get('location2')
        self.latitude2 = configuration.get('latitude2')
        self.longitude2 = configuration.get('longitude2')
        if self.location2:
            self.entry21.set_text(self.location2)
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
        configuration = Configuration()
        if self.checkbutton11.get_active() and\
                (len(self.entry11.get_text()) == 0 or self.latitude is None or
                 self.latitude == 0 or self.longitude is None or
                 self.longitude == 0):
            self.latitude, self.longitude = ipaddress.get_current_location()
            ans = geocodeapi.get_inv_direction(self.latitude, self.longitude)
            if ans is not None and 'locality' in ans.keys():
                self.location = ans['locality']
        if self.checkbutton21.get_active() and\
                (len(self.entry21.get_text()) == 0 or
                 self.latitude2 is None or self.latitude2 == 0 or
                 self.longitude2 is None or self.longitude2 == 0):
            self.latitude2, self.longitude2 = ipaddress.get_current_location()
            ans = geocodeapi.get_inv_direction(self.latitude2, self.longitude2)
            if ans is not None and 'locality' in ans.keys():
                self.location2 = ans['locality']
        if len(self.entry11.get_text()) > 0:
            self.location = self.entry11.get_text()
        if len(self.entry21.get_text()) > 0:
            self.location2 = self.entry21.get_text()
        configuration.set('first-time', False)
        configuration.set('version', comun.VERSION)
        configuration.set('main-location', self.checkbutton11.get_active())
        configuration.set('autolocation', self.checkbutton10.get_active())
        configuration.set('location', self.location)
        configuration.set('latitude', self.latitude)
        configuration.set('longitude', self.longitude)
        configuration.set('show-temperature', self.checkbutton12.get_active())
        configuration.set('show-notifications',
                          self.checkbutton13.get_active())
        configuration.set('widget1', self.checkbutton14.get_active())
        configuration.set('onwidget1hide', self.checkbutton15.get_active())
        configuration.set('onwidget1top', self.checkbutton16.get_active())
        configuration.set('showintaskbar1', self.checkbutton17.get_active())
        configuration.set('onalldesktop1', self.checkbutton18.get_active())
        configuration.set('skin1',
                          get_selected_value_in_combo(self.comboboxskin1))
        #
        configuration.set('second-location', self.checkbutton21.get_active())
        configuration.set('location2', self.location2)
        configuration.set('latitude2', self.latitude2)
        configuration.set('longitude2', self.longitude2)
        configuration.set('show-temperature2', self.checkbutton22.get_active())
        configuration.set('show-notifications2',
                          self.checkbutton23.get_active())
        configuration.set('widget2', self.checkbutton24.get_active())
        configuration.set('onwidget2hide', self.checkbutton25.get_active())
        configuration.set('onwidget2top', self.checkbutton26.get_active())
        configuration.set('showintaskbar2', self.checkbutton27.get_active())
        configuration.set('onalldesktop2', self.checkbutton28.get_active())
        configuration.set('skin2',
                          get_selected_value_in_combo(self.comboboxskin2))
        #
        if self.radiobutton251.get_active():
            configuration.set('weather-service', 'yahoo')
        elif self.radiobutton253.get_active():
            configuration.set('weather-service', 'openweathermap')
        #
        wwokey = self.wwokey.get_text()
        if len(wwokey) > 0:
            wwo = WorldWeatherOnlineService(key=wwokey)
            if wwo.test_connection():
                configuration.set('wwo-key', wwokey)
                if self.radiobutton252.get_active():
                    configuration.set('weather-service', 'worldweatheronline')
            else:
                if self.radiobutton252.get_active():
                    configuration.set('weather-service', 'openweathermap')
        wukey = self.wukey.get_text()
        if len(wukey) > 0:
            wu = UndergroundWeatherService(key=wukey)
            if wu.test_connection():
                configuration.set('wu-key', wukey)
                if self.radiobutton254.get_active():
                    configuration.set('weather-service', 'wunderground')
            else:
                if self.radiobutton254.get_active():
                    configuration.set('weather-service', 'openweathermap')
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
        filestart = os.path.join(
            os.getenv("HOME"),
            ".config/autostart/my-weather-indicator-autostart.desktop")
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
    exit(0)
