#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Leo on 2017/9/12

"""
代码说明：
"""

import psycopg2
import time

class pg_helper(object):

    def __init__(self):
        self.databse = "car"
        self.user = "postgres"
        self.password = "123123"
        self.host = "127.0.0.1"
        self.port = "5432"

    def insert_test(self):
        conn = psycopg2.connect(database=self.databse, user=self.user,
                                password=self.password,host=self.host,
                                port=self.port)
        cursor = conn.cursor()

        sql = ("insert into car_brand (code_guazi,name,name_e,first,create_uid,create_date,write_uid,write_date)"
               " values('%s','%s','%s','%s',%s,'%s',%s,'%s')")
        sql = sql % ("richan","日产","NISSAN","r",1,"2017-09-12 10:20:45.51225",1,"2017-09-12 10:20:45.51225")
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def insert(self,item,table_name):
        str_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        keys = ''
        values = ''
        for key,value in item.items():
            keys += "{},".format(key)
            values += "'{}',".format(value)
        keys += "create_uid,create_date,write_uid,write_date"
        values += "1,'{0}',1,'{0}'".format(str_time)
        sql = "insert into {0} ({1}) values ({2})".format(table_name,keys,values)

        conn = psycopg2.connect(database=self.databse, user=self.user,
                                password=self.password,host=self.host,
                                port=self.port)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    h = pg_helper()
    # h.insert_test()
    item = {}
    item['code_guazi'] = "richan"
    item['name'] = "日产"
    item['name_e'] = "NISSAN"
    item['first'] = "r"
    h.insert(item,"car_brand")