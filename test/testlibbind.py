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
		 type = 'query',
		 record = 'a',
		 host = 'www.company.example',
		 data = file(os.path.join('data', 'www.company.example-query')).read(),
		),
	    dict(id = 0xb7f8,
		 type = 'query',
		 record = 'a',
		 host = 'www.microsoft.com.nsatc.net',
		 data = file(os.path.join('data', 'www.microsoft.com-query')).read(),
		),
	    ]

	self.responses = [
	    dict(id = 0xf2eb,
		 type = 'response',
		 record = 'a',
		 host = 'www.company.example',
		 data = file(os.path.join('data', 'www.company.example-response')).read(),
		),
	    dict(id = 0xb7f8,
		 type = 'response',
		 record = 'a',
		 host = 'www.microsoft.com.nsatc.net',
		 data = file(os.path.join('data', 'www.microsoft.com-response')).read(),
		),
	    ]

	assert(self.queries)
	assert(self.responses)

    def testlibbind_ns_msg_id(self):
	for query in self.queries:
	    n = libbind.ns_msg(query['data'])
	    assert(libbind.ns_msg_id(n) == query['id'])
	
def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite(libbindTestCase, 'test') )
    return s

if __name__ == "__main__":
    unittest.main()
