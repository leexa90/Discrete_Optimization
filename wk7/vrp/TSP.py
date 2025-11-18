#!/usr/bin/python
# -*- coding: utf-8 -*-

import random,math
from collections import namedtuple
import numpy as np
#from pyomo.environ import *

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def get_score(d):
    r = [x[2] for x in d]
    return np.sum(r)
def TSP(points):
    # Modify this code to run your optimization algorithm
    nodeCount = len(points)
    # print(points)
    # build a trivial solution
    # visit the nodes in the order they appear in the file

    solution = list(range(len(points)))
    random.shuffle(solution)

    solution_edge = []
    for i in range(0,len(solution)-1):
        solution_edge += [(solution[i],solution[i+1],
                           length(points[solution[i]],points[solution[i+1]]))]
    solution_edge+= [(solution[i+1],solution[0],
                      length(points[solution[i]],points[solution[0]])),]
    print(get_score(solution_edge))
    print(solution_edge)
    best_result = solution_edge.copy()
    if nodeCount <=600:
        for attempt in range(30):
            random.shuffle(solution)

            solution_edge = []
            for i in range(0,len(solution)-1):
                solution_edge += [(solution[i],solution[i+1],
                                length(points[solution[i]],points[solution[i+1]]))]
            solution_edge+= [(solution[i+1],solution[0],
                            length(points[solution[i]],points[solution[0]])),]
            solution_edge = best_result.copy()
            best_score = get_score(best_result)
            current_score = get_score(solution_edge)
            print(best_score,current_score)
            T0 = get_score(solution_edge)/len(best_result)
            iteration = 0
            sucess = 1
            while iteration <=3000 :
                T = T0*0.998**np.abs(iteration)
                iteration += 1
                #get crisscross edges, to not do all the tiume for faster speed
                for k in range(2,3):#def k_opt(solution_edge,points,obj):
                    edge_i = np.random.choice(range(len(solution_edge)))

                    x1 = solution_edge[edge_i][0]
                    x2 = solution_edge[edge_i][1]

                    for edge_j in np.random.choice(range(len(solution_edge)),size=6):
                        x3 = solution_edge[edge_j][0]
                        x4 = solution_edge[edge_j][1]
                        if x4 not in [x1,x2] and x3 not in [x1,x2]:
                            break
                    if edge_i > edge_j:
                        edge_i,edge_j = edge_j,edge_i
                        x1 = solution_edge[edge_i][0]
                        x2 = solution_edge[edge_i][1]
                        x3 = solution_edge[edge_j][0]
                        x4 = solution_edge[edge_j][1]

                    
                    newedge_x1x3 = (x1,x3,length(points[x1],points[x3]))
                    newedge_x2x4 = (x2,x4,length(points[x2],points[x4]))

                    score = -solution_edge[edge_i][2] - solution_edge[edge_j][2]
                    score += newedge_x1x3[2] + newedge_x2x4[2]

                    if np.exp(-score/T) > np.random.uniform(0,1) :
                        if x1!=x3 and x2!=x4:
                            current_score += score
                            sucess  = 0.95*sucess + 0.05
                            solution_edge[edge_i] = newedge_x1x3
                            solution_edge[edge_j] = newedge_x2x4
                            
                            earlier_edge = min(edge_i,edge_j)
                            laster_edge = max(edge_i,edge_j)
                            temp = []
                            for edge_k in range(earlier_edge+1,laster_edge):
                                a,b,c = solution_edge[edge_k]
                                temp += [(b,a,c),]
                            for edge_k in range(earlier_edge+1,laster_edge):
                                solution_edge[edge_k] = tuple(temp.pop())

                            if best_score > current_score:
                                best_result = solution_edge.copy()
                                best_score = get_score(best_result)
                                current_score = get_score(solution_edge)

                    else: 
                        sucess  = 0.95*sucess 

                    if iteration%100000==0:
                        print(attempt,iteration,get_score(solution_edge),T)

                # reorder wrongly directed edges


    solution = []
    for i in best_result:
        solution += [i[0],]
    print(solution_edge)

    # calculate the length of the tour
    obj = []
    for index in range(0, nodeCount-1):
        obj += [length(points[solution[index]], points[solution[index+1]]),]
    obj += [length(points[solution[-1]], points[solution[0]]),]
    print (obj)

    # prepare the solution in the specified output format
    output_data = '%.2f' % np.sum(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    print(output_data)
    return solution


def FL(df_fac,df_cust):
    df_fac['demand'] = 0
    df_cust['assigned'] = -999


    N = len(df_fac)
    M = len(df_cust)
    P = 3
    d = np.sum((np.expand_dims(df_fac[['x','y']].values,1) - np.expand_dims(df_cust[['x','y']].values,0))**2,-1)**.5



    model = ConcreteModel()
    model.Locations = list(range(N))
    model.Customers = list(range(M))
    model.x = Var( model.Locations, model.Customers,within=Binary  ) #discrete, facilty,cust matrix
    model.y = Var( model.Locations, within=Binary ) #facility is open/closed

    model.obj = Objective( expr = sum( d[n,m]*model.x[n,m] for n in model.Locations for m in model.Customers )\
                          + sum([model.y[n]*c for n,c in zip(model.Locations,df_fac['setup_cost'])]),
                          sense=minimize )
    model.single_x = ConstraintList()
    for m in model.Customers:
        model.single_x.add(sum( model.x[n,m] for n in model.Locations ) == 1.0 )
    model.bound_y = ConstraintList()
    for n in model.Locations:
        for m in model.Customers:
            model.bound_y.add( model.x[n,m] <= model.y[n] )

    for n in model.Locations:
          model.bound_y.add( sum([ d*model.x[n,m] for m,d in zip(model.Customers,df_cust['demand']) ]) <=df_fac.loc[n,'capacity'] )
    model.num_facilities = Constraint(expr=sum( model.y[n] for n in model.Locations ) == N )

    #model.pprint()
    SolverFactory('cbc', executable='/usr/bin/cbc').solve(model).write()


    solution = np.argmax(np.reshape(model.x[:,:](),(N,M)),0)
    return solution

