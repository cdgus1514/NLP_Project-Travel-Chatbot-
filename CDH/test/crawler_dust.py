import urllib
from urllib.request import urlopen, Request

import bs4

from crawler_configs import Crawlerconfigs



# CONFIGS
config = Crawlerconfigs()
metropolitans = config.metropolitans    # 도시정보
governments = config.Governments        # 행정구역 정보

state = None
slot_data = None

# today_dust 정상

# tomorrow/after_tomorrow 비정상
# metropolitans, governments에 들어있는 도시/행정구역만 metropolitans 메소드로 크롤링 가능
# xx동 크롤링 가능
# 외 크롤링 안됨 (네이버 검색결과가 다른 폼으로 출력)



def today_dust(location):
    global state, slot_data

    try:
        enc_location = urllib.parse.quote(location + ' 오늘 날씨')
        url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location
        print("[DEBUG1-1]today_dust (url) >>\n", url, end="\n\n")
        
        locations = location.split(' ')
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')

        dust_figure = soup.find('dl', class_='indicator')
        dust_figure = dust_figure.text.replace('㎍/㎥', '마이크로그램퍼미터 ').replace('ppm', '피피엠 ').split()
        del dust_figure[0]
        del dust_figure[2]
        del dust_figure[4]
        print("\n[DEBUG1-2]today_dust (dust_figure[5]) >>", dust_figure[5])
        print("\n[DEBUG1-2]today_dust (dust_figure[5]) >>", dust_figure[4], end="\n\n")

        dust = '오늘 ' + location + '지역 미세먼지 정보를 알려드릴게요!\n\n' + '오늘 ' + location + '지역의 미세먼지 상태는 ' + dust_figure[
            1] + ' 이고, 농도는 ' + dust_figure[0] + '\n\n초미세먼지 상태는 ' + dust_figure[3] + ' 이고, 농도는' + dust_figure[
                2] + '\n\n오존 상태는 ' + dust_figure[5] + ' 이고, 농도는 ' + dust_figure[4] + '입니다!'

        if '나쁨' in dust:
            dust += '공기 상태가 안좋으니 마스크를 꼭 착용하세요!  :<'

    
    except:
        print("############################")
        print("#   DUST CRAWLER ERROR     #")
        print("############################")

        dust = "죄송해요, 지금은 " + location + " 미세먼지 정보를 확인 할 수 없어요." + "\n\n" + "지역의 이름을 알려주시면 다시 알려드릴게요."

    # print("\n\n[DEBUG3-1]today_dust (msg) >>\n", dust)
    return dust, state, slot_data, None



