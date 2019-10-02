from cdh_intent import get_intent
# from jbh_entity import get_entity

from tokenizer import tokenize
from configs import IntentConfigs
from model_configs import ModelConfigs

from gensim.models.word2vec import Word2Vec


#CONFIG
config = IntentConfigs()
print("###### application.py ######")

def run(pdata):
    print('Input Questuon', end='\n')
    speech = preprcoess(pdata)
    print("\n\nPreprocessed >> " + speech, sep="", end="\n\n")
    
    intent = get_intent(speech)
    print("Intent >> " + intent, sep="", end="\n\n")

    # entity = get_entity(intent, speech)
    # print("Entity >> " + str(entity), sep="", end="\n\n")

    # answer = scenario(intent, entity)
    # print("A.I >> " + answer, sep="", end="\n\n")
    
    return intent



def preprcoess(speech):
    speech = tokenize(speech)

    return speech


# def get_entity(intent, speech):
#     if intent == "날씨" or intent == "먼지":
#         return get_weather_entity(speech, False)
    
#     elif intent == "맛집":
#         return get_restaurant_entity(speech, False)

#     elif intent == "여행지":
#         return get_travel_entity(speech, False)

#     elif intent == "관광지":
#         return get_attraction_entity(speech, False)
    
#     else:
#         return None



def scenario(intent, entity):
    if intent == "먼지":
        return dust(entity)
    
    elif intent == "날씨":
        return weather(entity)

    elif intent == "맛집":
        return restaurant(entity)
    
    elif intent == "여행지":
        return travel(entity)
    
    elif intent == "관광지":
        return attraction(entity)
    
    else:
        return "그 기능은 아직 준비 중이에요.  :("