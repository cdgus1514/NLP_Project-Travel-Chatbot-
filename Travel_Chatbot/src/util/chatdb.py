import pymysql as py

def addChat(uid, question, answer):

    # insert chat
    conn = py.connect(host="cdgus1514.cafe24.com", user="cdgus1514", password="Chlehd131312", database="cdgus1514", charset="utf8")
    cursor = conn.cursor()

    query = "INSERT INTO chatbot_chat (user_id, question, answer) value (%s, %s, %s)"
    value = (uid, question, answer)
    cursor.execute(query, value)

    conn.commit()

    cursor.close()
    conn.close()