'''
Typical Usage:

reload_config_request = ReloadConfigRequest()
reload_config_request.extend(*configs)

model_service = ModelService(server, timeout)
reload_config_response = model_service.reload_config(reload_config_request)

print(reload_config_response)
'''

import grpc
from tensorflow_serving.apis import model_service_pb2_grpc
from tensorflow_serving.apis import get_model_status_pb2
from tensorflow_serving.apis import model_management_pb2
from tensorflow_serving.config import model_server_config_pb2

from base import _Message, _GRPCService
from pbs import ModelConfig


class ReloadConfigRequest(_Message):
    def __init__(self, config_list=None):
        super().__init__(model_management_pb2.ReloadConfigRequest(), config_list)
    
    def extend(self, *configs):
        cfg_pbs = [c.protobuf for c in configs]
        self.protobuf.model_config_list.extend(cfg_pbs)

class ReloadConfigResponse(_Message):
    def __init__(self, status=None):
        super().__init__(model_management_pb2.ReloadConfigResponse(), status)

    # add methods to process status

class GetModelStatusRequest(_Message):
    def __init__(self, model_spec=None):
        super().__init__(get_model_status_pb2.GetModelStatusRequest(),model_spec)
    
class GetModelStatusResponse(_Message):
    def __init__(self, model_version_status=None):
        super().__init__(get_model_status_pb2.GetModelStatusResponse(), model_version_status)

class ModelService(_GRPCService):
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
