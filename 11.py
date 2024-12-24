# Viết chương trình bấm button 1 lần 1 cả dòng chữ “Hello-World” chạy từ trái sang phải màn hình LCD; bấm button 1 lần 2 cả dòng chữ trên chạy từ phải sang trái màn hình LCD, bấm button 1 lần 3 thì xóa màn hình LCD.
import RPi.GPIO as GPIO
import time

LCD_PINS = {'RS': 23, 'E': 27, 'D4': 18, 'D5': 17, 'D6': 14, 'D7': 3, 'BL': 2}
BT_1 = 21
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE1 = 0x80
LCD_LINE2 = 0xC0
E_PULSE = 0.0005
E_DELAY = 0.0005
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BT_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def lcd_init():
    for pin in LCD_PINS.values():
        GPIO.setup(pin, GPIO.OUT)

    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)


def lcd_string(message, line=LCD_LINE1):
    message = message.center(LCD_WIDTH, "  ")
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)


def lcd_clear():
    lcd_byte(0x01, LCD_CMD)


def lcd_byte(bits, mode):
    GPIO.output(LCD_PINS['RS'], mode)
    for bit_num in range(4):
        GPIO.output(LCD_PINS[f'D{bit_num + 4}'], bits & (1 << (4 + bit_num)) != 0)

    time.sleep(E_DELAY)
    GPIO.output(LCD_PINS['E'], True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_PINS['E'], False)
    time.sleep(E_DELAY)
    for bit_num in range(4):
        GPIO.output(LCD_PINS[f'D{bit_num + 4}'], bits & (1 << bit_num) != 0)

    time.sleep(E_DELAY)
    GPIO.output(LCD_PINS['E'], True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_PINS['E'], False)
    time.sleep(E_DELAY)

def lcd_display_string(message, line):
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)


def main():
    lcd_init()
    GPIO.output(LCD_PINS['BL'], True)
    button_state = 0
    time.sleep(1)

    mess = "Hello-World!"

    while True:
        if GPIO.input(BT_1) == GPIO.LOW:
            button_state = button_state + 1
            time.sleep(0.25)

        if button_state == 1:
            for i in range(LCD_WIDTH - len(mess)):
                lcd_clear()
                lcd_display_string(" " * i + mess, 1)
                time.sleep(0.25)
                if GPIO.input(BT_1) == GPIO.LOW:
                    button_state = button_state + 1
                    time.sleep(0.1)
                    lcd_clear()
                    break
        elif button_state == 2:
            for i in range(LCD_WIDTH - len(mess), -1, -1):
                lcd_clear()
                lcd_display_string(" " * i + mess, 1)
                time.sleep(0.25)
                if GPIO.input(BT_1) == GPIO.LOW:
                    button_state = button_state + 1
                    time.sleep(0.1)
                    lcd_clear()
                    break
        elif button_state >= 3:
            lcd_clear()
            time.sleep(0.1)
            button_state = 0


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    lcd_clear()
