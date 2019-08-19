import google.protobuf.wrappers_pb2 as gpw
from tensorflow_serving.apis import model_pb2
from tensorflow_serving.config import model_server_config_pb2

from base import _Message

class ModelSpec(_Message):
    def __init__(self, name=None, version=None, version_label=None, signature_name=None):
        if version is not None and isinstance(version, int):
            version = gpw.Int64Value(value=version)
        super().__init__(model_pb2.ModelSpec(name=name, 
                                             version=version, 
                                             version_label=version_label, 
                                             signature_name=signature_name))

class ModelConfig(_Message):
    def __init__(self, 
                 name=None, base_path=None, model_platform=None, model_version_policy=None, 
                 version_labels=None, logging_config=None):
        super().__init__(model_server_config_pb2.ModelConfig(), name, base_path, 
                         model_platform, model_version_policy, version_labels, logging_config)