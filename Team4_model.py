import pandas as pd
from gurobipy import *
import networkx as nx
from networkx.algorithms import bipartite
import csv

Gfile=pd.read_csv('Team4_data_g.csv')
studentFile=pd.read_csv('Team4_data_students.csv')

G = nx.DiGraph()  # timeslot graph
ids=[]  # record all edge ids in G. id represents the number of a timeslot.
i=0
for ind, row in Gfile.iterrows():
    G.add_edge(row['u'], row['v'], weight=row['weight'], id=i)
    ids.append(i)
    i+=1

s=tuplelist()  # record student number and corresponding course numbers in a list.
courses=[]  # record all course numbers.
students=[]  # record all student numbers.
for ind, row in studentFile.iterrows():
    s.append((row['student'], row['subject']))
    if row['subject'] not in courses:
        courses.append(row['subject'])
    if row['student'] not in students:
        students.append(row['student'])

tc=tuplelist()  # record as two tuples: timeslot and course number.
for i in ids:
    for j in courses:
        tc.append((i, j))

m=Model()
x={}

G.nodes()
for u,v in G.edges():
    for j in courses:
        x[(G[u][v]['id'],j)] = m.addVar(vtype=GRB.BINARY, name=f'x_{u},{v}')  
# X(i,j) where i is time and j is course.


# Constraints(below)
# each course must take up only one exam timeslot.
for j in courses:
    m.addConstr(quicksum(x[(i,j)] for i in ids) == 1)
    
# at most 5 exams can take place during the same time.
for i in ids:
    m.addConstr(quicksum(x[(i,j)] for j in courses) <= 5)

# no exam time conflict for any student.
for i in ids:
    for u in students:
        lst=s.select(u, '*')
        m.addConstr(quicksum(x[(i,j)] for v,j in lst) <= 1)
        
# no back-to-back exams for any student.
for u in students:
    lst=s.select(u, '*')  # all courses that the student u takes
    for i in ids:
        if i%4 == 0:
            m.addConstr((quicksum(x[i,j] for v,j in lst) + quicksum(x[i+1,j] for v,j in lst)) <= 1)
        elif i%4 == 3:
            m.addConstr((quicksum(x[i,j] for v,j in lst) + quicksum(x[i-1,j] for v,j in lst)) <= 1)
        else:
            m.addConstr((quicksum(x[i,j] for v,j in lst) + quicksum(x[i+1,j] for v,j in lst) + quicksum(x[i-1,j] for v,j in lst)) <= 1)


m.setObjective(quicksum(x[(i, j)]*G[i][i+1]['weight'] for i,j in tc), GRB.MINIMIZE)


m.optimize()

# output to "schedule.csv"
date_col = []
exam_col = []
start_col = []
finish_col = []
for i,j in tc:
    if (x[(i,j)].x):
        if int(i/4) <= 3:
            day = 'July'+ str(int(i/4)+28) + ', 2020'
            date_col.append(day)
        if int(1/4) > 3:
            day = 'August ' + str(int(i/4)-3) + ', 2020 '
            date_col.append(day)
            
        exam_col.append(j)
        
        if i%4 == 0:
            start_col.append('9:00 AM')
            finish_col.append('11:30 AM')
        elif i%4 == 1:
            start_col.append('12:30 PM')
            finish_col.append('3:00 PM')
        elif i%4 == 2:
            start_col.append('4:00 PM')
            finish_col.append('6:30 PM')
        else:
            start_col.append('7:30 PM')
            finish_col.append('10:00 PM')
            
tc_cols = {'Exam': exam_col, 'Date': date_col, 'Start': start_col, 'Finish': finish_col}
df = pd.DataFrame(data=tc_cols)
df.to_csv('Team4_output_schedule.csv', index=False)

