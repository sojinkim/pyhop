"""
This file should work correctly in both Python 2.7 and Python 3.2.
download https://bitbucket.org/dananau/pyhop/downloads/
$ python pyhop_test.py
"""

import pyhop
import story_operators
from story_util import * 

last = pyhop.State('last')



def get_ring(state,a):
    if state.ring[state.loc[a]] > 0:
        return [('pickup_ring',a)]
    else:
        ring_loc = search_for_ring(state)
        if ring_loc is None: 
            return [('buy_ring',a)]
        else:
            return [('goto',a,ring_loc),('pickup_ring',a)]

pyhop.declare_methods('get_ring',get_ring)


def make_money(state,a):
    return [('goto',a,'factory'),('get_job',a),('work',a)]

pyhop.declare_methods('make_money',make_money)

def buy_ring(state,a):
    if state.own[a]['gold'] > 0:
        return [('goto',a,'shop'),('buy',a,'ring')]
    else:
        return [('make_money',a),('buy_ring',a)]

pyhop.declare_methods('buy_ring',buy_ring)


def attract_by_talk(state,a,b,goal):
    if state.like[b][a] >= goal.like[b][a]: 
	global last
	last = state
        return []
    if state.like[b][a] < 50:
        if at_same_place(state,a,b):
            return [('talk',a,b),('attract',a,b,goal)]
        else:
            return [('goto',a,state.loc[b]),('talk',a,b),('attract',a,b,goal)]
    else:
        return False

def attract_by_gift(state,a,b,goal):
    if state.like[b][a] >= goal.like[b][a]: 
	global last
	last = state
        return []
    if state.own[a]['ring'] == 0:
        return [('get_ring',a),('attract',a,b,goal)]
    if state.loc[a] == state.loc[b]:
        return [('give',a,b,'ring'),('attract',a,b,goal)]
    else:
        return [('goto',a,state.loc[b]),('give',a,b,'ring'),('attract',a,b,goal)]

pyhop.declare_methods('attract',attract_by_talk,attract_by_gift)


def upset_by_yelling(state,a,b,goal):
    if state.upset[b] >= goal.upset[b]: 
	global last
	last = state
        return []
    if state.upset[b] >= 50:
        return False
    if state.loc[a] == state.loc[b]:
        return [('yell',a,b),('upset',a,b,goal)]
    else:
        return [('goto',a,state.loc[b]),('upset',a,b,goal)]

def upset_by_stealing(state,a,b,goal):
    if state.upset[b] >= goal.upset[b]: 
	global last
	last = state
        return []
    if state.own[b]['ring'] == 0:
        return [('upset',a,b)]
    if state.loc[a] == state.loc[b]:
        return [('steal_ring',a,b),('upset',a,b,goal)]
    else:
        return [('goto',a,state.loc[b]),('upset',a,b,goal)]

pyhop.declare_methods('upset',upset_by_yelling,upset_by_stealing)


def make_calm_by_appology(state,a,b):
    if state.upset[b] <= 0:
        return []
    if state.upset[b] <= 50 or state.like[b][a] >= 0:
        return False
    if at_same_place(state,a,b):
        return [('appology',a,b),('make_calm',a,b)]
    else: 
        return [('goto',a,state.loc[b]),('make_calm',a,b)]

def make_calm_by_return_ring(state,a,b):
    if state.upset[b] <= 0:
        return []
    if at_same_place(state,a,b):
        return [('return_ring',a,b),('make_calm',a,b)]
    else:
        return [('goto',a,state.loc[b]),('make_calm',a,b)]

pyhop.declare_methods('make_calm',make_calm_by_appology,make_calm_by_return_ring)

def make_happy(state,a,b,goal):
    if state.happiness[b] > goal.happiness[b]:
        return []
    if at_same_place(state,a,b):
        return [('say_love',a,b),('make_happy',a,b)]
    else:
        return [('goto',a,state.loc[b]),('make_happy',a,b)]

pyhop.declare_methods('make_happy',make_happy)


def make_unhappy(state,a,b,goal):
    if most_unhappy(state) == b and state.happiness[b] < goal.happiness[b]: 
        return []
   
    if at_same_place(state,a,b):
        return [('curse',a,b),('make_unhappy',a,b,goal)]
    else:
        return [('goto',a,state.loc[b]),('make_unhappy',a,b,goal)]

pyhop.declare_methods('make_unhappy',make_unhappy)


def happy_ending(state,a,goal):
    if state.upset[a] > 0:
        return [('make_calm',most_dislike(state,a),a),('happy_ending',a,goal)]
    if state.happiness[a] < 100:
        return [('make_happy',most_like(state,a),a,goal),('happy_ending',a,goal)]
    else: 
        global last
        last = state
        return []

pyhop.declare_methods('happy_ending',happy_ending)
    
def bad_ending(state,a,goal):
    one = most_like(state,a)
    if state.happiness[a] < -50:
        global last
        last = state 
        return []
    else:
        return[('make_unhappy',one,a,goal),('bad_ending',a,goal)]

pyhop.declare_methods('bad_ending',bad_ending)



