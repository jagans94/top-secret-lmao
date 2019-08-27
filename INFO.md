# INFO:

### Minimal set of required `.proto` files:

- `serving_repo/tensorflow_serving/apis/*.proto`
- `serving_repo/tensorflow_serving/config/model_server_config.proto`
- `serving_repo/tensorflow_serving/core/logging.proto`
- `serving_repo/tensorflow_serving/core/logging_config.proto`
- `serving_repo/tensorflow_serving/util/status.proto`
- `serving_repo/tensorflow_serving/sources/storage_path/file_system_storage_path_source.proto`
- `serving_repo/tensorflow_serving/config/log_collector_config.proto`
- `tensorflow_repo/tensorflow/core/framework/tensor.proto`
- `tensorflow_repo/tensorflow/core/framework/tensor_shape.proto`
- `tensorflow_repo/tensorflow/core/framework/types.proto`
- `tensorflow_repo/tensorflow/core/framework/resource_handle.proto`
- `tensorflow_repo/tensorflow/core/example/example.proto`
- `tensorflow_repo/tensorflow/core/protobuf/tensorflow_server.proto`
- `tensorflow_repo/tensorflow/core/example/feature.proto`
- `tensorflow_repo/tensorflow/core/protobuf/named_tensor.proto`
- `tensorflow_repo/tensorflow/core/protobuf/config.proto`

### TLDR: What's this?

The implementation has two main parts:

1. A wrapper around compiled `protobuf` objects/instances in the `tensorflow_serving` and `tensorflow` repositories required for performing client calls to a hosted`tensorflow_model_server`.
2. A gRPC based client wrapper which interfaces with the wrapped `protobuf` instances to perform client calls.

# Motivation:

**TLDR:** If it ain't broke, don't fix it. So I improved it. (*subjective*) ;) 

-  Working with `protobuf` should be simple, i.e. the message objects should work like any other python objects. They don't! 
- Tensorflow Serving documentation doesn't cover client API in gRPC, and there is little available, mostly sparse, reference for implementing the gRPC clients. The [link](https://www.tensorflow.org/tfx/serving/api_rest) to gRPC client API is `grpc_tools` compiled code, which is to say not much actually :(

# Why?

I ask myself this now and then, so once for all, I'm putting it **down** in *mark____*.  ;P

The repo started as a by-product of working with [Tensorflow Serving](https://www.tensorflow.org/tfx/guide/serving), mostly focusing on implementing a distributed serving mechanism for all models `tensorflow` and otherwise.

I just wanted a simple, consolidated (even if not complete ;) ) gRPC-based client library (which ended up taking me down this rabbit hole) as well as testing whether gRPC is superior to REST for querying the hosted models and if so leverage it. 

Now, I know! <BENCHMARKED RESULTS HERE>

# Idea

**The idea:** Don't replace the internal mechanism, but augment it. 

The wrapper around `protobuf` messages aims to provide a flexible pythonic interface while also preserving the flexibility that comes in-built with it as part of  `google.protobuf`  library as well as provide an easier way of interfacing with some functionalities that's always used. <EDIT LATER>

It does this in the following way:

1. Exposes general `protobuf` functionalities to allow manipulation of internal attributes in an easy format <REWRITE WHAT THIS MEANS>
2. Complex fields/attributes in `protobuf` cannot be assigned to directly using `setattr` or `=` sign. To overcome this, the library provides custom `getter` and `setter` methods that allow such direct manipulation.
3. Issue with nested message fields: What do I return if the attribute of a `protobuf` message is another message? Well, to retain consistency across the API. 

# FAQs

Q: Hey, there's a lot of replicated logic here? Have you tried defining custom [descriptors](https://docs.python.org/3/howto/descriptor.html)?

A: I know. Want to PR? :)

# Future

- [ ] Service reflection
- [ ] Bench-marking vs REST API endpoints
- [ ] 



# Future (General)

- [ ] Add some insane stuff here. 
- [ ] 

## Why?

- Allow easy manipulation of `protobuf` instance with simple function calls.
- Abstract away the necessity to know the internal`protobuf` implementation and replace them with simple (probably), well-defined interface. ;) [Refer Here]() <POINT TO APPROPRIATE RESOURCE>
- <QUANTITY> number of LoCs saved. [Refer Here]() <POINT TO APPROPRIATE RESOURCE> <AN IMAGE MAYBE>
- A consolidated, extensible gRPC-based client implementation for querying `tensorflow_model_server` or it's variant, i.e. mainly `PredictionService` and `ModelService` services.
- A native, organic implementation, sidestepping heavy dependencies installation `tensorflow`  library. <UTILS NEEDS TO BE DIVORCED>
- Simpler interface, i.e. more pythonic.

