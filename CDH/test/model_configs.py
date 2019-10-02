import pandas as pd
from gensim.models.word2vec import Word2Vec
from keras.models import load_model



class ModelConfigs:
    root_path = "CDH/"
    intent_model_path = root_path+"model/intent/"
    entity_model_path = root_path+"model/entity/"
    fasttext_path = root_path+"fasttext/"


    def __init__(self):
        self.word2vec_model = Word2Vec.load(self.fasttext_path+"model")
        self.model = load_model(self.intent_model_path+'intent_model-'+str(4600)+'.h5')