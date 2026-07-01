"""
Display manager for managing multiple LCD displays and stat rotation
"""

import time
from config import STAT_ROTATION, ROTATION_INTERVAL

class DisplayManager:
    """Manage the display of stats across multiple LCD screens"""
    
    def __init__(self, lcds):
        """
        Initialize display manager
        lcds: list of LCD_I2C objects
        """
        self.lcds = lcds
        self.stats = {
            'cpu': 'N/A',
            'ram': 'N/A',
            'gpu': 'N/A',
            'temp': 'N/A',
            'network': 'N/A'
        }
        self.rotation_index = 0
        self.last_rotation = time.ticks_ms()
        self.display_modes = {
            0: self._display_screen_0,
            1: self._display_screen_1,
            2: self._display_screen_2
        }
    
    def update_stats(self, data):
        """
        Update statistics from received data
        data: dict with keys like 'cpu', 'ram', 'gpu', 'temp', 'network'
        """
        for key in self.stats.keys():
            if key in data:
                self.stats[key] = data[key]
        
        print(f"Stats updated: {self.stats}")
    
    def display_current_frame(self):
        """Display the current frame on all available screens"""
        for screen_id, lcd in enumerate(self.lcds):
            if screen_id in self.display_modes:
                self.display_modes[screen_id](lcd)
    
    def _format_stat(self, value):
        """Format a stat value for display (max 16 chars per line)"""
        if isinstance(value, (int, float)):
            return f"{value:.1f}" if isinstance(value, float) else str(value)
        return str(value)[:16]
    
    def _display_screen_0(self, lcd):
        """Display Screen 0: CPU and Temperature"""
        cpu_str = f"CPU: {self._format_stat(self.stats['cpu'])}%"[:16]
        temp_str = f"Temp: {self._format_stat(self.stats['temp'])}C"[:16]
        
        lcd.clear()
        lcd.write_line(0, cpu_str)
        lcd.write_line(1, temp_str)
    
    def _display_screen_1(self, lcd):
        """Display Screen 1: RAM and Network"""
        ram_str = f"RAM: {self._format_stat(self.stats['ram'])}%"[:16]
        net_str = f"Net: {self._format_stat(self.stats['network'])}"[:16]
        
        lcd.clear()
        lcd.write_line(0, ram_str)
        lcd.write_line(1, net_str)
    
    def _display_screen_2(self, lcd):
        """Display Screen 2: GPU and System Info"""
        gpu_str = f"GPU: {self._format_stat(self.stats['gpu'])}%"[:16]
        info_str = "Stat Display OK"[:16]
        
        lcd.clear()
        lcd.write_line(0, gpu_str)
        lcd.write_line(1, info_str)
    
    def show_message(self, screen_id, line1, line2=""):
        """Show a temporary message on a specific screen"""
        if screen_id < len(self.lcds):
            lcd = self.lcds[screen_id]
            lcd.clear()
            lcd.write_line(0, line1)
            if line2:
                lcd.write_line(1, line2)
