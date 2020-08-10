from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv

from controller.liff_controller import LiffController

load_dotenv()

from controller.line_controller import LineController
from controller.notify_controller import CallbackController, RootController, AuthLinkController

app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_resource(RootController, "/notify")
api.add_resource(AuthLinkController, "/notify/link")
api.add_resource(LineController, '/webhooks/line')
api.add_resource(CallbackController, '/notify/callback')
api.add_resource(LiffController, '/liff/air')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
