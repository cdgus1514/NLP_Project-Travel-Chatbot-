# -*- coding: utf-8 -*-
import urllib
from urllib.request import urlopen, Request

import bs4

state = None
slot_data = None

def __tone_maker(weather_morning, weather_noon):
    if weather_morning[0] == "흐림":
        weather_morning[0] = '흐리고'
    elif weather_morning[0] == "맑음":
        weather_morning[0] = '맑고'
    elif weather_morning[0] == "구름조금":
        weather_morning[0] = '구름이 조금 끼었고'
    elif weather_morning[0] == "구름많음":
        weather_morning[0] = '구름이 많이 끼었고'
    elif weather_morning[0] == "구름많고 한때 비":
        weather_morning[0] = '구름이 많이 끼고 한때 비가 내릴 수 있으며'
    elif weather_morning[0] == "비":
        weather_morning[0] = '비가 내리고'
    elif weather_morning[0] == "눈":
        weather_morning[0] = '눈이 내리고'
    elif weather_morning[0] == "우박":
        weather_morning[0] = '우박이 떨어지고'
    elif weather_morning[0] == "흐리고 가끔 비":
        weather_morning[0] = '흐리고 가끔 비가 내릴 수 있으며'
    if weather_noon[0] == "흐림":
        weather_noon[0] = '흐리고'
    elif weather_noon[0] == "맑음":
        weather_noon[0] = '맑고'
    elif weather_noon[0] == "구름조금":
        weather_noon[0] = '구름이 조금 끼었고'
    elif weather_noon[0] == "구름많음":
        weather_noon[0] = '구름이 많이 끼었고'
    elif weather_noon[0] == "구름많고 한때 비":
        weather_noon[0] = '구름이 많이 끼고 한때 비가 내릴 수 있으며'
    elif weather_noon[0] == "비":
        weather_noon[0] = '비가 내리고'
    elif weather_noon[0] == "눈":
        weather_noon[0] = '눈이 내리고'
    elif weather_noon[0] == "우박":
        weather_noon[0] = '우박이 떨어지고'
    elif weather_noon[0] == "흐리고 가끔 비":
        weather_noon[0] = '흐리고 가끔 비가 내릴 수 있으며'

    return weather_morning, weather_noon



def today_weather(location):
    global state, slot_data
    print("[DEBUG1-1]today_weather (location) >>", location)
    enc_location = urllib.parse.quote(location + '오늘 날씨')
    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html.parser')

    try:
        temperature = (soup
                       .find('div', class_='info_data')
                       .find('p', class_='info_temperature')
                       .find('span', class_='todaytemp').text) + '도'

        weather = (soup
                   .find('div', class_='info_data')
                   .find('ul', class_='info_list')
                   .find('li')
                   .find('p', class_='cast_txt').text).split(',')

        if weather[0] == '비':
            weather = '오늘은 우산을 챙겨야 할지도 몰라요. ☂ 오늘 ' + location + '에는 ' + '비가 와요. 🌧' + \
                      ' 현재 온도는 ' + temperature + '로' + weather[1].replace('˚', '도')
        elif weather[0] == '맑음':
            weather = '오늘 ' + location + '에는 ' + '해가 떴어요. 아주 맑아요. 🌤' + \
                      ' 현재 온도는 ' + temperature + '로' + weather[1].replace('˚', '도')
        elif weather[0] == '흐림':
            weather = '오늘 ' + location + '에는 ' + '구름이 끼어있을 거에요. 날씨가 꽤나 흐려요. ⛅' + \
                      ' 현재 온도는 ' + temperature + '로' + weather[1].replace('˚', '도')
        elif weather[0] == '구름많고 한때 비':
            weather = '오늘 ' + location + '에는 ' + '구름이 끼어있고 한때 비가 올 수도 있어요. 날씨가 꽤나 흐려요. 🌦' + \
                      ' 현재 온도는 ' + temperature + '로' + weather[1].replace('˚', '도')
        elif weather[0] == '구름많음':
            weather = '오늘 ' + location + '에는 ' + '구름이 많이 많이 끼어있어요. ☁' + \
                      ' 현재 온도는 ' + temperature + '로' + weather[1].replace('˚', '도')
        elif weather[0] == '구름조금':
            weather = '오늘 ' + location + '에는 ' + '구름이 조금 끼어있어요. ⛅' + \
                      ' 현재 온도는 ' + temperature + '로' + weather[1].replace('˚', '도')
        elif weather[0] == '눈':
            weather = '오늘 ' + location + '에는 ' + '눈이 와요. 🌨 추울테니까 옷을 따뜻하게 입고 가요. 🧤🧣' + \
                      ' 현재 온도는 ' + temperature + '로' + weather[1].replace('˚', '도')
        elif weather[0] == '우박':
            weather = '조심하세요! 😲 오늘 ' + location + '에는 ' + '우박이 내려요. ☄' + \
                      ' 현재 온도는 ' + temperature + '로' + weather[1].replace('˚', '도')
        elif weather[0] == '흐리고 가끔 비':
            weather = '오늘은 우산을 챙겨야 할지도 몰라요. ☂ 오늘 ' + location + '에는 ' + '비가 올 수 있고 흐린 날씨에요. 🌧' + \
                      ' 현재 온도는 ' + temperature + '로' + weather[1].replace('˚', '도')

        template_msg = '오늘 ' + location + ' 날씨를 알려드릴게요. 😊' + weather

    except:
        print("############################")
        print("#  WEATHER CRAWLER ERROR   #")
        print("############################")

        template_msg = "죄송해요, 지금은 " + location + "의 날씨는 알 수 없어요.  😭" + "\n\n" + "지역의 이름을 알려주시면 다시 알려드릴게요."

    # print("\n\n[DEBUG2-1]today_weather (msg) >>\n", template_msg, end="\n\n")
    return template_msg, state, slot_data, None



