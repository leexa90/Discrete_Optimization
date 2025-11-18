#!/usr/bin/python
# -*- coding: utf-8 -*-


from collections import namedtuple
import math,random
import numpy as np
from sklearn.neighbors import KDTree
import pandas as pd


Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    # build a trivial solution
    # pack the facilities one by one until all the customers are served

    df_fac = pd.DataFrame(facilities)
    df_cust= pd.DataFrame(customers)

    df_cust['x'] = df_cust['location'].apply(lambda p : p.x)
    df_cust['y'] = df_cust['location'].apply(lambda p : p.y)
    df_fac['x'] = df_fac['location'].apply(lambda p : p.x)
    df_fac['y'] = df_fac['location'].apply(lambda p : p.y)
    df_fac['demand'] = 0
    df_cust['assigned'] = -999

    df_fac0 = df_fac.copy()
    df_cust0 = df_cust.copy()

    chose_fac = df_fac0['index'].tolist()

    def get_cost(df_cust,df_fac,chose_fac):
        cost = 0
        for i in df_fac[df_fac['demand']>0].index:
            cost += df_fac.loc[i,'setup_cost']
            df_cust_assigned_i = df_cust[df_cust['assigned']==i]
            cost += np.sum( np.sum((( df_cust[df_cust['assigned']==i][['x','y']]-df_fac.loc[i,['x','y']])**2).values,1)**.5)
        return cost
            

    def greedy_assign(df_fac,df_cust,chose_fac,k_tree):
        df_fac['demand'] = 0
        df_cust['assigned'] = -999


        # get fac available and nearest fac to all customers
        df_fac2 = df_fac[df_fac['index'].isin(chose_fac)].reset_index(drop=1)
        if np.sum(df_fac2['capacity']) > np.sum(df_cust['demand']):
            #df_fac2 = df_fac.copy().iloc[::-1].reset_index(drop=1)
            dictt_map_sampled_dict_id = {}
            for i in df_fac2.index:
                dictt_map_sampled_dict_id[i] = df_fac2.loc[i,'index']
            tree = KDTree(df_fac2[['x','y']].iloc[:]) 
            nearest_fac = tree.query(df_cust[['x','y']],k=k_tree)


            # find customers which 1-3 nearest facility is far apart, means likely to do poorly if first/second choice not met
            df_cust['piority'] = (nearest_fac[0][:,2]-nearest_fac[0][:,0])*df_cust['demand']

            # greedy assign by piority
            fac_i = 0
            for i in df_cust.sort_values('piority',ascending=False).index:
                dd = df_cust.loc[i,'demand']
                for fac_i_unmap in nearest_fac[1][i]:
                    fac_i = dictt_map_sampled_dict_id[fac_i_unmap]
                    if  df_fac.loc[fac_i,'demand']+dd < df_fac.loc[fac_i,'capacity']:
                        df_cust.loc[i,'assigned']=fac_i
                        df_fac.loc[fac_i,'demand'] += dd
                        break
            return df_fac,df_cust

    k_tree = 10
    k=len(chose_fac)
    prev_cost ,new_cost,best_cost = np.inf,np.inf,np.inf

    chose_fac_old = chose_fac.copy()

    df_fac,df_cust = greedy_assign(df_fac0,df_cust0,chose_fac,k_tree) 
    T0 = get_cost(df_cust,df_fac,chose_fac)/len(df_cust)

    for iteration in range(30000):
        T = T0 * 0.999**iteration

        k=len(chose_fac_old )
        prob = np.random.uniform(0,1)
        random.shuffle(chose_fac_old )
        if prob <= 1/3 or k == len(df_fac):
            chose_fac =  chose_fac_old [1:].copy()
        elif prob <= 2/3:
            chose_fac = chose_fac_old [1:].copy() + df_fac[~df_fac['index'].isin(chose_fac)]['index'].sample(n=1).tolist()
        else :
            chose_fac = chose_fac_old [:].copy() + df_fac[~df_fac['index'].isin(chose_fac)]['index'].sample(n=1).tolist()
        
        #print(len(chose_fac))
        try:
            df_fac,df_cust = greedy_assign(df_fac0,df_cust0,chose_fac,k_tree) 
        except : 
            None
        if len(df_cust[df_cust['assigned']==-999]) >0:
            k_tree += 1
            print(k)
        else:
            new_cost = get_cost(df_cust,df_fac,chose_fac)
            if np.exp(-(new_cost - prev_cost)/T) >  np.random.uniform(0,1) :
                prev_cost = new_cost
                chose_fac_old = chose_fac.copy()
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_result = (df_fac.copy(),df_cust.copy())
                    df_cust.to_csv('df_cust.csv',index=0)

            if iteration%1000 == 1:
                print (iteration,new_cost,best_cost,len(chose_fac),T,sorted(chose_fac),)

    solution=best_result[1].assigned.tolist()
    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    # calculate the cost of the solution
    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

