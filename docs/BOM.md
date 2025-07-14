# Bill of Materials
*Note: Components used for prototyping*

| Hardware | Qty | Notes |
| :--: | :--: | :--: |
| Raspberry Pi Pico | 1 | RP2040 MCU |
| L298N Motor Driver | 1 | Fan & motor/relay control |
| 9V DC Battery | 1 | Power source for L298N motor driver |

| User Control | Qty | Notes |
| :--: | :--: | :--: |
| NO[^1] Buttons | 3 | `START`/`STOP`/`RESET` |

| User Feedback | Qty | Notes |
| :--: | :--: | :--: |
| LEDs | 3 | Green (`START`), Red (`STOP`), Blue (`RESET`) |
| I2C 1602 LCD | 1 | Displaying countdown time & temp |
| Piezoelectric Buzzer | 1 | Beeps on `RESET` button |

| System Feedback | Qty | Notes |
| :--: | :--: | :--: |
| 5V DC Fan | 1 | Thermal safety |
| 5V DC Motor | 1 | Relay testing |

| Passive Components | Qty | Notes |
| :--: | :--: | :--: |
| 330 &#8486; Resistors | 3 | LEDs current limiting |
| 100 &mu;F Capacitors | 3 | Button debouncing |


# Relay and Sump Pump Specs
*Note: Similar components connected in the final hardware*
| Components | Manufacturer Part Number | Datasheet | Notes |
| :--: | :--: | :--: | :--: |
| Relay | AZ9375-1A-24DEF | [AZ9375 SENSITIVE SUBMINIATURE RELAY](https://www.azettler.com/pdfs/az9375.pdf) | 12 VDC coil, 120 VAC (10 A) |
| Sump Pump | PF92342-PB | [PF92342 Thermoplastic Sump Pump](https://fergusonprod.a.bigcontent.io/v1/static/5097488_7397986_specification) | 2400 GPH at 0' lift |


[^1]: Normally open (NO)
