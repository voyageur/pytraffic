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

hint_enabled=0
import os,sys,string

def version_suffix():
	if os.name=='nt':
		return string.replace(sys.version[:3],'.','')
	else:
		return ''

if os.name=='nt' or os.name=='posix':
    try:
	print "Trying build binary..."
	import _hint
	hint_enabled=1
    except ImportError,e:
        _last_error=str(e)
	try:
		print "Trying included binary..."
	        _hint=__import__("python"+version_suffix()+"._hint",
			locals(),
			globals(),
			'_hint')
	        hint_enabled=1
	except ImportError,e:
		_last_error=str(e)
		pass
else:
    print "The hint feature only works on Windows and Unix."

if hint_enabled:
    _hint.init()

def bestmove(packedboard):
    rows,cols=packedboard
    _hint.bestmove(rows,cols)
    return (_hint.getbestmoverows(),
            _hint.getbestmovecolumns())


def findlevel(start,end):
	_hint.findlevel(start,end)
	return (_hint.getbestyoucando(),
                _hint.getpackedrows(),
                _hint.getpackedcolumns())

def last_error():
	return _last_error






