#!/usr/bin/env python
#
# testlib.py - Useful functions for the unit tests
#
# This file is part of Constrict.
#
# Constrict is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Constrict is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Constrict; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Should be imported for testing
import sys

baseDir  = ".."
if baseDir not in sys.path:
    sys.path.insert(0, baseDir)

def someIPAddresses(quantity=500, useInvalid=True):
    """Shuffled IP addresses.  BY DEFAULT INCLUDES INVALID ADDRESSES

    This generator returns tuples of the address, its string represenation,
    and whether it is a valid IP address.
    """
    #
    # Works by making a list for each byte of the IP address.  The list
    # is range(0, quantity).  Then each list is shuffled.  This algorithm
    # guarantees that every byte will be tried if quantity >= 255.  If
    # the "useInvalid" flag is True, then the byte values will go above 255.
    import random, sets

    def makeValid(x):
	return x % 256

    addresses = [None, None, None, None]
    for position in (0, 1, 2, 3):
	addresses[position] = range(0, quantity)
	random.shuffle(addresses[position])
	if useInvalid is False:
	    addresses[position] = map(makeValid, addresses[position])

    address = [None, None, None, None]
    while addresses[0]:
	isValid = True
	for position in (0, 1, 2, 3):
	    value = addresses[position].pop()
	    address[position] = value

	    if value > 255:
		isValid = False

	addressString = "%d.%d.%d.%d" % tuple(address)
	# print "Made", (address, addressString, isValid)
	yield address, addressString, isValid
