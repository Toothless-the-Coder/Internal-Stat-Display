"""
I2C 16x2 LCD Display Driver
Compatible with PCF8574 I2C backpack
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

# Flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# Flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# Flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# PCF8574 I2C backpack pins
BIT_RS = 0
BIT_RW = 1
BIT_EN = 2
BIT_BL = 3

class LCD_I2C:
    """I2C LCD Display controller for 16x2 displays with PCF8574 backpack"""
    
    def __init__(self, i2c, addr, rows=2, cols=16):
        self.i2c = i2c
        self.addr = addr
        self.rows = rows
        self.cols = cols
        self.row_offsets = [0x00, 0x40]
        
        time.sleep(0.05)
        
        # Initialize the display
        self._init_display()
    
    def _write_bits(self, value, bits, pin_start):
        """Write bits to the I2C backpack"""
        bits_value = 0
        for i in range(bits):
            if (value & (1 << i)):
                bits_value |= (1 << (pin_start + i))
        return bits_value
    
    def _enable_pulse(self, data):
        """Pulse the enable pin to latch data"""
        # Pull enable low
        self.i2c.writeto(self.addr, bytes([data & ~(1 << BIT_EN)]))
        time.sleep(0.00001)
        # Pull enable high
        self.i2c.writeto(self.addr, bytes([data | (1 << BIT_EN)]))
        time.sleep(0.00001)
        # Pull enable low
        self.i2c.writeto(self.addr, bytes([data & ~(1 << BIT_EN)]))
        time.sleep(0.00001)
    
    def _write_four_bits(self, value):
        """Write 4 bits to the LCD in 4-bit mode"""
        data = (value << 4) | (1 << BIT_BL)  # Backlight on
        self._enable_pulse(data)
    
    def _write_byte(self, value, mode):
        """Write a byte to the LCD
        mode: 0 = command, 1 = data
        """
        high = value & 0xF0
        low = (value << 4) & 0xF0
        
        # Set RS pin (0 for command, 1 for data)
        rs_bit = mode << BIT_RS
        
        # Write high nibble
        data = high | rs_bit | (1 << BIT_BL)
        self._enable_pulse(data)
        
        # Write low nibble
        data = low | rs_bit | (1 << BIT_BL)
        self._enable_pulse(data)
    
    def _init_display(self):
        """Initialize the LCD display"""
        time.sleep(0.05)
        
        # Set to 4-bit mode
        for _ in range(3):
            self._write_four_bits(0x03)
            time.sleep(0.005)
        
        self._write_four_bits(0x02)
        time.sleep(0.005)
        
        # Function set: 4-bit mode, 2 lines, 5x8 font
        self._write_byte(LCD_FUNCTIONSET | LCD_4BITMODE | LCD_2LINE | LCD_5x8DOTS, 0)
        time.sleep(0.001)
        
        # Display control: display on, cursor off, blink off
        self._write_byte(LCD_DISPLAYCONTROL | LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF, 0)
        time.sleep(0.001)
        
        # Entry mode: increment cursor, no shift
        self._write_byte(LCD_ENTRYMODESET | LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT, 0)
        time.sleep(0.001)
        
        # Clear display
        self.clear()
    
    def clear(self):
        """Clear the display"""
        self._write_byte(LCD_CLEARDISPLAY, 0)
        time.sleep(0.002)
    
    def home(self):
        """Move cursor to home position"""
        self._write_byte(LCD_RETURNHOME, 0)
        time.sleep(0.002)
    
    def set_cursor(self, row, col):
        """Set cursor position"""
        if row >= self.rows:
            row = self.rows - 1
        if col >= self.cols:
            col = self.cols - 1
        
        address = col + self.row_offsets[row]
        self._write_byte(LCD_SETDDRAMADDR | address, 0)
    
    def putstr(self, text):
        """Write text to the current cursor position"""
        for char in text:
            self._write_byte(ord(char), 1)
    
    def putch(self, char):
        """Write a single character"""
        self._write_byte(ord(char), 1)
    
    def write_line(self, row, text):
        """Write text to a specific line, clearing the rest"""
        if row >= self.rows:
            return
        
        self.set_cursor(row, 0)
        # Pad or truncate text to column width
        text = (text + ' ' * self.cols)[:self.cols]
        self.putstr(text)
    
    def create_char(self, location, pattern):
        """Create a custom character"""
        if location >= 8:
            return
        
        self._write_byte(LCD_SETCGRAMADDR | (location << 3), 0)
        for byte in pattern:
            self._write_byte(byte, 1)
