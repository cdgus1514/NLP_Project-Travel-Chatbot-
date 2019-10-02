import pandas as pd




class IntentConfigs:
    encode_length = 15
    vector_size = 300
    intent_mapping = {'날씨': 0, '맛집': 1, '먼지': 2, '여행지': 3, '관광지': 4}

    root_path = "CDH/"


    def __init__(self):
        self.df = pd.read_csv(self.root_path+"test/data/train_intent5.csv")