# TranscriptionTool

A desktop application for transcribing audio files using OpenAI's Whisper model. Built with Python and pywebview, this app provides a modern, user-friendly interface for converting audio files to text.

## Overview

TranscriptionTool is a local, offline-capable transcription application that:

- **Transcribes audio files** using whisper.cpp (a C++ port of OpenAI's Whisper)
- **Supports multiple audio formats** including WAV, MP3, M4A, AAC, OGG, FLAC, and more
- **Provides a modern web-based UI** displayed in a native window via pywebview
- **Saves transcription history** with automatic storage in JSON format
- **Works completely offline** - no internet connection required after setup

## Features

- Drag-and-drop or browse to select audio files
- Real-time progress updates during transcription
- View, copy, and manage previous transcriptions
- Dark-themed, responsive UI
- Native file dialogs
- Automatic audio conversion to optimal format for transcription

## Architecture

- **Frontend**: HTML/CSS/JavaScript with TailwindCSS (`web_view.html`)
- **Backend**: Python with pywebview for native window management (`main.py`)
- **Audio Processing**: FFmpeg for audio conversion
- **Transcription Engine**: whisper.cpp with ggml-base.en model
- **Storage**: JSON file-based storage for transcription history

## Prerequisites

- **Python 3.7+** (Python 3.8 or higher recommended)
- **pip** (Python package manager)
- **FFmpeg** - for audio conversion
- **whisper.cpp** - for transcription (requires compilation)
- **macOS, Windows, or Linux**

## Local Setup

### 1. Clone or Download the Repository

```bash
cd /path/to/Transcription\ App
```

### 2. Install Python Dependencies

```bash
pip3 install pywebview
```

**Note**: pywebview may require additional system dependencies depending on your OS:

- **macOS**: Uses native WebKit (no additional dependencies)
- **Linux**: May require `python3-gi`, `python3-gi-cairo`, `gir1.2-gtk-3.0`, `gir1.2-webkit2-4.0`
- **Windows**: Uses native Edge WebView2 (usually pre-installed on Windows 10/11)

### 3. Set Up FFmpeg

FFmpeg is required for audio conversion to the format expected by Whisper.

**Option A: Install via Package Manager (Recommended)**

- **macOS** (using Homebrew):

  ```bash
  brew install ffmpeg
  ```

- **Linux** (Ubuntu/Debian):

  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **Windows** (using Chocolatey):

  ```bash
  choco install ffmpeg
  ```

**Option B: Manual Installation**

1. Download FFmpeg for your platform from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Create the vendor directory structure:

   ```bash
   mkdir -p vendor/ffmpeg
   ```

3. Extract the `ffmpeg` executable to `vendor/ffmpeg/`
4. Make it executable (on macOS/Linux):

   ```bash
   chmod +x vendor/ffmpeg/ffmpeg
   ```

### 4. Set Up Whisper.cpp

Whisper.cpp must be compiled from source and placed in the vendor directory.

1. Clone and build whisper.cpp:

   ```bash
   git clone https://github.com/ggerganov/whisper.cpp.git
   cd whisper.cpp
   make
   ```

2. Download a Whisper model (base.en is recommended for English):

   ```bash
   bash ./models/download-ggml-model.sh base.en
   ```

   Available models: `tiny`, `tiny.en`, `base`, `base.en`, `small`, `small.en`, `medium`, `medium.en`, `large`

3. Create the vendor directory structure in your Transcription App folder:

   ```bash
   cd /path/to/Transcription\ App
   mkdir -p vendor/whisper_cpp/models
   ```

4. Copy the compiled executable and model:

   ```bash
   cp /path/to/whisper.cpp/main vendor/whisper_cpp/whisper-cli
   cp /path/to/whisper.cpp/models/ggml-base.en.bin vendor/whisper_cpp/models/
   ```

5. Make the executable runnable (on macOS/Linux):

   ```bash
   chmod +x vendor/whisper_cpp/whisper-cli
   ```

**Expected Directory Structure:**

```text
Transcription App/
├── main.py
├── web_view.html
├── transcriptions.json (created automatically)
└── vendor/
    ├── ffmpeg/
    │   └── ffmpeg (executable) - only if using manual installation
    └── whisper_cpp/
        ├── whisper-cli (executable)
        └── models/
            └── ggml-base.en.bin (model file)
```

### 5. Run the Application

```bash
python3 main.py
```

The application window should open, and you can start transcribing audio files!

## Usage

1. **Select an audio file**: Click "Browse Files" or drag and drop an audio file onto the drop zone
2. **Wait for transcription**: The app will convert the audio (if needed) and transcribe it using Whisper
3. **View results**: The transcription appears in the output area
4. **Copy or save**: Use the buttons to copy the text or save it
5. **Access history**: Click "Previous Transcriptions" in the sidebar to view past transcriptions

## Transcription Storage

Transcriptions are automatically saved to `transcriptions.json` in the app directory. Each entry includes:

- Unique ID
- Original filename and path
- File size
- Transcription text
- Timestamp
- Optional metadata

## Troubleshooting

### "FFmpeg executable not found"

- Ensure FFmpeg is in `vendor/ffmpeg/` and is executable
- Check the executable name matches `ffmpeg` (or update `FFMPEG_EXECUTABLE_NAME` in `main.py`)

### "Whisper.cpp executable not found"

- Ensure whisper.cpp is compiled and copied to `vendor/whisper_cpp/whisper-cli`
- Verify the executable has execute permissions

### "Whisper model not found"

- Download the model file and place it in `vendor/whisper_cpp/models/`
- Ensure the filename matches `ggml-base.en.bin` (or update `WHISPER_MODEL_NAME` in `main.py`)

### Window doesn't open

- Verify pywebview is installed: `pip3 show pywebview`
- Check for system-specific dependencies (see Prerequisites)

## Configuration

You can modify these settings in `main.py`:

- `WHISPER_MODEL_NAME`: Change to use different Whisper models (tiny, base, small, medium, large)
- `FFMPEG_EXECUTABLE_NAME`: Update if your FFmpeg executable has a different name
- `WHISPER_EXECUTABLE_NAME`: Update if your whisper.cpp executable has a different name

## License

See `LICENSE` file for details.