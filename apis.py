import grpc

from tensorflow_serving.apis import get_model_metadata_pb2, model_pb2, predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

from base import Message, GRPCService
from config import ModelConfig, ModelConfigList
from utils import _make_tensor_proto, _make_ndarray

# file specific imports, like .h for c++ 
from apis_dep import *

class ModelSpec(Message):
    def __init__(self, name=None, version=None, version_label=None, signature_name=None):
        super().__init__(model_pb2.ModelSpec(),
                         name=name,
                         version=version,
                         version_label=version_label,
                         signature_name=signature_name)
    
    # type: string
    @property
    def name(self):
        return self._protobuf.name
        
    @name.setter
    def name(self, _name):
        self._protobuf.name = _name

    # type: (Int64Wrapper) internal wrapper
    @property
    def version(self):
        return self._protobuf.version.value
        
    @version.setter
    def version(self, _version):
        self._protobuf.version.value = _version

    # type: string
    @property
    def version_label(self):
        return self._protobuf.version_label
        
    @version_label.setter
    def version_label(self, _version_label):
        self._protobuf.version_label = _version_label

    # type: string
    @property
    def signature_name(self):
        return self._protobuf.signature_name
        
    @signature_name.setter
    def signature_name(self, _signature_name):
        self._protobuf.signature_name = _signature_name 

