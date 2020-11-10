# -*- coding: utf-8 -*-
# Reference to https://qiita.com/undo0530/items/89540a03252e2d8f291b
# Run by Python 2.7.16

import binascii
import nfc
import time
from threading import Thread, Timer
import RPi.GPIO as GPIO
import os
id_list = os.environ["NFC_ID"].split(":")

# Suica待ち受けの1サイクル秒
TIME_cycle = 1.0
# Suica待ち受けの反応インターバル秒
TIME_interval = 0.2
# タッチされてから次の待ち受けを開始するまで無効化する秒
TIME_wait = 1

# NFC接続リクエストのための準備
# 212F(FeliCa)で設定
target_req_suica = nfc.clf.RemoteTarget("212F")
# 0003(Suica)
target_req_suica.sensf_req = bytearray.fromhex("0000030000")

#GPIO4を制御パルスの出力に設定
GPIO.setmode(GPIO.BCM)
gp_out = 4
GPIO.setup(gp_out, GPIO.OUT)
#「GPIO4出力」でPWMインスタンスを作成する。
#GPIO.PWM( [ピン番号] , [周波数Hz] )
#SG92RはPWMサイクル:20ms(=50Hz), 制御パルス:0.5ms〜2.4ms, (=2.5%〜12%)。
servo = GPIO.PWM(gp_out, 50)
#パルス出力開始。　servo.start( [デューティサイクル 0~100%] )
#とりあえずゼロ指定だとサイクルが生まれないので特に動かないっぽい？
servo.start(0)
time.sleep(0.5)
servo.ChangeDutyCycle(9.75)
time.sleep(0.5)

print 'Suica waiting...'
while True:
    # USBに接続されたNFCリーダに接続してインスタンス化
    clf = nfc.ContactlessFrontend('usb')
    # Suica待ち受け開始
    # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
    target_res = clf.sense(target_req_suica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)

    if target_res != None:

        tag = nfc.tag.activate(clf, target_res)
        tag.sys = 3

        #IDmを取り出す
        idm = binascii.hexlify(tag.idm)
        print 'Suica detected. idm = ' + idm

        print 'sleep ' + str(TIME_wait) + ' seconds'
        time.sleep(TIME_wait)

        if idm in id_list:
            print 'Suica ID is authenticated'
            servo.ChangeDutyCycle(5.25)
            time.sleep(0.5)
            servo.ChangeDutyCycle(9.75)
            time.sleep(0.5)

    #end if

    clf.close()

#end while

servo.stop()
GPIO.cleanup()