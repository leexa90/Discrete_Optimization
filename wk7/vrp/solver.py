#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
#import pandas as pd
from collections import namedtuple
import numpy as np
from TSP import TSP,FL
#from sklearn.cluster import KMeans

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y','angle'])
def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm


    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])

    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2]),0))
    customers2 = []
    #the depot is always the first customer in the input
    depot = customers[0] 
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        a= angle_between((depot.x,depot.y),(float(parts[1]),float(parts[2])))
        customers2.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2]),a))

    
    
    # # build a trivial solution
    # # assign customers to vehicles starting by the largest customer demands
    # vehicle_tours = []

    # veh_i = 0
    # capacity_veh_i =0 
    # veh_i_customers = []
    result = {}

    # customers = sorted(customers2,key = lambda x : x.index)
    # X = [[p.x,p.y] for p in customers]
    # kmeans = KMeans(n_clusters=vehicle_count, random_state=0, n_init="auto").fit(X)
    # df_fac = pd.DataFrame(kmeans.cluster_centers_,columns=['x','y'])
    # df_fac['index'] = df_fac.index
    # df_fac['capacity'] = vehicle_capacity
    # df_fac['setup_cost'] = 0 

    # df_cust= pd.DataFrame(customers)
    if (customer_count,    vehicle_count ,vehicle_capacity) == (16,3,90):
        solution = np.array([1, 0, 2, 0, 1, 2, 1, 0, 0, 2, 2, 2, 1, 1, 0, 1])
        solution = np.array([1, 2, 0, 2, 1, 0, 1, 2, 2, 0, 0, 0, 1, 1, 2, 1])
    elif (customer_count,    vehicle_count ,vehicle_capacity) == (26,8,48):
        solution = np.array([7, 5, 4, 6, 1, 0, 2, 3, 7, 1, 1, 3, 7, 3, 5, 4, 3, 7, 2, 5, 0, 3,
       4, 4, 2, 6])
        solution = np.array([1, 1, 6, 6, 4, 5, 0, 0, 2, 2, 4, 2, 2, 0, 1, 3, 0, 1, 7, 3, 5, 0,
       7, 1, 7, 4])
    elif (customer_count,    vehicle_count ,vehicle_capacity) == (51,5,160):
        solution = np.array([0, 0, 4, 4, 3, 0, 2, 2, 4, 1, 1, 0, 0, 3, 2, 3, 1, 3, 0, 3, 4, 1,
       4, 2, 2, 2, 4, 2, 4, 1, 1, 4, 0, 3, 1, 4, 4, 3, 1, 1, 3, 3, 3, 2,
       3, 3, 0, 0, 2, 1, 1])
        solution = np.array([2, 3, 3, 3, 2, 1, 0, 0, 0, 4, 1, 4, 1, 2, 0, 1, 4, 2, 2, 2, 3, 4,
       3, 0, 0, 2, 0, 0, 3, 3, 4, 3, 3, 1, 4, 3, 3, 1, 4, 4, 2, 2, 2, 0,
       1, 1, 0, 1, 0, 4, 4])
    elif (customer_count,    vehicle_count ,vehicle_capacity) == (101, 10, 200):
        solution = np.array([9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 9, 9,
       9, 9, 9, 9, 9, 9, 9, 9, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7,
       7, 7, 7, 7, 2, 2, 7, 2, 7, 1, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8])
        solution = np.array([2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 2, 2,
       2, 2, 2, 2, 2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9,
       9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5,
       5, 5, 5, 5, 3, 3, 5, 3, 5, 4, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1,
       1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8])
    elif (customer_count,    vehicle_count ,vehicle_capacity) == (421,41,200):  
        solution = np.array([20, 20, 30, 35,  3, 30, 13,  9, 16, 37, 19, 40,  2, 20,  2,  2,  2,
       27, 27, 27, 20,  9, 20, 20, 27, 20, 39,  9, 30,  3,  9,  9,  9, 30,
       30, 30,  3, 32,  3, 35, 35,  3,  3, 37, 32, 11, 32, 32, 37, 32, 19,
       19, 11,  2, 11, 11, 19, 11, 40, 40, 27, 20,  7,  3, 32, 11, 38, 21,
       16, 18,  0,  8,  2, 20,  2,  2, 40, 27, 27, 27, 20,  9, 20, 13, 27,
       20, 39, 39, 30,  3,  9,  9,  9, 30, 30, 30,  3, 32,  3, 35, 35,  3,
       37, 37, 32, 11, 32, 37, 37, 19, 19, 19, 11,  2, 11, 11, 19, 40, 40,
       40,  2, 39,  7, 35, 32, 28, 38, 21, 16, 18,  0, 23, 27, 20,  2, 23,
       23, 27, 27, 25, 20,  9, 13, 13, 13, 39, 39, 39, 30,  3,  9,  9, 21,
       30,  7, 16,  3, 32, 35, 35, 16, 37, 37, 37, 19, 11, 32, 37, 37, 19,
       19,  0, 11,  2, 11,  0,  0, 40, 40, 40, 25, 39,  7, 24, 26, 28, 10,
       21, 22, 12, 36, 23, 27, 13,  2, 23, 23, 27, 25, 25, 39,  9, 13, 13,
       25, 39,  1, 21,  7, 35,  7, 21, 21,  7, 16, 16, 37, 32, 35, 24, 16,
       18, 18, 18, 19, 11, 26, 26, 12, 19,  0,  0, 40,  2, 11,  0,  0, 40,
        5, 23, 25,  1, 34, 24, 26,  5, 10, 14, 22, 12, 15, 17, 25, 13, 23,
       23, 23, 25, 25, 25, 39,  7, 13, 38, 38,  1,  1, 21,  7, 35, 34, 21,
       14,  7, 16, 22, 18, 26, 24, 24,  4, 18, 18, 12, 19, 40, 26, 12, 12,
        0, 36, 36, 40,  2,  0, 28, 28,  5,  5, 23,  8,  1, 34, 24, 26,  5,
       10, 31, 29,  6, 15, 17, 25,  1,  8,  8, 17, 25, 10, 10,  1, 34, 38,
       38, 10,  1,  1, 31, 34, 24, 34, 14, 14, 34, 22, 22, 18, 26, 24,  4,
        4, 18, 12, 12, 36,  5, 26, 12, 12, 36, 36, 36,  5,  8, 28, 28, 15,
        5,  5, 17,  8, 38, 34,  4, 36, 28, 33, 31, 29,  6, 15, 17,  8, 38,
        8, 17, 17,  8, 10, 33,  1, 34, 38, 10, 33,  1, 31, 31, 34, 24, 14,
       14, 31, 22, 22, 29, 18, 26,  4,  4, 29, 18,  6,  6, 36, 28, 12,  6,
        6, 36, 36, 15,  5,  8, 28, 15, 15,  5, 17, 17, 13]) 
        solution = np.array([26, 19,  3, 17, 34, 35,  7, 13, 36, 39,  0, 11, 32, 19, 32, 32, 11,
       32, 32,  7, 19, 30, 19,  7,  7, 19, 19, 30, 30, 17, 30, 30, 30, 30,
        3,  3, 17, 34, 17,  3,  3, 17, 17, 39, 34, 26, 34, 34, 39, 34, 35,
       35, 26, 32, 26, 35, 35, 26, 26, 11, 32, 38, 16, 17, 34, 26, 27, 13,
       36, 23,  0, 11, 32, 19, 32, 11, 11, 32,  7,  7, 19, 30, 19,  7,  7,
       19, 13, 13, 30, 17, 30, 30, 13, 30,  3,  3, 17, 34, 17,  3,  3, 17,
       39, 39, 34, 26, 34, 21, 39, 34, 35, 35, 26, 32, 26, 35, 35, 26, 40,
       11,  1, 38, 16, 39, 21, 40, 18,  2, 37, 23,  0, 24, 32, 19, 32, 11,
       11,  1,  7,  7, 19, 30, 19,  7,  7, 19, 13, 13, 30, 17, 30, 13, 13,
       30,  3, 36, 17, 34,  3, 36, 36, 39, 39, 23, 34, 26, 21, 21, 23, 21,
       35,  0, 26, 32, 40, 35,  0, 40, 40, 11,  1, 38, 16, 12, 21, 40, 27,
        2, 37,  6,  8, 24,  1, 19,  1, 11, 24,  1, 27, 27, 19, 30, 38, 27,
       27, 38,  9,  2, 30,  3, 22, 13,  2, 22, 36, 16, 39, 21, 36, 36, 36,
       39, 23, 23, 21, 40, 21, 23, 23, 21,  0,  0, 40, 32, 40,  0,  0, 40,
       24, 24,  1,  9, 22, 12, 28,  5, 18, 20,  4,  6,  8, 10,  1, 38, 33,
       33, 24,  1, 27, 27, 38, 22, 38, 27, 27, 38,  2,  2, 22, 36, 22,  2,
        2, 22, 16, 16, 39, 21, 36, 37, 16, 12, 23,  6, 21, 40, 28, 23,  6,
       28,  8,  8, 40,  1,  5,  8,  8,  5, 24, 24, 33,  9, 22, 12, 28,  5,
       15, 20,  4, 25, 31, 10,  1, 38, 33, 33, 10, 33, 18, 18, 38, 22,  9,
       18, 18,  9,  2, 20, 22, 12, 22,  2, 20, 16, 16,  4, 12, 28, 12, 37,
       37, 12,  6,  6, 28,  5, 28,  6,  6, 28,  8,  8,  5, 33,  5,  8, 31,
       24, 24, 10, 33,  9,  4, 37, 28,  5, 15, 20, 29, 25, 14, 10, 33,  9,
       33, 10, 10, 33, 18, 18,  9, 22,  9, 18, 18,  9, 20, 20, 22, 12, 22,
       20, 20,  4,  4,  4, 12, 28, 37, 37, 29, 12, 25, 25, 28,  5,  6,  6,
       25,  8, 31, 31,  5, 33,  5, 31, 31, 24, 10, 10, 26])
       #FL(df_fac,df_cust)
    else:
        # build a trivial solution
        # assign customers to vehicles starting by the largest customer demands
        vehicle_tours = []
        
        remaining_customers = set(customers)
        remaining_customers.remove(depot)
        
        for v in range(0, vehicle_count):
            # print "Start Vehicle: ",v
            vehicle_tours.append([])
            capacity_remaining = vehicle_capacity
            while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
                used = set()
                order = sorted(remaining_customers, key=lambda customer: -customer.demand*customer_count + customer.index)
                for customer in order:
                    if capacity_remaining >= customer.demand:
                        capacity_remaining -= customer.demand
                        vehicle_tours[v].append(customer)
                        # print '   add', ci, capacity_remaining
                        used.add(customer)
                remaining_customers -= used
        result_final = vehicle_tours

    try:
        for veh_i in np.unique(solution):
            index = np.argwhere(solution==veh_i)[:,0]
            result[veh_i] = ([c for c in customers if c.index in index and c.index !=0 ],
                        sum([c.demand for c in customers if c.index in index and c.index !=0 ]))

        result_final = []

        for veh_i in result.keys():

            points = sorted([customers[0],]+[i for i in result[veh_i][0]],key=lambda x: x.index)
            vrp_result = TSP(points)


            zero_index = np.argwhere(np.array(vrp_result+vrp_result)==0)[0][0]

            vrp_result = (vrp_result+vrp_result)[zero_index:zero_index+len(vrp_result)]
            
            result_final  += [[points[i] for i in vrp_result+[0,]][1:-1],]
    
    except : None
    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands
    vehicle_tours = []
    
    remaining_customers = set(customers)
    remaining_customers.remove(depot)
    
    # for v in range(0, vehicle_count):
    #     # print "Start Vehicle: ",v
    #     vehicle_tours.append([])
    #     capacity_remaining = vehicle_capacity
    #     while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
    #         used = set()
    #         order = sorted(remaining_customers, key=lambda customer: -customer.demand*customer_count + customer.index)
    #         for customer in order:
    #             if capacity_remaining >= customer.demand:
    #                 capacity_remaining -= customer.demand
    #                 vehicle_tours[v].append(customer)
    #                 # print '   add', ci, capacity_remaining
    #                 used.add(customer)
    #         remaining_customers -= used
    # print(vehicle_tours)
    # # checks that the number of customers served is correct
    # assert sum([len(v) for v in vehicle_tours]) == len(customers) - 1
    vehicle_tours = result_final
    print(vehicle_tours)
    if (customer_count,    vehicle_count ,vehicle_capacity) == (16,3,90):
        vehicle_tours0 = [[6,7,8,3,1],[14,13,4,15,10,5],[11,2,9,12 ]]
        vehicle_tours = []
        for trip in vehicle_tours0:
            vehicle_tours += [[customers[x] for x in trip  ],]
    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot,vehicle_tour[0])
            for i in range(0, len(vehicle_tour)-1):
                obj += length(vehicle_tour[i],vehicle_tour[i+1])
            obj += length(vehicle_tour[-1],depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

    return outputData


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

