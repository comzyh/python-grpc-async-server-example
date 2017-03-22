# encoding: utf-8
import grpc
import time

from concurrent import futures
from threading import current_thread
from collections import defaultdict

import tensorflow as tf
import numpy as np

import protocol.example_pb2
import protocol.example_pb2_grpc


sessions = None
input_ph = None
task = None


def get_graph():
    input_ph = tf.placeholder(tf.float64, shape=(1024, 1024))
    x = input_ph
    for i in range(1000):
        x = x * x
    print('get_graph', x.graph)
    sess = tf.Session(
        # config=tf.ConfigProto(allow_soft_placement=True,
        #                       inter_op_parallelism_threads=1,
        #                       intra_op_parallelism_threads=1
        #                       ),
        graph=x.graph
    )
    sess.run(tf.global_variables_initializer())
    return input_ph, x


def new_session():
    sess = tf.Session(
        # config=tf.ConfigProto(allow_soft_placement=True,
        #                       inter_op_parallelism_threads=1,
        #                       intra_op_parallelism_threads=1
        #                       ),
        graph=task.graph,
    )
    # sess.run(tf.global_variables_initializer())
    return sess


class ExampleServer(protocol.example_pb2_grpc.ExampleServiceServicer):

    def Compute(self, request, context):
        question = request.question
        print('accept {}'.format(question))
        sess = sessions[current_thread().name]
        x = np.random.rand(1024, 1024)
        ret = sess.run(task, feed_dict={input_ph: x})
        print("current_thread: {}, question: {}".format(current_thread().name, question))

        return protocol.example_pb2.ComputeResponse(answer=question)


def serve():
    global sessions, input_ph, task
    sessions = defaultdict(new_session)
    print('Building graph')
    input_ph, task = get_graph()
    print('Finish Build graph')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
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
