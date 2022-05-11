import random, uuid, time, json, sys
from random import randrange
from datetime import timedelta, datetime
from psycopg2 import sql, Error, connect
import matplotlib.pyplot as plt
import os
import networkx as nx
from tkinter import *
from tkinter import ttk
from operator import itemgetter

def create_graph(type_of_graph = 'None'):
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
        sql_select_emotion = "with a as(select distinct peerid,  emotion, count(*) over (partition by peerid, emotion order by peerid) as cnt from vk_tst.message_semantic),b as (select peerid, emotion, max(cnt) as mes_amm  from a group by peerid,emotion),c as (select peerid, max(mes_amm) as max_amm_join from b group by peerid) select c.peerid,b.emotion  from b  join c on b.peerid=c.peerid and b.mes_amm = c.max_amm_join"
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
        cur.execute(sql_select_emotion)
        emotions = cur.fetchall()

        print('До преобразования', '\n', emotions)

        emotions = str(emotions)
        emotions = emotions.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',','')  # Преобразование из массива в словарь словарей - формат для построения графов
        emotions = emotions.split(' ')
        print('После преобразования', '\n', emotions)
        emote = {};
        for i in range(1, len(emotions)):
            if i % 2 == 1:
                startnode = emotions[i - 1]
                endnode = emotions[i]
                if startnode not in emote:
                    emote[startnode] = set()
                emote[startnode].add(endnode)
        print ('\n',emote)
                                                                                                                                                                     #Рисование графа

        node_and_degree = G.degree()
        (largest_hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
        hub_ego = nx.ego_graph(G, largest_hub)
        nx.draw(hub_ego, pos, node_color="b", node_size=50, with_labels=True)
        options = {"node_size": 300, "node_color": "r"}

        if type_of_graph == 'emotional':
            options_neutral = {"node_size": 100, "node_color": "grey"}
            options_negative = {"node_size": 100, "node_color": "b"}
            options_positive = {"node_size": 100, "node_color": "g"}
            nx.draw_networkx_nodes(hub_ego, pos, nodelist=[1], **options)
            node_list_neutral = []
            node_list_negative = []
            node_list_positive = []

            for i in emote.keys():
                if emote.get(i) == {'0'}:
                    node_list_neutral.append(i)
                    #nx.draw_networkx_nodes(hub_ego, pos, nodelist=node_list_neutral, label = "Нейтральный сентимент", **options_neutral)
                if emote.get(i)=={'-1'}:
                    node_list_negative.append(i)
                   # nx.draw_networkx_nodes(hub_ego, pos, nodelist=node_list_negative,label = "Негативный сентимент", **options_negative)
                if emote.get(i) == {'-1'}:
                    node_list_positive.append(i)
                   # nx.draw_networkx_nodes(hub_ego, pos, nodelist=node_list_positive,label = "Позитивный сентимент", **options_positive)
            nx.draw_networkx_nodes(hub_ego, pos, nodelist=node_list_neutral, label="Нейтральный сентимент",
                               **options_neutral)
            nx.draw_networkx_nodes(hub_ego, pos, nodelist=node_list_negative, label="Негативный сентимент",
                               **options_negative)
            nx.draw_networkx_nodes(hub_ego, pos, nodelist=node_list_positive, label="Позитивный сентимент",
                               **options_positive)




            plt.legend ( loc='lower right')
        plt.show()
        #plt.savefig("plot2.png")


root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Обыкновенный эго-граф", command=lambda :create_graph()).grid(column=1, row=0)
ttk.Button(frm, text="С учетом преобладающего сентимента", command= lambda :create_graph('emotional')).grid(column=2, row=0)

ttk.Button(frm, text = "quit", command=root.destroy).grid(column = 5, row = 5)
root.mainloop()