def tomorrow_weather(location):
    global state, slot_data
    enc_location = urllib.parse.quote(location + ' 내일 날씨')
    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html.parser')

    try:
        temperature_morning = (soup
                               .find_all('div', class_='main_info morning_box')[0]
                               .find('span', class_='todaytemp').text) + '도'

        temperature_noon = (soup
                            .find_all('div', class_='main_info morning_box')[1]
                            .find('span', class_='todaytemp').text) + '도'

        weather_morning = (soup
                           .find_all('div', class_='main_info morning_box')[0]
                           .find('div', class_='info_data')
                           .find('ul', class_='info_list')
                           .find('li')
                           .find('p', class_='cast_txt').text).split(',')

        weather_noon = (soup
                        .find_all('div', class_='main_info morning_box')[1]
                        .find('div', class_='info_data')
                        .find('ul', class_='info_list')
                        .find('li')
                        .find('p', class_='cast_txt').text).split(',')
        glue = '에는'
        if weather_morning[0] == weather_noon[0]:
            glue = '에도'

        weather_morning, weather_noon = __tone_maker(weather_morning, weather_noon)
        template_msg = '내일 ' + location + ' 날씨를 알려드릴게요. 😊' + ' 내일 오전엔 ' + weather_morning[
            0] + ' , 기온은 ' + temperature_morning + '에요. 오후' + glue + ' ' + weather_noon[
                           0] + ' , 기온은 ' + temperature_noon + '입니다.'

        if '비가 내' in template_msg:
            template_msg += ' 내일은 우산을 챙기는게 좋을 것 같아요. ☔'

        elif '눈이 내' in template_msg:
            template_msg += ' 내일 나가신다면 따뜻하게 입고 나가시는게 좋을 것 같아요. 🧣🧤'

        elif '우박이' in template_msg:
            template_msg += ' 내일은 우박을 꼭 조심하세요! 🌨'

    except:
        print("############################")
        print("#  WEATHER CRAWLER ERROR   #")
        print("############################")

        template_msg = "죄송해요, 지금은 " + location + "의 날씨는 알 수 없어요.  :(" + "\n\n" + "지역의 이름을 알려주시면 다시 알려드릴게요."

    # print("\n\n[DEBUG2-2]tomorrow_weather (msg) >>\n", template_msg, end="\n\n")
    return template_msg, state, slot_data, None



