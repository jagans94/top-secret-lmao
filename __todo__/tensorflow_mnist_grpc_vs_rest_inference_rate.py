import pickle
import numpy as np
import time
import requests
import subprocess
import re
from grpc.beta import implementations
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2


# returns the network IN traffic size for a given container
def get_network_i(container_name):
    command = 'docker stats --no-stream --format "table {{.NetIO}}" %s' % container_name
    proc = subprocess.Popen(['bash', '-c', command], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    object = proc.communicate()
    output = object[0]
    return float(re.sub("[^0-9.]", "", str.split(str.split(output, "\n")[1], '/')[0]))


def prepare_grpc_request(model_name, signature_name, data):
    request = predict_pb2.PredictRequest()
    request.model_spec.name = model_name
    request.model_spec.signature_name = signature_name
    request.inputs[input_name].CopyFrom(
        tf.contrib.util.make_tensor_proto(data, dtype=None))
    return request


host = 'localhost'
grpc_container_name = 'tf_serving_mnist1'
rest_container_name = 'tf_serving_mnist2'
grpc_port = '8500'
rest_port = '8501'
batch_size = 100
num_of_requests = 1000
model_name = 'model'
signature_name = 'predict_images'
input_name = 'images'
image_path = "./mnist_image.pkl"

with open(image_path, 'rb') as f:
    image = pickle.load(f)
print("input shape: %s" % str(np.shape(image)))
batch = np.repeat(image, batch_size, axis=0).tolist()
print("creating batch. Now shape is: %s" % str(np.shape(batch)))
image_cnt = num_of_requests * batch_size
print("total number of images to be sent: %d" % image_cnt)

channel = implementations.insecure_channel(host, int(grpc_port))
stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

# gRPC
print("starting gRPC test...")
print ("warming up....")
request = prepare_grpc_request(model_name, signature_name, batch)
stub.Predict(request, timeout=600)
grpc_start_net = get_network_i(grpc_container_name)

total_start = time.time()
for _ in range(num_of_requests):
    request = prepare_grpc_request(model_name, signature_name, batch)
    response = stub.Predict(request, timeout=600)

total_duration = float(time.time() - total_start)
grpc_rate = image_cnt / total_duration
grpc_end_net = get_network_i(grpc_container_name)
grpc_net = grpc_end_net - grpc_start_net
print("--gRPC--\n"
      "Duration: %f secs -- requests: %d -- images: %d -- batch size: %d -- rate: %f img/sec -- net: %s"
      % (total_duration, num_of_requests, image_cnt, batch_size, grpc_rate, grpc_net))

# REST
print("starting REST test...")
json = {
    "signature_name": signature_name,
    "instances": batch
}
print ("warming up....")
req = requests.Request('post', "http://%s:%s/v1/models/model:predict" % (host, rest_port), json=json)
rest_start_net = get_network_i(rest_container_name)

total_start = time.time()
for _ in range(num_of_requests):
    response = requests.post("http://%s:%s/v1/models/model:predict" % (host, rest_port), json=json)

total_duration = float(time.time() - total_start)
rest_rate = image_cnt / total_duration
rest_end_net = get_network_i(rest_container_name)
rest_net = rest_end_net - rest_start_net
print("--REST--\n"
      "Duration: %f secs -- requests: %d -- images: %d -- batch size: %d -- rate: %f img/sec -- net: %s"
      % (total_duration, num_of_requests, image_cnt, batch_size, rest_rate, rest_net))

print("--Summary--\n"
      "Inference rate ratio (REST/gRPC): %f" % (rest_rate / grpc_rate))
