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

import utils as cf
from sun import Sun
from moon import Moon
from datetime import datetime
from datetime import timedelta
import geocodeapi
import locale
import math
import logging

from comun import _
from conditions import WINDS, WINDS2, OMCONDITIONS

logger = logging.getLogger(__name__)


def degToCompass(num):
    val = int((cf.s2f(num) / 11.25) + 0.25)
    arr = [
        'n', 'nbe', 'nne', 'nebn', 'ne', 'nebe', 'ene', 'ebn', 'e', 'ebs',
        'ese', 'sebe', 'se', 'sebs', 'sse', 'sbe', 's', 'sbw', 'ssw', 'swbs',
        'sw', 'swbw', 'wsw', 'wbs', 'w', 'wbn', 'wnw', 'nwbw', 'nw', 'nwbn',
        'nnw', 'nbw'
    ]
    return WINDS[arr[(val % 32)]]


def degToCompass2(num):
    val = int((cf.s2f(num) / 11.25) + 0.25)
    return WINDS2[(val % 32)]


def time_is_lower(time1, time2):
    hora1, minutos1 = time1.split(':')
    hora2, minutos2 = time2.split(':')
    hora1 = int(hora1)
    hora2 = int(hora2)
    minutos1 = int(minutos1)
    minutos2 = int(minutos2)
    if hora1 < hora2:
        return True
    elif hora1 == hora2:
        if minutos1 < minutos2:
            return True
    return False


def time_is_upper(time1, time2):
    hora1, minutos1 = time1.split(':')
    hora2, minutos2 = time2.split(':')
    hora1 = int(hora1)
    hora2 = int(hora2)
    minutos1 = int(minutos1)
    minutos2 = int(minutos2)
    if hora1 > hora2:
        return True
    elif hora1 == hora2:
        if minutos1 > minutos2:
            return True
    return False


def get_condition_om(condition, tipo):
    if condition in OMCONDITIONS.keys():
        return OMCONDITIONS[condition][tipo]
    else:
        logger.error("Condition '{}' not found".format(condition))
        return OMCONDITIONS["NA"][tipo]


def get_condition_wwa(condition, tipo):
    if condition in CONDITIONS.keys():
        return CONDITIONS[condition][tipo]
    return CONDITIONS['not available'][tipo]


def get_condition(condition, tipo):
    # text = ''
    if condition is not None and len(condition) > 0:
        if condition.startswith('heavy'):
            condition = condition[6:]
            # text = _('Heavy') + ' '
        elif condition.startswith('light'):
            condition = condition[6:]
            # text = _('Light') + ' '
        if condition in CONDITIONS.keys():
            return CONDITIONS[condition][tipo]
        else:
            if tipo == 'text':
                return 'Error: %s' % condition
    return CONDITIONS['not available'][tipo]


def get_humidity(text):
    if text is not None and len(text) > 0:
        return text.split(' ')[1].strip()[:-1]
    return ''


def is_day_now(sunrise, sunset, rawOffset):
    now = datetime.time(datetime.utcnow() + timedelta(hours=rawOffset))
    hora = ('%s:%s') % (now.hour, now.minute)
    if time_is_lower(sunset, sunrise):
        # The sunset actually occurs on the next day based on UTC
        if time_is_lower(hora, sunrise) and time_is_upper(hora, sunset):
            return False
    else:
        if time_is_lower(hora, sunrise) or time_is_upper(hora, sunset):
            return False
    return True


def get_moon_icon(day):
    moon = Moon(day)
    return moon.icon()


def get_moon_phase(day):
    moon = Moon(day)
    return moon.phase()


def get_key(key, tree, default=None):
    if key.find('|') > -1:
        ans = tree
        for akey in key.split('|'):
            ans = get_key(akey, ans)
        return ans
    else:
        if key in tree.keys():
            return tree[key]
        return default


def get_dayLength(day, longitude, latitude):
    sun = Sun()
    return sun.dayLength(day.year, day.month, day.day, cf.s2f(longitude),
                         cf.s2f(latitude))


def get_dayCivilTwilightLength(day, longitude, latitude):
    sun = Sun()
    return sun.dayCivilTwilightLength(day.year, day.month, day.day,
                                      cf.s2f(longitude), cf.s2f(latitude))


