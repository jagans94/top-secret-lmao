# **Design** Considerations

### API consistency

The library abstracts away working directly with protocol buffers and replaces that with wrapper

Simply put, what you put in i

If the return object of a method is a protocol buffer message, then the message should be wrapped using  transformed to a wrapper object which implements custom functions and  of the class corresponding to the protocol buffer message defined.

The wrapper is built on top of protocol buffers `message` type. The whole idea of the wrapper is to abstract away the fact that you're working with protocol buffers and simplify 

### Mirroring:

The idea is to  mirror the internal state of the child `pb` inside the parent `pb`  using a wrapper, without breaking chain assignment while providing consistency across APIs. 

Only implemented for non-scalar, singular and repeated fields, a.k.a. the message and repeated message types. 

**Fact:** Protocol buffer messages generated from the compiled `.proto` files can consist of nested protocol buffer, i.e. `pb` messages.

When performing a `getattr` on the parent `pb` message for fetching a child `pb` message, things get a little tricky. 

- Firstly, the returned object should be a wrapped child `pb` message for API consistency. However, wrapping with an ad-hoc wrapper is a bad idea, since this would break [chain assignment]().
- Secondly, the wrapped child `pb` message should reflect the state of the child `pb` message as is in the parent `pb` message.

To implement this, we return a wrapped child `pb` message instead of the child `pb`message itself. The wrapper is treated as a static property of the wrapped parent `pb` message. The internal state of the child `pb` message is copied into the wrapper object before returning. To reiterate, this allows for consistency in internal state when accessing the attribute through the dot `(.)` operator as well as API 

This is only implemented for Messages nested as static attributes of parent messages, a.k.a child messages.

When retrieving child messages using `getter` method/s, the respective protocol buffer should be returned as instances of their corresponding wrapper class in order to maintain consistency across the API. 

Main issues:

- The returned message should not be wrapped in an ad-hoc wrapper, since this would break *<u>chain getting/setting of values</u>* supported by `protobuf`. [Link]()
- Violates an important design consideration, i.e. **"Don't replace or break what's already working. Augment it!"**

Proposed two part solution (discussed in chain getting/setting and mirroring):

- The returned message should implement a static attribute look-up for the wrapped instance to avoid unneeded wrapper generation on calls to the `getter` method/s while returning a static wrapped instance which reflects the protocol buffer of the child message. This makes sure the returned o
- Assigning values to internal attributes of a child message should reflect in 





The first is chained getting, i.e. any operator/function which upon invocation can/does change the state of the child message, but is  returns and the other chained  This is done by initialising the wrapped child message as a property of the parent message wrapper. The wrapped child message [mirrors]() the child pro

- This gett

### Don't replace what's already working. Augment it!

### Chain getting/setting:

### Design Considerations

### Compiled Python Code:  <WHY ARE YOU TELLING THIS>

Each message defined in the `.proto` files can (and some do) consist of multiple nested messages and  complex (i.e. read as repeated, map) scalar as well as non-scalar fields. The compiler doesn't generate your data access code for you directly. Instead, it generates special descriptors for all your messah

ges, enums, and fields, and some mysteriously empty classes, one for each message type and uses uses [Python metaclass](https://docs.python.org/2.7/reference/datamodel.html#metaclasses) to do the real work. 

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

**The idea:** Don't replace the internal mechanism, but augment it. 

The wrapper around `protobuf` messages aims to provide a flexible pythonic interface while also preserving the flexibility that comes in-built with it as part of  `google.protobuf`  library as well as provide an easier way of interfacing with some functionalities that's always used. <EDIT LATER>

It does this in the following way:

1. Exposes general `protobuf` functionalities to allow manipulation of internal attributes in an easy format <REWRITE WHAT THIS MEANS>
2. Complex fields/attributes in `protobuf` cannot be assigned to directly using `setattr` or `=` sign. To overcome this, the library provides custom `getter` and `setter` methods that allow such direct manipulation.
3. Issue with nested message fields: What do I return if the attribute of a `protobuf` message is another message? Well, to retain consistency across the API. 

Want to add

## 



