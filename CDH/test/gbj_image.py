from PIL import Image, ImageOps

import keras
import numpy as np
import pandas as pd
import os

import pymysql as py

from keras.preprocessing.image import ImageDataGenerator

from models.ImageModel import Load_Image
from configs import Configs



config = Configs()
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
    conn = py.connect(host="cdgus1514.cafe24.com", user="cdgus1514", password="Chlehd131312", database="cdgus1514")
    cursor = conn.cursor()
    cursor.execute("set names utf8")
    cursor.execute("SELECT * FROM Image_guide;")
    
    out_max = np.argmax(output) # (1, input_size)의 output에서 최고값의 인덱스 추출
    print('인덱스는: ', out_max)

    output_reshape = output.reshape(config.INPUT_SIZE, )

    if output_reshape[out_max] < 0.9:
        print('\n불확실할 수 있는 이미지입니다.')

    a = np.array(range(0, config.INPUT_SIZE))

    rows = cursor.fetchall()
    rows = np.array(rows)

    for i in a:
        if out_max == i:
            attraction = rows[i, 1]
            content = rows[i, 2]
            inquiry = rows[i, 3]
            website = rows[i, 4]
            address = rows[i, 5]
            fee = rows[i, 6]

            msg = "["+attraction+"]" + "\n\n"
            msg += "안내 정보 : " + content +"\n"
            msg += "전화번호 : " + inquiry + "\n"
            msg += "홈페이지 : " + website + "\n"
            msg += "주소 : " + address + "\n"
            msg += "이용료 : " + fee + "\n"
            print("\n\n[DEBUG1-2]idx_filter (msg) >>\n", msg, end="\n")    
            
            return msg