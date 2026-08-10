# dynamicisland-musiconly-linuxmintxfce
Dynamic Island, but Music Only and for Linux Mint XFCE Edition (thats where i made it)

I TRIED THIS AND ONLY TESTED IT WITH YouTube Music (website version in firefox: https://music.youtube.com/)
I TESTED THIS WITH CHROME NOW AND IT WORKS WELL BUT ALSO THE WEBSITE VERSION AND I THINK IT WORKS BETTER THAN FIREFOX
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
Or, if you renamed the .py file, you can install it using:

```bash
python3 yourrenamedfilesname.py
```
## 🚀 Quick Command Shortcut

If you want to launch the Dynamic Island by typing a short command (like `island`) from anywhere in your terminal instead of typing `python3 island.py`, you can set up a shell alias.

### Setup Instructions

1. Open your shell configuration file in a text editor:
   ```bash
   nano ~/.bashrc

*(Note: If you use Zsh, open `~/.zshrc` instead)*

2. Scroll to the bottom of the file and add the following alias (make sure to update `/path/to/your/island.py` to your actual file path):
   ```bash
   alias island='python3 /path/to/your/island.py'
   ```

3. Save and exit the editor:
   * Press **Ctrl + O**, then **Enter** to save.
   * Press **Ctrl + X** to exit.

4. Apply the changes to your current terminal session:
   ```bash
   source ~/.bashrc
   ```

### Usage
Now, no matter what directory you are in, you can simply type:
```bash
island
```

## Credits & Contributors
* **stefias** - Creator & Lead Developer (Vibe Coder)
* **Gemini** - AI Assistant (helped with code debugging and structure)
