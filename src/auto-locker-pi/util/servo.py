import servo-angle

def servo(gp_out, GPIO, angle):
    servo = GPIO.PWM(gp_out, 50)
    servo.start(0)
    servo-angle(angle)
    servo.stop()
