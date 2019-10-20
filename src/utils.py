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

from gi.repository import Gdk

def center(dialog):
    width, height = dialog.get_allocation().width, dialog.get_allocation().height
    monitor = Gdk.Display.get_primary_monitor(Gdk.Display.get_default())
    scale = monitor.get_scale_factor()
    mwidth = monitor.get_geometry().width / scale
    mheight = monitor.get_geometry().height / scale
    dialog.move((mwidth - width)/2, (mheight - height)/2)