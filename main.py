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
VehicleDispatchKind=0

def VehicleDispatchFg_now():
    global VehicleDispatchFg
    return VehicleDispatchFg

def VehicleDispatchCheck():
    Fg = VehicleDispatchFg_now()
    if Fg ==1:
        return True
    else:
        return False

def SetElseStr():
    wkStr = ""
    if VehicleDispatchKind == 0:
        wkStr = "現在は配車のオプション選択待ちです。\n１：車イス対応\n２：ストレッチャー対応\n３：マイクロバス\nからオプションをコメントして下さい。"
    elif VehicleDispatchKind == 1:
        wkStr = "現在はアイネット交通株式会社へ配車依頼中です。\nもうしばらくお待ち下さい。"
    elif VehicleDispatchKind == 2:
        wkStr = "現在はINET交通　株式会社へ配車依頼中です。\nもうしばらくお待ち下さい。"
    elif VehicleDispatchKind == 3:
        wkStr = "現在はあいねっと交通株式会社へ配車依頼中です。\nもうしばらくお待ち下さい。"

    return wkStr

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
    USER_ID = "U96671e7042e3f7fc2efee15b6c7f840f"
    KAIGO_USER_ID = "U409026962871bf8786172850baa56f62"
    global VehicleDispatchFg
    global VehicleDispatchKind
    #　メッセージは "event.message.text" という変数に格納される
    if event.source.user_id == KAIGO_USER_ID and event.message.text =="1":
        wkStr1 = ""
        wkStr2 = ""
        if VehicleDispatchKind == 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="現在このボタンは受け付けていません。")
            )            
        elif VehicleDispatchKind == 1:
            wkStr1 = "おまたせ致しました。\nアイネット交通株式会社からの配車が確定しました。"
            wkStr2 = "到着地：東京都大田区蒲田5-37-1\n車種：車イス対応タクシー"
            messages = TextSendMessage(text=wkStr1)
            line_bot_api.push_message(USER_ID, messages=messages)
            messages = TextSendMessage(text=wkStr2)
            line_bot_api.push_message(USER_ID, messages=messages)
            VehicleDispatchKind=0
            VehicleDispatchFg=0
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="対応可能な旨を返信しました。")
            )
        elif VehicleDispatchKind == 2:
            wkStr1 = "おまたせ致しました。\nINET交通　株式会社からの配車が確定しました。"
            wkStr2 = "到着地：東京都大田区蒲田5-37-1\n車種：ストレッチャー対応タクシー"
            messages = TextSendMessage(text=wkStr1)
            line_bot_api.push_message(USER_ID, messages=messages)
            messages = TextSendMessage(text=wkStr2)
            line_bot_api.push_message(USER_ID, messages=messages)
            VehicleDispatchKind=0
            VehicleDispatchFg=0
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="対応可能な旨を返信しました。")
            )
        elif VehicleDispatchKind == 3:
            wkStr1 = "おまたせ致しました。\nあいねっと交通株式会社からの配車が確定しました。"
            wkStr2 = "到着地：東京都大田区蒲田5-37-1\n車種：マイクロバス"
            messages = TextSendMessage(text=wkStr1)
            line_bot_api.push_message(USER_ID, messages=messages)
            messages = TextSendMessage(text=wkStr2)
            line_bot_api.push_message(USER_ID, messages=messages)
            VehicleDispatchKind=0
            VehicleDispatchFg=0
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="対応可能な旨を返信しました。")
            )
    elif event.source.user_id == KAIGO_USER_ID and event.message.text =="2" and VehicleDispatchKind != 0:
        messages = TextSendMessage(text="申し訳ございません。現在対応可能なタクシーはございません。\nしばらくして再度申し込み下さい。")
        line_bot_api.push_message(USER_ID, messages=messages)
        VehicleDispatchKind=0
        VehicleDispatchFg=0  
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="現在対応ができない旨をお伝えしました。")
        )
    elif event.source.user_id == KAIGO_USER_ID and event.message.text =="2" and VehicleDispatchKind == 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="現在このボタンは受け付けていません。")
            )          
    elif event.source.user_id != KAIGO_USER_ID and event.message.text == "配車依頼" and VehicleDispatchCheck()==False:
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
    elif event.source.user_id != KAIGO_USER_ID and VehicleDispatchCheck():
        profile = line_bot_api.get_profile(event.source.user_id)

        if event.message.text == "1":
            VehicleDispatchKind = 1
            messages = TextSendMessage(text=profile.display_name + "様から配車依頼がありました。\n車イス対応車を希望です。")
            line_bot_api.push_message(KAIGO_USER_ID, messages=messages)
            messages = TextSendMessage(text="対応可否を番号でご選択下さい。\n１：対応可能\n２：対応不可")
            line_bot_api.push_message(KAIGO_USER_ID, messages=messages)

            text = "アイネット交通株式会社へ依頼中です。\nしばらくお待ち下さい。"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )
        elif event.message.text == "2":
            VehicleDispatchKind = 2
            messages = TextSendMessage(text=profile.display_name + "様から配車依頼がありました。\nストレッチャー対応車を希望です。")
            line_bot_api.push_message(KAIGO_USER_ID, messages=messages)
            messages = TextSendMessage(text="対応可否を番号でご選択下さい。\n１：対応可能\n２：対応不可")
            line_bot_api.push_message(KAIGO_USER_ID, messages=messages)            
            text = "INET交通　株式会社へ依頼中です。\nしばらくお待ち下さい。"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )
        elif event.message.text == "3":
            VehicleDispatchKind = 3
            messages = TextSendMessage(text=profile.display_name + "様から配車依頼がありました。\nマイクロバスを希望です。")
            line_bot_api.push_message(KAIGO_USER_ID, messages=messages)
            messages = TextSendMessage(text="対応可否を番号でご選択下さい。\n１：対応可能\n２：対応不可")
            line_bot_api.push_message(KAIGO_USER_ID, messages=messages)    
            text = "あいねっと交通株式会社へ依頼中です。\nしばらくお待ち下さい。"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )
        elif event.message.text == "キャンセル":
            text = "配車の手配をキャンセルしました。\nまたのご利用をお待ちしております。"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )
            VehicleDispatchFg = 0
            VehicleDispatchKind = 0
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=SetElseStr())
            )        
    elif event.message.text == "あ":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.source.user_id)
            )
    elif event.source.user_id == KAIGO_USER_ID:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="このボタンは利用できません。")
            )        
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="現在は何も受付おりません。")
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