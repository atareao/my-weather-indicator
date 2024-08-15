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

import sys
import threading
import traceback
import gi
try:
    gi.require_version('GLib', '2.0')
except ValueError as value_error_exception:
    print(value_error_exception)
    sys.exit(1)
# pylint: disable=wrong-import-position
from gi.repository import GLib  # type: ignore

__all__ = ['async_function']


def _async_call(f, args, kwargs, on_done):
    """
    Asynchronously calls a function with the given arguments and keyword
    arguments.

    Args:
        f (function): The function to be called asynchronously.
        args (tuple): The positional arguments to be passed to the function.
        kwargs (dict): The keyword arguments to be passed to the function.
        on_done (function): The callback function to be called when the
        asynchronous call is done.
            It takes two arguments: the result of the function call and any
            error that occurred.

    Returns:
        None
    """
    def run(data):
        f, args, kwargs, on_done = data
        error = None
        result = None
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            traces = traceback.format_exc()
            error = f"Unhandled exception in asyn call: {e}\n{traces}"
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
