/* libbind.c - Wraps around the ns_msg_* BIND library routines
 *
 * This file is part of Constrict.
 *
 * Constrict is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Constrict is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Constrict; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include <Python.h>
//#include <python2.3/structmember.h>

/*
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/nameser.h>
#include <resolv.h>
*/

static char libbind_doc[] = 
"This module is a thin wrapper around the libbind parsing routines.";

static char libbind_ns_msg_id_doc[] =
"Returns the DNS message unique ID";

static PyObject *
libbind_ns_msg_id(PyObject *self, PyObject *args)
{
    unsigned id = 23;	/* TODO */

    return Py_BuildValue("i", id);
}

static PyMethodDef libbind_methods[] = {
    {"ns_msg_id", libbind_ns_msg_id, METH_VARARGS, libbind_ns_msg_id_doc},
    {NULL, NULL}
};

/* Initialize the extension. */
PyMODINIT_FUNC
initlibbind(void)
{
    PyObject *m;

    m = Py_InitModule3("Constrict.libbind", libbind_methods, libbind_doc);
}

// vim: sts=4 sw=4 noet
