# Development Plan: Local Whisper Transcription App

This document outlines the development phases and steps to create the Local Whisper Transcription App, integrating the UI and functionality specified in `examplecode.html`. Each step includes a suggested prompt for an AI coding assistant.

**Project Root:** `/Users/haydengroover/Documents/Transcription App/`

## Phase 1: Project Setup & Basic Electron Shell

### Step 1.1: Initialize Project and Install Core Dependencies

* **Description:** Set up the project directory, initialize `package.json`, and install Electron, React, and other foundational libraries.
* **Prompt for AI Assistant:**

    Initialize a new Node.js project in `/Users/haydengroover/Documents/Transcription App/`. Then, install the following core dependencies using npm:
  * electron (as a dev dependency)
  * react
  * react-dom

    Also, set up a basic `.gitignore` file suitable for a Node.js/Electron project.

### Step 1.2: Create Basic Electron Application Structure

* **Description:** Create the main Electron files (`main.js`, `preload.js`) and a minimal HTML file for the renderer process, as React will manage the UI.
* **Prompt for AI Assistant:**

    In the project `/Users/haydengroover/Documents/Transcription App/`, create the following Electron application structure:
    1. `main.js`:
        * Should handle app lifecycle events (ready, window-all-closed, activate).
        * Create a `BrowserWindow` with dimensions 1200x800, frameless (or with custom traffic lights if feasible later).
        * Load `index.html` into the `BrowserWindow`.
        * Include a basic `preload.js` script.
    2. `preload.js`:
        * Set up `contextBridge` to expose a simple test function to the renderer process (e.g., `electronAPI.ping()`).
    3. `index.html` (in a `src/renderer` directory):
        * Minimal HTML structure with a `div` with `id="root"` for React to mount.
        * A script tag to load the bundled React app (e.g., `renderer.js`).
    4. Update `package.json` `main` entry to `main.js` and add a script to start Electron (e.g., `"start": "electron ."`).

### Step 1.3: Implement Basic Inter-Process Communication (IPC)

* **Description:** Establish basic IPC between the main and renderer processes for future interactions.
* **Prompt for AI Assistant:**

    In the Electron project at `/Users/haydengroover/Documents/Transcription App/`:
    1. In `main.js`, set up an `ipcMain.handle` listener for a channel (e.g., `'test-ping'`) that returns a simple string (e.g., 'pong').
    2. In `preload.js`, expose a function (e.g., `window.electronAPI.sendTestPing = () => ipcRenderer.invoke('test-ping')`) that calls this IPC channel.
    3. In a temporary test within the initial React `App.jsx`, add a button that, when clicked, calls `window.electronAPI.sendTestPing()` and logs the result to the console.

## Phase 2: Frontend UI Development (React) - Integrating `examplecode.html`

### Step 2.1: Setup React with Vite, TailwindCSS, and Font Awesome

* **Description:** Integrate React into the Electron renderer process using Vite, and set up TailwindCSS and Font Awesome to match `examplecode.html`.
* **Prompt for AI Assistant:**

    Integrate React with Vite, TailwindCSS, and Font Awesome into the Electron project at `/Users/haydengroover/Documents/Transcription App/`.
    1. Set up Vite to manage the React code in the `src/renderer` directory.
    2. Install and configure TailwindCSS for the project, ensuring it processes styles for React components. Refer to `examplecode.html` for Tailwind CDN usage and replicate its setup locally.
    3. Install Font Awesome for React (e.g., `@fortawesome/react-fontawesome` and relevant icon packs) to use icons as seen in `examplecode.html`.
    4. Create a basic `App.jsx` component in `src/renderer/` that will serve as the root for the UI.
    5. Ensure `src/renderer/index.html` correctly loads the Vite-bundled JavaScript.
    6. Modify Electron's `main.js` to load the Vite dev server URL in development and the built `index.html` in production.
    7. Update `package.json` with scripts for running Vite dev server and building the React app.