def get_dawn(day, longitude, latitude, rawOffset):
    sun = Sun()
    ss = sun.civilTwilightLocal(day.year, day.month, day.day,
                                cf.s2f(longitude), cf.s2f(latitude), rawOffset)
    return '%s' % (ss[0])


def get_dusk(day, longitude, latitude, rawOffset):
    sun = Sun()
    ss = sun.civilTwilightLocal(day.year, day.month, day.day,
                                cf.s2f(longitude), cf.s2f(latitude), rawOffset)
    return '%s' % (ss[1])


def get_sunrise(day, longitude, latitude, rawOffset):
    sun = Sun()
    ss = sun.sunRiseSetLocal(day.year, day.month, day.day, cf.s2f(longitude),
                             cf.s2f(latitude), rawOffset)
    return '%s' % (ss[0])


def get_sunset(day, longitude, latitude, rawOffset):
    sun = Sun()
    ss = sun.sunRiseSetLocal(day.year, day.month, day.day, cf.s2f(longitude),
                             cf.s2f(latitude), rawOffset)
    return '%s' % (ss[1])


def change_temperature2(valor, a):
    valor = cf.s2f(valor)
    # initial a in ºF
    if a == 'C':
        valor = 5.0 / 9.0 * (valor - 32.0)
    elif a == 'K':
        valor = 5.0 / 9.0 * (valor - 32.0) + 273.15
        return '{0} {1}'.format(cf.redondea_digits(valor), a)
    return '{0} {1:c}{2}'.format(cf.redondea_digits(valor), 176, a)


def get_wind_chill(temperature, wind_velocity):
    wind_velocity = cf.s2f(wind_velocity)
    temperature = cf.s2f(temperature)
    # temperature ºF
    # wind_velocity mph
    if temperature <= 50.0 and wind_velocity >= 3.0:
        wc = 35.74 + 0.6215 * temperature - 35.76 *\
            math.pow(wind_velocity, 0.16) + 0.4275 * temperature *\
            math.pow(wind_velocity, 0.16)
        return wc - temperature
    return 0.0


def get_wind_icon(wind_direction):
    wind_direction = wind_direction.upper()
    for element in WINDS2:
        if wind_direction == element[0]:
            return element[2]
    return WINDS2[0][2]


def get_wind_condition(wind_velocity, wind_direction, wind_units):
    wind_velocity = cf.s2f(wind_velocity)
    wind_direction = wind_direction.lower()
    if wind_direction in WINDS.keys():
        wind_direction = WINDS[wind_direction]
    wind_velocity = change_velocity(wind_velocity, wind_units)
    if wind_units == 'Beaufort':
        return wind_velocity + ' ' + _('from') + ' ' + wind_direction
    else:
        return _('from') + ' ' + wind_direction + ' ' + _(
            'at') + ' ' + wind_velocity


def get_wind_condition2(wind_velocity, wind_direction, wind_units):
    wind_velocity = change_velocity(cf.s2f(wind_velocity), wind_units)
    return '%s (%s)' % (wind_velocity, wind_direction)


def get_feels_like(temperature, humidity, wind_velocity, temperature_units):
    # temperature ºF
    # velocity mph
    temperature = cf.s2f(temperature)
    humidity = cf.s2f(humidity)
    wind_velocity = cf.s2f(wind_velocity)
    hi = get_heat_index(temperature, humidity)
    wc = get_wind_chill(temperature, wind_velocity)
    ta = temperature + hi + wc
    return cf.change_temperature(ta, temperature_units)


def get_dew_point(humidity, temperature, temperature_units):
    # humidity (%)
    # temperature (ºF)
    if humidity and temperature and humidity > 0.0:
        h = cf.s2f(humidity)
        t = cf.s2f(temperature)
        t = 5.0 / 9.0 * (t - 32.0)
        dp = math.pow(h / 100.0, 1.0 / 8.0) * (110.0 + t) - 110.0
        dp = cf.redondea_digits(9.0 / 5.0 * dp + 32)
        return cf.change_temperature(dp, temperature_units)
    return _('n/a')


