#!/usr/bin/env python
#
# print.py - Print out a packet
#
# This file is part of Strangle.
#
# Strangle is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Strangle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Strangle; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os, sys

sys.path.insert(0, '.')
sys.path.append('..')
from Strangle import *

fileName = 'oreilly.com-response'
if os.path.isfile(os.path.join('data', fileName)):
    f = file(os.path.join('data', fileName))
elif os.path.isfile(os.path.join('test', 'data', fileName)):
    f = file(os.path.join('test', 'data', fileName))
else:
    print "Cannot find data file"
    os.exit(1)

msg = DNSMessage(f)
print msg
