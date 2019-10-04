# __Choi DongHyeon__
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
5. scenario   (의도, 개체명, 크롤링 >> 결과출력)

<br>
<br>

# cdh_scenario.py
- 크롤링 실행 소스

1. intent 확인 후 맞는 카테고리 메소드 실행
2. 테그 분리 후 크롤링 실행

<br>
<br>

# flaskrestful.py
- flask_restful api 사용
- POST방식으로 온 json 데이터를 파싱 후 훈련된 모델에 넣어 결과값 예측, POST 방식으로 클라이언트에게 결과값 전달

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

1. 구글 드라이브에서 가장 최신 모델 다운 후 model/intent/ 경로에 저장
2. configs 파일 root_path 수정 (경로 다를 시)
3. main.py 실행

<br>
<br>
<br>

# 수정 -- 10/02
- ~~main~~
- application [get_intent(o), get_entity(x), scenario(x)]
- tokenizer
- preprocess
- cdh_intent
- configs
- model_configs
- flaskrestful (main)

<br>

### flask-restful api
### post로 받아 predict 후 post로 client에 결과전달

<br>

1. 구글드라이브에서 최신 모델 다운로드 후 model/intent/ 경로에 저장
2. configs 파일 root_path 수정 (경로 다를 경우)
3. model_configs 파일 root_path 수정 (경로 다를 경우)
4. flaskrestful.py 실행
5. 클라이언트에서 질문입력, 결과출력

<br>
<br>
<br>

# 수정 -- 10/04
- application [get_intent(○), get_entity(×), scenario(△)]
- tokenizer
- preprocess
- cdh_intent
- configs
- model_configs
- flaskrestful (main)
- cdh_scenario
- crawler_restaurant
- crawler_weather
- crawler_dust
<br>

##### application 수정
##### crawler 파일 추가
##### scenario 파일 추가
##### config 파일 수정
<br>

1. 구글드라이브에서 최신 모델 다운로드 후 model/intent/ 경로에 저장
2. configs 파일 root_path 수정 (경로 다를 경우)
3. model_configs 파일 root_path 수정 (경로 다를 경우)
4. flaskrestful.py 실행
5. 클라이언트에서 질문입력, 결과출력