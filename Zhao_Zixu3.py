#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from gurobipy import *
import networkx as nx
import csv


# Read in csv file 'g3.csv'.
# Store the tree graph in T and all edges of E' in NT.
Tfile = pd.read_csv('g3.csv')

T=nx.Graph()
i=0
NT=tuplelist()

for ind, row in Tfile.iterrows():
    if row['type'] == 'T':
        T.add_edge(row['u'], row['v'], id=i)
    else:
        NT.append((row['u'], row['v']))
    i+=1

p=nx.shortest_path(T)  # p is a 2-dimensional array of all paths in T


# Set up model
m = Model()
x={}


# Set up variables x(u,v). x(u,v) equals to 1 if it is chose to be in set C, otherwise it equals 0.
for u, v in NT:
    x[(u,v)] = m.addVar(vtype=GRB.BINARY, name=f'x_{u},{v}')


# Set up constraints for x(u, v).
for u, v in T.edges():
    uvs = tuplelist()  # uvs is a list that stores all possible pairs of u,v if x(u,v) may equal 1.
    for start, end in NT:
        path = p[start][end]  # compute the path between start and end.
        G=nx.Graph()  # set up a graph G to record path.
        G.add_path(path)
        if G.has_edge(u,v):  # check if the edge (u,v) is in path.
            uvs.append((start, end))  # store a pair of u,v if edge(u,v) is in path, which means x(u,v) may equal 1.
    m.addConstr(quicksum(x[(u,v)] for u,v in uvs) >= 1)  # the egde(u,v) should be covered in a path at least once.

m.setObjective(quicksum(x[(u, v)] for u,v in NT), GRB.MINIMIZE)

m.optimize()

# export data in x(u, v) to a csv file
u_col=[]
v_col=[]
for u, v in NT:
    if x[(u, v)].x == 1:
        u_col.append(u)
        v_col.append(v)
uv_cols = {'u': u_col, 'v': v_col}
df = pd.DataFrame(data=uv_cols)
df.to_csv('Zhao_Zixu_sol.csv', index=False)

