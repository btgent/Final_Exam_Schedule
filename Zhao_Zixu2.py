#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from gurobipy import *

# Input k and alpha here:
k = 3
alpha = 1/4


# Read in csv file 'g1.csv'
graph = pd.read_csv('g1.csv')


# Setup variables we need:
arcs = tuplelist()
w = {}
nodes = []

for r in graph.index:
    arcs.append((graph.iloc[r]['u'], graph.iloc[r]['v']))
    w.update({(graph.iloc[r]['u'], graph.iloc[r]['v']) : graph.iloc[r]['weight']})
    nodes.append(graph.iloc[r]['u'])
    nodes.append(graph.iloc[r]['v'])

nodes = list(dict.fromkeys(nodes)) # remove the duplicated nodes
nodes.sort() # sort nodes in ascending order


m = Model()
x = {}
y = {}
balance = alpha * len(nodes) # balanced number of nodes = alpha * \V\
B = {}

for i in range(1, k+1):
    for j in range(1, k+1):
        if i != j:
            B[i,j] = (i,j)

# Setup variable x(u, i). x(u, i) equals 1 if node u is in partition i, otherwise it equals 0.
for v in nodes:
    for i in range(1, k+1):
        x[(v, i)] = m.addVar(vtype=GRB.BINARY, name=f'x_{v},{i}')

# Setup variable y(u, v). y(u, v) equals 1 if u and v are in the different partition, otherwise it equals 0.
for u,v in arcs:
    y[(u, v)] = m.addVar(vtype=GRB.BINARY, name=f'y_{u},{v}')


m.setObjective(quicksum(y[(u, v)]*w[(u, v)] for u,v in arcs), GRB.MINIMIZE)


# Add a constraint that each partition is balanced.
for i in range(1, k+1):
    m.addConstr(quicksum(x[(v, i)] for v in nodes) >= balance)

# Add a constraint that for any node u, the summation of x(u, i) over all partition i equals 1.
for v in nodes:
    m.addConstr(quicksum(x[(v, i)] for i in range(1, k+1)) == 1)

# Setup a constraint such that y(u, v) >= x(u, i) - x(v, i) over all partition i for any u, v in arcs.
for u,v in arcs:
    for i in range(1, k+1):
        m.addConstr(x[(u, i)]-x[(v, i)] <= y[(u, v)])
            
m.optimize()


# export data in x(u, i) to a csv file
u_col = []
i_col = []
for u in nodes:
    for i in range(1, k+1):
        if x[u, i].x == 1:
            u_col.append(u)
            i_col.append(i)

ui_cols = {'u': u_col, 'part_number': i_col}
df = pd.DataFrame(data=ui_cols)
df.to_csv('Zhao_Zixu_sol.csv', index=False)

