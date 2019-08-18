import grpc
from tensorflow_serving.apis import prediction_service_pb2
from tensorflow_serving.apis import predict_pb2

from base import _Message, GRPCService
from utils import _make_tensor_proto, _make_ndarray
from utils import unpack_dict, unpack_list
from pbs import ModelSpec

class PredictRequest(_Message):
    def __init__(self, model_spec=None, inputs=None, output_filter=None):
        super().__init__(predict_pb2.PredictRequest(),
                         model_spec=model_spec,
                         inputs=inputs,
                         output_filter=output_filter)

    @property
    def model_spec(self):
        return self.protobuf.model_spec

    @model_spec.setter
    def model_spec(self, _model_spec):
        self.protobuf.model_spec.CopyFrom(_model_spec)

    @property
    def inputs(self):
        return self.protobuf.inputs

    @inputs.setter
    def inputs(self, _dict):
        for key, values in _dict.items():
            self.protobuf.inputs[key].CopyFrom(_make_tensor_proto(values))

    @property
    def output_filter(self):
        return self.protobuf.output_filter

    @output_filter.setter
    def output_filter(self, _list):
        if not isinstance(_list, (list, tuple)):
            _list = [_list]
        self.protobuf.ClearField('output_filter')
        self.protobuf.output_filter.extend(_list)


class PredictResponse(_Message):
    def __init__(self, model_spec=None, outputs=None):
        super().__init__(predict_pb2.PredictResponse(),
                         model_spec=model_spec,
                         outputs=outputs)

    def parse_outputs(self):
        parse_outputs = None
        print(self.protobuf.outputs)
        return parse_outputs
        
class PreditionService(_GRPCService):
    def __init__(self, server, timeout=5):
        super().__init__(server, timeout)
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)

    def predict(self, request):
        response = PredictResponse()
        if not request.is_intialized(): # Test this by sending a non-initialized request
            raise ValueError('The request needs to be initialized before sending.')
        response.copy(self.stub.Predict(request.protobuf, self.timeout))
        return response

