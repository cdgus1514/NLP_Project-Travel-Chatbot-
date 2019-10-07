import random
import re
import urllib
from urllib.request import urlopen, Request

import bs4
# from bs4 import BeautifulSoup


def recommand_tour(location):
    if location == "부산":
        url = "https://bto.or.kr/renewal/06_visitor/b01.php"

    rand = random.randint(1, 5)
    req = Request(url)
    # print("\n(req) >>\n", req)
    
    page = urlopen(req)
    # print("\n(page) >>\n", page)
    
    html = page.read()
    # print("\n(html) >>\n", html)
    
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # print("\n(soup) >>\n", soup)
    
    n = rand
    tab_ = ("tab_"+str(n))
    # list_name = soup.find("li", {"id":"tab_1"})
    list_name = soup.find("li", {"id":tab_})
    # list_name = list_name.find_all("dd")
    print("\n(list_name) >>\n", list_name)
    
    v_tab =("v_tab"+str(n))
    list_info = soup.find("div", {"id":v_tab})
    list_info = list_info.find_all("dd")

    if list_info is not None and " ":
        info_sub = list_info.find("expe_box")
        # info_sub = info_sub.find_all("<h3>")
        print("\n(info_sub) >>", info_sub)
        print("\n(list_info1) >>\n", list_info)

    else:
        list_info = soup.find("div", {"id":v_tab})
        print("\n(list_info2) >>\n", list_info)



recommand_tour("부산")