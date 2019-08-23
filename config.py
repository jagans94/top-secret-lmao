import grpc
from tensorflow_serving.config import model_server_config_pb2
from tensorflow_serving.config import logging_config_pb2

from base import Message, GRPCService
from sources import ServableVersionPolicy

class ModelConfig(Message):
    def __init__(self, name=None, base_path=None, model_platform=None,
                 model_version_policy=None, version_labels=None, logging_config=None):
        super().__init__(model_server_config_pb2.ModelConfig(),
                        name=name,
                        base_path=base_path, 
                        model_platform=model_platform,
                        model_version_policy=model_version_policy,
                        version_labels=version_labels,
                        logging_config=logging_config)

    @property
    def name(self):
        return self._protobuf.name
        
    @name.setter
    def name(self, _name):
        self._protobuf.name = _name

    @property
    def base_path(self):
        return self._protobuf.base_path
        
    @base_path.setter
    def base_path(self, _base_path):
        self._protobuf.base_path = _base_path

    @property
    def model_platform(self):
        return self._protobuf.model_platform
        
    @model_platform.setter
    def model_platform(self, _model_platform):
        self._protobuf.model_platform = _model_platform

    @property
    def model_version_policy(self):
        return self._protobuf.model_version_policy
        
    @model_version_policy.setter
    def model_version_policy(self, _policy_choice):
        model_version_policy = ServableVersionPolicy(_policy_choice)
        self._protobuf.model_version_policy.CopyFrom(self._unwrap_pb(model_version_policy))

    @property
    def version_labels(self):
        return self._protobuf.version_labels

    @version_labels.setter
    def version_labels(self, _dict):
        for key, value in _dict.items():
            self._protobuf.version_labels[key] = value

    @property
    def logging_config(self):
        raise AttributeError('`logging_config` is not supported as of now.')

    @logging_config.setter
    def logging_config(self, value):
        raise AttributeError('`logging_config` is not supported as of now.')


class ModelConfigList(Message):
    def __init__(self, config=None):
        super().__init__(model_server_config_pb2.ModelConfigList(),
                        name=config)

    @property
    def config(self):
        # Since you're returning a list of configs, 
        # you'd need to wrap each element of the list before returning
        return [self.wrap_pb(ModelConfig(), cfg) for cfg in self._protobuf.config]
        
    @config.setter
    def config(self, _list):
        if not isinstance(_list, (list, tuple)):
            _list = [_list]
        # Unwrap each instance of the list
        _list = [self.unwrap_pb(cfg) for cfg in _list]
        self._protobuf.ClearField('model_config_list')
        self._protobuf.model_config_list.extend(_list)
