import pandas as pd



class Configs:
    # welcom message
    welcome_msg = "안녕하세요!  저는 여행관련 정보를 알려주는 병주봇 입니다  😊" + "\n\n" + "여행관련(여행지, 관광지, 맛집, 날씨/미세먼지)에 대한 정보를 제공하고 있어요!" + "\n\n" + "무엇이든 물어보세요!!"



    # path
    root_path = "Travel_Chatbot/"
    img_path = root_path+"img_upload/input/"
    img_path_category = root_path+"img_upload/"
    intent_model_path = root_path+"model/intent/"
    entity_model_path = root_path+"model/entity/"
    fasttext_path = root_path+"model/fasttext/"
    seq2seq_path = root_path+"model/seq2seq/"



    # Intent config
    encode_length = 15
    intent_vector_size = 300
    fallback_msg = "죄송해요, 그 기능은 아직 준비중이에요.  :("
    intent_mapping = {'날씨': 0, '맛집': 1, '먼지': 2, '여행지': 3, '관광지': 4}



    # Entity config
    entity_input_size = 20
    entity_vector_size = 300
        


    # Image config
    TARGET_SIZE = (256, 256)
    TEST_BATCH_SIZE = 5
    INPUT_SIZE = 27   # 클래스 개수
    

    


    def __init__(self):
        self.df = pd.read_csv(self.root_path+"src/data/train_intent6.csv")