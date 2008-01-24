/* libbind.c - A wrapper around the bind library
 *
 * This file is part of Strangle.
 *
 * Strangle is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Strangle is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Strangle; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include <Python.h>

#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/nameser.h>
#include <resolv.h>

#include <strings.h>

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
    "Strangle.libbind.ns_msg",			/* tp_name */
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

static char libbind_ns_rr_doc[] =
"This is a Python type that wraps the libbind ns_rr structure.  It is useful\n\
with the other libbind functions";

typedef struct {
    PyObject_HEAD
    ns_rr record;
} libbind_ns_rr;

/* __init__() */
static int
libbind_ns_rr_init(libbind_ns_rr *self, PyObject *args)
{
    PyObject       *firstArg;
    libbind_ns_msg *message;
    int section, rrnum, result;
    PyTypeObject *messageType;
    char         *messageTypeStr;

    if( !PyArg_ParseTuple(args, "Oii", &firstArg, &section, &rrnum) )
	return -1;

    messageType    = (PyTypeObject *)(firstArg->ob_type);
    messageTypeStr = messageType->tp_name;
    if( strcmp(messageTypeStr, "Strangle.libbind.ns_msg") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_msg object");
	return -1;
    }

    message = (libbind_ns_msg *)firstArg;

    result = ns_parserr(&(message->packet), section, rrnum, &(self->record));
    if( result != 0 ) {
	PyErr_SetString(PyExc_TypeError, "BIND says there is no such record in this message");
	return -1;
    }

    return 0;
}

static PyTypeObject libbind_ns_rrType = {
    PyObject_HEAD_INIT(NULL)
    0,						/* ob_size */
    "Strangle.libbind.ns_rr",			/* tp_name */
    sizeof(libbind_ns_rr),			/* tp_basicsize */
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
    libbind_ns_rr_doc,				/* tp_doc */
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
    (initproc)libbind_ns_rr_init,		/* tp_init           */
};

static char libbind_ns_msg_id_doc[] =
"Returns the DNS message unique ID";

static PyObject *
libbind_ns_msg_id(PyObject *self, PyObject *args)
{
    u_int16_t id;
    PyObject *message;
    PyTypeObject *messageType;
    char         *messageTypeStr;

    if( !PyArg_ParseTuple(args, "O", &message) )
	return NULL;

    messageType    = (PyTypeObject *)(message->ob_type);
    messageTypeStr = messageType->tp_name;
    if( strcmp(messageTypeStr, "Strangle.libbind.ns_msg") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_msg object");
	return NULL;
    }

    id = ns_msg_id( ((libbind_ns_msg *)message)->packet );
    return PyInt_FromLong((long)id);
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
    if( strcmp(messageTypeStr, "Strangle.libbind.ns_msg") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_msg object");
	return NULL;
    }

    flagVal = ns_msg_getflag(((libbind_ns_msg *)message)->packet, flag);
    return Py_BuildValue("i", (int)flagVal);
}

static char libbind_ns_msg_count_doc[] =
"Returns the number of entries in a given section of an ns_msg object";

static PyObject *
libbind_ns_msg_count(PyObject *self, PyObject *args)
{
    PyObject *message;
    int section;
    u_int16_t count;

    PyTypeObject *messageType;
    char         *messageTypeStr;

    if( !PyArg_ParseTuple(args, "Oi", &message, &section) )
	return NULL;

    messageType    = (PyTypeObject *)(message->ob_type);
    messageTypeStr = messageType->tp_name;
    if( strcmp(messageTypeStr, "Strangle.libbind.ns_msg") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_msg object");
	return NULL;
    }

    count = ns_msg_count(((libbind_ns_msg *)message)->packet, section);
    return Py_BuildValue("i", (int)count);
}

static char libbind_ns_rr_name_doc[] =
"Returns the name (i.e. usually host name) in an ns_rr record";

static PyObject *
libbind_ns_rr_name(PyObject *self, PyObject *args)
{
    PyObject *rr;
    char *name;

    PyTypeObject *argType;
    char         *argTypeStr;

    if( !PyArg_ParseTuple(args, "O", &rr) )
	return NULL;

    argType    = (PyTypeObject *)(rr->ob_type);
    argTypeStr = argType->tp_name;
    if( strcmp(argTypeStr, "Strangle.libbind.ns_rr") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_rr object");
	return NULL;
    }

    name = ns_rr_name(((libbind_ns_rr *)rr)->record);
    return PyString_FromString(name);
}

