from distutils.core import setup, Extension

libbind = Extension('Constrict.libbind',
		    ['Constrict/libbind.c'],
		    libraries=['bind'],
		   )

setup( name         = 'Constrict',
       version      = '0.1.0',
       description  = 'Library for comprehending DNS messages using BIND parsing',
       author       = 'Open Enterprise Systems',
       author_email = 'jhs@oes.co.th',
       url          = 'http://projects.oes.co.th/Constrict',
       packages     = ['Constrict'],
       ext_modules  = [ libbind ],
     )
