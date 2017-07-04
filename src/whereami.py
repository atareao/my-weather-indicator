#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#
# Copyright (C) 2012 Lorenzo Carbonell
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
    gi.require_version('OsmGpsMap', '1.0')
    gi.require_version('GLib', '2.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import WebKit
from gi.repository import OsmGpsMap
from geolocation import get_latitude_longitude_city
from async import async_function
import geocodeapi
import comun
from comun import _


def match_anywhere(completion, entrystr, iter, data):
    modelstr = completion.get_model()[iter][2]['city'].lower()
    print(entrystr, modelstr)
    return modelstr.startswith(entrystr.lower())


class WhereAmI(Gtk.Dialog):
    def __init__(self, parent=None, location=None, latitude=0,
                 longitude=0):
        # ***************************************************************
        Gtk.Dialog.__init__(self, 'my-weather-indicator | ' + _('Where Am I'),
                            parent, Gtk.DialogFlags.MODAL |
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                             Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        # self.set_size_request(450, 350)
        self.connect('destroy', self.on_close_application)
        self.set_icon_from_file(comun.ICON)
        #
        self.lat = latitude
        self.lng = longitude
        self.locality = location
        #
        vbox = Gtk.VBox()
        self.get_content_area().add(vbox)
        #
        hbox = Gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)
        #
        self.entry1 = Gtk.Entry()
        self.entry1.set_width_chars(60)

        self.entry1.set_property('primary_icon_name', 'edit-find-symbolic')
        self.entry1.set_property('secondary_icon_name', 'edit-clear-symbolic')
        self.entry1.set_property('primary_icon_tooltip_text',
                                 _('Search location'))
        self.entry1.set_property('secondary_icon_tooltip_text',
                                 _('Clear location'))
        self.entry1.set_tooltip_text(_('Input the name of your city'))
        self.entry1.connect('icon-press', self.on_icon_press)
        self.entry1.connect('activate', self.on_button1_clicked)
        hbox.pack_start(self.entry1, True, True, 0)
        #
        button1 = Gtk.Button(_('Search'))
        button1.connect('clicked', self.on_button1_clicked)
        hbox.pack_start(button1, False, False, 0)
        #
        button2 = Gtk.Button(_('Find me'))
        button2.connect('clicked', self.on_button2_clicked)
        hbox.pack_start(button2, False, False, 0)
        self.expander = Gtk.Expander(label=_('Locations found'))
        self.expander.set_expanded(False)
        vbox.pack_start(self.expander, False, False, 0)
        #
        frame = Gtk.Frame()
        self.expander.add(frame)
        self.expander.connect("notify::expanded", self.on_expander_expanded)
        #
        scrolledwindow0 = Gtk.ScrolledWindow()
        scrolledwindow0.set_policy(Gtk.PolicyType.AUTOMATIC,
                                   Gtk.PolicyType.AUTOMATIC)
        scrolledwindow0.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        scrolledwindow0.set_size_request(450, 100)
        frame.add(scrolledwindow0)
        # city, county, country, latitude, longitude
        store = Gtk.ListStore(str, str, str, float, float)
        store.set_sort_column_id(2, Gtk.SortType.ASCENDING)
        self.treeview = Gtk.TreeView(model=store)
        self.treeview.set_reorderable(True)
        treeviewcolumn0 = Gtk.TreeViewColumn(_('City'),
                                             Gtk.CellRendererText(), text=0)
        treeviewcolumn0.set_reorderable(True)
        treeviewcolumn0.set_sort_column_id(0)
        treeviewcolumn1 = Gtk.TreeViewColumn(_('State'),
                                             Gtk.CellRendererText(), text=1)
        treeviewcolumn1.set_reorderable(True)
        treeviewcolumn1.set_sort_column_id(1)
        treeviewcolumn2 = Gtk.TreeViewColumn(_('Country'),
                                             Gtk.CellRendererText(), text=2)
        treeviewcolumn2.set_reorderable(True)
        treeviewcolumn2.set_sort_column_id(2)
        self.treeview.append_column(treeviewcolumn0)
        self.treeview.append_column(treeviewcolumn1)
        self.treeview.append_column(treeviewcolumn2)
        self.treeview.connect('cursor-changed',
                              self.ontreeviewcursorchanged)
        scrolledwindow0.add(self.treeview)
        #
        #
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                  Gtk.PolicyType.AUTOMATIC)
        scrolledwindow.set_shadow_type(Gtk.ShadowType.IN)
        vbox.pack_start(scrolledwindow, True, True, 0)
        #
        self.viewer = OsmGpsMap.Map()
        self.viewer.layer_add(OsmGpsMap.MapOsd(show_dpad=True,
                                               show_zoom=True,
                                               show_crosshair=True))
        # connect keyboard shortcuts
        self.viewer.set_keyboard_shortcut(OsmGpsMap.MapKey_t.FULLSCREEN,
                                          Gdk.keyval_from_name("F11"))
        self.viewer.set_keyboard_shortcut(OsmGpsMap.MapKey_t.UP,
                                          Gdk.keyval_from_name("Up"))
        self.viewer.set_keyboard_shortcut(OsmGpsMap.MapKey_t.DOWN,
                                          Gdk.keyval_from_name("Down"))
        self.viewer.set_keyboard_shortcut(OsmGpsMap.MapKey_t.LEFT,
                                          Gdk.keyval_from_name("Left"))
        self.viewer.set_keyboard_shortcut(OsmGpsMap.MapKey_t.RIGHT,
                                          Gdk.keyval_from_name("Right"))
        scrolledwindow.add(self.viewer)
        scrolledwindow.set_size_request(550, 550)

        #
        self.show_all()
        #
        self.set_wait_cursor()
        self.search_string = ''
        self.locality = ''
        print('============================')
        print(location, latitude, longitude)
        print('============================')
        if latitude and longitude:
            self.latitude = latitude
            self.longitude = longitude
            self.viewer.set_center_and_zoom(self.lat, self.lng, 14)
            if location is not None and len(location) > 0:
                self.locality = location
                print(1)
                self.entry1.set_text(location)
            else:
                print(2)
                self.do_search_location(latitude, longitude)
        else:
            self.search_location2()
        self.set_normal_cursor()

    def on_expander_expanded(self, widget, selected):
        print(widget, selected)
        if not self.expander.get_expanded():
            self.resize(450, 350)

    def ontreeviewcursorchanged(self, treeview):
        selection = treeview.get_selection()
        if selection is not None:
            model, aiter = treeview.get_selection().get_selected()
            if model is not None and aiter is not None:
                self.entry1.set_text(model[aiter][0])
                self.locality = model[aiter][0]
                self.lat = model[aiter][3]
                self.lng = model[aiter][4]
                self.viewer.set_center_and_zoom(self.lat, self.lng, 14)

    def on_icon_press(self, widget, icon_pos, event):
        if icon_pos == Gtk.EntryIconPosition.PRIMARY:
            self.on_button1_clicked(None)
        elif icon_pos == Gtk.EntryIconPosition.SECONDARY:
            self.entry1.set_text('')

    def on_permission_request(self, widget, frame, geolocationpolicydecision):
        WebKit.geolocation_policy_allow(geolocationpolicydecision)
        return True

    def on_button2_clicked(self, widget):
        self.do_center()

    def do_center(self):
        def on_center_done(result, error):
            print(result)
            if result is not None:
                latitude, longitude, city = result
                self.lat = latitude
                self.lng = longitude
                self.locality = city
                self.entry1.set_text(city)
                print(self.lat, self.lng)
                self.viewer.set_center_and_zoom(self.lat, self.lng, 14)
            self.set_normal_cursor()

        @async_function(on_done=on_center_done)
        def do_center_in_thread():
            return get_latitude_longitude_city()

        self.set_wait_cursor()
        do_center_in_thread()

    def on_button1_clicked(self, widget):
        self.set_wait_cursor()
        search_string = self.entry1.get_text()
        model = self.treeview.get_model()
        model.clear()
        self.expander.set_expanded(True)
        print(search_string)
        for direction in geocodeapi.get_directions(search_string):
            print(direction)
            # city, county, state, country, latitude, longitude
            if 'city' in direction.keys() and\
                    direction['city'] is not None and\
                    len(direction['city']) > 0:
                model.append([direction['city'], direction['state'],
                              direction['country'], direction['lat'],
                              direction['lng']])
        if len(model) > 0:
            self.treeview.set_cursor(0)
        self.set_normal_cursor()

    def search_location2(self):
        self.do_center()

    def do_search_location(self, latitude, longitude):
        def on_search_location_done(result, error):
            print(6)
            print(result)
            if result is not None:
                self.lat = result['lat']
                self.lng = result['lng']
                if result['city'] is None:
                    if result['state'] is not None:
                        city = result['state']
                    else:
                        city = result['country']
                else:
                    city = result['city']
                self.locality = city
                self.entry1.set_text(city)
                self.viewer.set_center_and_zoom(self.lat, self.lng, 14)
            self.set_normal_cursor()

        @async_function(on_done=on_search_location_done)
        def do_search_location_in_thread(latitude, longitude):
            print(5)
            return geocodeapi.get_inv_direction(latitude, longitude)
        print(3)
        self.set_wait_cursor()
        print(4)
        do_search_location_in_thread(latitude, longitude)

    def on_close_application(self, widget):
        self.set_normal_cursor()
        self.hide()

    def get_lat_lon_loc(self):
        return self.lat, self.lng, self.locality

    def set_wait_cursor(self):
        self.get_root_window().set_cursor(Gdk.Cursor(Gdk.CursorType.WATCH))
        while Gtk.events_pending():
            Gtk.main_iteration()

    def set_normal_cursor(self):
        self.get_root_window().set_cursor(Gdk.Cursor(Gdk.CursorType.ARROW))
        while Gtk.events_pending():
            Gtk.main_iteration()


if __name__ == '__main__':
    cm = WhereAmI()
    if cm.run() == Gtk.ResponseType.ACCEPT:
        print(cm.get_lat_lon_loc())
    cm.hide()
    cm.destroy()
    exit(0)