static char libbind_ns_rr_type_doc[] =
"Returns the type of an ns_rr record";

static PyObject *
libbind_ns_rr_type(PyObject *self, PyObject *args)
{
    PyObject *rr;
    u_int16_t type;

    PyTypeObject *argType;
    char         *argTypeStr;

    if( !PyArg_ParseTuple(args, "O", &rr) )
	return NULL;

    argType    = (PyTypeObject *)(rr->ob_type);
    argTypeStr = argType->tp_name;
    if( strcmp(argTypeStr, "Strangle.libbind.ns_rr") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_rr object");
	return NULL;
    }

    type = ns_rr_type(((libbind_ns_rr *)rr)->record);
    return PyInt_FromLong((long)type);
}

static char libbind_ns_rr_class_doc[] =
"Returns the network class of an ns_rr record (usually ns_c_in for Internet)";

static PyObject *
libbind_ns_rr_class(PyObject *self, PyObject *args)
{
    PyObject *rr;
    u_int16_t class;

    PyTypeObject *argType;
    char         *argTypeStr;

    if( !PyArg_ParseTuple(args, "O", &rr) )
	return NULL;

    argType    = (PyTypeObject *)(rr->ob_type);
    argTypeStr = argType->tp_name;
    if( strcmp(argTypeStr, "Strangle.libbind.ns_rr") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_rr object");
	return NULL;
    }

    class = ns_rr_class(((libbind_ns_rr *)rr)->record);
    return PyInt_FromLong((long)class);
}

static char libbind_ns_rr_ttl_doc[] =
"Returns the time to live of an ns_rr record";

static PyObject *
libbind_ns_rr_ttl(PyObject *self, PyObject *args)
{
    PyObject *rr;
    u_int32_t ttl;

    PyTypeObject *argType;
    char         *argTypeStr;

    if( !PyArg_ParseTuple(args, "O", &rr) )
	return NULL;

    argType    = (PyTypeObject *)(rr->ob_type);
    argTypeStr = argType->tp_name;
    if( strcmp(argTypeStr, "Strangle.libbind.ns_rr") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_rr object");
	return NULL;
    }

    ttl = ns_rr_ttl(((libbind_ns_rr *)rr)->record);
    return PyInt_FromLong((long)ttl);
}

static char libbind_ns_rr_rdlen_doc[] =
"Returns the length of the record data in an ns_rr object";

static PyObject *
libbind_ns_rr_rdlen(PyObject *self, PyObject *args)
{
    PyObject *rr;
    u_int16_t length;

    PyTypeObject *argType;
    char         *argTypeStr;

    if( !PyArg_ParseTuple(args, "O", &rr) )
	return NULL;

    argType    = (PyTypeObject *)(rr->ob_type);
    argTypeStr = argType->tp_name;
    if( strcmp(argTypeStr, "Strangle.libbind.ns_rr") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_rr object");
	return NULL;
    }

    length = ns_rr_rdlen(((libbind_ns_rr *)rr)->record);
    return PyInt_FromLong((long)length);
}

static char libbind_ns_rr_rdata_doc[] =
"Returns a string representing the data in an ns_rr object";

static PyObject *
libbind_ns_rr_rdata(PyObject *self, PyObject *args)
{
    PyObject *rr;
    const u_char *rdata;
    u_int16_t length;

    PyTypeObject *argType;
    char         *argTypeStr;

    if( !PyArg_ParseTuple(args, "O", &rr) )
	return NULL;

    argType    = (PyTypeObject *)(rr->ob_type);
    argTypeStr = argType->tp_name;
    if( strcmp(argTypeStr, "Strangle.libbind.ns_rr") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_rr object");
	return NULL;
    }

    length = ns_rr_rdlen(((libbind_ns_rr *)rr)->record);
    rdata  = ns_rr_rdata(((libbind_ns_rr *)rr)->record);

    /* If the result is NULL it means there is no data in the record, so return None.
     * This seems to be happening implicitly from Py_BuildValue but we do it
     * anyway for clarity.
     */
    if( rdata == (const u_char *)NULL ) {
	Py_INCREF(Py_None);
	return Py_None;
    }

    return Py_BuildValue("s#", rdata, length);
}