### Design Considerations

### Compiled Python Code:  <WHY ARE YOU TELLING THIS>

Each message defined in the `.proto` files can (and some do) consist of multiple nested messages and  complex (i.e. read as repeated, map) scalar as well as non-scalar fields. The compiler doesn't generate your data access code for you directly. Instead, it generates special descriptors for all your messages, enums, and fields, and some mysteriously empty classes, one for each message type and uses uses [Python metaclass](https://docs.python.org/2.7/reference/datamodel.html#metaclasses) to do the real work. 

### Getting and Setting attributes:

Simplifying interface for setting some complex `attr`s that can't be set directly should be done by customising the derived class to manage around the said `attr`s. This makes sense, since each `protobuf` definition is different. This can be done by writing custom `getter` and `setter` methods for the necessary `protobuf` attributes.

### Catching Errors

Since, `google.protobuf.message` takes care of handling most of the errors, it shouldn't be a problem. IMO, letting  errors percolate with sensible warnings should be the way to go, i.e. shouldn't cause the user to go mad. 

### Nested Messages: 

### `protobuf`

Each wrapper class contains a private `protobuf` attribute, which is an instance of the compiled `.proto` file.  Nested child messages, i.e. provided either during initialisation or otherwise, are unwrapped before applying methods from `google.protobuf` library. 

Two major issues:

1. The nested child message is always considered to be an instance of the wrapper class.
2. Every input method accepting such instance, should need to unwrap the object before processing it.

<More clarification required>

### Internal vs External:

Each wrapper class contains a private `protobuf` attribute, which is an instance of a protocol buffer message compiled from the corresponding `.proto` file.  Each protocol buffer message can consist of nested child messages, which results in two main complications while working with them:

- The child messages (as well as other non-singular fields) cannot be assigned directly. They can be assigned, by setting any of the attributes of the child message or by calling `SetInParent()` method on the said child message.
- The wrapper, i.e. the `Message` class and its sub-classes, abstract around the protocol buffer

### Request vs Response:

Shouldn't be able to set values to response attributes; therefore initialisation support can be removed.

### Defining Message Classes:

Non-complicated message types that who values can be set and gotten easily remain non-modified and in general not implemented. 

However, complicated ones are broken down to make easier pythonic interfaces.

Reusable (across APIs) dependencies are defined separately, whereas dependencies specific to a single (or an already grouped set of APIs) are defined along with the corresponding APIs.

### Duck Typing

Placeholder

### Mirroring:

Check `id()` for every returned item/instance using `getattr`, i.e. to make sure the wrappers are not created newly each time. If so, implement a static attribute look-up to avoid unneeded wrapper generation.

### Why?

- 

## WRAPPER

### TO DO:

- [x] Annotate message fields/attributes with types by commenting with appropriate type reference (as an alternative to static typing).
- [x] Managing dependencies, i.e. restructuring the files and APIs.
- [ ] Create a custom list/map data containers for message types. 
  - [x] List
  - [ ] Map
- [ ] Write generic test script for the following:
  - Write down expected behaviours for each wrapper class and write a test function covering general aspects.

### Limitations:

- Chained attribute access doesn't work, i.e.

  ```python
  model_spec = ModelSpec(name='mnist')
  pred_req = PredictRequest(model_spec=model_spec)
  pred_req.model_spec
  # >>> name: "mnist"
  pred_req.model_spec.name = '12'
  pred_req.model_spec # i.e. the initial value doesn't change
  # >>> name: "mnist" 
  
  # To overcome this, set the child attribute directly
  pred_req.model_spec = ModelSpec(name='12')
  pred_req.model_spec
  # >>> name: "12" 
  ```

- Custom container implementation i.e. MessageList support most of the methods expected of the class (as suggested by the name). However, certain methods such as splicing and probably many more i.e. <INSERT METHODS HERE> are not supported, but can be implemented as required.

## gRPC

### TO DO:

- [ ] Concurrent Asynchronous Requests

- [ ] Write a mock server, for downloading model to a specified folder based around on `ReloadConfigRequest`.
- [ ] Authentication <OUT OF SCOPE>



