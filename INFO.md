### Required set of `.proto` files:

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

This is done to provide a sensible and easy-to-use abstraction layer around the compiled`protobuf`

## Design Considerations

### Exposing `protobuf`

Each message in the `.proto` files inside `tensorflow_serving` or `tensorflow` library consists of multiple nested messages and complex singular as well as non-singular fields. Wrapping around each `protobuf` is good OO approach, which allows for increased customisation and control over `protobuf` objects. However, IMO only those APIs should be exposed to the user, which are required for constructing thevs sensible interface abstraction that can be justified, by  to open up. to decide the level of granularity to when dOne can define granularity

How much to expose vs how much to hide behind programmatic construction?

- Auto magic vs Control

<More clarification required>

### Getting and Setting attributes

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

### Why?

- Number of LOCs saved. <QUANTIFY>
- Consolidated implementation.
- Simpler interface, i.e. more pythonic.
- No external dependencies <if `make_tensor_proto` and `make_ndarray` are implemented organically>

## WRAPPER

### TO DO:

- [ ] Annotate message fields/attributes with types by commenting with appropriate type reference (as an alternative to static typing).
- [ ] Managing dependencies, i.e. restructuring the files and APIs.
- [ ] Create a custom list/map data containers for message types. 
  - [x] List
  - [ ] Map
- [ ] Write generic test script for the following:
  - Reading from and writing to a file in both text and binary format.
  - Test expected attribute input and output type for each wrapper.
- [ ] Check `id()` for every returned item/instance using `getattr`, i.e. to make sure the wrappers are not created newly each time. If so, implement a static attribute look-up to avoid unneeded wrapper generation.

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

- Custom container implementation i.e. MessageList, MessageMap support most of the methods expected of the class (as suggested by the name). However, certain methods such as splicing and probably many more i.e. <INSERT METHODS HERE> are not supported, but can be implemented as required.

## gRPC

### TO DO:

- [ ] Concurrent Asynchronous Requests

- [ ] Write a mock server, for downloading model to a specified folder based around on `ReloadConfigRequest`.
- [ ] Authentication <OUT OF SCOPE>



