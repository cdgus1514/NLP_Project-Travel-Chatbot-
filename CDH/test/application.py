from cdh_intent import get_intent
from jbh_entity import get_entity

from cdh_scenario import dust
from cdh_scenario import weather
from cdh_scenario import restaurant
from cdh_scenario import travel
# from cdh_scenario import attraction

from tokenizer import tokenize
from configs import IntentConfigs
from model_configs import ModelConfigs

from gensim.models.word2vec import Word2Vec


#CONFIG
config = IntentConfigs()
get_entity = get_entity()
print("###### application.py ######")

def run(pdata):
    print('\n\nInput Questuon', end='\n')
    speech = preprcoess(pdata)
    print("\n\nPreprocessed >> " + speech, sep="", end="\n\n")
    
    intent = get_intent(speech)
    print("Intent >> " + intent, sep="", end="\n\n")
    
    entity = get_entity.predict(speech.split(' '))
    print("Entity >> " + str(entity), sep="", end="\n\n")

    answer = scenario(intent, entity)
    
    return answer



def preprcoess(speech):
    speech = tokenize(speech)

    return speech



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
        # return attraction(entity)
        return intent
        pass
    
    else:
        # seq2seq
        return config.fallback_msg



# 테스트
# run('바다가 유명한 여행지 알려주라')