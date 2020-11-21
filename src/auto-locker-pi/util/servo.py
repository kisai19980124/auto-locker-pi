from .servoAngle import servoAngle

def servo(gp_out, GPIO, angle):
    servo = GPIO.PWM(gp_out, 50)
    servo.start(0)
    servoAngle(angle, servo)
    servo.stop()
