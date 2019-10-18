import random

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler_configs import Crawlerconfigs



# data1 = {"massage":"오늘 서초구 날씨 어때"}
# print(data1)

# key = data1.keys
# value = data1.values

# print(key)
# print(value)
# print(data1["massage"])



config = Crawlerconfigs()

city = config.spa
select_city = random.choice(list(city.items()))

info = config.info
info_index = info[str(select_city[1])]

result = [select_city, info_index]
print(result)

print(result[0][0]) # 이름
print(result[0][1]) # 인덱스