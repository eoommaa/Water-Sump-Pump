'''
Water Sump Pump Countdown Timer V5

--- SETUP INSTRUCTIONS ---
READ BEFORE RUNNING THIS FILE
1. Save 3 Pico LCD files to the Pi Pico:
    - `lcd_api.py`
    - `pico_i2c_lcd.py`
    - `pico_i2c_lcd_test.py`
1a. Important: Do NOT rename the files. Keep original filenames
2. Run pico_i2c_lcd_test.py to verify LCD functionality
3. Optional: Rename this file to `main.py` if the Pi Pico will be connected to a power source (e.g., power bank) instead of the computer
4. Run this file on a MicroPython IDE (e.g., Thonny or PyCharm) when the Pi Pico is connected to the computer

--- VERSION HISTORY ---
V1&2: N/A
V3: Fixed STOP btn
V4: Added fan to L298N motor driver. Fan activation @ Temp >= 80°F
V5: Changed variable names, components' GPIO pins, and organized comments
'''

import time
from machine import Pin, I2C, Timer, ADC
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


# GPIO Pins for buzzer, LEDs (G, R, B), btns, and L298N motor driver
buzzer = Pin(9, Pin.OUT)
start_led = Pin(10, Pin.OUT)
stop_led = Pin(11, Pin.OUT)
reset_led = Pin(12, Pin.OUT)

start_btn = Pin(13, Pin.IN, Pin.PULL_UP)
stop_btn = Pin(14, Pin.IN, Pin.PULL_UP)
reset_btn = Pin(15, Pin.IN, Pin.PULL_UP) 

# L298N motor driver GPIO pins
ENA = Pin(2, Pin.OUT)		# Enable A. Motor/Relay
IN1 = Pin(3, Pin.OUT)
IN2 = Pin(4, Pin.OUT)
ENB = Pin(7, Pin.OUT)		# Enable B. Fan
IN3 = Pin(5, Pin.OUT)
IN4 = Pin(6, Pin.OUT)

# Initialize components on/off (1/0)
start_led.value(1)
stop_led.value(0)
reset_led.value(0)
buzzer.value(0)
IN1.value(0)
IN2.value(0)

# LCD at the beginning
lcd.clear()
lcd.putstr("Press START!")


'''
System State Flags
- Initialize system (sys), countdown timer (countdown in the code), and countdown time
- Sys and countdown timer set to false means the both are running normally
- system_locked: True → Sys locked via RESET btn
- countdown_stop: True → Pauses countdown via STOP btn
- initial_countdown_time: Time in sec (e.g., 3600s = 1 hr). Change to 5s for prototyping
'''
system_locked = False
countdown_stop = False
initial_countdown_time = 3600
countdown_time = initial_countdown_time

'''
Hardware Timers & Sensor
- start_led_timer: Blinking G LED during countdown
- buzzer_timer: Buzzer on during RESET (or system_locked)
'''
stop = 1
start_led_timer = Timer()
buzzer_timer = Timer()
temp_sensor = ADC(4)		# Internal temp sensor connected to ADC channel 4


# Functions for LEDs, buzzer, relay, fan, and temp
def blink_start_led(timer):
    start_led.toggle()
    
def blink_reset_led(timer):
    reset_led.toggle()
    
def beep_buzzer(timer):
    buzzer.toggle()

'''
Relay Prototyping
- Motor used as a relay
- Note: relay_NC/relay_NO can be rename to motor_on/motor_off
'''
def relay_NC():
    ENA.value(1)
    IN1.value(1)
    IN2.value(0)

def relay_NO():
    ENA.value(0)
    IN1.value(0)
    IN2.value(0)
    
def fan_on():
    ENB.value(1)
    IN3.value(1)
    IN4.value(0)
    
def fan_off():
    ENB.value(0)
    IN3.value(0)
    IN4.value(0)

def control_fan(temp_F):
    if temp_F >= 80:
        fan_on()
    else:
        fan_off()

'''
Internal Temp Reading in F
- temp_sensor.read_u16: Reads 16-bit ACD
- ADC_voltage: Converts 16-bit ACD to voltage
'''
def read_temp():
    ADC_voltage = temp_sensor.read_u16() * (3.3 / 65535)
    temp_C = 27 - (ADC_voltage - 0.706) / 0.001721
    temp_C = max(min(temp_C, 80), -20)
    temp_F = (1.8 * temp_C) + 32
    return round(temp_F, 1)


