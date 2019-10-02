import pandas as pd
import numpy as np
import re

from konlpy.tag import Okt

from keras.models import Sequential
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional
from keras_contrib.layers import CRF
from keras.utils import np_utils

# 훈련 데이터 생성
def train_data_load(path):
    sentence = []
    tags = []

    word = []
    tag = []

    with open(path, 'r') as f:
        while True:
            # 한줄씩 읽어오기
            line = f.readline()

            # 빈칸 전까지 읽어서 sentence, tags 리스트에 넣고 word, tag 리스트 초기화(반복)
            # ex) ["다음", "주", "전주", "비", "오려나", ...]
            # ex) ["DATE", "DATE", "LOCATION", "O", "O", ...]
            if line == '\n' and len(word) > 0:
                sentence.append(word)
                tags.append(tag)
                word = []
                tag = []

            elif line != '\n':
                if not line:
                    return sentence, tags # 파싱 후 최종결과 리턴

                line = re.sub('\n','', line)    # 다음 DATE
                line = line.split(' ')          # ["다음", "DATE"]
                word.append(line[0])            # [다음, 주, 전주, 비, 오려나]
                tag.append(line[1])             # ["DATE", "DATE", "LOCATION", "O", "O"]



## 1. 훈련 데이터셋 생성
sentence, tags = train_data_load('HoingMarryShip\JBH\\temp\\data\\train_weather_entity.csv')
# print("[DEBUG3-1] train_data_load (sentence) >>\n", sentence) # (3898, )
# print("[DEBUG3-1] train_data_load (tags) >>", tags) # (3898, )
# print(sentence[0])    # ['다음', '주', '전주', '비', '오려나']
# print(tags[0])        # ['DATE', 'DATE', 'LOCATION', 'O', 'O']



## 2. 단어 빈도수 디렉토리 생성
# 1차원 변경 및 중복제거
sentence_flatten = []   # (16506, )
for i in sentence:
    sentence_flatten.extend(i)

word_list = list(set(sentence_flatten)) # (512, )

tag_list = []   # (16506, )
for i in tags:
    tag_list.extend(i)

tag_list = list(set(tag_list))  # (3, )


#단어의 빈도 수 별 인덱스 매핑 (모두 0으로 설정, 반복 개수만큼 +1)
word_count = {}
for i in word_list:
    word_count[i] = 0

for i in sentence_flatten:
    word_count[i] += 1

# 가장 많이 나온 단어부터 정렬
word_count = sorted(word_count.items(), key = lambda i:i[1], reverse=True)
# print("[DEBUG1-1] word_count (sort) >>\n", word_count)


# 단어와 태그에 인덱스 넘버를 부여.
word_to_index = {'PAD': 0, 'OOV': 1}    # (514)
num = 1
for i, _ in word_count: # 인덱스 2번부터 순서대로 매핑(단어)
    num += 1
    word_to_index[i] = num


tag_to_index = {'PAD': 0}   # (4)
num = 0
for i in tag_list:  # 인덱스 1번부터 순서대로 매핑(태그)
    num += 1
    tag_to_index[i] = num

print(word_to_index, end="\n\n")
print(tag_to_index, end="\n")

## 3. 신경망 모델에 적용할 수 있도록 차원변환
def input_trainData_Create(sentence, index, size = 15):
    # print("[DEBUG2-1] input_trainData_Create (sentence) >>", sentence)  # 각 문장 리스트 (3898, )
    # print("[DEBUG2-2] input_trainData_Create (index) >>\n", index)      # 매핑 디렉토리
    arr = []
    word_num = len(sentence)
    # print("[DEBUG2-3] input_trainData_Create (word_num) >>", word_num)  # 해당 sentence 리스트 개수

    for word in sentence:
        try:
            arr.append(index[word]) # 해당 단어 인덱스를 리스트에 추가
        except KeyError:
            arr.append(1)
    
    for i in range(size-word_num):  # padding 처리
        arr.append(0)

    return arr



# 단어(x) 데이터
x_data = []
for i in sentence:
    s = input_trainData_Create(i, word_to_index)
    x_data.extend(s)

x_data = np.array(x_data)
x_data_len = int(len(x_data)/15)
x_data = x_data.reshape(x_data_len, 15) # (58470, ) >> (3898, 15)


# 태그(y) 데이터
y_data = []
for i in tags:
    s = input_trainData_Create(i, tag_to_index)
    y_data.extend(s)

y_data = np.array(y_data)
# print(y_data[0:14])

y_data_len = int(len(y_data)/15)
y_data = y_data.reshape(y_data_len,15)      # (58470, ) >> (3898, 15)
y_data = np_utils.to_categorical(y_data)    # (3898, 15, 4)


# ## 4. 모델
print("\n[DEBUG1-2] x_data[0] >>", x_data[0])   # {x, x, x, x, x, x, x, x, x, x, x, x, x, x, x}
                                                # 각각의 sentence와 word_to_index와 매핑하여 정수 인코딩된 시퀀스로 저장
print("\n[DEBUG1-3] y_data[0] >>\n", y_data[0]) # {'PAD':0, 'O':1, 'DATE':2, 'LOCATION':3}
                                                # 각각의 tags와 tag_to_index와 매핑하여 정수 인코딩된 시퀀스+원-핫 인코딩 저장

model = Sequential()

# (Embedding(input_dim=514, output_dim=?, 15))
# (Embedding(단어개수(단어집합크기), 임베딩 후 크기, 입력 시퀀스 길이))
model.add(Embedding(len(word_to_index), 20, input_length = 15))                         # output shape(None, 15, 20)
model.add(Bidirectional(LSTM(units=50, return_sequences=True, recurrent_dropout=0.1)))  # output shape(None, 15, 100)
model.add(Bidirectional(LSTM(units=20, return_sequences=True, recurrent_dropout=0.1)))  # output shape(None, 15, 40)
model.add(TimeDistributed(Dense(50, activation="relu")))                                # output shape(None, 15, 50)
crf = CRF(len(tag_to_index))                                                            # output shape(None, 15, 4)
model.add(crf)

model.compile(optimizer="rmsprop", loss=crf.loss_function, metrics=[crf.accuracy])

model.summary()

# model.fit(x_data, y_data, batch_size=32, epochs=5, validation_split=0.1, verbose=1)


# print('───────────────────────────────────────────────────────────────────────────────')
# okt = Okt()
# print('Word:', word_to_index)
# print('tag::', tag_to_index)

# keys = list(tag_to_index.keys())
# tag_num = 0
# while True:

#     q_raw = okt.morphs(input('\n>> Input : '))
#     q = input_trainData_Create(q_raw, word_to_index)
#     q = np.array(q).reshape(1,15)
    
#     print('\nindex : ', q, end="\n")

#     ai = model.predict(q)
#     ai = ai[0]

#     print("\n>> A.i : ", end="")
#     for i in range(len(q_raw)):
#         k = np.argmax(ai[i])
#         print(q_raw[i],',', keys[k], end=' | ')

#     print('')
#     print('───────────────────────────────────────────────────────────────────────────────')



'''
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
embedding_1 (Embedding)      (None, 15, 20)            10280
_________________________________________________________________
bidirectional_1 (Bidirection (None, 15, 100)           28400
_________________________________________________________________
bidirectional_2 (Bidirection (None, 15, 40)            19360
_________________________________________________________________
time_distributed_1 (TimeDist (None, 15, 50)            2050
_________________________________________________________________
crf_1 (CRF)                  (None, 15, 4)             228
=================================================================
Total params: 60,318
Trainable params: 60,318
Non-trainable params: 0
_________________________________________________________________
'''