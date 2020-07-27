import os

from flask import request
from flask_restful import Resource, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import FlexSendMessage, MessageEvent, TextMessage, \
    CarouselContainer, TextSendMessage, QuickReply, QuickReplyButton, MessageAction

from utils.common import routing
from utils.db import find_sites, create_user_site, remove_user_site, find_counties
from utils.flex import create_county_flex, counties_template

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


class LineController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        body = request.get_data(as_text=True)
        signature = request.headers['X-Line-Signature']

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        return 'OK'

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        text = event.message.text
        user_id = event.source.user_id
        sub = routing('^訂閱\s+', text)
        cancel_sub = routing('^取消訂閱\s+', text)
        all_county = routing('所有縣市', text)
        if sub:
            create_user_site(user_id, sub)
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(
                    text=f'訂閱 {sub[1]} 成功！',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="所有縣市", text="所有縣市"))
                    ])
                )
            )
        elif cancel_sub:
            remove_user_site(user_id, cancel_sub)
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(
                    text=f'取消訂閱 {cancel_sub[1]} 完成...',
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="所有縣市", text="所有縣市"))
                    ])
                ))
        elif all_county:
            rows = find_counties()
            contents = counties_template(rows)
            message = FlexSendMessage(
                alt_text=event.message.text,
                contents=CarouselContainer(contents),
                quick_reply=QuickReply(items=[
                    QuickReplyButton(action=MessageAction(label="所有縣市", text="所有縣市"))
                ])
            )
            line_bot_api.reply_message(
                event.reply_token,
                messages=message
            )
        else:
            rows = find_sites(text)
            contents, flex_message = [], []
            for index in range(len(rows)):
                if (index + 1) % 10 == 0:
                    flex_message.append(FlexSendMessage(
                        alt_text=text,
                        contents=CarouselContainer(contents)
                    ))
                    contents = []
                else:
                    contents.append(create_county_flex(
                        line_id=user_id,
                        county=rows[index]['county'],
                        site=rows[index]['site_name'],
                        status=rows[index]['status'],
                        update_time=rows[index]['update_time']
                    ))
            flex_message.append(FlexSendMessage(
                    alt_text=text,
                    contents=CarouselContainer(contents),
                    quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="所有縣市", text="所有縣市"))
                    ])
                ))
            line_bot_api.reply_message(
                event.reply_token,
                messages=flex_message
            )
