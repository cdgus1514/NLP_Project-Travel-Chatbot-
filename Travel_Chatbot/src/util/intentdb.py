import pymysql as py

def addIntent(intent):
    
    # insert intent
    conn = py.connect(host="cdgus1514.cafe24.com", user="cdgus1514", password="Chlehd131312", database="cdgus1514", charset="utf8")
    cursor = conn.cursor()

    query = "INSERT INTO chatbot_intent (intent) value (%s)"
    value = intent
    cursor.execute(query, value)

    conn.commit()

    cursor.close()
    conn.close()