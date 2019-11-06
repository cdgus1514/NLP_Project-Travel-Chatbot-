import numpy as np
from konlpy.tag import Okt

import keras

from configs import Configs
from models.IntentModel import Load_Intent



# CONFIG
config = Configs()
mconfig = Load_Intent()

cnt = 0

word2vec_model = mconfig.word2vec_model
w2c_index = word2vec_model.wv.index2word # fasttext가 적용된 단어 목록들



# 입력받은 문자열(테스트 데이터) 임베딩&차원변경
def interface_embed(text):  
    global word2vec_model
    global w2c_index

    okt = Okt()
    q_raw = okt.morphs(text)

    q_raw = list(map(lambda word : word2vec_model[word], q_raw))
    q_raw = list(map(lambda idx : q_raw[idx] if idx < len(q_raw) else np.zeros(config.vector_size, dtype=float), range(config.encode_length)))
    q_raw = np.array(q_raw)
    q_raw = q_raw.reshape(1, 15, 300, 1)

    return q_raw
    


# 의도파악
def get_intent(speech):
    
    # fallback 상태 변수
    global cnt

    # 입력 문자열 Embedding & Predict
    speech = interface_embed(speech)
    model = mconfig.intent_model
    
    
    with keras.backend.get_session().graph.as_default():

        intent = model.predict(speech)
        print("\n[DEBUG6-1]get_intent (predict) >>\n", intent, end="\n\n")  # 각 카테고리 백터값 (numpy.ndarray)
        intent_chk = len(intent[0]) # 5

        index = np.argmax(intent)
        print("\n[DEBUG6-3]get_intent (index) >>", index, end="\n\n")
        print("\n[DEBUG6-3]get_intent (predict check) >>", intent[0][index], end="\n\n")

        
        # fallback check
        for i in intent[0]:
            if i == 0:
                cnt += 1
        print("\n[DEBUG6-4]get_intent (after cnt) >>", cnt, end="\n\n\n")
        
        if cnt != 4:
            result = "fallback"
            print(str(config.intent_mapping))
            print("\nIntent : ", result)
            cnt = 0
            print("____________________________________________________________________________________________________________________________", end="\n")

            return result
            
            
        elif cnt == 4:
            for result, num in config.intent_mapping.items():
                if index == num:
                    print(str(config.intent_mapping))
                    print("\nIntent : %s, index : %d"% (result, index), end="\n")
                    cnt = 0
                    print("____________________________________________________________________________________________________________________________", end="\n")

                    return result