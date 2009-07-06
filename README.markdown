This package is for parsing DNS messages as you would see them from a network
capture or your own network application.  It is a Python interface to the
libbind DNS message parsing library.

A useful reference for this software is DNS and BIND, 5th Edition from
O'Reilly.

Installation
============

Strangle is a standard distutils-driven Python package.  For all
platforms, you will need the C and Python development environment (e.g.
for .deb distributions, libc6-dev and python-dev; for RPM distributions,
python-devel).  Strangle
also has a C language component that must be compiled against the BIND
parsing library (libbind).  For Debian, you need the "bind-dev" package,
as well as standard C development packages (gcc, libc6-dev, etc.).  for
RPM-based distributions, try the bind-devel package.

1. Uncompress the archive that you have downloaded.  By default, it will
   extract to a directory named Strangle-<something>.

2. Change to that directory and run the install command:

        # python setup.py install

3. Everything should compile properly and you should be able to use the
   Strangle library from any location in your system.

        >>> import Strangle
        >>> Strangle
        <module 'Strangle' from '.../site-packages/Strangle/__init__.pyc'>
        >>>

Supported Platforms
===================

These platforms are tested and supported in this version of Strangle:

* Ubuntu
  * 8.04 Long-Term Support ("Hardy"): i386 builds from source; for amd64,
    you must install the libbind4 and libbind4-dev packages from
    the Debian Squeeze release or later.  The packages have very basic
    dependencies and install into Ubuntu trivially.
  * 9.04 ("Jaunty"): amd64

If you can confirm that this package builds for other architectures, please
contact Jason Smith at the address below.

Untested Platforms
==================

* Ubuntu 9.04, i386
* Solaris 10, both arches
* OpenSolaris, both arches
* CentOS, both arches
* OpenSUSE, both arches

Copyright Information
=====================

Strangle is licensed to you under the terms of the GNU General public
license, version 2.  For the full text of this license, please see the
COPYING file which accompanies these instructions.

Proven Corporation offers software and expertise based on Strangle.
Please see our web site.  Thank you very much.

Author:

    Jason Smith <jhs@proven-corporation.com>
    Proven Corporation Co., Ltd.
    Bangkok, Thailand
    http://www.proven-corporation.com
