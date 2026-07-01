"""
Raspberry Pi Pico - Computer Stats Display
Main entry point for the MicroPython firmware
"""

import machine
import time
from config import *
from lcd_i2c import LCD_I2C
from serial_handler import SerialHandler
from display_manager import DisplayManager

def main():
    """Main execution loop"""
    print("Initializing Pi Pico Stat Display...")
    
    # Initialize I2C
    i2c = machine.I2C(I2C_PORT, scl=machine.Pin(I2C_SCL), sda=machine.Pin(I2C_SDA), freq=400000)
    
    # Initialize LCD displays
    print(f"Scanning I2C devices: {i2c.scan()}")
    lcds = []
    for addr in LCD_ADDRESSES:
        try:
            lcd = LCD_I2C(i2c, addr, 2, 16)  # 2 rows, 16 columns
            lcd.clear()
            lcds.append(lcd)
            print(f"LCD initialized at 0x{addr:02x}")
        except Exception as e:
            print(f"Error initializing LCD at 0x{addr:02x}: {e}")
    
    if len(lcds) < 3:
        print("Warning: Not all LCDs initialized successfully")
    
    # Initialize serial handler
    serial_handler = SerialHandler()
    
    # Initialize display manager
    display_manager = DisplayManager(lcds)
    
    # Display startup message
    if lcds:
        lcds[0].putstr("Starting up...")
        time.sleep(1)
        lcds[0].clear()
    
    # Main loop
    last_update = 0
    while True:
        try:
            # Check for incoming serial data
            data = serial_handler.read_data()
            if data:
                display_manager.update_stats(data)
            
            # Update display every UPDATE_INTERVAL milliseconds
            current_time = time.ticks_ms()
            if time.ticks_diff(current_time, last_update) >= UPDATE_INTERVAL:
                display_manager.display_current_frame()
                last_update = current_time
            
            time.sleep(0.01)  # Small delay to prevent CPU hogging
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
