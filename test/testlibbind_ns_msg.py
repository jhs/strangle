#!/usr/bin/env python
#
# testlibbind_ns_msg.py - Unit tests for the libbind ns_msg wrapper
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

import sys, testutils, random
import unittest

from Strangle import libbind

class ns_msgTestCase(unittest.TestCase):
    """Tests for the wrapper around the libbind ns_msg struct"""

    def test000Exists(self):
	"""Check that the ns_msg type object exists cleanly in the module"""
	assert(libbind.ns_msg.__class__ is type)

    def testInstantiate(self):
	"""Check that the ns_msg type accepts the correct arguments"""

	# Too few
	self.assertRaises(TypeError, libbind.ns_msg)

	# Too many
	self.assertRaises(TypeError, libbind.ns_msg, 'one', 'two')

    def testNoticeInvalid(self):
	"""Test whether the ns_msg type can handle bad data"""
	rng = testutils.rng
	
	for testNum in range(0, 50):
	    packetLength = random.randrange(20, 80)
	    packetVal    = rng.read(packetLength)
	    self.assertRaises(TypeError, libbind.ns_msg, packetVal)
    
    def testParseValidQuery(self):
	"""Test whether ns_msg initialization parses valid NS queries"""
	packetData = file("data/www.company.example-query").read()
	n = libbind.ns_msg(packetData)
	assert(type(n) is libbind.ns_msg)

    def testParseValidResponse(self):
	"""Test whether ns_msg initialization parses valid NS queries"""
	packetData = file("data/www.company.example-response").read()
	n = libbind.ns_msg(packetData)
	assert(type(n) is libbind.ns_msg)

def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite(ns_msgTestCase, 'test') )
    return s

if __name__ == "__main__":
    unittest.main()
