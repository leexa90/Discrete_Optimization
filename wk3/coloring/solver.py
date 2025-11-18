#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    adj_mat = np.zeros((node_count,node_count))
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = list(map(int,line.split()))
        ##edges.append((int(parts[0]), int(parts[1])))
        #print(parts)
        adj_mat[parts[0],parts[1]]=1
        adj_mat[parts[1],parts[0]]=1
    #print(adj_mat)
    solutions = {}
    for n in range(20):
        node_color = np.zeros(node_count)
        color_counter = 1
        num_edges = np.sum(adj_mat,1)
        num_edges2 = np.sum(1*(np.linalg.matrix_power(adj_mat,2)==0),1)
        randn = np.random.randint(0,int(0.03*node_count),size= node_count)
        for edge_i in np.argsort(num_edges*10+randn)[::-1]:
            neighbours = np.argwhere(adj_mat[edge_i]==1)[:,0]
            neighbours_color = node_color[neighbours]
            #print(edge_i,neighbours,neighbours_color)
            for color_i in range(1,color_counter):
                #print (color_i)
                if color_i not in neighbours_color:
                    node_color[edge_i] = color_i
                    #print(color_i,'end')
                    break
            if node_color[edge_i]==0:
                    node_color[edge_i] = color_counter
                    color_counter += 1

        # build a trivial solution
        # every node has its own color
        solution = list(map(int,node_color-1))
        #print('node_color :',node_color )
        solutions[(max(solution),n)] = solution
    best_solution = sorted(solutions.keys())[0]
    solution = solutions[best_solution ]
    #print(solutions.keys(),solution),die
    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    print('output_data:',[output_data])
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