### Step 2.2: Convert `examplecode.html` Structure to React Components

* **Description:** Convert the static `examplecode.html` into a structure of reusable React components, replicating its layout, styling, and basic client-side interactions.
* **Prompt for AI Assistant:**

    In the React application (`src/renderer/`) of the Electron project, convert `examplecode.html` into a component-based structure:
    1. Main `App.jsx` component to hold the overall layout (sidebar and main content area).
    2. `Sidebar.jsx`: For navigation links ('Active Transcription', 'Previous', 'Account', 'Settings'). Implement active link styling.
    3. `Header.jsx`: For the top bar, including placeholder window controls and the current view title.
    4. View Components (initially, 'Active Transcription' is primary, others are placeholders):
        * `ActiveTranscriptionView.jsx`: Contains sections for file input, status/progress, and output.
        * `PreviousView.jsx`, `AccountView.jsx`, `SettingsView.jsx`: Placeholder components.
    5. `Modal.jsx`: For displaying messages (e.g., errors, success notifications).
    6. Replicate all HTML structure and apply TailwindCSS classes from `examplecode.html` to these components.
    7. Implement the custom scrollbar styles and ensure the Inter font is correctly applied as per `examplecode.html`.
    8. The initial state should show the 'Active Transcription' view.

### Step 2.3: Implement File Selection (Browse & Drag-and-Drop)

* **Description:** Implement audio file selection via a browse button and drag-and-drop area, matching `examplecode.html`.
* **Prompt for AI Assistant:**

    In the `ActiveTranscriptionView.jsx` component:
    1. Implement the 'Click to Browse' button. When clicked, it should trigger an IPC call to `main.js` (exposed via `preload.js`, e.g., `window.electronAPI.openFileDialog()`) to open a system file dialog. The dialog should filter for audio files (mp3, wav, m4a, etc.).
    2. Implement the drag-and-drop area:
        * It should accept audio files.
        * Provide visual feedback on drag over/leave (e.g., border style changes as in `examplecode.html`).
        * On drop, get the file path.
    3. When a file is selected (either by browse or drag-and-drop):
        * Update the UI to display the selected file name (e.g., 'Current File: audio.mp3').
        * Enable the 'Start Transcription' button.
        * If an invalid file type is selected, show an error message using the Modal component.
    4. Expose `dialog.showOpenDialog` from `main.js` via `preload.js` and `contextBridge`.

### Step 2.4: Implement Tab Navigation System

* **Description:** Enable navigation between different views using the sidebar links, as shown in `examplecode.html`.
* **Prompt for AI Assistant:**

    In the React application:
    1. Implement the logic in `App.jsx` or a context provider to manage the currently active view.
    2. When a link in `Sidebar.jsx` is clicked:
        a. Update the active view state.
        b. The main content area should render the corresponding view component (`ActiveTranscriptionView`, `PreviousView`, etc.).
        c. The clicked link in the sidebar should get an 'active' style (e.g., `sidebar-link-active`).
        d. The title in `Header.jsx` should update to reflect the current view (e.g., 'Active Transcription', 'Settings').
    3. Ensure the 'Active Transcription' view is shown by default.

### Step 2.5: Implement Transcription UI Elements (Status, Progress, Output)

* **Description:** Implement the UI elements for displaying transcription status, progress, and the final text, including copy/save buttons and the message modal, as per `examplecode.html`.
* **Prompt for AI Assistant:**

    In `ActiveTranscriptionView.jsx`:
    1. Implement state variables to manage:
        * Status text (e.g., 'Ready', 'Converting audio...', 'Transcribing...').
        * Progress bar percentage (0-100%).
        * Transcription output text.
        * Selected file object/path.
    2. Render these states in their respective UI elements (status paragraph, progress bar div, textarea for output).
    3. Implement the 'Start Transcription' button. Initially, it should be disabled and enabled only when a file is selected.
    4. Implement 'Copy Text' and 'Save As...' buttons. For now, 'Copy Text' can copy the content of the textarea to the clipboard. 'Save As...' will require IPC to `main.js` (to be detailed in Phase 5).
    5. Ensure the message modal (`Modal.jsx`) can be triggered to show messages (e.g., 'Transcription complete!', 'Error copying text').
    6. The transcription output textarea should be read-only.
    7. The UI should match `examplecode.html`'s simulated states (e.g., initial state, during conversion, during transcription, completed).

