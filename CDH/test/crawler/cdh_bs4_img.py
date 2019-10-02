import random
import re
import urllib
from urllib.request import urlopen, Request

import bs4
# from bs4 import BeautifulSoup


def recommand_tour(location):
    if location == "부산":
        url = "https://weather.com/ko-KR/weather/today/l/KSXX0037:1:KS"

    rand = random.randint(0, 10)
    req = Request(url)
    print("\n(req) >>\n", req)
    
    page = urlopen(req)
    print("\n(page) >>\n", page)
    
    html = page.read()
    # print("\n(html) >>\n", html)
    
    soup = bs4.BeautifulSoup(html, 'html.parser')
    print("\n(soup) >>\n", soup)
    

    list_img = soup.find("div", {"id":"main-LookingAhead-b39982dc-b828-42f9-9ca4-3d6686c1bb83"})
    print(list_img)





recommand_tour("부산")