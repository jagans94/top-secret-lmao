'''
Typical Usage:

predict_request = PredictRequest(model_spec, inputs, output_filters)
predict_request.read_inputs(**kwargs) # reads input key : value(numpy array) pairs

predict_service = PredictionService(server, timeout)
predict_response = predict_service.predict(predict_request)

outputs = predict_response.parse_outputs()
'''
import grpc
from tensorflow_serving.apis import prediction_service_pb2
from tensorflow_serving.apis import predict_pb2

from base import _Message, _GRPCService
from utils import _make_tensor_proto, _make_ndarray
from pbs import ModelSpec

class PredictRequest(_Message):
    def __init__(self, model_spec=None, inputs=None, output_filter=None):
        super().__init__(predict_pb2.PredictRequest(
            model_spec=model_spec,
            inputs=inputs,
            output_filter=output_filter))
        
    def read_inputs(self, **inputs):
        '''Reads (key, value) pairs into the request.
        '''
        for key, np_arr in inputs.items():
            self.protobuf.inputs[key].CopyFrom(_make_tensor_proto(np_arr))

    def extend(self, attr, )

class PredictResponse(_Message):
    def __init__(self, model_spec=None, outputs=None):
        super().__init__(predict_pb2.PredictResponse(), model_spec, outputs)

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

