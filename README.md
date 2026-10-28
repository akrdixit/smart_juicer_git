# 🍹 AI Smart Juicer: Automating Any Blender with Raspberry Pi, Antigravity AI & Smart Plug

> **Turn any standard kitchen blender or juicer into a smart, AI-voice/chat-controlled appliance using a Raspberry Pi and an affordable Wi-Fi Smart Plug — with zero cloud lag, zero subscriptions, and 100% local control!**

---

## 📌 How It Works

1. **The Juicer**: Any traditional blender or juicer with a mechanical switch (kept permanently in the **ON** position).
2. **The Smart Plug**: An affordable Tuya-based 16A smart plug (Wipro, Syska, Gosund, Smart Life, etc.) controls the AC wall power.
3. **The Raspberry Pi**: Communicates with the smart plug directly over your local Wi-Fi router using the `tinytuya` protocol (AES-128 encryption on port 6668).
4. **Google Antigravity AI**: Listens for your voice or chat commands (e.g. *"Hey, make strawberry shake"* or *"Stop"*) and automatically triggers the Python script on your Pi.

---

## 🛠️ Requirements

- **Raspberry Pi** (Pi 5, Pi 4, or Pi Zero 2W)
- **Wi-Fi Smart Plug** (16Amp recommended for heavy blenders, Tuya/Smart Life compatible)
- **Juicer / Blender** with a mechanical rocker or rotary switch
- **Python 3** with `tinytuya` installed:
  ```bash
  pip install tinytuya
  ```

---

## 🔑 How to Register & Get Your Smart Plug Keys (TinyTuya)

Tuya devices communicate locally using an encrypted **Local Key**. You only need to perform this setup once to extract your key:

### 1. Pair Plug in Mobile App
1. Plug your Smart Plug into the wall.
2. Open the **Smart Life** (or **Tuya Smart**) app on your phone.
3. Put the plug in pairing mode (press & hold the button for 5 seconds until it flashes).
4. Connect it to your **2.4 GHz Wi-Fi** network.

### 2. Create a Free Tuya Developer Account
1. Go to [iot.tuya.com](https://iot.tuya.com/) and sign up for a free developer account.
2. In the left sidebar, click **Cloud** ➔ **Development** ➔ **Create Cloud Project**.
3. Enter a project name (e.g., `Smart Home`), choose your country's data center, and select the default API services (*IoT Core*, *Authorization*, *Smart Home Device System*).

### 3. Link Your Mobile App
1. Inside your Cloud Project, go to the **Link Tuya App Account** tab.
2. Click **Add App Account** — a **QR code** will appear on your screen.
3. In your phone's **Smart Life** app, go to **Me** (Profile) ➔ tap the **Scan icon [ - ]** in the top right.
4. Scan the QR code and confirm the link.

### 4. Run the TinyTuya Wizard to Extract Keys
1. In your terminal on your computer or Raspberry Pi, run:
   ```bash
   python3 -m tinytuya wizard
   ```
2. When prompted, enter:
   - **API Key (Access ID)**: Copied from your Tuya Cloud Project overview page.
   - **API Secret (Access Secret)**: Copied from your Tuya Cloud Project overview page.
   - **Region**: Your region code (e.g. `us`, `eu`, `in`).
3. TinyTuya will scan your account and output your device details:
   - **Device ID**: (e.g. `bf76xxxxxxxxxxxx`)
   - **Local Key**: (e.g. `a1b2c3d4e5f6g7h8`)
   - **IP Address**: (e.g. `192.168.1.100`)

---

## ⚙️ Setup & Configuration

### 1. Configure `.env`
Copy the example environment file:
```bash
cp .env.example .env
```

Open `.env` in any text editor and fill in your details:
```env
PLUG_IP=192.168.1.100
PLUG_DEVICE_ID=your_device_id_here
PLUG_LOCAL_KEY=your_16_char_local_key_here
PLUG_VERSION=3.5
```
*(Note: `.env` is listed in `.gitignore` so your secrets and IP addresses are never committed to GitHub).*

---

## 🚀 Running the Juicer

### 1. Power ON
Powers on the juicer:
```bash
python3 juicer.py on
```

### 2. Timed Blend (Smoothie / Shake Mode)
Runs the blender for a specified number of seconds (e.g., 15s) with a live countdown, then automatically turns off:
```bash
python3 juicer.py blend 15
```

### 3. Power OFF / Stop
Immediately cuts power to the juicer:
```bash
python3 juicer.py off
# or
python3 juicer.py stop
```

### 4. Check Power Telemetry & Status
Shows whether the appliance is currently running, along with real-time **Watts**, **Amps**, and **Volts**:
```bash
python3 juicer.py status
```

---

## 🤖 Antigravity AI Agent Integration

You can integrate this with the **Google Antigravity Agent** by adding a trigger in your agent instructions (`AGENTS.md`):

```markdown
### Smart Juicer Commands:
- When user says "make strawberry shake" or "start juicer":
  Execute: `python3 smart_juicer/juicer.py blend 15`
- When user says "stop" or "turn off":
  Execute: `python3 smart_juicer/juicer.py off`
```

Whenever you speak or type to Antigravity, the AI agent autonomously runs the script locally on your Raspberry Pi!

---

## 🛡️ Safety Tips

- **16A Smart Plug**: Always use a 16Amp rated smart plug for kitchen appliances with heavy electric motors.
- **Auto-Stop**: Use the `blend <seconds>` command to ensure the blender stops automatically and never runs unattended.
- **Mechanical Switch**: Ensure the lid is securely closed before turning on power.
