/* libbind.c - A wrapper around the bind library
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

#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/nameser.h>
#include <resolv.h>

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

static char ns_msg_doc[] =
"This is a Python type that wraps the libbind ns_msg structure.  It is useful\n\
with the other libbind functions";

typedef struct {
    PyObject_HEAD
    ns_msg packet;
} libbind_ns_msg;

static PyTypeObject libbind_ns_msgType = {
    PyObject_HEAD_INIT(NULL)
    0,						/* ob_size */
    "Constrict.libbind.ns_msg",			/* tp_name */
    sizeof(libbind_ns_msg),			/* tp_basicsize */
    0,						/* tp_itemsize */
    0,						/* tp_dealloc */
    0,						/* tp_print */
    0,						/* tp_getattr */
    0,						/* tp_setattr */
    0,						/* tp_compare */
    0,						/* tp_repr */
    0,						/* tp_as_number */
    0,						/* tp_as_sequence */
    0,						/* tp_as_mapping */
    0,						/* tp_hash */
    0,						/* tp_call */
    0,						/* tp_str */
    0,						/* tp_getattro */
    0,						/* tp_setattro */
    0,						/* tp_as_buffer */
    Py_TPFLAGS_DEFAULT			,	/* tp_flags */
    ns_msg_doc,					/* tp_doc */
};

/* Initialize the extension. */
PyMODINIT_FUNC
initlibbind(void)
{
    PyObject *m;

    libbind_ns_msgType.tp_new = PyType_GenericNew;
    if( PyType_Ready(&libbind_ns_msgType) < 0 )
	return;

    m = Py_InitModule3("Constrict.libbind", libbind_methods, libbind_doc);

    if( m == NULL )
	return;

    Py_INCREF(&libbind_ns_msgType);
    PyModule_AddObject(m, "ns_msg", (PyObject *)&libbind_ns_msgType);
}

// vim: sts=4 sw=4 noet