'''
Countdown Timer Function
- Motor/Relay control, LED indicator, temp monitoring
- Button handling (STOP & RESET)
    STOP: countdown_stop, solid R LED, relay NO
    RESET: system_locked, blinking B LED, relay NO, buzzer beep
- `return`: Exit countdown
    STOP: Sys enters paused state
    RESET: Sys is locked
'''
def countdown():
    # Initialize countdown
    global countdown_time, countdown_stop, stop
    countdown_stop = False		# Countdown starts
    relay_NC()
    start_led_timer.init(period=500, mode=Timer.PERIODIC, callback=blink_start_led)
    
    for i in range(countdown_time, 0, -1):		# (initial time in sec | final | inc/dec)
        countdown_time = i						# Update countdown time
        if start_btn.value() == 0:
            print("START btn pressed! → Relay NC")
        
        # STOP Btn Handling
        if stop_btn.value() == 0:
            countdown_stop = True
            stop = 0
            start_led.value(0)
            start_led_timer.deinit()	# `deinit` stops START (green) LED blinking
            stop_led.value(1)
            relay_NO()
            print("STOP btn pressed! → Relay NO")
            time.sleep(2)
            return
        
        # RESET Btn Handling
        if reset_btn.value() == 0:
            global system_locked
            system_locked = True
            relay_NO()    
            start_led_timer.deinit()
            start_led.value(0)
            buzzer_timer.init(period=500, mode=Timer.PERIODIC, callback=beep_buzzer)
            print("RESET btn pressed! → System locked, Relay NO, and Buzzer beep beep")
            return
        
        '''
        Countdown Timer on LCD
        - Convert seconds to MM:SS format
        - LCD Line 1: Countdown & Line 2: Temp
        '''
        temp = read_temp()		# Read temp
        min = i // 60
        sec = i % 60
        lcd.clear()
        lcd.putstr(f"Countdown: {min:02}:{sec:02}")
        lcd.move_to(0, 1)
        lcd.putstr(f"Temp: {temp} F")       
        print(f"Countdown: {min:02}:{sec:02} Temp: {temp}°F")
        time.sleep(1)
        
    '''
    Countdown Timer 00:00 Time
    - LCD displays 00:00 when countdown completes
    - START (green) LED always on after countdown is done
    - countdown_time: Reset countdown time to 60:00 when it reaches 00:00
    '''
    lcd.clear()
    lcd.putstr("Countdown: 00:00")
    lcd.move_to(0, 1)
    lcd.putstr(f"Temp: {temp:.2f} F")
    time.sleep(2)
    lcd.clear()
    lcd.putstr("Press START to")
    lcd.move_to(0, 1)
    lcd.putstr("start agn")
        
    start_led.value(1)
    countdown_time = initial_countdown_time
    start_led_timer.deinit()
    relay_NO()
    print(f"Countdown: 00:00 Temp: {temp:.2f}°F")
    print("Countdown done → Relay NO")

'''
Main Control Loop - Button Handling
- Continuous temp monitoring
    control_fan: Automatically based on temp
- STOP: START & RESET btns
- RESET: START btns
- LCD displays specific messages repeatedly when in STOP/RESET mode
'''
while True:
    temp = read_temp()
    control_fan(temp)
    
    # START Btn Handling
    if start_btn.value() == 0 and not system_locked:
        reset_led.value(0)
        stop_led.value(0)
        lcd.clear()
        lcd.move_to(0, 1)
        temp = read_temp()
        lcd.putstr(f"Temp: {temp:.2f} F")
        countdown()
    
    '''
    STOP Btn Options (2)
    1. START: Resume countdown from the time paused on
    2. RESET: Restart the countdown at 60:00 after pressing START btn
    `break`: Exit STOP mode when START/RESET btn pressed
    '''
    if stop == 0:
        while True:
            lcd.clear()
            lcd.putstr("Countdown")
            lcd.move_to(0, 1)
            lcd.putstr("stopped!")
            time.sleep(0.5)
            lcd.clear()
            lcd.putstr("Press START or")
            lcd.move_to(0, 1)
            lcd.putstr("RESET")
            time.sleep(0.5)
            
            if start_btn.value() == 0:
                stop_led.value(0)
                lcd.clear()
                lcd.putstr("START btn")
                lcd.move_to(0, 1)
                lcd.putstr("pressed")
                print("START btn pressed! → Relay NC")
                time.sleep(2)
                stop = 1
                countdown()
                break
            
            if reset_btn.value() == 0:
                stop_led.value(0)
                system_locked = True
                reset_led.value(1)
                buzzer_timer.init(period=500, mode=Timer.PERIODIC, callback=beep_buzzer)
                print("RESET btn pressed! → System locked, Relay NO, and Buzzer beep beep")
                lcd.clear()
                lcd.putstr("RESET btn")
                lcd.move_to(0, 1)
                lcd.putstr("pressed")
                stop = 1
                time.sleep(2)
                break
        
    '''
    RESET Btn Option (1)
    1. START: Restart countdown at 60:00
    '''
    if system_locked:
        start_led.value(0)
        reset_led.toggle()
        time.sleep(0.4)
        
        lcd.clear()
        lcd.putstr("Countdown reset!")
        time.sleep(0.4)
        lcd.clear()
        lcd.putstr("Press START to")
        lcd.move_to(0, 1)
        lcd.putstr("start over")
        time.sleep(0.5)
        
        if start_btn.value() == 0:
            system_locked = False
            buzzer_timer.deinit()
            buzzer.value(0)
            countdown_time = initial_countdown_time
            reset_led.value(0)
            lcd.clear()
            lcd.putstr("START btn")
            lcd.move_to(0, 1)
            lcd.putstr("pressed")
            time.sleep(2)
            
            lcd.clear()
            lcd.putstr("Restarting countdown soon...")
            print("START btn pressed! Restarting countdown!")
            time.sleep(2)
            countdown()   
        continue			# Sys locked skips STOP & RESET until START is pressed
