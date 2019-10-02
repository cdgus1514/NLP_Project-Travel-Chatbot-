# CDH
<br>

# 서버에서 파이썬 구동 방법(예제소스)
- udp_socket 통신으로 데이터를 받아서 처리 후 DB에 저장
- 안드로이드에서 DB데이터를 불러와서 리스트뷰에 출력

1. main.py udp_echo.py 파일을 src 하위에 copy
   (main.py는 덮어쓰기 or 이름변경)

2. src 상위 경로에서 python -m src.main -s 8011

<br>
<br>


# cdh_intent.py
- 워드 임베딩, 의도파악 학습 후 모델에 적용 >> 의도출력

1. word2vec_model >> fasttext 학습 모델
2. model >> 의도파악 데이터셋 학습 된 모델
3. interface_embed >> 입력받은 데이터 토큰화 후 워드임베딩 모델에 적용
4. model.predict >> 워드임베딩 된 데이터를 학습된 모델에 predic 후 결과 출력


<br>
<br>


# application.py
- 챗봇 실행소스

1. input
2. preprocess (tokenize >> 형태소분석, 불용어 제거)
3. get_intent (의도파악)
4. get_entity (개체명 인식)
5. scenario   (의도가 개체명을 사용해서 결과 출력)

<br>
<br>
<br>

###### 모델은 구글 드라이드에 업로드해둠 (10/01)

<br>
<br>

# 실행방법 (구현단계) -- 10/01
- main
- application [get_intent(o), get_entity(x), scenario(x)]
- tokenizer
- preprocess
- cdh_intent
- config

<br>

1. 구글 드라이브에서 가장 최신 모델 다운 후 model/test/ 경로에 저장
2. configs 파일 root_path 수정 (경로 다를 시)
3. main.py 실행

<br>
<br>
<br>

# 수정 -- 10/02
- main
- application [get_intent(o), get_entity(x), scenario(x)]
- tokenizer
- preprocess
- cdh_intent
- configs
- model_configs
- flaskrestful
<br>

### flask-restful api
### post로 받아 predict 후 post로 client에 결과전달

<br>

1. 구글드라이브에서 최신 모델 다운로드 후 model/test/ 경로에 저장
2. configs 파일 root_path 수정 (경로 다를 시)
3. flaskrestful.py 실행
4. post api 요청 툴을 사용해서 post 전송