## Phase 3: Backend Core - Audio Processing Setup (`ffmpeg`)

### Step 3.1: Setup Worker Thread for Background Tasks

* **Description:** Implement the ability to run tasks in a separate Node.js worker thread to avoid freezing the UI.
* **Prompt for AI Assistant:**

    In the Electron project's `main.js` at `/Users/haydengroover/Documents/Transcription App/`:
    1. Create a function to spawn a Node.js `worker_threads` Worker (e.g., `audioWorker.js`).
    2. Set up IPC between `main.js` and the worker script using `parentPort.postMessage` and `worker.on('message')`.
    3. Create a basic `audioWorker.js` file that can receive a message, perform a simple task (e.g., echo the message back after a delay), and post a result/progress/error back to `main.js`.
    4. `main.js` should then forward these communications to the renderer process via its own IPC channels.

### Step 3.2: `ffmpeg` Integration - Audio Conversion Module

* **Description:** Create a module to handle audio conversion using `ffmpeg`. This includes bundling `ffmpeg` and calling it as a child process.
* **Prompt for AI Assistant:**

    In the Electron project at `/Users/haydengroover/Documents/Transcription App/`:
    1. Create a new JavaScript module (e.g., `src/main/audioConverter.js`).
    2. This module should export a function that takes an input audio file path and an output file path.
    3. The function should use Node.js `child_process.spawn` to execute a bundled `ffmpeg` command.
        * The command should convert the input audio to a 16-bit, 16kHz mono WAV file at the specified output path.
        * Example `ffmpeg` flags: `-i <input> -ar 16000 -ac 1 -c:a pcm_s16le <output>.wav`
    4. The function should return a Promise that resolves with the output path on successful conversion or rejects with an error. It should also be able to emit progress events (e.g. using an event emitter or callbacks passed to it, which the worker can then relay).
    5. Handle `ffmpeg`'s stdout/stderr for progress or error messages to be relayed.
    6. Address bundling `ffmpeg` later (Phase 7). For now, assume `ffmpeg` is in PATH or a known relative location for development.

### Step 3.3: Integrate `ffmpeg` Module with Worker Thread

* **Description:** Call the `ffmpeg` audio conversion module from the worker thread and relay progress/results.
* **Prompt for AI Assistant:**

    In the Electron project's `audioWorker.js` at `/Users/haydengroover/Documents/Transcription App/`:
    1. When it receives a message with an audio file path from `main.js` to start conversion:
        a.  Call the `audioConverter.js` module to convert the audio file.
        b.  The output WAV file should be saved to a temporary location (e.g., using `app.getPath('temp')`).
        c.  Send progress messages (e.g., `{ type: 'conversion-progress', data: { percent: 25, step: 'Converting audio...' } }`) and the final WAV file path (or an error object `{ type: 'conversion-error', data: { message: '...' } }`) back to `main.js` via `parentPort.postMessage`.
    2. `main.js` should then forward these messages to the renderer process.

## Phase 4: Backend Core - Transcription Engine Setup (`whisper.cpp`)

### Step 4.1: `whisper.cpp` Integration - Transcription Module

