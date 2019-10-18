from PIL import Image, ImageOps

import keras
import numpy as np
import pandas as pd
import os

from keras.preprocessing.image import ImageDataGenerator

# from model_configs import ModelConfigs
from models.ImageModel import Load_Image
from configs import IntentConfigs

config = IntentConfigs()
# mconfig = ModelConfigs()
mconfig = Load_Image()



def get_image(filename):
    global mconfig

    print("\n\n[DEBUG1-1]get_image (filename) >>", filename, end="\n\n\n")
    
    size = (256, 256)
    im = Image.open(filename)
    im = im.convert('RGB')
    im = ImageOps.fit(im, size, Image.ANTIALIAS, 0, (0.5, 0.5))
    im.save(filename)

    with keras.backend.get_session().graph.as_default():
        test_datagen = ImageDataGenerator(rescale=1./255)

        test_generator = test_datagen.flow_from_directory(config.img_path_category, # D:/Chatbot_KerasImage/data_testset_0924/
                                                        shuffle=False,
                                                        target_size=config.TARGET_SIZE,
                                                        batch_size=config.TEST_BATCH_SIZE,
                                                        class_mode='categorical')

        output = mconfig.image_model.predict_generator(test_generator, steps=1)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
        print('Predict output:\n', output)

        msg = idx_filter(output)

        # 가져온 파일을 삭제합니다.
        if os.path.isfile(filename):
            os.remove(filename)

        return msg, None, None, None




def idx_filter(output):

    out_max = np.argmax(output, axis=1) # (1, input_size)의 output에서 최고값의 인덱스 추출
    print('인덱스는: ', out_max)

    output_reshape = output.reshape(config.INPUT_SIZE, )

    if output_reshape[out_max] < 0.9:
        print('\n불확실할 수 있는 이미지입니다.')


    df = pd.read_csv(config.root_path+'test/data/image_guide.csv', sep=',', encoding='utf-8')
    df = np.array(df)

    a = np.array(range(0, config.INPUT_SIZE))
    
    msg = ""
    for i in a:
        if out_max == [i]:
            # print(df[i,0])
            # print(df[i,1])
            # print(df[i,2])
            # print(df[i,3])
            # print(df[i,4])
            msg += str(df[i, 0]) + '입니다.' + str(df[i, 1]) + '\n'
            msg += '문의 번호는' + str(df[i, 2]) + '이고 홈페이지는' + str(df[i, 3]) + '입니다.' + "\n"
            msg += '주소는' + str(df[i, 4]) + '이고 입장료는' + str(df[i, -1]) + '입니다.'
    
    print("\n\n[DEBUG1-2]idx_filter (msg) >>\n", msg, end="\n")
    print("\n\n[DEBUG1-2]idx_filter (msg type) >>\n", type(msg), end="\n\n\n")
    return msg