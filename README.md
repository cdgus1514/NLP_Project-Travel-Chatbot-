# __Choi DongHyeon__
<br>

## 개발환경
- Windows 10
- VSC
- python 3.7.3
<br>
<br>

### cdh_intent.py
- 워드 임베딩, 의도파악 학습 후 모델에 적용 >> 의도출력

1. word2vec_model >> fasttext 학습 모델
2. model >> 의도파악 데이터셋 학습 된 모델
3. interface_embed >> 입력받은 데이터 토큰화 후 워드임베딩 모델에 적용
4. model.predict >> 워드임베딩 된 데이터를 학습된 모델에 predic 후 결과 출력

<br>
<br>

### jbh_entity.py
- 워드임베딩, 개체명인식 학습 후 모델에 적용 >> 개체출력
<br>
<br>

### application.py
- 챗봇 실행소스

1. input
2. preprocess (tokenize >> 형태소분석, 불용어 제거)
3. get_intent (의도파악)
4. get_entity (개체명 인식)
5. scenario   (의도, 개체명 >> 크롤링 >> 결과출력)

<br>
<br>

### cdh_scenario.py
- 크롤링 실행 소스

1. intent 확인 후 맞는 카테고리 메소드 실행
2. 테그 분리 후 크롤링 실행

<br>
<br>

### flaskrestful.py
- flask_restful api 사용
- POST방식으로 온 json 데이터를 파싱 후 훈련된 모델에 넣어 결과값 예측, POST 방식으로 클라이언트에게 결과값 전달

<br>
<br>
<br>
<br>

# 실행방법 (구현중) -- 10/11
<br>

1. configs 파일 root_path 수정 (경로 다를 경우)
2. model_configs 파일 root_path 수정 (경로 다를 경우)
3. flaskrestful.py 실행 (ip수정필요)
4. 클라이언트에서 질문입력, 결과출력

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
<br>

##### application 수정
##### crawler 파일 추가
##### scenario 파일 추가
##### config 파일 수정
<br>

<br>
<br>
<br>

# 수정 -- 10/07
- application [get_intent(○), get_entity(×), scenario(△)]
- tokenizer
- preprocess
- cdh_intent
- configs
- model_configs
- crawler_configs
- flaskrestful (main)
- cdh_scenario
- crawler_restaurant
- crawler_weather
- crawler_dust
- crawler_travel
- crawler(seoul_cralwer, busan_cralwer, parsing_test)
<br>
<br>

##### crawler_travel 파일 추가
##### seoul, busan crawler 파일 추가
##### scenario 파일 수정
##### crawler_config 파일 추가
##### flaskrestful 파일 수정 (post 포맷 변경)
<br>

<br>
<br>
<br>

# 수정 -- 10/10
- application [get_intent(○), get_entity(○), scenario(△)]
- tokenizer
- preprocess
- cdh_intent
- configs
- model_configs
- crawler_configs
- flaskrestful (main)
- cdh_scenario
- crawler_restaurant
- crawler_weather
- crawler_dust
- crawler_travel
- crawler(seoul, busan, incheon, parsing_test, hwaseong, suwon, ganghwa, gyeongju, gangwon, jeju, jeonju)
<br>
<br>

##### crawler_travel 파일 수정
##### hwaseong, suwon, ganghwa, gyeongju, gangwon, jeju, jeonju crawler 파일 추가
##### scenario 파일 수정
##### cdh_intent 파일 수정 (fallback 처리)
##### application 파일 수정 (fallback 처리)
<br>

<br>
<br>
<br>

# 수정 -- 10/11
- application [get_intent(○), get_entity(○), scenario(△)]
- tokenizer
- preprocess
- cdh_intent
- configs
- model_configs
- crawler_configs
- flaskrestful (main)
- cdh_scenario
- crawler_restaurant
- crawler_weather
- crawler_dust
- crawler_travel
- crawler(seoul, busan, incheon, parsing_test, hwaseong, suwon, ganghwa, gyeongju, gangwon, jeju, jeonju)
<br>
<br>

##### crawler_travel 파일 수정 (예외처리)
##### crawler_configs 파일 수정 (도시목록 추가)
##### crawler_restaurant 파일 수정 (예외처리)
##### crawler_dust 파일 수정 (크롤링 수정)
##### application 파일 수정 (fallback 처리)
<br>

<br>
<br>
<br>

# 수정 -- 10/14
- application [get_intent(○), get_entity(○), scenario(△)]
- tokenizer
- preprocess
- cdh_intent
- jbh_entity
- configs
- model_configs
- crawler_configs
- flaskrestful (main)
- cdh_scenario
- crawler_restaurant
- crawler_weather
- crawler_dust
- crawler_travel
- crawler(seoul, busan, incheon, parsing_test, hwaseong, suwon, ganghwa, gyeongju, gangwon, jeju, jeonju)
<br>
<br>

##### crawler_travel 파일 수정 (check_purpose 함수 수정)
##### crawler_configs 파일 수정 (도시목록 추가)
<br>

<br>
<br>
<br>

# 수정 -- 10/15
- application [get_intent(○), get_entity(○), scenario(○), seq2seq(○)]
- tokenizer
- preprocess
- cdh_intent
- jbh_entity
- configs
- model_configs
- crawler_configs
- flaskrestful (main)
- cdh_scenario
- crawler_restaurant
- crawler_weather
- crawler_dust
- crawler_travel
- crawler_attraction
- crawler(seoul, busan, incheon, parsing_test, hwaseong, suwon, ganghwa, gyeongju, gangwon, jeju, jeonju, attraction, hanatour, festival)
- ljs_sqe2sqe
- util(constants, response, spell_checker, speel_dict.csv)
<br>
<br>

##### flaskrestful 파일 수정 (slot 처리)
##### application 파일 수정 (slot 처리, fallback-seq2seq 처리)
##### cdh_scenario 파일 수정 (slot 처리, attraction 추가)
##### crawler_* 파일 수정 (에러처리 [try-except])
##### crawler 파일 추가 (attraction, hanatour, festival)
##### crawler_configs 파일 수정 (하나투어 관광지 추가)
##### model_configs 파일 수정 (seq2seq 모델불러오기 추가)
##### ljs_seq2seq 파일 추가 (seq2seq[잡담-fallback 처리])
##### util폴더 추가 (토큰화 후 스펠링 체크&수정)
<br>

<br>
<br>
<br>

# 수정 -- 10/17
- application [get_intent(○), get_entity(○), scenario(○), seq2seq(○)]
- tokenizer
- preprocess
- cdh_intent
- jbh_entity
- configs
- model_configs
- crawler_configs
- flaskrestful (main)
- cdh_scenario
- crawler_restaurant
- crawler_weather
- crawler_dust
- crawler_travel
- crawler_attraction
- crawler(seoul, busan, incheon, parsing_test, hwaseong, suwon, ganghwa, gyeongju, gangwon, jeju, jeonju, attraction, hanatour, festival)
- ljs_sqe2sqe
- util(constants, response, spell_checker, speel_dict.csv)
<br>
<br>

##### flaskrestful 파일 수정 (slot 처리, welcom class 추가)
##### cdh_scenario 파일 수정 (slot 처리)
##### crawler_configs 파일 수정 (여행지 리스트 추가)
##### configs 파일 수정 (welcom 메세지 추가)
##### spell_dict 파일 수정 (오타사전 데이터 추가)
<br>