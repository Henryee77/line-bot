from langdetect import detect
import translators as ts

lang_target = {'en': 'zh-Hant', 'zh-tw': 'en', 'zh-cn': 'en', 'ko': 'en', 'ja': 'en'}

while True:
  msg = input()
  print(detect(msg))
  print(ts.translate_text(query_text=msg,
                          to_language=lang_target.get(detect(msg), 'zh-Hant')))
