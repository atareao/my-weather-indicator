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
