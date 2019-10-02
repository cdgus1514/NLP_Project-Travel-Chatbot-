from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import application as app
 
app = Flask(__name__)
api = Api(app)
 
 # 호출 메소드 생성
class RegistUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument("name", type=str)
        parser.add_argument("massage", type=str)
        args = parser.parse_args()

        # name = args["name"]
        massage = args["massage"]
        

        # 받아온 json 데이터 파싱
        req_data = request.get_json(force=True)
        pdata = req_data["massage"]
        # print("pdata >>", pdata)

        


        # return {'result': 'ok'}
        # return {"name":name, "massage":massage}
        return {"massage":massage}
 

 # URL과 메서드를 연결
api.add_resource(RegistUser, '/user')
 


if __name__ == '__main__':
    app.run(host="192.168.0.147")
