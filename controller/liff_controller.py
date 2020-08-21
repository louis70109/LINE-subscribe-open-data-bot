import os
from flask import request, render_template, Response
from flask_restful import Resource

from utils.db import find_site
from utils.flex import county_flex_template

AIR_ID = os.getenv('LIFF_SHARE_ID')
AIR_LIFF = f"https://liff.line.me/{AIR_ID}"


class LiffController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        if request.args.get('liff.state'):
            return Response(render_template('liff_redirect.html', liff_id=AIR_ID))
        site = request.args.get('site')
        if site:
            import urllib.parse as parser
            site = parser.unquote(site)
            row = find_site(site)
            flex = county_flex_template(
                county=row['county'],
                site=row['site_name'],
                status=row['status'],
                update_time=row['update_time'])

            msg = {"type": "flex", "altText": "空汙狀態", "contents": {**flex}}
            return Response(render_template('share_message.html', flex=msg, liff_id=AIR_ID))
