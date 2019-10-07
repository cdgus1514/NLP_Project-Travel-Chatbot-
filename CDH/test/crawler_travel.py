import random
import re
import urllib
from urllib.request import urlopen, Request

import bs4

from crawler_configs import Crawlerconfigs



def check_purpose(entity):
    # 제주[1]:7, 전주[2]:28, 경주[3]:29, 수원[4]:30, 화성[5]:31, 부산[6]:35, 서울[7]:36, 강원[8]:37, 인천[9]:45, 강화[10]:51
    config = Crawlerconfigs()

    if entity == "바다" or "깨끗한 바다" or "해수욕장" or "수영" or "서핑":
        # 하나투어
        city = config.beach
        select_city = random.choice(list(city.items()))[1]

        info = config.info
        info_index = info[str(select_city)]

        result = [select_city, info_index]

    elif entity == "산" or "등산" or "단풍" or "단풍 놀이" or "절" or "사찰":
        # 하나투어
        city = config.mountain
        select_city = random.choice(list(city.tiems()))[1]
    
    elif entity == "온천" or "스파":
        # 네이버
        city = config.spa
        select_city = random.choice(list(city.tiems()))[1]

    elif entity == "캠핑":
        # 네이버
        city = config.camping
        select_city = random.choice(list(city.tiems()))[1]

    elif entity == "자연 경관" or "섬":
        # 하나투어
        city = config.Nlandscape
        select_city = random.choice(list(city.items()))[1]

    elif entity == "역사" or "유적지":
        # 하나투어
        city = config.historic
        select_city = random.choice(list(city.items()))[1]

    elif entity == "체험" or "관광":
        # 하나투어
        city = config.sightseeing
        select_city = random.choice(list(city.items()))[1]

    elif entity == "시장":
        # 하나투어
        city = config.market
        select_city = random.choice(list(city.items()))[1]

    elif entity == "놀이동산" or "놀이 공원":
        # 네이버
        city = config.amusement_park
        select_city = random.choice(list(city.items()))[1]

    elif entity == "경기장" or "축구장" or "야구장":
        # 네이버
        city = config.stadium
        select_city = random.choice(list(city.items()))[1]

    elif entity == "거리":
        # 하나투어
        city = config.load
        select_city = random.choice(list(city.items()))[1]
    
    elif entity == "쇼핑" or "백화점":
        # 하나투어
        city = config.shopping
        select_city = random.choice(list(city.items()))[1]

    elif entity == "수목원" or "박물관" or "미술관":
        # 네이버
        city = config.city
        select_city = random.choice(list(city.items()))[1]

    elif entity == "테마 파크":
        # 네이버
        city = config.theme_park
        select_city = random.choice(list(city.items()))[1]

    elif entity == "동물원":
        # 네이버
        city = config.zoo
        select_city = random.choice(list(city.items()))[1]

    return result



def recommand_travelCity(entity):

    purpose = check_purpose(entity) # 추천도시 선택

    # 도시정보 크롤링
    if purpose[0] == 99:
        pass
    else:
        city = purpose[0]   # 도시 인덱스
        info = purpose[1]   # 도시 정보 인덱스

    url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

