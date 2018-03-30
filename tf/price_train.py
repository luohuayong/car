#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Leo on 2017/9/18

"""
代码说明：
"""

import psycopg2
import tensorflow as tf
import numpy as np

class price_train:

    def __init__(self):
        self.databse = "car"
        self.user = "postgres"
        self.password = "123123"
        self.host = "127.0.0.1"
        self.port = "5432"

    def load_data(self):
        conn = psycopg2.connect(database=self.databse, user=self.user,
                                password=self.password,host=self.host,
                                port=self.port)
        cursor = conn.cursor()

        sql = "select model_id,city_id,used_months,xingshi,price_new,price from car_tf"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def line_train(self):
        rows = self.load_data()
        data = np.array(rows,dtype=np.float32)

        x_data = data[:,:5]
        x_data = x_data.T
        y_data = data[:,5:6]
        y_data = y_data.T

        b = tf.Variable(tf.zeros([1]))
        W = tf.Variable(tf.random_uniform([1, 5], -1.0, 1.0))
        y = tf.matmul(W, x_data) + b

        loss = tf.reduce_mean(tf.square(y - y_data))
        optimizer = tf.train.GradientDescentOptimizer(0.5)
        train = optimizer.minimize(loss)

        # 初始化变量
        init = tf.initialize_all_variables()

        # 启动图 (graph)
        sess = tf.Session()
        sess.run(init)

        # 拟合平面
        for step in range(0, 80001):
            sess.run(train)
            if step % 2000 == 0:
                print(step, sess.run(W), sess.run(b))
                print("loss={0}".format(sess.run(loss)))
        print("y={0}".format(sess.run(y)))
            # 得到最佳拟合结果 W: [[0.100  0.200]], b: [0.300]

    def train(self):
        rows = self.load_data()
        data = np.array(rows)

        dataset_size = data.shape[0]
        batch = 100
        rate = 0.001
        setps = 5000

        # 生成训练数据集
        X = data[:,:5]
        Y = data[:,5:6]

        W1 = tf.Variable(tf.random_normal([5, 100], stddev=1, seed=1))
        W2 = tf.Variable(tf.random_normal([100, 1], stddev=1, seed=1))

        x = tf.placeholder(dtype=tf.float32, shape=(None, 5), name='x')
        y = tf.placeholder(dtype=tf.float32, shape=(None, 1), name='y')

        a = tf.matmul(x, W1)
        y_ = tf.matmul(a, W2)

        loss = -tf.reduce_mean(y*tf.log(tf.clip_by_value(y_, 1e-10, 1.0)))
        train = tf.train.AdamOptimizer(rate).minimize(loss)

        init = tf.initialize_all_variables()
        with tf.Session() as sess:
            sess.run(init)
            print("begin W1 = %s" % sess.run(W1))
            print("begin W2 = %s" % sess.run(W2))
            for i in range(setps):
                start = (i*batch) % dataset_size
                end = min(start + batch, dataset_size)
                sess.run(train, feed_dict={x: X[start:end], y: Y[start:end]})
                if i % 500 == 0:
                    total_loss = sess.run(loss, feed_dict={x: X, y: Y})
                    print("i=%s, total_loss=%s" % (i, total_loss))
            print("end W1 = %s" % sess.run(W1))
            print("end W2 = %s" % sess.run(W2))

    def predition(self):
        model_id = 0.2775
        city_id = 0.248
        used_months = 0.086
        xingshi = 0.0649
        price_new = 0.0264
        price = 0.0085
        w = [-0.00107872, -0.00319275, -0.08732923, -0.017029, 0.52155691]
        b = 0.00614169
        y = w[0] * model_id + w[1] * city_id + w[2] * used_months + w[3] * xingshi + w[4] * price_new + b
        print y



if __name__ == '__main__':
    pt = price_train()
    # pt.train()
    pt.line_train()
    pt.predition()