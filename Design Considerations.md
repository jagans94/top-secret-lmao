# **Design** Considerations

**Note:** `protobuf` and `pb` interchangeably refer to the same thing, i.e. protocol buffers object.

## Guidelines:

1. Don't change what's already working.
2. Where change is required, do so in a complementary way.

## Simplicity and Customisation

The wrapper provides one-line invocation for many useful  `protobuf` functions as well as extends it in different ways for specific `protobuf` message/service definitions. 

Most of the methods that accept a wrapped `pb` instance also work fine with the internal `pb` message.

## Getting and Setting attributes

Simplifying interface for setting some complex `attr`s (i.e. nested `pb` messages, `ListValue` instances etc.) that can't be set directly is done by customising the derived class. 

This makes sense, since each `protobuf` definition is different, which is done by writing custom `getter` and `setter` methods for the necessary `protobuf` attributes.

## API consistency

The library abstracts away working directly with protocol buffers. It does so by providing a wrapper class around each definition.

As a principle, it doesn't expect the user to work with protocol buffers directly, even though that's an option, but instead work with the abstraction layer provided as part of the library. 

This is especially true while returning nested `pb` message attributes from inside a parent `pb` message. The nested `pb` message is wrapped in a corresponding class to provide a consistent API interface.

## Mirroring

In order to provide API consistency, without breaking features that made working with `protobuf` great in the first place,  we simply replicate/mirror the ***internal*** (part of the internal `protobuf` object) nested `pb` message attribute to an ***external*** (part of the wrapper, but exists outside of the internal `protobuf` object) `pb` wrapped message attribute. 

The external attribute is attached to the parent `pb` wrapper message, in a way so as to reflect any changes in the internal `protobuf` state, i.e. through chained assignment. 

This only applies to non-scalar (singular and repeated) fields, a.k.a. the message and repeated message types.  For scalar (singular or repeated) fields, the `getter` and `setter` methods directly exposes the internal `protobuf` state.

## Chained Assignment

Here's an example to explain what chained assignment looks like. Let's say we want to initialise a predict request. It goes something like this:

```python
model_spec = ModelSpec(name='mnist', signature_name='serving_default', version=1)
predict_request = PredictRequest(model_spec=model_spec)
```

## Response messages and wrappers

Response `pb` messages shouldn't be modifiable unless we want to insert some business logic into it and thereby transform it for delayed consumption. 

Response wrappers provide a non-mutable interface to the underlying response `pb` .

To be explicit, any modifications to the the response object can only be done directly on the internal `pb` message.

## Catching Errors

Since, `google.protobuf.message` takes care of handling most of the errors, it shouldn't be a problem. 

IMO, letting  errors percolate with sensible warnings should be the way to go, i.e. shouldn't cause the user to go mad. 

## Limitations

Currently, the main limitation is in the form of chained assignment on items inside `MessageList` container. `MessageList` container wraps around repeated message type (objects that are sometimes found in a `protobuf` definition) which for almost all purposes act like a python `list` object.

Another limitation is the current dependency on TensorFlow library for converting `np.array` inputs to `tensor_proto` and vice-versa. Though, the code for the that can be divorced from the TensorFlow library, some dependencies are too long or complicated to trace back and support. Therefore, right now a simple adaptation of the code is used, where required.





