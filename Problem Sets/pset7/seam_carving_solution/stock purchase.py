#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 21:21:29 2022

@author: mgokdeniz
"""

def limited_stock_table(total, count, start, end, limit):
    profit = [[i for j in range(0, count + 1)] for i in range(0, total + 1)]  # O(count * total)
    
    for cash in range(0, total + 1): # O(total * count * (sum of all finite stock limits))
        profit[cash][0] = cash
        
        for stock in range(1, count + 1): # O(count * (sum of all finite stock limits))
            profit[cash][stock] = profit[cash][stock - 1]
            
            for quantity in range(1, min([limit[stock], int(cash/start[stock])]) + 1): #O(sum of all finite stock limits)
              
                leftover = cash - quantity * start[stock]
                current = quantity * end[stock] + profit[leftover][stock - 1]
                if profit[cash][stock] < current:
                    profit[cash][stock] = current
                        
    return profit[-1][-1]

start = [0, 12, 10, 18, 15]

end = [0, 39, 13, 47, 45]

limit = [0, 3, float('inf'), 2, 1]

count = 4

total = 30