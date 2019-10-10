import random
import re
import urllib
from urllib.request import urlopen, Request

import bs4

from crawler_configs import Crawlerconfigs
import crawler.seoul_crawler as se
import crawler.busan_crawler as bs
import crawler.jeonju_crawler as jj
import crawler.jeju_crawler as jji
import crawler.incheon_crawler as inc
import crawler.gangwon_crawler as gw
import crawler.gyeongju_crawler as gj
import crawler.hwaseong_crawler as hs
import crawler.suwon_crawler as sw
import crawler.ganghwa_crawler as gh

import crawler.parsing_test



def check_purpose(entity):
    print("\n\n[DEBUG1-1]check_purpose (entity) >>", entity)
    # 제주[1]:7, 전주[2]:28, 경주[3]:29, 수원[4]:30, 화성[5]:31, 부산[6]:35, 서울[7]:36, 강원[8]:37, 인천[9]:45, 강화[10]:51
    config = Crawlerconfigs()

    if entity == "바다" or "깨끗한 바다" or "해수욕장" or "수영" or "서핑":
        # 하나투어
        city = config.beach
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "산" or "등산" or "단풍" or "단풍 놀이" or "절" or "사찰":
        # 하나투어
        city = config.mountain
        select_city = random.choice(list(city.tiems()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
    
    elif entity == "온천" or "스파":
        # 네이버
        city = config.spa
        select_city = random.choice(list(city.tiems()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "캠핑":
        # 네이버
        city = config.camping
        select_city = random.choice(list(city.tiems()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "자연 경관" or "섬":
        # 하나투어
        city = config.Nlandscape
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "역사" or "유적지":
        # 하나투어
        city = config.historic
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "체험" or "관광":
        # 하나투어
        city = config.sightseeing
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "시장":
        # 하나투어
        city = config.market
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "놀이동산" or "놀이 공원":
        # 네이버
        city = config.amusement_park
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "경기장" or "축구장" or "야구장":
        # 네이버
        city = config.stadium
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "거리":
        # 하나투어
        city = config.load
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
    
    elif entity == "쇼핑" or "백화점":
        # 하나투어
        city = config.shopping
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "수목원" or "박물관" or "미술관":
        # 네이버
        city = config.city
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "테마 파크":
        # 네이버
        city = config.theme_park
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]

    elif entity == "동물원":
        # 네이버
        city = config.zoo
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]


    return result



def recommand_travelCity(entity):

    purpose = check_purpose(entity) # 추천도시 선택 >> [('도시','index'), 'info_index']
    # purpose = [('서울', '35'), '1000056139101']
    # purpose = [('부산', '36'), '1000060452101']
    # purpose = [('전주', '28'), '1000043129101']
    # purpose = [('제주', '7'), '1000043115101']
    # purpose = [('인천', '45'), '1000072355101']
    # purpose = [('강원', '37'), '1000060540101']


    # 도시정보 크롤링
    if purpose[0][1] == 99:
        # 하나투어 리스트에 없는 도시들
        pass
    else:
        city = purpose[0][1]    # 도시 인덱스
        info = purpose[1]       # 도시 정보 인덱스
    
    msg = entity +"(으)로 유명한~!  " + purpose[0][0] +"에 가보는 건 어떠세요?  " + "제가 " + purpose[0][0]+ "에 대해 알려드릴게요!!  :)\n\n\n"
    
    if purpose[0][0] == "서울":
        msg += se.seoul_cr(str(city), info)
    
    elif purpose[0][0] == "제주":
        msg += jji.jeju_cr(str(city), info)

    elif purpose[0][0] == "전주":
        msg += jj.jeonju_cr(str(city), info)

    elif purpose[0][0] == "경주":
        msg += gj.gyeongju_cr(str(city), info)

    elif purpose[0][0] == "화성":
        msg += hs.hwaseong_cr(str(city), info)

    elif purpose[0][0] == "부산":
        msg += bs.busan_cr(str(city), info)

    elif purpose[0][0] == "수원":
        msg += sw.suwon_cr(str(city), info)

    elif purpose[0][0] == "강원":
        msg += gw.gangwon_cr(str(city), info)

    elif purpose[0][0] == "인천":
        msg += inc.incheon_cr(str(city), info)

    elif purpose[0][0] == "강화":
        msg += gh.ganghwa_cr(str(city), info)

    else:
        return "그 기능은 아직 준비 중이에요.  :("
    

    print("\n\n[DEBUG1-1]recommand_travelCity (msg) >>\n", msg)
    return msg



# recommand_travelCity('관광')