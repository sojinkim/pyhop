"""
This file should work correctly in both Python 2.7 and Python 3.2.
download https://bitbucket.org/dananau/pyhop/downloads/
$ python pyhop_test.py
"""
import pyhop
import story_methods as mt
from story_util import * 

print('')
pyhop.print_operators()
pyhop.print_methods()


state1 = pyhop.State('state1')
state1.loc = {'tom':'park', 'marry':'home', 'jack':'home'}
state1.ring = {'park':1, 'home':0}
state1.own = {'tom':{'ring':0, 'gold':0}, 
              'marry':{'ring':0, 'gold':0}, 
              'jack':{'ring':0, 'gold':0}}
state1.stole = {'tom':{'jack':{'ring':0}},  
              'jack':{'tom':{'ring':0}}}
state1.like = {'tom':{'marry':0, 'jack':0}, 
               'marry':{'tom':0, 'jack':50}, 
               'jack':{'marry':50, 'tom':0}}
state1.happiness = {'tom':0, 'marry':0, 'jack':0}
state1.upset = {'tom':0, 'marry':0, 'jack':0}


print('==== Initial State')
pyhop.print_state(state1)
print ''
print presentation(state1)

print('\n==== Goal 1')
goal = pyhop.State('goal')
goal.like = {'marry':{'tom':100}}
pyhop.print_state(goal)

pyhop.pyhop(state1,[('attract','tom','marry',goal)],verbose=1)
print('==== State')
pyhop.print_state(mt.last)
print presentation(mt.last)

print('\n==== Goal 2')
goal = pyhop.State('goal')
goal.like = {'marry':{'jack':100}}
pyhop.print_state(goal)

pyhop.pyhop(mt.last,[('attract','jack','marry',goal)],verbose=1)
print('==== State')
pyhop.print_state(mt.last)
print presentation(mt.last)

print('\n==== Goal 3')
goal = pyhop.State('goal')
prota = pick_protagonist(mt.last)
goal.like = {prota:{'marry':100}}
pyhop.print_state(goal)

pyhop.pyhop(mt.last,[('attract','marry',prota,goal)],verbose=1)
print('==== State')
pyhop.print_state(mt.last)
print presentation(mt.last)

print('\n==== Goal 4')
goal = pyhop.State('goal')
anta = pick_antagonist(mt.last,prota)
goal.upset = {prota:100}
pyhop.print_state(goal)

pyhop.pyhop(mt.last,[('upset',anta,prota,goal)],verbose=1)
print('==== State')
pyhop.print_state(mt.last)
print presentation(mt.last)

print('\n==== Ending')
goal = pyhop.State('goal')
## ending 1
goal.happiness = {prota:100, anta:-100}
pyhop.print_state(goal)
pyhop.pyhop(mt.last,[('happy_ending',prota,goal)],verbose=1)
pyhop.pyhop(mt.last,[('bad_ending',anta,goal)],verbose=1)

## ending 2
#goal.happiness = {prota:-100, anta:100}
#pyhop.print_state(goal)
#pyhop.pyhop(mt.last,[('happy_ending',anta,goal)],verbose=1)
#pyhop.pyhop(mt.last,[('bad_ending',prota,goal)],verbose=1)

## enging 3
#goal.happiness = {'marry':-100}
#pyhop.print_state(goal)
#pyhop.pyhop(mt.last,[('bad_ending','marry',goal)],verbose=1)

print presentation(mt.last)
print ending(mt.last)

print('\n==== Final State')
pyhop.print_state(mt.last)
