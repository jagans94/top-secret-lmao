# Fallback in case tensorflow library is not available.
try:
	# Tensorflow implementation
	from tensorflow.contrib.util import make_tensor_proto, make_ndarray
	_TENSORFLOW_AVAILABLE = True
except ImportError:
	# Internal implementation
	from tensorflow.python.tensor_util import MakeTensorProto, MakeNdarray
	_TENSORFLOW_AVAILABLE = False

def _make_tensor_proto(values, dtype=None, shape=None, verify_shape=False, allow_broadcast=False):
    if _TENSORFLOW_AVAILABLE:
		return make_tensor_proto(values, dtype, shape, verify_shape, allow_broadcast)
	return MakeTensorProto(values, dtype)

def _make_ndarray(tensor):
    if _TENSORFLOW_AVAILABLE:
    	return make_ndarray(tensor)
	return MakeNdarray(tensor)
