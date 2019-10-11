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
    config = Crawlerconfigs()

    if entity in config.p_beach:
        print("\n[DEBUG1-1]check_purpose (1)", end="\n")
        # 하나투어
        city = config.beach
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity in config.p_mountain:
        print("\n[DEBUG1-1]check_purpose (2)", end="\n")
        # 하나투어
        city = config.mountain
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result
    
    elif entity == "온천" or entity == "스파":
        print("\n[DEBUG1-1]check_purpose (3)", end="\n")
        # 네이버
        city = config.spa
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity == "캠핑":
        print("\n[DEBUG1-1]check_purpose (4)", end="\n")
        # 네이버
        city = config.camping
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity in config.p_Nlandscape:
        print("\n[DEBUG1-1]check_purpose (5)", end="\n")
        # 하나투어
        city = config.Nlandscape
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity == "역사" or entity == "유적지":
        print("\n[DEBUG1-1]check_purpose (6)", end="\n")
        # 하나투어
        city = config.historic
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity == "체험" or entity == "관광":
        print("\n[DEBUG1-1]check_purpose (7)", end="\n")
        # 하나투어
        city = config.sightseeing
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity == "시장":
        print("\n[DEBUG1-1]check_purpose (8)", end="\n")
        # 하나투어
        city = config.market
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity == "놀이동산" or entity == "놀이 공원":
        print("\n[DEBUG1-1]check_purpose (9)", end="\n")
        # 네이버
        city = config.amusement_park
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity in config.p_stadium:
        print("\n[DEBUG1-1]check_purpose (10)", end="\n")
        # 네이버
        city = config.stadium
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity == "거리":
        print("\n[DEBUG1-1]check_purpose (11)", end="\n")
        # 하나투어
        city = config.load
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result
    
    elif entity == "쇼핑" or entity == "백화점":
        print("\n[DEBUG1-1]check_purpose (12)", end="\n")
        # 하나투어
        city = config.shopping
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity in config.p_museum:
        print("\n[DEBUG1-1]check_purpose (13)", end="\n")
        # 네이버
        city = config.city
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity == "테마 파크":
        print("\n[DEBUG1-1]check_purpose (14)", end="\n")
        # 네이버
        city = config.theme_park
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result

    elif entity in config.p_amusement_park:
        print("\n[DEBUG1-1]check_purpose (15)", end="\n")
        # 네이버
        city = config.zoo
        select_city = random.choice(list(city.items()))

        info = config.info
        info_index = info[str(select_city[1])]

        result = [select_city, info_index]
        return result
    
    elif entity in config.p_mountain_leisure:
        print("\n[DEBUG1-1]check_purpose (16)", end="\n")
        # 아직 찾는중
        result = [("",99), ""]
        return result

    else:
        print("\n[DEBUG1-1]check_purpose (99)", end="\n")
        result = [("",99), ""]
        return result


    # return result



def recommand_travelCity(entity):
    
    # 추천도시 선택 >> [('도시','index'), 'info_index']
    purpose = check_purpose(entity) 
    # purpose = [('서울', '35'), '1000056139101']
    # purpose = [('부산', '36'), '1000060452101']
    # purpose = [('전주', '28'), '1000043129101']
    # purpose = [('제주', '7'), '1000043115101']
    # purpose = [('인천', '45'), '1000072355101']
    # purpose = [('강원', '37'), '1000060540101']
    print("\n[DEBUG1-1]recommand_travelCity (purpose) >>", purpose, end="\n\n")


    # 도시정보 크롤링
    if purpose[0][1] == 99:
        # 하나투어 리스트에 없는 도시들
        return '죄송해요, 이 질문에 대한 정보는 아직 준비중이에요  :('
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
        # msg += gj.gyeongju_cr(str(city), info)
        return '죄송해요, 이 질문에 대한 정보는 아직 준비중이에요  :('

    elif purpose[0][0] == "화성":
        # msg += hs.hwaseong_cr(str(city), info)
        return '죄송해요, 이 질문에 대한 정보는 아직 준비중이에요  :('

    elif purpose[0][0] == "부산":
        msg += bs.busan_cr(str(city), info)

    elif purpose[0][0] == "수원":
        # msg += sw.suwon_cr(str(city), info)
        return '죄송해요, 이 질문에 대한 정보는 아직 준비중이에요  :('

    elif purpose[0][0] == "강원":
        msg += gw.gangwon_cr(str(city), info)

    elif purpose[0][0] == "인천":
        msg += inc.incheon_cr(str(city), info)

    elif purpose[0][0] == "강화":
        # msg += gh.ganghwa_cr(str(city), info)
        return '죄송해요, 이 질문에 대한 정보는 아직 준비중이에요  :('

    else:
        return '죄송해요, 이 질문에 대한 정보는 아직 준비중이에요  :('
    

    print("\n\n[DEBUG1-2]recommand_travelCity (msg) >>\n", msg)
    return msg



recommand_travelCity('경기장')