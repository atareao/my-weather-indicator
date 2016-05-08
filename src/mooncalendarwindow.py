#!/usr/bin/python3
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
#
#
#

from gi.repository import Gtk, Gdk, GObject
from gi.repository import GdkPixbuf
import os
import shutil
import locale
import gettext
import datetime
from moon import Moon
import comun
from comun import _

DAY_OF_WEEK = [_('Monday'), _('Tuesday'), _('Wednesday'), _('Thursday'),
               _('Friday'), _('Saturday'), _('Sunday')]


def first_day_of_month(adatetime):
    adatetime = adatetime.replace(day=1)
    return adatetime.weekday()


class MoonDayWidget(Gtk.EventBox):

    def __init__(self, adate=None):
        Gtk.EventBox.__init__(self)
        self.set_size_request(100, 70)
        box1 = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.add(box1)
        self.label = Gtk.Label()
        box1.pack_start(self.label, True, True, padding=1)
        self.image = Gtk.Image()
        box1.pack_start(self.image, True, True, padding=1)
        if adate is not None:
            self.set_date(adate)
        self.image.show()

    def set_date(self, adate):
        self.adate = adate
        self.label.set_text(str(adate.day))
        self.moon = Moon(adate)
        phasename = self.moon.phase()
        i = adate.day
        roundedpos = round(float(self.moon.position()), 3)
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


