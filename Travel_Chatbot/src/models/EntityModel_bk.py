from keras.models import load_model
from keras.utils import CustomObjectScope
from keras_contrib.layers import CRF    # pip install git+https://www.github.com/keras-team/keras-contrib.git

import numpy as np
import pickle



class Load_Entity:
    root_path = "Travel_Chatbot/"
    entity_model_path = root_path+"model/entity/"
    

    def __init__(self):
        # 개체명인식 모델
            ## 불러오기 Keras+CRF save, load 시 custom_objects 구문 필요
            ## https://keras.io/getting-started/faq/#handling-custom-layers-or-other-custom-objects-in-saved-models
            self.crf = CRF(7)
            with CustomObjectScope({'CRF': self.crf, 'crf_loss': self.crf.loss_function, 'crf_viterbi_accuracy': self.crf.accuracy}):
                self.entity_model = load_model(self.entity_model_path+"model.h5")
                self.entity_weight = self.entity_model.load_weights(self.entity_model_path+"weight.h5")

            
            ## 개체명 태그
            self.entity_data = np.load(self.entity_model_path+"entity_data.npy")
            self.sentence_data = np.load(self.entity_model_path+"sentence_data.npy")
            with open(self.entity_model_path+"wordIndex.pickle", "rb") as f:
                self.word_index = pickle.load(f)
            with open(self.entity_model_path+"entityIndex.pickle", "rb") as f:
                self.entity_index = pickle.load(f)
            
            print("######################## Success Entity Model load ########################\n\n\n")