import time

def servoAngle(angle, servo):
    duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
    servo.ChangeDutyCycle(duty)     #デューティ比を変更
    time.sleep(0.5)  