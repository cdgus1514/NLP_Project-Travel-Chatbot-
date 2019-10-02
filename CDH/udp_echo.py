import sys
from socket import *

from src.entity.news.entity_recognizer import get_news_entity
from src.entity.restaurant.entity_recognizer import get_restaurant_entity
from src.entity.song.entity_recognizer import get_song_entity
from src.entity.translate.entity_recognizer import get_translate_entity
from src.entity.weather.entity_recognizer import get_weather_entity
from src.entity.wiki.entity_recognizer import get_wiki_entity
from src.intent.classifier import get_intent
from src.scenario.date import date
from src.scenario.issue import issue
from src.scenario.restaurant import restaurant
from src.scenario.song import song
from src.scenario.time import times
from src.scenario.translate import translate
from src.scenario.weather import weather
from src.scenario.dust import dust
from src.scenario.wiki import wiki
from src.scenario.wise import wise
from src.util.hanspell.spell_checker import fix
from src.util.tokenizer import tokenize

# ECHO_PORT 기본 포트
ECHO_PORT = 50000 + 7

# 버퍼 사이즈
BUFSIZE = 1024

# 메인 함수 
def main():
    # 매개변수가 2개보다 적다면
    if len(sys.argv) < 2:
        # 사용 방법 표시
        usage()

    # 첫 매개변수가 '-s' 라면 
    if sys.argv[1] == '-s':
        #서버 함수 호출 
        server()

    # 첫 매개변수가 '-c' 라면
    elif sys.argv[1] == '-c':
        #클라이언트 함수 호출
        client()

    # '-s' 또는 '-c' 가 아니라면 
    else:
        # 사용 방법 표시
        usage()

# 사용하는 방법 화면에 표시하는 함수
def usage():
    sys.stdout = sys.stderr
    print('Usage: udpecho -s      [port]       (server)')
    print('or:    udpecho -c host [port] <file (client)')
    # 종료
    sys.exit(2)

# 서버 함수
def server():
    # 매개 변수가 2개 초과라면 
    # ex>$ python udp_echo.py -s 8001
    if len(sys.argv) > 2:
        # 두번째 매개변수를 포트로 지정
        port = eval(sys.argv[2])

    # 매개 변수가 2개 라면 
    # ex>$ python udp_echo.py -s
    else:
        # 기본 포트로 설정        
        port = ECHO_PORT

    # 소켓 생성 (UDP = SOCK_DGRAM, TCP = SOCK_STREAM)
    s = socket(AF_INET, SOCK_DGRAM)
    
    # 포트 설정
    s.bind(('', port))
    
    # 준비 완료 화면에 표시
    print('udp echo server ready')
    print("----------------------------------------------------")

    # 무한 루프 돌림
    while 1:
        # 클라이언트로 메시지가 도착하면 다음 줄로 넘어가고
        # 그렇지 않다면 대기(Blocking)
        data, addr = s.recvfrom(BUFSIZE)

        # 받은 메시지와 클라이언트 주소 화면에 출력
        # print("recv data >> ", data)    # byte
        print('User : %r from %r' % (data.decode("utf-8"), addr))
        pdata = data.decode("utf-8")    # convert byte to str


        # used Özgür Vatansever-firebase REST API
        from firebase import firebase

        firebase = firebase.FirebaseApplication("https://python-test-66f9b.firebaseio.com/", None)
        speech = preprcoess(pdata)
        data = {"Name":"User", "text":speech}
        result = firebase.post("/Chatbot/", data)

        print('Preprocessed : ' + speech , sep='')
        intent = get_intent(speech)
        print('Intent : ' + intent , sep='')
        entity = get_entity(intent, speech)
        print('Entity : ' + str(entity) , sep='')
        
        # A.I 답변 firebase에서 전달
        answer = scenario(intent, entity)
        data = {"Name":"A.I", "text":answer}
        result = firebase.post("/Chatbot/", data)
        
        firebase_result = firebase.get("/Chatbot/", "")
        key = firebase_result.keys()
        key = list(key)
        n = key[-1]

        print("A.I(firebase) :" + firebase_result.get(n).get("text"))

    
        # 받은 메시지를 클라이언트로 다시 전송
        # print("sned origin data >> ", data)
        data = firebase_result.get(n).get("text")
        data = str(data).encode()   # convert dict to bytes
        # print("sned convert data >> ", data)
        print("----------------------------------------------------")
        s.sendto(data, addr)
        # 다시 처음 루프로 돌아감


# 클라이언트 함수
def client():
    # 매개변수가 3개 미만 이라면
    if len(sys.argv) < 3:
        # 사용 방법 화면에 출력
        # usage함수에서 프로그램 종료
        usage()

    # 두번째 매개변수를 서버 IP로 설정
    host = sys.argv[2]

    # 매개변수가 3개를 초과하였다면(4개라면)
    # ex>$ python udp_echo.py -c 127.0.0.1 8001
    if len(sys.argv) > 3:
        # 3번째 매개변수를 포트로 설정
        port = eval(sys.argv[3])

    # 초과하지 않았다면(즉, 3개라면) 
    # ex>$ python udp_echo.py -c 127.0.0.1
    else:
        # 기본 포트로 설정
        port = ECHO_PORT

    # IP 주소 변수에 서버 주소와 포트 설정 
    addr = host, port

    # 소켓 생성
    s = socket(AF_INET, SOCK_DGRAM)
   
    # 클라이언트 포트 설정 : 자동
    s.bind(('', 0))

    # 준비 완료 화면에 출력
    print("udp echo client ready, reading stdin")

    # 무한 루프
    while 1:
        #터미널 차(입력창)에서 타이핑을하고 ENTER키를 누를때 까지  
        line = sys.stdin.readline()
        #변수에 값이 없다면
        if not line:
            break

        # 입력받은 텍스트를 서버로 발송
        s.sendto(line.encode("utf-8"),(addr))

        # 리턴 대기
        data, fromaddr = s.recvfrom(BUFSIZE)
        # 서버로부터 받은 메시지 출력
        print('client received %r from %r' % (data, fromaddr))


def preprcoess(speech) -> str:
    speech = fix(speech)
    speech = tokenize(speech)
    speech = fix(speech)
    return speech


def get_entity(intent, speech):
    # @/entity_recognizer/get_@_entity(sentence, is_train) 실행
        # model = NERModel
        # model.build()
        # model.train() >>
        # model.evaluate() >>
        # return model.predict() >> (문장 형태소 분할), (단어 태그)
    if intent == '날씨' or intent == '먼지':
        return get_weather_entity(speech, False)
    elif intent == '뉴스':
        return get_news_entity(speech, False)
    elif intent == '음악':
        return get_song_entity(speech, False)
    elif intent == '위키' or intent == '인물':
        return get_wiki_entity(speech, False)
    elif intent == '맛집':
        return get_restaurant_entity(speech, False)
    elif intent == '번역':
        return get_translate_entity(speech, False)
    else:
        return None


def scenario(intent, entity) -> str:
    if intent == '먼지':
        return dust(entity)
    elif intent == '날씨':
        return weather(entity)
    elif intent == '인물' or intent == '위키':
        return wiki(entity)
    elif intent == '명언':
        return wise()
    elif intent == '달력':
        return date()
    elif intent == '시간':
        return times()
    elif intent == '번역':
        return translate(entity)
    elif intent == '이슈':
        return issue()
    elif intent == '음악':
        return song(entity)
    elif intent == '맛집':
        return restaurant(entity)
    else:
        return '그 기능은 아직 준비 중이에요.'


main()