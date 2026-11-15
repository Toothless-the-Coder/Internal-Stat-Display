
#!/usr/bin/env python3

"""
Reads system stats from Linux and sends them to a Raspberry Pi Pico
over a serial connection.
"""

import serial
import serial.tools.list_ports
import psutil
import json
import time
import sys
import signal
import argparse
import os


class StatSender:
    def __init__(self, port=None, baud=115200):
        self.baud = baud
        self.ser = None
        self.running = True

        # Handle Ctrl+C and other shutdown signals
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

        self.connect(port)

    def shutdown(self, sig=None, frame=None):
        print("\nShutting down...")
        self.running = False

        if self.ser and self.ser.is_open:
            self.ser.close()

        sys.exit(0)

    def find_pico(self):
        # Look through connected serial devices for the Pico
        ports = serial.tools.list_ports.comports()

        for port in ports:
            description = port.description.lower()
            device = port.device.lower()

            if any(name in description for name in ["pico", "ch340", "usb"]):
                return port.device

            if "ttyacm" in device:
                return port.device

        return None

    def connect(self, port=None):
        try:
            # Find the Pico automatically if no port was provided
            if port is None:
                port = self.find_pico()

                if port:
                    print(f"Found Raspberry Pi Pico on {port}")
                else:
                    print("Couldn't find a Raspberry Pi Pico.")
                    print("Available serial ports:")

                    for p in serial.tools.list_ports.comports():
                        print(f"  {p.device}: {p.description}")

                    raise Exception("No suitable serial port found")

            self.ser = serial.Serial(port, self.baud, timeout=1)

            print(f"Connected to {port} ({self.baud} baud)")

            # Give the Pico a moment to restart
            time.sleep(2)

        except Exception as e:
            print(f"Couldn't connect to serial port: {e}")
            raise

    def get_stats(self):
        try:
            # CPU and memory usage
            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory().percent

            # Other system information
            gpu = self.get_gpu_usage()
            temp = self.get_cpu_temp()
            network = self.get_network_speed()

            return {
                "cpu": cpu,
                "ram": ram,
                "gpu": gpu,
                "temp": temp,
                "network": network
            }

        except Exception as e:
            print(f"Couldn't collect system stats: {e}")
            return None

    def get_cpu_temp(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
                temp = int(file.read().strip())
                return temp / 1000

        except (OSError, ValueError):
            return 0

    def get_gpu_usage(self):
        # GPU usage isn't supported yet, so return 0 for now
        return 0

    def get_network_speed(self):
        try:
            before = psutil.net_io_counters()
            time.sleep(1)
            after = psutil.net_io_counters()

            sent = after.bytes_sent - before.bytes_sent
            received = after.bytes_recv - before.bytes_recv

            total = (sent + received) / 1024

            return f"{total:.1f}KB"

        except Exception:
            return "0KB"

    def send_stats(self, stats):
        try:
            if self.ser and self.ser.is_open:
                data = json.dumps(stats) + "\n"
                self.ser.write(data.encode("utf-8"))
                return True

        except Exception as e:
            print(f"Couldn't send stats: {e}")

        return False

    def run(self, interval=1):
        print("Collecting system stats. Press Ctrl+C to stop.")
        print("-" * 60)

        while self.running:
            try:
                stats = self.get_stats()

                if stats:
                    if self.send_stats(stats):
                        print(
                            f"\rCPU: {stats['cpu']:5.1f}% | "
                            f"RAM: {stats['ram']:5.1f}% | "
                            f"GPU: {stats['gpu']:5.1f}% | "
                            f"Temp: {stats['temp']:5.1f}C | "
                            f"Net: {stats['network']}",
                            end="",
                            flush=True
                        )
                    else:
                        print("Couldn't send stats to Pico.")

                time.sleep(interval)

            except KeyboardInterrupt:
                self.shutdown()

            except Exception as e:
                print(f"\nSomething went wrong: {e}")
                time.sleep(1)


def main():
    parser = argparse.ArgumentParser(
        description="Send Linux system stats to a Raspberry Pi Pico"
    )

    parser.add_argument(
        "--port",
        help="Serial port (example: /dev/ttyACM0)"
    )

    parser.add_argument(
        "--baud",
        type=int,
        default=115200,
        help="Serial baud rate (default: 115200)"
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Time between updates in seconds (default: 1.0)"
    )

    args = parser.parse_args()

    try:
        sender = StatSender(port=args.port, baud=args.baud)
        sender.run(interval=args.interval)

    except KeyboardInterrupt:
        print("\nExiting...")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
