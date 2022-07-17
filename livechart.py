from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pymysql
import sqlalchemy
import streamlit as st

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

plt.plot([], [], label='Temperature')
plt.plot([], [], label='Humidity')
plt.legend(loc="upper left")


def animate(i):
    sqlEngine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3325/demo22', pool_recycle=3600)
    data = pd.read_sql_table("data1", sqlEngine)
    x = data['ID']
    y1 = data['temperature']
    y2 = data['humidity']

    ax = plt.gca()
    line1, line2 = ax.lines

    line1.set_data(x, y1)
    line2.set_data(x, y2)

    xlim_low, xlim_high = ax.get_xlim()
    ylim_low, ylim_high = ax.get_ylim()

    ax.set_xlim(xlim_low, (x.max() + 5))

    y1max = y1.max()
    y2max = y2.max()
    current_ymax = y1max if (y1max > y2max) else y2max

    y1min = y1.min()
    y2min = y2.min()
    current_ymin = y1min if (y1min < y2min) else y2min

    ax.set_ylim((current_ymin - 5), (current_ymax + 5))


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.legend()
plt.tight_layout()
plt.show()

