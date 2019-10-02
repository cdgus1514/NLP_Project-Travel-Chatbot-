import string, re

name = ["생각나는부대찌개"]
name2 = ["E", "이태리부대찌개", "강남역"]
name3 = ['완백부대찌개', '강남', '더인피닛스퀘어점']
name4 = ['STEW', 'BUDAE']


new_name=[]

# for c in name3:
#     name = re.sub('[a-zA-Z]', "", c)
#     if name == "":
#         pass
#     else:
#         new_name.append(name)

# print(new_name)
# new_name = ' '.join(new_name)
# print(new_name)


print("-----------------------------------------------------------")

for c in name4:
    print(c)
    name = re.sub('[a-zA-Z]', "", c)
    if name == "":
        pass
    else:
        new_name.append(name)
    
print(new_name)
new_name = ' '.join(new_name)
print(new_name)