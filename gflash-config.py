#!/usr/bin/env python3

import os
import sys
import json
from typing import List, Dict, Optional

def get_input(prompt: str, default: str = "") -> str:
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "
    
    result = input(full_prompt).strip()
    return result if result else default

def get_yes_no(prompt: str, default: bool = True) -> bool:
    default_str = "Y/n" if default else "y/N"
    result = input(f"{prompt} [{default_str}]: ").strip().lower()
    
    if result in ('y', 'yes'):
        return True
    elif result in ('n', 'no'):
        return False
    else:
        return default

def add_partition() -> Dict:
    print("\n[*] Adding new partition...")
    
    name = get_input("[?] Partition name (e.g., boot, system, recovery)")
    if not name:
        print("[ERROR] Partition name cannot be empty")
        return None
    
    file_path = get_input("[?] Image file path (relative or absolute)")
    if not file_path:
        print("[ERROR] File path cannot be empty")
        return None
    
    required = get_yes_no("[?] Is this partition required?", True)
    description = get_input("[?] Description (optional)", "")
    sha256 = get_input("[?] SHA256 hash for verification (optional)", "")
    
    partition = {
        "name": name,
        "file": file_path,
        "required": required
    }
    
    if description:
        partition["description"] = description
    
    if sha256:
        partition["sha256"] = sha256
    
    return partition

def add_erase_partition(existing: List[str]) -> Optional[str]:
    print("\n[*] Adding partition to erase...")
    
    partition = get_input("[?] Partition name to erase (e.g., cache, userdata)")
    if not partition:
        return None
    
    if partition in existing:
        print("[WARNING] This partition is already in the erase list")
        return None
    
    return partition

def create_config() -> Dict:
    print("\n" + "="*60)
    print("gFlash Config Creator v0.3.1")
    print("="*60)
    
    device_name = get_input("\n[?] Device name", "My Android Device")
    description = get_input("[?] Configuration description", "Android device flash configuration")
    
    partitions = []
    while True:
        partition = add_partition()
        if partition:
            partitions.append(partition)
            print(f"[OK] Added partition: {partition['name']}")
        
        if not get_yes_no("\n[?] Add another partition?", True):
            break
    
    if not partitions:
        print("[ERROR] At least one partition is required")
        return None
    
    erase_partitions = []
    if get_yes_no("\n[?] Add partitions to erase after flash?", False):
        while True:
            erase_part = add_erase_partition(erase_partitions)
            if erase_part:
                erase_partitions.append(erase_part)
                print(f"[OK] Added erase partition: {erase_part}")
            
            if not get_yes_no("[?] Add another erase partition?", True):
                break
    
    post_flash_reboot = get_yes_no("\n[?] Reboot device after flash?", True)
    
    reboot_mode = ""
    if post_flash_reboot:
        print("\n[*] Reboot modes: bootloader, recovery, userspace, or leave empty for normal reboot")
        reboot_mode = get_input("[?] Reboot mode", "")
    
    config = {
        "device_name": device_name,
        "description": description,
        "version": "1.0",
        "partitions": partitions
    }
    
    if erase_partitions:
        config["erase_partitions"] = erase_partitions
    
    config["post_flash_reboot"] = post_flash_reboot
    
    if reboot_mode:
        config["reboot_mode"] = reboot_mode
    
    return config

def save_config(config: Dict, file_path: str) -> bool:
    try:
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save config: {str(e)}")
        return False

def print_summary(config: Dict):
    print("\n" + "="*60)
    print("Configuration Summary")
    print("="*60)
    
    print(f"\nDevice: {config.get('device_name', 'Unknown')}")
    print(f"Description: {config.get('description', 'N/A')}")
    
    partitions = config.get('partitions', [])
    print(f"\nPartitions ({len(partitions)}):")
    for i, part in enumerate(partitions, 1):
        status = "REQUIRED" if part.get('required', False) else "OPTIONAL"
        print(f"  {i}. {part['name']:20} | {part['file']:30} | {status}")
    
    erase_list = config.get('erase_partitions', [])
    if erase_list:
        print(f"\nErase partitions ({len(erase_list)}):")
        for part in erase_list:
            print(f"  - {part}")
    
    reboot = config.get('post_flash_reboot', False)
    if reboot:
        mode = config.get('reboot_mode', '')
        mode_str = f" ({mode})" if mode else ""
        print(f"\nPost-flash reboot: Yes{mode_str}")
    else:
        print(f"\nPost-flash reboot: No")
    
    print("\n" + "="*60)

def main():
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = get_input("\n[?] Output config file path", "flash_config.json")
    
    if not output_file:
        print("[ERROR] Output file path cannot be empty")
        return
    
    if os.path.exists(output_file):
        if not get_yes_no(f"[!] File {output_file} already exists. Overwrite?", False):
            print("[ERROR] Cancelled")
            return
    
    config = create_config()
    if not config:
        print("[ERROR] Failed to create configuration")
        return
    
    print_summary(config)
    
    if not get_yes_no("\n[?] Save this configuration?", True):
        print("[ERROR] Cancelled")
        return
    
    if save_config(config, output_file):
        print(f"\n[OK] Configuration saved to {output_file}")
        print(f"[*] You can now use: gflash.py dry-run {output_file}")
        print(f"[*] Then: gflash.py flash-all {output_file}")
    else:
        print("[ERROR] Failed to save configuration")

if __name__ == "__main__":
    main()
