# import required module
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import os
# create object
G = nx.Graph()

Y = {}
Y = {'642586157201': {'11900'}, '358160846853': {'1157'}, '492182732117': {'1135'}, '472876987010': {'1172'}, '235767701509': {'1176'}, '468957120608': {'1198'}, '588389670889': {'1185'}, '193277608861': {'1138'}, '12345': {'1149'}}
G.add_node(1)
X = {}
X = {'642586157201': {'1190'}, '358160846853': {'1157'}, '492182732117': {'1135'}, '472876987010': {'1172'}, '235767701509': {'1176'}, '468957120608': {'1198'}, '588389670889': {'1185'}, '193277608861': {'1138'}, '12345': {'1149'}}
#label = {'642586157201':{'Perviy'},'358160846853':{'vtoroy'},'492182732117':{'third'},'472876987010':{'fourth'},'235767701509':{'fifth'},'468957120608':{'sixth'},'588389670889':{'seventh'},'193277608861':{'eighth'},'12345':{'nineth'}}

for key in Y:
    G.add_node(key)
    value = Y.get(key)
    print('Value: ',value)
    for k in value:
        z=int(k)
        print (z)
        G.add_edge(1,key,weight=(z/1190*10+1))
for key in X:
    G.add_node(key)
    value = X.get(key)
    print('Value: ',value)
    for k in value:
        z=int(k)
        print (z)
        G.add_edge(1,key,weight=(z/1190*10+1))
pos = nx.spring_layout(G)
print (G,'\n',pos)

# illustrate graph
#nx.draw_networkx(G, pos,arrows = True)
# kwds = {"labels":label}

# nx.draw_networkx(G, pos = nx.spring_layout(G))

node_and_degree = G.degree()
(largest_hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
print(largest_hub)
hub_ego = nx.ego_graph(G, largest_hub)
nx.draw(hub_ego, pos, node_color="b", node_size=50, with_labels=True)
options = {"node_size": 300, "node_color": "y"}
nx.draw_networkx_nodes(hub_ego, pos, nodelist=[1], **options)
plt.show()