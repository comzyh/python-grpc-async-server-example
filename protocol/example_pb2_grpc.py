import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import protocol.example_pb2 as protocol_dot_example__pb2
import protocol.example_pb2 as protocol_dot_example__pb2


class ExampleServiceStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Compute = channel.unary_unary(
        '/example_service.ExampleService/Compute',
        request_serializer=protocol_dot_example__pb2.ComputeRequest.SerializeToString,
        response_deserializer=protocol_dot_example__pb2.ComputeResponse.FromString,
        )


class ExampleServiceServicer(object):

  def Compute(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ExampleServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Compute': grpc.unary_unary_rpc_method_handler(
          servicer.Compute,
          request_deserializer=protocol_dot_example__pb2.ComputeRequest.FromString,
          response_serializer=protocol_dot_example__pb2.ComputeResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'example_service.ExampleService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
