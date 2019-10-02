import os
import pandas as pd

# path = 'HoingMarryShip\\CDH\\model\\cdh_test'
path = "C:\\Study\\cdh_test\\"

df = pd.read_csv('HoingMarryShip\CDH\\test\\data\\train_intent.csv')    # 수정(3)
print(type(df))
print(len(df))

file_list = os.listdir(path)
print(file_list)

new_num = 0

# if os.path.exists(path):
#     for i in file_list:
#         num = int(i.split(".")[0].split("-")[-1])
#     print(num)

#     if new_num < num:
#         new_num = num + 100

#     print(new_num)

if os.path.exists(path):
    for i in file_list:
        num = int(i.split(".")[0].split("-")[-1])
        print(num)

        if new_num < num:
            new_num = num
            print("new_num >>", new_num)
        

    path = "C:\\Study\\cdh_test\\intent_model-"+str(new_num)+".txt"
    
    with open(path, 'r') as f:
        # 한줄씩 읽어오기
        line = f.readline()
        print("\n>>", line)
