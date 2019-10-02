# Author : Hyunwoong
# When : 5/6/2019
# Homepage : github.com/gusdnd852
# test/classifier
import os

import numpy as np
import pandas as pd
import tensorflow as tf
from gensim.models import FastText
from konlpy.tag import Okt

# from src.intent.configs import IntentConfigs
# configs = IntentConfigs()
# 파라미터 세팅
# data = configs.data
# encode_length = configs.encode_length
# label_size = configs.label_size
# filter_sizes = configs.filter_sizes
# num_filters = configs.num_filters
# intent_mapping = configs.intent_mapping
# learning_step = configs.learning_step
# learning_rate = configs.learning_rate
# vector_size = configs.vector_size


## modify(cdh)
data = pd.read_csv('HoingMarryShip\JBH\\temp\\data\\train_intent.csv')
encode_length = 15
label_size = 12
filter_sizes = [2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4]
num_filters = len(filter_sizes)
intent_mapping = {'날씨': 0, '뉴스': 1, '달력': 2, '맛집': 3, '먼지': 4, '명언': 5, '번역': 6, '시간': 7, '위키': 8, '음악': 9, '이슈': 10, '인물': 11}
learning_step = 3001
learning_rate = 0.00001
vector_size = 300
fasttext_path = "C:\\Study\\Chatbot\\src\\intent\\fasttext\\"
model_path = "C:\\Study\\Chatbot\\src\\intent\\model\\"
fallback_score = 2




def inference_embed(data):  # 문자열 분할(konlpy) >> vector변환(Fasttext) >> 결과리턴
    mecab = Okt()
    model = FastText.load(fasttext_path + 'model')
    print("\n[Debug1-1]inference_embed (model) >>", model, end="\n")
    encode_raw = mecab.morphs(data)
    encode_raw = list(map(lambda x: encode_raw[x] if x < len(encode_raw) else '#', range(encode_length)))

    print("\n[Debug1-2]inference_embed encode_raw >> ", encode_raw, end="\n")   # (문자열 분할, 최대15개 빈칸은 #처리)
    input = np.array(
        list(map(lambda x: model[x] if x in model.wv.index2word else np.zeros(vector_size, dtype=float), encode_raw)))

    print("\n[Debug1-3]inference_embed (return) >>\n", input)            # (백터화, 나머지는 0처리)
    print("\n[Debug1-3]inference_embed (return shape) >>", input.shape, end="\n")  # (15,300)
    
    return input


def create_graph(train=True):
    x = tf.placeholder("float", shape=[None, encode_length * vector_size], name='x')    # [None, 15*300]
    y_target = tf.placeholder("float", shape=[None, label_size], name='y_target')       # [None, 12]
    x_image = tf.reshape(x, [-1, encode_length, vector_size, 1], name="x_image")        # [-1,15,300,1]
    print("\n[DEBUG6-1]create_graph (x_image) >>", x_image, end="\n")
    l2_loss = tf.constant(0.0)
    pooled_outputs = []
    for i, filter_size in enumerate(filter_sizes):
        with tf.name_scope("conv-maxpool-%s" % filter_size):
            filter_shape = [filter_size, vector_size, 1, num_filters]   # [[2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4], 300, 1, 12]
            print("\n[Debug6-2]create_graph (filter_shape) >>", filter_shape, end="\n") #
            W_conv1 = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
            print("[DEBUG6-3]create_graph (W_conv1) >>", W_conv1, end="\n") # 
            b_conv1 = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")
            print("[DEBUG6-3]create_graph (b_conv1) >>", b_conv1, end="\n") #

            conv = tf.nn.conv2d(x_image, W_conv1, strides=[1, 1, 1, 1], padding="VALID", name="conv")
            h = tf.nn.relu(tf.nn.bias_add(conv, b_conv1), name="relu")
            pooled = tf.nn.max_pool(h, ksize=[1, encode_length - filter_size + 1, 1, 1], strides=[1, 1, 1, 1], padding='VALID', name="pool")
            pooled_outputs.append(pooled)

    num_filters_total = num_filters * len(filter_sizes)
    h_pool = tf.concat(pooled_outputs, 3)
    h_pool_flat = tf.reshape(h_pool, [-1, num_filters_total])
    keep_prob = 1.0
    if train:
        keep_prob = tf.placeholder("float", name="keep_prob")
        h_pool_flat = tf.nn.dropout(h_pool_flat, keep_prob)

    W_fc1 = tf.get_variable(
        "W_fc1",
        shape=[num_filters_total, label_size],
        initializer=tf.contrib.layers.xavier_initializer())
    b_fc1 = tf.Variable(tf.constant(0.1, shape=[label_size]), name="b")
    l2_loss += tf.nn.l2_loss(W_fc1)
    l2_loss += tf.nn.l2_loss(b_fc1)
    y = tf.nn.xw_plus_b(h_pool_flat, W_fc1, b_fc1, name="scores")
    predictions = tf.argmax(y, 1, name="predictions")
    losses = tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_target)
    cross_entropy = tf.reduce_mean(losses)
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
    correct_predictions = tf.equal(predictions, tf.argmax(y_target, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")
    return accuracy, x, y_target, keep_prob, train_step, y, cross_entropy, W_conv1


def predict(test_data):
    try:
        tf.reset_default_graph()
        sess = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True)))
        _, x, _, _, _, y, _, _ = create_graph(train=False)
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        dir = os.listdir(model_path)
        num_ckpt = 0
        for i in dir:
            try:
                new_one = int(i.split('-')[1].split('.')[0])
                if num_ckpt < new_one:
                    num_ckpt = new_one
            except:
                pass

        saver.restore(sess, model_path + 'check_point-' + str(num_ckpt) + '.ckpt')
        y = sess.run([y], feed_dict={x: np.array([test_data])})
        score = y[0][0][np.argmax(y)]
        if score > fallback_score:
            return format(np.argmax(y))
        else:
            return None
    except Exception as e:
        raise Exception("error on training: {0}".format(e))
    finally:
        sess.close()


def get_intent(text):   # 맞는 카테고리 리턴
    prediction = predict(np.array(inference_embed(text)).flatten())
    # Debug 7
    print("\n[DEBUG7-1]get_intent (prediction) >>", prediction, end="\n")
    if prediction is None:
        
        return "폴백"
    else:
        for mapping, num in intent_mapping.items():
            if int(prediction) == num:
                print("\n[DEBUG7-2]get_intent (mapping) >>", mapping, end="\n\n")

                return mapping



# DEBUG TEST
# print("\n[DEBUG TEST]get_intent\n")
# get_intent("서초구 날씨 알려줘")