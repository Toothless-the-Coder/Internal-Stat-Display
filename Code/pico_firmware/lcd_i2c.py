
"""
Driver for the 16x2 LCD screens.
Uses a PCF8574 I2C backpack to communicate with the displays.
"""

import machine
import time


# LCD commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Cursor and text settings
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Display settings
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# Cursor movement
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# LCD mode settings
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Pins on the I2C backpack
BIT_RS = 0
BIT_RW = 1
BIT_EN = 2
BIT_BL = 3


class LCD_I2C:
    def __init__(self, i2c, addr, rows=2, cols=16):
        self.i2c = i2c
        self.addr = addr
        self.rows = rows
        self.cols = cols

        # Starting addresses for each row
        self.row_offsets = [0x00, 0x40]

        time.sleep(0.05)
        self._init_display()

    def _write_bits(self, value, bits, pin_start):
        # Convert a value into the matching backpack pin positions
        result = 0

        for i in range(bits):
            if value & (1 << i):
                result |= (1 << (pin_start + i))

        return result

    def _enable_pulse(self, data):
        # Toggle the enable pin so the LCD reads the data
        self.i2c.writeto(self.addr, bytes([data & ~(1 << BIT_EN)]))
        time.sleep(0.00001)

        self.i2c.writeto(self.addr, bytes([data | (1 << BIT_EN)]))
        time.sleep(0.00001)

        self.i2c.writeto(self.addr, bytes([data & ~(1 << BIT_EN)]))
        time.sleep(0.00001)

    def _write_four_bits(self, value):
        # Send one half of a byte, with the backlight turned on
        data = (value << 4) | (1 << BIT_BL)
        self._enable_pulse(data)

    def _write_byte(self, value, mode):
        # The LCD uses 4-bit mode, so each byte is sent in two parts
        high = value & 0xF0
        low = (value << 4) & 0xF0

        # RS is low for commands and high for regular text
        rs_bit = mode << BIT_RS

        data = high | rs_bit | (1 << BIT_BL)
        self._enable_pulse(data)

        data = low | rs_bit | (1 << BIT_BL)
        self._enable_pulse(data)

    def _init_display(self):
        # Get the LCD ready to receive commands
        time.sleep(0.05)

        # Switch the display into 4-bit mode
        for _ in range(3):
            self._write_four_bits(0x03)
            time.sleep(0.005)

        self._write_four_bits(0x02)
        time.sleep(0.005)

        # Set up the display for two lines of text
        self._write_byte(
            LCD_FUNCTIONSET | LCD_4BITMODE | LCD_2LINE | LCD_5x8DOTS, 0
        )

        # Turn on the display and hide the cursor
        self._write_byte(
            LCD_DISPLAYCONTROL | LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF, 0
        )

        # Make the cursor move from left to right
        self._write_byte(
            LCD_ENTRYMODESET | LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT, 0
        )

        self.clear()

    def clear(self):
        # Clear everything currently on the screen
        self._write_byte(LCD_CLEARDISPLAY, 0)
        time.sleep(0.002)

    def home(self):
        # Move the cursor back to the top-left corner
        self._write_byte(LCD_RETURNHOME, 0)
        time.sleep(0.002)

    def set_cursor(self, row, col):
        # Keep the cursor within the screen's limits
        if row >= self.rows:
            row = self.rows - 1

        if col >= self.cols:
            col = self.cols - 1

        address = col + self.row_offsets[row]
        self._write_byte(LCD_SETDDRAMADDR | address, 0)

    def putstr(self, text):
        # Write a string starting at the current cursor position
        for char in text:
            self._write_byte(ord(char), 1)

    def putch(self, char):
        # Write a single character
        self._write_byte(ord(char), 1)

    def write_line(self, row, text):
        # Write a full line, clearing any leftover characters
        if row >= self.rows:
            return

        self.set_cursor(row, 0)

        text = (text + " " * self.cols)[:self.cols]
        self.putstr(text)

    def create_char(self, location, pattern):
        # Save a custom character to one of the LCD's character slots
        if location >= 8:
            return

        self._write_byte(LCD_SETCGRAMADDR | (location << 3), 0)

        for byte in pattern:
            self._write_byte(byte, 1)
