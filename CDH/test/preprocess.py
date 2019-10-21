from tokenizer import tokenize
from configs import Configs

# CONFIG
config = Configs()
df = config.df


def preprocess_data(tokenizing):
    if tokenizing:
        encode = []
        for i in df['question']:
            q = tokenize(i)
            encode.append(q)

    return encode