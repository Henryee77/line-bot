# coding: utf-8
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from langdetect import detect
import translators as ts

app = Flask(__name__)


class LineBotHandler:
  def __init__(self):
    # line token
    channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
    channel_secret = os.environ['LINE_CHANNEL_SECRET']
    self.line_bot_api = LineBotApi(channel_access_token)
    self.handler = WebhookHandler(channel_secret)
    self.lang_target = {'en': 'zh-Hant', 'zh-tw': 'en', 'zh-cn': 'en', 'ko': 'en', 'ja': 'en'}

  def callback(self):
    app.route("/callback", methods=['POST'])
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
      self.handler.handle(body, signature)
    except InvalidSignatureError:
      abort(400)
    return 'OK'

  def handle_message(self, event: MessageEvent):
    self.handler.add(MessageEvent, message=TextMessage)
    # translate
    msg = str(event.message.text).strip()
    if msg == 'Word of the day':
      ts_text = 't1'
    elif msg == 'Phrase of the day':
      ts_text = 't2'
    else:
      ts_text = ts.translate_text(query_text=msg,
                                  to_language=self.lang_target.get(detect(msg), 'zh-Hant'))
    message = TextSendMessage(text=ts_text)
    self.line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  line_bot = LineBotHandler()
  app.run(host='0.0.0.0', port=port)
