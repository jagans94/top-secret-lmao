import grpc

from tensorflow_serving.apis import get_model_metadata_pb2, model_pb2, predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

from base import Message, GRPCService
from config import ModelConfig
from utils import _make_tensor_proto, _make_ndarray

class ModelSpec(Message):
    def __init__(self, name=None, version=None, version_label=None, signature_name=None):
        super().__init__(model_pb2.ModelSpec(),
                         name=name,
                         version=version,
                         version_label=version_label,
                         signature_name=signature_name)
    
    @property
    def name(self):
        return self._protobuf.name
        
    @name.setter
    def name(self, _name):
        self._protobuf.name = _name

    @property
    def version(self):
        return self._protobuf.version.value
        
    @version.setter
    def version(self, _version):
        self._protobuf.version.value = _version

    @property
    def version_label(self):
        return self._protobuf.version_label
        
    @version_label.setter
    def version_label(self, _version_label):
        self._protobuf.version_label = _version_label

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

    @property
    def model_spec(self):
        return self.wrap_pb(ModelSpec(), self._protobuf.model_spec)

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

    @property
    def metadata_field(self):
        return self._protobuf.metadata_field

    @metadata_field.setter
    def metadata_field(self, _list):
        if isinstance(_list, (tuple, list)) and len(_list) != 1 or \
            _list[0] not in  GetModelMetadataRequest._supported_metadatafields:
            raise AttributeError('Currently, the `metadata_field` \
                only accepts `signature_def`.')
        if not isinstance(_list, (list, tuple)):
            _list = [_list]
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

    # TODO: Add a method to parse the response

        
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
    def __init__(self, model_config_list=None, custom_model_config=None):
        super().__init__(model_management_pb2.ReloadConfigRequest(), 
                         model_config_list=model_config_list,
                         custom_model_config=custom_model_config)
    
    @property
    def model_config_list(self):
        return self._protobuf.model_config_list

    @model_config_list.setter
    def model_config_list(self, _list):
        if not isinstance(_list, (list, tuple)):
            _list = [_list]
        self._protobuf.ClearField('model_config_list')
        self._protobuf.model_config_list.extend(_list)

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
        # TODO: Need to create a wrapper for status proto
        return self._protobuf.status 

    @status.setter
    def status(self, value):
        raise AttributeError("Attribute is read-only, can't be set.")

    # TODO: Add method to process status

class GetModelStatusRequest(_Message):
    def __init__(self, model_spec=None):
        super().__init__(get_model_status_pb2.GetModelStatusRequest(), 
                         model_spec=model_spec)
    
    @property
    def model_spec(self):
        return self.wrap_pb(ModelSpec(), self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        self._protobuf.model_spec.CopyFrom(self.unwrap_pb(_model_spec))
    
class GetModelStatusResponse(_Message):
    def __init__(self, model_version_status=None):
        super().__init__(get_model_status_pb2.GetModelStatusResponse(), model_version_status)

class ModelService(GRPCService):
    def __init__(self, server, timeout=5):
        super().__init__(server, timeout)
        self.stub = model_service_pb2_grpc.ModelServiceStub(self.channel)
        self.response = None

    def reload_config(self, request):
        response = ReloadConfigResponse()
        if not request.is_intialized(): # Test this by sending a non-initialized request
            raise ValueError('The request needs to be initialized before sending.')
        response.copy(self.stub.HandleReloadConfigRequest(request.protobuf, self.timeout))
        return response

    def get_model_status(self, request):
        response = GetModelStatusResponse()
        if not request.is_intialized(): # Test this by sending a non-initialized request
            raise ValueError('The request needs to be initialized before sending.')
        response.copy(self.stub.GetModelStatus(request.protobuf, self.timeout))
        return response
