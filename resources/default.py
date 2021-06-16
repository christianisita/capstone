from flask_restful import Resource

class DefaultEndpoint(Resource):
    def get(self):
        return {
            "success": "True",
            "message": "Hello World, this is default endpoint"
        }

