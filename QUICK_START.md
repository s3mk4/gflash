# gFlash v0.3.2 - Quick Start

## What is This?

gFlash - professional utility for flashing Android devices via fastboot.

**Features:**
- ✅ Safe flashing (validation, SHA256, logging)
- ✅ Automation (configs, dry-run, watch mode)
- ✅ Backups (partition backup before flashing)
- ✅ Development (watch mode auto-flash for frequent flashing)

## Installation (Windows)

1. **Download files:**
   - `gFlash.exe`
   - `gFlash-config.exe`
   - `flash_config_example.json`

2. **Install drivers (if needed):**
   - Download Zadig: https://zadig.akeo.ie/
   - Run Zadig
   - Options → List All Devices
   - Find your device
   - Select WinUSB
   - Install Driver

3. **Done!** You can use it now

## Usage

### Option 1: Quick

```bash
# 1. Connect device in fastboot mode
# 2. Run
gFlash.exe flash boot.img boot
gFlash.exe flash system.img system
```

### Option 2: Safe (Recommended)

```bash
# 1. Create config
gFlash-config.exe my_device.json

# 2. Validate config (dry-run, no device contact)
gFlash.exe dry-run my_device.json

# 3. Save current state (insurance)
gFlash.exe backup-all my_device.json ./backups

# 4. Flash device
gFlash.exe flash-all my_device.json
```

### Option 3: Development (Frequent Flashing)

```bash
# Run and leave it
gFlash.exe watch my_device.json auto

# Turn on phone in fastboot - automatic flashing!
# All operations logged to gflash.log
```

## Help

```bash
gFlash.exe help
```

## Logging

All operations written to `gflash.log`:
```bash
# Windows
type gflash.log

# Mac/Linux
cat gflash.log
```

## Fastboot Modes

How to enable fastboot on different devices:

**Google Pixel:**
- Turn off device
- Press Volume Down + Power (~10 seconds)
- Select "Fastboot" via Volume

**Samsung:**
- Turn off device
- Press Volume Up + Bixby + Power
- Confirm Download Mode

**OnePlus:**
- Turn off device
- Press Volume Down + Power
- Select "Fastboot" via Volume

**Xiaomi:**
- Turn off device
- Press Volume Up + Power
- Select "Fastboot" via Volume

## Example Configs

See `flash_config_example.json`

## Problems?

**Q: "Device not found"**
- Check device is in fastboot mode
- Install WinUSB driver (Zadig)
- Try different USB cable

**Q: "File not found"**
- Put image files in same folder as config
- Or use absolute path in config

**Q: "Hash mismatch"**
- File is corrupted
- Download image again

## Supported Devices

All devices with fastboot mode:
- Google Pixel (all generations)
- Samsung Galaxy
- OnePlus
- Xiaomi
- Motorola
- HTC
- Sony
- And others...

## License

g-lab project

## Author

Gigachad (r4nd0mzxc)
