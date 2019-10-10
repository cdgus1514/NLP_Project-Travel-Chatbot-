import pandas as pd




class IntentConfigs:
    encode_length = 15
    vector_size = 300
    fallback = 0.99999999
    intent_mapping = {'날씨': 0, '맛집': 1, '먼지': 2, '여행지': 3, '관광지': 4}

    root_path = "CDH/"
    intent_model_path = root_path+"model/intent/"
    entity_model_path = root_path+"model/entity/"
    fasttext_path = root_path+"fasttext/"
    


    def __init__(self):
        self.df = pd.read_csv(self.root_path+"test/data/train_intent6.csv")