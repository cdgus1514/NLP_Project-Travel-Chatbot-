import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tokenizer import tokenize

from crawler_configs import Crawlerconfigs


check = tokenize("바다가 유명한 여행지 추천해줘")
print(check)




