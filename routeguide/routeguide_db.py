#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   routeguide_db.py.py    
@Author  :   wangyawen
@Modify Time :  2021/1/26 下午1:18
@Version    :   1.0
"""
import json
import routeguide.routeguide_pb2 as routepb


def read_routeguide_db():
    feature_list = []
    with open('routeguide_db.json') as f:
        for item in json.load(f):
            feature = routepb.Feature(
                name=item['name'],
                location=routepb.Point(
                    latitude=item['location']['latitude'],
                    longitude=item['location']['longitude']
                )
            )
            feature_list.append(feature)
    return feature_list


if __name__ == '__main__':
    print('main')
