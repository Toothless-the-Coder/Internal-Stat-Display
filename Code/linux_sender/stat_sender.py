#!/usr/bin/env python3
"""
Linux Stat Sender for Raspberry Pi Pico Display
Reads system statistics and sends them via serial to the Pi Pico
"""

import serial
import serial.tools.list_ports
import psutil
import json
import time
import sys
import os
import signal

class StatSender:
    """Send system statistics via serial to Pi Pico"""
    
    def __init__(self, port=None, baud=115200):
        self.baud = baud
        self.ser = None
        self.running = True
        
        # Register signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Connect to serial port
        self.connect(port)
    
    def _signal_handler(self, sig, frame):
        """Handle termination signals"""
        print("\nShutting down...")
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        sys.exit(0)
    
    def find_pico_port(self):
        """
        Attempt to find the Pi Pico's serial port
        Returns port name or None
        """
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
            # Check for common Pi Pico identifiers
            if 'Pico' in port.description or 'CH340' in port.description or \
               'USB' in port.description or 'ttyACM' in port.device or \
               'COM' in port.device:
                return port.device
        
        return None
    
    def connect(self, port=None):
        """Connect to the serial port"""
        try:
            # Auto-detect port if not specified
            if port is None:
                port = self.find_pico_port()
                if port:
                    print(f"Found Pi Pico on port: {port}")
                else:
                    print("No Pi Pico found. Available ports:")
                    ports = serial.tools.list_ports.comports()
                    for p in ports:
                        print(f"  {p.device}: {p.description}")
                    raise Exception("Could not find Pi Pico")
            
            self.ser = serial.Serial(port, self.baud, timeout=1)
            print(f"Connected to {port} at {self.baud} baud")
            time.sleep(2)  # Wait for Pi Pico to reset
        except Exception as e:
            print(f"Error connecting to serial port: {e}")
            raise
    
    def get_system_stats(self):
        """Collect system statistics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.5)
            
            # RAM usage
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            
            # GPU usage (Linux)
            gpu_percent = self._get_gpu_usage()
            
            # CPU temperature (if available)
            temp = self._get_cpu_temp()
            
            # Network speed
            net_speed = self._get_network_speed()
            
            return {
                'cpu': cpu_percent,
                'ram': ram_percent,
                'gpu': gpu_percent,
                'temp': temp,
                'network': net_speed
            }
        except Exception as e:
            print(f"Error collecting stats: {e}")
            return None
    
    def _get_cpu_temp(self):
        """Get CPU temperature from /sys/class/thermal/thermal_zone0/temp"""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp_millidegrees = int(f.read().strip())
                return temp_millidegrees / 1000.0
        except:
            return 0
    
    def _get_gpu_usage(self):
        """Get GPU usage (placeholder - varies by GPU)"""
        try:
            # This is a placeholder - actual implementation depends on GPU type
            # For NVIDIA, you could use nvidia-smi
            # For Intel/AMD, other tools are needed
            
            # Try to read from /proc/acpi/battery if on ARM
            try:
                import os
                if os.path.exists('/sys/class/thermal/'):
                    # On Raspberry Pi, we might not have GPU usage info
                    return 0
            except:
                pass
            
            return 0
        except:
            return 0
    
    def _get_network_speed(self):
        """Get network speed in KB/s"""
        try:
            net_io_1 = psutil.net_io_counters()
            time.sleep(1)
            net_io_2 = psutil.net_io_counters()
            
            bytes_sent = net_io_2.bytes_sent - net_io_1.bytes_sent
            bytes_recv = net_io_2.bytes_recv - net_io_1.bytes_recv
            
            total_kb = (bytes_sent + bytes_recv) / 1024
            return f"{total_kb:.1f}KB"
        except:
            return "0KB"
    
    def send_stats(self, stats):
        """Send statistics via serial"""
        try:
            if self.ser and self.ser.is_open:
                json_data = json.dumps(stats) + '\n'
                self.ser.write(json_data.encode('utf-8'))
                return True
        except Exception as e:
            print(f"Error sending stats: {e}")
        return False
    
    def run(self, interval=1):
        """
        Main loop - continuously collect and send stats
        interval: time in seconds between updates
        """
        print("Starting stat collection (press Ctrl+C to stop)...")
        print("-" * 50)
        
        while self.running:
            try:
                stats = self.get_system_stats()
                if stats:
                    if self.send_stats(stats):
                        # Display stats locally
                        print(f"\rCPU: {stats['cpu']:5.1f}% | "
                              f"RAM: {stats['ram']:5.1f}% | "
                              f"GPU: {stats['gpu']:5.1f}% | "
                              f"Temp: {stats['temp']:5.1f}C | "
                              f"Net: {stats['network']}", end="", flush=True)
                    else:
                        print("Warning: Failed to send stats")
                
                time.sleep(interval)
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Send Linux system stats to Raspberry Pi Pico via serial'
    )
    parser.add_argument('--port', help='Serial port (e.g., /dev/ttyACM0, COM3)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate (default: 115200)')
    parser.add_argument('--interval', type=float, default=1.0, help='Update interval in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    try:
        sender = StatSender(port=args.port, baud=args.baud)
        sender.run(interval=args.interval)
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
