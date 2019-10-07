import string, re

def parsing_data(text):

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


    # print("-----------------------------------------------------------")

    for c in text:
        # print(c)
        name = re.sub('[a-zA-Z/<>"-=^0-9]', "", c)
        if name == "":
            pass
        else:
            new_name.append(name)
        
    # print(new_name)
    new_name = ''.join(new_name)
    # print(new_name)

    
    return new_name