
"""
Handles communication between the Pico and the computer.
Receives system stats over UART and converts them from JSON.
"""

import machine
import json
import time


class SerialHandler:
    def __init__(self, uart_id=0, baud=115200, tx_pin=0, rx_pin=1):
        # Set up the UART connection
        self.uart = machine.UART(
            uart_id,
            baudrate=baud,
            tx=machine.Pin(tx_pin),
            rx=machine.Pin(rx_pin)
        )

        self.uart.init(bits=8, parity=None, stop=1)

        # Incoming data is collected here until a full message arrives
        self.buffer = ""
        self.last_read = time.ticks_ms()

    def read_data(self):
        # Check if there's anything waiting to be read
        if self.uart.any():
            try:
                char = self.uart.read(1).decode("utf-8", errors="ignore")

                # Each message ends with a newline
                if char == "\n":
                    if self.buffer.strip():
                        try:
                            data = json.loads(self.buffer)
                            self.buffer = ""
                            return data

                        except ValueError as e:
                            print(f"Couldn't read incoming data: {e}")
                            self.buffer = ""

                    self.buffer = ""

                else:
                    self.buffer += char

                    # Clear the buffer if a message gets too long
                    if len(self.buffer) > 256:
                        self.buffer = ""

            except Exception as e:
                print(f"Serial read error: {e}")

        return None

    def write_data(self, data):
        # Convert the data to JSON before sending it
        try:
            if isinstance(data, dict):
                message = json.dumps(data) + "\n"
            else:
                message = str(data) + "\n"

            self.uart.write(message.encode("utf-8"))

        except Exception as e:
            print(f"Serial write error: {e}")

    def send_ack(self):
        # Let the computer know the message was received
        self.write_data({"status": "ok"})
