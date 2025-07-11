# Water Sump Pump Countdown Timer
- A countdown timer for managing a water sump pump using a Raspberry Pi Pico programmed in MicroPython, designed for SLAC National Accelerator Laboratory during Summer 2024
- **Features:** Automates sump pump intervals with a 60-minute countdown, 3-button control (`START`/`STOP`/`RESET`), and thermal safety from 80°F fan activation to prevent overheating
  - Each button (`START`/`STOP`/`RESET`) is mapped to an LED and activates a specific state when a user presses on it
  - 60-minute countdown displayed in `MM:SS` format with the temperature on the LCD (`Countdown: 60:00` & `Temp: 80 F`)

## Bill of Material (BOM)
*Note: Components used for prototyping*
| Hardware | Quantity | Notes |
| :--: | :--: | :--: |
| Raspberry Pi Pico | 1 | RP2040 MCU |
| L298N Motor Driver | 1 | Fan & motor/relay control |
| 9V DC Battery | 1 | Power source for L298N motor driver |

| User Control | Quantity | Notes |
| :--: | :--: | :--: |
| NO[^1] Buttons | 3 | `START`/`STOP`/`RESET` |

| User Feedback | Quantity | Notes |
| :--: | :--: | :--: |
| LEDs | 3 | Green (`START`), Red (`STOP`), Blue (`RESET`) |
| I2C LCD 1602 | 1 | Displaying countdown time & temp |
| Piezoelectric Buzzer | 1 | Beeps on `RESET` button | |

| System Feedback | Quantity | Notes |
| :--: | :--: | :--: |
| 5V Fan | 1 | Thermal safety |
| Motor | 1 | Relay testing |

| Passive Components | Quantity | Notes |
| :--: | :--: | :--: |
| 330 &#8486; Resistors | 3 | LEDs current limiting |
| 100 &mu;F Capacitors | 3 | Button debouncing |

<br>

***Water Sump Pump Countdown Timer Schematic***[^2]

***RP2040 Water Sump Pump Countdown Timer Schematic***[^3]

- [ ] rp2040 pic here, pics/gif of 3 buttons


# `START`/`STOP`/`RESET` Button Controls
## Relay Behavior
- `START`: Relay becomes NC[^1] &rarr; pump activates
- `STOP`/`RESET`: Relay becomes NO &rarr; pump deactivates

## `START` Button
- Default state where the system starts 60-minute countdown timer and blinking green LED


## `STOP` Button
- Red LED on and LCD displays the countdown time paused on and message:
  > Press START or RESET
- [`countdown_stop`](LINK) is set to `True` for the countdown timer to stop continuing

### `START` Button on `STOP`
- Countdown timer continues from the time it was paused on
- Red LED off and blinking green LED

### `RESET` Button on `STOP`
- Countdown timer restarts at `60:00`


## `RESET` Button
- Blinking blue LED and buzzer beeps repeatedly
- LCD displays the message repeatedly until a user presses the START button:
  >  Press START to start over
- [`system_locked`](LINK) is set to `True` and only allows the user one button to press on to restart
  - User can press on the `STOP` or `RESET` button, but the program ignores the two button presses when in `RESET` mode

### `START` Button on `RESET`
- Countdown timer restarts at `60:00`


# Notes
- In the [`water sump pump` schematic](LINK), a `K1` relay is connected to the LN298N motor driver, which is the component connected in the final physical hardware
- A motor is used for testing the Pi Pico since the relay acts like a switch
  - Ex: Motor turns on when countdown timer is running and vice versa when it is off
  - See the [`rp2040 water sump pump` schematic](LINK) for Pi Pico testing where the motor is connected to the L298N motor driver and IC2 LCD 1602 is used


[^1]: Normally open (NO) & normally closed (NC)
[^2]: [Water Sump Pump Countdown Timer KiCad File](LINK)
[^3]: [RP2040 Water Sump Pump Countdown Timer KiCad File](LINK)
