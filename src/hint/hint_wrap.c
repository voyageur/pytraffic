/*
 * hint_wrap.c - Python 3 C extension wrapper for the _hint module.
 *
 * Replaces the original SWIG 1.1 (Python 2) generated wrapper with a
 * hand-written Python 3 module definition.  The interface is simple:
 * all exported functions take only int arguments and return int or None.
 *
 * Error handling: internal C code calls hint_set_error() instead of
 * exit() to signal a fatal condition.  Each wrapper checks
 * hint_error_pending() after calling into C and raises RuntimeError.
 */

#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "gtlevel.h"

/* -----------------------------------------------------------------------
 * Module-level error flag.  Set by hint_set_error(); cleared on each
 * new wrapper entry so that a single failed call does not poison later
 * calls (though in practice the caller is expected to propagate the
 * exception and not continue).
 * --------------------------------------------------------------------- */

static int   _hint_error = 0;
static char  _hint_error_msg[512] = {0};

void hint_set_error(const char *msg)
{
    _hint_error = 1;
    if (msg) {
        /* truncating copy — buffer is 512 bytes */
        strncpy(_hint_error_msg, msg, sizeof(_hint_error_msg) - 1);
        _hint_error_msg[sizeof(_hint_error_msg) - 1] = '\0';
    } else {
        _hint_error_msg[0] = '\0';
    }
}

int hint_error_pending(void)
{
    return _hint_error;
}

const char *hint_error_msg(void)
{
    return _hint_error_msg;
}

/* Convenience macro: check the error flag and raise RuntimeError. */
#define CHECK_HINT_ERROR(retval)                                \
    do {                                                        \
        if (_hint_error) {                                      \
            _hint_error = 0;                                    \
            PyErr_SetString(PyExc_RuntimeError, _hint_error_msg); \
            return (retval);                                    \
        }                                                       \
    } while (0)

extern void bestmove(int, int);
extern void init(void);
extern int  getbestmoverows(void);
extern int  getbestmovecolumns(void);
extern void findlevel(int, int);
extern int  getbestyoucando(void);
extern int  getpackedrows(void);
extern int  getpackedcolumns(void);

static PyObject *_wrap_bestmove(PyObject *self, PyObject *args)
{
    int arg0, arg1;
    if (!PyArg_ParseTuple(args, "ii:bestmove", &arg0, &arg1))
        return NULL;
    _hint_error = 0;
    bestmove(arg0, arg1);
    CHECK_HINT_ERROR(NULL);
    Py_RETURN_NONE;
}

static PyObject *_wrap_init(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ":init"))
        return NULL;
    _hint_error = 0;
    init();
    CHECK_HINT_ERROR(NULL);
    Py_RETURN_NONE;
}

static PyObject *_wrap_getbestmoverows(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ":getbestmoverows"))
        return NULL;
    return PyLong_FromLong(getbestmoverows());
}

static PyObject *_wrap_getbestmovecolumns(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ":getbestmovecolumns"))
        return NULL;
    return PyLong_FromLong(getbestmovecolumns());
}

static PyObject *_wrap_findlevel(PyObject *self, PyObject *args)
{
    int arg0, arg1;
    if (!PyArg_ParseTuple(args, "ii:findlevel", &arg0, &arg1))
        return NULL;
    _hint_error = 0;
    findlevel(arg0, arg1);
    CHECK_HINT_ERROR(NULL);
    Py_RETURN_NONE;
}

static PyObject *_wrap_getbestyoucando(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ":getbestyoucando"))
        return NULL;
    return PyLong_FromLong(getbestyoucando());
}

static PyObject *_wrap_getpackedrows(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ":getpackedrows"))
        return NULL;
    return PyLong_FromLong(getpackedrows());
}

static PyObject *_wrap_getpackedcolumns(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ":getpackedcolumns"))
        return NULL;
    return PyLong_FromLong(getpackedcolumns());
}

static PyMethodDef _hintMethods[] = {
    { "bestmove",           _wrap_bestmove,           METH_VARARGS, "bestmove(rows, cols)" },
    { "init",               _wrap_init,               METH_VARARGS, "init()" },
    { "getbestmoverows",    _wrap_getbestmoverows,    METH_VARARGS, "getbestmoverows() -> int" },
    { "getbestmovecolumns", _wrap_getbestmovecolumns, METH_VARARGS, "getbestmovecolumns() -> int" },
    { "findlevel",          _wrap_findlevel,          METH_VARARGS, "findlevel(start, end)" },
    { "getbestyoucando",    _wrap_getbestyoucando,    METH_VARARGS, "getbestyoucando() -> int" },
    { "getpackedrows",      _wrap_getpackedrows,      METH_VARARGS, "getpackedrows() -> int" },
    { "getpackedcolumns",   _wrap_getpackedcolumns,   METH_VARARGS, "getpackedcolumns() -> int" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef _hintmodule = {
    PyModuleDef_HEAD_INIT,
    "_hint",  /* module name */
    NULL,     /* module docstring */
    -1,       /* per-interpreter state size */
    _hintMethods
};

PyMODINIT_FUNC
PyInit__hint(void)
{
    return PyModule_Create(&_hintmodule);
}
