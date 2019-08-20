from tensorflow.contrib.util import make_tensor_proto, make_ndarray

from base import Message

def _make_tensor_proto(values, dtype=None, shape=None, verify_shape=False, allow_broadcast=False):
    '''
    A wrapper function around tensorflow's `make_tensor_proto` method.
    
    ------------------
    The `make_tensor_proto` method in TF can be divorced from the its codebase
    with minimal assumptions. This means you can use this code without installing 
    the TF library. For now, the function defaults to the already implemented 
    `make_tensor_proto` method. In future, it'll work without needing to import 
    the TF library.
    ------------------
    '''
    return make_tensor_proto(values, dtype, shape, verify_shape, allow_broadcast)


def _make_ndarray(values):
    '''
    A wrapper function around tensorflow's `make_ndarray` method.

    ------------------
    Refer above
    ------------------
    '''
    return make_ndarray(values)
