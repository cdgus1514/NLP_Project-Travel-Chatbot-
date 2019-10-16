import numpy as np
import os
import pickle # Dictinary를 저장하는 라이브러리

import keras
from keras.models import Sequential
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional, BatchNormalization
# from keras.utils import CustomObjectScope

from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split

from model_configs import ModelConfigs



class get_entity():

    _path = 'HoingMarryShip\JBH\chatbot02\data\\train\\entity\\' # 데이터 저장 경로

    # 인덱스 번호
    word_index = {}
    entity_index = {}
    config = ModelConfigs()

    # 훈련 데이터
    trainSize = 20
    sentence_data = None
    entity_data = None
    trainModel = None



    def save_Dataset(self, sentence_list, entity_list, folderName = 'ft'):

        if not os.path.exists(self._path + folderName): os.makedirs(self._path + folderName)
        # 풀더가 없을 경우 생성.

        # 단어 인덱스
        sentence_flatten = sum(sentence_list, []) # 배열 차원 펼치기
        morphs = list(set(sentence_flatten)) # 중복 제거

        # 단어의 빈도 수 체크
        word_count = {} # 

        for word in morphs:
            word_count[word] = 0

        for word in sentence_flatten:
            word_count[word] += 1

        # 내림차순 정렬
        word_count = sorted(word_count.items(), key = lambda i:i[1], reverse=True)

        # 단어마다 인덱스 부여
        word_index = {'#': 0, 'OOV': 1} # PAD: 패딩, OOV: 모르는 단어.
        idx = 2
        for word, _ in word_count:
            word_index[word] = idx
            idx += 1
        self.word_index = word_index
        with open(self._path + folderName + '\\wordIndex.pickle', 'wb') as f:
            pickle.dump(self.word_index, f, pickle.HIGHEST_PROTOCOL)
        
        # entity 인덱스
        entity_set = sum(entity_list, []) # 배열 차원 펼치기
        entity_set = list(set(entity_set)) # 중복 제거

        # entity 인덱스 번호 부여
        entity_index = {'#': 0}
        for idx in range(len(entity_set)): entity_index[entity_set[idx]] = idx + 1
        self.entity_index = entity_index
        with open(self._path + folderName + '\\entityIndex.pickle', 'wb') as f:
            pickle.dump(self.entity_index, f, pickle.HIGHEST_PROTOCOL)
        
        # entity 훈련 데이터 생성
        entity_data = []
        for y in entity_list:
            y = self.entity_pred(y)
            entity_data.append(y)
        entity_data = to_categorical(entity_data)
        self.entity_data = entity_data
        np.save(self._path + folderName+ '\\entity_data.npy', self.entity_data)

        # sentence 훈련 데이터 생성
        sentence_data = []
        for x in sentence_list:
            x = self.input_pred(x)
            sentence_data.append(x)
        self.sentence_data = np.array(sentence_data)
        np.save(self._path + folderName+ '\\sentence_data.npy', self.sentence_data)
        print(len(sentence_data), len(entity_data))



    # def load_Dataset(self, folderName = 'ft'):
    #     self.entity_data = np.load(self._path+ folderName+ '\\entity_data.npy')
    #     self.sentence_data = np.load(self._path+ folderName+ '\\sentence_data.npy')
    #     with open(self._path+folderName+'\\wordIndex.pickle', 'rb') as f:
    #         self.word_index = pickle.load(f)
    #     with open(self._path+folderName+'\\entityIndex.pickle', 'rb') as f:
    #         self.entity_index = pickle.load(f)



    # 입력 데이터 수치화및 패딩 추가
    def input_pred(self, raw):

        result = []
        for word in raw:
            try: result.append(self.config.word_index[word])
            except KeyError: result.append(self.config.word_index['OOV'])   
        for i in range(self.trainSize - len(raw)):
            result.append(self.config.word_index['#'])

        print("\n[DEBUG1-1]input_pred (pred) >>", result)

        return result



    def entity_pred(self, raw):
        result = []
        for tag in raw:
            result.append(self.config.entity_index[tag])
        for i in range(self.trainSize - len(raw)):
            result.append(self.config.entity_index['#'])

        return result



    # 신경망 모델
    def train(self, save = False, folderName = 'ft'):
        x_train = self.sentence_data
        y_train = self.entity_data
        print('>> '+folderName+' Entity Model', x_train.shape, y_train.shape)
        print('단어의 수',len(self.word_index))
        print('Tag',self.entity_index)
        crf = config.crf

        if save:
            # 훈련
            model = Sequential()
            model.add(Embedding(len(self.word_index), 100, input_length = self.trainSize))
            model.add(Bidirectional(LSTM(units=32, return_sequences=True))) # recurrent_dropout=0.2
            model.add(BatchNormalization())
            model.add(Bidirectional(LSTM(units=64, return_sequences=True)))
            model.add(BatchNormalization())
            model.add(Bidirectional(LSTM(units=32, return_sequences=True)))
            model.add(BatchNormalization())
            model.add(TimeDistributed(Dense(100, activation="relu"))) # timeDistributed wrapper를 사용하여 3차원 입력을 받을 수 있게 확장해 주어야 한다.
            model.add(crf)
            model.compile(optimizer="rmsprop", loss=crf.loss_function, metrics=[crf.accuracy])
            model.fit(x_train, y_train, batch_size=32, epochs=5)
            
            # 저장
            if not os.path.exists(self._path + folderName): os.makedirs(self._path + folderName)
            model.save(self._path + folderName + '\\model.h5')
            model.save_weights(self._path + folderName + '\\weight.h5')
        else: 
            model = self.config.entity_model

        self.trainModel = model



    # 결과 도출
    def predict(self, tokenize):
        t = self.input_pred(tokenize)
        t = np.array(t).reshape(1, self.trainSize)
        
        with keras.backend.get_session().graph.as_default():
            t = self.config.entity_model.predict(t)
            result = []

            for d in t[0]:
                d = np.argmax(d)
                for tag, idx in self.config.entity_index.items():
                    if d == idx:
                        result.append(tag)
                        break
            
            print("[DEBUG1-2]predict (result) >>", result)  # ['tag', 'tag', ...]
            print("[DEBUG1-3]predict (result) >>", len(result)) # 20
            # result = result[:len(tokenize)-1]
            result = result[:len(tokenize)]
            results = (tokenize, result)
            
            return results