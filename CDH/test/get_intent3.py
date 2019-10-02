# Author : Choi Donghyeon

import os

import numpy as np
from gensim.models import FastText
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt

from keras.utils.np_utils import to_categorical

from tokenizer import tokenize

from keras.models import load_model


def get_intent():
    ## 1. 워드 임베딩 모델 불러오기
    word2vec_model = Word2Vec.load('HoingMarryShip\CDH\\fasttext\\model')
    w2c_index = word2vec_model.wv.index2word # fasttext가 적용된 단어 목록들


    # config
    vector_size = 300
    intent_mapping = {'날씨': 0, '맛집': 1, '먼지': 2, '여행지': 3, '관광지': 4}
    encode_length = 15


    # def tokenize(sentence):
    #     stop_word = []
    #     josa = [
    #         '이구나', '이네', '이야', '에', '에서', '의', '할', '수', '있는',
    #         '은', '는', '이', '가', '을', '를', '로서', '로', '으로', '이야', '야', '냐', '니']

    #     tokenizer = Okt()
    #     word_bag = []
    #     pos = tokenizer.pos(sentence)
    #     print("\n[DEBUG4-1]tokenize pos >>", pos)
    #     for word, tag in pos:
    #         if word in stop_word:
    #             continue
    #         elif (tag == 'Josa' and word in josa) or tag == 'Punctuation':
    #             continue
    #         else:
    #             word_bag.append(word)
    #             print("[DEBUG4-2]tokenize word_bag >>", word_bag)
    #     result = ' '.join(word_bag)

    #     return result


    def interface_embed(text):  # 입력(테스트)데이터 임베딩&차원변경
        okt = Okt()
        q_raw = okt.morphs(text)
        print("\n[DEBUG5-1]q_raw (형태소 분석) >>", q_raw)
        q_raw = list(map(lambda x: q_raw[x] if x < len(q_raw) else '#', range(encode_length)))
        print("[DEBUG5-2]pred (q_raw) >>", q_raw)
        q_raw = np.array(list(map(lambda x: word2vec_model[x] if x in w2c_index else np.zeros(vector_size, dtype=float), q_raw)))
        q_raw = q_raw.reshape(1, 15, 300, 1)

        return q_raw


    # 실행
    path = 'HoingMarryShip\\CDH\\model\\test\\'
    file_list = os.listdir(path)
    new_num = 0
    if os.path.exists(path):    # 파일 있을경우
        for i in file_list:
            num = int(i.split(".")[0].split("-")[-1])

            if new_num < num:
                new_num = num

    print("\nUSE MODEL >> intent_model-"+str(new_num)+".h5", end="\n")

    while True:
        print('User : ', end='')
        speech = tokenize(input())
        print('\ntokenize : ',speech, end="\n\n")
        speech = interface_embed(speech)


        # 결과
        model = load_model('HoingMarryShip\CDH\\model\\test\\intent_model-'+str(new_num)+'.h5')
        intent = model.predict(speech)
        print("\n[DEBUG6-1]y_intent(predict) >>\n", intent, end="\n")  # 각 카테고리 백터값
        index = np.argmax(intent)
        print("\n")

        for result, num in intent_mapping.items():
            if index == num:
                print(str(intent_mapping))
                print("\nIntent :%s, index :%d"% (result, index), end="\n")
                print("____________________________________________________________________________________________________________________________", end="\n")    
                break
        

################################### start ###################################

if __name__ == '__main__':
    # main()
    get_intent()