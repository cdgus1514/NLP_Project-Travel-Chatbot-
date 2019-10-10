from cdh_intent import get_intent
from jbh_entity import get_entity

from cdh_scenario import dust
from cdh_scenario import weather
from cdh_scenario import restaurant

from tokenizer import tokenize
from configs import IntentConfigs
from model_configs import ModelConfigs

from gensim.models.word2vec import Word2Vec


# CONFIG
config = IntentConfigs()
print("###### application.py ######")

def run():
    print("###### Chatbot Run ######", end="\n\n")

    while True:
        # print('User : ', end='')
        print('\n\nInput Questuon', end='\n')
        speech = preprcoess(input())
        print("\n\nPreprocessed >> " + speech, sep="", end="\n\n")
        
        intent = get_intent(speech)
        print("Intent >> " + intent, sep="", end="\n\n")

        check_intent(intent, speech)


        if intent == "맛집":
            a = ['강남역', '근처', '분위기', '좋은', '카페', '추천해줘'], ['LOCATION', 'O', 'LOCATION', 'O', 'LOCATION', 'O']
            entity = tuple(a)
        
        elif intent == "날씨":
            b = ['오늘', '서초구', '날씨', '어떠니'], ['DATE', 'LOCATION', 'O', 'O']
            entity = tuple(b)

        elif intent == "먼지":
            c = ['오늘', '인천', '미세먼지', '알려줘'], ['DATE', 'LOCATION', 'O', 'O']
            entity = tuple(c)


        # entity = get_entity(intent, speech)
        # print("Entity >> " + str(entity), sep="", end="\n\n")

        # answer = get_scenario(intent, entity)
        # print("A.I >> " + answer, sep="", end="\n\n")



def preprcoess(speech):
    speech = tokenize(speech)

    return speech



def check_intent(intent, speech):
    if intent == "날씨" or intent == "먼지":
        pass
        # return get_entity(speech, False)
    
    elif intent == "맛집":
        pass
        # return get_entity(speech, False)

    elif intent == "여행지":
        pass
        # return get_entity(speech, False)

    elif intent == "관광지":
        pass
        # return get_entity(speech, False)
    
    else:
        print("죄송해요, 그 기능은 아직 준비 중이에요.  :(")
        pass
        # return "죄송해요, 그 기능은 아직 준비 중이에요.  :("



def get_scenario(intent, entity):

    print("[DEBUG1-1]scenario (inetnt) >>", intent, end="\n")
    print("[DEBUG1-1]scenario (intent type) >>", type(intent), end="\n\n")

    if intent == "먼지":
        return dust(entity)

    elif intent == "날씨":
        return weather(entity)

    elif intent == "여행지":
        # return travel(entity)
        pass

    elif intent == "관광지":
        # return attraction(entity)
        pass

    elif intent == "맛집":
        return restaurant(entity)

    else:
        return "죄송해요, 그 기능은 아직 준비 중이에요.  :("
    


run()