import uuid
import random
import string
import subprocess
import winreg
import ctypes

def print_banner():
    banner = """
    ****************************************
    *                                      *
    *            spoofxiz v1               *
    *                                      *
    ****************************************
    """
    print(banner)

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def spoof_mac(interface_name="Ethernet"):
    new_mac = "02:%s:%s:%s:%s:%s" % tuple(''.join(random.choices("0123456789AB", k=2)) for _ in range(5))
    print(f"[+] Spoofing MAC to {new_mac}")
    reg_path = r"SYSTEM\CurrentControlSet\Control\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\"
    for i in range(0, 100):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path + f"{i:04}", 0, winreg.KEY_ALL_ACCESS)
            desc, _ = winreg.QueryValueEx(key, "DriverDesc")
            if interface_name.lower() in desc.lower():
                winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, new_mac.replace(":", ""))
                winreg.CloseKey(key)
                print(f"[+] MAC spoofed in registry. Restart required.")
                return True
        except:
            continue
    return False

def spoof_product_id():
    new_id = ''.join(random.choices(string.digits + string.ascii_uppercase, k=20))
    print(f"[+] Spoofing Windows Product ID to: {new_id}")
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "ProductId", 0, winreg.REG_SZ, new_id)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"[!] Failed to spoof Product ID: {e}")
        return False

def spoof_volume_serial(drive='C'):
    new_serial = ''.join(random.choices(string.hexdigits, k=8)).upper()
    print(f"[+] Spoofing Volume Serial Number to: {new_serial}")
    new_serial = random.randint(10000000, 99999999)
    print(f"[~] Volume serial spoof would set to: {new_serial:08X} (simulated)")
    return True

def schedule_reboot():
    print("[*] Scheduling system reboot in 10 seconds...")
    run_cmd("shutdown /r /t 10 /f")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    print_banner()

    # Ask for user confirmation to continue
    start = input("Do you want to start the spoofing process? (y/n): ").strip().lower()
    if start != 'y':
        print("[!] Exiting...")
        return

    if not is_admin():
        print("[!] Please run as Administrator.")
        return

    print("[*] Starting Advanced HWID Spoofer...")
    spoof_mac()
    spoof_product_id()
    spoof_volume_serial()
    schedule_reboot()

if __name__ == "__main__":
    main()