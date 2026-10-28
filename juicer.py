#!/usr/bin/env python3
"""
🍹 AI Smart Juicer Controller
Control any traditional blender/juicer using a Wi-Fi Smart Plug (Tuya/Wipro)
and Raspberry Pi with Antigravity AI.

Reads credentials securely from .env:
  PLUG_IP, PLUG_DEVICE_ID, PLUG_LOCAL_KEY, PLUG_VERSION
"""

import sys
import os
import time
import argparse
from pathlib import Path


# ==============================================================================
# 🔐 LOAD CREDENTIALS FROM .ENV (No hardcoded keys or passwords)
# ==============================================================================
def load_env():
    """Load key-value pairs from .env file without external dependencies."""
    search_paths = [
        Path(__file__).resolve().parent / ".env",
        Path(__file__).resolve().parent.parent / ".env",
        Path.cwd() / ".env"
    ]
    for env_path in search_paths:
        if env_path.exists():
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        key = key.strip()
                        val = val.strip().strip('"').strip("'")
                        if key not in os.environ:
                            os.environ[key] = val
            break

load_env()

PLUG_IP       = os.environ.get("PLUG_IP", "")
DEVICE_ID     = os.environ.get("PLUG_DEVICE_ID", "")
LOCAL_KEY     = os.environ.get("PLUG_LOCAL_KEY", "")
PLUG_VERSION  = float(os.environ.get("PLUG_VERSION", 3.5))
SAFETY_CUTOFF = 60  # Maximum run duration in seconds


# ==============================================================================
# 🔌 SMART PLUG DRIVER (Local Wi-Fi / TinyTuya)
# ==============================================================================
def get_plug():
    """Connect to the smart plug locally via TinyTuya."""
    try:
        import tinytuya
    except ImportError:
        print("❌ Error: 'tinytuya' library is not installed.")
        print("👉 Run: pip install tinytuya")
        sys.exit(1)

    if not PLUG_IP or not DEVICE_ID or not LOCAL_KEY:
        print("❌ Error: Missing credentials in .env file.")
        print("👉 Copy .env.example to .env and fill in PLUG_IP, PLUG_DEVICE_ID, and PLUG_LOCAL_KEY.")
        sys.exit(1)

    return tinytuya.OutletDevice(DEVICE_ID, PLUG_IP, LOCAL_KEY, version=PLUG_VERSION)


# ==============================================================================
# 🎮 JUICER ACTIONS
# ==============================================================================
def turn_on():
    """Turn the smart plug ON."""
    plug = get_plug()
    try:
        plug.turn_on()
        print("\n⚡ ==========================================")
        print("🍹 JUICER IS RUNNING!")
        print(f"🔌 Connected to Plug at: {PLUG_IP}")
        print("👉 Run 'python3 juicer.py off' or say 'stop' to halt.")
        print("==========================================\n")
    except Exception as e:
        print(f"❌ Failed to turn on: {e}")


def turn_off():
    """Turn the smart plug OFF."""
    plug = get_plug()
    try:
        plug.turn_off()
        print("\n🛑 ==========================================")
        print("⛔ JUICER STOPPED")
        print("🔌 Power is completely OFF.")
        print("==========================================\n")
    except Exception as e:
        print(f"❌ Failed to turn off: {e}")


def blend(seconds: int):
    """Run blender for exact duration (e.g. 15s) and automatically stop."""
    plug = get_plug()
    try:
        print(f"\n🥤 Blending for {seconds} seconds...")
        plug.turn_on()
        for remaining in range(seconds, 0, -1):
            sys.stdout.write(f"\r⏱️  Blending... {remaining:2d}s remaining ")
            sys.stdout.flush()
            time.sleep(1)
        plug.turn_off()
        print("\n✨ Done! Shake/Juice is ready! 🍓🥤\n")
    except KeyboardInterrupt:
        plug.turn_off()
        print("\n🛑 Stopped by user.")
    except Exception as e:
        plug.turn_off()
        print(f"\n❌ Error during blend: {e}")


def status():
    """Check live plug state and power telemetry (Watts, Volts, Amps)."""
    plug = get_plug()
    try:
        data = plug.status()
        if "dps" in data:
            dps = data["dps"]
            is_on = dps.get("1", False)
            voltage = dps.get("20", 0) / 10.0      # 2300 -> 230.0V
            current = dps.get("18", 0) / 1000.0    # 1500 -> 1.50A
            power = dps.get("19", 0) / 10.0        # 3500 -> 350.0W

            state_label = "🟢 ON (RUNNING)" if is_on else "🔴 OFF (STOPPED)"
            print("\n📊 ==========================================")
            print(f"🍹 Juicer State: {state_label}")
            print(f"📈 Telemetry:    {power:.1f}W | {current:.2f}A | {voltage:.1f}V")
            print("==========================================\n")
        else:
            print(f"Plug raw response: {data}")
    except Exception as e:
        print(f"❌ Could not get status: {e}")


# ==============================================================================
# 🚀 CLI ENTRYPOINT
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="AI Smart Juicer Controller")
    parser.add_argument("command", choices=["on", "off", "stop", "blend", "status"], help="Command to run")
    parser.add_argument("seconds", nargs="?", type=int, default=15, help="Blend duration in seconds (default: 15)")
    args = parser.parse_args()

    cmd = args.command.lower()
    if cmd == "on":
        turn_on()
    elif cmd in ("off", "stop"):
        turn_off()
    elif cmd == "blend":
        blend(args.seconds)
    elif cmd == "status":
        status()


if __name__ == "__main__":
    main()
