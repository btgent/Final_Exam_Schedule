#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from gurobipy import *


# In[2]:


arcs, w = multidict({
    (1, 4): 2,
    (1, 5): 2,
    (2, 4): 1,
    (2, 5): 1,
    (3, 5): 3,
    (3, 6): 2})


# In[3]:


m = Model()


# Set x[i, j] as a binary variable.

# In[4]:


x = {}
for i, j in arcs:
    x[(i, j)] = m.addVar(vtype=GRB.BINARY, name=f'x_{i},{j}')


# Set the objective function

# In[5]:


m.setObjective(quicksum(x[(i, j)]*w[(i, j)] for i,j in arcs), GRB.MAXIMIZE)


# Set the constraints

# In[6]:


m.addConstr((x[(1, 4)] + x[(1, 5)]) <= 1)
m.addConstr((x[(2, 4)] + x[(2, 5)]) <= 1)
m.addConstr((x[(3, 5)] + x[(3, 6)]) <= 1)
m.addConstr((x[(1, 4)] + x[(2, 5)]) <= 1)
m.addConstr((x[(1, 5)] + x[(2, 5)] + x[(3, 5)]) <= 1)
m.addConstr((x[(3, 6)]) <= 1)


# In[7]:


m.optimize()


# The optimal objective value is 6

# Interpret the solution (the value of all variables)

# In[8]:


for i, j in arcs:
    print(f"x[{i},{j}]= {x[i,j].x}")


# In[ ]:




