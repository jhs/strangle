#!/usr/bin/env python
#
# testlib.py - Useful functions for the unit tests
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

# Should be imported for testing
import sys, os
import random
import glob

baseDir  = glob.glob('../build/lib*')[0]
if not os.path.exists(baseDir):
    sys.stderr.write("Cannot find build directory.  Try running 'setup.py build' first.\n")
    sys.exit(1)

if baseDir not in sys.path:
    sys.path.insert(0, baseDir)

# Random number generator
try:
    rng = file('/dev/urandom', 'r')
except IOError:
    # Need to use our own
    class RNG(object):
	def read(self, size):
	    str = ""
	    for byte in range(0, size):
		str = str + chr(random.randrange(0, 255))
	    return str
    rng = RNG()

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
    import sets

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

# Values taken from ethereal and hex dump
queries   = [
    dict(id = 0xf2eb,
	 flags = dict(ns_f_qr     = 0,	    # query
		      ns_f_opcode = 0,	    # standard query
		      ns_f_aa     = 0,	    # not authoritative
		      ns_f_tc	  = 0,	    # not truncated
		      ns_f_rd     = 1,	    # recursion desired
		      ns_f_ra	  = 0,	    # recursion not available
		      ns_f_z	  = 0,	    # reserved
		      ns_f_ad	  = 0,	    # dnssec authenticated
		      ns_f_cd     = 0,	    # dnssec checking disabled
		      ns_f_rcode  = 0,	    # no error
		      ns_f_max    = 0,
		     ),
	 sections = dict(ns_s_qd = 1,	    # queries
			 ns_s_an = 0,	    # answers
			 ns_s_ns = 0,	    # name server
			 ns_s_ar = 0,	    # additional
			),
	 record = 'a',
	 host = 'www.company.example',
	 data = file(os.path.join('data', 'www.company.example-query')).read(),
	),
    dict(id = 0xb7f8,
	 flags = dict(ns_f_qr     = 0,	    # query
		      ns_f_opcode = 0,	    # standard query
		      ns_f_aa     = 0,	    # not authoritative
		      ns_f_tc	  = 0,	    # not truncated
		      ns_f_rd     = 1,	    # recursion desired
		      ns_f_ra	  = 0,	    # recursion not available
		      ns_f_z	  = 0,	    # reserved
		      ns_f_ad	  = 0,	    # dnssec authenticated
		      ns_f_cd     = 0,	    # dnssec checking disabled
		      ns_f_rcode  = 0,	    # no error
		      ns_f_max    = 0,
		     ),
	 sections = dict(ns_s_qd = 1,	    # queries
			 ns_s_an = 0,	    # answers
			 ns_s_ns = 0,	    # name server
			 ns_s_ar = 0,	    # additional
			),
	 record = 'a',
	 host = 'www.microsoft.com.nsatc.net',
	 data = file(os.path.join('data', 'www.microsoft.com-query')).read(),
	),
    dict(id = 0xb2b9,
	 flags = dict(ns_f_qr     = 0,	    # query
		      ns_f_opcode = 0,	    # standard query
		      ns_f_aa     = 0,	    # not authoritative
		      ns_f_tc	  = 0,	    # not truncated
		      ns_f_rd     = 1,	    # recursion desired
		      ns_f_ra	  = 0,	    # recursion not available
		      ns_f_z	  = 0,	    # reserved
		      ns_f_ad	  = 0,	    # dnssec authenticated
		      ns_f_cd     = 0,	    # dnssec checking disabled
		      ns_f_rcode  = 0,	    # no error
		      ns_f_max    = 0,
		     ),
	 sections = dict(ns_s_qd = 1,	    # queries
			 ns_s_an = 0,	    # answers
			 ns_s_ns = 0,	    # name server
			 ns_s_ar = 0,	    # additional
			),
	 record = 'mx',
	 host = 'oreilly.com',
	 data = file(os.path.join('data', 'oreilly.com-query')).read(),
	),
    ]

responses = [
    dict(id = 0xf2eb,
	 flags = dict(ns_f_qr     = 1,	    # response
		      ns_f_opcode = 0,	    # standard query
		      ns_f_aa     = 1,	    # authoritative
		      ns_f_tc	  = 0,	    # not truncated
		      ns_f_rd     = 1,	    # recursion desired
		      ns_f_ra	  = 1,	    # recursion available
		      ns_f_z	  = 0,	    # reserved
		      ns_f_ad	  = 0,	    # dnssec authenticated
		      ns_f_cd     = 0,	    # dnssec checking disabled
		      ns_f_rcode  = 0,	    # no error
		      ns_f_max    = 0,
		     ),
	 sections = dict(ns_s_qd = 1,	    # queries
			 ns_s_an = 1,	    # answers
			 ns_s_ns = 1,	    # name server
			 ns_s_ar = 1,	    # additional
			),
	 record = 'a',
	 host = 'www.company.example',
	 data = file(os.path.join('data', 'www.company.example-response')).read(),
	),
    dict(id = 0xb7f8,
	 flags = dict(ns_f_qr     = 1,	    # response
		      ns_f_opcode = 0,	    # query
		      ns_f_aa     = 1,	    # authoritative
		      ns_f_tc	  = 0,	    # not truncated
		      ns_f_rd     = 0,	    # recursion desired
		      ns_f_ra	  = 0,	    # recursion not available
		      ns_f_z	  = 0,	    # reserved
		      ns_f_ad	  = 0,	    # dnssec authenticated
		      ns_f_cd     = 0,	    # dnssec checking disabled
		      ns_f_rcode  = 0,	    # no error
		      ns_f_max    = 0,
		     ),
	 sections = dict(ns_s_qd = 1,	    # queries
			 ns_s_an = 1,	    # answers
			 ns_s_ns = 4,	    # name server
			 ns_s_ar = 4,	    # additional
			),
	 record = 'a',
	 host = 'www.microsoft.com.nsatc.net',
	 data = file(os.path.join('data', 'www.microsoft.com-response')).read(),
	),
    dict(id = 0xb2b9,
	 flags = dict(ns_f_qr     = 1,	    # response
		      ns_f_opcode = 0,	    # standard query
		      ns_f_aa     = 1,	    # authoritative
		      ns_f_tc	  = 0,	    # not truncated
		      ns_f_rd     = 1,	    # recursion desired
		      ns_f_ra	  = 1,	    # recursion available
		      ns_f_z	  = 0,	    # reserved
		      ns_f_ad	  = 0,	    # dnssec authenticated
		      ns_f_cd     = 0,	    # dnssec checking disabled
		      ns_f_rcode  = 0,	    # no error
		      ns_f_max    = 0,
		     ),
	 sections = dict(ns_s_qd = 1,	    # queries
			 ns_s_an = 2,	    # answers
			 ns_s_ns = 3,	    # name server
			 ns_s_ar = 5,	    # additional
			),
	 record = 'mx',
	 host = 'oreilly.com',
	 data = file(os.path.join('data', 'oreilly.com-response')).read(),
	),
    ]
