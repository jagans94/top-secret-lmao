# Simple TensorFlow Serving Client

## What's is it?

A simple, consolidated, extensible [gRPC](https://grpc.io/)-based client implementation for querying a hosted`tensorflow_model_server`.

**What it does do?**

It simplifies working with [protocol buffers](https://developers.google.com/protocol-buffers/) and provides custom functions to manipulate and change the internal state of certain [Tensorflow Serving](https://www.tensorflow.org/tfx/guide/serving) protocol buffer definitions, all without leaving the comfort of python. 

Implements `GetModelMetadata`, `GetModelStatus`, `HandleReloadConfig` and `Predict` APIs.

**What it doesn't do?**

It doesn't completely abstract away working with protocol buffers. The internal protocol buffer can still be accessed and manipulated using methods specific to protocol buffers. This is preferred when working with gRPC clients that expect raw protocol buffers.

## Motivation:

I ask myself this now and then, so once for all, I'm putting it **down** in *mark____*.  ;P

- Working with `protobuf` should be simple, i.e. the message objects should work like any other python objects. They don't! (specifically, getting and setting values)
- Tensorflow Serving documentation doesn't cover [gRPC client API](https://github.com/tensorflow/serving/tree/master/tensorflow_serving/apis), and there is little available, mostly sparse, reference for implementing the gRPC clients for TensorFlow Serving.
- If it ain't broke, don't fix it, improve it. ~*subjective*~

The repo started as a by-product of working with Tensorflow Serving, mostly focusing on implementing a distributed serving mechanism for all models [Tensorflow](https://www.tensorflow.org/) and otherwise.

## How to start using it?

### Install client:

```bash
pip install <>
```

### Install `tensorflow_model_server` server on Debian/Ubuntu:

**Note:** Run as `sudo`

```bash
echo "deb http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | tee /etc/apt/sources.list.d/tensorflow-serving.list && \
curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | apt-key add -
apt update
apt-get install tensorflow-model-server
```

### Tutorial:

<PLACeHOLDER>

## Benchmarks

 ![](https://github.com/jagans94/top-secret-lmao/blob/master/tests/latency-comp-mnist.png)

gRPC predict requests have a lot smaller latency profile (approx. 6 times faster) when compared with REST based requests on MNIST data set! :)

**Note:** Code for bench marking can be found at  `tests/comparison_http_vs_grpc_prediction_request_response.ipynb`

## To Do:

### General

- [ ] Documentation

### Message

- [ ] Reduce replicated `property` logic by defining custom [descriptors](https://docs.python.org/3/howto/descriptor.html).
- [ ] Implement `Classify`,  `Regress` and `MultiInference` APIs.
- [ ] Write test script for expected behaviours for each wrapper class as well as a generic test suite covering the base class implementation.
- [ ] Add parser for reading `signature_def` from  `GetModelMetadataResponse`.

### gRPC

- [ ] Add examples for asynchronous requests.
- [ ] Create a gRPC service for downloading a model from a blob store on client request. 
- [ ] Create  gRPC service for querying latest versions available from a blob store and making them available automatically, based on policy, etc.
- [ ] Support authentication (gRPC already supports authentication. However, the wrapper around the gRPC client services uses `insecure_channel` for communication. Ideally, I'd like to extend authentication support for  both client, i.e. this library and server, i.e. hosted  `tensorflow_model_server` using the many already in-built authentication mechanisms as well as custom plugins)
- [ ] Add more bench-marking tests for gRPC vs REST API endpoints.

## Contributions:

Want to add a feature that's not in here or implement the ones above. Raise an **Issue** or better yet **PR**. ;)
