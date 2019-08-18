import grpc
from model_service import ReloadConfigRequest, ReloadConfigResponse, ModelService, ModelConfig
from model_service import ModelService, ModelConfig

if __name__ == "__main__":
    config_1 = ModelConfig(name='mnist', base_path='/models/mnist', model_platform='tensorflow')

    reload_config_request = ReloadConfigRequest()
    print(reload_config_request.describe())
    reload_config_request.extend([config_1])
    
    model_service = ModelService('192.168.94.94:8500', 5)
    reload_config_response = model_service.reload_config(reload_config_request)
    
    print(reload_config_response)
    