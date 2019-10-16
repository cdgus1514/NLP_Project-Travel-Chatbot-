import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

import parsing_test as ps

url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EA%B2%BD%EB%B3%B5%EA%B6%81"

while(True):
    print("관광지 입력 >> ", end="")
    att = input()
    enc_att = urllib.parse.quote(att)
    url ="https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query="+enc_att
    print("\n\nurl >>\n", url, end="\n\n\n")

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')


    ## 관광지 정보
    try:
        info = soup.find_all('div', {'class': '_1h3B_0FxjX'})

        if info[len(info)-1].find('span', {'class': 'WoYOwsMl8Q'}) is None:
            data = info[len(info)-1].text
            print("info1 >>\n", data, end="\n\n\n")
        else:
            data = info[len(info)-1].find('span', {'class': 'WoYOwsMl8Q'}).text
            print("info2 >>\n", data, end="\n\n\n")
    except:
        print("죄송합니다. 요청하신 정보는 준비중이에요  :(\n\n")





# att = '마리원캠핑장'
# enc_att = urllib.parse.quote(att)
# url ="https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query="+enc_att
# print("\n\nurl >>\n", url, end="\n\n\n")

# req = Request(url)
# page = urlopen(req)
# html = page.read()

# soup = bs4.BeautifulSoup(html, 'html.parser')


# info = soup.find_all('div', {'class': '_1h3B_0FxjX'})
# pdata = info[len(info)-1].text

# print(pdata)