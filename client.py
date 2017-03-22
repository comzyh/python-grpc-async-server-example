# encoding: utf-8
import grpc
from concurrent import futures
from protocol import example_pb2
from protocol import example_pb2_grpc


def client(question):
    channel = grpc.insecure_channel('[::]:50055')
    stub = example_pb2_grpc.ExampleServiceStub(channel)
    resp = stub.Compute(example_pb2.ComputeRequest(question=question))
    print((question, resp.answer))


def main():
    executor = futures.ThreadPoolExecutor(max_workers=10)
    for i in range(100):
        executor.submit(client, str(i))
    executor.shutdown()
    print('Exit')
    # input()


if __name__ == '__main__':
    main()
