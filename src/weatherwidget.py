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

import gi
try:
    gi.require_version('AppIndicator3', '0.1')
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
except Exception as e:
    print(e)
    print('Repository version required not present')
    exit(1)
from gi.repository import Gtk  # pyright: ignore
from gi.repository import Gdk  # pyright: ignore
from gi.repository import GObject  # pyright: ignore
from gi.repository import GdkPixbuf  # pyright: ignore
from gi.repository import AppIndicator3 as appindicator  # pyright: ignore
import cairo
import datetime
import os
import math
import comun
from configurator import Configuration


class WeatherWidget(Gtk.Window):
    __gsignals__ = {
        'pinit': (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (bool,)),
    }

    def __init__(self, indicator=None, widgetnumber=1, weather=None):
        Gtk.Window.__init__(self)
        self.set_title('My-Weather-Indicator')
        self.set_default_size(5, 5)
        self.set_icon_from_file(comun.ICON)
        if os.environ.get('DESKTOP_SESSION') == "ubuntu":
            self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        else:
            self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.supports_alpha = False
        self.set_decorated(False)
        self.set_border_width(0)
        self.set_accept_focus(False)
        self.set_app_paintable(True)
        self.set_skip_pager_hint(True)
        self.set_role('')
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual is not None and Gdk.Screen.get_default().is_composited():
            self.set_visual(visual)
        self.add_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self.connect('draw', self.on_expose, None)
        self.connect('configure-event', self.configure_event)
        self.connect('button-press-event', self.on_button_pressed)
        self.connect('button-release-event', self.on_button_released)
        self.connect('motion-notify-event', self.on_mouse_moved)
        self.connect('screen-changed', self.screen_changed)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.add(vbox)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        vbox.pack_start(hbox, False, False, 10)
        button = Gtk.Button()
        button.connect('clicked', self.on_button_clicked)
        hbox.pack_start(button, False, False, 10)
        self.pin = Gtk.Image()
        button.add(self.pin)
        button.set_name('pin')

        self.is_in_drag = False
        self.x_in_drag = 0
        self.y_in_drag = 0
        #
        self.datetime = datetime.datetime.utcnow()
        self.filename = None
        self.temperature = None
        self.location = None
        self.parse_time = False
        self.widgetnumber = widgetnumber
        self.indicator = indicator
        self.weather_data = weather
        self.load_preferences()
        self.read_widgetfile()
        ans = self.read_main_data()
        if ans is not None:
            self.set_size_request(ans[0], ans[1])
        self.parse_data()
        #
        style_provider = Gtk.CssProvider()
        css = """
            #pin{
                opacity:0.05;
                border-image: none;
                background-image: none;
                background-color: rgba(0, 0, 0, 0);
                border-radius: 0px;
                border-color: rgba(0, 0, 0, 0);
            }
            #pin:hover {
                transition: 1000ms linear;
                opacity:1.0;
                border-image: none;
                background-image: none;
                background-color: rgba(0, 0, 0, 0);
                border-radius: 0px;
                border-color: rgba(0, 0, 0, 0);
            }
        """
        style_provider.load_from_data(css.encode('UTF-8'))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        #
        self.screen_changed(self)
        self.show_all()

    def read_widgetfile(self):
        if os.path.exists(os.path.join(self.skin, 'skin')):
            f = open(os.path.join(self.skin, 'skin'))
            self.widgetdata = f.read()
            f.close()
            if self.widgetdata.find('$HOUR$') > -1 or\
                    self.widgetdata.find('$MINUTES$') > -1:
                self.parse_time = True
            else:
                self.parse_time = False
        else:
            self.skin = None
            self.widgetdata = None

    def set_weather(self, weather):
        self.weather_data = weather
        self.parse_data()
        self.queue_draw()

    def set_location(self, location):
        self.location = location
        self.parse_data()
        self.queue_draw()

    def set_datetime(self, utcnow):
        parse_time = (self.datetime.day != utcnow.day)
        self.datetime = utcnow
        if self.parse_time or parse_time:
            self.parse_data()
            self.queue_draw()

    def set_hideindicator(self, hideindicator):
        self.hideindicator = hideindicator
        if hideindicator:
            if self.indicator.get_status() ==\
                    appindicator.IndicatorStatus.PASSIVE:
                self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
            else:
                self.indicator.set_status(appindicator.IndicatorStatus.PASSIVE)

    def is_set_keep_above(self, keep_above):
        self.is_above = keep_above
        if keep_above:
            self.pin.set_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    os.path.join(comun.IMAGESDIR, 'pinin.svg'), 36, 72, 1))
        else:
            self.pin.set_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    os.path.join(comun.IMAGESDIR, 'pinup.svg'), 36, 36, 1))
        self.hide()
        self.show()

    def load_preferences(self):
        configuration = Configuration()
        self.a24h = configuration.get('24h')
        if self.widgetnumber == 0:
            x = configuration.get('wp1-x')
            y = configuration.get('wp1-y')
            self.location = configuration.get('location')
            self.showwidget = configuration.get('widget1')
            self.hideindicator = configuration.get('onwidget1hide')
            self.set_keep_above(configuration.get('onwidget1top'))
            self.is_set_keep_above(configuration.get('onwidget1top'))
            self.set_keep_below(not configuration.get('onwidget1top'))
            self.set_skip_taskbar_hint(not configuration.get('showintaskbar1'))
            if configuration.get('onalldesktop1'):
                self.stick()
            else:
                self.unstick()
            self.skin = configuration.get('skin1')
        else:
            x = configuration.get('wp2-x')
            y = configuration.get('wp2-y')
            self.location = configuration.get('location2')
            self.showwidget = configuration.get('widget2')
            self.hideindicator = configuration.get('onwidget2hide')
            self.set_keep_above(configuration.get('onwidget2top'))
            self.is_set_keep_above(configuration.get('onwidget2top'))
            self.set_keep_below(not configuration.get('onwidget2top'))
            self.set_skip_taskbar_hint(not configuration.get('showintaskbar2'))
            if configuration.get('onalldesktop2'):
                self.stick()
            else:
                self.unstick()
            self.skin = configuration.get('skin2')
        self.move(x, y)

    def show_in_taskbar(self, show_in_taskbar):
        self.set_skip_taskbar_hint(not show_in_taskbar)

    def save_preferences(self):
        configuration = Configuration()
        x, y = self.get_position()
        if self.widgetnumber == 0:
            configuration.set('wp1-x', x)
            configuration.set('wp1-y', y)
            configuration.set('onwidget1top', self.is_above)
        else:
            configuration.set('wp2-x', x)
            configuration.set('wp2-y', y)
            configuration.set('onwidget2top', self.is_above)
        configuration.save()

    def on_button_clicked(self, widget):
        self.emit('pinit', not self.is_above)

    def screen_changed(self, widget, old_screen=None):
        # To check if the display supports alpha channels, get the colormap
        screen = widget.get_screen()
        visual = screen.get_rgba_visual()
        if visual is None or not Gdk.Screen.get_default().is_composited():
            self.supports_alpha = False
        else:
            self.supports_alpha = True
        return False

    def configure_event(self, widget, event):
        self.save_preferences()

    def on_mouse_moved(self, widget, event):
        if self.is_in_drag:
            xi, yi = self.get_position()
            xf = int(xi + event.x_root - self.x_in_drag)
            yf = int(yi + event.y_root - self.y_in_drag)
            if math.sqrt(math.pow(xf-xi, 2) + math.pow(yf-yi, 2)) > 10:
                self.x_in_drag = event.x_root
                self.y_in_drag = event.y_root
                self.move(xf, yf)

    def on_button_released(self, widget, event):
        if event.button == 1:
            self.is_in_drag = False
            self.x_in_drag = event.x_root
            self.y_in_drag = event.y_root

    def on_button_pressed(self, widget, event):
        if self.hideindicator:
            if self.indicator.get_status() ==\
                    appindicator.IndicatorStatus.PASSIVE:
                self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
            else:
                self.indicator.set_status(appindicator.IndicatorStatus.PASSIVE)
        if event.button == 1:
            self.is_in_drag = True
            self.x_in_drag, self.y_in_drag = self.get_position()
            self.x_in_drag = event.x_root
            self.y_in_drag = event.y_root
            return True
        return False

    def on_expose(self, widget, cr, data):
        if self.surface is not None:
            cr.save()
            cr.set_operator(cairo.OPERATOR_CLEAR)
            cr.rectangle(0.0, 0.0, *widget.get_size())
            cr.fill()
            cr.restore()
            while Gtk.events_pending():
                Gtk.main_iteration()
            '''
            if self.supports_alpha:
                pb = take_screenshot(widget)
                surface = get_surface_from_pixbuf(pb)
                cr.save()
                cr.set_source_surface(surface)
                cr.paint()
                cr.restore()
            '''
            cr.save()
            cr.set_source_surface(self.surface)
            cr.paint()
            cr.restore()

    def read_main_data(self):
        if self.widgetdata is not None:
            row = self.widgetdata.split('\n')[0].split('|')
            if row[0] == 'MAIN':
                atype, title, width, height = row
                width = int(width)
                height = int(height)
                return width, height
        return None

    def parse_data(self):
        if self.skin is not None and\
                os.path.exists(os.path.join(self.skin, 'skin')):
            maindir = self.skin
            ans = self.read_main_data()
            if ans is not None and self.weather_data is not None:
                mainsurface = cairo.ImageSurface(
                    cairo.FORMAT_ARGB32, ans[0], ans[1])
                cr = cairo.Context(mainsurface)
                # try:
                for index, line in enumerate(self.widgetdata.split('\n')):
                    row = line.split('|')
                    cr.save()
                    if row is not None and len(row) > 1:
                        if row[0] == 'CLOCK':
                            atype, minutesorhours, fileimage, x, y, width,\
                                height, xpos, ypos = row
                            fileimage = os.path.join(maindir, fileimage)
                            x = float(x)
                            y = float(y)
                            width = float(width)
                            height = float(height)
                            surface = get_surface_from_file(fileimage)
                            if surface is not None:
                                s_width = surface.get_width()
                                s_height = surface.get_height()
                                if xpos == 'CENTER':
                                    x = x - width / 2.0
                                elif xpos == 'RIGHT':
                                    x = x - width
                                if ypos == 'CENTER':
                                    y = y - height / 2.0
                                elif ypos == 'BOTTOM':
                                    y = y - height
                                hours = float(self.weather_data['current_conditions']['rawOffset'])
                                now = self.datetime +\
                                    datetime.timedelta(hours=hours)
                                atime = float(now.hour) + float(now.minute) / 60.0
                                hours = atime
                                if not self.a24h and hours > 12:
                                    hours -= 12.0
                                minutes = (atime - int(atime)) * 60.0
                                cr.translate(x, y)
                                cr.scale(width / s_width, height / s_height)
                                if minutesorhours == '$HOUR$':
                                    cr.rotate(2.0 * math.pi / 12.0 * hours - math.pi / 2.0)
                                elif minutesorhours == '$MINUTES$':
                                    cr.rotate(2.0 * math.pi / 60.0 * minutes - math.pi / 2.0)
                                cr.set_source_surface(surface)
                                cr.paint()
                        elif row[0] == 'IMAGE':
                            atype, fileimage, x, y, width, height, xpos, ypos = row
                            if self.weather_data is not None:
                                if fileimage == '$CONDITION$':
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['current_conditions']['condition_image'])
                                elif fileimage == '$CONDITION_ICON_LIGHT$':
                                    fileimage = os.path.join(comun.ICONDIR, self.weather_data['current_conditions']['condition_icon_light'])
                                elif fileimage == '$CONDITION_ICON_DARK':
                                    fileimage = os.path.join(comun.ICONDIR, self.weather_data['current_conditions']['condition_icon_dark'])
                                elif fileimage == '$MOONPHASE$':
                                    fileimage = os.path.join(comun.IMAGESDIR, self.weather_data['current_conditions']['moon_icon'])
                                elif fileimage == '$WIND$':
                                    fileimage = os.path.join(comun.IMAGESDIR, self.weather_data['current_conditions']['wind_icon'])
                                elif fileimage == '$CONDITION_01$' and len(self.weather_data['forecasts']) > 0:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][0]['condition_image'])
                                elif fileimage == '$CONDITION_02$' and len(self.weather_data['forecasts']) > 1:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][1]['condition_image'])
                                elif fileimage == '$CONDITION_03$' and len(self.weather_data['forecasts']) > 2:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][2]['condition_image'])
                                elif fileimage == '$CONDITION_04$' and len(self.weather_data['forecasts']) > 3:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][3]['condition_image'])
                                elif fileimage == '$CONDITION_05$' and len(self.weather_data['forecasts']) > 4:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][4]['condition_image'])
                                elif fileimage == '$MOONPHASE_01$' and len(self.weather_data['forecasts']) > 0:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][0]['moon_phase'])
                                elif fileimage == '$MOONPHASE_02$' and len(self.weather_data['forecasts']) > 1:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][1]['moon_phase'])
                                elif fileimage == '$MOONPHASE_03$' and len(self.weather_data['forecasts']) > 2:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][2]['moon_phase'])
                                elif fileimage == '$MOONPHASE_04$' and len(self.weather_data['forecasts']) > 3:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][3]['moon_phase'])
                                elif fileimage == '$MOONPHASE_05$' and len(self.weather_data['forecasts']) > 4:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][4]['moon_phase'])
                                elif fileimage == '$WIND_01$' and len(self.weather_data['forecasts']) > 0:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][0]['wind_icon'])
                                elif fileimage == '$WIND_02$' and len(self.weather_data['forecasts']) > 1:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][1]['wind_icon'])
                                elif fileimage == '$WIND_03$' and len(self.weather_data['forecasts']) > 2:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][2]['wind_icon'])
                                elif fileimage == '$WIND_04$' and len(self.weather_data['forecasts']) > 3:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][3]['wind_icon'])
                                elif fileimage == '$WIND_05$' and len(self.weather_data['forecasts']) > 4:
                                    fileimage = os.path.join(comun.WIMAGESDIR, self.weather_data['forecasts'][4]['wind_icon'])
                                else:
                                    fileimage = os.path.join(maindir, fileimage)
                            else:
                                fileimage = os.path.join(maindir, fileimage)
                            x = float(x)
                            y = float(y)
                            width = float(width)
                            height = float(height)
                            surface = get_surface_from_file(fileimage)
                            if surface is not None:
                                s_width = surface.get_width()
                                s_height = surface.get_height()
                                if xpos == 'CENTER':
                                    x = x - width / 2.0
                                elif xpos == 'RIGHT':
                                    x = x - width
                                if ypos == 'CENTER':
                                    y = y - height / 2.0
                                elif ypos == 'BOTTOM':
                                    y = y - height
                                cr.translate(x, y)
                                cr.scale(width / s_width, height / s_height)
                                cr.set_source_surface(surface)
                                cr.paint()
                        elif row[0] == 'TEXT':
                            atype, text, x, y, font, size, color, xpos, ypos = row
                            x = float(x)
                            y = float(y)
                            size = int(size)
                            r, g, b, a = color.split(',')
                            cr.set_source_rgba(float(r), float(g), float(b), float(a))
                            cr.select_font_face(font)
                            cr.set_font_size(size)
                            now = self.datetime + datetime.timedelta(hours=float(self.weather_data['current_conditions']['rawOffset']))
                            if self.parse_time:
                                now = self.datetime + datetime.timedelta(hours=float(self.weather_data['current_conditions']['rawOffset']))
                                hours = now.hour
                                if not self.a24h:
                                    if hours > 12:
                                        hours -= 12
                                    if hours < 1:
                                        hours += 12
                                hours = str(hours)
                                hours = '0' * (2 - len(hours)) + hours
                                minutes = str(now.minute)
                                minutes = '0' * (2 - len(minutes)) + minutes
                                if text.find('$HOUR$') > -1:
                                    text = text.replace('$HOUR$', hours)
                                if text.find('$MINUTES$') > -1:
                                    text = text.replace('$MINUTES$', minutes)
                            if text.find('$WEEKDAY$') > -1:
                                text = text.replace('$WEEKDAY$', now.strftime('%A'))
                            if text.find('$DAY$') > -1:
                                text = text.replace('$DAY$', now.strftime('%d'))
                            if text.find('$MONTH$') > -1:
                                text = text.replace('$MONTH$', now.strftime('%m'))
                            if text.find('$MONTHNAME$') > -1:
                                text = text.replace('$MONTHNAME$', now.strftime('%B'))
                            if text.find('$YEAR$') > -1:
                                text = text.replace('$YEAR$', now.strftime('%Y'))
                            if text.find('$LOCATION$') > -1 and self.location is not None:
                                text = text.replace('$LOCATION$', self.location)
                            if self.weather_data is not None:
                                if text.find('$TEMPERATURE$') > -1:
                                    text = text.replace('$TEMPERATURE$', '{0}{1:c}'.format(self.weather_data['current_conditions']['temperature'], 176))
                                if text.find('$MAX_TEMPERATURE$') > -1:
                                    text = text.replace('$MAX_TEMPERATURE$', '{0}{1:c}'.format(self.weather_data['forecasts'][0]['high'], 176))
                                if text.find('$MIN_TEMPERATURE$') > -1:
                                    text = text.replace('$MIN_TEMPERATURE$', '{0}{1:c}'.format(self.weather_data['forecasts'][0]['low'], 176))
                                if text.find('$HUMIDITY$') > -1:
                                    text = text.replace('$HUMIDITY$', self.weather_data['current_conditions']['humidity'])
                                if text.find('$PRESSURE$') > -1:
                                    text = text.replace('$PRESSURE$', self.weather_data['current_conditions']['pressure'])
                                if text.find('$WIND$') > -1:
                                    text = text.replace('$WIND$', self.weather_data['current_conditions']['wind_condition'])
                                if text.find('$CONDITION$') > -1:
                                    text = text.replace('$CONDITION$', self.weather_data['current_conditions']['condition_text'])
                                if len(self.weather_data['forecasts']) > 0:
                                    if text.find('$MAX_TEMPERATURE_01$') > -1:
                                        text = text.replace('$MAX_TEMPERATURE_01$', self.weather_data['forecasts'][0]['high'])
                                    if text.find('$MIN_TEMPERATURE_01$') > -1:
                                        text = text.replace('$MIN_TEMPERATURE_01$', self.weather_data['forecasts'][0]['low'])
                                    if text.find('$CONDITION_01$') > -1:
                                        text = text.replace('$CONDITION_01$', self.weather_data['forecasts'][0]['condition_text'])
                                    if text.find('$DAY_OF_WEEK_01$') > -1:
                                        text = text.replace('$DAY_OF_WEEK_01$', self.weather_data['forecasts'][0]['day_of_week'])
                                    if text.find('$WIND_01$') > -1:
                                        text = text.replace('$WIND_01$', self.weather_data['forecasts'][0]['avewind'])
                                if len(self.weather_data['forecasts']) > 1:
                                    if text.find('$MAX_TEMPERATURE_02$') > -1:
                                        text = text.replace('$MAX_TEMPERATURE_02$', self.weather_data['forecasts'][1]['high'])
                                    if text.find('$MIN_TEMPERATURE_02$') > -1:
                                        text = text.replace('$MIN_TEMPERATURE_02$', self.weather_data['forecasts'][1]['low'])
                                    if text.find('$CONDITION_02$') > -1:
                                        text = text.replace('$CONDITION_02$', self.weather_data['forecasts'][1]['condition_text'])
                                    if text.find('$DAY_OF_WEEK_02$') > -1:
                                        text = text.replace('$DAY_OF_WEEK_02$', self.weather_data['forecasts'][1]['day_of_week'])
                                    if text.find('$WIND_02$') > -1:
                                        text = text.replace('$WIND_02$', self.weather_data['forecasts'][1]['avewind'])
                                if len(self.weather_data['forecasts']) > 2:
                                    if text.find('$MAX_TEMPERATURE_03$') > -1:
                                        text = text.replace('$MAX_TEMPERATURE_03$', self.weather_data['forecasts'][2]['high'])
                                    if text.find('$MIN_TEMPERATURE_03$') > -1:
                                        text = text.replace('$MIN_TEMPERATURE_03$', self.weather_data['forecasts'][2]['low'])
                                    if text.find('$CONDITION_03$') > -1:
                                        text = text.replace('$CONDITION_03$', self.weather_data['forecasts'][2]['condition_text'])
                                    if text.find('$DAY_OF_WEEK_03$') > -1:
                                        text = text.replace('$DAY_OF_WEEK_03$', self.weather_data['forecasts'][2]['day_of_week'])
                                    if text.find('$WIND_03$') > -1:
                                        text = text.replace('$WIND_03$', self.weather_data['forecasts'][2]['avewind'])
                                if len(self.weather_data['forecasts']) > 3:
                                    if text.find('$MAX_TEMPERATURE_04$') > -1:
                                        text = text.replace('$MAX_TEMPERATURE_04$', self.weather_data['forecasts'][3]['high'])
                                    if text.find('$MIN_TEMPERATURE_04$') > -1:
                                        text = text.replace('$MIN_TEMPERATURE_04$', self.weather_data['forecasts'][3]['low'])
                                    if text.find('$CONDITION_04$') > -1:
                                        text = text.replace('$CONDITION_04$', self.weather_data['forecasts'][3]['condition_text'])
                                    if text.find('$DAY_OF_WEEK_04$') > -1:
                                        text = text.replace('$DAY_OF_WEEK_04$', self.weather_data['forecasts'][3]['day_of_week'])
                                    if text.find('$WIND_04$') > -1:
                                        text = text.replace('$WIND_04$', self.weather_data['forecasts'][3]['avewind'])
                                if len(self.weather_data['forecasts']) > 4:
                                    if text.find('$MAX_TEMPERATURE_05$') > -1:
                                        text = text.replace('$MAX_TEMPERATURE_05$', self.weather_data['forecasts'][4]['high'])
                                    if text.find('$MIN_TEMPERATURE_05$') > -1:
                                        text = text.replace('$MIN_TEMPERATURE_05$', self.weather_data['forecasts'][4]['low'])
                                    if text.find('$CONDITION_05$') > -1:
                                        text = text.replace('$CONDITION_05$', self.weather_data['forecasts'][4]['condition_text'])
                                    if text.find('$DAY_OF_WEEK_05$') > -1:
                                        text = text.replace('$DAY_OF_WEEK_05$', self.weather_data['forecasts'][4]['day_of_week'])
                                    if text.find('$WIND_05$') > -1:
                                        text = text.replace('$WIND_05$', self.weather_data['forecasts'][4]['avewind'])

                            x_bearing, y_bearing, width, height, x_advance, y_advance = cr.text_extents(text)
                            if xpos == 'CENTER':
                                x = x - width / 2.0
                            elif xpos == 'RIGHT':
                                x = x - width
                            if ypos == 'CENTER':
                                y = y + height / 2.0
                            elif ypos == 'TOP':
                                y = y + height
                            cr.move_to(x, y)
                            cr.show_text(text)
                    cr.restore()
                self.surface = mainsurface
                return
        self.surface = None


