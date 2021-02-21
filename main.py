
from flask import Flask, request
import random, json, requests
import pandas as pd
import random
import os
import sys

# line libray
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, StickerSendMessage,ImageSendMessage)

#ユーザ区分[0:タクシー会社、1:依頼者]
dicUsrKbn={'U7bb673b5d4a90c19698ef689b421985e':1,
           'U409026962871bf8786172850baa56f62':0}
#申請状況を管理[0:配車依頼中、1:オプション選択中、2:車イス対応返信待ち、
#　　　　　　　 3:ストレッチャー対応返信待ち、4:マイクロバス返信街、9:現在処理中]
dicStatus={}

#名前を取得する
dicGetName={}

#タクシー会社の返信状況を管理[0:未処理、9:処理中]
dicTaxiStatus={'U409026962871bf8786172850baa56f62':0}

#メッセージを返信します。
def replyMessage(event,msg):
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=msg)
    )

#依頼者へメッセージを返信します。
def pushMessage(userId,msg):
    messages = TextSendMessage(text=msg)
    line_bot_api.push_message(userId, messages=messages)


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
    if event.message.text == "ユーザ":
        replyMessage(event,event.source.user_id)

    #リクエストのあったユーザの区分を取得
    usrKbn=dicUsrKbn.get(event.source.user_id,-1)
    #ディクショナリーになかったときは、依頼者として追加する
    if usrKbn==-1:
        dicUsrKbn[event.source.user_id]=1
        usrKbn=1
    
    #現在タクシー会社が処理中ではないことを確認する。
    if dicTaxiStatus[event.source.user_id]==9:
        replyMessage(event,"現在処理中です。")
        sys.exit()

    #タクシー会社の場合
    if usrKbn==0:
        replyFG = False
        #依頼者に申請中のステータスがある場合、配車を受け付けた旨を返信する。
        if event.message.text == "1":
            for key in dicStatus:
                if dicStatus[key]==2:
                    #依頼者へ受け付けた旨を返信する
                    pushMessage(key,"おまたせ致しました。\nアイネット交通株式会社からの配車が確定しました。")
                    pushMessage(key,"到着地：東京都大田区蒲田5-37-1\n車種：車イス対応タクシー")
                    #タクシー会社へマッチングした旨を返信する
                    replyMessage(event,dicGetName[key] + '様の配車依頼を受付ました。')
                    replyFG = True
                elif dicStatus[key]==3:
                    #依頼者へ受け付けた旨を返信する
                    pushMessage(key,"おまたせ致しました。\nINET交通　株式会社からの配車が確定しました。")
                    pushMessage(key,"到着地：東京都大田区蒲田5-37-1\n車種：ストレッチャー対応タクシー")
                    #タクシー会社へマッチングした旨を返信する
                    replyMessage(event,dicGetName[key] + '様の配車依頼を受付ました。')
                    replyFG = True
                elif dicStatus[key]==4:
                    #依頼者へ受け付けた旨を返信する
                    pushMessage(key,"おまたせ致しました。\nあいねっと交通株式会社からの配車が確定しました。")
                    pushMessage(key,"到着地：東京都大田区蒲田5-37-1\n車種：マイクロバス")
                    #タクシー会社へマッチングした旨を返信する
                    replyMessage(event,dicGetName[key] + '様の配車依頼を受付ました。')
                    replyFG = True

        #依頼者に申請中のステータスがある場合、配車を受け付けられなかった旨を返信する。
        elif event.message.text == "2":
            for key in dicStatus:
                if dicStatus[key]==2 or dicStatus[key]==3 or dicStatus[key]==4:
                    #対応不可のメッセージを依頼者へ返信する
                    pushMessage(key,"申し訳ございません。現在対応可能なタクシー会社はございません。")
                    #申請状況ディクショナリーからキーを削除する
                    del dicStatus[key]
                    replyFG = True
        else:
            replyMessage(event,'このボタンは受け付けていません') 
            sys.exit()
            
        #一つでも返信があった場合と一つも返信がなかった場合で処理を分ける
        if replyFG==False:
            replyMessage(event,'現在返信待ちの依頼はありませんでした')           

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