class CalendarWindow(Gtk.Window):

    def __init__(self, adate=None):
        title = comun.APPNAME + ' | '+_('Moon phases')
        '''
        Gtk.Dialog.__init__(self,
                            title,
                            None,
                            Gtk.DialogFlags.MODAL |
                            Gtk.DialogFlags.DESTROY_WITH_PARENT)
        '''
        Gtk.Window.__init__(self)
        self.set_size_request(750, 700)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_icon_from_file(comun.ICON)
        self.connect('destroy', self.close_application)
        self.edited = False
        #
        #
        self.headerbar = Gtk.HeaderBar.new()
        self.headerbar.set_title(title)
        self.headerbar.set_subtitle('-')
        self.headerbar.set_show_close_button(True)
        self.set_titlebar(self.headerbar)

        vbox0 = Gtk.VBox(spacing=5)
        vbox0.set_border_width(5)
        self.add(vbox0)
        #
        button0 = Gtk.Button()
        button0.set_size_request(40, 40)
        button0.set_tooltip_text(_('One year less'))
        button0.set_image(
            Gtk.Image.new_from_stock(Gtk.STOCK_GOTO_FIRST,
                                     Gtk.IconSize.BUTTON))
        button0.connect('clicked', self.on_button0_clicked)
        self.headerbar.pack_start(button0)
        #
        button1 = Gtk.Button()
        button1.set_size_request(40, 40)
        button1.set_tooltip_text(_('One month less'))
        button1.set_image(
            Gtk.Image.new_from_stock(Gtk.STOCK_GO_BACK,
                                     Gtk.IconSize.BUTTON))
        button1.connect('clicked', self.on_button1_clicked)
        self.headerbar.pack_start(button1)
        #
        button3 = Gtk.Button()
        button3.set_size_request(40, 40)
        button3.set_tooltip_text(_('One year more'))
        button3.set_image(
            Gtk.Image.new_from_stock(Gtk.STOCK_GOTO_LAST,
                                     Gtk.IconSize.BUTTON))
        button3.connect('clicked', self.on_button3_clicked)
        self.headerbar.pack_end(button3)
        #
        button2 = Gtk.Button()
        button2.set_size_request(40, 40)
        button2.set_tooltip_text(_('One month more'))
        button2.set_image(
            Gtk.Image.new_from_stock(Gtk.STOCK_GO_FORWARD,
                                     Gtk.IconSize.BUTTON))
        button2.connect('clicked', self.on_button2_clicked)
        self.headerbar.pack_end(button2)
        #
        frame1 = Gtk.Frame()
        vbox0.pack_start(frame1, True, True, 0)
        #
        hbox2 = Gtk.HBox()
        vbox0.pack_start(hbox2, False, False, 0)
        #
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
        hbox2.pack_start(button4, False, False, 0)
        #
        button5 = Gtk.Button()
        button5.set_size_request(40, 40)
        button5.set_tooltip_text(_('Close'))
        button5.set_image(
            Gtk.Image.new_from_stock(Gtk.STOCK_OK,
                                     Gtk.IconSize.BUTTON))
        button5.connect('clicked', self.on_button5_clicked)
        hbox2.pack_end(button5, False, False, 0)
        #
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                  Gtk.PolicyType.AUTOMATIC)
        scrolledwindow.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        frame1.add(scrolledwindow)
        #
        table1 = Gtk.Table(rows=7, columns=8, homogeneous=False)
        table1.override_background_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(1., 1., 1., 0))
        table1.set_border_width(2)
        table1.set_col_spacings(2)
        table1.set_row_spacings(2)
        scrolledwindow.add(table1)
        #
        self.days = {}
        self.week_days = {}
        contador = 0
        for row in range(1, 7):
            self.week_days[row] = Gtk.Label(str(row))
            table1.attach(self.week_days[row], 0, 0 + 1, row, row + 1,
                          xoptions=Gtk.AttachOptions.SHRINK,
                          yoptions=Gtk.AttachOptions.SHRINK)
        for column in range(1, 8):
            table1.attach(Gtk.Label(DAY_OF_WEEK[column-1]),
                          column,
                          column+1, 0, 1,
                          xoptions=Gtk.AttachOptions.SHRINK,
                          yoptions=Gtk.AttachOptions.SHRINK)
        for row in range(1, 7):
            for column in range(1, 8):
                self.days[contador] = MoonDayWidget()
                table1.attach(self.days[contador], column, column+1,
                              row, row+1,
                              xoptions=Gtk.AttachOptions.EXPAND,
                              yoptions=Gtk.AttachOptions.EXPAND)
                contador += 1
        #
        if adate is None:
            self.adate = datetime.datetime.now()
        else:
            self.adate = adate
        #
        self.set_date()
        #
        self.show_all()

    def close_application(self, widget):
        self.ok = False

    def set_date(self):
        self.headerbar.set_subtitle(self.adate.strftime('%B - %Y'))
        fdom = first_day_of_month(self.adate)
        adate = self.adate.replace(day=1)
        for row in range(1, 7):
            wd = adate + datetime.timedelta(days=7*(row-1))
            self.week_days[row].set_text(str(wd.isocalendar()[1]))
        max = {'position': -1, 'value': 0}
        med = {'position': -1, 'value': 1}
        min = {'position': -1, 'value': 1}
        for contador in range(0, 42):
            if contador < fdom:
                tadate = adate - datetime.timedelta(days=(fdom-contador))
            else:
                tadate = adate + datetime.timedelta(days=(contador-fdom))
            self.days[contador].set_date(tadate)
            if tadate.month != adate.month:
                self.days[contador].override_background_color(
                    Gtk.StateFlags.NORMAL, Gdk.RGBA(.5, .5, .5, 1))
            elif tadate.date() == datetime.datetime.today().date():
                self.days[contador].override_background_color(
                    Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 0.0, 0.0, 1))
            else:
                self.days[contador].override_background_color(
                    Gtk.StateFlags.NORMAL, Gdk.RGBA(1., 1., 1., 1))
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
        self.days[med['position']].override_background_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.5, 0.0, 1))
        self.days[min['position']].override_background_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(0.5, 0.0, 0.5, 1))

    def on_button0_clicked(self, widget):
        year = self.adate.year - 1
        if year < 1:
            year = 1
        self.adate = self.adate.replace(year=year)
        self.set_date()

    def on_button1_clicked(self, widget):
        month = self.adate.month-1
        if month < 1:
            month = 12
            year = self.adate.year-1
            if year < 1:
                year = 1
            self.adate = self.adate.replace(month=month, year=year)
        else:
            self.adate = self.adate.replace(month=month)
        self.set_date()

    def on_button2_clicked(self, widget):
        month = self.adate.month+1
        if month > 12:
            month = 1
            year = self.adate.year+1
            self.adate = self.adate.replace(month=month, year=year)
        else:
            self.adate = self.adate.replace(month=month)
        self.set_date()

    def on_button3_clicked(self, widget):
        self.adate = self.adate.replace(year=(self.adate.year+1))
        self.set_date()

    def on_button4_clicked(self, widget):
        today = datetime.datetime.today().date()
        self.adate = self.adate.replace(month=today.month, year=today.year)
        self.set_date()

    def on_button5_clicked(self, widget):
        self.hide()
        self.destroy()


if __name__ == "__main__":
    p = CalendarWindow()
    p.show_all()
    Gtk.main()
    exit(0)
