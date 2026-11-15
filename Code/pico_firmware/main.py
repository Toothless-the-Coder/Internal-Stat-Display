
"""
Main program for the Raspberry Pi Pico stats display.
Sets up the LCD screens and listens for stats from the computer.
"""

import machine
import time

from config import *
from lcd_i2c import LCD_I2C
from serial_handler import SerialHandler
from display_manager import DisplayManager


def main():
    print("Starting up the stats display...")

    # Set up the I2C connection
    i2c = machine.I2C(
        I2C_PORT,
        scl=machine.Pin(I2C_SCL),
        sda=machine.Pin(I2C_SDA),
        freq=400000
    )

    # Find and initialize the LCD screens
    print(f"Found I2C devices: {i2c.scan()}")

    lcds = []

    for addr in LCD_ADDRESSES:
        try:
            lcd = LCD_I2C(i2c, addr, 2, 16)
            lcd.clear()
            lcds.append(lcd)

            print(f"Connected to LCD at 0x{addr:02x}")

        except Exception as e:
            print(f"Couldn't initialize LCD at 0x{addr:02x}: {e}")

    if len(lcds) < 3:
        print("Warning: Some of the LCD screens weren't detected.")

    # Set up the serial connection and display manager
    serial_handler = SerialHandler()
    display_manager = DisplayManager(lcds)

    # Show a quick startup message
    if lcds:
        lcds[0].putstr("Starting up...")
        time.sleep(1)
        lcds[0].clear()

    # Keep checking for new stats and updating the screens
    last_update = 0

    while True:
        try:
            # Check if the computer has sent any new information
            data = serial_handler.read_data()

            if data:
                display_manager.update_stats(data)

            # Refresh the screens when it's time
            current_time = time.ticks_ms()

            if time.ticks_diff(current_time, last_update) >= UPDATE_INTERVAL:
                display_manager.display_current_frame()
                last_update = current_time

            # A short pause keeps the Pico from constantly running this loop
            time.sleep(0.01)

        except Exception as e:
            print(f"Something went wrong: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
