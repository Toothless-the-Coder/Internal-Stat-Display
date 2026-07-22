<img width="957" height="963" alt="Screenshot 2026-06-30 104208" src="https://github.com/user-attachments/assets/607aaf98-ea60-49aa-be36-d177a4b82aee" />
<img width="1073" height="547" alt="Screenshot 2026-06-15 144144" src="https://github.com/user-attachments/assets/9676ddd9-fd63-4346-b980-2573a8146d65" />
<img width="1025" height="300" alt="Screenshot 2026-06-14 211706" src="https://github.com/user-attachments/assets/60bbf416-721c-4d7d-b440-d447574e5e66" />
<img width="658" height="255" alt="Screenshot 2026-06-11 095840" src="https://github.com/user-attachments/assets/5e51f81d-c3c4-4936-8111-69059166b957" />
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
| Raspberry Pi Pico | $6 | digikey |
| 3x LCD 1602 + I2C backpack | $14.99 each | WaveShare |
| Micro USB cable | $7.99| newegg |
| **Total** | **~$78.49** | |
