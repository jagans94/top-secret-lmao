import grpc
from google.protobuf import text_format

def unwrap_pb(obj):
    if isinstance(obj, Message.__subclasses__()):
        return obj._protobuf
    return obj

def wrap_pb(pb, cls):
    return cls()._protobuf

class Message(object):
    def __init__(self, protobuf, **kwargs):
        self._protobuf = protobuf
        self.update(**kwargs)
    
    def update(self, **kwargs):
        if kwargs is None:
            raise ValueError('No values provided.')
        
        for attr, val in kwargs.items():
            val = self._unwrap_pb(val)
            if val is not None:
                # use the class attribute setter method
                setattr(self, attr, val)

    def _unwrap_pb(self, val):
        # extract protobuf, if the nested message shares the same base class, 
        # i.e. `Message`
        if isinstance(val, self.__class__.__bases__):
            return val._protobuf
        return val

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
        self._protobuf.CopyFrom(self._unwrap_pb(obj))

    def merge(self, obj):
        self._protobuf.MergeFrom(self._unwrap_pb(obj))

    @property
    def is_initialized(self):
        return self._protobuf.IsInitialized()
    
    @property
    def byte_size(self):
        return self._protobuf.ByteSize()

class GRPCService(object):
    def __init__(self, server, timeout=5):
        self.channel = self.create_insecure_channel(server)
        self.timeout = timeout
        
    def _unwrap_pb(self, val):
        # extract protobuf, if the nested message shares the same base class, 
        # i.e. `Message`
        if isinstance(val, Message):
            return val._protobuf
        return val

    def create_secure_channel(self):
        raise NotImplementedError

    def create_insecure_channel(self, server):
        return grpc.insecure_channel(server)