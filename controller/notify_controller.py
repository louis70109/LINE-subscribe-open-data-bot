import os
import uuid

from flask import request, render_template
from flask_restful import Resource
from lotify.client import Client

CLIENT_ID = os.getenv('LINE_NOTIFY_CLIENT_ID')
SECRET = os.getenv('LINE_NOTIFY_CLIENT_SECRET')
URI = os.getenv('LINE_NOTIFY_REDIRECT_URI')

"""
If your keys are 
LINE_NOTIFY_CLIENT_ID, LINE_NOTIFY_CLIENT_SECRET, LINE_NOTIFY_REDIRECT_URI
you can drop them in Client() cause they are default environment name.
"""
lotify = Client(client_id=CLIENT_ID, client_secret=SECRET, redirect_uri=URI)


class RootController(Resource):
    def get(self):
        link = lotify.get_auth_link(state=uuid.uuid4())
        return render_template('notify_index.html', auth_url=link)


class CallbackController(Resource):
    def get(self):
        token = lotify.get_access_token(code=request.args.get('code'))
        return render_template('notify_confirm.html', token=token)


class LineNotifyhController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        pass
