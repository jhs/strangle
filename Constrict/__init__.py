# Constrict.py - An object-oriented look at DNS messages based on libbind
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

"""An object-oriented library for comprehending DNS messages using BIND parsing"""

import libbind

class ConstrictError(StandardError):
    """Error parsing DNS packet"""

class DNSMessage(object):
    """A DNS message.  This is an easy-to-understand object-oriented
    representation of standard DNS queries and responses, based on libbind.

    A DNSMessage contains these members:
    * id - a number representing the unique query ID
    * flags - a DNSFlags object from the header flags
    * sections - a dict of sections (usually "question", "authority", etc.)
    """

    def __init__(self, packetData):
	"""Create a DNSMessage object from a string of the raw DNS message"""

	# If packetData has a read() method, we use it as for a file.
	if getattr(packetData, 'read', None) is not None:
	    packetData = packetData.read()
	
	try:
	    msg = libbind.ns_msg(packetData)
	except TypeError:
	    raise ConstrictError, "Failed to parse the packet"
	
	self.id       = libbind.ns_msg_id(msg)
	self.flags    = DNSFlags(msg)
	self.sections = {}

	for sectionName in ('question', 'answer', 'authority', 'additional'):
	    section = DNSSection(msg, section=sectionName)
	    if section is not None:
		self.sections[sectionName] = section
    
    def __str__(self):
	info = []

	info.append("ID: %d" % self.id)
	info.append(self.flags.__str__())
	for section in self.sections.values():
	    info.append(section.__str__())
	
	return "\n".join(info)

class DNSFlags(object):
    """Flags from a DNS message headers

    A DNSFlags object contains the following members:
	type               - String ('query', 'response')
	opcode             - Integer
	authoritative      - Boolean
	truncated          - Boolean
	recursionDesired   - Boolean
	recursionAvailable - Boolean
	reponse            - Integer (server response code)
    """

    def __init__(self, msg):
	"""Fills in all flag values to the object members"""

	if type(msg) is not libbind.ns_msg:
	    raise ConstrictError, "DNSFlags initialized but without an ns_msg"

	isResponse = libbind.ns_msg_getflag(msg, libbind.ns_f_qr)
	if isResponse:
	    self.type = 'response'
	else:
	    self.type = 'query'
	
	self.opcode = libbind.ns_msg_getflag(msg, libbind.ns_f_opcode)
    
# TODO
class DNSSection(object):
    def __init__(self, *args, **kwargs):
	pass

# vim: sts=4 sw=4 noet
