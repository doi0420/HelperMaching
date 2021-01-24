from flask import Flask, request
import random, json, requests
import pandas as pd
import gspread
import json
import os

from oauth2client.service_account import ServiceAccountCredentials
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

# def connect_gspread(jsonf,key):
#     scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
#     gc = gspread.authorize(credentials)
#     SPREADSHEET_KEY = key
#     worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
#     return worksheet

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
    USER_ID = "U7bb673b5d4a90c19698ef689b421985e"
    global VehicleDispatchFg
    global VehicleDispatchKind
    path = os.path.dirname(os.path.abspath(__file__)) + "/"
    jsonf = path + "helpermaching-9f5798e53f3c.json"
    # spread_sheet_key = "1mFmBA6wC_YFOy_47nrJboLFfgKnBmUhPL6-XAXOUYNM"
    # ws = connect_gspread(jsonf,spread_sheet_key)

    #　メッセージは "event.message.text" という変数に格納される
    if event.message.text == "配車依頼":
        VehicleDispatchStr1 = "配車を手配致します。"
        VehicleDispatchStr2 = "ご希望の車種を番号でご選択下さい。\n１：車イス対応\n２：ストレッチャー対応\n３：マイクロバス"
        VehicleDispatchFg = 1
        #ws.update_cell(1,1,event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=VehicleDispatchStr1),
                TextSendMessage(text=VehicleDispatchStr2)
            ]
        )
    elif VehicleDispatchCheck():
        profile = line_bot_api.get_profile(event.source.user_id)
    
        if event.message.text == "1":
            VehicleDispatchKind = 1
            messages = TextSendMessage(text=profile.display_name + "様から配車依頼がありました。\n車イス対応車を希望です。")
            line_bot_api.push_message(USER_ID, messages=messages)
            text = "アイネット交通株式会社へ依頼中です。\nしばらくお待ち下さい。"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )
        elif event.message.text == "2":
            VehicleDispatchKind = 2
            messages = TextSendMessage(text=profile.display_name + "様から配車依頼がありました。\nストレッチャー対応車を希望です。")
            line_bot_api.push_message(USER_ID, messages=messages)
            text = "INET交通　株式会社へ依頼中です。\nしばらくお待ち下さい。"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )
        elif event.message.text == "3":
            VehicleDispatchKind = 3
            messages = TextSendMessage(text=profile.display_name + "様から配車依頼がありました。\nマイクロバスを希望です。")
            line_bot_api.push_message(USER_ID, messages=messages)
            text = "あいねっと交通株式会社へ依頼中です。\nしばらくお待ち下さい。"
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
        elif event.message.text == "キャンセル":
            text = "配車の手配をキャンセルしました。\nまたのご利用をお待ちしております。"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=jsonf)
            )
            VehicleDispatchFg = 0
            VehicleDispatchKind = 0
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=SetElseStr())
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
# [END gae_python37_app]
