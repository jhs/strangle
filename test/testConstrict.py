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

	self.msgFileName = "data/oreilly.com-response"

    def testNoticeInvalid(self):
	"""Test whether the DNSMessage parser can handle bad data"""
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

class testDNSFlags(unittest.TestCase):
    """Tests all interfaces to the DNSFlags object"""
    def setUp(self):
	self.queries   = testutils.queries
	self.responses = testutils.responses

	self.msgFileName = "data/oreilly.com-response"

    def testDetectsBadType(self):
	"""Test that DNSFlags insists on receiving a ns_msg argument"""
	self.assertRaises(Constrict.ConstrictError, Constrict.DNSFlags, 'foo')
	self.assertRaises(Constrict.ConstrictError, Constrict.DNSFlags, 23)

	dataFile = file(self.msgFileName)
	self.assertRaises(Constrict.ConstrictError, Constrict.DNSFlags, dataFile)

	data = dataFile.read()
	self.assertRaises(Constrict.ConstrictError, Constrict.DNSFlags, data)

    def testDetectsQR(self):
	"""Test whether DNSFlags detects whether the message is a query or response"""
	for message in self.queries:
	    messageText = message['data']
	    msg = Constrict.DNSMessage(messageText)
	    self.assertEquals(msg.flags.type, 'query')
	for message in self.responses:
	    messageText = message['data']
	    msg = Constrict.DNSMessage(messageText)
	    self.assertEquals(msg.flags.type, 'response')
    
    def testGetsOpcode(self):
	"""Test whether DNSFlags determines the proper opcodes"""
	for message in self.queries + self.responses:
	    msg = Constrict.DNSMessage(message['data'])
	    self.assertEquals(msg.flags.opcode, message['flags']['ns_f_opcode'])

    def testGetsAuthor(self):
	"""Test whether DNSFlags determines whether the message is authoritative"""
	for message in self.queries + self.responses:
	    msg = Constrict.DNSMessage(message['data'])
	    self.assertEquals(msg.flags.authoritative, message['flags']['ns_f_aa'])
	
    def testGetsTrunc(self):
	"""Test whether DNSFlags determines whether the message is truncated"""
	for message in self.queries + self.responses:
	    msg = Constrict.DNSMessage(message['data'])
	    self.assertEquals(msg.flags.truncated, message['flags']['ns_f_tc'])
	
    def testGetsRD(self):
	"""Test whether DNSFlags determines whether recursion is desired"""
	for message in self.queries + self.responses:
	    msg = Constrict.DNSMessage(message['data'])
	    self.assertEquals(msg.flags.recursionDesired, message['flags']['ns_f_rd'])
	
    def testGetsRA(self):
	"""Test whether DNSFlags determines whether recursion is available"""
	for message in self.queries + self.responses:
	    msg = Constrict.DNSMessage(message['data'])
	    self.assertEquals(msg.flags.recursionAvailable, message['flags']['ns_f_ra'])
	
    def testGetsResponse(self):
	"""Test whether DNSFlags determines the correct response code"""
	for message in self.queries + self.responses:
	    msg = Constrict.DNSMessage(message['data'])
	    self.assertEquals(msg.flags.response, message['flags']['ns_f_rcode'])

class testDNSRecord(unittest.TestCase):
    """Tests all interfaces to the DNSsection object"""
    def setUp(self):
	from Constrict import libbind

	self.queries   = testutils.queries
	self.responses = testutils.responses

	self.msgFileName = "data/www.microsoft.com-response"
	self.msg         = libbind.ns_msg( file(self.msgFileName).read() )

    def testDetectsBadType(self):
	"""Test that DNSSection insists on receiving proper arguments"""
	self.assertRaises(TypeError, Constrict.DNSRecord, 'too few arguments')
	self.assertRaises(TypeError, Constrict.DNSRecord, 'also not', 'enough')
	self.assertRaises(TypeError, Constrict.DNSRecord, "now", "there's", "too", "many")

	self.assertRaises(Constrict.DNSRecordError, Constrict.DNSRecord, "the", "wrong", "type")

	rec = Constrict.DNSRecord(self.msg, 'query', 0)
	assert(type(rec) is Constrict.DNSRecord)

def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite(testDNSMessage, 'test') )
    s.addTest( unittest.makeSuite(testDNSFlags  , 'test') )
    s.addTest( unittest.makeSuite(testDNSRecord , 'test') )
    return s

if __name__ == "__main__":
    unittest.main()
