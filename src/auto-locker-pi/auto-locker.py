import RPi.GPIO as GPIO
import time
import sys
from util import servo

GPIO.setmode(GPIO.BCM)

gp_in_blue = 24
gp_in_red = 25
GPIO.setup(gp_in_blue, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(gp_in_red, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO4を制御パルスの出力に設定
gp_out = 4
GPIO.setup(gp_out, GPIO.OUT)
servo(gp_out, GPIO, 0)

while True:
    try:
        if(GPIO.input(gp_in_blue) == 1):    #GPIO24が"1"であれば以下を実行
            deg = 90                         #変数"deg"に90を格納
            servo(gp_out, GPIO, deg)                     #サーボモータを変数"deg"の角度に動作
            deg = 0                         #変数"deg"に0を格納
            servo(gp_out, GPIO, deg)                     #サーボモータを変数"deg"の角度に動作
        if(GPIO.input(gp_in_red) == 1):  #GPIO25が"1"であれば以下を実行
            deg = -90                        #変数"deg"に-90を格納
            servo(gp_out, GPIO, deg)                     #サーボモータを変数"deg"の角度に動作
            deg = 0                        #変数"deg"に0を格納
            servo(gp_out, GPIO, deg)                     #サーボモータを変数"deg"の角度に動作
    except KeyboardInterrupt:                #Ctrl+Cキーが押された
        GPIO.cleanup()                       #GPIOをクリーンアップ
        sys.exit()                           #プログラムを終了

GPIO.cleanup()