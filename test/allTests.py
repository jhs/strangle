#!/usr/bin/env python
#
# allTests.py - Big wrapper around all Unit tests
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

import unittest

fullSuite = unittest.TestSuite()

import testlibbind_ns_msg
fullSuite.addTest(testlibbind_ns_msg.suite())

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(fullSuite)