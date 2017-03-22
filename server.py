# encoding: utf-8
import grpc
import time

from concurrent import futures

import protocol.example_pb2
import protocol.example_pb2_grpc


class ExampleServer(protocol.example_pb2_grpc.ExampleServiceServicer):

    def Compute(self, request, context):
        question = request.question
        print(question)
        time.sleep(2)

        return protocol.example_pb2.ComputeResponse(answer=question)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protocol.example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleServer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
