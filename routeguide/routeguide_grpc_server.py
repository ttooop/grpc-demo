#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   routeguide_grpc_server.py    
@Author  :   wangyawen
@Modify Time :  2021/1/26 下午1:51
@Version    :   1.0
"""
from concurrent import futures
import math
import time
import grpc
import routeguide.routeguide_pb2 as routepb
import routeguide.routeguide_pb2_grpc as routepbgrpc
import routeguide.routeguide_db as routedb


def get_feature(db, point):
    """
    拿point到db中匹配，返回db中匹配到的数据
    :param db:
    :param point:
    :return:
    """
    for feature in db:
        if feature.location == point:
            return feature
    return None


def get_distance(start, end):
    coord_factor = 10000000.0
    lat_1 = start.latitude / coord_factor
    lat_2 = end.latitude / coord_factor
    lon_1 = start.longitude / coord_factor
    lon_2 = end.longitude / coord_factor
    lat_rad_1 = math.radians(lat_1)
    lat_rad_2 = math.radians(lat_2)
    delta_lat_rad = math.radians(lat_2 - lat_1)
    delta_lon_rad = math.radians(lon_2 - lon_1)

    a = (pow(math.sin(delta_lat_rad / 2), 2) +
         (math.cos(lat_rad_1) * math.cos(lat_rad_2) * pow(
             math.sin(delta_lon_rad / 2), 2
         )))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000
    return R * c


class RouteGuide(routepbgrpc.RouteGuideServicer):
    def __init__(self):
        self.db = routedb.read_routeguide_db()

    def GetFeature(self, request, context):
        """
        将request中的point到数据源中匹配，返回相应的feature
        :param request:
        :param context:
        :return:
        """
        feature = get_feature(self.db, request)
        if feature is None:
            return routepb.Feature(name='', location=request)
        else:
            return feature

    def ListFeature(self, request, context):
        """
        获得请求中的Rectangle
        返回矩形中的地点point list
        :param request:
        :param context:
        :return:
        """
        left = min(request.lo.longitude, request.hi.longitude)
        right = max(request.lo.longitude, request.hi.longitude)
        top = max(request.lo.latitude, request.hi.latitude)
        bottom = min(request.lo.latitude, request.hi.latitude)
        for feature in self.db:
            if (feature.location.longitude >= left
                    and feature.location.longitude <= right
                    and feature.location.latitude >= bottom
                    and feature.location.latitude <= top):
                yield feature

    def RecordRoute(self, request_iterator, context):
        """
        统计传来的20个点的统计信息
        :param request_iterator:
        :param context:
        :return:
        """
        point_count = 0
        feature_count = 1
        distance = 0.0
        prev_point = None

        start_time = time.time()
        for point in request_iterator:
            point_count += 1
            if get_feature(self.db, point):
                feature_count += 1
            if prev_point:
                distance += get_distance(prev_point, point)
            prev_point = point
        elapsed_time = time.time() - start_time
        return routepb.RouteSummary(
            point_count=point_count,
            feature_count=feature_count,
            distance=int(distance),
            elapsed_time=int(elapsed_time)
        )

    def RouteChat(self, request_iterator, context):
        """
        客户端与服务器进行聊天
        :param request_iterator:
        :param context:
        :return:
        """
        prev_notes = []
        for new_note in request_iterator:
            for prev_note in prev_notes:
                if prev_note.location == new_note.location:
                    yield prev_note
            prev_notes.append(new_note)


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    routepbgrpc.add_RouteGuideServicer_to_server(RouteGuide(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("server start successfully.")
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    server()