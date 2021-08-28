from flask import Flask, request, abort
import pya3rt
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YodoBhoFKf039maxY4sLH47U31DLdunlYr/ejWDCBIOfQKmgGFolxEMfY0Ovy1eSp06poHHLE6zIJP0DH423L79iXhnxa1+6Lhv4cejohkfSt5Z8FaNqXO0EjbgJfN2emZhHlgKBo3dZnkW2DTX77gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6dacdd52abcb583f7dc0be0bd66ecf21')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # リプライを作成する
    reply = create_reply(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        # 実際にcreate_replyの返り値をTextMessageの引数として渡してます。
        TextSendMessage(text=reply))

def create_reply(user_text):
  apikey = "DZZE2RrQsXik7q0ZUQHtCFiHYZqQWUzB"
  client = pya3rt.TalkClient(apikey)
  res = client.talk(user_text)

  return res['results'][0]['reply']

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    app.run()