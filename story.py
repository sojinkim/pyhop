"""
This file should work correctly in both Python 2.7 and Python 3.2.
download https://bitbucket.org/dananau/pyhop/downloads/
$ python pyhop_test.py
"""
import pyhop
import story_methods as mt

print('')
pyhop.print_operators()
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
pyhop.pyhop(state1,[('attract','me','marry',goal)],verbose=1)
print('Final State')
pyhop.print_state(mt.last)

goal.like = {'me':{'marry':120}}
print('')
print('Goal State 2 ========')
pyhop.print_state(goal)

print('')
pyhop.pyhop(mt.last,[('attract','marry','me',goal)],verbose=1)
print('Final State')
pyhop.print_state(mt.last)

goal.upset = {'me':100}
print('')
print('Goal State 3 ========')
pyhop.print_state(goal)

print('')
pyhop.pyhop(mt.last,[('upset','jack','me',goal)],verbose=1)
print('Final State')
pyhop.print_state(mt.last)

goal.happiness = {'me':100}
goal.upset = {'me':0}
print('')
print('Goal State 4 ========')
pyhop.print_state(goal)

print('')
pyhop.pyhop(mt.last,[('happy_ending','me',goal)],verbose=1)
print('Final State')
pyhop.print_state(mt.last)
