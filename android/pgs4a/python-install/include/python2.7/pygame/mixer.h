/*
    pygame - Python Game Library
    Copyright (C) 2000-2001  Pete Shinners

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public
    License as published by the Free Software Foundation; either
    version 2 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Library General Public License for more details.

    You should have received a copy of the GNU Library General Public
    License along with this library; if not, write to the Free
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

    Pete Shinners
    pete@shinners.org
*/

#include <Python.h>
#include <SDL_mixer.h>
#include <structmember.h>


/* test mixer initializations */
#define MIXER_INIT_CHECK() \
	if(!SDL_WasInit(SDL_INIT_AUDIO)) \
		return RAISE(PyExc_SDLError, "mixer system not initialized")



#define PYGAMEAPI_MIXER_NUMSLOTS 7
typedef struct {
  PyObject_HEAD
  Mix_Chunk* chunk;
  PyObject *weakreflist;
} PySoundObject;
typedef struct {
  PyObject_HEAD
  int chan;
} PyChannelObject;
#define PySound_AsChunk(x) (((PySoundObject*)x)->chunk)
#define PyChannel_AsInt(x) (((PyChannelObject*)x)->chan)
#ifndef PYGAMEAPI_MIXER_INTERNAL
#define PySound_Check(x) ((x)->ob_type == (PyTypeObject*)PyMIXER_C_API[0])
#define PySound_Type (*(PyTypeObject*)PyMIXER_C_API[0])
#define PySound_New (*(PyObject*(*)(Mix_Chunk*))PyMIXER_C_API[1])
#define PySound_Play (*(PyObject*(*)(PyObject*, PyObject*))PyMIXER_C_API[2])
#define PyChannel_Check(x) ((x)->ob_type == (PyTypeObject*)PyMIXER_C_API[3])
#define PyChannel_Type (*(PyTypeObject*)PyMIXER_C_API[3])
#define PyChannel_New (*(PyObject*(*)(int))PyMIXER_C_API[4])
#define PyMixer_AutoInit (*(PyObject*(*)(PyObject*, PyObject*))PyMIXER_C_API[5])
#define PyMixer_AutoQuit (*(void(*)(void))PyMIXER_C_API[6])
#define import_pygame_mixer() { \
	PyObject *_module = PyImport_ImportModule(IMPPREFIX "mixer"); \
	if (_module != NULL) { \
		PyObject *_dict = PyModule_GetDict(_module); \
		PyObject *_c_api = PyDict_GetItemString(_dict, PYGAMEAPI_LOCAL_ENTRY); \
		if(PyCObject_Check(_c_api)) {\
			void** localptr = (void**)PyCObject_AsVoidPtr(_c_api); \
			memcpy(PyMIXER_C_API, localptr, sizeof(void*)*PYGAMEAPI_MIXER_NUMSLOTS); \
} Py_DECREF(_module); } }
#endif



static void* PyMIXER_C_API[PYGAMEAPI_MIXER_NUMSLOTS] = {NULL};
