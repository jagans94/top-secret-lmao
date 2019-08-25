import grpc

from tensorflow_serving.apis import get_model_metadata_pb2, model_pb2
from tensorflow_serving.apis import get_model_status_pb2
from tensorflow_serving.apis import predict_pb2

from tensorflow_serving.apis import prediction_service_pb2_grpc
from tensorflow_serving.apis import model_service_pb2_grpc

from base import Message, GRPCService
from config import ModelConfig, ModelConfigList
from util import Status
from tfs_utils import _make_tensor_proto, _make_ndarray


class ModelSpec(Message):
    def __init__(self, name=None, version=None, version_label=None,
                    signature_name=None, **kwargs):
        super().__init__(model_pb2.ModelSpec(),
                         name=name,
                         version=version,
                         version_label=version_label,
                         signature_name=signature_name,
                         **kwargs)
    
    # type: string
    @property
    def name(self):
        return self._protobuf.name
        
    @name.setter
    def name(self, _name):
        self._protobuf.name = _name
        self.__set_in_parent__()

    # type: (Int64Wrapper) message
    @property
    def version(self):
        return self._protobuf.version.value
        
    @version.setter
    def version(self, _version):
        self._protobuf.version.value = _version
        self.__set_in_parent__()

    # type: string
    @property
    def version_label(self):
        return self._protobuf.version_label
        
    @version_label.setter
    def version_label(self, _version_label):
        self._protobuf.version_label = _version_label
        self.__set_in_parent__()

    # type: string
    @property
    def signature_name(self):
        return self._protobuf.signature_name
        
    @signature_name.setter
    def signature_name(self, _signature_name):
        self._protobuf.signature_name = _signature_name
        self.__set_in_parent__()


class ModelVersionStatus(Message):
    def __init__(self, version=None, state=None, status=None, **kwargs):
        super().__init__(get_model_status_pb2.ModelVersionStatus(),
                         version=version,
                         state=state,
                         status=status,
                         **kwargs)
    
    # type: int
    @property
    def version(self):
        return self._protobuf.version
        
    @version.setter
    def version(self, _version):
        self._protobuf.version = _version
        self.__set_in_parent__()

    # type: enum
    @property
    def state(self):
        return self._protobuf.state
        
    @state.setter
    def state(self, _state):
        self._protobuf.state = _state
        self.__set_in_parent__()

    # type: message
    @property
    def status(self):
        if not hasattr(self, , _status):
            self._status = Status(container=self, descriptor='status')
        return self._status.copy(self._protobuf.status)
        
    @status.setter
    def status(self, _status):
        self._protobuf.status.CopyFrom(self.unwrap_pb(_status))
        self.__set_in_parent__()


