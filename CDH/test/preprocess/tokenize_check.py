import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tokenizer import tokenize

from crawler_configs import Crawlerconfigs


check = tokenize("테마파크")
print(check)




