# gFlash v0.3.2 - Build Instructions

## Requirements

- Python 3.7+
- pip

## Quick Build

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Build exe
python build.py
```

Done! Files will be in `dist/`:
- `gFlash.exe` - main utility
- `gFlash-config.exe` - configurator

## Command Line Usage

```bash
# Show help
gFlash.exe help

# Create config
gFlash-config.exe my_config.json

# Validate config
gFlash.exe dry-run my_config.json

# Save current state
gFlash.exe backup-all my_config.json ./backups

# Flash device
gFlash.exe flash-all my_config.json

# Watch mode (wait for connection)
gFlash.exe watch my_config.json auto
```

## Build Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'usb'"

**Solution:** install libusb drivers
```bash
pip install pyusb
# Or on Linux:
sudo apt-get install libusb-1.0-0
```

### Problem: PyInstaller not installed

**Solution:** script will install it automatically
```bash
pip install pyinstaller
python build.py
```

### Problem: "usb backend not found"

Need to install WinUSB driver via Zadig:
1. Download Zadig: https://zadig.akeo.ie/
2. Run Zadig
3. Options → List All Devices
4. Select Android device
5. Select WinUSB driver
6. Install Driver

## Distribution

Just distribute files from `dist/`:
- `gFlash.exe`
- `gFlash-config.exe`
- `flash_config_example.json`
- `README.md`

No Python or dependencies needed!

## Building on Mac/Linux

```bash
# Install dependencies
pip install -r requirements.txt

# Build for your platform
python build.py
```

Output: `dist/gFlash` and `dist/gFlash-config`

## GitHub Actions

For automated builds on release:

Create `.github/workflows/build.yml`:

```yaml
name: Build Executables

on:
  release:
    types: [created]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python build.py
      - uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ github.event.release.upload_url }}
          asset_path: ./dist/gFlash.exe
          asset_name: gFlash.exe
          asset_content_type: application/octet-stream
```

## License

g-lab project
