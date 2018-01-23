"""
This file should work correctly in both Python 2.7 and Python 3.2.
download https://bitbucket.org/dananau/pyhop/downloads/
$ python pyhop_test.py
"""
import pyhop
import story_methods as mt

#print('')
#pyhop.print_operators()
#pyhop.print_methods()


state1 = pyhop.State('state1')
state1.loc = {'me':'park', 'marry':'home', 'jack':'park'}
state1.ring = {'park':1, 'home':0}
state1.own = {'me':{'ring':0, 'gold':0}, 
              'marry':{'ring':0, 'gold':0}, 
              'jack':{'ring':0, 'gold':0}}
state1.stole = {'me':{'jack':{'ring':0}},  
              'jack':{'me':{'ring':0}}}
state1.like = {'me':{'marry':0, 'jack':0}, 
               'marry':{'me':0, 'jack':50}, 
               'jack':{'marry':50, 'me':0}}
state1.happiness = {'me':0, 'marry':0, 'jack':0}
state1.upset = {'me':0, 'marry':0, 'jack':0}

print('Initial State')
pyhop.print_state(state1)

print('')
print('Goal 1 ========')
goal = pyhop.State('goal')
goal.like = {'marry':{'me':100}}
pyhop.print_state(goal)

print('')
pyhop.pyhop(state1,[('attract','me','marry',goal)],verbose=1)
print('Final State')
pyhop.print_state(mt.last)

print('')
print('Goal 2 ========')
goal.like = {'marry':{'jack':100}}
pyhop.print_state(goal)

print('')
pyhop.pyhop(mt.last,[('attract','jack','marry',goal)],verbose=1)
print('Final State')
pyhop.print_state(mt.last)

print('')
print('Goal 3 ========')
goal.like = {'me':{'marry':100}}
pyhop.print_state(goal)

print('')
pyhop.pyhop(mt.last,[('attract','marry','me',goal)],verbose=1)
print('Final State')
pyhop.print_state(mt.last)

print('')
print('Goal 4 ========')
goal.upset = {'me':100}
pyhop.print_state(goal)

print('')
pyhop.pyhop(mt.last,[('upset','jack','me',goal)],verbose=1)
print('Final State')
pyhop.print_state(mt.last)

print('')
print('Ending ========')

print('')
#pyhop.pyhop(mt.last,[('happy_ending','me')],verbose=1)
pyhop.pyhop(mt.last,[('happy_ending','jack')],verbose=1)
#pyhop.pyhop(mt.last,[('bad_ending','jack')],verbose=1)
#pyhop.pyhop(mt.last,[('bad_ending','me')],verbose=1)
print('Final State')
pyhop.print_state(mt.last)
