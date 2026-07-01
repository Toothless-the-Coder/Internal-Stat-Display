# Pi Pico Computer Stats Display

> A compact, always-on dashboard for monitoring your Linux system—built with hardware that costs less than a coffee.

## 🎯 Why I Built This

I wanted a **physical, always-on display** of my system stats without using screen real estate or keeping another app open. Most monitoring tools are digital dashboards on your monitor—I wanted something tangible on my desk. Plus, there's something satisfying about watching real hardware respond to your system's performance in real-time.

This project combines:
- **Raspberry Pi Pico** (~$5)—a tiny, powerful microcontroller
- **3 LCD displays**—each showing different stats
- **Your Linux computer**—streaming live data

The result? A **device that sits on your desk and shows your system's heartbeat** in real-time.

## 📊 What It Does

This system continuously monitors your Linux computer and displays key performance metrics on three physical LCD screens:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  SCREEN 1       │    │  SCREEN 2       │    │  SCREEN 3       │
│                 │    │                 │    │                 │
│  CPU: 45.2%     │    │  RAM: 62.3%     │    │  GPU: 78%       │
│  Temp: 52.5°C   │    │  Net: 1.5MB/s   │    │  OK             │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Monitored Stats:**
- CPU usage percentage
- RAM usage percentage
- GPU usage percentage
- CPU temperature
- Network speed

All updating in real-time, wirelessly communicating over USB.

## 🔧 How It Fits Together

### The Big Picture

```
┌──────────────────────────────────────────────────────────────┐
│                      YOUR LINUX PC                           │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ stat_sender.py (Python script)                      │   │
│  │ • Reads CPU, RAM, GPU, Temperature, Network data   │   │
│  │ • Packages it as JSON                              │   │
│  │ • Sends over USB serial connection                 │   │
│  └────────────────────────────┬────────────────────────┘   │
│                               │                             │
│                          USB Port                           │
│                          (Serial)                           │
│                               │                             │
└───────────────────────────────┼─────────────────────────────┘
                                │
                        [USB Cable]
                                │
┌───────────────────────────────┼─────────────────────────────┐
│                               │                             │
│  ┌────────────────────────────▼───────────────────────┐    │
│  │         RASPBERRY PI PICO (Microcontroller)        │    │
│  │                                                    │    │
│  │  • Receives JSON data via USB serial              │    │
│  │  • Decodes and parses stats                       │    │
│  │  • Manages 3 I2C LCD displays in parallel         │    │
│  └────────────────┬──────────────────────────────────┘    │
│                   │                                        │
│        I2C Bus (2 wires: SDA + SCL)                       │
│                   │                                        │
│    ┌──────────────┼──────────────┐                         │
│    │              │              │                         │
│  ┌─┴──┐         ┌─┴──┐         ┌─┴──┐                      │
│  │LCD1│         │LCD2│         │LCD3│                      │
│  │0x27│         │0x26│         │0x25│                      │
│  └────┘         └────┘         └────┘                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Hardware Connections

#### **I2C Bus (Data Connection)**

All three LCDs connect to the **same I2C bus** on the Pico using just 2 wires:

```
Raspberry Pi Pico        All 3 LCD Displays
─────────────────        ──────────────────

GPIO0 (SDA) ─────┬──────► LCD1 SDA
            │   LCD2 SDA
            │   LCD3 SDA
            └─────────────────────
                 (all connected)

GPIO1 (SCL) ─────┬──────► LCD1 SCL
            │   LCD2 SCL
            │   LCD3 SCL
            └─────────────────────
                 (all connected)

VBUS (5V) ────┬──────► LCD1 VCC
          │   LCD2 VCC
          │   LCD3 VCC
          └─────────────────────

GND ──────┬──────► LCD1 GND
          │   LCD2 GND
          │   LCD3 GND
          └─────────────────────
```

**Why I2C?** It's designed for exactly this—multiple devices on the same bus, each with a unique address. Perfect for daisy-chaining displays.

#### **USB Connection (Power + Data)**

```
Raspberry Pi Pico              Your Linux Computer
─────────────────              ───────────────────

Micro USB Port ════════════════ USB Port
  - Power (5V)
  - Data (RX/TX serial)
