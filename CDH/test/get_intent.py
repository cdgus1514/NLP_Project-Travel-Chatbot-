# Author : Choi Donghyeon

import os

import pandas as pd
import numpy as np
from gensim.models import FastText
from konlpy.tag import Okt

from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, LSTM, BatchNormalization, Dropout, Conv2D, MaxPooling2D, Flatten

from keras.models import load_model


def main():
    # intent 훈련 데이터 불러오기
    # df = pd.read_csv('HoingMarryShip\JBH\\temp\\data\\train_intent.csv')  # 원본(12)
    df = pd.read_csv('HoingMarryShip\CDH\\test\\data\\train_intent.csv')    # 수정(3)
    # df = pd.read_csv('C:\\Study\\HoingMarryShip\\JBH\\temp\\data\\train_intent.csv')  # CMD
    # print(df.shape) # (3918, 2) or (1029, 2)

    vector_size = 300
    okt = Okt()

    question = df['question']       # 질문 문장 데이터
    joinStr = ' '.join(question)    # list -> str 형 변환

    morphs = okt.morphs(joinStr)
    joinString = ' '.join(morphs)
    pos1 = okt.pos(joinString)
    pos2 = ' '.join(list(map(lambda x: '\n' if x[1] in ['Punctuation'] else x[0], pos1))).split('\n')
    morphs = list(map(lambda x: okt.morphs(x), pos2))

    print("\n### Fasttext bulid model ###", end="\n")
    word2vec_model = FastText(size = vector_size, window=3, workers=8, min_count= 1)
    word2vec_model.build_vocab(morphs)
    print('\n### Fasttext build complete ###', end="\n")


    print('\n### Fasttext trian start ###', end="\n")
    word2vec_model.train(morphs, total_examples= word2vec_model.corpus_count, epochs= word2vec_model.epochs, compute_loss=True, verbose=1)
    print('\n### Fasttext train complete ###', end="\n")

    w2c_index = word2vec_model.wv.index2word # fasttext가 적용된 단어 목록들
    # print("\n[DEBUG1-1]w2c_index >>\n", w2c_index, end="\n")


    # y_data 생성
    # intent_mapping = {'날씨': 0, '뉴스': 1, '달력': 2, '맛집': 3, '먼지': 4, '명언': 5, '번역': 6, '시간': 7, '위키': 8, '음악': 9, '이슈': 10, '인물': 11}
    intent_mapping = {'날씨': 0, '맛집': 1, '먼지': 2}
    
    y_data = df['intent']
    y_data = y_data.map(intent_mapping)
    y_data = to_categorical(y_data)
    # y_data[1]    >> [1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.] (3918, 12)
    # y_data[500]  >> [0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.] (3918, 12)
    # y_data[1000] >> [0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0.] (3918, 12)
    # y_data[1500] >> [0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0.] (3918, 12)
    # y_data[2000] >> [0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0.] (3918, 12)
    # y_data[3000] >> [0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0.] (3918, 12)

    
    # x_data 생성
    encode_length = 15
    x_data = []
    for q_raw in question:
        q_raw = okt.morphs(q_raw) # 문장 형태소별로 분리(단어 분리). str > list
        q_raw = list(map(lambda x: q_raw[x] if x < len(q_raw) else '#', range(encode_length)))
        q_raw = list(map(lambda x: word2vec_model[x] if x in w2c_index else np.zeros(vector_size, dtype=float), q_raw))
        q_raw = np.array(q_raw)
        x_data.append(q_raw)
        
    x_data = np.array(x_data)   # (None, 15, 300)
    print(x_data.shape)
    x_data = x_data.reshape(1041, 15, 300, 1)
    print("_________________________________________________________________________________________________________________")


    # model
    # x_data = x_data.reshape(len(x_data), encode_length * vector_size)
    print("shape >>", x_data.shape, y_data.shape)   # (None, 15 ,300, 1) / (None, 12)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(2,2), input_shape=(15, 300, 1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=1))
    model.add(Conv2D(64, kernel_size=(3,3), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=1))
    model.add(Conv2D(64, kernel_size=(4,4), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=1))
    model.add(Flatten())
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    # model.add(Dense(128, activation="relu"))
    # model.add(Dropout(0.1))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.summary()
    
    model.fit(x_data, y_data, batch_size=128, epochs=100)

    print("_________________________________________________________________________________________________________________")
    loss, acc = model.evaluate(x_data, y_data)
    print("loss >> ", loss)
    print("acc >>", acc)

    # 모델 저장
    path = 'HoingMarryShip\\CDH\\model\\test\\'
    file_list = os.listdir(path)

    new_num = 0
    if os.path.exists(path):    # 파일 있을경우
        for i in file_list:
            num = int(i.split(".")[0].split("-")[-1])

        if new_num < num:
            new_num = num + 100

        name = "intent_model-"+str(new_num)+".h5"
        print("File name >>",name)
        model.save(path+name)
            
    else:
        model.save(dir+"intent_model-100.h5")

    print("\n#### MODEL SAVE ####", end='\n')

    
    stop_word = []

    josa = [
        '이구나', '이네', '이야',
        '은', '는', '이', '가', '을', '를',
        '로', '으로', '이야', '야', '냐', '니']

    def tokenize(sentence):
        tokenizer = Okt()
        word_bag = []
        pos = tokenizer.pos(sentence)
        print("\n[DEBUG4-1]tokenize pos >>", pos)
        for word, tag in pos:
            if word in stop_word:
                continue
            elif (tag == 'Josa' and word in josa) or tag == 'Punctuation':
                continue
            else:
                word_bag.append(word)
                print("[DEBUG4-2]tokenize word_bag >>", word_bag)
        result = ' '.join(word_bag)

        return result


    def interface_embed(text):  # 테스트 데이터 임베딩/차원변경
        q_raw = okt.morphs(text)
        print("\n[DEBUG5-1]q_raw (형태소 분석) >>", q_raw)
        q_raw = list(map(lambda x: q_raw[x] if x < len(q_raw) else '#', range(encode_length)))
        print("[DEBUG5-2]pred (q_raw) >>", q_raw)
        q_raw = np.array(list(map(lambda x: word2vec_model[x] if x in w2c_index else np.zeros(vector_size, dtype=float), q_raw)))
        # print("\n[DEBUG5-3]pred (q_raw.shape) >>", q_raw.shape) # (15,300)
        q_raw = q_raw.reshape(1, 15, 300, 1)

        return q_raw


    # 실행
    new_num = 0
    if os.path.exists(path):    # 파일 있을경우
        for i in file_list:
            num = int(i.split(".")[0].split("-")[-1])

            if new_num < num:
                new_num = num
                print(new_num)

    print("\nUSE MODEL >> intent_model-"+str(new_num)+".h5", end="\n")

    while True:
        print('User : ', end='')
        speech = tokenize(input())
        print('\ntokenize : ',speech, end="\n")
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
                print("Intent :%s, index :%d"% (result, index), end="\n")
                print("_________________________________________________________________________________________________________________", end="\n")    
                break
        

################################### start ###################################

main()