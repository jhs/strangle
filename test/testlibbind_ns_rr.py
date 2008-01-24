#!/usr/bin/env python
#
# testlibbind_ns_rr.py - Unit tests for the libbind ns_rr wrapper
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

import sys, testutils
import unittest

from Strangle import libbind

class ns_rrTestCase(unittest.TestCase):
    """Tests for the wrapper around the libbind ns_rr struct"""

    def setUp(self):
	self.packetData = file("data/oreilly.com-response").read()
	self.msg = libbind.ns_msg(self.packetData)

    def test000Exists(self):
	"""Check that the ns_rr type object exists cleanly in the module"""
	assert(libbind.ns_rr.__class__ is type)

    def testInstantiate(self):
	"""Check that the ns_rr type accepts the correct arguments"""

	# Too few
	self.assertRaises(TypeError, libbind.ns_rr)
	self.assertRaises(TypeError, libbind.ns_rr, 'one')
	self.assertRaises(TypeError, libbind.ns_rr, 'one', 'two')

	# Too many
	self.assertRaises(TypeError, libbind.ns_rr, 'one', 'two', 'three', 'four')

	# Not a libbind.ns_msg object
	self.assertRaises(TypeError, libbind.ns_rr, 'one', 'two', 'three')

	# Not two integers
	self.assertRaises(TypeError, libbind.ns_rr, self.msg, 'not an int', 'not an int')
	self.assertRaises(TypeError, libbind.ns_rr, self.msg, libbind.ns_s_ns, 'not an int')

    def testNoticeInvalid(self):
	"""Test whether the ns_rr type can handle bad data"""
	self.assertRaises(TypeError, libbind.ns_rr, self.msg, libbind.ns_s_ns, 100)

    def testParseValidMessage(self):
	"""Test whether ns_rr initialization parses valid NS messages"""
	rr = libbind.ns_rr(self.msg, libbind.ns_s_qd, 0)
	assert(type(rr) is libbind.ns_rr)

def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite(ns_rrTestCase, 'test') )
    return s

if __name__ == "__main__":
    unittest.main()
