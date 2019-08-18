import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
import time
import base64
import requests
import pickle
import numpy as np
import random


def prepare_grpc_request(model_name, signature_name, data):
    request = predict_pb2.PredictRequest()
    request.model_spec.name = model_name
    request.model_spec.signature_name = signature_name
    request.inputs[input_name].CopyFrom(
        tf.contrib.util.make_tensor_proto(data, dtype=None))
    return request


model_name = 'model'
signature_name = 'predict_images'
input_name = 'images'
input_type = None
batch_size = 1

n_grpc_string = 10000
n_grpc_arr = 10000
n_rest_string = 10000
n_rest_arr = 10000

input_size = 10000

with open("./mnist_image.png", 'rb') as f:
    string = f.read()

string = ''.join([random.choice('abcdefghijklmnopqrst><1234567890:') for _ in range(input_size)])

with open("./mnist_image.pkl", 'rb') as f:
    arr = pickle.load(f)

arr = [random.randint(0, 10000) for _ in range(input_size)]

batch = np.repeat(string, batch_size, axis=0).tolist()

print("--gRPC--")
start = time.time()
for _ in range(n_grpc_string):
    request = prepare_grpc_request(model_name, signature_name, batch)

duration = float(time.time() - start)
rate = n_grpc_string*batch_size/duration
print("String: %f ser/sec" % rate)

batch = np.repeat(arr, batch_size, axis=0).tolist()

start = time.time()
for _ in range(n_grpc_arr):
    request = prepare_grpc_request(model_name, signature_name, batch)

duration = float(time.time() - start)
rate = n_grpc_arr*batch_size/duration
print("Numpy array: %f ser/sec" % rate)


print("--REST--")

batch = np.repeat(string, batch_size, axis=0).tolist()
start = time.time()
for _ in range(n_rest_string):
    batch_for_json = [{'b64': base64.b64encode(x)} for x in batch]
    json = {
        "signature_name": signature_name,
        "instances": batch_for_json
    }

    with requests.Session() as sess:
        req = requests.Request('post', "http://x:1/v1/models/model:predict", json=json)
        prepped = sess.prepare_request(req)

duration = float(time.time() - start)
rate = n_rest_string*batch_size/duration
print("String: %f ser/sec" % rate)


batch = np.repeat(arr, batch_size, axis=0).tolist()
start = time.time()
for _ in range(n_rest_arr):
    json = {
        "signature_name": signature_name,
        "instances": batch
    }

    with requests.Session() as sess:
        req = requests.Request('post', "http://x:1/v1/models/model:predict", json=json)
        prepped = sess.prepare_request(req)

duration = float(time.time() - start)
rate = n_rest_arr*batch_size/duration
print("Numpy array: %f ser/sec" % rate)
