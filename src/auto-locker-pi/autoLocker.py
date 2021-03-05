import RPi.GPIO as GPIO
import time
import sys
from util import servo, reader, LINENotifyBot
import os

# LINE BOT用のライブラリ
import paho.mqtt.client as mqtt
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import datetime        
        
class Locker(object):
    def __init__(self):
        
        #登録済みNFC IDの読み取り
        self.id_list = os.environ["NFC_ID"].split(":")

        #GPIOピンをプルダウン入力に設定
        self.gp_in_yellow = 16
        self.gp_in_red = 25
        self.gp_in_green = 24
        self.gp_in_blue = 23

        #GPIO4を制御パルスの出力に設定
        self.gp_out = 4

        self.if_open = True

        #LINE Notify用のアクセストークン
        access_token = os.environ["LINE_NOTIFY_KEY"]
        self.bot = LINENotifyBot(access_token=access_token)

        GPIO.setmode(GPIO.BCM)

        #アンロックピンのセットアップ
        GPIO.setup(self.gp_in_yellow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.gp_in_yellow, GPIO.RISING, callback=self.callback_open, bouncetime=1000)
        
        #ロックピンのセットアップ
        GPIO.setup(self.gp_in_red, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.gp_in_red, GPIO.RISING, callback=self.callback_close, bouncetime=1000)

        #補助ピンAのセットアップ
        GPIO.setup(self.gp_in_green, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.gp_in_green, GPIO.RISING, callback=self.callback_wait_lock, bouncetime=1000)

        #補助ピンBのセットアップ
        GPIO.setup(self.gp_in_blue, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.gp_in_blue, GPIO.RISING, callback=self.callback_donki, bouncetime=1000)

        #出力ピンのセットアップ
        GPIO.setup(self.gp_out, GPIO.OUT)
        servo(self.gp_out, GPIO, 0)

        # LINE BOT APIの設定
        self.wait = 0
        self.line_bot_api = LineBotApi(os.environ["YOUR_CHANNEL_ACCESS_TOKEN"])
        self.client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
        self.client.on_connect = self.on_connect         # 接続時のコールバック関数を登録
        self.client.on_disconnect = self.on_disconnect   # 切断時のコールバックを登録
        self.client.on_message = self.on_message         # メッセージ到着時のコールバック

        self.client.username_pw_set(os.environ["USERNAME_PW_SET"])
        self.client.tls_set(os.environ["TLS_SET"])
        self.client.connect(os.environ["CONNECT_URL"], 8883, 60)
        self.client.loop_start()

        self.send_line_msg('システムを起動するよ！')

    def exec(self):
        cr = reader(self.id_list)
        while True:
            try:
                self.client.on_message
               # cr.read_id()
                #if self.if_open:
                 #   self.callback_close(0)
                #else:
                  #  self.callback_open(0)
                if self.wait == 1:
                    self.callback_open(0)
                    self.wait = 0
                elif self.wait == 2:
                    self.callback_close(0)
                    self.wait = 0
            except KeyboardInterrupt: #Ctrl+Cキーが押して,
                GPIO.cleanup()        #GPIOをクリーンアップし，
                sys.exit()            #プログラムを終了
                self.send_line_msg('システムが終了しました')

    def callback_open(self, channel):
        servo(self.gp_out, GPIO, 90) #サーボモータを90度に動作
        servo(self.gp_out, GPIO, 0)  #サーボモータを0度に動作
        self.if_open = True
        self.send_line_msg('あけたよ！')
        #self.bot.send(message = "解錠しました")

    def callback_close(self, channel):
        servo(self.gp_out, GPIO, -90) #サーボモータを-90度に動作
        servo(self.gp_out, GPIO, 0)   #サーボモータを0度に動作
        self.if_open = False
        self.send_line_msg('しめたよ！')
        #self.bot.send(message = "施錠しました")

    def callback_costco(self, channel):
        self.send_line_msg('Costco行かね？')
        #self.bot.send(message = "Costco行かね？")

    def callback_donki(self, channel):
        self.send_line_msg('ドンキ行かね？')
        #self.bot.send(message = "ドンキ行かね？")

    def callback_wait_lock(self, channel):
        self.send_line_msg('5秒後に施錠します')
        #self.bot.send(message = "5秒後に施錠します")
        time.sleep(5)
        self.callback_close(0)

    # ブローカーに接続できたときの処理
    def on_connect(self, client, userdata, flag, rc):
        print('[autoLocker.py] Connected with result code ' + str(rc))  # 接続できた旨表示
        self.client.subscribe('Genkan_doa/raspie')  # subするトピックを設定 

    # ブローカーが切断したときの処理
    def on_disconnect(self, client, userdata, flag, rc):
        if  rc != 0:
            print('[autoLocker.py] Unexpected disconnection.')

    def send_line_msg(self, msg):
        self.line_bot_api.broadcast(TextSendMessage(text=msg))
            
    # メッセージが届いたときの処理
    def on_message(self, client, userdata, msg):
        get_msg = msg.payload.decode('utf-8')
        if get_msg == 'on':
            self.wait=1
        elif get_msg == 'off':
            self.wait=2


if __name__ == "__main__":
    locker = Locker()
    locker.exec()
