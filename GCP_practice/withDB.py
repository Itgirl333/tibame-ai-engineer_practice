#t.ly/_Ufz
import psycopg2

from flask import Flask, request, abort
import json
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os 

line_bot_api = LineBotApi("your channel access token")
handler = WebhookHandler("your channel secret")

app = Flask(__name__)
app.secret_key = os.urandom(20)


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

@handler.add(PostbackEvent)
def handle_postback(event):
    ts = event.postback.data
    print(ts)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    print(profile.display_name)
    
    #連線資料庫
    conn = psycopg2.connect(
        database="Product",
        password="You64310",
        user="postgres",
        host="127.0.0.1", 
        port="5432"
        )
    with conn:
        cur = conn.cursor()
        with cur:             
            #第一層 所有特價訊息
            if event.message.text=="所有特價訊息" :                
                message = TemplateSendMessage(
                    alt_text='圖文表單',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://www.agriharvest.tw/wp-content/uploads/2022/03/0-13-1024x768.jpg',
                        title='特價功能表',
                        text='本小店目前特價商品',
                        actions=[
                            MessageTemplateAction(
                                label='鳳梨特價',
                                text='鳳梨特價列表',                    
                            ),
                            MessageTemplateAction(
                                label='葡萄特價',
                                text='葡萄特價列表'
                            ),
                            MessageTemplateAction(
                                label='蘋果特價',
                                text='蘋果特價列表'
                            ),
                            URITemplateAction(
                                label='查看更詳細的優惠目錄',
                                uri='https://rtgo.rt-mart.com.tw/group1/M00/01/5E/rBUAEGCTnquAbQfkAAbwUHK1bMA497.jpg'
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, message )    
            
            #第二層 XX特價列表
            if event.message.text.find('特價列表')>=0:
                SalesListName=event.message.text[0:event.message.text.find('特價列表')]                
                cur = conn.cursor()
                cur.execute("SELECT *  from 產品 where 品名 like '%" + SalesListName + "'")
                rows = cur.fetchall()    
                msg=[]
                for row in rows:
                    msg =msg + [
                        MessageTemplateAction(
                                label=row[0] + ' $' + str(row[2]),
                                text=row[0] +'特價商品',                    
                            )]                    

                msg = msg + [MessageTemplateAction(
                                label='返回目錄',
                                text='所有特價訊息'
                            )]
                
                message = TemplateSendMessage(
                    alt_text='圖文表單',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://img.shoplineapp.com/media/image_clips/60a75b39cdd676002ce9c496/original.jpg?1621580601',
                        title='特價功能表',
                        text= SalesListName + '特價',
                        actions=msg
                    )
                )

                line_bot_api.reply_message(event.reply_token,message )    
        
            #第三層 XX特價商品
            if event.message.text.find('特價商品')>=0:
                SaleProductName=event.message.text[0:event.message.text.find('特價商品')]
                cur = conn.cursor()
                cur.execute("SELECT *  from 產品 where 品名 like '%" + SaleProductName + "'")
                rows = cur.fetchall()
                for row in rows:
                   SaleProductPrice=row[2]
                   SaleProcuctQty=row[1]                   

                message = TemplateSendMessage(
                    alt_text='確認購買',
                    template=ConfirmTemplate(                        
                        text='購買' + SaleProductName + '\r\n售價：' + str(SaleProductPrice) + '\r\n庫存量：' + str(SaleProcuctQty),
                        actions=[                              
                                MessageTemplateAction(
                                    label='購買',
                                    text='購買' + SaleProductName,
                                ),
                                MessageTemplateAction(
                                    label='否，返回',
                                    text='所有特價訊息'
                                )                            ]
                        )
                    )
                line_bot_api.reply_message(event.reply_token,message)
            
            #第四層 加入購物車
            if event.message.text.find('購買')>=0:
                BuyProductName=event.message.text[2:]                
                #存入資料庫
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO 訂單(品名,訂購人) VALUES (%s, %s)",
                    (BuyProductName, profile.display_name))

                #顯示購物清單
                cur = conn.cursor()
                cur.execute("SELECT * from 購買清單 where 訂購人='" + profile.display_name + "'")
                rows = cur.fetchall()
                
                msg ="你已購買：\r\n" 
                for row in rows:
                    msg = msg +  row[0] + ',單價：' + str(row[1]) + ',小計：' + str(row[1]) + '\r\n'
                
                message = TemplateSendMessage(
                    alt_text='購物清單',
                    template=ConfirmTemplate(                        
                        text=msg,
                        actions=[                              
                                MessageTemplateAction(
                                    label='付款',
                                    text='付款',
                                ),
                                MessageTemplateAction(
                                    label='否，刪除',
                                    text='刪除'
                                )                            ]
                        )
                    )
                line_bot_api.reply_message(event.reply_token,message)

            #第五層 刪除
            if event.message.text.find('刪除')>=0:
                cur = conn.cursor()
                sql="delete from 訂單 where 訂購人='" + profile.display_name + "'"
                print(sql)
                cur.execute(sql)                
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='購物車已經清空') )
            
            #第五層 付款
            if event.message.text.find('付款')>=0:                
                #顯示購物清單
                payUrl=getCheck()
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=payUrl))
                #產生付款網址


            #查看購物車                
            if event.message.text.find('購物車')>=0:
                cur = conn.cursor()
                cur.execute("SELECT * from 購買清單 where 訂購人='" + profile.display_name + "'")
                rows = cur.fetchall()
                
                msg ="你已購買：\r\n" 
                for row in rows:
                    msg = msg +  row[0] + ',單價：' + str(row[1]) + ',小計：' + str(row[1]) + '\r\n'
                
                message = TemplateSendMessage(
                    alt_text='購物清單',
                    template=ConfirmTemplate(                        
                        text=msg,
                        actions=[                              
                                MessageTemplateAction(
                                    label='付款',
                                    text='付款',
                                ),
                                MessageTemplateAction(
                                    label='否，刪除',
                                    text='刪除'
                                )                            ]
                        )
                    )
                line_bot_api.reply_message(event.reply_token,message)
#付款網址
def getCheck(amount):
    import requests
    import json
    # put the ip address or dns of your apic-em controller in this url
    url = "https://sandbox-api-pay.line.me/v2/payments/request"

    #Content type must be included in the header
    header = {"Content-Type":"application/json","X-LINE-ChannelId":"1657280313","X-LINE-ChannelSecret":"e89f1b5fea4b0b902e20c95829bce8e7"}
    #the username and password to access the APIC-EM Controller
    payload = {"amount": amount,
    "currency": "TWD", 
    "productName": "各式水果一批",
    "productImageUrl": "https://cimg.cnyes.cool/prod/news/4556115/l/79b7b76238dcaa28d626ec007bff576f.jpg",
    "confirmUrl": "http://127.0.0.1:3000",
    "orderId": "Order202203110011"}



    #Performs a POST on the specified url to get the service ticket
    response= requests.post(url,data=json.dumps(payload), headers=header, verify=False)

    #convert response to json format
    r_json=response.json()

    #parse the json to get the service ticket
    print(r_json['info']['paymentUrl']['web'])
    return r_json['info']['paymentUrl']['web']

if __name__ == "__main__":
    app.run()


