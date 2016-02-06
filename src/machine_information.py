#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Report Ubuntu and Machine information
# Adding keybiding
#
# Copyright (C) 2010 Lorenzo Carbonell
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

import platform
	
def get_information():
	information = '#####################################################\n'
	information += ('System: %s\n')%(platform.system())
	information += ('Machine: %s\n')%(platform.machine())
	information += ('Node: %s\n')%(platform.node())
	information += ('Release: %s\n')%(platform.release())
	information += ('Version: %s\n')%(platform.version())
	information += ('Platform: %s\n')%(platform.platform())
	information += '#####################################################\n'
	return information

	
if __name__=='__main__':
	print(get_information())
	exit(0)
