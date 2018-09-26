"""
This file should work correctly in both Python 2.7 and Python 3.2.
download https://bitbucket.org/dananau/pyhop/downloads/
$ python pyhop_test.py
"""

import pyhop
last = pyhop.State('last')

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
        state.own[a]['ring'] = True
        state.ring[state.loc[a]] -= 1
        return state
    else:
        return False 

def give(state,a,b,x):
    if at_same_place(state,a,b) and state.own[a][x] == True:
        state.own[a][x] = False
        state.own[b][x] = True
        state.like[b][a] += 50
        state.like[a][b] += 20
        state.happiness[b] += 50
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
    if at_same_place(state,a,b):
        state.upset[b] += 50
        state.happiness[b] -= 50
        state.own[b]['ring'] = False
        return state
    else: 
        return False 


def yell(state,a,b):
    if at_same_place(state,a,b):
        state.upset[b] += 20
        state.happiness[b] -= 20
        return state
    else: 
        return False 


def appology(state,a,b):
    if at_same_place(state,a,b):
        if state.upset[b] <= 20: 
            state.upset[b] = 0 
        else:
            state.upset[b] -= 20
        return state
    else: 
        return False

def return_ring(state,a,b):
    if at_same_place(state,a,b):
        if state.upset[b] <= 50: 
            state.upset[b] = 0 
        else:
            state.upset[b] -= 50
        return state
    else:
        return False

def say_love(state,a,b):
    if at_same_place(state,a,b):
        state.happiness[b] += 50
        return state
    else:
        return False



pyhop.declare_operators(appology, return_ring, say_love, goto, pickup_ring, give, talk, steal_ring, yell)
print('')
pyhop.print_operators()


def get_ring(state,a):
    if state.ring[state.loc[a]] > 0:
        return [('pickup_ring',a)]
    else:
        ring_loc = search_for_ring(state)
        if ring_loc is None: 
            return []
        return [('goto',a,ring_loc),('pickup_ring',a)]

pyhop.declare_methods('get_ring',get_ring)


def attract_by_talk(state,a,b):
    if state.like[b][a] >= goal.like[b][a]: 
	global last
	last = state
        return []
    if state.like[b][a] < 50:
        if at_same_place(state,a,b):
            return [('talk',a,b),('attract',a,b)]
        else:
            return [('goto',a,state.loc[b]),('talk',a,b),('attract',a,b)]
    else:
        return False

def attract_by_gift(state,a,b):
    if state.like[b][a] >= goal.like[b][a]: 
	global last
	last = state
        return []
    if state.own[a]['ring'] == False:
        return [('get_ring',a),('attract',a,b)]
    if state.loc[a] == state.loc[b]:
        return [('give',a,b,'ring'),('attract',a,b)]
    else:
        return [('goto',a,state.loc[b]),('give',a,b,'ring'),('attract',a,b)]

pyhop.declare_methods('attract',attract_by_talk,attract_by_gift)


def upset_by_yelling(state,a,b):
    if state.upset[b] >= goal.upset[b]: 
	global last
	last = state
        return []
    if state.upset[b] >= 50:
        return False
    if state.loc[a] == state.loc[b]:
        return [('yell',a,b),('upset',a,b)]
    else:
        return [('goto',a,state.loc[b]),('upset',a,b)]

def upset_by_stealing(state,a,b):
    if state.upset[b] >= goal.upset[b]: 
	global last
	last = state
        return []
    if state.own[b]['ring'] == False:
        return [('upset',a,b)]
    if state.loc[a] == state.loc[b]:
        return [('steal_ring',a,b),('upset',a,b)]
    else:
        return [('goto',a,state.loc[b]),('upset',a,b)]

pyhop.declare_methods('upset',upset_by_yelling,upset_by_stealing)
print('')
pyhop.print_methods()


def make_calm_by_appology(state,a,b):
    if state.upset[b] <= goal.upset[b]:
        return []
    if state.upset[b] <= 50:
        return False
    if at_same_place(state,a,b):
        return [('appology',a,b),('make_calm',a,b)]
    else: 
        return [('goto',a,state.loc[b]),('make_calm',a,b)]

def make_calm_by_return_ring(state,a,b):
    if state.upset[b] <= goal.upset[b]:
        return []
    if at_same_place(state,a,b):
        return [('return_ring',a,b),('make_calm',a,b)]
    else:
        return [('goto',a,state.loc[b]),('make_calm',a,b)]

pyhop.declare_methods('make_calm',make_calm_by_appology,make_calm_by_return_ring)
print('')
pyhop.print_methods()

def make_happy(state,a,b):
    if state.happiness[b] >= goal.happiness[b]:
        return []
    if at_same_place(state,a,b):
        return [('say_love',a,b),('make_happy',a,b)]
    else:
        return [('goto',a,state.loc[b]),('make_happy',a,b)]

pyhop.declare_methods('make_happy',make_happy)
print('')
pyhop.print_methods()

def happy_ending(state,a):
    if state.upset[a] > goal.upset[a]:
        return [('make_calm','jack',a),('happy_ending',a)]
    if state.happiness[a] < goal.happiness[a]:
        return [('make_happy','marry',a),('happy_ending',a)]
    else: 
        global last
        last = state
        return []

pyhop.declare_methods('happy_ending',happy_ending)
print('')
pyhop.print_methods()


state1 = pyhop.State('state1')
state1.loc = {'me':'park','marry':'home', 'jack':'park'}
state1.ring = {'park':1,'home':1}
state1.own = {'me':{'ring':False},'marry':{'ring':False}}
state1.like = {'me':{'marry':30}, 'marry':{'me':10}}
state1.happiness = {'me':50, 'marry':50, 'jack':50}
state1.jealous = {'me':0, 'marry':0, 'jack':0}
state1.upset = {'me':0, 'marry':0, 'jack':0}


goal = pyhop.State('goal')
goal.like = {'marry':{'me':120}}

print('Initial State')
pyhop.print_state(state1)

print('')
print('Goal State 1 ========')
pyhop.print_state(goal)

print('')
pyhop.pyhop(state1,[('attract','me','marry')],verbose=1)
print('Final State')
pyhop.print_state(last)

goal.like = {'me':{'marry':120}}
print('')
print('Goal State 2 ========')
pyhop.print_state(goal)

print('')
pyhop.pyhop(last,[('attract','marry','me')],verbose=1)
print('Final State')
pyhop.print_state(last)

goal.upset = {'me':100}
print('')
print('Goal State 3 ========')
pyhop.print_state(goal)

print('')
pyhop.pyhop(last,[('upset','jack','me')],verbose=1)
print('Final State')
pyhop.print_state(last)

goal.happiness = {'me':100}
goal.upset = {'me':0}
print('')
print('Goal State 4 ========')
pyhop.print_state(goal)

print('')
pyhop.pyhop(last,[('happy_ending','me')],verbose=1)
print('Final State')
pyhop.print_state(last)
