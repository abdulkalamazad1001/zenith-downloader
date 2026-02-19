<div align="center">

# ⚡ ZENITH DOWNLOADER
### Experience Media at its Peak

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-black?style=for-the-badge&logo=flask&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-green?style=for-the-badge&logo=ffmpeg&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

<p align="center">
  <strong>The Ultimate Local Media Downloader for YouTube, Instagram, and X (Twitter).</strong>
</p>

[Features](#-features) • [Installation](#-quick-start) • [How It Works](#-under-the-hood) • [Troubleshooting](#-troubleshooting)

</div>

---

## 🌟 Why Zenith?

Most online downloaders are filled with ads, pop-ups, and slow speeds. Cloud-based downloaders get blocked by YouTube. 
**Zenith is different.** It runs **locally on your machine**, giving you:
*   🚀 **Unlimited Speed:** Downloads as fast as your internet allows.
*   🛡️ **Privacy:** No data leaves your computer.
*   � **No Blocking:** Bypasses "Sign in to confirm you’re not a bot" errors by using your own residential IP.
*   ✨ **Premium UI:** A beautiful, dark-mode Glassmorphism interface.

## ✨ Features

*   **Multi-Platform Support**: 
    *   🟥 **YouTube**: Videos (up to 4K), Shorts, and Audio.
    *   📸 **Instagram**: Reels and Videos.
    *   ✖️ **X (Twitter)**: High-quality videos.
*   **Smart Quality Selection**: Choose from 1080p, 720p, or just the Audio.
*   **Auto-Conversion**: Extracts high-quality MP3s from any video link.
*   **Real-Time Progress**: Watch the download bar fill up in real-time.
*   **History**: Keeps track of your recent downloads locally.

---

## 🚀 Quick Start (Windows)

We've made it incredibly easy. You don't need to know code to run this.

### Step 1: Install FFmpeg (One-Time Setup)
Zenith needs **FFmpeg** to merge high-quality video and audio content.
1.  Open the project folder.
2.  Right-click **`install_ffmpeg.ps1`**.
3.  Select **"Run with PowerShell"**.
4.  Wait for it to finish. (It will download and configure everything for you).

### Step 2: Launch the App
1.  Double-click **`run_locally.bat`**.
2.  Wait a moment for it to update dependencies.
3.  **The app will automatically open in your browser!** 

---

## 🚀 Quick Start (Mac & Linux)

### 1. Install FFmpeg
*   **Mac**: Open Terminal and run `brew install ffmpeg`.
*   **Linux**: Run `sudo apt install ffmpeg` (or your distro's equivalent).

### 2. Run the App
1.  Open Terminal in the project folder.
2.  Run this command to start:
    ```bash
    chmod +x run_mac_linux.sh && ./run_mac_linux.sh
    ```
3.  The app will open in your browser!

---

## 🧠 Under the Hood

Zenith is powered by a robust stack:
*   **Backend**: `Flask` (Python) handles the logic and server.
*   **Engine**: `yt-dlp` (Bleeding-edge Git version) interacts with media providers.
*   **Processing**: `FFmpeg` merges separate video/audio streams into a perfect `.mp4` file.
*   **Frontend**: Vanilla JS + CSS for a lightweight, snappy experience.

---

## � Troubleshooting

**Q: The window closes immediately when I run `run_locally.bat`.**
*   **Fix**: Try running it as Administrator once, or open a Command Prompt in the folder and type `run_locally.bat` to see the error message.

**Q: "FFmpeg not found" error?**
*   **Fix**: Run the `install_ffmpeg.ps1` script again. If that fails, [download FFmpeg manually](https://ffmpeg.org/download.html) and add it to your system PATH.

**Q: Download stuck at 0%?**
*   **Fix**: Check your internet. If it's a very long video, it might take a moment to start.

---

## 👨‍� Contributing

Found a bug? Want to add a feature?
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

---

<div align="center">
  <sub>Built by <b>Abdul Kalam Azad</b></sub>
</div>
