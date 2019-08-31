from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from controller.todos_controller import TodosController
app = Flask(__name__)
CORS(app)


api = Api(app)
api.add_resource(TodosController, '/todos')

if __name__ == '__main__':
    app.run(debug=True)
