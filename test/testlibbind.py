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
		 record = 'a',
		 host = 'www.microsoft.com.nsatc.net',
		 data = file(os.path.join('data', 'www.microsoft.com-query')).read(),
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
		 record = 'a',
		 host = 'www.microsoft.com.nsatc.net',
		 data = file(os.path.join('data', 'www.microsoft.com-response')).read(),
		),
	    ]

	assert(self.queries)
	assert(self.responses)

	self.flags = ['qr', 'opcode', 'aa', 'tc', 'rd', 'ra', 'z', 'ad', 'cd', 'rcode', 'max']
	self.flags = map(lambda str: 'ns_f_' + str, self.flags)

	self.sections = ['qd', 'zn', 'an', 'pr', 'ns', 'ud', 'ar']
	self.sections = map(lambda str: 'ns_s_' + str, self.sections)

    def testlibbindHasEnums(self):
	"""Test whether libbind correctly defines all header flags"""
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

def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite(libbindTestCase, 'test') )
    return s

if __name__ == "__main__":
    unittest.main()
