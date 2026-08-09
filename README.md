# dynamicisland-musiconly-linuxmintxfce
Dynamic Island, but Music Only and for Linux Mint XFCE Edition (thats where i made it)

I TRIED THIS AND ONLY TESTED IT WITH YouTube Music (website version in firefox: https://music.youtube.com/)
**AND GUYS DONT BE MAD BUT I USED GEMINI AI (HATE ME ALL YOU WANT)**

**Note:** The time could be a bit glitched, but just pause the music in the Dynamic Island then play it again to fix it.

**virustotal.com results: https://www.virustotal.com/gui/file/2bd4fd656e8ea40d1355c40037a3ee36d0b2573b5b173a92ce944d2810e5a120?nocache=1**

## Requirements

### Software Dependencies
* **Python 3**
* **PyQt5**
* **dbus-python**

### PC Requirements
* **CPU:** Any multi-core processor (virtually zero CPU usage)
* **RAM:** 1 GB or higher
* **Storage:** Less than 10 MB free space
* **OS:** Linux (tested on Linux Mint XFCE Edition with active D-Bus session)
* **Media Player:** An MPRIS-compatible player or browser session (e.g., Firefox with YouTube Music)

## Installation

For Linux Mint, Ubuntu, or Debian users, it is recommended to install the dependencies using your system package manager to avoid header compilation issues:

```bash
sudo apt update
sudo apt install python3-pyqt5 python3-dbus
```

Alternatively, you can install them using pip:

```bash
pip install PyQt5 dbus-python
```

## How to Run

```bash
python3 island.py
```
## Credits & Contributors
* **stefias** - Creator & Lead Developer (Vibe Coder)
* **Gemini** - AI Assistant (helped with code debugging and structure)
