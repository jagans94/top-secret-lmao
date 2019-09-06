# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Library of dtypes (Tensor element types).
NOTE: Adapted from TensorFlow library.
"""

import numpy as np
from six.moves import builtins

from tensorflow.core.framework import types_pb2
# from tensorflow.python import pywrap_tensorflow

# Comment out _np_bfloat16 
# Can't seem to backtrack the definition in pywrap_tensorflow
# _np_bfloat16 = pywrap_tensorflow.TF_bfloat16_type()


class DType(object):
    """Represents the type of the elements in a `Tensor`.
    """
    def __init__(self, type_enum):
        """Creates a new `DataType`.
        """
        type_enum = int(type_enum)
        if (type_enum not in types_pb2.DataType.values() or
            type_enum == types_pb2.DT_INVALID):
            raise TypeError("type_enum is not a valid types_pb2.DataType: %s" %
                        type_enum)
        self._type_enum = type_enum

    @property
    def _is_ref_dtype(self):
        """Returns `True` if this `DType` represents a reference type."""
        return self._type_enum > 100

    @property
    def base_dtype(self):
        """Returns a non-reference `DType` based on this `DType`."""
        if self._is_ref_dtype:
            return _INTERN_TABLE[self._type_enum - 100]
        else:
            return self

    @property
    def is_numpy_compatible(self):
        return self._type_enum not in _NUMPY_INCOMPATIBLE

    @property
    def as_numpy_dtype(self):
        """Returns a `numpy.dtype` based on this `DType`."""
        return _TF_TO_NP[self._type_enum]

    @property
    def as_datatype_enum(self):
        """Returns a `types_pb2.DataType` enum value based on this `DType`."""
        return self._type_enum


# Define data type range of numpy dtype
# For documentation purpose
dtype_range = {
    np.bool_: (False, True),
    np.bool8: (False, True),
    np.uint8: (0, 255),
    np.uint16: (0, 65535),
    np.int8: (-128, 127),
    np.int16: (-32768, 32767),
    np.int64: (-2**63, 2**63 - 1),
    np.uint64: (0, 2**64 - 1),
    np.int32: (-2**31, 2**31 - 1),
    np.uint32: (0, 2**32 - 1),
    np.float32: (-1, 1),
    np.float64: (-1, 1)
}

# Define standard wrappers for the types_pb2.DataType enum.
resource = DType(types_pb2.DT_RESOURCE)
variant = DType(types_pb2.DT_VARIANT)
float16 = DType(types_pb2.DT_HALF)
half = float16
float32 = DType(types_pb2.DT_FLOAT)
float64 = DType(types_pb2.DT_DOUBLE)
double = float64
int32 = DType(types_pb2.DT_INT32)
uint8 = DType(types_pb2.DT_UINT8)
uint16 = DType(types_pb2.DT_UINT16)
uint32 = DType(types_pb2.DT_UINT32)
uint64 = DType(types_pb2.DT_UINT64)
int16 = DType(types_pb2.DT_INT16)
int8 = DType(types_pb2.DT_INT8)
string = DType(types_pb2.DT_STRING)
complex64 = DType(types_pb2.DT_COMPLEX64)
complex128 = DType(types_pb2.DT_COMPLEX128)
int64 = DType(types_pb2.DT_INT64)
bool = DType(types_pb2.DT_BOOL)  # pylint: disable=redefined-builtin
qint8 = DType(types_pb2.DT_QINT8)
quint8 = DType(types_pb2.DT_QUINT8)
qint16 = DType(types_pb2.DT_QINT16)
quint16 = DType(types_pb2.DT_QUINT16)
qint32 = DType(types_pb2.DT_QINT32)
resource_ref = DType(types_pb2.DT_RESOURCE_REF)
variant_ref = DType(types_pb2.DT_VARIANT_REF)
# bfloat16 = DType(types_pb2.DT_BFLOAT16)
float16_ref = DType(types_pb2.DT_HALF_REF)
half_ref = float16_ref
float32_ref = DType(types_pb2.DT_FLOAT_REF)
float64_ref = DType(types_pb2.DT_DOUBLE_REF)
double_ref = float64_ref
int32_ref = DType(types_pb2.DT_INT32_REF)
uint32_ref = DType(types_pb2.DT_UINT32_REF)
uint8_ref = DType(types_pb2.DT_UINT8_REF)
uint16_ref = DType(types_pb2.DT_UINT16_REF)
int16_ref = DType(types_pb2.DT_INT16_REF)
int8_ref = DType(types_pb2.DT_INT8_REF)
string_ref = DType(types_pb2.DT_STRING_REF)
complex64_ref = DType(types_pb2.DT_COMPLEX64_REF)
complex128_ref = DType(types_pb2.DT_COMPLEX128_REF)
int64_ref = DType(types_pb2.DT_INT64_REF)
uint64_ref = DType(types_pb2.DT_UINT64_REF)
bool_ref = DType(types_pb2.DT_BOOL_REF)
qint8_ref = DType(types_pb2.DT_QINT8_REF)
quint8_ref = DType(types_pb2.DT_QUINT8_REF)
qint16_ref = DType(types_pb2.DT_QINT16_REF)
quint16_ref = DType(types_pb2.DT_QUINT16_REF)
qint32_ref = DType(types_pb2.DT_QINT32_REF)
# bfloat16_ref = DType(types_pb2.DT_BFLOAT16_REF)

_NUMPY_INCOMPATIBLE = frozenset([
    types_pb2.DT_VARIANT, types_pb2.DT_VARIANT_REF, types_pb2.DT_RESOURCE,
    types_pb2.DT_RESOURCE_REF
])

# Maintain an intern table so that we don't have to create a large
# number of small objects.
_INTERN_TABLE = {
    types_pb2.DT_HALF: float16,
    types_pb2.DT_FLOAT: float32,
    types_pb2.DT_DOUBLE: float64,
    types_pb2.DT_INT32: int32,
    types_pb2.DT_UINT8: uint8,
    types_pb2.DT_UINT16: uint16,
    types_pb2.DT_UINT32: uint32,
    types_pb2.DT_UINT64: uint64,
    types_pb2.DT_INT16: int16,
    types_pb2.DT_INT8: int8,
    types_pb2.DT_STRING: string,
    types_pb2.DT_COMPLEX64: complex64,
    types_pb2.DT_COMPLEX128: complex128,
    types_pb2.DT_INT64: int64,
    types_pb2.DT_BOOL: bool,
    types_pb2.DT_QINT8: qint8,
    types_pb2.DT_QUINT8: quint8,
    types_pb2.DT_QINT16: qint16,
    types_pb2.DT_QUINT16: quint16,
    types_pb2.DT_QINT32: qint32,
    #types_pb2.DT_BFLOAT16: bfloat16,
    types_pb2.DT_RESOURCE: resource,
    types_pb2.DT_VARIANT: variant,
    types_pb2.DT_HALF_REF: float16_ref,
    types_pb2.DT_FLOAT_REF: float32_ref,
    types_pb2.DT_DOUBLE_REF: float64_ref,
    types_pb2.DT_INT32_REF: int32_ref,
    types_pb2.DT_UINT32_REF: uint32_ref,
    types_pb2.DT_UINT8_REF: uint8_ref,
    types_pb2.DT_UINT16_REF: uint16_ref,
    types_pb2.DT_INT16_REF: int16_ref,
    types_pb2.DT_INT8_REF: int8_ref,
    types_pb2.DT_STRING_REF: string_ref,
    types_pb2.DT_COMPLEX64_REF: complex64_ref,
    types_pb2.DT_COMPLEX128_REF: complex128_ref,
    types_pb2.DT_INT64_REF: int64_ref,
    types_pb2.DT_UINT64_REF: uint64_ref,
    types_pb2.DT_BOOL_REF: bool_ref,
    types_pb2.DT_QINT8_REF: qint8_ref,
    types_pb2.DT_QUINT8_REF: quint8_ref,
    types_pb2.DT_QINT16_REF: qint16_ref,
    types_pb2.DT_QUINT16_REF: quint16_ref,
    types_pb2.DT_QINT32_REF: qint32_ref,
    # types_pb2.DT_BFLOAT16_REF: bfloat16_ref,
    types_pb2.DT_RESOURCE_REF: resource_ref,
    types_pb2.DT_VARIANT_REF: variant_ref,
}

# Standard mappings between types_pb2.DataType values and string names.
_TYPE_TO_STRING = {
    types_pb2.DT_HALF: "float16",
    types_pb2.DT_FLOAT: "float32",
    types_pb2.DT_DOUBLE: "float64",
    types_pb2.DT_INT32: "int32",
    types_pb2.DT_UINT8: "uint8",
    types_pb2.DT_UINT16: "uint16",
    types_pb2.DT_UINT32: "uint32",
    types_pb2.DT_UINT64: "uint64",
    types_pb2.DT_INT16: "int16",
    types_pb2.DT_INT8: "int8",
    types_pb2.DT_STRING: "string",
    types_pb2.DT_COMPLEX64: "complex64",
    types_pb2.DT_COMPLEX128: "complex128",
    types_pb2.DT_INT64: "int64",
    types_pb2.DT_BOOL: "bool",
    types_pb2.DT_QINT8: "qint8",
    types_pb2.DT_QUINT8: "quint8",
    types_pb2.DT_QINT16: "qint16",
    types_pb2.DT_QUINT16: "quint16",
    types_pb2.DT_QINT32: "qint32",
    # types_pb2.DT_BFLOAT16: "bfloat16",
    types_pb2.DT_RESOURCE: "resource",
    types_pb2.DT_VARIANT: "variant",
    types_pb2.DT_HALF_REF: "float16_ref",
    types_pb2.DT_FLOAT_REF: "float32_ref",
    types_pb2.DT_DOUBLE_REF: "float64_ref",
    types_pb2.DT_INT32_REF: "int32_ref",
    types_pb2.DT_UINT32_REF: "uint32_ref",
    types_pb2.DT_UINT8_REF: "uint8_ref",
    types_pb2.DT_UINT16_REF: "uint16_ref",
    types_pb2.DT_INT16_REF: "int16_ref",
    types_pb2.DT_INT8_REF: "int8_ref",
    types_pb2.DT_STRING_REF: "string_ref",
    types_pb2.DT_COMPLEX64_REF: "complex64_ref",
    types_pb2.DT_COMPLEX128_REF: "complex128_ref",
    types_pb2.DT_INT64_REF: "int64_ref",
    types_pb2.DT_UINT64_REF: "uint64_ref",
    types_pb2.DT_BOOL_REF: "bool_ref",
    types_pb2.DT_QINT8_REF: "qint8_ref",
    types_pb2.DT_QUINT8_REF: "quint8_ref",
    types_pb2.DT_QINT16_REF: "qint16_ref",
    types_pb2.DT_QUINT16_REF: "quint16_ref",
    types_pb2.DT_QINT32_REF: "qint32_ref",
    # types_pb2.DT_BFLOAT16_REF: "bfloat16_ref",
    types_pb2.DT_RESOURCE_REF: "resource_ref",
    types_pb2.DT_VARIANT_REF: "variant_ref",
}
_STRING_TO_TF = {
    value: _INTERN_TABLE[key] for key, value in _TYPE_TO_STRING.items()
}
# Add non-canonical aliases.
_STRING_TO_TF["half"] = float16
_STRING_TO_TF["half_ref"] = float16_ref
_STRING_TO_TF["float"] = float32
_STRING_TO_TF["float_ref"] = float32_ref
_STRING_TO_TF["double"] = float64
_STRING_TO_TF["double_ref"] = float64_ref

# Numpy representation for quantized dtypes.
#
# These are magic strings that are used in the swig wrapper to identify
# quantized types.
# TODO(mrry,keveman): Investigate Numpy type registration to replace this
# hard-coding of names.
_np_qint8 = np.dtype([("qint8", np.int8)])
_np_quint8 = np.dtype([("quint8", np.uint8)])
_np_qint16 = np.dtype([("qint16", np.int16)])
_np_quint16 = np.dtype([("quint16", np.uint16)])
_np_qint32 = np.dtype([("qint32", np.int32)])

# _np_bfloat16 is defined by a module import.

# Custom struct dtype for directly-fed ResourceHandles of supported type(s).
np_resource = np.dtype([("resource", np.ubyte)])

# Standard mappings between types_pb2.DataType values and numpy.dtypes.
_NP_TO_TF = {
    np.float16: float16,
    np.float32: float32,
    np.float64: float64,
    np.int32: int32,
    np.int64: int64,
    np.uint8: uint8,
    np.uint16: uint16,
    np.uint32: uint32,
    np.uint64: uint64,
    np.int16: int16,
    np.int8: int8,
    np.complex64: complex64,
    np.complex128: complex128,
    np.object_: string,
    np.string_: string,
    np.unicode_: string,
    np.bool_: bool,
    _np_qint8: qint8,
    _np_quint8: quint8,
    _np_qint16: qint16,
    _np_quint16: quint16,
    _np_qint32: qint32,
    # _np_bfloat16: bfloat16,
}

# Map (some) NumPy platform dtypes to TF ones using their fixed-width
# synonyms. Note that platform dtypes are not always simples aliases,
# i.e. reference equality is not guaranteed. See e.g. numpy/numpy#9799.
for pdt in [
    np.intc,
    np.uintc,
    np.int_,
    np.uint,
    np.longlong,
    np.ulonglong,
]:
  if pdt not in _NP_TO_TF:
    _NP_TO_TF[pdt] = next(
        _NP_TO_TF[dt] for dt in _NP_TO_TF if dt == pdt().dtype)


TF_VALUE_DTYPES = set(_NP_TO_TF.values())


_TF_TO_NP = {
    types_pb2.DT_HALF:
        np.float16,
    types_pb2.DT_FLOAT:
        np.float32,
    types_pb2.DT_DOUBLE:
        np.float64,
    types_pb2.DT_INT32:
        np.int32,
    types_pb2.DT_UINT8:
        np.uint8,
    types_pb2.DT_UINT16:
        np.uint16,
    types_pb2.DT_UINT32:
        np.uint32,
    types_pb2.DT_UINT64:
        np.uint64,
    types_pb2.DT_INT16:
        np.int16,
    types_pb2.DT_INT8:
        np.int8,
    # NOTE(touts): For strings we use np.object as it supports variable length
    # strings.
    types_pb2.DT_STRING:
        np.object,
    types_pb2.DT_COMPLEX64:
        np.complex64,
    types_pb2.DT_COMPLEX128:
        np.complex128,
    types_pb2.DT_INT64:
        np.int64,
    types_pb2.DT_BOOL:
        np.bool,
    types_pb2.DT_QINT8:
        _np_qint8,
    types_pb2.DT_QUINT8:
        _np_quint8,
    types_pb2.DT_QINT16:
        _np_qint16,
    types_pb2.DT_QUINT16:
        _np_quint16,
    types_pb2.DT_QINT32:
        _np_qint32,
    # types_pb2.DT_BFLOAT16:
        # _np_bfloat16,

    # Ref types
    types_pb2.DT_HALF_REF:
        np.float16,
    types_pb2.DT_FLOAT_REF:
        np.float32,
    types_pb2.DT_DOUBLE_REF:
        np.float64,
    types_pb2.DT_INT32_REF:
        np.int32,
    types_pb2.DT_UINT32_REF:
        np.uint32,
    types_pb2.DT_UINT8_REF:
        np.uint8,
    types_pb2.DT_UINT16_REF:
        np.uint16,
    types_pb2.DT_INT16_REF:
        np.int16,
    types_pb2.DT_INT8_REF:
        np.int8,
    types_pb2.DT_STRING_REF:
        np.object,
    types_pb2.DT_COMPLEX64_REF:
        np.complex64,
    types_pb2.DT_COMPLEX128_REF:
        np.complex128,
    types_pb2.DT_INT64_REF:
        np.int64,
    types_pb2.DT_UINT64_REF:
        np.uint64,
    types_pb2.DT_BOOL_REF:
        np.bool,
    types_pb2.DT_QINT8_REF:
        _np_qint8,
    types_pb2.DT_QUINT8_REF:
        _np_quint8,
    types_pb2.DT_QINT16_REF:
        _np_qint16,
    types_pb2.DT_QUINT16_REF:
        _np_quint16,
    types_pb2.DT_QINT32_REF:
        _np_qint32,
    # types_pb2.DT_BFLOAT16_REF:
        # _np_bfloat16,
}

_QUANTIZED_DTYPES_NO_REF = frozenset([qint8, quint8, qint16, quint16, qint32])
_QUANTIZED_DTYPES_REF = frozenset(
    [qint8_ref, quint8_ref, qint16_ref, quint16_ref, qint32_ref])
QUANTIZED_DTYPES = _QUANTIZED_DTYPES_REF.union(_QUANTIZED_DTYPES_NO_REF)

_PYTHON_TO_TF = {
    builtins.float: float32,
    builtins.bool: bool,
    builtins.object: string
}

_ANY_TO_TF = {}
_ANY_TO_TF.update(_INTERN_TABLE)
_ANY_TO_TF.update(_STRING_TO_TF)
_ANY_TO_TF.update(_PYTHON_TO_TF)
_ANY_TO_TF.update(_NP_TO_TF)

# Ensure no collisions.
assert len(_ANY_TO_TF) == sum(
    len(d) for d in [_INTERN_TABLE, _STRING_TO_TF, _PYTHON_TO_TF, _NP_TO_TF])


def as_dtype(type_value):
  """Converts the given `type_value` to a `DType`.
  """
  if isinstance(type_value, DType):
    return type_value

  if isinstance(type_value, np.dtype):
    try:
      return _NP_TO_TF[type_value.type]
    except KeyError:
      pass

  try:
    return _ANY_TO_TF[type_value]
  except KeyError:
    pass

  raise TypeError("Cannot convert value %r to a TensorFlow DType." %
                  (type_value,))