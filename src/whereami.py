#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
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
#
#
#

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import WebKit
import sys
if sys.version_info[0] > 2:
	import queue
else:
	import Queue as queue
import ipaddress
import geocodeapi
import comun
import time
from comun import _

def match_anywhere(completion, entrystr, iter, data):
    modelstr = completion.get_model()[iter][2]['city'].lower()
    print(entrystr,modelstr)
    return modelstr.startswith(entrystr.lower())

def wait(time_lapse):
	time_start = time.time()
	time_end = (time_start + time_lapse)
	while time_end > time.time():
		while Gtk.events_pending():
			Gtk.main_iteration()

class WhereAmI(Gtk.Dialog): # needs GTK, Python, Webkit-GTK
	def __init__(self,parent=None,location = None,latitude=None,longitude=None):
		#***************************************************************
		Gtk.Dialog.__init__(self,'my-weather-indicator | '+_('Where Am I'),parent,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		#self.set_size_request(450, 350)
		self.connect('destroy', self.on_close_application)
		self.set_icon_from_file(comun.ICON)
		#
		vbox = Gtk.VBox()
		self.get_content_area().add(vbox)
		#
		hbox = Gtk.HBox()
		vbox.pack_start(hbox,False,False,0)
		#
		self.entry1 = Gtk.Entry()
		self.entry1.set_width_chars(60)

		self.entry1.set_property('primary_icon_name','edit-find-symbolic')
		self.entry1.set_property('secondary_icon_name','edit-clear-symbolic')
		self.entry1.set_property('primary_icon_tooltip_text',_('Search location'))
		self.entry1.set_property('secondary_icon_tooltip_text',_('Clear location'))
		self.entry1.set_tooltip_text(_('Input the name of your city'))
		self.entry1.connect('icon-press',self.on_icon_press)
		self.entry1.connect('activate',self.on_button1_clicked)
		hbox.pack_start(self.entry1,True,True,0)
		#
		button1 = Gtk.Button(_('Search'))
		button1.connect('clicked',self.on_button1_clicked)	
		hbox.pack_start(button1,False,False,0)
		#
		button2 = Gtk.Button(_('Find me'))
		button2.connect('clicked',self.on_button2_clicked)	
		hbox.pack_start(button2,False,False,0)
		self.expander = Gtk.Expander(label=_('Locations found'))
		self.expander.set_expanded(False)
		vbox.pack_start(self.expander,False,False,0)
		#
		frame = Gtk.Frame()
		self.expander.add(frame)
		self.expander.connect("notify::expanded", self.on_expander_expanded)
		#
		scrolledwindow0 = Gtk.ScrolledWindow()
		scrolledwindow0.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolledwindow0.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
		scrolledwindow0.set_size_request(450,100)
		frame.add(scrolledwindow0)
		# city, county, country, latitude, longitude
		store = Gtk.ListStore(str,str,str,float,float)
		store.set_sort_column_id(2,Gtk.SortType.ASCENDING)
		self.treeview = Gtk.TreeView(model=store)
		self.treeview.set_reorderable(True)
		treeviewcolumn0  =Gtk.TreeViewColumn(_('City'), Gtk.CellRendererText(),text=0)
		treeviewcolumn0.set_reorderable(True)
		treeviewcolumn0.set_sort_column_id(0)
		treeviewcolumn1  =Gtk.TreeViewColumn(_('State'), Gtk.CellRendererText(),text=1)
		treeviewcolumn1.set_reorderable(True)
		treeviewcolumn1.set_sort_column_id(1)
		treeviewcolumn2  =Gtk.TreeViewColumn(_('Country'), Gtk.CellRendererText(),text=2)
		treeviewcolumn2.set_reorderable(True)
		treeviewcolumn2.set_sort_column_id(2)		
		self.treeview.append_column(treeviewcolumn0)
		self.treeview.append_column(treeviewcolumn1)
		self.treeview.append_column(treeviewcolumn2)
		self.treeview.connect('cursor-changed',self.ontreeviewcursorchanged)
		scrolledwindow0.add(self.treeview)
		#
		#
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolledwindow.set_shadow_type(Gtk.ShadowType.IN)
		vbox.pack_start(scrolledwindow,True,True,0)
		#
		self.viewer = WebKit.WebView()
		self.viewer.connect('title-changed', self.title_changed)
		self.viewer.connect('geolocation-policy-decision-requested',self.on_permission_request)
		self.viewer.open('file://' + comun.HTML_WAI)
		#self.viewer.open('/home/atareao/Escritorio/whereami.html')
		scrolledwindow.add(self.viewer)
		scrolledwindow.set_size_request(450,350)
		#
		self.coordinates = None
		self.time = time.time()		
		self.message_queue = queue.Queue()
		#
		self.show_all()
		#
		self.set_wait_cursor()
		while(self.viewer.get_load_status()!=WebKit.LoadStatus.FINISHED):
			wait(1)
		self.search_string = ''
		self.locality = ''
		if latitude and longitude:
			self.search_location(latitude,longitude)
		elif location and len(location)>0:
			self.entry1.set_text(location)
			self.on_button1_clicked(None)
		else:
			#latitude,longitude = ipaddress.get_current_location()
			self.search_location2()
		self.set_normal_cursor()

	def on_expander_expanded(self,widget,selected):
		print(widget,selected)
		if not self.expander.get_expanded():
			self.resize(450, 350)

	def ontreeviewcursorchanged(self,treeview):
		selection = treeview.get_selection()
		if selection is not None:
			model,aiter = treeview.get_selection().get_selected()
			if model is not None and aiter is not None:
				self.entry1.set_text(model[aiter][0])
				self.lat = model[aiter][3]
				self.lng = model[aiter][4]
				self.web_send('center(%s,%s)'%(self.lat,self.lng))
	
	def on_icon_press(self,widget,icon_pos, event):
		if icon_pos == Gtk.EntryIconPosition.PRIMARY:
			self.on_button1_clicked(None)
		elif icon_pos == Gtk.EntryIconPosition.SECONDARY:
			self.entry1.set_text('')
			
	def on_permission_request(self,widget,frame,geolocationpolicydecision):
		WebKit.geolocation_policy_allow(geolocationpolicydecision)
		return True

		
	def on_button2_clicked(self,widget):
		self.set_wait_cursor()
		#latitude,longitude = ipaddress.get_current_location()
		self.set_normal_cursor()
		#self.search_location(latitude,longitude)
		self.search_location2()
		

	def on_button1_clicked(self,widget):
		self.set_wait_cursor()
		search_string = self.entry1.get_text()
		model = self.treeview.get_model()
		model.clear()
		self.expander.set_expanded(True)
		for direction in geocodeapi.get_directions(search_string):
			# city, county, state, country, latitude, longitude
			model.append([direction['city'],direction['state'],direction['country'],direction['lat'],direction['lng']])
		if len(model)>0:
			self.treeview.set_cursor(0)
		self.set_normal_cursor()

	def search_location2(self):
		self.set_wait_cursor()
		self.web_send('findme()')
		self.set_normal_cursor()

	def search_location(self,latitude,longitude):
		self.set_wait_cursor()
		direction = geocodeapi.get_inv_direction(latitude,longitude)
		print(direction)
		if direction is not None:
			self.lat = direction['lat']
			self.lng = direction['lng']
			self.locality = direction['city']
			self.entry1.set_text(direction['city'])
			self.web_send('center(%s,%s)'%(self.lat,self.lng))
		self.set_normal_cursor()
		
	def on_close_application(self,widget):
		self.set_normal_cursor()
		self.hide()

	def get_lat_lon_loc(self):
		return self.lat,self.lng,self.locality

	####################################################################
	##########################ENGINE####################################
	####################################################################
	def inicialize(self):
		self.web_send('mlat=%s;'%(self.lat))
		self.web_send('mlon=%s;'%(self.lon))

	def work(self):
		while Gtk.events_pending():
			Gtk.main_iteration()			
		again = False
		msg = self.web_recv()
		if msg:
			try:
				if msg.startswith('lon='):
					longitude,latitude = msg.split(',')
					longitude = longitude[4:]
					latitude = latitude[4:]
					self.search_location(latitude,longitude)
					print(self.lat,self.lng)
					print(latitude,longitude)
					self.lat = latitude
					self.lng = longitude
					self.web_send('center(%s,%s)'%(self.lat,self.lng))
			except Exception as e:
				msg = None
				print('Error: %s'%e)
			again = True
		if msg == 'exit':
			self.close_application(None)	

	####################################################################
	#########################BROWSER####################################
	####################################################################

	def title_changed(self, widget, frame, title):
		if title != 'null':
			self.message_queue.put(title)
			self.work()

	def web_recv(self):
		if self.message_queue.empty():
			return None
		else:
			msg = self.message_queue.get()
			print('recivied: %s'%(msg))
			return msg

	def web_send(self, msg):
		print('send: %s'%(msg))
		self.viewer.execute_script(msg)

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

