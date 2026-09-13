<img width="1098" height="595" alt="image" src="https://github.com/user-attachments/assets/cbade2d0-f274-422a-b8c6-f6500f72ee7a" />
# Pi Pico Computer Stats Display


## Why I Built This

I wanted a **physical, always-on display** of my system stats without using up screen space or keeping another app open. Most monitoring tools are digital dashboards on your monitor—I wanted something tangible in my computer. Plus, there's something satisfying about watching real hardware respond to your system's performance in real-time.

## What It Does

This system continuously monitors your Linux computer and displays key performance metrics on three physical LCD screens


**Monitored Stats:**
- CPU usage percentage
- RAM usage percentage
- GPU usage percentage
- CPU temperature
- Network speed

### Component Wiring Diagram

<img width="1472" height="860" alt="image" src="https://github.com/user-attachments/assets/ce30568d-7762-4edf-bfb5-d55bf5ed1c0a" />


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

## How to assemble
1. Place the screens into their circular cutouts on the front
2. Slide in the plate behind the screens to keep them from falling back
3. Upload the code onto the raspberry pi
4. Plug the screens into the raspberry Pi
5. Route the cable from the usb headers through the cutout in the backplate and plug it into the raspberry pi's usb port
6. Screw or glue the raspberry pi's securing plate on (I recommend screws)
7. Screw on the back and top plate and connect it to the usb headers
8. Click it into place in your pc case (Designed specifically for mine so you'll have to edit the external case to make it fit your pc)
9. Enjoy the beautiful displays!

## What You Need

| Component | Price | Source | Link |
|-----------|-------|--------|------|
| Raspberry Pi Pico | $6 | digikey | https://www.digikey.com/en/products/detail/raspberry-pi/SC0918/16608263 |
| 6mm m2x.4 screws | $0.65 | digikey | https://www.digikey.com/en/products/detail/essentra-components/50M020040G004/11638015 |
| 3x LCD 1602 + I2C backpack | $14.99 each | WaveShare | https://www.waveshare.com/1.28inch-lcd-module.htm |
| Micro USB cable | $8.43 | newegg | https://www.newegg.com/p/27U-00H1-000P4?Item=9SIAERNM1X0850 |
| Digikey Shipping | $8.49 | FedEx Ground | |
| NewEgg Shipping | Free | | |
| WaveShare Shipping | $10.00 | | |
| **Total** | **~$78.54** | | |

<img width="957" height="963" alt="Screenshot 2026-06-30 104208" src="https://github.com/user-attachments/assets/607aaf98-ea60-49aa-be36-d177a4b82aee" />
<img width="1098" height="595" alt="image" src="https://github.com/user-attachments/assets/cf387ef1-4976-4b4c-9a94-212f0a76cf5f" />
<img width="1025" height="300" alt="Screenshot 2026-06-14 211706" src="https://github.com/user-attachments/assets/60bbf416-721c-4d7d-b440-d447574e5e66" />
<img width="1021" height="399" alt="image" src="https://github.com/user-attachments/assets/f4d8a65f-de95-491f-a1d3-0adbbb943c42" />

I do not have a hackatime project for this, the connectors aren't jst, they're standard 2.54mm shrouded pin sockets
