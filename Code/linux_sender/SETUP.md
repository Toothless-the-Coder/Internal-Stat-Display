# Pi Pico Stat Display - Linux Sender Setup

## Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Find Your Pi Pico's Serial Port

```bash
ls /dev/ttyACM* 
# or
dmesg | grep USB
```

### 3. Run the Sender

```bash
# Auto-detect Pi Pico
python3 stat_sender.py

# Or specify port explicitly
python3 stat_sender.py --port /dev/ttyACM0

# Custom update interval (e.g., 2 seconds)
python3 stat_sender.py --interval 2.0
```

### 4. Run as a Service (Optional)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/pico-stat-sender.service
```

Add the following (adjust paths as needed):

```ini
[Unit]
Description=Pi Pico Stat Sender
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/pico-stat-sender
ExecStart=/usr/bin/python3 stat_sender.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable pico-stat-sender
sudo systemctl start pico-stat-sender
```

Check status:

```bash
sudo systemctl status pico-stat-sender
```

## Command Line Options

- `--port PORT`: Specify serial port manually (e.g., `/dev/ttyACM0`)
- `--baud RATE`: Set baud rate (default: 115200)
- `--interval SECONDS`: Update interval (default: 1.0)

## Troubleshooting

### No Pi Pico Found
- Check the USB cable connection
- Verify the device appears with `lsusb`
- May need to install CH340 drivers: `sudo apt install ch340-dkms`

### Permission Denied
```bash
sudo usermod -a -G dialout $USER
# Then log out and log back in
```

### Serial Port Not Found
- List all ports: `sudo python3 -c "import serial.tools.list_ports; print([p for p in serial.tools.list_ports.comports()])"`
- Try different ports manually with `--port` option
