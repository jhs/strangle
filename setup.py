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

libbind = Extension('Constrict.libbind',
		    [
		     'Constrict/libbind.c',
		    ],
		    libraries=['bind'],
		    **extras
		   )

setup( name         = 'Constrict',
       version      = '0.2.1',
       description  = 'Library for comprehending DNS messages using BIND parsing',
       license      = 'GNU GPL 2.0',
       author       = 'Open Enterprise Systems',
       author_email = 'jhs@oes.co.th',
       url          = 'http://projects.oes.co.th/Constrict',
       packages     = ['Constrict'],
       ext_modules  = [ libbind ],
     )
