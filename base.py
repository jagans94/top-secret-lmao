import grpc
from google.protobuf import text_format
import warnings

class _Message(object):
    def __init__(self, protobuf):
        self.protobuf = protobuf

    def update(self, **kwargs):
        if kwargs is None:
            raise ValueError('No values provided.')
        
        attr_not_found = list() 
        '''
        Q: A catch mechanism for `attr`s that could not be set. Is it needed? Why?
        A: Not needed, I guess, since `google.protobuf.message` takes care of handling 
        the errors. Let's take a call on it in the future, depending on if and how the code breaks.
        The only way I see this making sense, is to let the errors percolate with sensible warnings, 
        i.e. shouldn't cause the user to go mad. IMHO.

        Simplifying interface for setting some complex `attr`s that can't be set directly
        should be done by customizing the derived class to manage around the said `attr`s.
        This makes sense, since each protobuf definition is different.
        '''
        for attr, val in kwargs.items():
            if hasattr(self.protobuf, attr) and val is not None: 
                setattr(self.protobuf, attr, val)
            else:
                attr_not_found.append(attr)
        if attr_not_found:
            raise warnings.warn('The follwing attributes were not found: {}'.format(attr_not_found))

    def __str__(self):
        return str(self.protobuf)
            
    def from_text(self, path):
        with open(path, 'r+') as f:
            self.protobuf.CopyFrom(text_format.Parse(text=f.read(), message=self.protobuf)) 

    def to_text(self, path):
        with open(path, 'w+') as f:
            f.write(text_format.MessageToString(message=self.protobuf))

    def from_pb(self, path):
        with open(path, 'rb') as f:
            self.protobuf.ParseFromString(f.read())

    def to_pb(self, path):
        with open(path, 'wb') as f:
            f.write(self.protobuf.SerializeToString())            

    def copy(self, protobuf):
        self.protobuf.CopyFrom(protobuf)

    def merge(self, protobuf):
        self.protobuf.MergeFrom(protobuf)

    @property
    def is_initialized(self):
        return self.protobuf.IsInitialized()
    
    @property
    def byte_size(self):
        return self.protobuf.ByteSize()

class _GRPCService(object):
    def __init__(self, server, timeout=5):
        self.channel = self.create_insecure_channel(server)
        self.timeout = timeout

    def create_secure_channel(self):
        raise NotImplementedError

    def create_insecure_channel(self, server):
        return grpc.insecure_channel(server)