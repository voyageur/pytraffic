## PyTraffic -- A python simulation of the game Rush Hour invented by
## Nob Yoshigahara and commercialized by Binary Arts Corporation.
##
## Copyright (C) 2001-2005 Michel Van den Bergh <michel.vandenbergh@uhasselt.be>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING.
## If not, write to the Free Software Foundation, Inc.,
## 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
##

import os
import sys
import os.path
import Misc
import urllib.parse
import string

np=Misc.normalize_path


def sanitize(file_name):
	return string.replace(file_name,' ',r'\ ')

def sanitize_url(url):
	return string.replace(url,' ','%20')

def which_python(program):
	if os.path.exists(program):
		return 1
	path=string.split(os.environ['PATH'],":")
	for dir in path:
		abs_path=os.path.join(dir,program)
		if os.path.exists(abs_path):
			return 1
	return 0

def program_present(program):
    if os.name=='posix':
 	return which_python(program)
    else:
        return 0

def showhtml_program(program,file,terminal=0):
    program=sanitize(program)
    url=sanitize_url('file://'+os.path.abspath(np(file)))
    if not terminal:
	os.system(program+" "+url+' &')
    else:
	os.system('xterm -sb -e '+program+" "+url+' &')

def showhtml_nt(file):
    sanitized_url=sanitize_url("file://"+os.path.abspath(np(file)))
    url="file://"+os.path.abspath(np(file))
    if sys.version[:3]>='2.0':
       print("Starting " + url)
       os.startfile(url)
    else:
	os.system("start "+sanitized_url)

def showhtml_dummy(file):
    pass

def init_showhtml():
    global showhtml, _can_display_html, _last_error

    _can_display_html=1
    _last_error=''

    if os.name=="nt":
        showhtml=showhtml_nt
    elif Misc.isCygwin():
	if program_present('lynx'):	
		showhtml=lambda file:showhtml_program('lynx',file,1)
	else:
	        _can_display_html=0
	        _last_error="Please install lynx. Other browsers are broken\
on Cygwin. Sorry."
    elif program_present('xdg-open'):
            showhtml=lambda file:showhtml_program('xdg-open',file)
    else:
        _can_display_html=0
        _last_error="Please install xdg-utils"


def can_display_html():
    return _can_display_html

def last_error():
    return _last_error


init_showhtml()
