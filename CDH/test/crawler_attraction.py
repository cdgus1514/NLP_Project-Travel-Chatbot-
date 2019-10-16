from crawler.hanatour_crawler import travel_search, city_search
from crawler.attraction_crawler import place_link, place_list
from crawler.festival_crawler import festival_list, festival_cr



# 네이버 검색
crawler = [place_link, place_list, festival_cr, festival_list]

state = None
slot_data = None



def search_cr(str_):
    # https://developers.naver.com/docs/search/blog/ 참고

    for func in crawler:
        # print("[DEBUG11-0]search_cr (crawler) >>", func, end="\n\n")
        func = func(str_)
        
        if not func == None:
            return func
    
    return None



def recommand_attraction(local, travel):
    
    try:
        city_idx = city_search(local)

        # 하나투어에 없는 지역(도시)일 경우
        if city_idx == None and len(local) > 1:
            # 네이버
            print('@네이버', end="\n")
            query = local + ' ' + travel
            print('네이버 검색어 :', query, end="\n\n")
            msg = search_cr(query)
            if not msg == None:
                
                print("\n[DEBUG1-1] recommand_attraction (msg(naver-naver)) >>\n", msg)
                return msg, state, slot_data

            
            # 하나 투어
            print('@하나투어', end="\n")
            msg = travel_search(travel, city_idx)
            
            print("\n[DEBUG1-2] recommand_attraction (msg(hana)) >>\n", msg)
            return msg, state, slot_data

        else:
            # 하나 투어
            print('@하나투어 (in 하나투어)', end="\n")
            msg = travel_search(travel, city_idx)
            if not msg == None:

                print("\n[DEBUG1-1] recommand_attraction (msg(hana)) >>\n", msg)            
                return msg, state, slot_data

            # 네이버
            print('@네이버 (in 하나투어)', end="\n")
            query = local + ' ' + travel
            print('네이버 검색어 :', query, end="\n\n")
            msg = search_cr(query)
            
            if not msg == None:
                print("\n[DEBUG1-2] recommand_attraction (msg(hana-naver)) >>\n", msg)
                return msg, state, slot_data
            
        
        # return result, state, slot_data
    
    except:
        print("############################")
        print("# ATTRACTION CRAWLER ERROR #")
        print("############################")

        msg = "죄송해요, " + local + travel +"관광지에 대한 정보는 아직 준비중이에요  :(" + "\n" + "더 많은 정보를 제공할 수 있도록 노력할게요."


    return msg, state, slot_data


# TEST
# recommand_attraction('', '에버랜드')
# recommand_attraction('', '남산타워')
# recommand_attraction('', '박물관')
# recommand_attraction('', '남산')