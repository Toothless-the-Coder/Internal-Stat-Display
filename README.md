# Pi Pico Computer Stats Display

> A compact, always-on dashboard for monitoring your Linux system—built with hardware that costs less than a coffee.

## Why I Built This

I wanted a **physical, always-on display** of my system stats without using screen real estate or keeping another app open. Most monitoring tools are digital dashboards on your monitor—I wanted something tangible on my desk. Plus, there's something satisfying about watching real hardware respond to your system's performance in real-time.

## What It Does

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

## The Three Screens

Each LCD is independently addressable on the I2C bus:

| Screen | Address | Content | Purpose |
|--------|---------|---------|---------|
| **LCD1** | `0x27` | CPU Usage + Temperature | Processor monitoring |
| **LCD2** | `0x26` | RAM Usage + Network Speed | Memory & connectivity |
| **LCD3** | `0x25` | GPU Usage + Status | Graphics performance |

## System Features
- Real-time system stat monitoring (CPU, RAM, GPU, Temperature, Network)
- Display on three separate 16x2 character LCD screens
- USB serial communication from host computer
- JSON-based protocol for easy extension
- Low power consumption (~500mA)
- Auto-detection of connected displays

## What You Need

| Component | Price | Source |
|-----------|-------|--------|
| Raspberry Pi Pico | $5 | raspberrypi.com |
| 3x LCD 1602 + I2C backpack | $3-5 each | Amazon/AliExpress |
| Micro USB cable | $2-5 | Any electronics store |
| Breadboard & jumper wires | $5-10 | Electronics kit |
| **Total** | **~$30-40** | Budget-friendly! |
