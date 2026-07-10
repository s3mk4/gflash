#!/usr/bin/env python3

import os
import sys
import time
import hashlib
import logging
import json
import usb.core
import usb.util
from typing import Tuple, List, Dict
from datetime import datetime

__version__ = "0.3.2"

CHUNK_SIZE = 4 * 1024 * 1024

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('gflash.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

SAFE_PARTITIONS = {"boot", "recovery", "system", "vendor", "product", "odm", "oem", "userdata", "cache", "metadata", "super", "payload", "vbmeta", "vbmeta_a", "vbmeta_b", "misc", "dtbo", "persist", "logo"}

CRITICAL_PARTITIONS = {"bootloader", "tz", "rpm", "sbl1", "aboot", "lk", "lk2", "efs", "nv", "nvdata", "modem", "mdm", "qdsp6m", "partition", "mbr", "gpt"}

class FlashConfig:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = None
        self.base_dir = os.path.dirname(os.path.abspath(config_path))
    
    def load(self) -> bool:
        if not os.path.exists(self.config_path):
            logger.error(f"Config file not found: {self.config_path}")
            return False
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Loaded config: {self.config.get('device_name', 'Unknown')}")
            return True
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")
            return False
    
    def get_device_name(self) -> str:
        return self.config.get('device_name', 'Unknown') if self.config else "Unknown"
    
    def get_partitions(self) -> List[Dict]:
        return self.config.get('partitions', []) if self.config else []
    
    def get_erase_list(self) -> List[str]:
        return self.config.get('erase_partitions', []) if self.config else []
    
    def should_reboot(self) -> bool:
        return self.config.get('post_flash_reboot', True) if self.config else True
    
    def get_reboot_mode(self) -> str:
        return self.config.get('reboot_mode', '') if self.config else ''
    
    def resolve_file_path(self, filename: str) -> str:
        if os.path.isabs(filename):
            return filename
        return os.path.join(self.base_dir, filename)
    
    def validate(self) -> Tuple[bool, str]:
        if not self.config:
            return False, "Config not loaded"
        if 'partitions' not in self.config:
            return False, "No partitions in config"
        for partition in self.config['partitions']:
            if 'name' not in partition or 'file' not in partition:
                return False, "Partition missing name or file"
            file_path = self.resolve_file_path(partition['file'])
            if not os.path.exists(file_path):
                return False, f"File not found: {partition['file']}"
        return True, "Valid"

class FastbootDevice:
    VENDOR_IDS = {0x18D1, 0x0451, 0x0502, 0x0FCE, 0x05C6, 0x22B8, 0x0955, 0x413C, 0x2314, 0x0BB4, 0x8087, 0x0489, 0x2E04, 0x0E8D}
    MAX_PACKET_SIZE = 512
    TIMEOUT_MS = 10000
    
    def __init__(self):
        self.device = None
        self.ep_out = None
        self.ep_in = None
    
    def find_device(self) -> bool:
        for vendor_id in self.VENDOR_IDS:
            devices = usb.core.find(find_all=True, idVendor=vendor_id)
            for dev in devices:
                try:
                    cfg = dev.get_active_configuration()
                    intf = cfg[(0, 0)]
                    if intf.bInterfaceClass == 0xFF:
                        self.device = dev
                        self.ep_out = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
                        self.ep_in = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
                        return True
                except:
                    continue
        return False
    
    def send_command(self, command: str) -> str:
        try:
            self.ep_out.write(command.encode() + b'\x00')
            data = self.ep_in.read(self.MAX_PACKET_SIZE, timeout=self.TIMEOUT_MS)
            return bytes(data).decode('utf-8', errors='ignore').strip()
        except Exception as e:
            logger.error(f"Command failed: {str(e)}")
            return ""
    
    def flash(self, partition: str) -> bool:
        response = self.send_command(f"flash:{partition}")
        if "OKAY" in response:
            print(f"[OK] Flashed {partition}")
            return True
        print(f"[ERROR] Flash failed")
        return False
    
    def reboot(self, mode: str = "") -> bool:
        cmd = f"reboot:{mode}" if mode else "reboot"
        response = self.send_command(cmd)
        if "OKAY" in response:
            print(f"[OK] Rebooting...")
            return True
        return False

class GFlash:
    def flash_image(self, image_path: str, partition: str) -> bool:
        if not os.path.exists(image_path):
            print(f"[ERROR] File not found: {image_path}")
            return False
        
        device = FastbootDevice()
        if not device.find_device():
            print("[ERROR] Device not found")
            return False
        
        print(f"[*] Connected to device")
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            file_hash = hashlib.sha256(image_data).hexdigest()
            print(f"[*] File SHA256: {file_hash[:16]}...")
            
            confirm = input(f"[!] Confirm flash? (yes/no): ")
            if confirm.strip().lower() != "yes":
                print("[*] Cancelled")
                return False
            
            size_hex = f"{len(image_data):08x}".lower()
            response = device.send_command(f"download:{size_hex}")
            
            if not response.startswith("DATA"):
                print(f"[ERROR] Download rejected")
                return False
            
            device.ep_out.write(image_data)
            response = device.send_command("")
            
            if response.startswith("OKAY"):
                print(f"[OK] Downloaded")
            else:
                print(f"[ERROR] Download failed")
                return False
            
            return device.flash(partition)
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return False
    
    def flash_all(self, config_path: str) -> bool:
        config = FlashConfig(config_path)
        if not config.load():
            print("[ERROR] Failed to load config")
            return False
        
        is_valid, msg = config.validate()
        if not is_valid:
            print(f"[ERROR] {msg}")
            return False
        
        print(f"[*] Device: {config.get_device_name()}")
        print(f"[*] Partitions: {len(config.get_partitions())}")
        
        confirm = input("\n[!] Proceed? (yes/no): ")
        if confirm.strip().lower() != "yes":
            return False
        
        device = FastbootDevice()
        if not device.find_device():
            print("[ERROR] Device not found")
            return False
        
        for part in config.get_partitions():
            file_path = config.resolve_file_path(part['file'])
            print(f"[*] Flashing {part['name']}...")
            if not self.flash_image(file_path, part['name']):
                if part.get('required', False):
                    print(f"[ERROR] Required partition failed!")
                    return False
        
        if config.should_reboot():
            device.reboot(config.get_reboot_mode())
        
        print(f"[OK] Done!")
        return True
    
    def dry_run(self, config_path: str) -> bool:
        config = FlashConfig(config_path)
        if not config.load():
            print("[ERROR] Failed to load config")
            return False
        
        is_valid, msg = config.validate()
        if not is_valid:
            print(f"[ERROR] {msg}")
            return False
        
        print(f"[OK] Config is valid!")
        print(f"Device: {config.get_device_name()}")
        print(f"Partitions: {len(config.get_partitions())}")
        return True
    
    def watch_device(self, config_path: str, auto_flash: bool = False) -> bool:
        config = FlashConfig(config_path)
        if not config.load():
            print("[ERROR] Failed to load config")
            return False
        
        print(f"[*] Watching for device...")
        attempt = 0
        
        try:
            while True:
                device = FastbootDevice()
                if device.find_device():
                    print(f"[OK] Device found!")
                    if auto_flash or input("Flash? (yes/no): ").lower() == "yes":
                        self.flash_all(config_path)
                        return True
                else:
                    attempt += 1
                    if attempt % 10 == 0:
                        print(f"[*] Waiting...")
                
                time.sleep(0.5)
        except KeyboardInterrupt:
            print(f"\n[*] Stopped")
            return False

def main():
    if len(sys.argv) < 2:
        print(f"gFlash v{__version__}")
        print("Usage: gflash.py <command> [args]")
        print("Commands: flash, flash-all, dry-run, watch, help")
        return
    
    gflash = GFlash()
    cmd = sys.argv[1].lower()
    
    if cmd == "flash" and len(sys.argv) >= 4:
        gflash.flash_image(sys.argv[2], sys.argv[3])
    elif cmd == "flash-all" and len(sys.argv) >= 3:
        gflash.flash_all(sys.argv[2])
    elif cmd == "dry-run" and len(sys.argv) >= 3:
        gflash.dry_run(sys.argv[2])
    elif cmd == "watch" and len(sys.argv) >= 3:
        auto = len(sys.argv) > 3 and sys.argv[3].lower() == "auto"
        gflash.watch_device(sys.argv[2], auto)
    elif cmd == "help":
        print(f"gFlash v{__version__} - Fastboot Flasher")
        print("Commands:")
        print("  flash <file> <partition>  - Flash single partition")
        print("  flash-all <config.json>   - Flash from config")
        print("  dry-run <config.json>     - Validate config")
        print("  watch <config> [auto]     - Wait for device")
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