def get_heat_index(temperature, humidity):
    temperature = cf.s2f(temperature)
    humidity = cf.s2f(humidity)
    if humidity > 0.0 and temperature >= 77.0:
        # temperature ºF
        # humidity over 100
        c1 = -42.379
        c2 = 2.04901523
        c3 = 10.14333127
        c4 = -0.22475541
        c5 = -0.00683783
        c6 = -0.05481717
        c7 = 0.00122874
        c8 = 0.00085282
        c9 = -0.00000199
        hi = c1 + c2 * temperature + c3 * humidity + c4 * temperature *\
            humidity + c5 * math.pow(temperature, 2.0) + c6 *\
            math.pow(humidity, 2.0) + c7 * math.pow(temperature, 2.0) *\
            humidity + c8 * temperature * math.pow(humidity, 2.0) + c9 *\
            math.pow(temperature, 2.0) * math.pow(humidity, 2.0)
        return hi - temperature
    return 0


def change_pressure(valor, a):
    valor = cf.s2f(valor)
    units_u = {'mb': 1, 'in': 0.0294985250737, 'mm': 0.751879699248}
    units_m = {
        'mb': _('millibar'),
        'in': _('inches of mercury'),
        'mm': _('millimeters of mercury')
    }
    if a in units_u.keys():
        if a == 'in':
            digits = 1
        else:
            digits = 0
        return '%s %s' % (locale.str(
            cf.redondea_digits(valor * units_u[a], digits)), units_m[a])


def change_distance(valor, a):
    valor = cf.s2f(valor)
    units_u = {'mi': 1, 'km': 1.609344}
    units_m = {'mi': _('mi'), 'km': _('km')}
    if a in units_u.keys():
        return '%s %s' % (locale.str(cf.redondea_digits(
            valor * units_u[a])), units_m[a])


def change_longitude(valor, a):
    valor = cf.s2f(valor)
    units_u = {'in': 1, 'cm': 2.54, 'mm': 25.4}
    units_m = {'in': _('in'), 'cm': _('cm'), 'mm': _('mm')}
    if a in units_u.keys():
        return '%s %s' % (locale.str(cf.redondea_digits(
            valor * units_u[a])), units_m[a])

def change_velocity(valor, a):
    valor = cf.s2f(valor)
    # initial a in mph
    units_u = {
        'mph': 1,
        'km/h': 1.609344,
        'm/s': 0.44704,
        'knots': 0.868976,
        'ft/s': 1.466667
    }
    units_m = {
        'mph': _('mph'),
        'km/h': _('km/h'),
        'm/s': _('m/s'),
        'knots': _('knots'),
        'ft/s': _('ft/s')
    }
    if a in units_u.keys():
        return '%s %s' % (locale.str(cf.redondea_digits(
            valor * units_u[a])), units_m[a])
    if a == 'Beaufort':
        if valor <= 1:
            return "0 - " + _('Calm')
        elif valor <= 3:
            return "1 - " + _('Light air')
        elif valor <= 7:
            return "2 - " + _('Light breeze')
        elif valor <= 12:
            return "3 - " + _('Gentle breeze')
        elif valor <= 18:
            return "4 - " + _('Moderate breeze')
        elif valor <= 24:
            return "5 - " + _('Fresh breeze')
        elif valor <= 31:
            return "6 - " + _('Strong breeze')
        elif valor <= 38:
            return "7 - " + _('High wind')
        elif valor <= 46:
            return "8 - " + _('Gale')
        elif valor <= 54:
            return "9 - " + _('Strong gale')
        elif valor <= 63:
            return "10 - " + _('Storm')
        elif valor <= 72:
            return "11 - " + _('Violent storm')
        elif valor > 72:
            return "12 - " + _('Hurricane')
    return ''


def timeformat(hhmm, AMPM=False):
    """
    This method converts time in 24h format to 12h format
    Example:   "00:32" is "12:32 AM"
    "13:33" is "01:33 PM"
    """

    hh, mm = hhmm.split(":")
    if cf.s2f(mm) == 60.0:
        hh = str(int(cf.s2f(hh) + 1.0))
        hhmm = hh + ':00'
    if AMPM:
        ampm = hhmm.split(":")
        if (len(ampm) == 0) or (len(ampm) > 3):
            return hhmm
        # is AM? from [00:00, 12:00[
        hour = int(ampm[0]) % 24
        isam = (hour >= 0) and (hour < 12)
        # 00:32 should be 12:32 AM not 00:32
        if isam:
            ampm[0] = ('12' if (hour == 0) else "%02d" % (hour))
        else:
            ampm[0] = ('12' if (hour == 12) else "%02d" % (hour - 12))
        return ': '.join(ampm) + (' AM' if isam else ' PM')
    else:
        return hhmm


