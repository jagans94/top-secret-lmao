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
"""
Helper classes for tensor shape inference.
NOTE: Adapted from TensorFlow library.
"""

from tensorflow.core.framework import tensor_shape_pb2
from tensorflow.python.framework import dtypes

class Dimension(object):
	"""Represents the value of one dimension in a TensorShape."""

	def __init__(self, value):
		"""Creates a new Dimension with the given value."""
		if value is None:
			self._value = None
		elif isinstance(value, Dimension):
			self._value = value.value
		elif isinstance(value, dtypes.DType):
			raise TypeError("Cannot convert %s to Dimension" % value)
		else:
			self._value = int(value)
			if self._value != value:
				raise ValueError("Ambiguous dimension: %s" % value)
			if self._value < 0:
				raise ValueError("Dimension %d must be >= 0" % self._value)

	def __repr__(self):
		return "Dimension(%s)" % repr(self._value)

	def __int__(self):
		return self._value

	@property
	def value(self):
		"""The value of this dimension, or None if it is unknown."""
		return self._value

def as_dimension(value):
	"""Converts the given value to a Dimension.
	"""
	if isinstance(value, Dimension):
		return value
	else:
		return Dimension(value)

class TensorShape(object):
	"""Represents the shape of a tensor in TensorProto."""

	def __init__(self, dims):
		"""Creates a new Dimension with the given value."""
		if dims is None:
			self._dims = None
		elif isinstance(dims, tensor_shape_pb2.TensorShapeProto):
			if dims.unknown_rank:
				self._dims = None
			else:
				# Protos store variable-size dimensions as -1
				self._dims = [as_dimension(dim.size if dim.size != -1 else None) for dim in dims.dim]
		elif isinstance(dims, TensorShape):
			self._dims = dims.dims
		else:
			try:
				dims_iter = iter(dims)
			except TypeError:
				# Treat as a singleton dimension
				self._dims = [as_dimension(dims)]
			else:
				# Got a list of dimensions
				self._dims = [as_dimension(d) for d in dims_iter]

	def __repr__(self):
		if self._dims is not None:
			return "TensorShape(%r)" % [dim.value for dim in self._dims]
		else:
			return "TensorShape(None)"

	@property
	def rank(self):
		"""Returns the rank of this shape, or None if it is unspecified."""
		if self._dims is not None:
			return len(self._dims)
		return None

	@property
	def dims(self):
		"""Returns a list of Dimensions, or None if the shape is unspecified."""
		return self._dims

	def __iter__(self):
		"""Returns `self.dims` if the rank is known, otherwise raises ValueError."""
		if self._dims is None:
			raise ValueError("Cannot iterate over a shape with unknown rank.")
		else:
			return iter(d for d in self._dims)

	def __getitem__(self, key):
		if self._dims is not None:
			if isinstance(key, slice):
				return TensorShape(self._dims[key])
			else:
				return self._dims[key]
		else:
			raise ValueError("Steps are not yet handled")

	def as_list(self):
		"""Returns a list of integers or `None` for each dimension,
		otherwise raises ValueError.
		"""
		if self._dims is None:
			raise ValueError("Can't call `as_list()` on a unknown TensorShape.")
		return [dim.value for dim in self._dims]

	def as_proto(self):
		"""Returns this shape as a `TensorShapeProto`."""
		if self._dims is None:
			return tensor_shape_pb2.TensorShapeProto(unknown_rank=True)
		else:
			return tensor_shape_pb2.TensorShapeProto(dim=[
			tensor_shape_pb2.TensorShapeProto.Dim(
				size=-1 if d.value is None else d.value) for d in self._dims
		])


def as_shape(shape):
	"""Converts the given object to a TensorShape."""
	if isinstance(shape, TensorShape):
		return shape
	else:
		return TensorShape(shape)
