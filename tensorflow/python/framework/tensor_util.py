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
"""Utilities to create TensorProtos.
NOTE: Adapted from TensorFlow library.
"""

import numpy as np

from tensorflow.core.framework import tensor_pb2
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import tensor_shape

_TENSOR_CONTENT_TYPES = frozenset([
	dtypes.float32, dtypes.float64, dtypes.int32, dtypes.uint8, dtypes.int16,
	dtypes.int8, dtypes.int64, dtypes.qint8, dtypes.quint8, dtypes.qint16,
	dtypes.quint16, dtypes.qint32, dtypes.uint32, dtypes.uint64
])

def MakeTensorProto(values, dtype=None):
	"""Expects only np.ndarrya object or tensor_proto as inputs."""
	
	if isinstance(values, tensor_pb2.TensorProto):
		return values
	if not isinstance(values, (np.ndarray, np.generic)):
		raise ValueError('`values` expected to be of type %s but is of type %s'% (np.ndarray, type(values)))

	if dtype:
		dtype = dtypes.as_dtype(dtype)

	is_quantized = (
		dtype in [
			dtypes.qint8, dtypes.quint8, dtypes.qint16, dtypes.quint16,
			dtypes.qint32
		])

	# Convert nparray.dtype to a compatible DType instance; otherwise doesn't force it
	if dtype and dtype.is_numpy_compatible:
		nparray = values.astype(dtype.as_numpy_dtype)
	else:
		nparray = values

	# python/numpy default float type is float64. We prefer float32 instead.
	if (nparray.dtype == np.float64) and dtype is None:
		nparray = nparray.astype(np.float32)
	# python/numpy default int type is int64. We prefer int32 instead.
	elif (nparray.dtype == np.int64) and dtype is None:
		downcasted_array = nparray.astype(np.int32)
		# Do not down cast if it leads to precision loss.
		if np.array_equal(downcasted_array, nparray):
			nparray = downcasted_array

	# If dtype is provided, it must be compatible with what numpy
	# conversion says.
	numpy_dtype = dtypes.as_dtype(nparray.dtype)
	if numpy_dtype is None:
		raise TypeError("Unrecognized data type: %s" % nparray.dtype)

	# If dtype was specified and is a quantized type, we convert
	# numpy_dtype back into the quantized version.
	if is_quantized:
		numpy_dtype = dtype

	if dtype is not None:
		if not hasattr(dtype, "base_dtype") or dtype.base_dtype != numpy_dtype.base_dtype:
			raise TypeError("Incompatible types: %s vs. %s. Value is %s" %
							(dtype, nparray.dtype, values))

	# Get the shape from the numpy array.
	shape = nparray.shape

	# Set dtype and shape for `tensor_proto`
	tensor_proto = tensor_pb2.TensorProto(
		dtype=numpy_dtype.as_datatype_enum,
		tensor_shape=tensor_shape.as_shape(shape).as_proto())

	if numpy_dtype in _TENSOR_CONTENT_TYPES:
		if nparray.size * nparray.itemsize >= (1 << 31):
			raise ValueError(
				"Cannot create a tensor proto whose content is larger than 2GB.")
		tensor_proto.tensor_content = nparray.tostring()
		return tensor_proto
	raise ValueError('`tensor_proto` could not be generated.')

def MakeNdarray(tensor):
	"""Create a numpy ndarray from a tensor."""

	shape = [d.size for d in tensor.tensor_shape.dim]
	num_elements = np.prod(shape, dtype=np.int64)
	tensor_dtype = dtypes.as_dtype(tensor.dtype)
	dtype = tensor_dtype.as_numpy_dtype

	if tensor.tensor_content:
		return (np.frombuffer(tensor.tensor_content,
							dtype=dtype).copy().reshape(shape))

	if tensor_dtype == dtypes.string:
		# np.pad throws error on these arrays of type np.object.
		values = list(tensor.string_val)
		padding = num_elements - len(values)
		if padding > 0:
			last = values[-1] if values else ""
			values.extend([last] * padding)
		return np.array(values, dtype=dtype).reshape(shape)

	if tensor_dtype == dtypes.float16 or tensor_dtype == dtypes.bfloat16:
		# the half_val field of the TensorProto stores the binary representation
		# of the fp16: we need to reinterpret this as a proper float16
		values = np.fromiter(tensor.half_val, dtype=np.uint16)
		values.dtype = tensor_dtype.as_numpy_dtype
	elif tensor_dtype == dtypes.float32:
		values = np.fromiter(tensor.float_val, dtype=dtype)
	elif tensor_dtype == dtypes.float64:
		values = np.fromiter(tensor.double_val, dtype=dtype)
	elif tensor_dtype in [
		dtypes.int32, dtypes.uint8, dtypes.uint16, dtypes.int16, dtypes.int8,
		dtypes.qint32, dtypes.quint8, dtypes.qint8, dtypes.qint16, dtypes.quint16
	]:
		values = np.fromiter(tensor.int_val, dtype=dtype)
	elif tensor_dtype == dtypes.int64:
		values = np.fromiter(tensor.int64_val, dtype=dtype)
	elif tensor_dtype == dtypes.complex64:
		it = iter(tensor.scomplex_val)
		values = np.array([complex(x[0], x[1]) for x in zip(it, it)], dtype=dtype)
	elif tensor_dtype == dtypes.complex128:
		it = iter(tensor.dcomplex_val)
		values = np.array([complex(x[0], x[1]) for x in zip(it, it)], dtype=dtype)
	elif tensor_dtype == dtypes.bool:
		values = np.fromiter(tensor.bool_val, dtype=dtype)
	else:
		raise TypeError("Unsupported tensor type: %s" % tensor.dtype)

	if values.size == 0:
		return np.zeros(shape, dtype)

	if values.size != num_elements:
		values = np.pad(values, (0, num_elements - values.size), "edge")

	return values.reshape(shape)
