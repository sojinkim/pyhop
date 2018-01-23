"""
This file should work correctly in both Python 2.7 and Python 3.2.
download https://bitbucket.org/dananau/pyhop/downloads/
$ python pyhop_test.py
"""

import pyhop

def at_same_place(state,a,b):
    return state.loc[a] == state.loc[b]

def search_for_ring(state):
    for k in state.ring:
        if state.ring[k] > 0: return k
    return None

 

def goto(state,a,p):
    state.loc[a] = p
    return state

def pickup_ring(state,a):
    if state.ring[state.loc[a]] > 0:
        state.own[a]['ring'] += 1 
        state.ring[state.loc[a]] -= 1
        return state
    else:
        return False 

def give(state,a,b,x):
    if at_same_place(state,a,b) and state.own[a][x] > 0:
        state.own[a][x] -= 1
        state.own[b][x] += 1
        state.like[b][a] += 50
        state.happiness[b] += 20
        state.happiness[a] += 20
        return state
    else: 
        return False 

def talk(state,a,b):
    if at_same_place(state,a,b):
        state.like[b][a] += 20
        state.like[a][b] += 20
        state.happiness[b] += 20
        state.happiness[a] += 20
        return state
    else: 
        return False 


def steal_ring(state,a,b):
    if at_same_place(state,a,b) and state.own[b]['ring'] > 0:
        if state.like[b][a] > 0: 
            state.happiness[b] -= 50
        state.own[b]['ring'] -= 1
        state.own[a]['ring'] += 1
        state.upset[b] += 50
        state.like[b][a] -= 50
        state.stole[a][b]['ring'] += 1
        return state
    else: 
        return False 


def yell(state,a,b):
    if at_same_place(state,a,b):
        if state.like[b][a] > 0: 
            state.happiness[b] -= 20
        state.upset[b] += 20
        state.like[b][a] -= 20
        return state
    else: 
        return False 


def appology(state,a,b):
    if at_same_place(state,a,b):
        if state.upset[b] <= 20: 
            state.upset[b] = 0 
        else:
            state.upset[b] -= 20
        state.like[b][a] += 20
        return state
    else: 
        return False

def return_ring(state,a,b):
    if at_same_place(state,a,b) and state.stole[a][b]['ring'] > 0:
        state.own[b]['ring'] += 1
        state.own[a]['ring'] -= 1
        if state.upset[b] <= 50: 
            state.upset[b] = 0 
        else:
            state.upset[b] -= 50
        state.like[b][a] += 50
        state.stole[a][b]['ring'] -= 1
        return state
    else:
        return False

def say_love(state,a,b):
    if at_same_place(state,a,b):
        state.happiness[b] += 50
        return state
    else:
        return False

def curse(state,a,b):
    if at_same_place(state,a,b):
        state.happiness[b] -= 50
        return state
    else:
        return False

def suicide(state,a):
    return state

def get_job(state,a):
    state.happiness[a] += 10
    return state

def work(state, a):
    state.own[a]['gold'] += 1
    return state 

def buy(state,a,x):
    if state.own[a]['gold'] > 0:
        state.own[a]['gold'] -= 1
        state.own[a][x] += 1 
        return state
    else:
        return False



pyhop.declare_operators(get_job, work, buy, appology, return_ring, say_love, goto, pickup_ring, give, talk, steal_ring, yell, curse, suicide)


