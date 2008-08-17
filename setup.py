import sys
from distutils.core import setup, Extension

extras = {}

if sys.platform == 'sunos5':
    # This handles Solaris systems with BIND installed from the package
    extras['include_dirs'] = ['/usr/local/bind/include']
    extras['library_dirs'] = ['/usr/local/bind/lib']

    # This allows non-PIC code (in our case, libbind.a) to become a shared
    # library.  It is not exactly the same as a true shared library, but
    # it works.  See the GCC man page on -mimpure-text.
    extras['extra_link_args'] = ['-mimpure-text']

libbind = Extension('Strangle.libbind',
		    [
		     'Strangle/libbind.c',
		    ],
		    libraries=['bind'],
		    **extras
		   )

long_desc = """
Summary
=======

Strangle is BIND for Python: a Python library for parsing DNS messages
using libbind. Strangle allows you to see DNS messages in two ways:

  * Direct access to the libbind parsing functions (C-style)
  * A Python object with various meaningful attributes (OO-style)

Demo
====

Here is an example of how simple it is to parse DNS messages::

  >>> import Strangle
  >>> msgFile = file("test/data/www.microsoft.com-query")
  >>> msg = Strangle.DNSMessage(msgFile)
  >>> msg.id
  47096
  >>> print msg
  ID     : 47096
  Headers:
    Type               : question
    Opcode             : 0
    Authoritative      : False
    Truncated          : False
    Recursion Desired  : True
    Recursion Available: False
    Response Code      : 0
  
  ;; QUESTION SECTION:
  www.microsoft.com.nsatc.net 0       IN      A
  
  >>> msg.flags.type
  'question'
  >>> msg.flags.recursionDesired
  True
"""

classifiers = """
    Development Status :: 5 - Production/Stable
    Environment :: No Input/Output (Daemon)
    Intended Audience :: Developers
    License :: OSI Approved
    License :: OSI Approved :: GNU General Public License (GPL)
    Operating System :: POSIX
    Operating System :: POSIX :: Linux
    Operating System :: Unix
    Programming Language :: C
    Programming Language :: Python
    Topic :: Internet :: Name Service (DNS)
    Topic :: Software Development :: Libraries
    Topic :: Software Development :: Libraries :: Python Modules
    Topic :: System :: Monitoring
    Topic :: System :: Networking
"""

setup( name         = 'Strangle',
       version      = '0.3.1',
       description  = 'Library for comprehending DNS messages using BIND parsing',
       long_description = long_desc,
       classifiers  = [line.strip() for line in classifiers.split('\n') if line != ""],
       license      = 'GNU GPL 2.0',
       author       = 'Proven Corporation',
       author_email = 'jhs@proven-corporation.com',
       url          = 'http://www.proven-corporation.com/software/strangle/',
       packages     = ['Strangle'],
       ext_modules  = [ libbind ],
     )
