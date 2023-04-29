#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
'''
moonphase.py - Calculate Lunar Phase
Author: Sean B. Palmer, inamidst.com
Cf. http://en.wikipedia.org/wiki/Lunar_phase#Lunar_phase_calculation
'''

import math
import decimal
import datetime
from comun import _
import logging

logger = logging.getLogger(__name__)


dec = decimal.Decimal


class Moon(object):
    def __init__(self, date):
        self._date = date

    def position(self):
        diff = self._date - datetime.datetime(2001, 1, 1)
        days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
        lunations = dec('0.20439731') + (days * dec('0.03386319269'))
        return lunations % dec(1)

    def phase(self):
        pos = self.position()
        index = (pos * dec(8)) + dec('0.5')
        index = math.floor(index)
        return {
            0: _('New Moon'),
            1: _('Waxing Crescent'),
            2: _('First Quarter'),
            3: _('Waxing Gibbous'),
            4: _('Full Moon'),
            5: _('Waning Gibbous'),
            6: _('Last Quarter'),
            7: _('Waning Crescent')
        }[int(index) & 7]

    def phase_int(self):
        pos = self.position()
        index = (pos * dec(8)) + dec('0.5')
        index = math.floor(index)
        return int(index) & 7

    def icon(self):
        pos = self.position()
        index = (pos * dec(28)) + dec('0.5')
        index = int(math.floor(index))
        index = str(index)
        if len(index) < 2:
            index = '0' + index
        value = "mwi-moon{}.png".format(index)
        logger.debug("Moon: {} => {}".format(index, value))
        return value

    def image(self):
        pos = self.position()
        index = (pos * dec(28)) + dec('0.5')
        index = int(math.floor(index))
        index = str(index)
        if len(index) < 2:
            index = '0' + index
        return 'mwi-moon' + index + '.svg'


if __name__ == '__main__':
    y = 2030
    m = 3
    days = 31
    for i in range(1, days):
        moon = Moon(datetime.datetime(y, m, i))
        phasename = moon.phase()
        roundedpos = round(float(moon.position()), 3)
        icon = moon.icon()
        logger.info("dia {} -> {} ({}): {}".format(
            i, phasename, roundedpos, icon))
    exit(0)
