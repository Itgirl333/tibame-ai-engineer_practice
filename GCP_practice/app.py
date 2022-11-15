from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, ImageMessage
)


# 圖片下載與上傳專用
import urllib.request
import os

# 建立日誌紀錄設定檔
# https://googleapis.dev/python/logging/latest/stdlib-usage.html
import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud import storage
from google.cloud import firestore

# 啟用log的客戶端
client = google.cloud.logging.Client()


# 建立line event log，用來記錄line event
bot_event_handler = CloudLoggingHandler(client,name="cxcxc_bot_event")
bot_event_logger=logging.getLogger('cxcxc_bot_event')
bot_event_logger.setLevel(logging.INFO)
bot_event_logger.addHandler(bot_event_handler)


app = Flask(__name__)
line_bot_api = LineBotApi("your channel access token")
handler = WebhookHandler("your channel secret")


# 設定機器人訪問入口
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    # 消息整個交給bot_event_logger，請它傳回GCP
    bot_event_logger.info(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 當用戶收到文字消息的時候，回傳用戶講過的話
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 請line_bot_api回應，回應用戶講過的話
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


@handler.add(FollowEvent)
def handle_follow_event(event):
    # 取個資
    line_user_profile= line_bot_api.get_profile(event.source.user_id)

    # 跟line 取回照片，並放置在本地端
    file_name = line_user_profile.user_id + '.jpg'
    urllib.request.urlretrieve(line_user_profile.picture_url, file_name)

    # 設定內容
    storage_client = storage.Client()
    bucket_name="linebot-tibame01-storage"
    destination_blob_name=f"{line_user_profile.user_id}/user_pic.png"
    source_file_name=file_name
    
    # 進行上傳
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    # 設定用戶資料json
    user_dict={
        "user_id":line_user_profile.user_id,
        "picture_url": f"https://storage.googleapis.com/{bucket_name}/destination_blob_name",
        "display_name": line_user_profile.display_name,
        "status_message": line_user_profile.status_message
    }
    # 插入firestore
    db = firestore.Client()
    doc_ref = db.collection(u'line-user').document(user_dict.get("user_id"))
    doc_ref.set(user_dict)

    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text="個資已取"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))