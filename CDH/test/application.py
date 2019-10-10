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

    ## 크롤링 테스트 ##
    # if intent == "맛집":
    #     a = ['강남역', '근처', '분위기', '좋은', '카페', '추천해줘'], ['LOCATION', 'O', 'LOCATION', 'O', 'LOCATION', 'O']
    #     entity = tuple(a)
    
    # elif intent == "날씨":
    #     b = ['오늘', '서초구', '날씨', '어떠니'], ['DATE', 'LOCATION', 'O', 'O']
    #     entity = tuple(b)

    # elif intent == "먼지":
    #     c = ['오늘', '인천', '미세먼지', '알려줘'], ['DATE', 'LOCATION', 'O', 'O']
    #     entity = tuple(c)

    # elif intent == "여행지":
    #     d = ['바다', '유명한', '여행지', '알려주라'], ['PURPOSE', 'O', 'O', 'O']
    #     entity = tuple(d)
    
    entity = get_entity.predict(speech.split(' '))
    print("Entity >> " + str(entity), sep="", end="\n\n")

    answer = scenario(intent, entity)
    
    return intent



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
        return "죄송해요, 그 기능은 아직 준비 중이에요.  :("



# 테스트
# run('바다가 유명한 여행지 알려주라')