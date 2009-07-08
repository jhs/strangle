import sys
from distutils.core import setup, Extension

extras = {}

if sys.platform == 'sunos5':
    # This handles Solaris systems with BIND installed from the package
    extras['include_dirs'] = ['/usr/local/bind/include']
    extras['library_dirs'] = ['/usr/local/bind/lib']

    # This allows non-PIC code (in our case, libresolv.a) to become a shared
    # library.  It is not exactly the same as a true shared library, but
    # it works.  See the GCC man page on -mimpure-text.
    extras['extra_link_args'] = ['-mimpure-text']

elif sys.platform == 'linux2':
    import os
    import re
    import platform

    is_64 = platform.machine() == 'x86_64'

    if os.path.exists('/etc/lsb-release'):
        if os.path.exists('/etc/SuSE-release'):
            # Configure for openSUSE / SLED.
            release = None
            for line in file('/etc/SuSE-release').readlines():
                match = re.search(r'VERSION = (.*)$', line)
                if match:
                    release = match.groups()[0]
            if release != '11.1':
                sys.stderr.write("Warning: Building for unknown SuSE release: %s\n" % release)

            # Dynamic link against glibc.
            extras['libraries'] = ['resolv']
        else:
            # Configure for Ubuntu.
            release = None
            for line in file('/etc/lsb-release').readlines():
                match = re.search(r'DISTRIB_RELEASE=(.*)$', line)
                if match:
                    release = match.groups()[0]
            if release == '8.04':
                # Configure for Hardy / LTS.
                if is_64:
                    # Dynamic link against the (backported) libbind4 package.
                    extras['libraries'] = ['bind']
                else:
                    # Static link against libc's code.
                    extras['extra_link_args'] = ['/usr/lib/libresolv.a']
            elif release == '9.04':
                # Configure for 9.04 Jaunty.  By now, libresolv.so exports the symbols we need.
                extras['libraries'] = ['resolv']
            else:
                sys.stderr.write("Warning: Building for unknown Ubuntu release: %s\n" % release)

    elif os.path.exists('/etc/redhat-release'):
        # Configure for CentOS / RHEL.
        line = file('/etc/redhat-release').read()
        match = re.search(r'release (.*) \(', line)
        release = match.groups()[0]
        if release != '5.3':
            sys.stderr.write("Warning: Building for unknown Red Hat release: %s\n" % release)

        # Dynamic link against libbind from bind-libs.
        extras['libraries'] = ['bind']
    else:
        # Configure for a general (whatever that means) Linux system.
        sys.stderr.write("Warning: Building for unknown Linux distribution")
        extras['libraries'] = ['resolv']

#
# Actual package configuration begins here.
#

libbind = Extension('Strangle.libbind',
		    [
		     'Strangle/libbind.c',
		    ],
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
       version      = '0.3.2',
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
