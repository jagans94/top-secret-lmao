import grpc

from tensorflow_serving.apis import model_pb2
from tensorflow_serving.apis import model_service_pb2_grpc
from tensorflow_serving.apis import get_model_status_pb2
from tensorflow_serving.apis import model_management_pb2
from tensorflow_serving.apis import prediction_service_pb2
from tensorflow_serving.apis import predict_pb2

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
        return self._protobuf.model_spec

    @model_spec.setter
    def model_spec(self, _model_spec):
        self._protobuf.model_spec.CopyFrom(self._unwrap_pb(_model_spec))

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

    def parse_outputs(self):
        parse_outputs = None
        print(self._protobuf.outputs)
        return parse_outputs
        
class PreditionService(GRPCService):
    def __init__(self, server, timeout=5):
        super().__init__(server, timeout)
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)

    def predict(self, request):
        response = PredictResponse()
        if not request.is_intialized(): # Test this by sending a non-initialized request
            raise ValueError('The request needs to be initialized before sending.')
        response.copy(self.stub.Predict(request._protobuf, self.timeout))
        return response