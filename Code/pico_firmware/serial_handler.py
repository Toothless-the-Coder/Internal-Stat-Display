"""
Serial communication handler for receiving stats from the computer
"""

import machine
import json
import time

class SerialHandler:
    """Handle serial communication with the computer"""
    
    def __init__(self, uart_id=0, baud=115200, tx_pin=0, rx_pin=1):
        """
        Initialize UART serial communication
        Default: UART0 on GPIO0 (TX) and GPIO1 (RX)
        For UART1: TX=GPIO4, RX=GPIO5
        """
        self.uart = machine.UART(uart_id, baudrate=baud, tx=machine.Pin(tx_pin), rx=machine.Pin(rx_pin))
        self.uart.init(bits=8, parity=None, stop=1)
        self.buffer = ""
        self.last_read = time.ticks_ms()
    
    def read_data(self):
        """
        Read data from serial port
        Expects JSON format: {"cpu": 45.2, "ram": 62.3, "gpu": 78, "temp": 52.5, "network": "1.5MB/s"}
        Returns dict if valid JSON received, None otherwise
        """
        if self.uart.any():
            try:
                char = self.uart.read(1).decode('utf-8', errors='ignore')
                
                if char == '\n':
                    if self.buffer.strip():
                        try:
                            data = json.loads(self.buffer)
                            self.buffer = ""
                            return data
                        except json.JSONDecodeError as e:
                            print(f"JSON decode error: {e}")
                            self.buffer = ""
                    self.buffer = ""
                else:
                    self.buffer += char
                    # Prevent buffer overflow (max 256 chars)
                    if len(self.buffer) > 256:
                        self.buffer = ""
            except Exception as e:
                print(f"Serial read error: {e}")
        
        return None
    
    def write_data(self, data):
        """
        Send data to computer
        data: dict or string
        """
        try:
            if isinstance(data, dict):
                message = json.dumps(data) + '\n'
            else:
                message = str(data) + '\n'
            
            self.uart.write(message.encode('utf-8'))
        except Exception as e:
            print(f"Serial write error: {e}")
    
    def send_ack(self):
        """Send acknowledgment to computer"""
        self.write_data({"status": "ok"})
