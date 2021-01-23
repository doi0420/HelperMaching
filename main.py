from flask import Flask, request
import random, json, requests
import pandas as pd
import random


# line libray
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage,ImageSendMessage
)

import os

VehicleDispatchFg=0

def VehicleDispatchFg_now():
    global VehicleDispatchFg
    return VehicleDispatchFg

def VehicleDispatchCheck():
    Fg = VehicleDispatchFg_now()
    if Fg ==1:
        return True
    else:
        return False

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET       = os.environ["YOUR_CHANNEL_SECRET"]
STORAGE_BUCKET            = os.environ["STORAGE_BUCKET"]

app = Flask(__name__)

# LINE APIおよびWebhookの接続
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler      = WebhookHandler(YOUR_CHANNEL_SECRET)

# Flaskのルート設定
@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# メッセージ応答メソッド
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global VehicleDispatchFg
    #　メッセージは "event.message.text" という変数に格納される
    if event.message.text == "配車依頼":
        VehicleDispatchStr1 = "配車を手配致します。"
        VehicleDispatchStr2 = "ご希望の車種を番号でご選択下さい。\n１：車イス対応\n２：ストレッチャー対応\n３：マイクロバス"
        VehicleDispatchFg = 1
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=VehicleDispatchStr1),
                TextSendMessage(text=VehicleDispatchStr2)
            ]
        )
    elif event.message.text == "1" and VehicleDispatchCheck():
        text = "平和交通株式会社へ依頼中です。\nしばらくお待ち下さい。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    elif event.message.text == "2" and VehicleDispatchCheck():
        text = "フラワー交通　株式会社へ依頼中です。\nしばらくお待ち下さい。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    elif event.message.text == "3":
        profile = line_bot_api.get_profile(event.source.user_id)
        text = "三慶交通株式会社へ依頼中です。\nしばらくお待ち下さい。"
        user_id = "U7bb673b5d4a90c19698ef689b421985e"

        messages = TextSendMessage(text=profile.display_name + "様から配車依頼がありました。\nマイクロバスを希望です。")
        line_bot_api.push_message(user_id, messages=messages)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.source.user_id)
        )
    elif event.message.text == "キャンセル" and VehicleDispatchCheck():
        text = "配車の手配をキャンセルしました。\nまたのご利用をお待ちしております。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
        VehicleDispatchFg = 0
    elif event.message.text == "キャンセル" and VehicleDispatchCheck() == False:
        text = "現在は何も受付おりません。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        ) 
    elif event.message.text == "タクシー会社":
        TaxiListStr1 = "対応可能なタクシー会社です。"
        TaxiListStr2 = "https://www.taxisite.com/station/info/9931003.aspx"
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=TaxiListStr1),
                TextSendMessage(text=TaxiListStr2)
            ]
        )  
    else:
        messages = random.choice(["？？？","ワタシタクシーノテハイシカデキマセン","スタンプ"])
        if messages == "スタンプ":
            line_bot_api.reply_message(
                event.reply_token,
                StickerSendMessage(package_id=1 ,sticker_id=1)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=messages)
            )
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080))
    )
# [END gae_python37_app]
