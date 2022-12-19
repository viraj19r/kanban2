from flask_restful import Resource,Api
from application import app
api = Api(app)
#test api
class hello(Resource):
    def get(self):
        return {"data": "Hello Viraj"}

api.add_resource(hello,"/api/viraj")
