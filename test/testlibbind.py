#!/usr/bin/env python
#
# testlibbind.py - Unit tests for the libbind functions
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

# All tests will be in here since it's not an object-oriented interface
class libbindTestCase(unittest.TestCase):
    """Tests all useful functions in libbind"""
    def setUp(self):
	import os, re

	# Values taken from ethereal and hex dump
	self.queries   = [
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

	self.responses = [
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

	assert(self.queries)
	assert(self.responses)

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

    def testReturnsRdata(self):
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

def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite(libbindTestCase, 'test') )
    return s

if __name__ == "__main__":
    unittest.main()
