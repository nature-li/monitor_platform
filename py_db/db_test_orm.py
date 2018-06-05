#!/usr/bin/env python2.7
# coding: utf-8

import datetime
import json
import traceback
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_orm import *


engine = create_engine('sqlite:////Users/liyanguo/work/web/hive/sqlite/count.db', echo=False)


# 打印日志
def query_network_list(network_name, off_set, limit):
        # 转换类型
        off_set = int(off_set)
        limit = int(limit)
        if limit == -1:
            limit_count = None
        else:
            limit_count = off_set + limit
        print 25, limit_count

        # 创建session
        session = sessionmaker(bind=engine)()
        # 查询数据
        if network_name != '':
            like_condition = '%' + network_name + '%'
            count = session.query(NetworkList.id,
                                  NetworkList.network,
                                  NetworkList.update_time).filter(NetworkList.network.like(like_condition)).count()
            print count
            values = session.query(NetworkList.id,
                                   NetworkList.network,
                                   NetworkList.update_time).filter(NetworkList.network.like(like_condition))[
                     off_set: limit_count]
            print 40, len(values)
        else:
            count = session.query(NetworkList.id,
                                  NetworkList.network,
                                  NetworkList.update_time).count()
            print count
            values = session.query(NetworkList.id,
                                   NetworkList.network,
                                   NetworkList.update_time)[off_set: limit_count]
        print 49, len(values)
        # 关闭session
        session.close()


query_network_list('', 0, -1)
