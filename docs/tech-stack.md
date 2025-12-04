# Tech Stack: Local Whisper Transcription App

## Core Framework

* **Application Shell:** Electron (Provides the desktop application wrapper and Node.js backend environment)

## Frontend (Renderer Process)

* **Base:** HTML5, CSS3, JavaScript (ES6+)
* **UI Framework (Choose One - Recommended):**
  * React.js
  * Vue.js
  * Svelte
* **Styling (Choose One/Mix):**
  * TailwindCSS
  * Standard CSS / CSS Modules
  * SASS/SCSS
  * Styled-Components / Emotion (If using React)
* **State Management (Optional, depending on complexity):**
  * Redux / Zustand (for React)
  * Vuex / Pinia (for Vue)
  * Svelte Stores (built-in)

## Backend (Main Process & Workers)

* **Runtime:** Node.js (Bundled with Electron)
* **STT Engine (Choose One - *Crucial Decision*):**
  * `whisper.cpp`
    * **Integration:** Requires Node.js bindings (e.g., using N-API or `node-addon-api`) to call the C++ library directly, or via shell command execution (simpler but less efficient).
* **Audio Handling/Conversion:** `ffmpeg`
  * **Integration:** Bundle the `ffmpeg` binary and call it from Node.js (e.g., using libraries like `fluent-ffmpeg` or direct `child_process` execution).
* **Inter-Process Communication (IPC):** Electron's built-in IPC (ipcMain, ipcRenderer) for communication between the UI and the backend/STT processes.
* **Background Processing:** Electron Worker Threads / Node.js `worker_threads` (Essential for running STT without freezing the UI).

## Build & Packaging

* **Bundler/Packager:** `electron-builder` or `electron-forge` (Manages building and packaging for Windows, macOS, Linux).
* **Frontend Bundler:** `Vite` or `Webpack` (Bundles the UI framework code).
* **C++/Python Build (If needed):**
  * `node-gyp` (for C++ Node.js addons).
  * Cross-platform C++ toolchains (GCC/Clang/MSVC).
  * Python packaging tools if bundling Python (`PyInstaller`, `Nuitka` - though complex in an Electron context).

## Development & Infrastructure

* **Version Control:** Git (+ GitHub / GitLab / Bitbucket)
* **Package Manager:** `npm` or `yarn`
* **Testing:** Jest / Vitest (Unit/Integration), Playwright / Cypress (E2E Testing for Electron)
* **CI/CD (Optional but Recommended):** GitHub Actions / GitLab CI / Jenkins (For automated builds and releases).

## Key Considerations

* **Packaging Complexity:** Reliably bundling non-JavaScript components (`whisper.cpp`, `ffmpeg`, Python) for cross-platform use is the primary technical hurdle.
* **Performance Management:** Ensuring the STT process doesn't consume all system resources or block the UI.
* **Model Distribution:** How will Whisper models be included? Bundled? Downloaded on first run? Selectable by the user?
* **Installer Size:** The final package size can become large.