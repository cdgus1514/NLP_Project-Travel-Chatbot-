# Author : Choi Donghyeon

import os

import pandas as pd
import numpy as np
from gensim.models import FastText
from konlpy.tag import Okt

from tokenizer import tokenize
from preprocess import preprocess_data


from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, LSTM, BatchNormalization, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.callbacks import EarlyStopping

from configs import IntentConfigs



def main():
    ## 1. intent 데이터셋 불러오기
    config = IntentConfigs()
    okt = Okt()

    question = preprocess_data(True)
    joinStr = ' '.join(question)

    morphs = okt.morphs(joinStr)
    joinString = ' '.join(morphs)
    pos1 = okt.pos(joinString)
    pos2 = ' '.join(list(map(lambda x: '\n' if x[1] in ['Punctuation'] else x[0], pos1))).split('\n')
    morphs = list(map(lambda x: okt.morphs(x), pos2))


    ## 2. 워드 임베딩
    print("\n### Fasttext bulid model ###", end="\n")
    word2vec_model = FastText(size = config.vector_size, window=3, workers=8, min_count= 1)
    word2vec_model.build_vocab(morphs)
    print('\n### Fasttext build complete ###', end="\n")

    print('\n### Fasttext trian start ###', end="\n")
    word2vec_model.train(morphs, total_examples= word2vec_model.corpus_count, epochs= word2vec_model.epochs, compute_loss=True, verbose=1)
    print('\n### Fasttext train complete ###', end="\n")

    word2vec_model.save(config.fasttext_path+"model")
    print('\n### Fasttext model save ###', end="\n")
    
    w2c_index = word2vec_model.wv.index2word # fasttext가 적용된 단어 목록들
    print("_________________________________________________________________________________________________________________\n")



    # y_data 생성
    y_data = config.df['intent']
    y_data = y_data.map(config.intent_mapping)
    y_data = to_categorical(y_data)

    
    # x_data 생성
    encode_length = 15
    x_data = []
    for q_raw in question:
        q_raw = okt.morphs(q_raw) # 문장 형태소별로 분리(단어 분리). str > list
        q_raw = list(map(lambda x: q_raw[x] if x < len(q_raw) else '#', range(encode_length)))
        q_raw = list(map(lambda x: word2vec_model[x] if x in w2c_index else np.zeros(config.vector_size, dtype=float), q_raw))
        q_raw = np.array(q_raw)
        x_data.append(q_raw)
        
    x_data = np.array(x_data)   # (None, 15, 300)
    x_data = x_data.reshape(len(config.df), 15, 300, 1)
    print("_________________________________________________________________________________________________________________\n")



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
    # model.add(Dropout(1.0))
    model.add(Dense(128, activation="relu"))
    # model.add(Dropout(0.1))
    model.add(Dense(5, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # stop = EarlyStopping(monitor="loss", patience=15, mode="auto")


    model.summary()
    
    # model.fit(x_data, y_data, batch_size=16, epochs=500, callbacks=[stop])
    model.fit(x_data, y_data, batch_size=64, epochs=500)

    print("_________________________________________________________________________________________________________________")
    loss, acc = model.evaluate(x_data, y_data)
    print("loss >> ", loss)
    print("acc >>", acc, end="\n")



    ## 4. 모델 저장
    path = config.intent_model_path
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


if __name__ == "__main__":
    main()