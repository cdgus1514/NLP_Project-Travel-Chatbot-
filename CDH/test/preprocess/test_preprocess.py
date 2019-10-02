import os

import numpy as np
import pandas as pd
import tensorflow as tf
from gensim.models import FastText
from konlpy.tag import Okt


intent_mapping = {'날씨': 0, '뉴스': 1, '달력': 2, '맛집': 3, '먼지': 4, '명언': 5, '번역': 6, '시간': 7, '위키': 8, '음악': 9, '이슈': 10, '인물': 11}
data = pd.read_csv('HoingMarryShip\\JBH\\chatbot01\\data\\train_intent.csv')
encode_length = 15
label_size = 12
filter_sizes = [2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4]
num_filters = len(filter_sizes)
learning_step = 3001
learning_rate = 0.00001
vector_size = 300


def preprocess_data(tokenizing):
    data['intent'] = data['intent'].map(intent_mapping)
    print("\n[DEBUG1-1]preprocess_data (data) >>\n", data)
    # print("\n[DEBUG1-1]preprocess_data (data) >>\n", data[3850:])

    if tokenizing:
        count = 0
        for i in data['question']:
            data.replace(i, tokenize(i), regex=True, inplace=True)
            if count % 100 == 0:
                print("CURRENT COLLECT : ", count)
            count += 1

    encode = []
    decode = []
    for q, i in data.values:
        encode.append(q)
        decode.append(i)

    # print("\n[DEBUG1-1]preprocess_data (encode) >>\n", encode, end="\n")
    # print("\n[DEBUG1-1]preprocess_data (decode) >>\n", decode, end="\n")
    # print(type(encode), type(decode), len(encode), len(decode))   (list, list / 3919, 3919)
    return {'encode': encode, 'decode': decode}


############################################## train_vector_model ##############################################
def train_vector_model(datas, train):
    path = "C:\\Study\\HoingMarryShip\\model\\"
    if train:
        mecab = Okt()
        str_buf = datas['encode']   # train_data_list(encode, decode)
        joinString = ' '.join(str_buf)
        pos1 = mecab.pos(joinString)
        # print("\n[DEBUG3-1]train_vector_model (pos1) >>\n", pos1, end="\n") # 품사태깅
        pos2 = ' '.join(list(map(lambda x: '\n' if x[1] in ['Punctuation'] else x[0], pos1))).split('\n')
        # print("\n[DEBUG3-2]train_vector_model (pos2) >>\n", pos2, len(pos2), end="\n")   # 토큰만 하나의 리스트로 정리
        morphs = list(map(lambda x: mecab.morphs(x), pos2))
        # print("\n[DEBUG3-3]train_vector_model (morphs) >>\n", morphs, len(morphs), end="\n")   # 토큰화

        print("BUILD MODEL")
        model = FastText(size=vector_size, window=3, workers=8, min_count=2, iter=1500)
        model.build_vocab(morphs)
        print("BUILD COMPLETE")

        print("TRAIN START")
        model.train(morphs, total_examples=model.corpus_count, epochs=model.epochs, compute_loss=True)

        if not os.path.exists(path):
            os.makedirs(path)

        model.save(path + 'model')
        print("TRAIN COMPLETE")
        return model
    else:
        print("LOAD SAVED MODEL")

        return FastText.load(path + 'model')




############################################## tokenize ##############################################
from konlpy.tag import Okt

stop_word = []

josa = [
    '이구나', '이네', '이야',
    '은', '는', '이', '가', '을', '를',
    '로', '으로', '이야', '야', '냐', '니']


def tokenize(sentence):
    tokenizer = Okt()
    word_bag = []
    pos = tokenizer.pos(sentence)
    for word, tag in pos:
        if word in stop_word:
            continue
        elif (tag == 'Josa' and word in josa) or tag == 'Punctuation':
            continue
        else:
            word_bag.append(word)
    result = ''.join(word_bag)

    return result




############################################## load_csv ##############################################
def load_csv(data_path):
    df_csv_read = pd.DataFrame(data_path)

    return df_csv_read




############################################## get_test_data ##############################################
def get_test_data():
    train_data, train_label = embed(load_csv(train_data_list))
    test_data, test_label = embed(load_csv(train_data_list))
    # print("\n[DEBUG2-1]get_test_data (train_data) >>\n", train_data[0:10], end="\n")
    # print("\n[DEBUG2-2]get_test_data (train_label) >>\n", train_label[0:10], end="\n")
    # print("\n[DEBUG2-3]get_test_data (test_data) >>\n", test_data[0:10], end="\n")
    # print("\n[DEBUG2-4]get_test_data (test_label) >>\n", test_label[0:10], end="\n")

    return train_label, test_label, train_data, test_data




############################################## embed ##############################################
def embed(data):
    mecab = Okt()
    inputs = []
    labels = []
    for encode_raw in data['encode']:
        # print("\n[DEBUG4-1]embed encode_raw >>", encode_raw)
        encode_raw = mecab.morphs(encode_raw)
        # print("\n[DEBUG4-2]embed encode_raw (형태소분할) >>", encode_raw)
        encode_raw = list(map(lambda x: encode_raw[x] if x < len(encode_raw) else '#', range(encode_length)))
        # print("\n[DEBUG4-3]embed encode_raw encode1 >>", encode_raw)
        input = np.array(list(
            map(lambda x: model[x] if x in model.wv.index2word else np.zeros(vector_size, dtype=float),
                encode_raw)))
        inputs.append(input.flatten())
        # print("\n[DEBUG4-4]enbed encode_raw (input) >>", input, end="\n")

    for decode_raw in data['decode']:
        label = np.zeros(label_size, dtype=float)
        # print("\n[DEBUG4-5]enbed decode_raw (label) >>", label)
        np.put(label, decode_raw, 1)
        labels.append(label)
        # print("\n[DEBUG4-6]enbed decode_raw (label) >>", label, end="\n")

    print("\n[DEBUG4-7]embed output (inputs, labels) >>", inputs, labels)
    return inputs, labels



################################### start ###################################
train_data_list = preprocess_data(tokenizing=True)
model = train_vector_model(train_data_list, train=True)

get_test_data()