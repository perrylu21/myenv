from __future__ import unicode_literals
import os
from flask import Flask, request, jsonify, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser

import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
user_id = config.get('line-bot', 'user_id')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback1():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body1: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@app.route("/params", methods=['GET'])
def get_params():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    text_msg ="My name is " + name + " and I am " + str(age) + " years old" 
    try:
        line_bot_api.push_message(user_id,TextSendMessage(text=text_msg))
    except LineBotApiError as e:
        print("LineBot Error:{0}".format(e.message))
    return jsonify(message=text_msg)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        
        pretty_text = 'Happy New Year 2023,'
        pretty_text += event.message.text
        
        #for i in event.message.text:
        
        #    pretty_text += i
        #    pretty_text += random.choice(pretty_note)
    
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )

if __name__ == "__main__":
    app.run()