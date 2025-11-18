#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)
    if item_count*capacity > 200*100000:
        for item in sorted(items,key = lambda x : -x.value/x.weight):
            if weight + item.weight <= capacity:
                taken[item.index] = 1
                value += item.value
                weight += item.weight
    else:
        #dynamic programming
        # item_count = 4
        # capacity = 7
        #Item = namedtuple("Item", ['index', 'value', 'weight'])
        #item = [(16,1),(22,3),(23,3),(28,6)]
        #items = []
        # for i in range(1, item_count+1):
        #     items.append(Item(i-1, int(item[i-1][0]), int(item[i-1][1])))
        #df= pd.DataFrame([],columns=range(item_count+1),index=range(0,capacity+1)).fillna(0)
        df = {}
        for i in  range(0, item_count+1) :
            for j in range(0,capacity+1): 
                df[(j,i)] = 0

        for i in  range(1, item_count+1) :
            v = items[i-1].value
            w = items[i-1].weight
            for j in range(1,capacity+1):
                if i==1:
                    if j >= w:
                        df[(j,i)] = v
                else:
                    if j>=w:
                        df[(j,i)] = max(df[(j-w,i-1)]+v , df[(j,i-1)] )
                    else:
                        df[(j,i)] =  df[(j,i-1)]
        j = capacity 
        got = []
        for i in range(item_count,0,-1):
            v = items[i-1].value
            w = items[i-1].weight
            if i !=0 :
                if df[(j,i)] == df[(j,i-1)]:
                    continue
                else:
                    for j2 in range(j,1,-1):
                        if df[(j,i)] == df[(j2,i)]:
                            j =j2
                    #print('impt',i,j)
                    j += -w
                    taken[i-1] = 1
        #print(taken)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