class PredictRequest(Message):
    def __init__(self, model_spec=None, inputs=None, output_filter=None):
        super().__init__(predict_pb2.PredictRequest(),
                         model_spec=model_spec,
                         inputs=inputs,
                         output_filter=output_filter)

    # type: message
    @property
    def model_spec(self):
        if not hasattr(self, '_model_spec'):
            self._model_spec = ModelSpec()
        print(id(self._model_spec))
        return self._model_spec.copy(self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        self._protobuf.model_spec.CopyFrom(self.unwrap_pb(_model_spec))

    @property
    def inputs(self):
        return self._protobuf.inputs

    @inputs.setter
    def inputs(self, _dict):
        for key, values in _dict.items():
            self._protobuf.inputs[key].CopyFrom(_make_tensor_proto(values))

    # type: (repeated) string
    @property
    def output_filter(self):
        return self._protobuf.output_filter

    @output_filter.setter
    def output_filter(self, _list):
        if not isinstance(_list, (list, tuple)):
            _list = [_list]
        self._protobuf.ClearField('output_filter')
        self._protobuf.output_filter.extend(_list)


class PredictResponse(Message):
    def __init__(self, model_spec=None, outputs=None):
        super().__init__(predict_pb2.PredictResponse(),
                         model_spec=model_spec,
                         outputs=outputs)
        
    @property
    def model_spec(self):
        return self.wrap_pb(ModelSpec(), self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        raise AttributeError("Attribute is read-only, can't be set.")

    @property
    def outputs(self):
        return self._protobuf.outputs

    @outputs.setter
    def outputs(self, _dict):
        raise AttributeError("Attribute is read-only, can't be set.")

    def parse_outputs(self):
        parsed_output_dict = dict()
        for key in self.outputs.keys():
            parsed_output_dict.setdefault(key, _make_ndarray(self.outputs[key]))
        return parsed_output_dict

    
class GetModelMetadataRequest(Message):
    
    _supported_metadatafields = frozenset('signature_def')

    def __init__(self, model_spec=None, metadata_field=None):
        super().__init__(get_model_metadata_pb2.GetModelMetadataRequest(),
                         model_spec=model_spec,
                         metadata_field=metadata_field)
        
    @property
    def model_spec(self):
        return self.wrap_pb(ModelSpec(), self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        self._protobuf.model_spec.CopyFrom(self.unwrap_pb(_model_spec))
    
    # type: (repeated) string
    @property
    def metadata_field(self):
        return self._protobuf.metadata_field

    @metadata_field.setter
    def metadata_field(self, _list):
        if not isinstance(_list, (list, tuple)):
            _list = [_list]
        if isinstance(_list, (tuple, list)):
            if len(_list) != 1: 
                raise AttributeError("Currently, the `metadata_field` only accepts a single value.")
            elif _list[0] not in  GetModelMetadataRequest._supported_metadatafields:
                raise ValueError(\
                    '{} not among supported values: {}`.'.format(_list[0],
                    GetModelMetadataRequest._supported_metadatafields))

        self._protobuf.ClearField('metadata_field')
        self._protobuf.metadata_field.extend(_list)

        
class GetModelMetadataResponse(Message):
    def __init__(self, model_spec=None, metadata=None):
        super().__init__(get_model_metadata_pb2.GetModelMetadataResponse(),
                         model_spec=model_spec,
                         metadata=metadata)
        
    @property
    def model_spec(self):
        return self.wrap_pb(ModelSpec(), self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        raise AttributeError("Attribute is read-only, can't be set.")

    @property
    def metadata(self):
        return self._protobuf.metadata

    @metadata.setter
    def metadata(self, _dict):
        raise AttributeError("Attribute is read-only, can't be set.")

    # TODO: Add a method to parse the metadata response

        
class PredictionService(GRPCService):
    def __init__(self, server):
        super().__init__(server)
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)

    def predict(self, request, timeout=5):
        request = self.unwrap_pb(request)
        response = self.wrap_pb(PredictResponse(),
                                self.stub.Predict(request, timeout))
        return response

    def get_model_metadata(self, request, timeout=5):
        request = self.unwrap_pb(request)
        response = self.wrap_pb(GetModelMetadataResponse(),
                                self.stub.GetModelMetadata(request, timeout))
        return response
    
    
class ReloadConfigRequest(Message):
    def __init__(self, config=None):
        super().__init__(model_management_pb2.ReloadConfigRequest(), 
                         config=model_config_list)
    
    @property
    def config(self):
        return self.wrap_pb(ModelServerConfig(), self._protobuf.config)

    @config.setter
    def config(self, _config):
        self._protobuf.config.CopyFrom(self.unwrap(_config))


class ModelServerConfig(Message):
    def __init__(self, model_config_list=None, custom_model_config=None):
        super().__init__(model_management_pb2.ReloadConfigRequest(), 
                         model_config_list=model_config_list,
                         custom_model_config=custom_model_config)
    
    @property
    def model_config_list(self):
        return self.wrap_pb(ModelConfigList(), self._protobuf.model_config_list)

    @model_config_list.setter
    def model_config_list(self, _model_config_list):
        self._protobuf.model_config_list.CopyFrom(self.unwrap(_model_config_list))

    @property
    def custom_model_config(self):
        return NotImplementedError

    @custom_model_config.setter
    def custom_model_config(self, value):
        return NotImplementedError


class ReloadConfigResponse(Message):
    def __init__(self, status=None):
        super().__init__(model_management_pb2.ReloadConfigResponse(), 
                         status=status)

    @property
    def status(self):
        return self._protobuf.status 

    @status.setter
    def status(self, value):
        raise AttributeError("Attribute is read-only, can't be set.")

    # TODO: Add method to process status if required; 
    # if it's general enough create a class for status and add to it.


class GetModelStatusRequest(Message):
    def __init__(self, model_spec=None):
        super().__init__(get_model_status_pb2.GetModelStatusRequest(), 
                         model_spec=model_spec)
    
    @property
    def model_spec(self):
        return self.wrap_pb(ModelSpec(), self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        self._protobuf.model_spec.CopyFrom(self.unwrap_pb(_model_spec))
    
class GetModelStatusResponse(Message):
    def __init__(self, model_version_status=None):
        super().__init__(get_model_status_pb2.GetModelStatusResponse(), 
                         model_version_status=model_version_status)

    @property
    def model_version_status(self):
        return self.wrap_pb(ModelVersionStatus(), self._protobuf._model_version_status)

    @model_version_status.setter
    def model_version_status(self, _model_version_status):
        self._protobuf.model_version_status.CopyFrom(self.unwrap_pb(_model_version_status))


class ModelService(GRPCService):
    def __init__(self, server):
        super().__init__(server)
        self.stub = model_service_pb2_grpc.ModelServiceStub(self.channel)

    def reload_config(self, request, timeout=5):
        request = self.unwrap_pb(request)
        response = self.wrap_pb(ReloadConfigResponse(),
                                self.stub.HandleReloadConfigRequest(request, timeout))
        return response


    def get_model_status(self, request, timeout=5):
        request = self.unwrap_pb(request)
        response = self.wrap_pb(GetModelStatusResponse(),
                                self.stub.GetModelStatus(request, timeout))
        return response
