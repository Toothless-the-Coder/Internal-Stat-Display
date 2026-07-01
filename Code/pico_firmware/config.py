"""
Configuration for the Pi Pico Stat Display
Modify these settings based on your hardware setup
"""

# I2C Configuration
I2C_PORT = 0  # I2C0 (GPIO0/GP1) or I2C1 (GPIO2/3)
I2C_SDA = 0   # GPIO0 for I2C0, or GPIO2 for I2C1
I2C_SCL = 1   # GPIO1 for I2C0, or GPIO3 for I2C1

# LCD I2C Addresses (default for common I2C LCD modules)
# Adjust these based on your specific modules
LCD_ADDRESSES = [0x27, 0x26, 0x25]  # 3 LCD displays

# Display settings
UPDATE_INTERVAL = 1000  # Update display every 1000ms (1 second)
ROTATION_INTERVAL = 5000  # Rotate displayed stats every 5 seconds

# Serial Configuration
SERIAL_BAUD = 115200
SERIAL_TIMEOUT = 100  # milliseconds

# Stats display rotation (which stats show on each screen)
STAT_ROTATION = {
    0: ['cpu', 'temp'],      # Screen 1: CPU and Temperature
    1: ['ram', 'network'],   # Screen 2: RAM and Network
    2: ['gpu', 'info']       # Screen 3: GPU and System Info
}