* **Description:** Create a module to run `whisper.cpp` for transcription. This includes bundling `whisper.cpp` and its models.
* **Prompt for AI Assistant:**

    In the Electron project at `/Users/haydengroover/Documents/Transcription App/`:
    1. Create a new JavaScript module (e.g., `src/main/transcriber.js`).
    2. This module should export a function that takes an input WAV file path and a path to a `whisper.cpp` model.
    3. The function should use Node.js `child_process.spawn` to execute a bundled `whisper.cpp` command.
        * Example `whisper.cpp` command: `./main -m <model_path> -f <input_wav_path> -otxt` (for plain text output).
    4. The function should return a Promise that resolves with the transcribed text on success or rejects with an error. It should also be able to emit progress events.
    5. Capture `whisper.cpp`'s stdout for the transcription and stderr for progress/errors to be relayed.
    6. Address bundling `whisper.cpp` and models later (Phase 7). For now, assume executable and a model (e.g., `ggml-base.en.bin`) are in a known relative path.

### Step 4.2: Integrate `whisper.cpp` Module with Worker Thread

* **Description:** Call the `whisper.cpp` transcription module from the worker thread after audio conversion and relay progress/results.
* **Prompt for AI Assistant:**

    In the Electron project's `audioWorker.js` at `/Users/haydengroover/Documents/Transcription App/`:
    1. After the audio conversion by `ffmpeg` is successful and the worker has the path to the WAV file:
        a.  It should receive a message/signal to start transcription, including the model path.
        b.  Call the `transcriber.js` module to transcribe the WAV file using the specified model path.
        c.  Send progress messages (e.g., `{ type: 'transcription-progress', data: { percent: 25, step: 'Transcribing audio...' } }`), intermediate transcription segments if available, and the final transcribed text (or an error object) back to `main.js` via `parentPort.postMessage`.
    2. `main.js` should forward these messages to the renderer process.

### Step 4.3: Implement `whisper.cpp` Output Parsing

* **Description:** Parse the output from `whisper.cpp` if it's not plain text or requires cleaning (e.g., for timestamps as in `examplecode.html` simulation).
* **Prompt for AI Assistant:**

    Review the `whisper.cpp` output format (e.g., with flags like `-osrt` or `-ovtt` if desired for timestamps, or plain `-otxt`). In `src/main/transcriber.js`, ensure the output captured from `whisper.cpp`'s stdout is processed into a clean string or structured data (like the array of objects in `examplecode.html`'s simulation if using timed output). The goal is to match the display format shown in `examplecode.html`'s output area.

## Phase 5: Connecting Frontend to Backend & Workflow

### Step 5.1: Orchestrate Full Transcription Workflow

* **Description:** Connect the UI 'Start Transcription' button to trigger the full backend workflow: file selection -> `ffmpeg` conversion -> `whisper.cpp` transcription -> display result, aligning with `examplecode.html`'s flow.
* **Prompt for AI Assistant:**

    In the Electron project at `/Users/haydengroover/Documents/Transcription App/`:
    1. In the React UI (`ActiveTranscriptionView.jsx`), when the 'Start Transcription' button is clicked (and a file and model are selected):
        a.  Send an IPC message to `main.js` (e.g., `'transcribe-audio'`) with the selected audio file path and selected model identifier.
        b.  Disable the 'Start Transcription' button and other relevant inputs.
    2. In `main.js`, upon receiving this message:
        a.  Send a message to `audioWorker.js` to start the audio conversion process with the file path.
        b.  Once conversion is done, `main.js` (or the worker directly if orchestrated there) will trigger the transcription process in the worker, passing the WAV path and model path.
    3. Ensure `main.js` relays all progress, error, and result messages from `audioWorker.js` back to the renderer process using specific IPC channels (e.g., `conversion-progress`, `transcription-progress`, `transcription-complete`, `transcription-error`).

### Step 5.2: Display Transcription Progress and Results in UI

