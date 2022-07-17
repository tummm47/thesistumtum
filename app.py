import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import time
import sys
import subprocess

import sqlalchemy

from livechart import *
from process import *
from linear_predict import *
from predictive_maintainance import *
from aggregate import *

sqlEngine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3325/demo22', pool_recycle=3600)
data = pd.read_sql_table("data1", sqlEngine)

sale_data = pd.read_csv('data_train/clean_data.csv')
sale_data_short = sale_data[["Date", "Weekly_Sales", "IsHoliday", "Temperature", "Fuel_Price", "CPI"]]

maintainance_data = pd.read_csv("data_train/predictive_maintenance.csv")
maintainance_data_short = maintainance_data[
    ["Product ID", "Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", "Torque [Nm]",
     "Tool wear [min]", "Failure Type"]]

aggregate_data = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3325/aggregate', pool_recycle=3600)
aggregate_data_short = pd.read_sql_table("data1", aggregate_data)

if __name__ == '__main__':
    st.set_page_config(page_title='@tum_demo',
                       page_icon='random', layout='wide',
                       initial_sidebar_state="expanded")
    st.title("#TumvaStreamlit")
    option_db = st.sidebar.selectbox(
        'Which db you need?',
        ('', "All Data", "Live Chart", "Forecast Demand", "Predictive Maintainance", "Aggregate Planning"))
    placeholder = st.empty()
    # Database Temperature + Humidity
    if option_db == "All Data":
        # Dashboard
        st.subheader("Current Data")
        hide_dataframe_row_index = """
                    <style>
                    .row_heading.level0 {display:none}
                    .column_heading.level0 {display:none}
                    .blank {display:none}
                    </style>
                    """
        # Inject CSS with Markdown
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        table = st.dataframe(data.style.format(subset=['humidity', 'temperature'], formatter="{:.1f}"))
        # CRUD
        option_crud = st.selectbox(
            'You want to ...',
            ('', "Create", "Update", "Delete"))
        if option_crud == "Create":
            with st.form(key="Create"):
                humidity = st.text_input('Enter current Humidity', 'Type here !!!')
                temperature = st.text_input('Enter current Temperature', 'Type here !!!')
                create_button = st.form_submit_button("Create")
            # CONFIG
            if create_button:
                new_data = add_data(humidity, temperature)
                table.dataframe(get_all_data().style.format(subset=['humidity', 'temperature'], formatter="{:.1f}"))

        elif option_crud == "Update":
            date_of_data = [data["date"][5]]
            # date_of_data = ["YYYY-MM-DD HH:MM:SS"]
            for i in data["date"]:
                date_of_data.append(i)
            option_date = st.selectbox(
                'You want to update ...', date_of_data)
            # st.write(option_date)
            index_value = int(data.index[data["date"] == option_date].values)
            humidity = st.text_input('Enter new value of Humidity', data["humidity"][index_value])
            temperature = st.text_input('Enter new value of Temperature', data["temperature"][index_value])
            # CONFIG
            if st.button('Update'):
                ID = data["ID"][index_value]
                date = data["date"][index_value]
                update_data = update_data(ID, humidity, temperature, date)
                table.dataframe(get_all_data().style.format(subset=['humidity', 'temperature'], formatter="{:.1f}"))

        elif option_crud == "Delete":
            date_of_data = []
            for i in data["date"]:
                date_of_data.append(i)
            # st.write(date_of_data)
            option_date = st.selectbox(
                'You want to delete ...', date_of_data)
            # st.write(option_date)
            index_value = int(data.index[data["date"] == option_date].values)
            if st.button('Delete'):
                ID = data["ID"][index_value]
                delete_data = delete_data(ID)
                table.dataframe(get_all_data().style.format(subset=['humidity', 'temperature'], formatter="{:.1f}"))

    elif option_db == "Live Chart":
        subprocess.run([f"{sys.executable}", "livechart.py"])

    elif option_db == "Forecast Demand":
        st.subheader("Sales Data")
        hide_dataframe_row_index = """
                    <style>
                    .row_heading.level0 {display:none}
                    .blank {display:none}
                    </style>
                    """
        # Inject CSS with Markdown
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        # table = st.dataframe(sale_data.style.format(subset=["Weekly_Sales", "Temperature", "Fuel_Price"], formatter="{:.1f}"))
        table = st.dataframe(sale_data_short.iloc[:100])
        with st.form(key="Predict_Demand"):
            fuel_index = st.text_input("Enter Fuel_Price: ")
            predict_button = st.form_submit_button("Predict")
        # CONFIG
        if predict_button:
            sale_predict = predict(float(fuel_index), weight, bias)
            st.text(f"Weekly sale is: {round(sale_predict, 2)}")

    elif option_db == "Predictive Maintainance":
        st.subheader("Machine Data")
        hide_dataframe_row_index = """
                    <style>
                    .row_heading.level0 {display:none}
                    .blank {display:none}
                    </style>
                    """
        # Inject CSS with Markdown
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        table = st.dataframe(maintainance_data_short.iloc[:100])
        with st.form(key="Predictive_Maintainance"):
            processtemp_input = st.text_input("Enter the Process temperature in K: ")
            torque_input = st.text_input("Enter the Torque in Nm: ")
            toolwear_input = st.text_input("Enter the Tool wear in mins: ")
            predict_button_2 = st.form_submit_button("Predict")
        # CONFIG
        if predict_button_2:
            maintenance_predict = MPM_model_decision(np.array([[processtemp_input, torque_input, toolwear_input]]))
            st.text(f"{maintenance_predict}")

    elif option_db == "Aggregate Planning":
        # Dashboard
        st.subheader("Current Data")
        hide_dataframe_row_index = """
                    <style>
                    .row_heading.level0 {display:none}
                    .blank {display:none}
                    </style>
                    """
        # Inject CSS with Markdown
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        table = st.dataframe(
            aggregate_data_short.style.format(subset=["demand", "production_cost", "holding_cost", "labor_cost",
                                                      "overtime_cost", "avai_labor_hour", "avai_over_hour"],
                                              formatter="{:.1f}"))
        # CRUD
        option_crud = st.selectbox(
            'You want to ...',
            ('', "Create", "Update", "Aggregate Production Planning"))
        if option_crud == "Create":
            with st.form(key="Create"):
                demand_aggregate = st.text_input('Enter current Demand', 'Type here !!!')
                production_cost = st.text_input('Enter current Production Cost', 'Type here !!!')
                holding_cost = st.text_input('Enter current Holding Cost', 'Type here !!!')
                labor_cost = st.text_input('Enter current Labor Cost', 'Type here !!!')
                overtime_cost = st.text_input('Enter current Overtime Cost', 'Type here !!!')
                avai_labor_hour = st.text_input('Enter current Available Labor Hour', 'Type here !!!')
                avai_over_hour = st.text_input('Enter current Available Overtime Hour', 'Type here !!!')
                create_button_agg = st.form_submit_button("Create")
            # CONFIG
            if create_button_agg:
                new_data_agg = add_data_agg(demand_aggregate, production_cost, holding_cost, labor_cost, overtime_cost, avai_labor_hour, avai_over_hour)
                table.dataframe(
                    get_all_data_agg().style.format(subset=["demand", "production_cost", "holding_cost", "labor_cost",
                                                            "overtime_cost", "avai_labor_hour", "avai_over_hour"],
                                                    formatter="{:.1f}"))
        elif option_crud == "Update":
            date_of_data = [data["date"][5]]
            # date_of_data = ["YYYY-MM-DD HH:MM:SS"]
            for i in data["date"]:
                date_of_data.append(i)
            option_date = st.selectbox(
                'You want to update ...', date_of_data)
            # st.write(option_date)
            index_value = int(data.index[data["date"] == option_date].values)
            humidity = st.text_input('Enter new value of Humidity', data["humidity"][index_value])
            temperature = st.text_input('Enter new value of Temperature', data["temperature"][index_value])
            # CONFIG
            if st.button('Update'):
                ID = data["ID"][index_value]
                date = data["date"][index_value]
                update_data = update_data(ID, humidity, temperature, date)
                table.dataframe(get_all_data().style.format(subset=['humidity', 'temperature'], formatter="{:.1f}"))
        elif option_crud == "Aggregate Production Planning":
            with st.form(key="Aggregate_Production)Planning"):
                predict_button_3 = st.form_submit_button("Planning")
            # CONFIG
            if predict_button_3:
                st.text(f"Total Production Plan Cost = {value(prob.objective)}")