static char libbind_ns_name_uncompress_doc[] =
"Returns a string of the uncompressed hostname from an ns_msg object.\n\
    \n\
    Only pass this function an ns_msg object and the ns_rr record which\n\
    has the data you want decompressed.";

static PyObject *
libbind_ns_name_uncompress(PyObject *self, PyObject *args)
{
    libbind_ns_msg *message;
    libbind_ns_rr  *rr;
    const u_char *msgStart, *msgEnd, *compressedName;
    char fullName[MAXDNAME + 1];
    int  length;

    PyTypeObject *argType;
    char         *argTypeStr;

    if( !PyArg_ParseTuple(args, "OO", (PyObject *)&message, (PyObject *)&rr) )
	return NULL;

    /* First argument must be an ns_msg. */
    argType    = (PyTypeObject *)(message->ob_type);
    argTypeStr = argType->tp_name;
    if( strcmp(argTypeStr, "Strangle.libbind.ns_msg") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_msg object");
	return NULL;
    }

    /* Second argument must be an ns_rr. */
    argType    = (PyTypeObject *)(rr->ob_type);
    argTypeStr = argType->tp_name;
    if( strcmp(argTypeStr, "Strangle.libbind.ns_rr") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_rr object");
	return NULL;
    }

    /* It would be nice to validate whether the ns_rr came from the ns_msg. */

    msgStart       = ns_msg_base(message->packet);
    msgEnd         = ns_msg_end(message->packet);
    compressedName = ns_rr_rdata(rr->record);

    /* If the data is an MX record, then we need to skip two bytes to get to the hostname. */
    if( ns_rr_type(rr->record) == ns_t_mx )
	compressedName += 2;

    bzero((void *)fullName, (size_t)(MAXDNAME + 1));
    length = ns_name_uncompress(msgStart, msgEnd, compressedName, fullName, MAXDNAME);
    if( length == -1 ) {
	PyErr_SetString(PyExc_TypeError, "BIND cannot decompress this name");
	return NULL;
    }

    return PyString_FromString(fullName);
}

static char libbind_ns_data_offset_doc[] =
"Returns the offset in the raw message that contains the record data";

static PyObject *
libbind_ns_data_offset(PyObject *self, PyObject *args)
{
    libbind_ns_msg *message;
    libbind_ns_rr  *rr;
    const u_char *msgStart, *dataLocation;
    long offset;

    PyTypeObject *argType;
    char         *argTypeStr;

    if( !PyArg_ParseTuple(args, "OO", (PyObject *)&message, (PyObject *)&rr) )
	return NULL;

    /* First argument must be an ns_msg. */
    argType    = (PyTypeObject *)(message->ob_type);
    argTypeStr = argType->tp_name;
    if( strcmp(argTypeStr, "Strangle.libbind.ns_msg") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_msg object");
	return NULL;
    }

    /* Second argument must be an ns_rr. */
    argType    = (PyTypeObject *)(rr->ob_type);
    argTypeStr = argType->tp_name;
    if( strcmp(argTypeStr, "Strangle.libbind.ns_rr") != 0 ) {
	PyErr_SetString(PyExc_TypeError, "Argument must be a ns_rr object");
	return NULL;
    }

    /* It would be nice to validate whether the ns_rr came from the ns_msg. */

    msgStart     = ns_msg_base(message->packet);
    dataLocation = ns_rr_rdata(rr->record);

    /* NULL data location means the record does not have data (e.g. for a query). */
    if( dataLocation == (const u_char *)NULL ) {
	Py_INCREF(Py_None);
	return Py_None;
    }

    offset = dataLocation - msgStart;
    return PyInt_FromLong(offset);
}