```

The USB provides:
- **Power** to run the Pico and LCDs
- **Data** for serial communication (115200 baud)

### Component Wiring Diagram

```
                    Raspberry Pi Pico
                    
                    USB [to computer]
                     ▲
                     │
        ┌────────────┼────────────┐
        │            │            │
      VBUS          GND     GPIO0/GPIO1
        │            │        (SDA/SCL)
        │            │           │
        ├────────────┼───────────┬┤
        │            │           ││
     ┌──┴──┐     ┌───┴──┐   ┌───┴┴──┐
     │     │     │      │   │       │
    LCD1  LCD2  LCD3   GND  Pull-up  (optional)
   0x27  0x26  0x25    All  4.7kΩ   Resistors
     │     │     │      │   │
    VCC   VCC   VCC    GND  
     │     │     │      │
    (All connected in parallel on same 4 wires)
```

## 📦 The Three Screens

Each LCD is independently addressable on the I2C bus:

| Screen | Address | Content | Purpose |
|--------|---------|---------|---------|
| **LCD1** | `0x27` | CPU Usage + Temperature | Processor monitoring |
| **LCD2** | `0x26` | RAM Usage + Network Speed | Memory & connectivity |
| **LCD3** | `0x25` | GPU Usage + Status | Graphics performance |

## 🎛️ System Features
- Real-time system stat monitoring (CPU, RAM, GPU, Temperature, Network)
- Display on three separate 16x2 character LCD screens
- USB serial communication from host computer
- JSON-based protocol for easy extension
- Low power consumption (~500mA)
- Auto-detection of connected displays

## 🛒 What You Need

| Component | Price | Source |
|-----------|-------|--------|
| Raspberry Pi Pico | $5 | raspberrypi.com |
| 3x LCD 1602 + I2C backpack | $3-5 each | Amazon/AliExpress |
| Micro USB cable | $2-5 | Any electronics store |
| Breadboard & jumper wires | $5-10 | Electronics kit |
| **Total** | **~$30-40** | Budget-friendly! |

### Raspberry Pi Pico Specs
- **Microcontroller:** RP2040
- **RAM:** 264KB
- **Flash:** 2MB
- **I2C Support:** 2 I2C buses
- **UART Support:** 2 serial ports
- **Size:** 21x51mm (tiny!)

### LCD Displays
- **Type:** 1602 (16 characters × 2 rows)
- **Connection:** I2C via PCF8574 backpack
- **Power:** 5V
- **Current:** ~80-150mA per display (with backlight)

## 🏗️ Software Architecture

### On the Pico (MicroPython)

```
main.py ─────────────────────────────────────
    │
    ├─► config.py ◄─ [Configuration: pins, addresses, update rate]
    │
    ├─► serial_handler.py ◄─ [Receives JSON from Linux]
    │        │
    │        └─► Parses incoming stats
    │
    ├─► display_manager.py ◄─ [Manages 3 LCD screens]
    │        │
    │        └─► Updates stats on displays
    │
    └─► lcd_i2c.py ◄─ [I2C LCD driver]
             │
             └─► Controls each display
```

**Key Files:**
- `main.py` — Runs the main loop
- `config.py` — I2C pins, LCD addresses, update speed
- `serial_handler.py` — Reads JSON from USB
- `display_manager.py` — Logic for what shows on each screen
- `lcd_i2c.py` — Low-level LCD communication

### On Your Linux Computer (Python 3)

```
stat_sender.py ────────────────────────────────
    │
    ├─► Read system stats (psutil library)
    │    ├─ CPU usage
    │    ├─ RAM usage
    │    ├─ GPU usage
    │    ├─ Temperature
    │    └─ Network speed
    │
    ├─► Format as JSON
    │
    └─► Send via USB serial
             │
             └─► To Pico
