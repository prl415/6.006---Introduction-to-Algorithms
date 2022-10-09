#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 22:36:04 2022

@author: mgokdeniz
"""

def ADD(A, B, N):
    pass

def MULTIPLY(A, B, N):
    pass

def SUB(A, B, N):
    pass

def CMP(A, B, N):
    pass

def DIV(A, B, N):
    pass

def MOD(A, B, N):
    pass

def fast_exp(A, B, N):
    '''
    Returns the result of A^B
    '''
    if CMP(B, 0, N) == 'EQUAL':
        return 1
    
    elif CMP(B, 1, N) == 'EQUAL':
        return A
    
    elif CMP(B, SUB(0, -1, 1), N) == 'EQUAL':
        return DIV(1, A, N)

    else:
        exp = DIV(A, B, N)
        if MOD(A, B, N):
            return MULTIPLY(fast_exp(A, exp, N), fast_exp(A, exp, N), N)
        else:
            return MULTIPLY(fast_exp(A, exp + 1, N), fast_exp(A, exp, N), N)
        
def kth_root(A, K, N):
    tol = fast_exp(10, 6, 6)
    high = A
    low = 0
    guess = DIV(high, low, N)
    while CMP(SUB(fast_exp(guess, K, N), A, N), tol, N) == 'GREATER':
        if CMP(fast_exp(guess, K, N), A, N) == 'GREATER':
            high = guess
        else:
            low = guess
        guess = DIV(high, low, N)
        
    return guess
