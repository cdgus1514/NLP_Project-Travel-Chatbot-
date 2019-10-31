import pymysql as py

def addUser():
    conn = py.connect(host="cdgus1514.cafe24.com", user="cdgus1514", password="Chlehd131312", database="cdgus1514", charset="utf8")
    cursor = conn.cursor()
    query = "SELECT * FROM chatbot_users WHERE user_id = '%s'" % (Userid)
    cursor.execute(query)

    db_data = cursor.fetchall()
    

    if db_data:
        message = '중복되는 아이디 입니다.'
        print(message)
        result = [['message', message], ['sender', 'chatbot'], ['session', False]]
        
        return dict(result)

    else:
        query = "INSERT INTO chatbot_users (user_id, user_pw) value (%s, %s)"
        value = (Userid, Userpw)
        cursor.execute(query, value)

        conn.commit()

        cursor.close()
        conn.close()

        message = "Success Regist!!!"

        result = [['message', message], ['sender', 'chatbot'], ['session', True]]

        return dict(result)
    
    