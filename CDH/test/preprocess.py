from tokenizer import tokenize
from configs import IntentConfigs

# CONFIG
config = IntentConfigs()
df = config.df


def preprocess_data(tokenizing):
    if tokenizing:
        encode = []
        for i in df['question']:
            # df.replace(i, tokenize(i), regex=True, inplace=True)
            q = tokenize(i)
            encode.append(q)

    return encode