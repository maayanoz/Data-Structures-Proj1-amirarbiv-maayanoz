'''
    In order to run the tester:
    1.  Make sure your AVLTree.py file and this file
        are both in the same directory.
    2.  Run: python3 student_tester.py  
    3.  Your grade will be printed at the end.
        Only failed tests will be printed.
'''

import unittest
from AVLFingerTree import AVLFingerTree
import random

# ----------------------------
# AVLFingerTree insertion_sort
# ----------------------------
# Implement insertion_sort(arr) in AVLFingerTree class in AVLFingerTree.py
# Specifications:
# - Uses AVL tree insertion to insert each number from arr in the given order.
# - After all insertions, performs an in-order traversal to produce a sorted array.
# - Returns a tuple: (sorted_array, rebalance_ops, search_ops)
#   where:
#   - sorted_array: the sorted list of numbers
#   - rebalance_ops: total number of height changes during rebalancing
#   - search_ops: total number of node visits during all insertions (searches)
# - Resets the tree and stats at the start of the method.
# - You may add helper methods as needed.
# - Do NOT modify other parts of AVLFingerTree or AVLNode classes.
# ---------------------------- 

# Testing code - switches in sorted array

print("Testing switches in sorted array:")
for i in range (1,6):
    arr = []
    for j in range (1, 300*(2**i)+1):
        arr.append(j)
    count = 0
    for t in range(len(arr)-1):
        for p in range(t+1,len(arr)):
            if arr[p] < arr[t]:
                count += 1
    print(count)
    print()

# Testing code - switches in reversed sorted array

print("Testing switches in reversed sorted array:")
for i in range (1,6):
    arr = []
    for j in range (1, 300*(2**i)+1):
        arr.append(300*(2**i)+1-j)
    count = 0
    for t in range(len(arr)-1):
        for p in range(t+1,len(arr)):
            if arr[p] < arr[t]:
                count += 1
    print(count)
    print()

# Testing code - switches in random array

print("Testing switches in random array:")
for i in range (1,6):
    tot_count = 0
    for k in range(20):
        arr = list(range(1, 300*(2**i)+1))
        random.shuffle(arr)
        count = 0
        for t in range(len(arr)-1):
            for p in range(t+1,len(arr)):
                if arr[p] < arr[t]:
                    count += 1
        tot_count += count
    print(tot_count // 20)
    print()

# Testing code - switches in random switches array

print("Testing switches in random switches array:")
for i in range (1,6):
    tot_count = 0
    for k in range(20):
        arr = list(range(1, 300*(2**i)+1))
        for j in range(len(arr)-1):
            p = random.random()
            if p < 0.5:
                arr_j = arr[j]
                arr_j1 = arr[j+1]
                arr[j], arr[j+1] = arr_j1, arr_j
        count = 0
        for t in range(len(arr)-1):
            for s in range(t+1,len(arr)):
                if arr[s] < arr[t]:
                    count += 1
        tot_count += count
    print(tot_count // 20)
    print()

# Testing code - sorted array

print("Testing sorted array:")
for i in range (1,11):
    t = AVLFingerTree()
    arr = []
    for j in range (1, 300*(2**i)+1):
        arr.append(j)
    sorted_arr, reb_ops, search_ops = t.insertion_sort(arr)
    #print(sorted_arr)   # sorted array
    print(reb_ops)      # height-change count (during rebalancing only)
    print(search_ops)   # node-visit count during searches
    print()

# Testing code - reversed sorted array

print("Testing reversed sorted array:")
for i in range (1,11):
    t = AVLFingerTree()
    arr = []
    for j in range (1, 300*(2**i)+1):
        arr.append(300*(2**i)+1-j)
    sorted_arr, reb_ops, search_ops = t.insertion_sort(arr)
    #print(sorted_arr)   # sorted array
    print(reb_ops)      # height-change count (during rebalancing only)
    print(search_ops)   # node-visit count during searches
    print()

# Testing code - random array

print("Testing random array:")
for i in range (1,11):
    reb_ops_sum = 0
    search_ops_sum = 0
    for k in range(20):
        t = AVLFingerTree()
        arr = list(range(1, 300*(2**i)+1))
        random.shuffle(arr)
        sorted_arr, reb_ops, search_ops = t.insertion_sort(arr)
        reb_ops_sum += reb_ops
        search_ops_sum += search_ops
    print(reb_ops_sum // 20)
    print(search_ops_sum // 20)
    print()


# Testing code - random switches array

print("Testing random swithces array:")
for i in range (1,11):
    reb_ops_sum = 0
    search_ops_sum = 0
    for k in range(20):
        t = AVLFingerTree()
        arr = list(range(1, 300*(2**i)+1))
        for j in range(len(arr)-1):
            p = random.random()
            if p < 0.5:
                arr_j = arr[j]
                arr_j1 = arr[j+1]
                arr[j], arr[j+1] = arr_j1, arr_j
        sorted_arr, reb_ops, search_ops = t.insertion_sort(arr)
        reb_ops_sum += reb_ops
        search_ops_sum += search_ops
    print(reb_ops_sum // 20)
    print(search_ops_sum // 20)
    print()






    
    



