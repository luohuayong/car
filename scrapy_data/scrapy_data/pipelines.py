# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import time
import logging
import sys

class ScrapyDataPipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.databse = "car"
        self.user = "postgres"
        self.password = "123123"
        self.host = "127.0.0.1"
        self.port = "5432"

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

    def process_item(self, item, spider):
        logging.info("写入数据库")
        if spider.name == "guazi_area":
            self.insert(item,"car_area")
        # elif spider.name == "guazi":
        #     self.insert(item,"car_sale")
        # elif spider.name == "guazi_pinpai":
        #     self.insert(item,"car_temp1")
        return item
