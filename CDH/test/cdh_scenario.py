from crawler_restaurant import recommend_restaurant
from crawler_weather import today_weather
from crawler_weather import tomorrow_weather
from crawler_weather import this_week_weather
from crawler_weather import specific_weather
from crawler_dust import today_dust
from crawler_dust import tomorrow_dust
from crawler_dust import after_tomorrow_dust



def restaurant(named_entity):
    print("[DEBUG1-1]scenario restaurant (named_entity) >>\n", named_entity)
    keyword_group = named_entity[0]
    print("[DEBUG1-2]scenario restaurant (keyword) >>\n", keyword_group)
    entity_group = named_entity[1]
    print("[DEBUG1-2]scenario restaurant (entity) >>\n", entity_group)
    location = []

    for k in zip(keyword_group, entity_group):
        if 'LOCATION' in k[1]:
            location.append(k[0])

    print("[DEBUG1-3]scenario restaurant (location) >>", location)

    if len(location) == 0:
        while len(location) == 0:
            print('A.I : ' + '어떤 맛집을 알려드릴까요?')
            print('User : ', end='', sep='')
            loc = input()
            if loc is not None and loc.replace(' ', '') != '':
                location.append(loc)

    return recommend_restaurant(' '.join(location))



def weather(named_entity):
    print("[DEBUG2-1]scenario weather (named_entity) >>", named_entity, end="\n")
    keyword_group = named_entity[0]
    print("[DEBUG2-2]scenario weather (keyword) >>", keyword_group, end="\n")
    entity_group = named_entity[1]
    print("[DEBUG2-2]scenario weather (entity) >>", entity_group, end="\n\n")
    date = []
    location = []

    for k in zip(keyword_group, entity_group):
        if 'DATE' in k[1]:
            date.append(k[0])
        elif 'LOCATION' in k[1]:
            location.append(k[0])
    
    print("[DEBUG2-3]scenario weather (data) >> ", date, end="\n")
    print("[DEBUG2-3]scenario weather (location) >> ", location, end="\n")

    if len(date) == 0:
        date.append('오늘')

    if len(location) == 0:
        while len(location) == 0:
            print('A.I : ' + '어떤 지역을 알려드릴까요?')
            print('User : ', end='', sep='')
            loc = input()
            if loc is not None and loc.replace(' ', '') != '':
                location.append(loc)

    if '오늘' in date:
        return today_weather(' '.join(location))
    elif date[0] == '내일':
        return tomorrow_weather(' '.join(location))
    elif '모레' in date or '내일모레' in date:
        return after_tomorrow_weather(' '.join(location))
    elif '이번' in date and '주' in date:
        return this_week_weather(' '.join(location))
    else:
        return specific_weather(' '.join(location), ' '.join(date))



def dust(named_entity):
    print("[DEBUG3-1]scenario dust (named_entity) >>", named_entity, end="\n")
    keyword_group = named_entity[0]
    print("[DEBUG3-2]scenario dust (keyword) >>\n", keyword_group)
    entity_group = named_entity[1]
    print("[DEBUG3-2]scenario dust (entity) >>", entity_group, end="\n\n")
    date = []
    location = []

    for k in zip(keyword_group, entity_group):
        if 'DATE' in k[1]:
            date.append(k[0])
        elif 'LOCATION' in k[1]:
            location.append(k[0])

    print("[DEBUG3-3]scenario dust (data) >> ", date, end="\n")
    print("[DEBUG3-3]scenario dust (location) >> ", location, end="\n")

    if len(date) == 0:
        date.append('오늘')

    if len(location) == 0:
        while len(location) == 0:
            print('A.I : ' + '어떤 지역을 알려드릴까요?')
            print('User : ', end='', sep='')
            loc = input()
            if loc is not None and loc.replace(' ', '') != '':
                location.append(loc)

    if '오늘' in date:
        return today_dust(' '.join(location))
    elif date[0] == '내일':
        return tomorrow_dust(' '.join(location))
    elif '모레' in date or '내일모레' in date:
        return after_tomorrow_dust(' '.join(location))
    else:
        return '오늘, 내일, 모레의 미세먼지 상태만 알 수 있어요'