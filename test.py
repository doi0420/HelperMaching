from flask import Flask, request
import random, json, requests
import pandas as pd



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
    #　メッセージは "event.message.text" という変数に格納される
    if event.message.text == "配車依頼":
        text = "以下の内容で配車の手配します。\n・車椅子対応\n内容に問題ない場合は「はい」\内容に変更がある場合は「いいえ」とコメントしてください。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    elif event.message.text == "はい":
        text = "配車の手配をしました。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    elif event.message.text == "いいえ":
        text = "配車の手配をキャンセルしました。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    elif event.message.text == "空き病院":
        text = "・A病院\n・B病院\n・C病院\nが空いています。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    elif event.message.text == "タクシー":
        text = "利用可能なタクシー会社は\n・Dタクシー\n・Eタクシー\n・Fタクシー\nです。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )  
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
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