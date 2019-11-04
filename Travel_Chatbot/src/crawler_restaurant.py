import random
import re
import urllib
from urllib.request import urlopen, Request

import bs4

state = None
slot_data = None

def recommend_restaurant(location):
    global state, slot_data
    print("\n[DEBUG1-0]recommand_restaurant (location) >>", location)
    
    enc_location = urllib.parse.quote(location + ' 맛집')
    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location
    print("\n[DEBUG1-1]recommand_restaurant (url) >>", url, end="\n")

    rand = 20

    try:
        # 사용자가 요청한 맛집 검색 or 선정
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        list_name = soup.find_all('a', class_='name')
    
    
        # print("\n[DEBUG1-6]recommand_restaurant (list_name) >>\n", list_name)
        # print("\n[DEBUG1-6]recommand_restaurant (list_name) >>", len(list_name), end="\n")
        
        ## 검색 결과가 없을경우
        if len(list_name) == 0:
            # seq2seq or 사과멘트
            msg = '죄송해요, 이 질문에 대한 정보는 아직 준비중이에요  😥'
            return msg, state, slot_data, imgurl, locations

        list_info = soup.find_all('div', class_='txt ellp')
        # print("\n\n[DEBUG1-7]recommand_restaurant (list_info) >>\n", list_info)
        # print("\n[DEBUG1-7]recommand_restaurant (list_info) >>", len(list_info), end="\n")
        

        ######## DEBUG ########
        cnt_name = len(list_name)
        for i in range(cnt_name):
            print("[DEBUG1-6-1]rand",i, ">>", list_name[i], end="\n")

        
        cnt_info = len(list_info)
        for i in range(cnt_info):
            print("[DEBUG1-7-1]rand",i, ">>", list_info[i], end="\n")
        

        frand = random.randint(0, cnt_name-1)
        print("\n",frand,"번째 식당", end="\n")
        name = list_name[frand].text.split()
        print("\n[DEBUG1-8]recommand_restaurant (name) >>", name, end="\n")
        
        ## remove name tag
        new_name=[]
        for c in name:        
            if len(c) == 1:
                name = re.sub('[a-zA-Z]', "", c)
                print("\n[DEBUG1-8]recommand_restaurant (parse) >>", name)
                if name == "":
                    pass
                else:
                    new_name.append(name)
            else:
                new_name.append(c)


        print("\n[DEBUG1-8]recommand_restaurant (parsing name) >>", new_name, end="\n")
        name = ' '.join(new_name)
        print("\n[DEBUG1-8]recommand_restaurant (result) >>", name, end="\n")
        # info = list_info[rand_info].text
        
        #######################

        if frand > cnt_info-1:
            info = location
        else:
            info = list_info[frand].text
        print("\n[DEBUG1-8]recommand_restaurant (info) >>", info, end="\n\n")
        specific_url = list_name[frand].get('href')
        print("\n[DEBUG1-9]recommand_restaurant (specific_url) >>", specific_url, end="\n\n\n")

        
        # 검색 결과 중 랜덤으로 뽑은 맛집 정보 파싱
        req = Request(specific_url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        # print("\n\n[DEBUG2-0]recommand_restaurant (specific_url soup) >>\n\n", soup)
        document = soup.find_all('div', {'class': 'txt'})
        
        ############################################ 이미지 ############################################
        try:
            img_url = []
            img = soup.findAll('a')
            for link in img:
                if 'href' in link.attrs:
                    img_url.append(link.attrs)
            
            for i in range(len(img_url)):
                try:
                    img = img_url[i]
                    imgurl = img['data-kakaotalk-image-url']
                    print("\n\n[DEBUG2-0]recommand_restaurant (imgurl1) >>\n", imgurl, end="\n\n")
                except:
                    pass
        except:
            img = soup.find("img")
            print("\n\n[DEBUG2-0]recommand_restaurant (img2) >>\n", img, end="\n")
            
            imgurl = img.get('src')
            print("\n\n[DEBUG2-0]recommand_restaurant (imgurl2) >>\n", imgurl, end="\n\n")

            if img is None or len(img) == 0:
                img = []
                for meta in soup.find_all('meta'):
                    # print(meta)
                    img.append(meta.get('content'))
                
                img = img[-1]
                # print("\n\n[DEBUG2-0]recommand_restaurant (img3) >>\n", img, end="\n")
                imgurl = img
                print("\n\n[DEBUG2-0]recommand_restaurant (imgurl3) >>\n", imgurl, end="\n\n")
            
            else:
                print("################## Failed search img ##################")
                imgurl = None
        ###############################################################################################



        ########################################### 네이버맵 ###########################################
        map_url = []
        for link in soup.findAll('a'):
            if 'href' in link.attrs:
                map_url.append(link.attrs['href'])

        # print("[DEBUG2-2]recommand_restaurant (check url)\n", map_url)
        
        for i in range(3,10):
            try:
                mapurl = map_url[i]
                print("\n\n[DEBUG2-2]recommand_restaurant (map url)\n", mapurl, end="\n\n")
                position = mapurl.split('&')
                print("[DEBUG2-2]recommand_restaurant (position) >>", position, end="\n")
                print("[DEBUG2-2]recommand_restaurant (position lenghth) >>", len(position), end="\n")
                if len(position) == 5:
                    elng = position[2].split('=')
                    elat = position[4].split('=')
                    if  elng[0] != 'lng':
                        if elng[0] != 'elng':
                            raise Exception
                    elng = elng[1]
                    elat = elat[1]
                else:
                    elng = position[1].split('=')
                    elat = position[2].split('=')
                    if  elng[0] != 'lng':
                        if elng[0] != 'elng':
                            raise Exception
                    elng = elng[1]
                    elat = elat[1]
                print("[DEBUG2-2]recommand_restaurant (elng) >>", elng)
                print("[DEBUG2-2]recommand_restaurant (elat) >>", elat, end="\n\n")
                
                break
            
            except:
                pass

        locations = (elng, elat, specific_url)
        ###############################################################################################



        ############################################# 정보 ############################################
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
        print("\n[DEBUG2-3]recommand_restaurant (link_path) >>", link_path, end="\n\n")
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
                # print("\n[DEBUG2-1]recommand_restaurant (description_soup) >>\n", soup, end="\n\n")
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

        print("\n[DEBUG1-2-2]recommand_restaurant (description) >>\n", description)

        msg = info + '!  ' + name + '에 가보는 건 어떨까요?  🤗\n\n'

        if description != ' ':
            msg += description

        if time != '':
            msg += '\n\n⏰ 운영시간\n' + time

        if addr != '':
            msg += '\n\n📬 주소\n' + addr

        if tel != '':
            msg += '\n\n📞 전화번호\n' + tel

        # print("\n\n\n[DEBUG3-1]recommand_restaurant (msg) >>\n", msg, end="\n\n\n")
        print("[DEBUG3-1]recommand_restaurant (result imgUrl) >>\n", imgurl, end="\n\n")
        print("[DEBUG3-1]recommand_restaurant (result locations) >>\n", locations, end="\n\n")
        ###############################################################################################
    
    except:
        print("############################")
        print("# RESTAURANT CRAWLER ERROR #")
        print("#### 플레이스 정보 없음  ####")
        print("############################")

        msg = "죄송해요, " + location + "에 대한 맛집 정보는 아직 준비중이에요  😥" + "\n" + "더 많은 정보들을 제공할 수 있도록 노력할게요."
        imgurl = None
        locations = (None, None, None)
    

    return msg, state, slot_data, imgurl, locations



# while True:
#     print("키워드 입력 >> ", end=" ")
    
#     recommend_restaurant(input())

# recommend_restaurant("서초구 마카롱")
# print(recommend_restaurant("강남역 카페"))