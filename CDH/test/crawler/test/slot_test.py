state = None


def scenario(intent, entity):
    if intent == "먼지":
        state = "dust"
        return dust(entity, slot=None), test(state)




def dust(name_entity, slot):

    return name_entity, slot


def test(state):
    
    return state

# scenario('먼지', '바보')



# dust('바보', '멍청이')