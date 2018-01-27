import pyhop

def at_same_place(state,a,b):
    return state.loc[a] == state.loc[b]

def search_for_ring(state):
    for k in state.ring:
        if state.ring[k] > 0: return k
    return None


def get_max_key(d1):
    max_key = max(d1.iterkeys(), key=(lambda k: d1[k]))
    if d1[max_key] >= 0: return max_key
    else: return None

def get_min_key(d1):
    min_key = min(d1.iterkeys(), key=(lambda k: d1[k]))
    if d1[min_key] <= 0: return min_key
    else: return None 

def most_dislike(state,a):
    return get_min_key(state.like[a])

def most_like(state,a):
    return get_max_key(state.like[a])

def most_upset(state):
    return get_max_key(state.upset)

def most_happy(state):
    return get_max_key(state.happiness)

def most_unhappy(state):
    return get_min_key(state.happiness)


# marry picks protagonist
def pick_protagonist(state):
    return most_like(state,'marry')

def pick_antagonist(state,prota):
    members = list(state.like.keys())
    members.remove('marry')
    members.remove(prota)
    return members[0]
  
       
def presentation(state):
    actions = []

    members = list(state.like.keys())
    one = most_like(state,'marry')

    actors = list(members)
    actors.remove('marry')
    actors.remove(one)
    other = None    
    like_marry = 50
    for x in actors:
        if state.like[x]['marry'] >= like_marry:
            like_marry = state.like[x]['marry']
            other = x
        
    if at_same_place(state,'marry',one) and state.upset['marry'] == 0 and state.upset[one] == 0:
        if state.like['marry'][one] >= 100 and state.like[one]['marry'] >= 100:
            actions.append(('kiss','marry',one))
            if other: 
                state.happiness[other] -= state.like[other]['marry']/2
                state.upset[other] += state.like[other]['marry']/2

        if state.like['marry'][one] >= 50 and state.like[one]['marry'] >= 50:
            actions.append(('hangout','marry',one))

    for x in members:
        if state.upset[x] >= 100:
            actions.append(('blowup',x))
        elif state.upset[x] >= 50:
            actions.append(('grimace',x))
        elif state.upset[x] == 0 and state.happiness[x] >= 50:
            actions.append(('smile',x))
        elif state.happiness[x] <= -50:
            actions.append(('cry',x))

    return actions


def ending(state):
    actions = []
    members = list(state.like.keys())
    one = most_like(state,'marry')
    unhappy = most_unhappy(state)
    happy = most_happy(state)
    upset = most_upset(state)
    
    if one and state.like['marry'][one] >= 150 and state.like[one]['marry'] >= 150:
        actions.append(('marry','marry',one))
    if unhappy and state.happiness[unhappy] <= -100:
        if state.happiness[unhappy] > -150:
            actions.append(('leave',unhappy))
        elif state.upset[unhappy] < 100:
            actions.append(('suicide',unhappy))
        else:
            actions.append(('kill',unhappy,happy))

    return actions

  
