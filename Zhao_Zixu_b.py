#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from gurobipy import *


# Read in csv file and print it out

# In[3]:


graph = pd.read_csv('g.csv')
graph


# Set up model and variables we need

# In[4]:


m = Model()
x = {}
w = {}
u_nodes = []
v_nodes = []
arcs = tuplelist()


# w is the weight for each edge u,v.

# u_nodes is a list of all vertices in u.

# v_nodes is a list of all vertices in v.

# Set x[i,j] as a binary variable.

# In[5]:


for r in graph.index:
    u_nodes.append(graph.iloc[r]['u']) # add nodes into u_nodes
    v_nodes.append(graph.iloc[r]['v']) # add nodes into v_nodes
    arcs.append((graph.iloc[r]['u'], graph.iloc[r]['v'])) # add "arc" into arcs
    w.update({(graph.iloc[r]['u'], graph.iloc[r]['v']) : graph.iloc[r]['weight']}) # add weight on edge u,v into w

u_nodes = list(dict.fromkeys(u_nodes)) # remove the duplicated nodes
v_nodes = list(dict.fromkeys(v_nodes)) # remove the duplicated nodes

for i, j in arcs:
    x[(i, j)] = m.addVar(vtype=GRB.BINARY, name=f'x_{i},{j}')


# Set the objective function

# In[6]:


m.setObjective(quicksum(x[(i, j)]*w[(i, j)] for i,j in arcs), GRB.MAXIMIZE)


# Set the constraints

# In[8]:


for u in u_nodes:
    m.addConstr(quicksum(x[(i, j)] for i,j in arcs.select(u, '*')) <= 1) # no two edges share a vertex in u_nodes
    
for v in v_nodes:
    m.addConstr(quicksum(x[(i, j)] for i,j in arcs.select('*', v)) <= 1) # no two edges share a vertex in v_nodes


# In[120]:


m.optimize()


# The optimal objective value is 2215

# Interpret the solution (the value of all variables)

# In[122]:


for i, j in arcs:
    if x[i,j].x > 0.5:
        print(f"x[{i},{j}]= {x[i,j].x}")


# In[140]:


u_col = []
v_col = []
for i, j in arcs:
    if x[(i, j)].x > 0.5:
        u_col.append(i)
        v_col.append(j)

uv_cols = {'u': u_col, 'v': v_col}

df.to_csv('Zhao_Zixu_b_sol.csv', index=False)


# In[ ]:




