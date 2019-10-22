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
import datetime
from moon import Moon
import comun
from comun import _
from basedialog import BaseDialog

DAY_OF_WEEK = [_('Monday'), _('Tuesday'), _('Wednesday'), _('Thursday'),
               _('Friday'), _('Saturday'), _('Sunday')]


def first_day_of_month(adatetime):
    adatetime = adatetime.replace(day=1)
    return adatetime.weekday()


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


class CalendarWindow(BaseDialog):

    def __init__(self, adate=None):
        title = comun.APPNAME + ' | ' + _('Moon phases')
        self.adate = adate
        BaseDialog.__init__(self, title, cancel_button=False)

    def init_ui(self):
        BaseDialog.init_ui(self)

        self.headerbar = Gtk.HeaderBar.new()
        self.headerbar.set_title(self.get_title())
        self.headerbar.set_subtitle('-')
        self.headerbar.set_show_close_button(True)
        self.set_titlebar(self.headerbar)

        button0 = Gtk.Button()
        button0.set_size_request(40, 40)
        button0.set_tooltip_text(_('One year less'))
        button0.set_image(
            Gtk.Image.new_from_icon_name(Gtk.STOCK_GOTO_FIRST,
                                     Gtk.IconSize.BUTTON))
        button0.connect('clicked', self.on_button0_clicked)
        self.headerbar.pack_start(button0)

        button1 = Gtk.Button()
        button1.set_size_request(40, 40)
        button1.set_tooltip_text(_('One month less'))
        button1.set_image(
            Gtk.Image.new_from_icon_name(Gtk.STOCK_GO_BACK,
                                     Gtk.IconSize.BUTTON))
        button1.connect('clicked', self.on_button1_clicked)
        self.headerbar.pack_start(button1)

        button3 = Gtk.Button()
        button3.set_size_request(40, 40)
        button3.set_tooltip_text(_('One year more'))
        button3.set_image(
            Gtk.Image.new_from_icon_name(Gtk.STOCK_GOTO_LAST,
                                     Gtk.IconSize.BUTTON))
        button3.connect('clicked', self.on_button3_clicked)
        self.headerbar.pack_end(button3)

        button2 = Gtk.Button()
        button2.set_size_request(40, 40)
        button2.set_tooltip_text(_('One month more'))
        button2.set_image(
            Gtk.Image.new_from_icon_name(Gtk.STOCK_GO_FORWARD,
                                     Gtk.IconSize.BUTTON))
        button2.connect('clicked', self.on_button2_clicked)
        self.headerbar.pack_end(button2)

        button4 = Gtk.Button()
        button4.set_size_request(40, 40)
        button4.set_tooltip_text(_('Today'))
        image = Gtk.Image()
        image.set_from_pixbuf(
            GdkPixbuf.Pixbuf.new_from_file_at_size(
                os.path.join(
                    comun.IMAGESDIR,
                    '%s-light-normal.svg' % (
                        datetime.datetime.now().day)), 35, 35))
        button4.set_image(image)
        button4.connect('clicked', self.on_button4_clicked)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                  Gtk.PolicyType.AUTOMATIC)
        scrolledwindow.set_size_request(850, 560)

        self.grid.attach(scrolledwindow, 1, 1, 1, 1)

        table1 = Gtk.Grid()
        table1.set_border_width(2)
        scrolledwindow.add(table1)

        self.days = {}
        self.week_days = {}
        contador = 0
        for row in range(1, 7):
            label = Gtk.Label.new(str(row))
            label.set_width_chars(6)
            self.week_days[row] = label
            table1.attach(self.week_days[row], 0, row, 1, 1)
        for column in range(1, 8):
            label = Gtk.Label.new(DAY_OF_WEEK[column - 1])
            label.set_width_chars(14)
            label.set_size_request(0, 40)
            table1.attach(label,
                          column, 0, 1, 1)
        for row in range(1, 7):
            for column in range(1, 8):
                self.days[contador] = MoonDayWidget()
                table1.attach(self.days[contador], column, row, 1, 1)
                contador += 1
        if self.adate is None:
            self.adate = datetime.datetime.now()
        self.set_date()

    def close_application(self, widget):
        self.ok = False

    def set_date(self):
        self.headerbar.set_subtitle(self.adate.strftime('%B - %Y'))
        fdom = first_day_of_month(self.adate)
        adate = self.adate.replace(day=1)
        for row in range(1, 7):
            wd = adate + datetime.timedelta(days=7 * (row - 1))
            self.week_days[row].set_text(str(wd.isocalendar()[1]))
        max = {'position': -1, 'value': 0}
        med = {'position': -1, 'value': 1}
        min = {'position': -1, 'value': 1}
        for contador in range(0, 42):
            if contador < fdom:
                tadate = adate - datetime.timedelta(days=(fdom - contador))
            else:
                tadate = adate + datetime.timedelta(days=(contador - fdom))
            self.days[contador].set_date(tadate)
            if tadate.month != adate.month:
                self.days[contador].set_style('mcw_other_month')
            elif tadate.date() == datetime.datetime.today().date():
                self.days[contador].set_style('mcw_today')
                self.days[contador].set_tooltip_text(_('Today'))
            else:
                self.days[contador].set_style('mcw_current_month')
            if tadate.month == adate.month:
                if self.days[contador].get_position() >= max['value']:
                    max['position'] = contador
                    max['value'] = self.days[contador].get_position()
                if self.days[contador].get_position() <= min['value']:
                    min['position'] = contador
                    min['value'] = self.days[contador].get_position()
                if abs(float(self.days[contador].get_position()) - .5) <=\
                        (med['value']):
                    med['position'] = contador
                    med['value'] = abs(float(
                        self.days[contador].get_position()) - 0.5)
        self.days[med['position']].set_style('mcw_full')
        self.days[med['position']].set_tooltip_text(_('Full moon'))
        self.days[min['position']].set_style('mcw_med')
        self.days[min['position']].set_tooltip_text(_('New moon'))

    def on_button0_clicked(self, widget):
        year = self.adate.year - 1
        if year < 1:
            year = 1
        self.adate = self.adate.replace(year=year)
        self.set_date()

    def on_button1_clicked(self, widget):
        month = self.adate.month - 1
        if month < 1:
            month = 12
            year = self.adate.year - 1
            if year < 1:
                year = 1
            self.adate = self.adate.replace(month=month, year=year)
        else:
            self.adate = self.adate.replace(month=month)
        self.set_date()

    def on_button2_clicked(self, widget):
        month = self.adate.month + 1
        if month > 12:
            month = 1
            year = self.adate.year + 1
            self.adate = self.adate.replace(month=month, year=year)
        else:
            self.adate = self.adate.replace(month=month)
        self.set_date()

    def on_button3_clicked(self, widget):
        self.adate = self.adate.replace(year=(self.adate.year + 1))
        self.set_date()

    def on_button4_clicked(self, widget):
        today = datetime.datetime.today().date()
        self.adate = self.adate.replace(month=today.month, year=today.year)
        self.set_date()

    def on_button5_clicked(self, widget):
        self.hide()
        self.destroy()


if __name__ == "__main__":
    from comun import CSS_FILE
    from utils import load_css
    load_css(CSS_FILE)
    p = CalendarWindow()
    p.run()
    exit(0)