* **Description:** Update the React UI to show dual-phase progress messages (conversion and transcription) and the final transcription text, as per `examplecode.html`.
* **Prompt for AI Assistant:**

    In the React UI (`ActiveTranscriptionView.jsx`) of the Electron project:
    1. Set up IPC listeners (via `preload.js` and `contextBridge`, e.g., `window.electronAPI.onConversionProgress((event, data) => { ... })`) to receive messages from `main.js` regarding:
        * Conversion progress updates (percent, step message).
        * Transcription progress updates (percent, step message).
        * Final transcription result (text or structured data).
        * Errors from either stage.
    2. Update the `statusText` and `progressBar` states dynamically for both conversion and transcription phases.
    3. Update the `transcriptionText` state with the final result (formatting it as needed, e.g., with timestamps if parsed).
    4. Display error messages using the `Modal.jsx` component.
    5. Re-enable the 'Start Transcription' button and other inputs upon completion or error.

### Step 5.3: Implement Error Handling and User Feedback via Modal

* **Description:** Implement robust error handling throughout the workflow and provide clear feedback to the user using the modal component from `examplecode.html`.
* **Prompt for AI Assistant:**

    Review the entire transcription workflow in the Electron project (from UI interaction to `ffmpeg` and `whisper.cpp` execution):
    1. Ensure that errors from `child_process.spawn` (for `ffmpeg` and `whisper.cpp`), file operations, worker thread, and IPC are caught and propagated to the UI.
    2. Display user-friendly error messages in the React UI using the `Modal.jsx` component (e.g., 'Failed to convert audio', 'Transcription failed', 'File not found', 'Model not accessible').
    3. Disable/Enable UI elements (like the 'Start Transcription' button, file input) appropriately during processing and re-enable them on error or completion.

## Phase 6: Model Management

### Step 6.1: UI for Model Selection in Settings Tab

* **Description:** Add UI elements in the 'Settings' view for the user to select a `whisper.cpp` model from a list of bundled models.
* **Prompt for AI Assistant:**

    In the `SettingsView.jsx` component of the Electron project:
    1. Add a dropdown menu (or similar selector) to allow users to select a Whisper model (e.g., 'Base (English)', 'Small (English)'). These will correspond to bundled model files.
    2. Store the selected model choice in React state (possibly a global context if needed by `ActiveTranscriptionView.jsx`).
    3. For now, predefine a list of available models that will be bundled with the app (e.g., `ggml-base.en.bin`, `ggml-small.en.bin`).

### Step 6.2: Logic to Pass Selected Model to `whisper.cpp`

* **Description:** Modify the backend to use the model selected by the user via the Settings UI.
* **Prompt for AI Assistant:**

    In the Electron project:
    1. When transcription is initiated from `ActiveTranscriptionView.jsx`, it should retrieve the currently selected model identifier (from state/context reflecting the choice made in `SettingsView.jsx`).
    2. This model identifier is sent to `main.js` along with the audio file path.
    3. `main.js` passes this identifier to `audioWorker.js`.
    4. In `audioWorker.js`, map this identifier to the actual model file path (e.g., 'base.en' maps to `bin/ggml-base.en.bin`).
    5. Ensure `transcriber.js` uses this dynamically provided model path in the `whisper.cpp` command.

### Step 6.3 (Optional): Implement Model Downloading/Management

* **Description:** (Advanced - Defer) Allow users to download models if they don't have them, or manage existing models.
* **Prompt for AI Assistant:**

    (Optional Advanced Feature - Defer to a future version) In the Electron project:
    1. Design a system for managing Whisper models beyond bundled ones.
    2. In `main.js`, add functionality to check if a selected model file exists locally.
    3. If not, provide an option in the UI (perhaps Settings) to download it (e.g., from Hugging Face) using Node.js `https.get` or a library like `axios` or `electron-dl`.
    4. Show download progress in the UI (e.g., in the Settings tab or a global status area).
    5. Store downloaded models in a designated application support directory (e.g., `app.getPath('userData') + '/models'`).

## Phase 7: Build, Packaging, and Testing

### Step 7.1: Configure `electron-builder` or `electron-forge`

