# coding: utf-8
import os
import datetime
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from langdetect import detect
import translators as ts

app = Flask(__name__)
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
channel_secret = os.environ['LINE_CHANNEL_SECRET']
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
lang_target = {'en': 'zh-Hant', 'zh-tw': 'en', 'zh-cn': 'en', 'ko': 'en', 'ja': 'en'}
day_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
with open('vocabulary/Oxford 5000.txt', 'r') as f:
  words = f.readlines()
with open('vocabulary/09-conversational-phrases.txt', 'r') as f:
  phrases = f.readlines()


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
    abort(400)
  return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
  # translate
  msg = str(event.message.text).strip()
  if msg == 'Word of the day':
    msg = words[date_2_index() % len(words)].strip()
    ts_text = '每日一字: ' + msg + '  -  ' + ts.translate_text(query_text=msg, to_language='zh-Hant')
  elif msg == 'Phrase of the day':
    msg = phrases[date_2_index() % len(phrases)].strip()
    ts_text = '每日一句: ' + msg + '  -  ' + ts.translate_text(query_text=msg, to_language='zh-Hant')
  else:
    ts_text = ts.translate_text(query_text=msg,
                                translator='google',
                                to_language=lang_target.get(detect(msg), 'zh-Hant'))
  message = TextSendMessage(text=ts_text)
  line_bot_api.reply_message(event.reply_token, message)


def date_2_index():
  date = datetime.datetime.now()
  return (date.year * 365 + sum([day_in_months[m - 1] for m in range(1, date.month)]) + date.day)


if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
