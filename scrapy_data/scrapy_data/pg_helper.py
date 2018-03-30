#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Leo on 2017/9/12

"""
代码说明：
"""

import psycopg2
import time
import logging

class pg_helper(object):

    def __init__(self):
        self.databse = "car"
        self.user = "postgres"
        self.password = "123123"
        self.host = "127.0.0.1"
        self.port = "5432"
        self.log = logging.getLogger(name=__name__)

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

    def get_model_id(self, car_model_rows, model_name):
        for item in car_model_rows:
            if item[1] == model_name:
                return float(item[0])/10000
        return None

    def get_price_new(self, car_model_rows, model_name):
        for item in car_model_rows:
            if item[1] == model_name:
                return float(item[2])/1000
        return None

    def git_city_id(self, car_area_rows, address):
        for item in car_area_rows:
            if item[1] == address:
                return float(item[0])/1000
        return None

    def get_used_months(self,shangpai_date):
        try:
            now_year = time.localtime().tm_year
            now_month = time.localtime().tm_mon
            shangpai_year = int(shangpai_date.split("-")[0])
            shangpai_month = int(shangpai_date.split("-")[1])
            used_months = abs((shangpai_year-now_year)*12 + (shangpai_month-now_month))
            used_months = float(used_months)/1000
            return used_months
        except:
            self.log.info("计算使用月份失败")
            return None

    def get_xingshi(self,xingshi):
        xingshi_new = xingshi[:xingshi.index("万")]
        xingshi_new = float(xingshi_new)/100
        return xingshi_new

    def get_price(self,price):
        price_new = price[price.index("¥")+2:].strip()
        price_new = float(price_new)/1000
        return price_new


    def insert_tf_data(self):
        conn = psycopg2.connect(database=self.databse, user=self.user,
                                password=self.password,host=self.host,
                                port=self.port)
        cursor = conn.cursor()
#         insert into car_tf (model_id,city_id,used_months,xingshi,price_new,price)
# select cm.id as model_id,
# ca.id as city_id,
# date_part('month', age(to_date(cs.shangpai_date,'YYYY-MM'))) as used_months,
# substring(xingshi from 0 for position('万' in xingshi)) as xingshi,
# cm.price_new as price_new,
# trim(substring(price from 2))
# from car_sale cs left join car_model cm on cs.model_name=cm.name
# left join car_area ca on cs.address=ca.city_name
# where position( '价' in cs.price_new) > 0 and city_id is not null;

        sql = "select model_name,address,shangpai_date,xingshi,price_new,price from car_sale"
        cursor.execute(sql)
        car_sale_rows = cursor.fetchall()

        sql = "select id,name,price_new from car_model"
        cursor.execute(sql)
        car_model_rows = cursor.fetchall()

        sql = "select id,city_name from car_area"
        cursor.execute(sql)
        car_area_rows = cursor.fetchall()

        for item in car_sale_rows:
            model_name = item[0]
            address = item[1]
            shangpai_date = item[2]
            xingshi = item[3]
            price = item[5]
            model_id = self.get_model_id(car_model_rows, model_name)
            if model_id is None:
                continue
            price_new = self.get_price_new(car_model_rows,model_name)
            if price_new is None:
                continue
            city_id = self.git_city_id(car_area_rows, address)
            if city_id is None:
                continue
            used_months = self.get_used_months(shangpai_date)
            if used_months is None:
                continue
            xingshi = self.get_xingshi(xingshi)
            price = self.get_price(price)
            sql = "insert into car_tf (model_id,city_id,used_months,xingshi,price_new,price)" +\
            " values ({0},{1},{2},{3},{4},{5})"
            sql = sql.format(model_id,city_id,used_months,xingshi,price_new,price)
            cursor.execute(sql)
            conn.commit()

        cursor.close()
        conn.close()


if __name__ == '__main__':
    h = pg_helper()
    # h.insert_tf_data()
    h.insert_test()
    # item = {}
    # item['code_guazi'] = "richan"
    # item['name'] = "日产"
    # item['name_e'] = "NISSAN"
    # item['first'] = "r"
    # h.insert(item,"car_brand")