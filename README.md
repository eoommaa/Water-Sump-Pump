# Water Sump Pump Countdown Timer
A countdown timer for managing a water sump pump using a Raspberry Pi Pico programmed in MicroPython, designed for SLAC National Accelerator Laboratory during Summer 2024.
- **Features:** Automates sump pump intervals and relay activation with a 60-minute countdown timer, 3-button control (`START`/`STOP`/`RESET`), and thermal safety from 80°F fan activation to prevent overheating
  - Each button (`START`/`STOP`/`RESET`) is mapped to an LED and activates a specific state when the user presses on it
  - 60-minute countdown timer displayed in `MM:SS` format with the temperature on the LCD (`Countdown: 60:00` & `Temp: 80 F`)
- **Components:** [Full BOM](docs/BOM.md) with relay and sump pump specs

# Schematics[^1][^2]

## SLAC Water Sump Pump Countdown Timer Schematic
![image](https://github.com/eoommaa/Water-Sump-Pump/blob/main/kicad/schematics/SLAC%20Water%20Sump%20Pump.svg)

## RP2040 Water Sump Pump Countdown Timer Schematic
![image](https://github.com/eoommaa/Water-Sump-Pump/blob/main/kicad/schematics/RP2040%20Water%20Sump%20Pump.svg)


# Relay Behavior
Relay controls the 120 VAC outlet like a feedback loop.
- **[`SLAC Water Sump Pump Countdown Timer` Schematic](#slac-water-sump-pump-countdown-timer-schematic):** Pin 3 from `K1` relay has an input of 120 VAC L input (10 A) and Pin 4 is an input to the same 120 VAC output
- **`START`:** Relay NC[^3] &rarr; Sump pump activates
- **`STOP` & `RESET`:** Relay NO[^3] &rarr; Sump pump deactivates


# `START`/`STOP`/`RESET` Button Controls
## `START` Button
- **Function:** Default state where the system starts 60-minute countdown timer
- **LED:** Blinking green


## `STOP` Button
- **Function:** Pauses the countdown timer
- **LED:** Solid red
- **LCD:** Displays messages repeatedly
  > Countdown stopped!
  
  > Press START or RESET
- [`countdown_stop`](LINK) set to `True` to pause the countdown timer

### `START` & [`RESET`](#reset-button) Button on `STOP`
- **`START`:** Countdown timer continues from the time it was paused on
  - **LED:** Red off and blinking green


## `RESET` Button
- **Function:** Emergency reset (Countdown timer restarts at `60:00` after the user presses `START` button)
- **LED & Buzzer** Blinking blue & buzzer beeps repeatedly
- **LCD:** Displays messages repeatedly
  > Countdown reset!
  
  > Press START to start over
- [`system_locked`](LINK) set to `True` and only allows the user one button to press on to restart the countdown timer
  - User can press on `STOP` or `RESET` button, but the program ignores the two button presses when in `RESET` mode


## Countdown Idle and Completion LCD Messages
- **Countdown Idle:** `Press START!`
- **Countdown Completion:** `Press START to start agn`


# Notes
- **[`SLAC Water Sump Pump Countdown Timer` Schematic](#slac-water-sump-pump-countdown-timer-schematic):** A `K1` relay is connected to the L298N motor driver, which is the component connected in the final hardware
- **[`RP2040 Water Sump Pump Countdown Timer` Schematic](#rp2040-water-sump-pump-countdown-timer-schematic):** A 5V DC motor is used since the relay acts like a switch along with an IC2 1602 LCD connected to the RP2040
  - Ex: Motor on when countdown timer is running and vice versa when it is off
- **Power Indicator:** Green LED stays on during both idle and after completion states to indicate that the Pi Pico is powered


[^1]: [`SLAC Water Sump Pump Countdown Timer` Schematic](https://github.com/eoommaa/Water-Sump-Pump/blob/main/kicad/schematics/SLAC%20Water%20Sump%20Pump.pdf) and [`.kicad_sch`](https://github.com/eoommaa/Water-Sump-Pump/blob/main/kicad/SLAC%20Water%20Sump%20Pump.kicad_sch)
[^2]: [`RP2040 Water Sump Pump Countdown Timer` Schematic](https://github.com/eoommaa/Water-Sump-Pump/blob/main/kicad/schematics/RP2040%20Water%20Sump%20Pump.pdf) and [`.kicad_sch`](https://github.com/eoommaa/Water-Sump-Pump/blob/main/kicad/RP2040%20Water%20Sump%20Pump.kicad_sch)
[^3]: Normally open (NO) & normally closed (NC)
