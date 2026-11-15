
"""
Handles the LCD screens and decides what information
gets shown on each one.
"""

import time
from config import STAT_ROTATION, ROTATION_INTERVAL


class DisplayManager:
    def __init__(self, lcds):
        self.lcds = lcds

        # Starting values until we receive actual stats
        self.stats = {
            'cpu': 'N/A',
            'ram': 'N/A',
            'gpu': 'N/A',
            'temp': 'N/A',
            'network': 'N/A'
        }

        self.rotation_index = 0
        self.last_rotation = time.ticks_ms()

        # Each screen has its own layout
        self.display_modes = {
            0: self._display_screen_0,
            1: self._display_screen_1,
            2: self._display_screen_2
        }

    def update_stats(self, data):
        # Update any stats that were included in the received data
        for key in self.stats:
            if key in data:
                self.stats[key] = data[key]

        print(f"Updated stats: {self.stats}")

    def display_current_frame(self):
        # Update each connected screen
        for screen_id, lcd in enumerate(self.lcds):
            if screen_id in self.display_modes:
                self.display_modes[screen_id](lcd)

    def _format_stat(self, value):
        # Keep text short enough to fit on the LCD
        if isinstance(value, (int, float)):
            if isinstance(value, float):
                return f"{value:.1f}"
            return str(value)

        return str(value)[:16]

    def _display_screen_0(self, lcd):
        # First screen shows CPU usage and temperature
        cpu = f"CPU: {self._format_stat(self.stats['cpu'])}%"[:16]
        temp = f"Temp: {self._format_stat(self.stats['temp'])}C"[:16]

        lcd.clear()
        lcd.write_line(0, cpu)
        lcd.write_line(1, temp)

    def _display_screen_1(self, lcd):
        # Second screen shows RAM usage and network activity
        ram = f"RAM: {self._format_stat(self.stats['ram'])}%"[:16]
        network = f"Net: {self._format_stat(self.stats['network'])}"[:16]

        lcd.clear()
        lcd.write_line(0, ram)
        lcd.write_line(1, network)

    def _display_screen_2(self, lcd):
        # Third screen shows GPU usage and a simple status message
        gpu = f"GPU: {self._format_stat(self.stats['gpu'])}%"[:16]
        info = "Stat Display OK"

        lcd.clear()
        lcd.write_line(0, gpu)
        lcd.write_line(1, info)

    def show_message(self, screen_id, line1, line2=""):
        # Show a message on one screen instead of the usual stats
        if screen_id < len(self.lcds):
            lcd = self.lcds[screen_id]

            lcd.clear()
            lcd.write_line(0, line1)

            if line2:
                lcd.write_line(1, line2)
