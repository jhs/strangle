# Strangle.py - An object-oriented look at DNS messages based on libbind
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

"""An object-oriented library for comprehending DNS messages using BIND parsing"""

import libbind
import socket
import struct

class StrangleError(StandardError):
    """Error parsing DNS packet"""

class DNSSectionError(StrangleError):
    """Error generating a message section"""

class DNSRecordError(StrangleError):
    """Error accessing record in message"""

class DNSMessage(object):
    """A DNS message.  This is an easy-to-understand object-oriented
    representation of standard DNS queries and responses, based on libbind.

    A DNSMessage contains these members:
    * id - a number representing the unique query ID
    * flags - a DNSFlags object from the header flags
    * records - A dict; the keys are sections ("question", "authority", etc.) and the
                values are lists of DNSRecord objects.
    
    Also there is a "msg" member, which references the low-level libbind.ns_msg object,
    if you need it.
    """

    def __init__(self, packetData):
	"""Create a DNSMessage object from a string of the raw DNS message"""

	# If packetData has a read() method, we use it as for a file.
	if getattr(packetData, 'read', None) is not None:
	    packetData = packetData.read()
	
	try:
	    msg = libbind.ns_msg(packetData)
	except TypeError:
	    raise StrangleError, "Failed to parse the packet"
	
	self.msg = msg
    
	self.id       = libbind.ns_msg_id(msg)
	self.flags    = DNSFlags(msg)

	self.sections = {}
	for sectionName in ('question', 'answer', 'authority', 'additional'):
	    try:
		self.sections[sectionName] = DNSSection(msg, section=sectionName)
	    except DNSSectionError:
		# This is normal.  It means that the section does not exist in this message.
		pass

    def __str__(self):
	info = []

	info.append("ID     : %d" % self.id)
	info.append(self.flags.__str__())
	sections = self.sections.keys()
	sections.sort(self.sectionSorter)
	for section in sections:
	    info.append(self.sections[section].__str__())
	
	return "\n".join(info)

    def sectionSorter(self, a, b):
	"""A comparison function for sort routines to output sections in the right order"""
	order = [ 'question', 'answer', 'authority', 'additional' ]
	return cmp(order.index(a), order.index(b))