static PyMethodDef libbind_methods[] = {
    {"ns_msg_id"     , libbind_ns_msg_id     , METH_VARARGS, libbind_ns_msg_id_doc},
    {"ns_msg_getflag", libbind_ns_msg_getflag, METH_VARARGS, libbind_ns_msg_getflag_doc},
    {"ns_msg_count"  , libbind_ns_msg_count  , METH_VARARGS, libbind_ns_msg_count_doc},

    {"ns_rr_name"    , libbind_ns_rr_name    , METH_VARARGS, libbind_ns_rr_name_doc},
    {"ns_rr_type"    , libbind_ns_rr_type    , METH_VARARGS, libbind_ns_rr_type_doc},
    {"ns_rr_class"   , libbind_ns_rr_class   , METH_VARARGS, libbind_ns_rr_class_doc},
    {"ns_rr_ttl"     , libbind_ns_rr_ttl     , METH_VARARGS, libbind_ns_rr_ttl_doc},
    {"ns_rr_rdlen"   , libbind_ns_rr_rdlen   , METH_VARARGS, libbind_ns_rr_rdlen_doc},
    {"ns_rr_rdata"   , libbind_ns_rr_rdata   , METH_VARARGS, libbind_ns_rr_rdata_doc},

    {"ns_name_uncompress", libbind_ns_name_uncompress, METH_VARARGS, libbind_ns_name_uncompress_doc},

    {"ns_data_offset", libbind_ns_data_offset, METH_VARARGS, libbind_ns_data_offset_doc},
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

    libbind_ns_rrType.tp_new = PyType_GenericNew;
    if( PyType_Ready(&libbind_ns_rrType) < 0 )
	return;

    m = Py_InitModule3("Strangle.libbind", libbind_methods, libbind_doc);

    if( m == NULL )
	return;

    Py_INCREF(&libbind_ns_msgType);
    PyModule_AddObject(m, "ns_msg", (PyObject *)&libbind_ns_msgType);

    Py_INCREF(&libbind_ns_rrType);
    PyModule_AddObject(m, "ns_rr" , (PyObject *)&libbind_ns_rrType);

    /* These are the ns_flag enums.  We just use Python ints. */
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

    /* These are the ns_sect enums.  We just use Python ints. */
    PyModule_AddObject(m, "ns_s_qd", PyInt_FromLong(ns_s_qd));
    PyModule_AddObject(m, "ns_s_zn", PyInt_FromLong(ns_s_zn));
    PyModule_AddObject(m, "ns_s_an", PyInt_FromLong(ns_s_an));
    PyModule_AddObject(m, "ns_s_pr", PyInt_FromLong(ns_s_pr));
    PyModule_AddObject(m, "ns_s_ns", PyInt_FromLong(ns_s_ns));
    PyModule_AddObject(m, "ns_s_ud", PyInt_FromLong(ns_s_ud));
    PyModule_AddObject(m, "ns_s_ar", PyInt_FromLong(ns_s_ar));

    /* These are the allowed record types. */
    PyModule_AddObject(m, "ns_t_invalid", PyInt_FromLong(ns_t_invalid));
    PyModule_AddObject(m, "ns_t_a", PyInt_FromLong(ns_t_a));
    PyModule_AddObject(m, "ns_t_ns", PyInt_FromLong(ns_t_ns));
    PyModule_AddObject(m, "ns_t_md", PyInt_FromLong(ns_t_md));
    PyModule_AddObject(m, "ns_t_mf", PyInt_FromLong(ns_t_mf));
    PyModule_AddObject(m, "ns_t_cname", PyInt_FromLong(ns_t_cname));
    PyModule_AddObject(m, "ns_t_soa", PyInt_FromLong(ns_t_soa));
    PyModule_AddObject(m, "ns_t_mb", PyInt_FromLong(ns_t_mb));
    PyModule_AddObject(m, "ns_t_mg", PyInt_FromLong(ns_t_mg));
    PyModule_AddObject(m, "ns_t_mr", PyInt_FromLong(ns_t_mr));
    PyModule_AddObject(m, "ns_t_null", PyInt_FromLong(ns_t_null));
    PyModule_AddObject(m, "ns_t_wks", PyInt_FromLong(ns_t_wks));
    PyModule_AddObject(m, "ns_t_ptr", PyInt_FromLong(ns_t_ptr));
    PyModule_AddObject(m, "ns_t_hinfo", PyInt_FromLong(ns_t_hinfo));
    PyModule_AddObject(m, "ns_t_minfo", PyInt_FromLong(ns_t_minfo));
    PyModule_AddObject(m, "ns_t_mx", PyInt_FromLong(ns_t_mx));
    PyModule_AddObject(m, "ns_t_txt", PyInt_FromLong(ns_t_txt));
    PyModule_AddObject(m, "ns_t_rp", PyInt_FromLong(ns_t_rp));
    PyModule_AddObject(m, "ns_t_afsdb", PyInt_FromLong(ns_t_afsdb));
    PyModule_AddObject(m, "ns_t_x25", PyInt_FromLong(ns_t_x25));
    PyModule_AddObject(m, "ns_t_isdn", PyInt_FromLong(ns_t_isdn));
    PyModule_AddObject(m, "ns_t_rt", PyInt_FromLong(ns_t_rt));
    PyModule_AddObject(m, "ns_t_nsap", PyInt_FromLong(ns_t_nsap));
    PyModule_AddObject(m, "ns_t_nsap_ptr", PyInt_FromLong(ns_t_nsap_ptr));
    PyModule_AddObject(m, "ns_t_sig", PyInt_FromLong(ns_t_sig));
    PyModule_AddObject(m, "ns_t_key", PyInt_FromLong(ns_t_key));
    PyModule_AddObject(m, "ns_t_px", PyInt_FromLong(ns_t_px));
    PyModule_AddObject(m, "ns_t_gpos", PyInt_FromLong(ns_t_gpos));
    PyModule_AddObject(m, "ns_t_aaaa", PyInt_FromLong(ns_t_aaaa));
    PyModule_AddObject(m, "ns_t_loc", PyInt_FromLong(ns_t_loc));
    PyModule_AddObject(m, "ns_t_nxt", PyInt_FromLong(ns_t_nxt));
    PyModule_AddObject(m, "ns_t_eid", PyInt_FromLong(ns_t_eid));
    PyModule_AddObject(m, "ns_t_nimloc", PyInt_FromLong(ns_t_nimloc));
    PyModule_AddObject(m, "ns_t_srv", PyInt_FromLong(ns_t_srv));
    PyModule_AddObject(m, "ns_t_atma", PyInt_FromLong(ns_t_atma));
    PyModule_AddObject(m, "ns_t_naptr", PyInt_FromLong(ns_t_naptr));
    PyModule_AddObject(m, "ns_t_kx", PyInt_FromLong(ns_t_kx));
    PyModule_AddObject(m, "ns_t_cert", PyInt_FromLong(ns_t_cert));
    PyModule_AddObject(m, "ns_t_a6", PyInt_FromLong(ns_t_a6));
    PyModule_AddObject(m, "ns_t_dname", PyInt_FromLong(ns_t_dname));
    PyModule_AddObject(m, "ns_t_sink", PyInt_FromLong(ns_t_sink));
    PyModule_AddObject(m, "ns_t_opt", PyInt_FromLong(ns_t_opt));
    //PyModule_AddObject(m, "ns_t_apl", PyInt_FromLong(ns_t_apl));	/* (These two have no C symbol even       */
    //PyModule_AddObject(m, "ns_t_tkey", PyInt_FromLong(ns_t_tkey));	/*  though I got this code from nameser.h */
    PyModule_AddObject(m, "ns_t_tsig", PyInt_FromLong(ns_t_tsig));
    PyModule_AddObject(m, "ns_t_ixfr", PyInt_FromLong(ns_t_ixfr));
    PyModule_AddObject(m, "ns_t_axfr", PyInt_FromLong(ns_t_axfr));
    PyModule_AddObject(m, "ns_t_mailb", PyInt_FromLong(ns_t_mailb));
    PyModule_AddObject(m, "ns_t_maila", PyInt_FromLong(ns_t_maila));
    PyModule_AddObject(m, "ns_t_any", PyInt_FromLong(ns_t_any));
    PyModule_AddObject(m, "ns_t_zxfr", PyInt_FromLong(ns_t_zxfr));
    PyModule_AddObject(m, "ns_t_max", PyInt_FromLong(ns_t_max));

    /* These are the ns_class enums.  We just use Python ints. */
    PyModule_AddObject(m, "ns_c_invalid", PyInt_FromLong(ns_c_invalid));
    PyModule_AddObject(m, "ns_c_in", PyInt_FromLong(ns_c_in));
    PyModule_AddObject(m, "ns_c_2", PyInt_FromLong(ns_c_2));
    PyModule_AddObject(m, "ns_c_chaos", PyInt_FromLong(ns_c_chaos));
    PyModule_AddObject(m, "ns_c_hs", PyInt_FromLong(ns_c_hs));
    PyModule_AddObject(m, "ns_c_none", PyInt_FromLong(ns_c_none));
    PyModule_AddObject(m, "ns_c_any", PyInt_FromLong(ns_c_any));
    PyModule_AddObject(m, "ns_c_max", PyInt_FromLong(ns_c_max));
}

// vim: sts=4 sw=4 noet