def after_tomorrow_weather(location):
    global state, slot_data
    enc_location = urllib.parse.quote(location + ' 모레 날씨')
    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html.parser')

    try:
        temperature_morning = (soup
                               .find('div', class_='tomorrow_area day_after _mainTabContent')
                               .find_all('div', class_='main_info morning_box')[0]
                               .find('span', class_='todaytemp').text) + '도'

        temperature_noon = (soup
                            .find('div', class_='tomorrow_area day_after _mainTabContent')
                            .find_all('div', class_='main_info morning_box')[1]
                            .find('span', class_='todaytemp').text) + '도'

        weather_morning = (soup
                           .find('div', class_='tomorrow_area day_after _mainTabContent')
                           .find_all('div', class_='main_info morning_box')[0]
                           .find('div', class_='info_data')
                           .find('ul', class_='info_list')
                           .find('li')
                           .find('p', class_='cast_txt').text).split(',')

        weather_noon = (soup
                        .find('div', class_='tomorrow_area day_after _mainTabContent')
                        .find_all('div', class_='main_info morning_box')[1]
                        .find('div', class_='info_data')
                        .find('ul', class_='info_list')
                        .find('li')
                        .find('p', class_='cast_txt').text).split(',')
        glue = '에는'
        if weather_morning[0] == weather_noon[0]:
            glue = '에도'

        weather_morning, weather_noon = __tone_maker(weather_morning, weather_noon)
        template_msg = '모레 ' + location + ' 날씨를 알려드릴게요. 😊' + ' 모레 오전엔 ' + weather_morning[
            0] + ' , 기온은 ' + temperature_morning + '에요. 오후' + glue + ' ' + weather_noon[
                           0] + ' , 기온은 ' + temperature_noon + '입니다.'

        if '비가 내' in template_msg:
            template_msg += ' 모레는 우산을 챙기는게 좋을 것 같아요. ☔'
        elif '눈이 내' in template_msg:
            template_msg += ' 모레 나가신다면 따뜻하게 입고 나가시는게 좋을 것 같아요. 🧤🧣'
        elif '우박이' in template_msg:
            template_msg += ' 모레는 우박을 꼭 조심하세요! 🌨'

    except:
        print("############################")
        print("#  WEATHER CRAWLER ERROR   #")
        print("############################")

        # dust = "죄송해요, 지금은 " + location + " 미세먼지 정보를 확인 할 수 없어요." + "\n\n" + "지역의 이름을 알려주시면 다시 알려드릴게요."
        template_msg = "죄송해요, 지금은 " + location + "의 날씨는 알 수 없어요.  😭" + "\n\n" + "지역의 이름을 알려주시면 다시 알려드릴게요."

    # print("\n\n[DEBUG2-2]after_tomorrow_weather (msg) >>\n", template_msg, end="\n\n")
    return template_msg, state, slot_data, None



def specific_weather(location, date):
    global state, slot_data
    try:
        enc_location = urllib.parse.quote(location + date + ' 날씨')
        url = 'https://www.google.com/search?q=' + enc_location
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'referer': 'http://google.com'}
        req = Request(url, headers=headers)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')

        weather = soup.find('span', {'id': 'wob_dc'}).text
        temp = soup.find('span', class_='wob_t').text
        if weather == '비': weather = '비가 오고'
        response = date + ' 날씨를 알려드릴게요. 😊' + location + '의 ' + date + ' 날씨는 ' + weather + ' 온도는 ' + temp + '도입니다.'
    except:
        response = "죄송해요, 지금은 " + location + "의 날씨는 알 수 없어요.  😭" + "\n\n" + "지역의 이름을 알려주시면 다시 알려드릴게요."

    # print("\n\n[DEBUG2-3]specific_weather (msg) >>\n", response, end="\n\n")
    return response, state, slot_data, None



def this_week_weather(location):
    global state, slot_data
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'referer': 'http://google.com'}

        days = ['월', '화', '수', '목', '금', '토', '일']
        templete_msg = location + '의 이번주 날씨를 알려드릴게요. 😊'
        response = []
        response.append(templete_msg)

        for i in days:
            loc = urllib.parse.quote(location + ' ' + i + '요일' + ' 날씨')
            url = 'https://www.google.com/search?q=' + loc
            req = Request(url, headers=headers)
            page = urlopen(req)
            html = page.read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            weather = soup.find('span', {'id': 'wob_dc'}).text
            temp = soup.find('span', class_='wob_t').text
            if weather == '비': weather = '비가 오고'
            weather = i + '요일의 날씨는 ' + weather + ' 온도는 ' + temp + '도 입니다. '
            response.append(weather)
    except:
        print("############################")
        print("#  WEATHER CRAWLER ERROR   #")
        print("############################")

        response = "죄송해요, 지금은 " + location + "의 날씨는 알 수 없어요.  😭" + "\n\n" + "지역의 이름을 알려주시면 다시 알려드릴게요."

    # print("\n\n[DEBUG2-3]this_week_weather (msg) >>\n", response, end="\n\n")
    return ' '.join(response), state, slot_data, None