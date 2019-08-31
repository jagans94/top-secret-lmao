import grpc
from google.protobuf import text_format

class Message(object):
    def __init__(self, protobuf, **kwargs):
        self._protobuf = protobuf
        self._container = kwargs.pop('container', None)
        self._descriptor = kwargs.pop('descriptor', None)
        self.update(**kwargs)
    
    def update(self, **kwargs):
        if kwargs is None:  
            return
        
        for attr, val in kwargs.items():
            val = self.unwrap_pb(val)
            if val is not None:
                # use the class attribute setter method
                setattr(self, attr, val)

    def __set_in_parent__(self):
        if self._container:
            setattr(self._container, self._descriptor, self)

    def __str__(self):
        return str(self._protobuf)

    def __repr__(self):
        return repr(self._protobuf)
            
    def from_text(self, path):
        with open(path, 'r+') as f: 
            text_format.Merge(text=f.read(), message=self._protobuf)           

    def to_text(self, path):
        with open(path, 'w+') as f:
            f.write(text_format.MessageToString(message=self._protobuf))

    def from_pb(self, path):
        with open(path, 'rb') as f:
            self._protobuf.ParseFromString(f.read())

    def to_pb(self, path):
        with open(path, 'wb') as f:
            f.write(self._protobuf.SerializeToString())       

    def copy(self, obj):
        self._protobuf.CopyFrom(self.unwrap_pb(obj))
        return self

    def merge(self, obj):
        self._protobuf.MergeFrom(self.unwrap_pb(obj))
        return self

    @property
    def is_initialized(self):
        return self._protobuf.IsInitialized()
    
    @property
    def byte_size(self):
        return self._protobuf.ByteSize()

    @staticmethod
    def unwrap_pb(obj):
        if isinstance(obj, Message):
            return obj._protobuf
        return obj


class GRPCService(object):
    def __init__(self, server, **kwargs):
        self.channel = self.create_insecure_channel(server)


# A container class for a list of messages
class MessageList(Message):
    def __init__(self, protobuf, wrapper, **kwargs):
        super().__init__(protobuf, **kwargs)
        self._wrapper = wrapper

    def __len__(self):
        return self._protobuf.__len__()

    def __getitem__(self, key):
        return self.wrap_pb(self._wrapper, self._protobuf.__getitem__(key))

    def __setitem__(self, key, value):
        self._protobuf.__setitem__(key, self.unwrap_pb(value))
        self.__set_in_parent__()

    def __delitem__(self, key):
        return self._protobuf.__delitem__(key)

    def __iter__(self):
        return iter([self.wrap_pb(self._wrapper, item) for item in self._protobuf])

    def extend(self, _list):
        # extend works like append for single non-list items
        if not isinstance(_list, (tuple, list)):
            _list = [_list]
        _list = [self.unwrap_pb(item) for item in _list]
        self._protobuf.extend(_list)

    def insert(self, index, _item):
        self._protobuf.insert(index, self.unwrap_pb(_item))

    def pop(self, index=None):
        index = index or -1
        return self.wrap_pb(self._wrapper, self._protobuf.pop(index))

    def remove(self, value):
        self._protobuf.remove(value)

    def sort(self):
        self._protobuf.sort()