class Units(object):

    def __init__(self,
                 temperature='C',
                 wind='km/h',
                 pressure='mb',
                 visibility='km',
                 snow='cm',
                 rain='mm',
                 ampm=False):
        self.temperature = temperature
        self.wind = wind
        self.pressure = pressure
        self.visibility = visibility
        self.snow = snow
        self.rain = rain
        self.ampm = ampm


class WeatherService(object):

    def __init__(self,
                 longitude=-0.418,
                 latitude=39.360,
                 location="Silla",
                 timezone="Europe/Madrid",
                 units=Units()):
        if not longitude:
            longitude = 0
        if not latitude:
            latitude = 0
        self._longitude = longitude
        self._latitude = latitude
        self._timezone = timezone
        self._location = location
        self._units = units

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        self._timezone = value

    def get_default_values(self):
        current_conditions = {}
        current_conditions['rawOffset'] =\
            geocodeapi.get_rawOffset(self._timezone)
        current_conditions['condition_text'] = _('Not available')
        current_conditions['condition_image'] = 'mwig-not-available.png'
        current_conditions['condition_icon_dark'] = 'mwid-not-available.png'
        current_conditions['condition_icon_light'] = 'mwil-not-available.png'
        current_conditions['temperature'] = _('N/A')
        current_conditions['pressure'] = _('N/A')
        current_conditions['humidity'] = _('N/A')
        current_conditions['dew_point'] = _('N/A')
        current_conditions['wind_condition'] = _('N/A')
        current_conditions['wind_icon'] = None
        #
        current_conditions['heat_index'] = _('N/A')
        current_conditions['windchill'] = _('N/A')
        #
        current_conditions['feels_like'] = _('N/A')
        #
        current_conditions['visibility'] = _('N/A')
        current_conditions['cloudiness'] = _('N/A')
        current_conditions['solarradiation'] = _('N/A')
        current_conditions['UV'] = _('N/A')
        current_conditions['precip_1hr'] = _('N/A')
        current_conditions['precip_today'] = _('N/A')
        #
        dayLength = get_dayLength(datetime.today(), self._longitude,
                                  self._latitude)
        dayCivilTwilightLength = get_dayCivilTwilightLength(
            datetime.today(), self._longitude, self._latitude)
        if dayLength == 0.0:
            current_conditions['sunrise_time'] = _('Down all day')
            current_conditions['sunset_time'] = _('Down all day')
            current_conditions['sunrise'] = _('Down all day')
            current_conditions['sunset'] = _('Down all day')
            current_conditions['isday'] = False
        elif dayLength == 24.0:
            current_conditions['sunrise_time'] = _('Up all day')
            current_conditions['sunset_time'] = _('Up all day')
            current_conditions['sunrise'] = _('Up all day')
            current_conditions['sunset'] = _('Up all day')
            current_conditions['isday'] = True
        else:
            current_conditions['sunrise_time'] = get_sunrise(
                datetime.today(), self._longitude, self._latitude,
                current_conditions['rawOffset'])
            current_conditions['sunset_time'] = get_sunset(
                datetime.today(), self._longitude, self._latitude,
                current_conditions['rawOffset'])
            current_conditions['isday'] = is_day_now(
                current_conditions['sunrise_time'],
                current_conditions['sunset_time'],
                current_conditions['rawOffset'])
            current_conditions['sunrise'] = timeformat(
                current_conditions['sunrise_time'], self._units.ampm)
            current_conditions['sunset'] = timeformat(
                current_conditions['sunset_time'], self._units.ampm)
        current_conditions['sunrise_time_utc'] = get_sunrise(
            datetime.today(), self._longitude, self._latitude, 0)
        current_conditions['sunset_time_utc'] = get_sunset(
            datetime.today(), self._longitude, self._latitude, 0)
        if dayCivilTwilightLength == 0.0:
            current_conditions['dawn_time'] = _('Down all day')
            current_conditions['dusk_time'] = _('Down all day')
            current_conditions['dawn'] = _('Down all day')
            current_conditions['dusk'] = _('Down all day')
        elif dayLength == 24.0:
            current_conditions['dawn_time'] = _('Up all day')
            current_conditions['dusk_time'] = _('Up all day')
            current_conditions['dawn'] = _('Up all day')
            current_conditions['dusk'] = _('Up all day')
        else:
            current_conditions['dawn_time'] = get_dawn(
                datetime.today(), self._longitude, self._latitude,
                current_conditions['rawOffset'])
            current_conditions['dusk_time'] = get_dusk(
                datetime.today(), self._longitude, self._latitude,
                current_conditions['rawOffset'])
            current_conditions['dawn'] = timeformat(
                current_conditions['dawn_time'], self._units.ampm)
            current_conditions['dusk'] = timeformat(
                current_conditions['dusk_time'], self._units.ampm)
        current_conditions['moon_icon'] = get_moon_icon(datetime.today())
        current_conditions['moon_phase'] = get_moon_phase(datetime.today())
        dayLength = get_dayLength(datetime.today(), self._longitude,
                                  self._latitude)
        dayCivilTwilightLength = get_dayCivilTwilightLength(
            datetime.today(), self._longitude, self._latitude)
        if current_conditions['sunrise_time'] ==\
                current_conditions['sunset_time']:
            if dayLength > 0:
                current_conditions['sunrise_time'] = _('Up all day')
                current_conditions['sunset_time'] = _('Up all day')
            else:
                current_conditions['sunrise_time'] = _('Down all day')
                current_conditions['sunset_time'] = _('Down all day')
        if current_conditions['dawn_time'] == current_conditions['dusk_time']:
            if dayCivilTwilightLength > 0:
                current_conditions['dawn_time'] = _('Up all day')
                current_conditions['dusk_time'] = _('Up all day')
            else:
                current_conditions['dawn_time'] = _('Down all day')
                current_conditions['dusk_time'] = _('Down all day')

        #
        forecast_conditions = []
        dia = datetime.today()
        undia = timedelta(days=1)
        i = 0
        while i < 7:
            i += 1
            fc = {}
            fc['day_of_week'] = dia.strftime('%A').capitalize()
            fc['low'] = _('N/A')
            fc['high'] = _('N/A')
            fc['cloudiness'] = _('N/A')
            #
            fc['qpf_allday'] = _('N/A')
            fc['qpf_day'] = _('N/A')
            fc['qpf_night'] = _('N/A')
            fc['snow_allday'] = _('N/A')
            fc['snow_day'] = _('N/A')
            fc['snow_night'] = _('N/A')
            fc['maxwind'] = _('N/A')
            fc['avewind'] = _('N/A')
            fc['wind_icon'] = None
            fc['avehumidity'] = _('N/A')
            fc['maxhumidity'] = _('N/A')
            fc['minhumidity'] = _('N/A')
            #
            fc['condition'] = _('N/A')
            fc['condition_text'] = _('N/A')
            fc['condition_image'] = 'mwig-not-available.png'
            fc['condition_icon'] = 'mwil-not-available.png'
            dayLength = get_dayLength(datetime.today(), self._longitude,
                                      self._latitude)
            if dayLength == 0.0:
                fc['sunrise'] = _('Down all day')
                fc['sunset'] = _('Down all day')
            elif dayLength == 24.0:
                fc['sunrise'] = _('Up all day')
                fc['sunset'] = _('Up all day')
            else:
                fc['sunrise'] = timeformat(
                    get_sunrise(dia, self._longitude, self._latitude,
                                current_conditions['rawOffset']),
                    self._units.ampm)
                fc['sunset'] = timeformat(
                    get_sunset(dia, self._longitude, self._latitude,
                               current_conditions['rawOffset']),
                    self._units.ampm)
            fc['moon_icon'] = get_moon_icon(dia)
            fc['moon_phase'] = get_moon_phase(dia)
            forecast_conditions.append(fc)
            dia = dia + undia
        #
        forecast_information = {}
        forecast_information['city'] = '...'
        forecast_information['postal_code'] = ''
        forecast_information['latitude_e6'] = ''
        forecast_information['longitude_e6'] = ''
        forecast_information['forecast_date'] = ''
        forecast_information['current_date_time'] = ''
        forecast_information['unit_system'] = 'SI'
        #
        weather_data = {}
        weather_data['update_time'] = 0
        weather_data['ok'] = False
        weather_data['current_conditions'] = current_conditions
        weather_data['forecasts'] = forecast_conditions
        weather_data['forecast_information'] = forecast_information
        return weather_data

    def get_weather(self):
        pass


if __name__ == '__main__':
    print(get_condition('light rain', 'image'))
    print(get_condition('heavy rain', 'text'))
    print(degToCompass(9))
    print('Esta es la temperatura ' + cf.change_temperature(20, 'C'))
