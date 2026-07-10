import subprocess
import sys
import os
import shutil

def install_deps():
    print("[*] Checking dependencies...")
    try:
        import PyInstaller
    except ImportError:
        print("[*] Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

def check_files():
    print("[*] Checking source files...")
    files = ["gflash.py", "gflash-config.py"]
    for f in files:
        if not os.path.exists(f):
            print(f"[ERROR] File not found: {f}")
            print(f"[*] Current directory: {os.getcwd()}")
            print(f"[*] Files in directory: {os.listdir('.')}")
            return False
    return True

def build_gflash():
    print("[*] Building gFlash.exe...")
    
    script_path = os.path.abspath("gflash.py")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "gFlash",
        "--distpath", "dist",
        "--workpath", "build",
        "--specpath", ".",
        "--hidden-import=usb",
        "--hidden-import=usb.backend.libusb1",
        script_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("[OK] gFlash.exe built successfully!")
        return True
    else:
        print(f"[ERROR] Build failed:\n{result.stderr}")
        return False

def build_config():
    print("[*] Building gFlash-config.exe...")
    
    script_path = os.path.abspath("gflash-config.py")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "gFlash-config",
        "--distpath", "dist",
        "--workpath", "build",
        "--specpath", ".",
        script_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("[OK] gFlash-config.exe built successfully!")
        return True
    else:
        print(f"[ERROR] Build failed:\n{result.stderr}")
        return False

def cleanup():
    print("[*] Cleaning up build artifacts...")
    if os.path.exists("build"):
        shutil.rmtree("build", ignore_errors=True)
    for spec in ["gFlash.spec", "gFlash-config.spec"]:
        if os.path.exists(spec):
            os.remove(spec)
    print("[OK] Cleanup complete")

if __name__ == "__main__":
    try:
        print(f"[*] Working directory: {os.getcwd()}")
        
        install_deps()
        
        if not check_files():
            sys.exit(1)
        
        if build_gflash() and build_config():
            cleanup()
            
            print("\n" + "="*60)
            print("BUILD SUCCESSFUL!")
            print("="*60)
            print("\nExecutables created in ./dist/")
            print("  - gFlash.exe")
            print("  - gFlash-config.exe")
            print("\nUsage:")
            print("  gFlash.exe help")
            print("  gFlash.exe dry-run config.json")
            print("  gFlash.exe flash-all config.json")
            print("  gFlash-config.exe")
            print("="*60)
        else:
            print("[ERROR] Build failed!")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)
