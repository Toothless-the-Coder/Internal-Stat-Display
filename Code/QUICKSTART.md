# Quick Start Guide

Get your Pi Pico stat display running in 15 minutes.

## Prerequisites

- Raspberry Pi Pico (flashed with MicroPython)
- 3x LCD 1602 displays with I2C backpack
- Linux computer
- USB cable for Pico
- Python 3.7+ on Linux

## Step 1: Flash MicroPython to Pi Pico (5 min)

1. Download MicroPython: https://micropython.org/download/rp2-pico/
2. Hold BOOTSEL button on Pico
3. Connect USB to computer (Pico still held)
4. Release BOOTSEL
5. Copy downloaded `.uf2` file to `RPI-RP2` drive
6. Pico reboots automatically

## Step 2: Verify I2C Addresses (2 min)

Use Thonny IDE to run this code on Pico:

```python
import machine
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
print("I2C addresses found:", [hex(addr) for addr in i2c.scan()])
```

Should output something like: `['0x27', '0x26', '0x25']`

If not all three show up:
- Check wiring
- Verify LCD power connections
- See [HARDWARE.md](HARDWARE.md) troubleshooting

## Step 3: Upload Pico Firmware (3 min)

In Thonny IDE:
1. File → Open → Select each Python file from `pico_firmware/`
2. Save each to Pico (right-click file → Save to device)
3. Upload in this order:
   - `config.py`
   - `lcd_i2c.py`
   - `serial_handler.py`
   - `display_manager.py`
   - `main.py`

Pico should start running automatically after `main.py` is uploaded.

## Step 4: Setup Linux Sender (3 min)

```bash
cd linux_sender
pip install -r requirements.txt
python3 stat_sender.py
```

That's it! You should see stats updating on the displays.

## Troubleshooting

### No stats appearing on display?

1. **Check serial connection:**
   ```bash
   ls /dev/ttyACM*
   ```

2. **Check I2C connection:**
   - Run I2C scan in Thonny (Step 2)
   - All three LCDs should appear

3. **Manual port specification:**
   ```bash
   python3 stat_sender.py --port /dev/ttyACM0
   ```

4. **Check Pico output:**
   - Open Thonny serial monitor
   - Should see connection messages
   - Watch for errors

### One or more LCDs not showing data?

- Check I2C address (run scan, update `config.py`)
- Verify all are connected to same I2C bus
- Check power to each LCD

### Stats not updating?

- Verify stat_sender.py is running: `ps aux | grep stat_sender`
- Check for errors in Linux terminal
- Restart both Pico and stat_sender

## What's Next?

- **Customize stats:** Edit `display_manager.py` to show different info
- **Change refresh rate:** Edit `UPDATE_INTERVAL` in `config.py`
- **Add new metrics:** See [PROTOCOL.md](../docs/PROTOCOL.md) for extending
- **Run as service:** See [SETUP.md](SETUP.md) for systemd integration

## Important Files

| File | Purpose |
|------|---------|
| `pico_firmware/main.py` | Pico entry point |
| `pico_firmware/config.py` | I2C addresses, pins, update rate |
| `linux_sender/stat_sender.py` | Sends system stats to Pico |
| `docs/README.md` | Full documentation |
| `docs/HARDWARE.md` | Wiring diagrams |
| `docs/PROTOCOL.md` | Communication format |

## Display Layout

**LCD 1 (Screen 1):**
```
CPU: 45.2%
Temp: 52.5C
```

**LCD 2 (Screen 2):**
```
RAM: 62.3%
Net: 1.5MB/s
```

**LCD 3 (Screen 3):**
```
GPU: 78%
Stat Display OK
```

## Performance

- CPU usage (Pico): <5%
- CPU usage (Linux): <2%
- Update latency: <100ms
- Power consumption: ~400-600mA

## Support

For detailed information:
- Wiring issues → See `docs/HARDWARE.md`
- Communication problems → See `docs/PROTOCOL.md`
- Installation help → See `linux_sender/SETUP.md`
- General info → See `docs/README.md`
