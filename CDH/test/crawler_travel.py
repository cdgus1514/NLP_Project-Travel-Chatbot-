import random
import re
import urllib
from urllib.request import urlopen, Request

import bs4



def check_purpose(entity):
    # 제주[1]:7, 전주[2]:28, 경주[3]:29, 수원[4]:30, 화성[5]:31, 부산[6]:35, 서울[7]:36, 강원[8]:37, 인천[9]:45, 강화[10]:51
    city = {'제주':7, '전주':28, '경주':29, '수원':30, '화성':31, '부산':35, '서울':36, '강원':37, '인천':45, '강화':51}

    if entity == "바다" or "깨끗한 바다" or "해수욕장" or "수영" or "서핑":
        # 바다 리스트 중 하나를 선택해서 전달
        
        pass

    elif entity == "산" or "등산" or "단풍":
        # 산 리스트 중 하나를 선택해서 전달
        pass
    
    elif entity == "온천" or "스파":
        # 온천 or 스파 리스트 중 하나를 선택해서 전달
        pass

    elif entity == "캠핑":
        # 캠핑 리시트 중 하나를 선택해서 전달
        pass

    elif entity == "자연경관":
        pass

    elif entity == "역사":
        pass

    elif entity == "공원" or "박물관" or "미술관":
        pass

    elif entity == "시장":
        pass

    elif entity == "놀이동산" or "놀이공원":
        pass

    return purpose


def recommand_travel(entity):

    purpose = check_purpose(entity)
    enc_purpose = urllib.parse.quote(purpose)