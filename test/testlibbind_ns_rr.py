#!/usr/bin/env python
#
# testlibbind_ns_rr.py - Unit tests for the libbind ns_rr wrapper
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

from Constrict import libbind

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

    def testReturnsName(self):
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

    def testReturnsType(self):
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

    def testReturnsClass(self):
	"""Test whether ns_rr_type returns the correct class"""

	# This is only tested for inet class.  Chaosnet and Hesiod users will just have to wait.
	rr = libbind.ns_rr(self.msg, libbind.ns_s_ar, 0)
	assert(libbind.ns_rr_class(rr) == libbind.ns_c_in)

    def testReturnsTTL(self):
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

    def testReturnsRdlen(self):
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

def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite(ns_rrTestCase, 'test') )
    return s

if __name__ == "__main__":
    unittest.main()
