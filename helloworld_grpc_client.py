#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   helloworld_grpc_client.py    
@Author  :   wangyawen
@Modify Time :  2021/1/23 下午10:53
@Version    :   1.0
"""
import grpc
import helloworld_pb2_grpc
import helloworld_pb2


def run():
    # 连接rpc服务器
    channel = grpc.insecure_channel('localhost:50051')
    # 调用rpc服务
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='test1'))
    print("Greeter client received : " + response.message)
    response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='test22'))
    print("Greeter client received : " + response.message)


if __name__ == '__main__':
    run()