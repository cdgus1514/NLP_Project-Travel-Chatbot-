import random
import re
import urllib
from urllib.request import urlopen, Request

import bs4


def recommend_restaurant(location):
    print("\n[DEBUG1-0]recommand_restaurant (location) >>", location)
    
    enc_location = urllib.parse.quote(location + '맛집')
    # print("\n[DEBUG1]recommand_restaurant (enc_location) >>", enc_location)
    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location
    print("\n[DEBUG1-1]recommand_restaurant (url) >>", url, end="\n")

    rand = 20

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # print("\n[DEBUG1-5]recommand_restaurant (soup) >>\n", soup)
    list_name = soup.find_all('a', class_='name')
    print("\n[DEBUG1-6]recommand_restaurant (list_name) >>\n", list_name)
    print("\n[DEBUG1-6]recommand_restaurant (list_name) >>", len(list_name), end="\n")

    list_info = soup.find_all('div', class_='txt ellp')
    print("\n\n[DEBUG1-7]recommand_restaurant (list_info) >>\n", list_info)
    print("\n[DEBUG1-7]recommand_restaurant (list_info) >>", len(list_info), end="\n")
    
    ######## DEBUG ########
    cnt_name = len(list_name)

    for i in range(cnt_name):
        print("[DEBUG1-6-1]rand",i, ">>", list_name[i], end="\n")
    #######################
    
    ######## DEBUG ########
    cnt_info = len(list_info)

    for i in range(cnt_info):
        print("[DEBUG1-7-1]rand",i, ">>", list_info[i], end="\n")
    #######################



    # rand_name = random.randint(0, cnt_name-1)
    # rand_info = random.randint(0, cnt_info-1)
    frand = random.randint(0, cnt_name-1)
    print("\n",frand,"번째 식당", end="\n")
    name = list_name[frand].text.split()
    print("\n[DEBUG1-8]recommand_restaurant (name) >>", name, end="\n")
    
    
    new_name=[]
    for c in name:
        name = re.sub('[a-zA-Z]', "", c)
        if name == "":
            pass
        else:
            new_name.append(name)

    print("\n[DEBUG1-8]recommand_restaurant (parsing name) >>", new_name, end="\n")
    name = ' '.join(new_name)
    print("\n[DEBUG1-8]recommand_restaurant (name) >>", name, end="\n")
    # info = list_info[rand_info].text
    print(frand)
    if frand > cnt_info-1:
        info = location
    else:
        info = list_info[frand].text
    print("\n[DEBUG1-8]recommand_restaurant (info) >>", info, end="\n")
    # specific_url = list_name[rand_name].get('href')
    specific_url = list_name[frand].get('href')
    print("\n[DEBUG1-8]recommand_restaurant (specific_url) >>", specific_url, end="\n")
    req = Request(specific_url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    document = soup.find_all('div', {'class': 'txt'})

    tel = ''
    if document[0] is not None:
        tel = document[0].text

    addr = ''
    if document[1].find('span', {'class': 'addr'}) is not None:
        addr = document[1].find('span', {'class': 'addr'}).text

    time = ''
    if document[2].find('span', {'class': 'time'}) is not None:
        time = document[2].find('span', {'class': 'time'}).text
        time = re.sub("-", " 에서 ", time)

    if document[3].find_all('em', {'class': 'price'}) is not None:
        price_list = document[3].find_all('em', {'class': 'price'})
        menu_list = document[3].find_all('span', {'class': 'name'})

        menu_size = len(price_list)
        menu = []
        menu_dict = {}
        for i in range(menu_size):
            for p in price_list, menu_list:
                menu.append(p[i].text)
        for i in range(len(menu)):
            if i % 2 == 0:
                menu_dict[menu[i + 1]] = menu[i]

    link_path = soup.find('ul', {'class': 'list_relation_link'})
    if link_path is not None:

        link = link_path.find_all('li', {'class': 'list_item'})
        siksin = ''
        for i in link:
            link_spceific = i.find('a').get('href')
            if 'siksinhot' in link_spceific:
                siksin = link_spceific
        if siksin != '':
            req = Request(siksin)
            page = urlopen(req)
            html = page.read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            siksin_doc = soup.find('div', {'itemprop': 'articleBody'}).text.split()

            counter = False
            response_list = []
            for word in siksin_doc:
                word = re.sub('하다', '합니다', word)
                word = re.sub('한다', '합니다', word)
                word = re.sub('했다', '했어요', word)
                word = re.sub('했었다', '했었어요', word)
                word = re.sub('이다', '입니다', word)
                word = re.sub('있다', '있어요', word)
                word = re.sub('있었다', '있었어요', word)

                if '전화번호' in word:
                    response_list.append(word.split(sep='전화번호', maxsplit=1)[0])
                    counter = False
                if counter:
                    response_list.append(word)
                if '매장소개' in word:
                    response_list.append(word.split(sep='매장소개', maxsplit=1)[1])
                    counter = True

            description = ' '.join(response_list)
        else:
            description = ''
    else:
        description = ''

    print("\n[DEBUG1-9]recommand_restaurant (description) >>\n", description)

    msg = info + '!  ' + name + '에 가보는 건 어떨까요?\n'

    if description != ' ':
        msg += description

    if time != '':
        msg += '\n\n운영시간은 ' + time

    if addr != '':
        msg += '\n주소 : ' + addr

    if tel != '':
        msg += '\n전화번호 : ' + tel

    print("\n[DEBUG2-1]recommand_restaurant (msg) >>\n", msg)
    return msg


# recommend_restaurant("신논현역 고깃집")