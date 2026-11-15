
"""
Settings for the Raspberry Pi Pico stats display.

Change these values to match your hardware and how you
want the information to show up on the screens.
"""

# I2C pins
I2C_PORT = 0
I2C_SDA = 0
I2C_SCL = 1

# Addresses for the LCD screens
# These are common addresses, but yours might be different.
LCD_ADDRESSES = [0x27, 0x26, 0x25]

# How often the screens update and switch between stats (in milliseconds)
UPDATE_INTERVAL = 1000
ROTATION_INTERVAL = 5000

# Serial connection settings
SERIAL_BAUD = 115200
SERIAL_TIMEOUT = 100

# Choose which information appears on each screen
STAT_ROTATION = {
    0: ['cpu', 'temp'],       # CPU usage and temperature
    1: ['ram', 'network'],    # Memory usage and network activity
    2: ['gpu', 'info']        # GPU usage and system information
}
