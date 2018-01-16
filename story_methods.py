"""
This file should work correctly in both Python 2.7 and Python 3.2.
download https://bitbucket.org/dananau/pyhop/downloads/
$ python pyhop_test.py
"""

import pyhop
import story_operators as op

last = pyhop.State('last')

def get_ring(state,a):
    if state.ring[state.loc[a]] > 0:
        return [('pickup_ring',a)]
    else:
        ring_loc = op.search_for_ring(state)
        if ring_loc is None: 
            return False
        return [('goto',a,ring_loc),('pickup_ring',a)]

pyhop.declare_methods('get_ring',get_ring)


def attract_by_talk(state,a,b,goal):
    if state.like[b][a] >= goal.like[b][a]: 
	global last
	last = state
        return []
    if state.like[b][a] < 50:
        if op.at_same_place(state,a,b):
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
    if state.own[a]['ring'] == False:
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
    if state.own[b]['ring'] == False:
        return [('upset',a,b)]
    if state.loc[a] == state.loc[b]:
        return [('steal_ring',a,b),('upset',a,b,goal)]
    else:
        return [('goto',a,state.loc[b]),('upset',a,b,goal)]

pyhop.declare_methods('upset',upset_by_yelling,upset_by_stealing)


def make_calm_by_appology(state,a,b,goal):
    if state.upset[b] <= goal.upset[b]:
        return []
    if state.upset[b] <= 50:
        return False
    if op.at_same_place(state,a,b):
        return [('appology',a,b),('make_calm',a,b,goal)]
    else: 
        return [('goto',a,state.loc[b]),('make_calm',a,b,goal)]

def make_calm_by_return_ring(state,a,b,goal):
    if state.upset[b] <= goal.upset[b]:
        return []
    if op.at_same_place(state,a,b):
        return [('return_ring',a,b),('make_calm',a,b,goal)]
    else:
        return [('goto',a,state.loc[b]),('make_calm',a,b,goal)]

pyhop.declare_methods('make_calm',make_calm_by_appology,make_calm_by_return_ring)

def make_happy(state,a,b,goal):
    if state.happiness[b] >= goal.happiness[b]:
        return []
    if op.at_same_place(state,a,b):
        return [('say_love',a,b),('make_happy',a,b,goal)]
    else:
        return [('goto',a,state.loc[b]),('make_happy',a,b,goal)]

pyhop.declare_methods('make_happy',make_happy)

def happy_ending(state,a,goal):
    if state.upset[a] > goal.upset[a]:
        return [('make_calm','jack',a,goal),('happy_ending',a,goal)]
    if state.happiness[a] < goal.happiness[a]:
        return [('make_happy','marry',a,goal),('happy_ending',a,goal)]
    else: 
        global last
        last = state
        return []

pyhop.declare_methods('happy_ending',happy_ending)