class DNSFlags(object):
    """Flags from a DNS message headers

    A DNSFlags object contains the following members:
	type               - String ('question', 'answer')
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
	    raise StrangleError, "DNSFlags initialized but without an ns_msg"

	isResponse = libbind.ns_msg_getflag(msg, libbind.ns_f_qr)
	if isResponse:
	    self.type = 'answer'
	else:
	    self.type = 'question'
	
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

class DNSSection(object):
    """A section of a DNS message.  Typically these are 'question', 'answer',
       'authority', or 'additional'.

       Members:
           name     - name of the section
    """

    def __init__(self, msg, *args, **kwargs):
	"""Initialize a message section"""

	self.mapping = { 'question'   : libbind.ns_s_qd,
			 'answer'     : libbind.ns_s_an,
			 'authority'  : libbind.ns_s_ns,
			 'additional' : libbind.ns_s_ar,
		       }

	if type(msg) is not libbind.ns_msg:
	    raise DNSSectionError, "DNSSection initialized but without an ns_msg"
	
	try:
	    sectionName = kwargs['section']
	except KeyError:
	    try:
		sectionName = args[0]
	    except IndexError:
		raise DNSSectionError, "DNSSection requires a section name argument"
	
	if sectionName not in self.mapping.keys():
	    raise DNSSectionError, "DNSSection requires a valid section name"

	section = self.mapping[sectionName]
	totalRecords = libbind.ns_msg_count(msg, section)
	if totalRecords < 1:
	    raise DNSSectionError, "No such section in this message"
	
	self.name = sectionName

	self.records = []
	for recordNum in range(0, totalRecords):
	    self.addRecord(DNSRecord(msg, sectionName, recordNum))

    def numRecords(self):
	"""Return the number of records in this section"""
	return len(self.records)

    def addRecord(self, record):
	"""Add a DNSRecord to the section"""
	self.records.append(record)
	return self.records[-1] is record

    def getRecord(self, recordNum):
	"""Fetch a DNSRecord from the section"""
	try:
	    record = self.records[recordNum]
	except IndexError:
	    raise DNSSectionError, "No such record"
	return record

    def __str__(self):
	"""Printable output"""
	import string

	info = []
	info.append("\n;; %s SECTION:" % string.upper(self.name))
	for record in self.records:
	    info.append(record.__str__())
	
	return "\n".join(info)

class DNSRecord(object):
    """An individual record from a DNS message

    DNSRecord objects contain the following members:
	name       - Host name
	type       - Query type ('A', 'NS', 'CNAME', etc. or 'Unknown')
	queryClass - Network class ('IN', 'Unknown')
	ttl        - Time to live for the data in the record
	data       - The value of the record or None if not applicable

    Also there is an "rr" member, which references the low-level libbind.ns_rr object,
    if you need it.
    """

    def __init__(self, msg, sectionName, recordNum):
	"""Fills in all record values to the object members"""

	if type(msg) is not libbind.ns_msg:
	    raise DNSRecordError, "DNSRecord initialized but without an ns_msg"
	
	self.mapping = { 'question'   : libbind.ns_s_qd,
			 'answer'     : libbind.ns_s_an,
			 'authority'  : libbind.ns_s_ns,
			 'additional' : libbind.ns_s_ar,
		       }

	if sectionName not in self.mapping.keys():
	    raise DNSRecordError, "DNSRecord requires a valid section name"

	section = self.mapping[sectionName]
	try:
	    self.rr = libbind.ns_rr(msg, section, recordNum)
	except TypeError:
	    raise DNSRecordError, 'The section "%"s does not have this record, %d' % (sectionName, recordNum)
	
	self.name       = libbind.ns_rr_name(self.rr)
	self.ttl        = libbind.ns_rr_ttl(self.rr)

	self.queryClass = libbind.ns_rr_class(self.rr)
	if self.queryClass == libbind.ns_c_in:
	    self.queryClass = 'IN'
	elif self.queryClass == libbind.ns_c_none:
	    self.queryClass = 'None'
	else:
	    self.queryClass = 'Unknown (%d)' % self.queryClass
	
	self.type = libbind.ns_rr_type(self.rr)
	typeDict = { libbind.ns_t_a     : 'A',
		     libbind.ns_t_ns    : 'NS',
		     libbind.ns_t_cname : 'CNAME',
		     libbind.ns_t_soa   : 'SOA',
		     libbind.ns_t_null  : 'NULL',
		     libbind.ns_t_ptr   : 'PTR',
		     libbind.ns_t_hinfo : 'HINFO',
		     libbind.ns_t_mx    : 'MX',
		     libbind.ns_t_txt   : 'TXT',
		     libbind.ns_t_sig   : 'SIG',
		     libbind.ns_t_key   : 'KEY',
		     libbind.ns_t_aaaa  : 'AAAA',
		     libbind.ns_t_loc   : 'LOC',
		     libbind.ns_t_srv   : 'SRV',
		     libbind.ns_t_tsig  : 'TSIG',
		     libbind.ns_t_ixfr  : 'IXFR',
		     libbind.ns_t_axfr  : 'AXFR',
		     libbind.ns_t_any   : 'ANY',
		     libbind.ns_t_zxfr  : 'ZXFR',
		   }
	try:
	    self.type = typeDict[self.type]
	except KeyError:
	    self.type = 'Unknown'
	
	rdata = libbind.ns_rr_rdata(self.rr)
	if rdata is None:
	    # Query records look like this
	    self.data = ""
	else:
	    if self.type == 'A':
		if len(rdata) == 4:
		    self.data = socket.inet_ntoa(rdata)
		else:
		    self.data = ''
	    elif self.type in ('NS', 'CNAME', 'SOA', 'PTR'):
		self.data = libbind.ns_name_uncompress(msg, self.rr)
	    elif self.type == 'MX':
		preference = struct.unpack('!H', rdata[0:2])[0]
		self.data = "%d %s" % (preference, libbind.ns_name_uncompress(msg, self.rr))
	    else:
		self.data = rdata

    def __str__(self):
	return "%-23s %-7d %-7s %-7s %s" % (self.name, self.ttl, self.queryClass, self.type, self.data)

# vim: sts=4 sw=4 noet
