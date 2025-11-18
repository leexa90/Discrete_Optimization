#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
from collections import namedtuple
import random

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def get_score(d):
    r = [x[2] for x in d]
    return np.sum(r)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    # print(points)
    D = {}
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
    best_result = solution_edge.copy()
    if nodeCount <=600:
        for attempt in range(10):
            solution_edge = best_result.copy()
            best_score = get_score(best_result)
            current_score = get_score(solution_edge)
            print(best_score,current_score)
            if best_score < 430 and nodeCount == 51:
                break
            if best_score < 20800 and nodeCount==100:
                break
            if best_score < 30000 and nodeCount==200:
                break
            if best_score < 40000 and nodeCount==574:
                break
            T0 = get_score(solution_edge)/len(best_result)
            iteration = 0
            sucess = 1
            while iteration <=3000000  or sucess >= 0.05:
                T = T0*0.999998**np.abs(iteration)
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
                        current_score += score
                        sucess  = 0.995*sucess + 0.001
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
                        sucess  = 0.995*sucess 

                    if iteration%200000==0:
                        print(attempt,iteration,get_score(solution_edge),T)

                # reorder wrongly directed edges


    solution = []
    for i in solution_edge:
        solution += [i[0],]

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
    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