* **Description:** Set up `electron-builder` (or `electron-forge`) to package the application, including bundling `ffmpeg`, `whisper.cpp`, and default models.
* **Prompt for AI Assistant:**

    Integrate `electron-builder` into the Electron project at `/Users/haydengroover/Documents/Transcription App/`.
    1. Install `electron-builder` as a dev dependency.
    2. Configure `electron-builder` in `package.json` or an `electron-builder.yml` file.
    3. Ensure that `ffmpeg` and `whisper.cpp` executables, along with the default selected Whisper model files (e.g., `ggml-base.en.bin`), are correctly bundled as external resources (`extraResources` or `asarUnpack`) and are accessible at runtime.
    4. Adjust paths in `audioConverter.js` and `transcriber.js` to correctly locate these bundled executables and models at runtime (e.g., using `process.resourcesPath` or similar logic for packaged apps).
    5. Add build scripts to `package.json` for macOS, Windows, and Linux.

### Step 7.2: Implement Basic Unit/Integration Tests

* **Description:** Write basic tests for critical functions (e.g., utility functions, IPC handlers if possible, simple component rendering).
* **Prompt for AI Assistant:**

    Set up a testing framework (e.g., Jest or Vitest with React Testing Library) in the Electron project.
    1. Write unit tests for any pure JavaScript utility functions (e.g., path manipulation, text formatting).
    2. Write basic React component rendering tests for key UI elements (e.g., does `Sidebar.jsx` render its links? Does `ActiveTranscriptionView.jsx` render its buttons?).
    3. If feasible, write basic integration tests for IPC communication or module interactions (mocking child processes and Electron APIs).

### Step 7.3: Perform Manual End-to-End Testing

* **Description:** Manually test the application on target platforms to ensure full functionality, paying close attention to the UI/UX from `examplecode.html`.
* **Prompt for AI Assistant:**

    Provide a checklist of core functionalities to test for the Local Whisper Transcription App, covering:
  * Application launch and initial UI state (Active Transcription view shown).
  * File selection (Browse button and Drag & Drop for various audio types).
  * Visual feedback during drag & drop.
  * Tab navigation via sidebar: switching views, header title updates, active link styling.
  * Model selection in Settings tab and its effect on transcription.
  * Full transcription process: initiation, dual-phase progress display (conversion & transcription), completion message via modal.
  * Correctness of transcribed text displayed in the textarea.
  * Copy Text and Save As functionality (Save As might be mocked if full implementation is complex).
  * Error handling: invalid file type, failed conversion, failed transcription, displayed via modal.
  * UI responsiveness during transcription; button disabling/enabling.
  * Test on different platforms if possible (macOS, Windows, Linux) after building.

### Step 7.4: Create Application Build

* **Description:** Generate distributable application packages.
* **Prompt for AI Assistant:**

    Using the configured `electron-builder` setup in the project, run the build commands to generate application packages for macOS, Windows, and Linux. List the commands to execute.

### Step 7.5: UI/UX and Functionality Review against `examplecode.html`

* **Description:** Perform a dedicated review to ensure the implemented React application faithfully reproduces the design, interactions, and simulated workflow of `examplecode.html`.
* **Prompt for AI Assistant:**

    Provide a detailed checklist for comparing the final application's UI and UX against the `examplecode.html` specification. This should cover:
  * Visual fidelity: layout, colors (dark theme, accents), fonts (Inter), spacing, scrollbar style for all views and components.
  * Correct implementation and styling of sidebar navigation and view switching.
  * Accurate behavior of file input (browse button and drag & drop area, including hover/active states).
  * Correct display and updates for status messages and the dual-phase progress bar.
  * Functionality and appearance of the transcription output area, including placeholder text.
  * Correct operation and styling of 'Copy Text' and 'Save As' buttons.
  * Correct operation and styling of the message modal for success, error, and info messages.
  * Placeholder status and appearance for 'Previous', 'Account', and 'Settings' (model selection part of Settings should be functional).
  * Overall responsiveness and feel, matching the smooth interactions implied by `examplecode.html`.
  * Icon usage matching `examplecode.html`.
