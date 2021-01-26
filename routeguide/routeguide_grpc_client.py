#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   routeguide_grpc_client.py    
@Author  :   wangyawen
@Modify Time :  2021/1/26 下午2:58
@Version    :   1.0
"""
import grpc
import routeguide.routeguide_pb2 as routepb
import routeguide.routeguide_pb2_grpc as routepbgrpc
import routeguide.routeguide_db as routedb
import random


def get_feature(feature):
    """
    通信方式1
    :param feature:
    :return:
    """
    if not feature.location:
        print("server returned incomplete feature")
        return
    if feature.name:
        print("feature called {name} at {location}".format(name=feature.name, location=feature.location))
    else:
        print("found no feature at {location}".format(location=feature.location))


def generate_route(feature_list):
    """
    从原数据列表中随机获得20个数据点point
    :param feature_list:
    :return:
    """
    for _ in range(0, 20):
        random_feature = feature_list[random.randint(0, len(feature_list) - 1)]
        print("random feature {name} at {location}".format(
            name=random_feature.name, location=random_feature.location
        ))
        yield random_feature.location


def make_route_node(message, latitude, longitude):
    return routepb.RouteNote(
        message=message,
        location=routepb.Point(latitude=latitude, longitude=longitude)
    )


def generate_route_note():
    """
    构建点
    :return:
    """
    msgs = [
        make_route_node('msg 1', 0, 0),
        make_route_node('msg 2', 1, 0),
        make_route_node('msg 3', 0, 1),
        make_route_node('msg 4', 0, 0),
        make_route_node('msg 5', 1, 1),
    ]
    for msg in msgs:
        print("send message {message} location {location}"
              .format(message=msg.message, location=msg.location))
        yield msg


def run():
    """
    客户端运行函数：
    发送请求+接收response
    实现四种通信交互
    :return:
    """
    # 连接service
    channel = grpc.insecure_channel('localhost:50051')
    stub = routepbgrpc.RouteGuideStub(channel)

    # 通信方式1
    """
    GetFeature(Point)
    """
    print("----------GetFeature----------")
    # 从服务中获得地点对应的feature
    response = stub.GetFeature(routepb.Point(latitude=409146138, longitude=-746188906))
    # 将response传到函数中输出结果
    get_feature(response)
    response = stub.GetFeature(routepb.Point(latitude=0, longitude=-0))
    get_feature(response)

    print("----------ListFeature----------")
    # 通信方式2
    """
    ListFeature(Rectangle):返回矩形中的点
    """
    response = stub.ListFeature(routepb.Rectangle(
        lo=routepb.Point(latitude=400000000, longitude=-750000000),
        hi=routepb.Point(latitude=420000000, longitude=-730000000)
    ))
    for feature in response:
        print("Feature called {name} at {location}"
              .format(name=feature.name, location=feature.location))

    print("----------RecordRoute----------")
    # 通信方式3
    """
    RecordRoute(route_iterator)向服务器发送许多点的信息
    返回统计信息RouteSummary
    """
    # 读取获得db列表
    feature_list = routedb.read_routeguide_db()
    # 随机获得20个数据点point
    route_iterator = generate_route(feature_list)
    # 获取服务的RecordRoute
    response = stub.RecordRoute(route_iterator)
    print("point count:{point_count} feature count:{feature_count} "
          "distance:{distance} elapsed time:{elapsed_time}"
          .format(point_count=response.point_count,
                  feature_count=response.feature_count,
                  distance=response.distance,
                  elapsed_time=response.elapsed_time))

    print("----------RouteChat----------")
    # 通信方式4
    """
    RouteChat
    """
    # generate:先生成点
    response = stub.RouteChat(generate_route_note())
    for msg in response:
        print("received message {message} location {location}"
              .format(message=msg.message, location=msg.location))


if __name__ == '__main__':
    run()
