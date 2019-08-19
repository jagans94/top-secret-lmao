import grpc
from tensorflow_serving.sources.storage_path import file_system_storage_path_source_pb2

from base import Message

class ServableVersionPolicy(Message):
    def __init__(self, policy_choice=None):
        super().__init__(file_system_storage_path_source_pb2.FileSystemStoragePathSourceConfig.ServableVersionPolicy(),
                        policy_choice=policy_choice)
    
    @property
    def policy_choice(self):
        return self._protobuf.policy_choice
        
    @policy_choice.setter
    def policy_choice(self, _policy_choice):
        if isinstance(_policy_choice, dict):
            (attr, val), = _policy_choice.items()
        elif isinstance(_policy_choice, str):
            attr = _policy_choice
        else:
            raise TypeError('Unsupported value of type {} provided. \
                Should either be `str` or single key-value `dict`.'.format(type(_policy_choice)))

        if attr == 'latest':
            self._set_latest(value)
        elif attr == 'specific':
            self._set_specific(value)
        elif attr == 'all':
            self._set_all()
        else:
            raise ValueError("Unrecognized value `{}` given for attribute `policy_choice`.".format(attr))
    
    def _set_latest(self, value):
        self._protobuf.latest.num_versions = value
    
    def _set_specific(self, value):
        if not isinstance(value, (list, tuple)):
            value = [value]
        self._protobuf.specific.ClearField('versions')
        self._protobuf.specific.versions.extend(value)

    def _set_all(self):
        self._protobuf.all.SetInParent()