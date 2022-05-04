import random, uuid, time, json, sys
from random import randrange
from datetime import timedelta, datetime
from psycopg2 import sql, Error, connect
import matplotlib.pyplot as plt
import os
import networkx as nx
try:
    # declare a new PostgreSQL connection object
    conn = connect(
        dbname = "vkdb",
        user = "postgres",
        host = "localhost",
        port = "5432",
        password = "12345678",
        # attempt to connect for 3 seconds then raise exception
        connect_timeout = 3
    )

    cur = conn.cursor()
    print ("\ncreated cursor object:", cur)

except Error as err:
    print ("\npsycopg2 connect error:", err)
    conn = None
    cur = None
    records = []

    # only attempt to execute SQL if cursor is valid
if cur!= None:
    sql_select_query = "select distinct peerid, count(*) over (partition by peerid order by peerid)  from vk_tst.messages"                                      #Селект айди отправителя и количество отправленных и принятых сообщений
    sql_select_max = "with a as (select distinct peerid, count(*) over (partition by peerid order by peerid)  from vk_tst.messages) select max(count) from a "  #Селект максимального значения количества сообщений из базы
    cur.execute(sql_select_query)

    records = cur.fetchall()
    print('До преобразования','\n', records)
    records = str(records)
    records = records.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',', '')                                                      #Преобразование из массива в словарь словарей - формат для построения графов
    records = records.split(' ')
    print('После преобразования','\n',records)
    G = nx.Graph()
    edges = {};
    for i in range(1, len(records)):
        if i % 2 == 1:
            startnode = records[i - 1]
            endnode = records[i]
            if startnode not in edges:
                edges[startnode] = set()
            edges[startnode].add(endnode)                                                                                                                       #Конец создания словаря словарей для построения графов
    G.add_node(1)                                                                                                                                               #Создание центрального узла - то есть пользователя, от которого строят эго-граф
    cur.execute(sql_select_max)
    maximum = cur.fetchall()
    maximum_2 = int(str(maximum[0][0]))
    print ('---MAXIMUM---','\n',maximum_2)
    for key in edges:                                                                                                                                           #Создание нод для членов эго-графа
        G.add_node(key)
        value = edges.get(key)
        for k in value:
            z = int(k)
            print(z)
            G.add_edge(1, key, weight=(round( z / maximum_2 * 10 + 1,3)))

    pos = nx.spring_layout(G)
    print(G, '\n', pos)
                                                                                                                                                                #Рисование графа
    nx.draw_networkx(G, pos, arrows=True)
    plt.savefig("plot2.png")