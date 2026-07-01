# Hardware Setup Guide

## Pinout Reference

### Raspberry Pi Pico

```
        USB
       ╔═══╗
     1 ║o o║ 40
    20 ╚═══╝ 21

GPIO Pins (numbers are GPIO numbers):
Top Row (L to R):    1(GP0), 2(GP1), 4(GP2), 5(GP3), 7(GP4), 8(GP5),
                     10(GP6), 11(GP7), 13(GP8), 14(GP9), 16(GP10), 17(GP11),
                     19(GP12), 20(GP13), 22(GP14), 24(GP15), 25(GP16), 26(GP17),
                     27(GP18), 28(GP19), 30(GP20), 31(GP21), 32(GP22)

Bottom Row (L to R):  GND, GP23, GND, GND, GND, VSYS, GND, 3V3-OUT, 3V3-EN
```

### I2C LCD 1602 Pinout (with PCF8574 Backpack)

```
Pin 1: VSS (GND)
Pin 2: VDD (5V)
Pin 3: V0 (Contrast) - Connected to backpack
Pin 4: RS (Register Select) - PCF8574 Pin 0
Pin 5: RW (Read/Write) - PCF8574 Pin 1 (GND on backpack)
Pin 6: EN (Enable) - PCF8574 Pin 2
Pin 7-10: D4-D7 (Data pins) - PCF8574 Pins 4-7
Pin 11-14: D0-D3 (not used in 4-bit mode)
Pin 15: A (Backlight +) - PCF8574 Pin 3 through resistor
Pin 16: K (Backlight -) - GND
```

## Wiring Diagram

### Single I2C LCD to Pico

```
LCD I2C Backpack          Raspberry Pi Pico
─────────────────         ──────────────────
VCC (5V)   ────────────── VBUS (Pin 40)
GND        ────────────── GND (Pin 38, 43)
SDA        ────────────── GPIO0 (Pin 1)
SCL        ────────────── GPIO1 (Pin 2)
```

### Three I2C LCDs to Pico (Parallel I2C Bus)

```
                     ┌─────────┐
                     │ Pico    │
                     │ GPIO0   │
                     │ (SDA)   │
                     │ GPIO1   │
                     │ (SCL)   │
                     │ VBUS    │
                     │ GND     │
                     └────┬────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    ┌───┴────┐        ┌───┴────┐       ┌───┴────┐
    │LCD1    │        │LCD2    │       │LCD3    │
    │0x27    │        │0x26    │       │0x25    │
    └────────┘        └────────┘       └────────┘
```

All three LCDs share the same SDA and SCL lines (I2C is a shared bus).
Each LCD has a different I2C address (set via A0, A1, A2 pins on backpack).

## I2C Address Selection

PCF8574 I2C addresses are determined by A0, A1, A2 pins:

| A2 | A1 | A0 | Address |
|----|----|----|---------|
| 0  | 0  | 0  | 0x20    |
| 0  | 0  | 1  | 0x21    |
| 0  | 1  | 0  | 0x22    |
| 0  | 1  | 1  | 0x23    |
| 1  | 0  | 0  | 0x24    |
| 1  | 0  | 1  | 0x25    |
| 1  | 1  | 0  | 0x26    |
| 1  | 1  | 1  | 0x27    |

Most modules default to 0x27 (all pins pulled high).

## Component List

### Essential
- 1x Raspberry Pi Pico (~$5)
- 3x LCD 1602 displays with I2C backpack (~$10-15 each)
- 1x Micro USB cable (for power/data)
- 1x Breadboard (for prototyping)
- Jumper wires (22 AWG)

### Recommended
- Pull-up resistors: 4.7kΩ (2x, for SDA/SCL lines)
- Small resistor: 330Ω (for LCD backlight, already included on most backpacks)
- Pi Pico debug probe (optional, for advanced debugging)

## Assembly Steps

### 1. Connect I2C Bus
Solder or connect with breadboard:
- Connect all LCD SDA pins → Pico GPIO0 (Pin 1)
- Connect all LCD SCL pins → Pico GPIO1 (Pin 2)
- Connect all LCD GND → Pico GND
- Connect all LCD VCC → Pico VBUS (5V)

### 2. Add Pull-up Resistors (if needed)
If LCDs aren't responding:
- 4.7kΩ resistor from SDA → VBUS
- 4.7kΩ resistor from SCL → VBUS

### 3. Verify I2C Addresses
Set different addresses on each LCD by connecting/leaving A0, A1, A2 pins:
- Open each display and set pins as needed
- Or program via I2C address selection

### 4. USB Connection
- Connect Pico micro USB port to Linux computer

## Power Considerations

### Power Budget
- Pico: ~120mA typical
- Each LCD (with backlight): ~80-150mA
- Total: ~500-600mA

**Note:** Most USB ports provide 500mA, so you may need a powered hub or additional power supply for all displays at full brightness.

### Reducing Power
- Reduce LCD backlight brightness (PWM on backlight pin)
- Reduce I2C clock speed (affects power consumption slightly)
- Reduce stat update frequency

## Testing the Wiring

### Test 1: Scan I2C Bus
```python
import machine
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0), freq=400000)
devices = i2c.scan()
print(f"Found {len(devices)} devices: {[f'0x{d:02x}' for d in devices]}")
# Should output: Found 3 devices: ['0x27', '0x26', '0x25']
```

### Test 2: Write to LCD
```python
from lcd_i2c import LCD_I2C
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
lcd = LCD_I2C(i2c, 0x27, 2, 16)
lcd.write_line(0, "Test Display")
lcd.write_line(1, "Screen 1")
```

### Test 3: Check USB Serial
```bash
# Linux
sudo dmesg | tail
# Look for "CDC ACM device" or similar
ls /dev/ttyACM*
```

## Troubleshooting Hardware

### LCDs Not Responding
1. Check power: Measure 5V on LCD VCC pin
2. Check I2C communication: Use logic analyzer or oscilloscope
3. Verify pull-up resistors if bus fails at distances > 1m

### One LCD Missing from Scan
1. Check physical connection
2. Verify A0/A1/A2 pins set correctly
3. Try swapping with known-working LCD
4. Reset LCD with power cycle

### Intermittent Display Glitches
1. Reduce I2C clock speed in code (from 400kHz to 100kHz)
2. Add 0.1µF capacitors near LCD power pins
3. Check for ground loops or long wire runs

### USB Connection Not Working
1. Try different USB port on computer
2. Try different USB cable (some are power-only)
3. Check dmesg for connection errors
4. Press BOOTSEL + Power to reset Pico

## Performance Tips

- **I2C Speed**: 400kHz is standard and reliable
- **Cable Length**: Keep I2C cables <1m for 400kHz
- **Power Supply**: Use regulated 5V, not USB hub's voltage
- **Grounding**: Good ground connections are critical for I2C reliability