class PredictRequest(Message):
    def __init__(self, model_spec=None, inputs=None, output_filter=None, **kwargs):
        super().__init__(predict_pb2.PredictRequest(),
                         model_spec=model_spec,
                         inputs=inputs,
                         output_filter=output_filter,
                         **kwargs)

    # type: message
    @property
    def model_spec(self):
        if not hasattr(self, '_model_spec'):
            self._model_spec = ModelSpec(container=self, descriptor='model_spec')
        return self._model_spec.copy(self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        self._protobuf.model_spec.CopyFrom(self.unwrap_pb(_model_spec))
        self.__set_in_parent__()

    # type: (map) string : tensor_proto
    @property
    def inputs(self):
        return self._protobuf.inputs

    @inputs.setter
    def inputs(self, _dict):
        for key, values in _dict.items():
            self._protobuf.inputs[key].CopyFrom(_make_tensor_proto(values))
        self.__set_in_parent__()

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
        self.__set_in_parent__()


class PredictResponse(Message):
    def __init__(self, model_spec=None, outputs=None, **kwargs):
        super().__init__(predict_pb2.PredictResponse(),
                         model_spec=model_spec,
                         outputs=outputs,
                         **kwargs)
    
    # type: message
    @property
    def model_spec(self):
        if not hasattr(self, '_model_spec'):
            self._model_spec = ModelSpec(container=self, descriptor='model_spec')
        return self._model_spec.copy(self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        raise AttributeError("Attribute is read-only, can't be set.")

    # type: (map) string : tensor_proto
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

    def __init__(self, model_spec=None, metadata_field=None, **kwargs):
        super().__init__(get_model_metadata_pb2.GetModelMetadataRequest(),
                         model_spec=model_spec,
                         metadata_field=metadata_field,
                         **kwargs)
        
    # type: message
    @property
    def model_spec(self):
        if not hasattr(self, '_model_spec'):
            self._model_spec = ModelSpec(container=self, descriptor='model_spec')
        return self._model_spec.copy(self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        self._protobuf.model_spec.CopyFrom(self.unwrap_pb(_model_spec))
        self.__set_in_parent__()
    
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
        self.__set_in_parent__()

        
class GetModelMetadataResponse(Message):
    def __init__(self, model_spec=None, metadata=None, **kwargs):
        super().__init__(get_model_metadata_pb2.GetModelMetadataResponse(),
                         model_spec=model_spec,
                         metadata=metadata,
                         **kwargs)
        
    # type: message
    @property
    def model_spec(self):
        if not hasattr(self, '_model_spec'):
            self._model_spec = ModelSpec(container=self, descriptor='model_spec')
        return self._model_spec.copy(self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        raise AttributeError("Attribute is read-only, can't be set.")

    # type: (map) string : any_proto
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
    def __init__(self, config=None, **kwargs):
        super().__init__(model_management_pb2.ReloadConfigRequest(), 
                         config=config,
                         **kwargs)
    
    # type: message
    @property
    def config(self):
        if not hasattr(self, '_config'):
            self._config = ModelServerConfig(container=self, descriptor='config')
        return self._config.copy(self._protobuf.config)

    @config.setter
    def config(self, _config):
        self._protobuf.config.CopyFrom(self.unwrap_pb(_config))
        self.__set_in_parent__()


class ReloadConfigResponse(Message):
    def __init__(self, status=None, **kwargs):
        super().__init__(model_management_pb2.ReloadConfigResponse(), 
                         status=status,
                         **kwargs)

    # type: message
    @property
    def status(self):
        if not hasattr(self, '_status'):
            self._status = Status(container=self, descriptor='status')
        return self._status.copy(self._protobuf.status)

    @status.setter
    def status(self, value):
        raise AttributeError("Attribute is read-only, can't be set.")

    # TODO: Add method to process status if required; 
    # if it's general enough create a class for status and add to it.


class GetModelStatusRequest(Message):
    def __init__(self, model_spec=None):
        super().__init__(get_model_status_pb2.GetModelStatusRequest(), 
                         model_spec=model_spec)
    
    # type: message
    @property
    def model_spec(self):
        if not hasattr(self, '_model_spec'):
            self._model_spec = ModelSpec(container=self, descriptor='model_spec')
        return self._model_spec.copy(self._protobuf.model_spec)

    @model_spec.setter
    def model_spec(self, _model_spec):
        self._protobuf.model_spec.CopyFrom(self.unwrap_pb(_model_spec))
        self.__set_in_parent__()
    
class GetModelStatusResponse(Message):
    def __init__(self, model_version_status=None):
        super().__init__(get_model_status_pb2.GetModelStatusResponse(), 
                         model_version_status=model_version_status)

    # type: message
    @property
    def model_version_status(self):
        if not hasattr(self, '_model_version_status'):
            self._model_version_status = ModelVersionStatus(container=self, descriptor='model_version_status')
        return self._model_version_status.copy(self._protobuf.model_version_status)

    @model_version_status.setter
    def model_version_status(self, _model_version_status):
        self._protobuf.model_version_status.CopyFrom(self.unwrap_pb(_model_version_status))
        self.__set_in_parent__()


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
