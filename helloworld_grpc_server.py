#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   helloworld_grpc_server.py    
@Author  :   wangyawen
@Modify Time :  2021/1/23 下午10:53
@Version    :   1.0
"""
from concurrent import futures
import time
import grpc
import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    """
    实现proto文件中定义的GreeterServicer
    """

    def SayHello(self, request, context):
        """
        实现proto 文件中定义的rpc调用
        :param request:
        :param context:
        :return:
        """
        return helloworld_pb2.HelloReply(message='hello {msg}'.format(msg=request.name))

    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloReply(message='hello {msg}'.format(msg=request.name))


def server():
    # 启动rpc服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    server()
