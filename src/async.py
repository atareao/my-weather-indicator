#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# async.py
#
# This file is part of uPodcatcher
#
# Copyright (C) 2014
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
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
    gi.require_version('GLib', '2.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import GLib
import threading
import traceback

__all__ = ['async_function']


def _async_call(f, args, kwargs, on_done):
    def run(data):
        f, args, kwargs, on_done = data
        error = None
        result = None
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            e.traceback = traceback.format_exc()
            error = 'Unhandled exception in asyn call:\n{}'.format(e.traceback)
        GLib.idle_add(lambda: on_done(result, error))

    data = f, args, kwargs, on_done
    thread = threading.Thread(target=run, args=(data,))
    thread.daemon = True
    thread.start()


def async_function(on_done=None):
    '''
    A decorator that can be used on free functions so they will always be
    called asynchronously. The decorated function should not use any resources
    shared by the main thread.

    Example:
    def do_async_stuff(self, input_string):
        def on_async_done(result, error):
            # Do stuff with the result and handle errors in the main thread.
            if error:
                print(error)
            elif result:
                print(result)

        @async_function(on_done=on_async_done)
        def do_expensive_stuff_in_thread(input_string):
            # Pretend to do expensive stuff...
            time.sleep(10)
            stuff = input_string + ' Done in a different thread'
            return stuff

        do_expensive_stuff_in_thread(input_string)
    '''

    def wrapper(f):
        def run(*args, **kwargs):
            _async_call(f, args, kwargs, on_done)
        return run
    return wrapper
