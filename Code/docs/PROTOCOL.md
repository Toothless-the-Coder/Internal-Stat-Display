# Communication Protocol

## Overview

The Pi Pico and Linux computer communicate via USB serial using JSON messages. Each message is one line of JSON terminated with a newline (`\n`).

## Baud Rate & Serial Settings
- **Baud Rate**: 115200
- **Data Bits**: 8
- **Parity**: None
- **Stop Bits**: 1
- **Flow Control**: None

## Message Format

All messages are UTF-8 encoded JSON strings, one per line.

### Host → Pico: Statistics Update

**Message Type**: `stats`

```json
{
  "cpu": 45.2,
  "ram": 62.3,
  "gpu": 78,
  "temp": 52.5,
  "network": "1.5MB/s"
}
```

**Fields:**
| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `cpu` | float | 0-100 | CPU usage percentage |
| `ram` | float | 0-100 | RAM usage percentage |
| `gpu` | float | 0-100 | GPU usage percentage (0 if unavailable) |
| `temp` | float | -50-120 | CPU temperature in Celsius |
| `network` | string | - | Network speed (e.g., "1.5MB/s", "250KB/s") |

**Frequency**: Recommended 1-2 times per second for smooth display updates

### Pico → Host: Status Acknowledgment (Optional)

**Message Type**: `status`

```json
{"status": "ok"}
```

Sent by Pico after successfully parsing a stats message (optional feature, not implemented by default).

## Protocol Examples

### Valid Statistics Messages

```json
{"cpu": 0, "ram": 0, "gpu": 0, "temp": 20, "network": "0KB/s"}

{"cpu": 100, "ram": 95.5, "gpu": 87.2, "temp": 85.3, "network": "500MB/s"}

{"cpu": 45.2, "ram": 62.3, "gpu": 78, "temp": 52.5, "network": "1.5MB/s"}
```

### Invalid Messages (Will Be Ignored)

```json
{"cpu": "high", "ram": 62}   // Invalid: cpu should be number

{cpu: 45.2, ram: 62.3}       // Invalid: not valid JSON (missing quotes)

cpu: 45.2\nram: 62.3         // Invalid: not JSON format
```

## Serial Communication Flow

```
Linux Computer                          Raspberry Pi Pico
────────────────                        ───────────────

stat_sender.py
    │
    ├─ Read system stats
    │
    ├─ Format JSON
    │
    └─ Send via USB serial
                                        ├─ Receive via UART
                                        │
                                        ├─ Parse JSON
                                        │
                                        ├─ Update display
                                        │
                                        └─ Optionally send ACK
    
    Repeat at configured interval (default: 1 second)
```

## Error Handling

### Pico Behavior on Invalid Data

1. **Invalid JSON**: Message is ignored, error printed to REPL
2. **Missing Fields**: Preserved stats retain previous values
3. **Serial Overflow**: Buffer limited to 256 characters, older data discarded
4. **Timeout**: No timeout - Pico waits indefinitely

### Host Behavior

1. **Connection Lost**: stat_sender.py exits with error
2. **Port Error**: Retries every 5 seconds (configurable)
3. **System Stats Error**: Uses last valid stats or shows "N/A"

## Extending the Protocol

To add new statistics:

### 1. Update Linux Sender

In `linux_sender/stat_sender.py`:

```python
def get_system_stats(self):
    stats = {
        'cpu': psutil.cpu_percent(interval=0.5),
        'ram': psutil.virtual_memory().percent,
        'gpu': self._get_gpu_usage(),
        'temp': self._get_cpu_temp(),
        'network': self._get_network_speed(),
        'disk': self._get_disk_usage(),  # NEW FIELD
    }
    return stats

def _get_disk_usage(self):
    """Get disk usage percentage"""
    disk = psutil.disk_usage('/')
    return disk.percent
```

### 2. Update Pico Firmware

In `pico_firmware/display_manager.py`:

```python
def __init__(self, lcds):
    self.stats = {
        'cpu': 'N/A',
        'ram': 'N/A',
        'gpu': 'N/A',
        'temp': 'N/A',
        'network': 'N/A',
        'disk': 'N/A',  # NEW FIELD
    }

def _display_screen_new(self, lcd):
    """Display Screen N: Disk usage"""
    disk_str = f"Disk: {self._format_stat(self.stats['disk'])}%"[:16]
    other_str = "Storage Info"[:16]
    
    lcd.clear()
    lcd.write_line(0, disk_str)
    lcd.write_line(1, other_str)
```

### 3. Update Configuration

In `pico_firmware/config.py`:

```python
# Add new display mode
STAT_ROTATION = {
    0: ['cpu', 'temp'],
    1: ['ram', 'network'],
    2: ['gpu', 'disk'],  # NEW
}
```

## Debugging

### Monitor Serial Communication

#### Using minicom (Linux)
```bash
minicom -D /dev/ttyACM0 -b 115200
```

#### Using screen (Linux)
```bash
screen /dev/ttyACM0 115200
```

#### Using pyserial (Python)
```python
import serial
ser = serial.Serial('/dev/ttyACM0', 115200)
while True:
    line = ser.readline().decode('utf-8')
    print(f"Received: {line}")
```

### Enable Debug Output

Add to `main.py`:

```python
DEBUG = True

if DEBUG:
    print(f"Received data: {data}")
    print(f"Stats: {display_manager.stats}")
```

### Test Message Send

```python
# In Thonny REPL on Pico
from serial_handler import SerialHandler
ser = SerialHandler()
ser.write_data({"cpu": 50, "ram": 60, "gpu": 70, "temp": 45, "network": "100KB/s"})
```

## Performance Considerations

- **Message Size**: ~80-100 bytes typical (well within serial buffer)
- **Throughput**: 1 message/second = ~1KB/minute (minimal bandwidth)
- **Latency**: <10ms typical (USB serial + Pico processing)
- **CPU Usage**: <1% on Pico, <2% on Linux host

## Security Notes

- No authentication/encryption (local USB connection assumed safe)
- No buffer overflow protection (length limits in place)
- No rate limiting (could DOS with rapid messages, but single host expected)
- If extended for network use, consider:
  - Message signing
  - Rate limiting
  - Data validation schemas
