#!/usr/bin/env python
#
# testConstrict.py - Unit tests for the objects in the Constrict module
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

import sys, testutils
import unittest

import Constrict

# All tests will be in here since it's not an object-oriented interface
class testDNSMessage(unittest.TestCase):
    """Tests all interfaces to the DNSMessage object"""
    def setUp(self):
	self.queries   = testutils.queries
	self.responses = testutils.responses

	self.msgFileName = "data/oreilly.com-respones"

    def testNoticeInvalid(self):
	"""Test whether the ns_msg type can handle bad data"""
	from Constrict import DNSMessage, ConstrictError
	import random

	rng = testutils.rng
	
	for testNum in range(0, 50):
	    packetLength = random.randrange(20, 80)
	    packetVal    = rng.read(packetLength)
	    self.assertRaises(ConstrictError, DNSMessage, packetVal)
    
    def testParseFromString(self):
	"""Test whether DNSMessage can initialize from a passed string"""
	packetData = file("data/www.company.example-query").read()
	msg = Constrict.DNSMessage(packetData)
	assert(type(msg) is Constrict.DNSMessage)
	
    def testParseFromFile(self):
	"""Test whether DNSMessage can initialize from a file-like object"""
	packetSource = file("data/www.microsoft.com-response")
	msg = Constrict.DNSMessage(packetSource)
	assert(type(msg) is Constrict.DNSMessage)

    def testParseValidQuery(self):
	"""Test whether DNSMessage initialization parses valid NS queries"""
	packetData = file("data/www.company.example-query").read()
	msg = Constrict.DNSMessage(packetData)
	assert(type(msg) is Constrict.DNSMessage)

    def testParseValidResponse(self):
	"""Test whether DNSMessage initialization parses valid NS queries"""
	packetData = file("data/www.company.example-response").read()
	n = Constrict.DNSMessage(packetData)
	assert(type(n) is Constrict.DNSMessage)

    def testID(self):
	"""Test whether DNSMessage has a proper ID attribute"""
	for message in self.queries + self.responses:
	    msg = Constrict.DNSMessage(message['data'])
	    self.assertEquals(msg.id, message['id'])

def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite(testDNSMessage, 'test') )
    return s

if __name__ == "__main__":
    unittest.main()
