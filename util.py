from tensorflow_serving.util import status_pb2

from base import Message

class Status(Message):
    def __init__(self, error_code=None, error_message=None, **kwargs):
        super().__init__(status_pb2.StatusProto(),
                         error_code=error_code,
                         error_message=error_message,
                         **kwargs)
    # type: enum
    @property
    def error_code(self):
        return self._protobuf.error_code

    @error_code.setter
    def error_code(self, _error_code):
        self._protobuf.error_code = _error_code

    # type: string
    @property
    def error_message(self):
        return self._protobuf.error_message

    @error_message.setter
    def error_message(self, _error_message):
        self._protobuf.error_message = _error_message

    # TODO: Add method to parse `error_code`.