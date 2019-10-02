from firebase import firebase

firebase = firebase.FirebaseApplication("https://python-test-66f9b.firebaseio.com/", None)

data =  { 'Name': '고병주2',  
          'RollNo': 3,  
          'Percentage': 18.18  
          }

# result = firebase.post("/python-test-66f9b/Students/", data)

# Chatbot 테이블에 있는 키 값들 불러오기
result = firebase.get("/Chatbot/", "")
key=result.keys()

key=list(result.keys())

i = key[-1]
print(result.get(i).get("text"))

# for i in key:
#     # print(result.get(i).get("Name"))
#     name = result.get(i).get("Name")
#     if name == "User":
#         print("User :"+result.get(i).get("text"))
#     # print(result.get(i).get("text"))
    
#     if name == "A.I":
#         print("A.I :"+result.get(i).get("text"))

print(i)
test = firebase.get("/Chatbot", None, {"Name": "User"})
print(test)