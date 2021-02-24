import RPi.GPIO as GPIO
import time
import sys
from util import servo, reader, LINENotifyBot
import os

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
        GPIO.add_event_detect(self.gp_in_green, GPIO.RISING, callback=self.callback_costco, bouncetime=1000)

        #補助ピンBのセットアップ
        GPIO.setup(self.gp_in_blue, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.gp_in_blue, GPIO.RISING, callback=self.callback_donki, bouncetime=1000)

        #出力ピンのセットアップ
        GPIO.setup(self.gp_out, GPIO.OUT)
        servo(self.gp_out, GPIO, 0)

    def exec(self):
        cr = reader(self.id_list)
        while True:
            try:
                #最初に表示 
                print("Please Touch")
        
                #タッチ待ち 
                cr.read_id()
        
                #リリース時の処理 
                print("【 Released 】")
                if self.if_open:
                    self.callback_close(0)
                else:
                    self.callback_open(0)

            except KeyboardInterrupt: #Ctrl+Cキーが押された
                GPIO.cleanup()        #GPIOをクリーンアップ
                sys.exit()            #プログラムを終了

    def callback_open(self, channel):
        servo(self.gp_out, GPIO, 90) #サーボモータを90度に動作
        servo(self.gp_out, GPIO, 0)  #サーボモータを0度に動作
        self.if_open = True

    def callback_close(self, channel):
        servo(self.gp_out, GPIO, -90) #サーボモータを-90度に動作
        servo(self.gp_out, GPIO, 0)   #サーボモータを0度に動作
        self.if_open = False

    def callback_costco(self, channel):
        self.bot.send(message = "Costco行かね？")

    def callback_donki(self, channel):
        self.bot.send(message = "ドンキ行かね？")

if __name__ == "__main__":
    locker = Locker()
    locker.exec()