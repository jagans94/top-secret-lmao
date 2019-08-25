from tensorflow_serving.sources.storage_path import file_system_storage_path_source_pb2

from base import Message

class ServableVersionPolicy(Message):
    '''
    TODO: A cleaner implementation for setting the one-of values exclusively, 
    while preserving input definition in the constructor.
    '''
    def __init__(self, latest=None, specific=None, _all=None, **kwargs):
        super().__init__(file_system_storage_path_source_pb2.FileSystemStoragePathSourceConfig.ServableVersionPolicy(),
                        latest=latest, 
                        specific=specific, 
                        _all=_all,
                        **kwargs)        
    
    # type: int
    @property
    def latest(self):
        return self._protobuf.latest

    @latest.setter
    def latest(self, value):
        self._protobuf.latest.num_versions = value
        self.__set_in_parent__()

    # type: (repeated) int
    @property
    def specific(self):
        return self._protobuf.specific

    @specific.setter
    def specific(self, value):
        if not isinstance(value, (list, tuple)):
            value = [value]
        self._protobuf.specific.ClearField('versions')
        self._protobuf.specific.versions.extend(value)
        self.__set_in_parent__()
    
    # type: none
    # getting/setting this attribute, set's the policy to `all`
    @property
    def _all(self):
        self._protobuf.all.SetInParent()
        self.__set_in_parent__()
        return

    @_all.setter
    def _all(self, value):
        if value is not None:
            self._protobuf.all.SetInParent()
            self.__set_in_parent__()
            

    def clear(self):
        self._protobuf.ClearField('policy_choice')
        
