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

class DNSRecordError(ConstrictError):
    """Error accessing record in message"""

class DNSMessage(object):
    """A DNS message.  This is an easy-to-understand object-oriented
    representation of standard DNS queries and responses, based on libbind.

    A DNSMessage contains these members:
    * id - a number representing the unique query ID
    * flags - a DNSFlags object from the header flags
    * records - A dict; the keys are sections ("question", "authority", etc.) and the
                values are lists of DNSRecord objects.
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
	sectionNames  = ('question', 'answer', 'authority', 'additional')
	sectionLabels = ('ns_s_qd', 'ns_s_an', 'ns_s_ns'  , 'ns_s_ar'   )

	for sectionName, sectionLabel in zip(sectionNames, sectionLabels):
	    section = getattr(libbind, sectionLabel)

	    totalRecords = libbind.ns_msg_count(msg, section)
	    if totalRecords > 0:
		self.sections[sectionName] = []
		for recordNum in range(0, totalRecords):
		    self.sections[sectionName].append(DNSRecord(msg, sectionName, recordNum))
    
    def __str__(self):
	info = []

	info.append("ID     : %d" % self.id)
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

	if libbind.ns_msg_getflag(msg, libbind.ns_f_aa):
	    self.authoritative = True
	else:
	    self.authoritative = False
	
	if libbind.ns_msg_getflag(msg, libbind.ns_f_tc):
	    self.truncated = True
	else:
	    self.truncated = False
	
	if libbind.ns_msg_getflag(msg, libbind.ns_f_rd):
	    self.recursionDesired = True
	else:
	    self.recursionDesired = False
	
	if libbind.ns_msg_getflag(msg, libbind.ns_f_ra):
	    self.recursionAvailable = True
	else:
	    self.recursionAvailable = False
	
	self.response = libbind.ns_msg_getflag(msg, libbind.ns_f_rcode)

    def __str__(self):
	return "\n".join((
	"Headers:",
	"  Type               : %s" % self.type,
	"  Opcode             : %d" % self.opcode,
	"  Authoritative      : %s" % str(self.authoritative),
	"  Truncated          : %s" % str(self.truncated),
	"  Recursion Desired  : %s" % str(self.recursionDesired),
	"  Recursion Available: %s" % str(self.recursionAvailable),
	"  Response Code      : %d" % self.response,
	))
    
class DNSRecord(object):
    """An individual record from a DNS message

    DNSRecord objects contain the following members:
	name       - Host name
	type       - Query type ('A', 'NS', 'CNAME', etc.)
	queryClass - Network class ('IN', 'Unknown')
	ttl        - Time to live for the data in the record
	data       - The value of the record
    """

    def __init__(self, msg, sectName, recordNum):
	"""Fills in all record values to the object members"""

	if type(msg) is not libbind.ns_msg:
	    raise DNSRecordError, "DNSFlags initialized but without an ns_msg"

# vim: sts=4 sw=4 noet
