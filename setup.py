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

setup( name         = 'Strangle',
       version      = '0.2.2',
       description  = 'Library for comprehending DNS messages using BIND parsing',
       license      = 'GNU GPL 2.0',
       author       = 'Proven Corporation',
       author_email = 'jhs@proven-corporation.com',
       url          = 'http://www.proven-corporation.com/software/strangle/',
       packages     = ['Strangle'],
       ext_modules  = [ libbind ],
     )
