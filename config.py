import grpc
from tensorflow_serving.config import model_server_config_pb2
from tensorflow_serving.config import logging_config_pb2

from base import Message, MessageList, GRPCService
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

    # type: string
    @property
    def name(self):
        return self._protobuf.name
        
    @name.setter
    def name(self, _name):
        self._protobuf.name = _name

    # type: string
    @property
    def base_path(self):
        return self._protobuf.base_path
        
    @base_path.setter
    def base_path(self, _base_path):
        self._protobuf.base_path = _base_path

    # type: string
    @property
    def model_platform(self):
        return self._protobuf.model_platform
        
    @model_platform.setter
    def model_platform(self, _model_platform):
        self._protobuf.model_platform = _model_platform

    # type: message
    @property
    def model_version_policy(self):
        return self.wrap_pb(ServableVersionPolicy(), self._protobuf.model_version_policy)
        
    @model_version_policy.setter
    def model_version_policy(self, _model_version_policy):
        self._protobuf.model_version_policy.CopyFrom(self.unwrap_pb(_model_version_policy))

    # type: map
    @property
    def version_labels(self):
        return self._protobuf.version_labels

    @version_labels.setter
    def version_labels(self, _dict):
        for key, value in _dict.items():
            self._protobuf.version_labels[key] = value

    # type: message
    @property
    def logging_config(self):
        raise AttributeError('`logging_config` is not supported as of now.')

    @logging_config.setter
    def logging_config(self, value):
        raise AttributeError('`logging_config` is not supported as of now.')


class ModelConfigList(Message):
    def __init__(self, config=None):
        super().__init__(model_server_config_pb2.ModelConfigList(),
                        config=config)
    
    # type: (repeated) message
    @property
    def config(self):
        return MessageList(self._protobuf.config, ModelConfig())
        
    @config.setter
    def config(self, _list):
        if not isinstance(_list, (list, tuple)):
            _list = [_list]
        _list = [self.unwrap_pb(cfg) for cfg in _list]
        self._protobuf.ClearField('config')
        self._protobuf.config.extend(_list)


class ModelServerConfig(Message):
    def __init__(self, model_config_list=None, custom_model_config=None):
        super().__init__(model_server_config_pb2.ModelServerConfig(),
                        model_config_list=model_config_list,
                        custom_model_config=custom_model_config)

    # type: (oneof) message
    @property
    def model_config_list(self):
        return self.wrap_pb(ModelConfigList(), self._protobuf.model_config_list)
    
    @model_config_list.setter
    def model_config_list(self, _model_config_list):
        self._protobuf.model_config_list.CopyFrom(self.unwrap_pb(_model_config_list))

    # type: (oneof) message
    @property
    def custom_model_config(self):
        return NotImplementedError

    @custom_model_config.setter
    def custom_model_config(self, _custom_model_config):
        return NotImplementedError