```

**Key File:**
- `stat_sender.py` — Gathers stats and sends to Pico

## ⚡ Quick Start (15 Minutes)

**Start here:** See [QUICKSTART.md](../QUICKSTART.md)

For detailed setup:
1. [Wiring & Hardware Setup](../docs/HARDWARE.md)
2. [Pico Firmware Installation](../QUICKSTART.md)
3. [Linux Sender Setup](../linux_sender/SETUP.md)

## 🚀 Running It

### Start the Linux Sender

```bash
cd linux_sender
python3 stat_sender.py
```

**Options:**
```bash
python3 stat_sender.py --port /dev/ttyACM0  # Specify port
python3 stat_sender.py --interval 2.0       # Update every 2 seconds
python3 stat_sender.py --baud 115200        # Custom baud rate
```

**That's it!** Stats should start appearing on your displays within seconds.

### Run as a Background Service

To have it start automatically on boot:

```bash
# See linux_sender/SETUP.md for systemd service installation
```

## 🖥️ What You'll See

The three LCD displays show:

```
LCD 1 (0x27)              LCD 2 (0x26)              LCD 3 (0x25)
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ CPU: 45.2%       │      │ RAM: 62.3%       │      │ GPU: 78%         │
│ Temp: 52.5C      │      │ Net: 1.5MB/s     │      │ Stat Display OK  │
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

Each display updates **1x per second** (configurable).

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **No displays showing** | Check I2C wiring: SDA (GPIO0), SCL (GPIO1), power, ground |
| **Only some displays work** | Run I2C scan to find addresses, update `config.py` |
| **Serial connection fails** | Check port: `ls /dev/ttyACM*` or use `--port` option |
| **Stats not updating** | Verify `stat_sender.py` is running |
| **Garbled text on displays** | Ensure 5V power to LCDs, check wiring |

**For detailed troubleshooting:** See [HARDWARE.md](../docs/HARDWARE.md)

## Performance Notes

- I2C clock: 400kHz (standard)
- Serial baud: 115200
- Update frequency: 1 second (adjustable)
- Pico CPU usage: <5% typical

## 💬 How Devices Communicate

The Pico and Linux computer exchange information in **JSON format** over USB serial.

### Message Format (Linux → Pico)

```json
{
  "cpu": 45.2,
  "ram": 62.3,
  "gpu": 78,
  "temp": 52.5,
  "network": "1.5MB/s"
}
```

Each message is one line, sent **1x per second**.

**For the full protocol spec:** See [PROTOCOL.md](../docs/PROTOCOL.md)

## ⚙️ Performance Specs

- **I2C Speed:** 400kHz (standard)
- **Serial Baud:** 115200
- **Update Frequency:** 1 second (adjustable)
- **Pico CPU Usage:** <5%
- **Power Consumption:** 400-600mA total

## 📚 Documentation

- **[QUICKSTART.md](../QUICKSTART.md)** — Get running in 15 minutes
- **[HARDWARE.md](../docs/HARDWARE.md)** — Detailed wiring and troubleshooting
- **[PROTOCOL.md](../docs/PROTOCOL.md)** — Communication format and extending
- **[SETUP.md](../linux_sender/SETUP.md)** — Linux sender installation

## 🛠️ Customization

### Change Update Frequency
Edit `pico_firmware/config.py`:
```python
UPDATE_INTERVAL = 500  # Update every 500ms instead of 1000ms
```

### Adjust What's Displayed
Edit `pico_firmware/display_manager.py`:
```python
def _display_screen_0(self, lcd):
    # Customize Screen 1 here
    cpu_str = f"CPU: {self.stats['cpu']}%"
    custom_str = f"Your stat here"
    lcd.write_line(0, cpu_str)
    lcd.write_line(1, custom_str)
```

### Add New Statistics
1. Update Linux sender to collect the stat
2. Add the field to the JSON message
3. Update Pico's `display_manager.py` to show it

See [PROTOCOL.md](../docs/PROTOCOL.md) for a detailed example.

## 🚀 Future Ideas

- [ ] OLED display support for better visuals
- [ ] Graph mode (bar graphs on LCD)
- [ ] SD card logging
- [ ] Pi Pico W (wireless Ethernet instead of USB)
- [ ] Custom character support for better icons
- [ ] Multi-computer monitoring

## 📝 License

Open source — modify and share freely!

## 🤝 Support

1. **Can't get it working?** Start with [QUICKSTART.md](../QUICKSTART.md)
2. **Hardware issues?** Check [HARDWARE.md](../docs/HARDWARE.md)
3. **Need more info?** See full documentation in `/docs`
