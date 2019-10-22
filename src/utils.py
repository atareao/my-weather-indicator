#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2016 Lorenzo Carbonell
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

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
except ValueError as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
import os


DEFAULT_CURSOR = Gdk.Cursor(Gdk.CursorType.ARROW)
WAIT_CURSOR = Gdk.Cursor(Gdk.CursorType.WATCH)

def load_css(css_filename):
    with open(css_filename, 'r') as css_file:
        css_code = css_file.read()
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css_code.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)

def load_image(filename, size=24):
    if os.path.exists(filename):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filename, size, size)
        return Gtk.Image.new_from_pixbuf(pixbuf)
    return None



def redondea(valor):
    valor = valor * 10.0
    return int(valor) / 10.0


def redondea_digits(valor, digits=0):
    if digits == 0:
        return int(round(valor, digits))
    return round(valor, digits)


def s2f(cadena):
    try:
        value = float(cadena)
    except BaseException:
        value = 0.0
    return value


def s2f_print(word):
    try:
        return float(word)
    except Exception as e:
        print('error:', str(e))
    return 0


def cambia(valor, a, SI=True):
    if len(valor) == 0:
        return ''
    valor = float(valor)
    if SI is False:
        valor = redondea(5.0 / 9.0 * (valor - 32.0))
    if a == 'F':
        return str(redondea(valor * 9.0 / 5.0 + 32.0))
    elif a == 'K':
        return str(redondea(valor + 273.15))
    return str(valor)


def change_temperature(valor, a):
    valor = s2f(valor)
    # initial a in ºF
    if a == 'C':
        valor = 5.0 / 9.0 * (valor - 32.0)
    elif a == 'K':
        valor = 5.0 / 9.0 * (valor - 32.0) + 273.15
    return str(redondea_digits(valor))


def fa2f(temperature):
    return (temperature - 273.15) * 9.0 / 5.0 + 32.0


def f2c(temperature):
    return (s2f(temperature) - 32.0) * 5.0 / 9.0
