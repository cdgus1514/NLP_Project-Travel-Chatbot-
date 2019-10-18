import pandas as pd
from gensim.models.word2vec import Word2Vec
from keras.models import load_model

from keras.utils import CustomObjectScope
from keras_contrib.layers import CRF    # pip install git+https://www.github.com/keras-team/keras-contrib.git

import numpy as np
import pickle

import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)



class ModelConfigs:
    root_path = "CDH/"
    intent_model_path = root_path+"model/intent/"
    fasttext_path = root_path+"model/fasttext/"
    entity_model_path = root_path+"model/entity/"
    seq2seq_path = root_path+"model/seq2seq/"
    image_model_path = root_path+"model/image/"


    def __init__(self):
        # # 의도파악 모델
        # self.word2vec_model = Word2Vec.load(self.fasttext_path+"model")
        # self.intent_model = load_model(self.intent_model_path+'intent_model-'+str(5400)+'.h5')
        
        # print("######################## Success Intent Model load ########################\n\n\n")


        # # 개체명인식 모델
        # ## 불러오기 Keras+CRF save, load 시 custom_objects 구문 필요
        # ## https://keras.io/getting-started/faq/#handling-custom-layers-or-other-custom-objects-in-saved-models
        # self.crf = CRF(7)
        # with CustomObjectScope({'CRF': self.crf, 'crf_loss': self.crf.loss_function, 'crf_viterbi_accuracy': self.crf.accuracy}):
        #     self.entity_model = load_model(self.entity_model_path+"model.h5")
        #     self.entity_weight = self.entity_model.load_weights(self.entity_model_path+"weight.h5")

        
        # ## 개체명 태그
        # self.entity_data = np.load(self.entity_model_path+"entity_data.npy")
        # self.sentence_data = np.load(self.entity_model_path+"sentence_data.npy")
        # with open(self.entity_model_path+"wordIndex.pickle", "rb") as f:
        #     self.word_index = pickle.load(f)
        # with open(self.entity_model_path+"entityIndex.pickle", "rb") as f:
        #     self.entity_index = pickle.load(f)
        
        # print("######################## Success Entity Model load ########################\n\n\n")



        # # Seq2Seq 모델
        # self.encoder_model = load_model(self.seq2seq_path+"seq2seq_encoded_model_with_weights.h5")
        # self.decoder_model = load_model(self.seq2seq_path+"seq2seq_decoded_model_with_weights.h5")

        # ## Seq2Seq 태크
        # self.seq2words = np.load(self.seq2seq_path+"seq2seq_words.npy")

        # print("######################## Success Seq2Seq Model load ########################\n\n\n")


        # # Image 모델
        # self.image_model = load_model(self.image_model_path+"image-model_700.h5")

        # print("######################## Success Image Model load ########################\n\n\n")