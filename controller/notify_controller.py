import os
from flask import request, render_template, Response, jsonify
from flask_restful import Resource
from lotify.client import Client

from utils.db import create_user_notify

CLIENT_ID = os.getenv('LINE_NOTIFY_CLIENT_ID')
SECRET = os.getenv('LINE_NOTIFY_CLIENT_SECRET')
URI = os.getenv('LINE_NOTIFY_REDIRECT_URI')
LIFF_BIND_ID = os.getenv('LIFF_BIND_ID')
LIFF_CONFIRM_ID = os.getenv('LIFF_CONFIRM_ID')

"""
If your keys are 
LINE_NOTIFY_CLIENT_ID, LINE_NOTIFY_CLIENT_SECRET, LINE_NOTIFY_REDIRECT_URI
you can drop them in Client() cause they are default environment name.
"""
lotify = Client()


class RootController(Resource):
    def get(self):
        return Response(render_template('index.html', liff_id=LIFF_BIND_ID))


class AuthLinkController(Resource):
    def post(self):
        data = request.get_json()
        user_id = data['state']
        link = lotify.get_auth_link(state=user_id)
        return jsonify({'link': link})


class CallbackController(Resource):
    def get(self):
        if request.args.get('liff.state'):
            return Response(render_template('liff_redirect.html', liff_id=LIFF_CONFIRM_ID))

        user_id = request.args.get('state')
        token = lotify.get_access_token(code=request.args.get('code'))
        create_user_notify(user_id, token)
        return Response(render_template('confirm.html', liff_id=LIFF_CONFIRM_ID))


class LineNotifyController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        pass
