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

static char libbind_ns_msg_doc[] =
"This is a Python type that wraps the libbind ns_msg structure.  It is useful\n\
with the other libbind functions";

typedef struct {
    PyObject_HEAD
    ns_msg packet;
} libbind_ns_msg;

/* __init__() */
static int
libbind_ns_msg_init(libbind_ns_msg *self, PyObject *args)
{
    char *packetData;
    int  packetLength, result;

    if( !PyArg_ParseTuple(args, "s#", &packetData, &packetLength) )
	return -1;

    result = ns_initparse(packetData, packetLength, &(self->packet));
    if( result != 0 ) {
	PyErr_SetString(PyExc_TypeError, "BIND cannot parse this packet");
	return -1;
    }

    return 0;
}

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
    Py_TPFLAGS_DEFAULT,				/* tp_flags */
    libbind_ns_msg_doc,				/* tp_doc */
    0,						/* tp_traverse       */
    0,						/* tp_clear          */
    0,						/* tp_richcompare    */
    0,						/* tp_weaklistoffset */
    0,						/* tp_iter           */
    0,						/* tp_iternext       */
    0,						/* tp_methods        */
    0,						/* tp_members        */
    0,						/* tp_getset         */
    0,						/* tp_base           */
    0,						/* tp_dict           */
    0,						/* tp_descr_get      */
    0,						/* tp_descr_set      */
    0,						/* tp_dictoffset     */
    (initproc)libbind_ns_msg_init,		/* tp_init           */
};

static char libbind_ns_msg_id_doc[] =
"Returns the DNS message unique ID";

static PyObject *
libbind_ns_msg_id(PyObject *self, PyObject *args)
{
    unsigned id;
    PyObject *message;
    PyTypeObject *messageType;
    char         *messageTypeStr;

    if( !PyArg_ParseTuple(args, "O", &message) )
	return NULL;

    messageType    = (PyTypeObject *)(message->ob_type);
    messageTypeStr = messageType->tp_name;
    if( strcmp(messageTypeStr, "Constrict.libbind.ns_msg") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_msg object");
	return NULL;
    }

    id = ns_msg_id( ((libbind_ns_msg *)message)->packet );
    return Py_BuildValue("i", id);
}

static char libbind_ns_msg_getflag_doc[] =
"Returns the requested flag field from an ns_msg object";

static PyObject *
libbind_ns_msg_getflag(PyObject *self, PyObject *args)
{
    PyObject *message;
    int flag;
    u_int16_t flagVal;

    PyTypeObject *messageType;
    char         *messageTypeStr;

    if( !PyArg_ParseTuple(args, "Oi", &message, &flag) )
	return NULL;

    messageType    = (PyTypeObject *)(message->ob_type);
    messageTypeStr = messageType->tp_name;
    if( strcmp(messageTypeStr, "Constrict.libbind.ns_msg") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_msg object");
	return NULL;
    }

    flagVal = ns_msg_getflag(((libbind_ns_msg *)message)->packet, flag);
    return Py_BuildValue("i", (int)flagVal);
}

static PyMethodDef libbind_methods[] = {
    {"ns_msg_id"      , libbind_ns_msg_id      , METH_VARARGS, libbind_ns_msg_id_doc},
    {"ns_msg_getflag", libbind_ns_msg_getflag, METH_VARARGS, libbind_ns_msg_getflag_doc},
    {NULL, NULL}
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

    /* These are the ns_flag enums.  We just use Python ints (PyLongs). */
    PyModule_AddObject(m, "ns_f_qr"    , PyInt_FromLong(ns_f_qr));
    PyModule_AddObject(m, "ns_f_opcode", PyInt_FromLong(ns_f_opcode));
    PyModule_AddObject(m, "ns_f_aa", PyInt_FromLong(ns_f_aa));
    PyModule_AddObject(m, "ns_f_tc", PyInt_FromLong(ns_f_tc));
    PyModule_AddObject(m, "ns_f_rd", PyInt_FromLong(ns_f_rd));
    PyModule_AddObject(m, "ns_f_ra", PyInt_FromLong(ns_f_ra));
    PyModule_AddObject(m, "ns_f_z", PyInt_FromLong(ns_f_z));
    PyModule_AddObject(m, "ns_f_ad", PyInt_FromLong(ns_f_ad));
    PyModule_AddObject(m, "ns_f_cd", PyInt_FromLong(ns_f_cd));
    PyModule_AddObject(m, "ns_f_rcode", PyInt_FromLong(ns_f_rcode));
    PyModule_AddObject(m, "ns_f_max", PyInt_FromLong(ns_f_max));
}

// vim: sts=4 sw=4 noet
