import pymysql as py

def checkUser(Userid, Userpw):

    # check user_id & user_pw
    conn = py.connect(host="cdgus1514.cafe24.com", user="cdgus1514", password="Chlehd131312", database="cdgus1514", charset="utf8")
    cursor = conn.cursor()
    
    query = "SELECT user_id, user_pw FROM chatbot_users WHERE user_id = %s"
    value = (Userid)
    cursor.execute("set names utf8")
    cursor.execute(query, value)
    check_user = cursor.fetchone()

    cursor.close()
    conn.close()

    try:
        print(check_user, end="\n\n")
        # print("ID >> ", check_user[0][0])
        # print("PW >> ", check_user[0][1], end="\n\n")
        print("ID >> ", check_user[0])
        print("PW >> ", check_user[1], end="\n\n\n")

    except:
        message = "############## Failed Login ##############\n\n\n\n"
        print(message)

        result = [['nick', Userid], ['state', None]]


        return result, False


    # ID/PW 체크
    if Userid == check_user[0] and Userpw == check_user[1]:
        message = "############## Success Login!!! ##############\n\n\n\n"
        print(message)

        result = [['nick', Userid], ['state', 'OK']]
        
        return result, True
    
    else:
        message = "############## Failed Login ##############\n\n\n\n"
        print(message)

        result = [['nick', Userid], ['state', None]]

        return result, False