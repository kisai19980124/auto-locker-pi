import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)

gp_in_blue = 24
gp_in_red = 25
GPIO.setup(gp_in_blue, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(gp_in_red, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO4を制御パルスの出力に設定
gp_out = 4
GPIO.setup(gp_out, GPIO.OUT)

#「GPIO4出力」でPWMインスタンスを作成する。
#GPIO.PWM( [ピン番号] , [周波数Hz] )
#SG92RはPWMサイクル:20ms(=50Hz), 制御パルス:0.5ms〜2.4ms, (=2.5%〜12%)。
servo = GPIO.PWM(gp_out, 50)

#パルス出力開始。　servo.start( [デューティサイクル 0~100%] )
#とりあえずゼロ指定だとサイクルが生まれないので特に動かないっぽい？
servo.start(0)
#time.sleep(1)

def servo_angle(angle):
    duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
    servo.ChangeDutyCycle(duty)     #デューティ比を変更
    time.sleep(0.5)                 #0.5秒間待つ

deg = 0
servo_angle(deg)                     #サーボモータを変数"deg"の角度に動作

while True:
    try:
        if(GPIO.input(gp_in_blue) == 1):    #GPIO24が"1"であれば以下を実行
            deg = 90                         #変数"deg"に90を格納
            servo_angle(deg)                     #サーボモータを変数"deg"の角度に動作
            deg = 0                         #変数"deg"に0を格納
            servo_angle(deg)                     #サーボモータを変数"deg"の角度に動作
        if(GPIO.input(gp_in_red) == 1):  #GPIO25が"1"であれば以下を実行
            deg = -90                        #変数"deg"に-90を格納
            servo_angle(deg)                     #サーボモータを変数"deg"の角度に動作
            deg = 0                        #変数"deg"に0を格納
            servo_angle(deg)                     #サーボモータを変数"deg"の角度に動作
    except KeyboardInterrupt:                #Ctrl+Cキーが押された
        Servo.stop()                         #サーボモータをストップ
        GPIO.cleanup()                       #GPIOをクリーンアップ
        sys.exit()                           #プログラムを終了


servo.stop()
GPIO.cleanup()