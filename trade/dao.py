# coding=utf-8

import pymysql
from pymysql.err import MySQLError

db = pymysql.connect("localhost", "btc", "btc123", "btc", charset='utf8')
cursor = db.cursor()


def insert_into_db_self(type, trd_b, trd_r, blnc_b, blnc_r, success):
    sql = f"insert into trade_record(time,type,trade_b,trade_r,balance_b,balance_r,success) values (NULL,{type},{trd_b},{trd_r},{blnc_b},{blnc_r},{success})"
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except MySQLError as e:
        db.rollback()


def select_count():
    sql = "select count(*) from trade_record"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except MySQLError as e:
        print("Error:unable to fetch data")
    return results


def select_new_trade():
    sql = "select * from trade_record order by time desc limit 1"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            time = row[0]
            type = row[1]
            trd_b = row[2]
            trd_r = row[3]
            blnc_b = row[4]
            blnc_r = row[5]
            success = row[6]
    except MySQLError as e:
        print("Error:unable to fetch data")
    return time, type, trd_b, trd_r, blnc_b, blnc_r, success


def select_asset_self():
    sql = "select balance_b,balance_r from trade_record order by time desc limit 1"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            blnc_b = row[0]
            blnc_r = row[1]
    except MySQLError as e:
        print("Error:unable to fetch data")
    return blnc_b, blnc_r


def insert_to_db_trade(rid, price, order_amount, type, final_amount, fee):
    sql = f"insert into history_trade(id,price,order_amount,type,final_amount,fee) values({rid},{price},{order_amount},'{type}',{final_amount},{fee})"
    try:
        cursor.execute(sql)
        db.commit()
    except MySQLError as e:
        print(e)
        db.rollback()


def insert_to_db_price(open, close, high, low, amnt):
    sql = f"insert into history_price(open,close,high,low,amount) values({open},{close},{high},{low},{amnt})"
    try:
        cursor.execute(sql)
        db.commit()
    except MySQLError as e:
        db.rollback()


def select_trade(num):
    sql = "select * from history_trade order by id desc limit " + str(num)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except MySQLError as e:
        print("Error:unable to fetch data")
    return results


def insert_log(message):
    sql = "insert into log(log) values('%s')" % message
    try:
        cursor.execute(sql)
        db.commit()
    except MySQLError as e:
        db.rollback()