def take_screenshot(widget):
    w = Gdk.get_default_root_window()
    left, top = widget.get_position()
    width, height = widget.get_size()
    pixbuf = Gdk.pixbuf_get_from_window(w, left, top, width, height)
    return pixbuf


def get_surface_from_pixbuf(pixbuf):
    surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32, pixbuf.get_width(), pixbuf.get_height())
    micairo = cairo.Context(surface)
    micairo.save()
    Gdk.cairo_set_source_pixbuf(micairo, pixbuf, 0, 0)
    micairo.paint()
    micairo.restore()
    return surface


def get_surface_from_file(filename):
    if os.path.exists(filename):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
        if pixbuf:
            surface = cairo.ImageSurface(
                cairo.FORMAT_ARGB32, pixbuf.get_width(), pixbuf.get_height())
            context = cairo.Context(surface)
            Gdk.cairo_set_source_pixbuf(context, pixbuf, 0, 0)
            context.paint()
            return surface
    return None


def transparent_expose(widget, event):
    cr = widget.cairo_create()
    cr.set_operator(cairo.OPERATOR_CLEAR)
    region = Gtk.gdk.region_rectangle(event.area)
    cr.region(region)
    cr.fill()
    return False


if __name__ == "__main__":
    ss = WeatherWidget()
    ss.show()
    Gtk.main()
    exit(0)
