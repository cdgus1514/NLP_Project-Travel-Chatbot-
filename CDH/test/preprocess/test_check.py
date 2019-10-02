import random
import pandas as pd

cnt_name = 8
cnt_info = 5

frand = random.randint(0, cnt_name-1)
print(frand)

if frand > cnt_info:
    print("pass")
else:
    print("use frand")



df = pd.read_csv('C:\\Study\\Chatbot\\src\\entity\\restaurant\\train_entity.csv')

print(df)