# Author : Choi Donghyeon

import os

import pandas as pd
import numpy as np
from gensim.models import FastText
from konlpy.tag import Okt


from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, LSTM, BatchNormalization, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.callbacks import EarlyStopping


def main():
    ## 1. intent 훈련 데이터 불러오기
    # df = pd.read_csv('HoingMarryShip\JBH\\temp\\data\\train_intent.csv')  # 원본(12)
    df = pd.read_csv('HoingMarryShip\CDH\\test\\data\\train_intent4.csv')    # 수정(5)
    # df = pd.read_csv('C:\\Study\\HoingMarryShip\\JBH\\temp\\data\\train_intent.csv')  # CMD
    print(len(df)) # 2120


    vector_size = 300
    okt = Okt()

    question = df['question']       # 질문 문장 데이터
    joinStr = ' '.join(question)    # list -> str 형 변환
    print(joinStr)
    print("joinStr len >>", len(joinStr)) # 2333

    morphs = okt.morphs(joinStr)
    joinString = ' '.join(morphs)
    pos1 = okt.pos(joinString)
    pos2 = ' '.join(list(map(lambda x: '\n' if x[1] in ['Punctuation'] else x[0], pos1))).split('\n')
    morphs = list(map(lambda x: okt.morphs(x), pos2))


    ## 2. 워드 임베딩
    print("\n### Fasttext bulid model ###", end="\n")
    word2vec_model = FastText(size = vector_size, window=3, workers=8, min_count= 1)
    word2vec_model.build_vocab(morphs)
    print('\n### Fasttext build complete ###', end="\n")


    print('\n### Fasttext trian start ###', end="\n")
    word2vec_model.train(morphs, total_examples= word2vec_model.corpus_count, epochs= word2vec_model.epochs, compute_loss=True, verbose=1)
    print('\n### Fasttext train complete ###', end="\n")

    word2vec_model.save('HoingMarryShip\CDH\\fasttext\\model')
    print('\n### Fasttext model save ###', end="\n")
    
    w2c_index = word2vec_model.wv.index2word # fasttext가 적용된 단어 목록들


    # y_data 생성
    intent_mapping = {'날씨': 0, '맛집': 1, '먼지': 2, '여행지': 3, '관광지': 4}
    
    y_data = df['intent']
    y_data = y_data.map(intent_mapping)
    y_data = to_categorical(y_data)

    
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
    print(x_data.shape, len(x_data))
    x_data = x_data.reshape(length, 15, 300, 1)
    print("_________________________________________________________________________________________________________________")


    ## 3. 모델 생성 및 훈련
    print("shape >>", x_data.shape, y_data.shape)   # (None, 15 ,300, 1) / (None, 5) >> (1167, 15, 300, 1) (2120, 5)

    model = Sequential()
    model.add(Conv2D(12, kernel_size=(2,2), input_shape=(15, 300, 1), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(4,4), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    
    model.add(Conv2D(12, kernel_size=(2,2), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(4,4), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))

    model.add(Conv2D(12, kernel_size=(2,2), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu", data_format='channels_first'))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(4,4), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))

    model.add(Flatten())
    model.add(BatchNormalization())
    model.add(Dropout(1.0))
    model.add(Dense(128, activation="relu"))
    # model.add(Dropout(0.1))
    model.add(Dense(5, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    stop = EarlyStopping(monitor="loss", patience=15, mode="auto")


    model.summary()
    
    model.fit(x_data, y_data, batch_size=4, epochs=100, callbacks=[stop])

    print("_________________________________________________________________________________________________________________")
    loss, acc = model.evaluate(x_data, y_data)
    print("loss >> ", loss)
    print("acc >>", acc, end="\n")


    ## 4. 모델 저장
    path = 'HoingMarryShip\\CDH\\model\\test\\'
    file_list = os.listdir(path)

    new_num = 0
    if os.path.exists(path):    # 파일 있을경우
        for i in file_list:
            num = int(i.split(".")[0].split("-")[-1])
            print("num >>", num)

            if new_num <= num:
                new_num = num + 100
                print("new_num >>", new_num)
            else:
                pass

        
        name = "intent_model-"+str(new_num)+".h5"
        print("\n\nFile name >>",name)
        model.save(path+name)
            
    else:
        model.save(path+"intent_model-100.h5")

    print("\n#### MODEL SAVE ####", end='\n')
        
################################### start ###################################

main()