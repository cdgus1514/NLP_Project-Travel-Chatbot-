# Author : Choi Donghyeon

import os

import numpy as np
from gensim.models import FastText
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt

import keras
from keras.utils.np_utils import to_categorical

from tokenizer import tokenize
from configs import IntentConfigs
from model_configs import ModelConfigs



# CONFIG
config = IntentConfigs()
mconfig = ModelConfigs()



# 입력받은 문자열(테스트 데이터) 임베딩&차원변경
def interface_embed(text):  
    okt = Okt()
    ## 1. 워드 임베딩 모델 불러오기
    word2vec_model = mconfig.word2vec_model
    w2c_index = word2vec_model.wv.index2word # fasttext가 적용된 단어 목록들

    q_raw = okt.morphs(text)
    print("\n[DEBUG5-1]q_raw (형태소 분석) >>", q_raw)
    q_raw = list(map(lambda x: q_raw[x] if x < len(q_raw) else '#', range(config.encode_length)))
    print("[DEBUG5-2]pred (q_raw) >>", q_raw)
    q_raw = np.array(list(map(lambda x: word2vec_model[x] if x in w2c_index else np.zeros(config.vector_size, dtype=float), q_raw)))
    q_raw = q_raw.reshape(1, 15, 300, 1)

    return q_raw
    


# 의도파악
def get_intent(speech):

    # 입력 문자열 Embedding & Predict
    speech = interface_embed(speech)

    model = mconfig.model
    # print("\n[DEBUG6-1]get_intent(speech) >>\n", speech, end="\n")
    # print("\n[DEBUG6-2]get_intent(speech shape) >> ", speech.shape, end="\n") # (1, 15, 300, 1)
    
    # intent = model._make_predict_function(speech)
    with keras.backend.get_session().graph.as_default():

        intent = model.predict(speech)
        print("\n[DEBUG6-1]y_intent(predict) >>\n", intent, end="\n")  # 각 카테고리 백터값
        index = np.argmax(intent)
        print("\n")

        for result, num in config.intent_mapping.items():
            if index == num:
                print(str(config.intent_mapping))
                print("\nIntent : %s, index :%d"% (result, index), end="\n")
                print("____________________________________________________________________________________________________________________________", end="\n")

                return result