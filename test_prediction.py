from PIL import Image
import numpy as np

from prediction_service import PredictRequest, PredictResponse, PreditionService
from pbs import ModelSpec

def preprocess_image(img_file, input_height=224, input_width=224):
    data = Image.open(img_file)
    data = data.resize((input_height, input_width), 1)
    data = np.asarray(data).astype(np.float32)
    return data/255

model_spec = ModelSpec(name='ods_cls', version=3, signature_name='serving_default')

data = preprocess_image('/home/jagan-s/Jagan/Projects/Serving/occupancy_detection_system/client/ods_test_data/drinking1.jpg')
inputs = {'image': data}

server = '192.168.94.49:8500'
timeout = 5

predict_request = PredictRequest(model_spec)
predict_request.read_inputs(**inputs)

predict_service = PredictionService(server, timeout)
predict_response = predict_service.predict(predict_request)

predict_response.parse_outputs()
