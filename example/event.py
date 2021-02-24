import RPi.GPIO as GPIO
import time

BUTTON_PIN = 16

def main():
    GPIO.setwarnings(False)
    # Set the layout for the pin declaration
    GPIO.setmode(GPIO.BCM)
    # BCMの21番ピンを入力に設定
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    # callback登録（GIO.FALLING:立下りエッジ検出、bouncetime:300ms）
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=callback, bouncetime=300)

    try:
        while(True):
            time.sleep(1)

    # Keyboard入力があれば終わり
    except KeyboardInterrupt:
        print("break")
        GPIO.cleanup()

def callback(channel):
  print("button pushed %s"%channel)

if __name__ == "__main__":
    main()