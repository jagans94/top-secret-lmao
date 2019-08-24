from tensorflow_serving.apis import get_model_status_pb2

from base import Message

class ModelVersionStatus(Message):
    def __init__(self, version=None, state=None, Status=None):
        super().__init__(get_model_status_pb2.ModelVersionStatus(),
                         version=version,
                         state=state,
                         status=status)
    
    @property
    def version(self):
        return self._protobuf.version
        
    @version.setter
    def version(self, _version):
        self._protobuf.version = _version

    @property
    def state(self):
        return self._protobuf.state
        
    @state.setter
    def state(self, _state):
        self._protobuf.state = _state

    @property
    def status(self):
        return self._protobuf.status
        
    @status.setter
    def status(self, _status):
        self._protobuf.status.CopyFrom(_status)
