from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from controller.line_controller import LineIconSwitchController

app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_resource(LineIconSwitchController, '/webhooks/line')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
