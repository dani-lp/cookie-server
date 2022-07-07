from flask.views import MethodView

class UnitsAPI(MethodView):
    def get(self):
        return 'he'
    
    def post(self):
        return 'hi'
