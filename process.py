import os
from flask import request, jsonify, send_file
from __init__ import *
import pandas as pd

import MySQLdb

data_con = MySQLdb.connect("127.0.0.1", "root", "", "demo22", 3325)
my_cursor = data_con.cursor()

data_con_agg = MySQLdb.connect("127.0.0.1", "root", "", "aggregate", 3325)
my_cursor_agg = data_con_agg.cursor()


def add_data(humidity, temperature):
    if humidity and temperature:
        sqlquery = f"insert into data1(humidity, temperature) values ({humidity}, {temperature})"
        my_cursor.execute(sqlquery)
        try:
            data_con.commit()
            return True
        except Exception as ex:
            print(ex)
    return False


def update_data(ID, humidity, temperature, date):
    print(ID, humidity, temperature, date)
    if ID and humidity and temperature and date:
        my_cursor.execute(f" UPDATE data1 SET humidity = {humidity}, temperature = {temperature} WHERE ID = {ID}")
        try:
            data_con.commit()
            return True
        except Exception as ex:
            print(ex)
    return False


def delete_data(ID):
    if ID:
        my_cursor.execute(f" DELETE FROM data1 WHERE ID = {ID}")
        try:
            data_con.commit()
            return True
        except Exception as ex:
            print(ex)
    return False


# def delete_data(ID):
#     if ID:
#         my_cursor.execute("SELECT * FROM data1")
#         my_result = my_cursor.fetchall()
#         delete_old_product = my_result.query.filter_by(ID=ID).first()
#         if delete_old_product:
#             try:
#                 data_con.delete(delete_old_product)
#                 data_con.commit()
#                 return True
#             except Exception as ex:
#                 print(ex)
#
#     return False


def get_all_data():
    my_cursor.execute("SELECT * FROM data1")
    my_result = my_cursor.fetchall()
    all_data_list = list(my_result)
    all_data_df = pd.DataFrame(
        all_data_list, columns=['ID', 'humidity', 'temperature', "date"])
    # for x in my_result:
    #     print(x)
    return all_data_df


def add_data_agg(demand_aggregate, production_cost, holding_cost, labor_cost, overtime_cost, avai_labor_hour, avia_over_hour):
    if demand_aggregate and production_cost and holding_cost and labor_cost and overtime_cost and avai_labor_hour and avia_over_hour:
        sqlquery_agg = f"insert into data1(demand_aggregate, production_cost, holding_cost, labor_cost, overtime_cost, avai_labor_hour, avia_over_hour) " \
                   f"values ({demand_aggregate}, {production_cost}, {holding_cost}, {labor_cost}, {overtime_cost}, {avai_labor_hour}, {avia_over_hour})"
        my_cursor_agg.execute(sqlquery_agg)
        try:
            data_con_agg.commit()
            return True
        except Exception as ex:
            print(ex)
    return False


def get_all_data_agg():
    my_cursor_agg.execute("SELECT * FROM data1")
    my_result_agg = my_cursor_agg.fetchall()
    all_data_list_agg = list(my_result_agg)
    all_data_df_agg = pd.DataFrame(
        all_data_list_agg, columns=["ID", "demand", "production_cost", "holding_cost", "labor_cost",
                                    "overtime_cost", "avai_labor_hour", "avia_over_hour", "date"])
    # for x in my_result:
    #     print(x)
    return all_data_df_agg


def get_name_id_products():
    products = Product.query.all()
    df = pd.DataFrame(columns=['', ''])
    for i in range(len(products)):
        df.loc[i] = [products[i].name, products[i].id]
    return df


def get_all_material():
    materials = Material.query.all()
    model = Material()
    df = pd.DataFrame(columns=model.column_names())
    for i in range(len(materials)):
        df.loc[i] = materials[i].column_value()
    # print(df)
    return df