def metropolitan(day, location):
    try:
        dust = day + ' ' + location + '의 미세먼지 정보를 알려드릴게요!'
        enc_location = urllib.parse.quote(location + ' ' + day + ' 미세먼지')
        url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location
        print("[DEBUG1-1]metropolitan (url) >>\n", url, end="\n\n\n")

        req = Request(url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        # print("[DEBUG1-2]metropolitan (soup) >>\n", soup, end="\n\n")

        dust_soup = soup.find_all('dl')
        dust_morn = dust_soup[6].text.split()[1]
        print("[DEBUG1-2]metropolitan (parsing_dust_morn) >>", dust_morn, end="\n")
        dust_noon = dust_soup[7].text.split()[1]
        print("[DEBUG1-2]metropolitan (parsing_dust_noon) >>", dust_noon, end="\n")

        dust += '\n\n' + day + ' 오전 미세먼지 상태는 ' + dust_morn + ', 오후 상태는 ' + dust_noon
        
        
        enc_location = urllib.parse.quote(location + '+ ' + day + ' 초미세먼지')
        url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        dust_soup = soup.find_all('dl')
        dust_morn = dust_soup[6].text.split()[1]
        dust_noon = dust_soup[7].text.split()[1]
        dust += '\n\n' + day + ' 오전 초미세먼지 상태는 ' + dust_morn + ', 오후 상태는 ' + dust_noon


        enc_location = urllib.parse.quote(location + '+ ' + day + ' 오존')
        url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        dust_soup = soup.find_all('dl')
        ozone_morn = dust_soup[6].text.split()[1]
        ozone_noon = dust_soup[7].text.split()[1]
        dust += '\n\n' + day + ' 오전 오존 상태는 ' + ozone_morn + ', 오후 상태는 ' + ozone_noon + '입니다'

        if '나쁨' in dust:
            dust += '\n\n공기 상태가 나쁘니 마스크를 꼭 착용하세요!  :<'
    
    except:
        print("############################")
        print("#   DUST CRAWLER ERROR     #")
        print("############################")

        dust = "죄송해요, 지금은 " + location + " 미세먼지 정보를 확인 할 수 없어요." + "\n\n" + "지역의 이름을 알려주시면 다시 알려드릴게요."

    # print("\n\n[DEBUG3-2]metropolitan (msg) >>\n", dust)
    return dust



def tomorrow_dust(location):
    print("\n[DEBUG1-1]tomorrow_dust (location) >>", location, end="\n\n")

    try:
        if len(location.split()) == 1 and location in metropolitans:
            tdust = metropolitan('내일', location)
        elif len(location.split()) == 1 and location in governments:
            tdust = metropolitan('내일', location)
        else:
            enc_location = urllib.parse.quote(location + ' 내일 미세먼지')
            url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location
            print("[DEBUG1-1]tomorrow_dust (url) >>\n", url, end="\n\n\n")

            req = Request(url)
            page = urlopen(req)
            html = page.read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            # print("[DEBUG1-2]tomorrow_dust (soup) >>\n", soup, end="\n\n")

            dust_figure = soup.find_all('tbody')[2].text.split()
            dust_figure.remove('미세먼지')
            dust_figure.remove('초미세먼지')
            dust_figure.remove('오존')
            dust_figure.remove('자외선')
            dust_figure.remove('황사')

            tdust = '내일 ' + location + '의 미세먼지 정보를 알려드릴게요!\n\n'
            dust_morn = dust_figure[0]
            print("[DEBUG1-2]tomorrow_dust (dust_morn) >>", dust_morn, end="\n")
            dust_noon = dust_figure[1]
            print("[DEBUG1-2]tomorrow_dust (dust_norn) >>", dust_noon, end="\n")

            tdust += '내일 오전 미세먼지 상태는 ' + dust_morn + ', 오후 상태는 ' + dust_noon + '\n\n'
            supdust_morn = dust_figure[4]
            supdust_noon = dust_figure[5]
            tdust += '내일 오전 초미세먼지 상태는 ' + supdust_morn + ', 오후 상태는 ' + supdust_noon +'\n\n'
            ozone_morn = dust_figure[8]
            ozone_noon = dust_figure[9]
            tdust += '내일 오전 오존 상태는 ' + ozone_morn + ', 오후 상태는 ' + ozone_noon + '입니다'

            if '나쁨' in tdust:
                tdust += '\n\n공기 상태가 나쁘니 마스크를 꼭 착용하세요!  :<'
    except:
        print("############################")
        print("#   DUST CRAWLER ERROR     #")
        print("############################")

        tdust = "죄송해요, 지금은 " + location + " 미세먼지 정보를 확인 할 수 없어요." + "\n\n" + "지역의 이름을 알려주시면 다시 알려드릴게요."

    # print("\n\n[DEBUG3-3]tomorrow_dust (msg) >>\n", tdust)
    return tdust, state, slot_data, None



def after_tomorrow_dust(location):
    try:
        if len(location.split()) == 1 and location in metropolitans:
            dust = metropolitan('내일', location)
        elif len(location.split()) == 1 and location in governments:
            dust = metropolitan('내일', location)
        else:
            enc_location = urllib.parse.quote(location + ' 내일 미세먼지')
            url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location
            print("[DEBUG1-1]after_tomorrow_dust (url) >>\n", url, end="\n\n")

            req = Request(url)
            page = urlopen(req)
            html = page.read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            dust_figure = soup.find_all('tbody')[2].text.split()
            dust_figure.remove('미세먼지')
            dust_figure.remove('초미세먼지')
            dust_figure.remove('오존')
            dust_figure.remove('자외선')
            dust_figure.remove('황사')

            dust = '모레 ' + location + '의 미세먼지 정보를 알려드릴게요!\n\n'
            dust_morn = dust_figure[2]
            dust_noon = dust_figure[3]
            dust += '모레 오전 미세먼지 상태는 ' + dust_morn + ', 오후 상태는 ' + dust_noon + '\n\n'
            supdust_morn = dust_figure[6]
            supdust_noon = dust_figure[7]
            dust += '모레 오전 초미세먼지 상태는 ' + supdust_morn + ', 오후 상태는 ' + supdust_noon +'\n\n'
            ozone_morn = dust_figure[10]
            ozone_noon = dust_figure[11]
            dust += '모레 오전 오존 상태는 ' + ozone_morn + ', 오후 상태는 ' + ozone_noon + '입니다'

            if '나쁨' in dust:
                dust += '\n\n공기 상태가 나쁘니 마스크를 꼭 착용하세요!  :<'
    except:
        print("############################")
        print("#   DUST CRAWLER ERROR     #")
        print("############################")

        tdust = "죄송해요, 지금은 " + location + " 미세먼지 정보를 확인 할 수 없어요." + "\n\n" + "지역의 이름을 알려주시면 다시 알려드릴게요."


    # print("\n\n[DEBUG3-4]after_tomorrow_dust (msg) >>\n", dust)
    return dust.replace('-', '아직 알수 없음'), state, slot_data, None


# tomorrow_dust("강원도")