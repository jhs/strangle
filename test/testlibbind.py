#!/usr/bin/env python
#
# testlibbind.py - Unit tests for the libbind functions
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

# All tests will be in here since it's not an object-oriented interface
class libbindTestCase(unittest.TestCase):
    """Tests all useful functions in libbind"""
    def setUp(self):
	import os, re

	self.queries = testutils.queries
	self.responses = testutils.responses

	self.packetData = file("data/oreilly.com-response").read()
	self.msg = libbind.ns_msg(self.packetData)

	self.flags = ['qr', 'opcode', 'aa', 'tc', 'rd', 'ra', 'z', 'ad', 'cd', 'rcode', 'max']
	self.flags = map(lambda str: 'ns_f_' + str, self.flags)

	self.sections = ['qd', 'an', 'ns', 'ar']
	self.sections = map(lambda str: 'ns_s_' + str, self.sections)

    def testlibbindHasEnums(self):
	"""Test whether libbind correctly defines all libbind enums"""
	for flag in self.flags:
	    assert(getattr(libbind, flag, None) is not None)
	
	for section in self.sections:
	    assert(getattr(libbind, section, None) is not None)
	
    def testlibbind_ns_msg_getflagArgs(self):
	"""Test whether ns_msg_getflags accepts the proper arguments"""
	self.assertRaises(TypeError, libbind.ns_msg_getflag)

	msg = libbind.ns_msg(self.queries[0]['data'])
	self.assertRaises(TypeError, libbind.ns_msg_getflag, msg)

	self.assertRaises(TypeError, libbind.ns_msg_getflag, msg, 'not an int')

    def testlibbind_ns_msg_getflag(self):
	"""Test whether libbind correctly returns the message flags"""
	for message in self.queries + self.responses:
	    msg = libbind.ns_msg(message['data'])
	    for flag in self.flags:
		flagVal = getattr(libbind, flag)
		self.assertEquals(libbind.ns_msg_getflag(msg, flagVal), message['flags'][flag])

    def testlibbind_ns_msg_countArgs(self):
	"""Test whether ns_msg_count accepts the proper arguments"""
	self.assertRaises(TypeError, libbind.ns_msg_count)

	msg = libbind.ns_msg(self.queries[0]['data'])
	self.assertRaises(TypeError, libbind.ns_msg_count, msg)

	self.assertRaises(TypeError, libbind.ns_msg_count, msg, 'not an int')

    def testlibbind_ns_msg_count(self):
	"""Test whether ns_msg_count correctly returns the section counts"""
	for message in self.queries + self.responses:
	    msg = libbind.ns_msg(message['data'])
	    for section in self.sections:
		sectionVal = getattr(libbind, section)
		self.assertEquals(libbind.ns_msg_count(msg, sectionVal), message['sections'][section])

    def testlibbind_ns_rr(self):
	"""Test whether ns_rr_name returns the correct name"""

	# Query
	rr = libbind.ns_rr(self.msg, libbind.ns_s_qd, 0)
	assert(libbind.ns_rr_name(rr) == 'oreilly.com')

	# Answer
	rr = libbind.ns_rr(self.msg, libbind.ns_s_an, 0)
	assert(libbind.ns_rr_name(rr) == 'oreilly.com')
	rr = libbind.ns_rr(self.msg, libbind.ns_s_an, 1)
	assert(libbind.ns_rr_name(rr) == 'oreilly.com')

	# Name servers
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 0)
	assert(libbind.ns_rr_name(rr) == 'oreilly.com')
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 1)
	assert(libbind.ns_rr_name(rr) == 'oreilly.com')
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 2)
	assert(libbind.ns_rr_name(rr) == 'oreilly.com')

	# Additional
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 0)
	assert(libbind.ns_rr_name(rr) == 'smtp1.oreilly.com')
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 1)
	assert(libbind.ns_rr_name(rr) == 'smtp2.oreilly.com')
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 2)
	assert(libbind.ns_rr_name(rr) == 'ns.oreilly.com')
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 3)
	assert(libbind.ns_rr_name(rr) == 'ns1.sonic.net')
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 4)
	assert(libbind.ns_rr_name(rr) == 'ns2.sonic.net')

    def testlibbind_ns_rr_type(self):
	"""Test whether ns_rr_type returns the correct type"""

	# Query
	rr = libbind.ns_rr(self.msg, libbind.ns_s_qd, 0)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_mx)

	# Answer
	rr = libbind.ns_rr(self.msg, libbind.ns_s_an, 0)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_mx)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_an, 1)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_mx)

	# Name servers
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 0)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_ns)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 1)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_ns)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 2)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_ns)

	# Additional
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 0)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_a)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 1)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_a)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 2)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_a)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 3)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_a)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 4)
	assert(libbind.ns_rr_type(rr) == libbind.ns_t_a)

    def testlibbind_ns_rr_class(self):
	"""Test whether ns_rr_class returns the correct class"""

	# This is only tested for inet class.  Chaosnet and Hesiod users will just have to wait.
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 0)
	assert(libbind.ns_rr_class(rr) == libbind.ns_c_in)

    def testlibbind_ns_rr_ttl(self):
	"""Test whether ns_rr_ttl returns the correct TTL"""

	# Query
	rr = libbind.ns_rr(self.msg, libbind.ns_s_qd, 0)
	assert(libbind.ns_rr_ttl(rr) == 0)

	# Answer
	rr = libbind.ns_rr(self.msg, libbind.ns_s_an, 0)
	assert(libbind.ns_rr_ttl(rr) == 0xe10)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_an, 1)
	assert(libbind.ns_rr_ttl(rr) == 0xe10)

	# Name servers
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 0)
	assert(libbind.ns_rr_ttl(rr) == 0x5460)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 1)
	assert(libbind.ns_rr_ttl(rr) == 0x5460)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 2)
	assert(libbind.ns_rr_ttl(rr) == 0x5460)

	# Additional
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 0)
	assert(libbind.ns_rr_ttl(rr) == 0x5460)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 1)
	assert(libbind.ns_rr_ttl(rr) == 0x5460)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 2)
	assert(libbind.ns_rr_ttl(rr) == 0x5460)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 3)
	assert(libbind.ns_rr_ttl(rr) == 0x7f19)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 4)
	assert(libbind.ns_rr_ttl(rr) == 0x7f19)

    def testns_rr_rdlen(self):
	"""Test whether ns_rr_rdlen returns the correct data length"""

	# Query
	rr = libbind.ns_rr(self.msg, libbind.ns_s_qd, 0)
	assert(libbind.ns_rr_rdlen(rr) == 0)

	# Answer
	rr = libbind.ns_rr(self.msg, libbind.ns_s_an, 0)
	assert(libbind.ns_rr_rdlen(rr) == 0x0a)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_an, 1)
	assert(libbind.ns_rr_rdlen(rr) == 0x0a)

	# Name servers
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 0)
	assert(libbind.ns_rr_rdlen(rr) == 0x0f)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 1)
	assert(libbind.ns_rr_rdlen(rr) == 0x06)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 2)
	assert(libbind.ns_rr_rdlen(rr) == 0x05)

	# Additional
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 0)
	assert(libbind.ns_rr_rdlen(rr) == 4)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 1)
	assert(libbind.ns_rr_rdlen(rr) == 4)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 2)
	assert(libbind.ns_rr_rdlen(rr) == 4)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 3)
	assert(libbind.ns_rr_rdlen(rr) == 4)
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 4)
	assert(libbind.ns_rr_rdlen(rr) == 4)

    def testlibbind_ns_rr_rdata(self):
	"""Test whether ns_rr_rdata returns the correct data"""
	import struct, socket
	def ip2str(str):
	    vals = str.split('.')
	    vals = map(int, vals)
	    return ''.join( map(chr, vals) )

	# Query
	rr = libbind.ns_rr(self.msg, libbind.ns_s_qd, 0)
	assert(libbind.ns_rr_rdata(rr) is None)

	# Answer
	rr = libbind.ns_rr(self.msg, libbind.ns_s_an, 0)
	assert(libbind.ns_rr_rdata(rr) == '\x00\x14\x05smtp1\xc0\x0c')
	rr = libbind.ns_rr(self.msg, libbind.ns_s_an, 1)
	assert(libbind.ns_rr_rdata(rr) == '\x00\x14\x05smtp2\xc0\x0c')

	# Name servers
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 0)
	assert(libbind.ns_rr_rdata(rr) == '\x03ns1\x05sonic\x03net\00')
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 1)
	assert(libbind.ns_rr_rdata(rr) == '\x03ns2\xc0\x59')
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ns, 2)
	assert(libbind.ns_rr_rdata(rr) == '\x02ns\xc0\x0c')

	# Additional
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 0)
	assert(libbind.ns_rr_rdata(rr) == ip2str('209.204.146.22'))
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 1)
	assert(libbind.ns_rr_rdata(rr) == ip2str('209.58.173.22'))
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 2)
	assert(libbind.ns_rr_rdata(rr) == ip2str('209.204.146.21'))
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 3)
	assert(libbind.ns_rr_rdata(rr) == ip2str('208.201.224.11'))
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 4)
	assert(libbind.ns_rr_rdata(rr) == ip2str('208.201.224.33'))

    def testlibbind_ns_rr_rdataNone(self):
	"""Test that ns_rr_rdata properly handles None's ref count"""

	# There is no way to test this with assert.  We just run a bunch of times
	# and if Python crashes, well, then we failed the test.
	rr = libbind.ns_rr(self.msg, libbind.ns_s_qd, 0)
	for i in xrange(1, 10000):
	    data = libbind.ns_rr_rdata(rr)
	    del data
	
	assert True

    def testlibbind_ns_name_uncompress(self):
	"""Test whether ns_name_uncompress returns the correct name"""
	msg = libbind.ns_msg(self.responses[2]['data'])

	# Query has no name record

	# Answer
	rr = libbind.ns_rr(msg, libbind.ns_s_an, 0)
	assert(libbind.ns_name_uncompress(msg, rr) == 'smtp1.oreilly.com')
	rr = libbind.ns_rr(msg, libbind.ns_s_an, 1)
	assert(libbind.ns_name_uncompress(msg, rr) == 'smtp2.oreilly.com')

	# Name servers
	rr = libbind.ns_rr(msg, libbind.ns_s_ns, 0)
	assert(libbind.ns_name_uncompress(msg, rr) == 'ns1.sonic.net')
	rr = libbind.ns_rr(msg, libbind.ns_s_ns, 1)
	assert(libbind.ns_name_uncompress(msg, rr) == 'ns2.sonic.net')
	rr = libbind.ns_rr(msg, libbind.ns_s_ns, 2)
	assert(libbind.ns_name_uncompress(msg, rr) == 'ns.oreilly.com')

	# Additional is just A records

    def testlibbind_ns_data_offset(self):
	"""Test whether ns_data_offset returns the correct offsets"""
	msg = libbind.ns_msg(self.responses[0]['data'])

	# Query has no name record
	rr = libbind.ns_rr(msg, libbind.ns_s_qd, 0)
	assert libbind.ns_data_offset(msg, rr) is None

	# Answer
	rr = libbind.ns_rr(msg, libbind.ns_s_an, 0)
	self.assertEquals(libbind.ns_data_offset(msg, rr), 49)

	# Name servers
	rr = libbind.ns_rr(msg, libbind.ns_s_ns, 0)
	self.assertEquals(libbind.ns_data_offset(msg, rr), 65)

	# Additional
	rr = libbind.ns_rr(msg, libbind.ns_s_ar, 0)
	self.assertEquals(libbind.ns_data_offset(msg, rr), 83)

    def testlibbind_ns_data_offsetNone(self):
	"""Test that ns_data_offset properly handles None's ref count"""

	msg = libbind.ns_msg(self.responses[0]['data'])
	rr  = libbind.ns_rr(msg, libbind.ns_s_qd, 0)

	# There is no way to test this with assert.  We just run a bunch of times
	# and if Python crashes, well, then we failed the test.
	for i in xrange(1, 10000):
	    data = libbind.ns_data_offset(msg, rr)
	    del data
	
	assert True

def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite(libbindTestCase, 'test') )
    return s

if __name__ == "__main__":
    unittest.main()
