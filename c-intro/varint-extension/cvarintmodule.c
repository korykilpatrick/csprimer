#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *cvarint_encode(PyObject *self, PyObject *args) {
    unsigned int i;
    unsigned long long n;
    char part, out[10]; // 10 byte max encoding

    if (!PyArg_ParseTuple(args, "K", &n))
        return NULL;
        
    i = 0;
    while (n > 0) {
        part = n & 0x7f;
        n >>= 7;
        if (n > 0) part |= 0x80;
        out[i++] = part;
    }
    return PyBytes_FromStringAndSize(out, i);
}

static PyObject *cvarint_decode(PyObject *self, PyObject *args) {
    Py_buffer buf;
    if (!PyArg_ParseTuple(args, "y*", &buf))
        return NULL;
    
    char * varn = buf.buf;
    short num_bytes = buf.len;
    
    short b;
    unsigned long long n = 0;
    for (b = num_bytes; b >= 0; b--) {
        n <<= 7;
        n |= (varn[b] & 0x7f);
    }
    return PyLong_FromUnsignedLongLong(n);
}

static PyMethodDef CVarintMethods[] = {
    {"encode", cvarint_encode, METH_VARARGS, "Encode an integer as varint."},
    {"decode", cvarint_decode, METH_VARARGS,
     "Decode varint bytes to an integer."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef cvarintmodule = {
    PyModuleDef_HEAD_INIT, "cvarint",
    "A C implementation of protobuf varint encoding", -1, CVarintMethods};

PyMODINIT_FUNC PyInit_cvarint(void) { return PyModule_Create(&cvarintmodule); }
