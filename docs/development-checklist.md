# Development Checklist

## Phase 1: Project Setup & Basic Electron Shell

### Step 1.1: Initialize Project and Install Core Dependencies

- [x] Initialize Node.js project in `/Users/haydengroover/Documents/Transcription App/`
- [x] Install Electron as a dev dependency
- [x] Install React and React DOM
- [x] Install Vite for development server and build
- [x] Set up `.gitignore` for Node.js/Electron project
- [x] Initialize Git repository

### Step 1.2: Create Basic Electron Application Structure

- [x] Create `main.js` with basic Electron setup
  - [x] Handle app lifecycle events
  - [x] Create BrowserWindow (1200x800)
  - [x] Load `index.html`
- [x] Create `preload.js` with secure contextBridge setup
- [x] Create `src/renderer/index.html` with root div for React
- [x] Update `package.json` with main entry and start script
- [x] Update `vite.config.js` for Electron integration
- [x] Set up TypeScript configuration
- [x] Add Tailwind CSS and PostCSS configuration
- [x] Create basic React component structure

### Step 1.3: Implement Basic Inter-Process Communication (IPC)

- [x] Set up `ipcMain.handle` in `main.js`
- [x] Expose test function in `preload.js`
- [x] Create test React component to test IPC

## Save for later

- [ ] Implement error handling for IPC
- [ ] Implement timeout handling for IPC
- [ ] Implement retry logic for failed IPC calls
- [ ] Implement logging for IPC calls
- [ ] Implement IPC event emitter for progress updates
- [ ] Implement IPC event emitter for error updates
- [ ] Implement IPC event emitter for success updates

## Phase 2: Frontend UI Development (React)

### Step 2.1: Setup React with Vite, TailwindCSS, and Font Awesome

- [x] Set up Vite for React in `src/renderer`
- [x] Install and configure TailwindCSS with PostCSS
- [x] Set up Font Awesome for React with required icon packs
- [x] Configure Vite build settings for Electron
- [x] Set up environment variables for development/production
- [x] Create basic `App.jsx` component with layout structure
- [x] Update Electron to load Vite dev server in development
- [x] Configure Electron to load built files in production

### Step 2.2: Convert `examplecode.html` to React Components

- [ ] Create `App.jsx` layout component
- [ ] Create `Sidebar.jsx` with navigation links
- [ ] Create `Header.jsx` with window controls
- [ ] Create view components:
  - [ ] `ActiveTranscriptionView.jsx`
  - [ ] `PreviousView.jsx`
  - [ ] `AccountView.jsx`
  - [ ] `SettingsView.jsx`
- [ ] Create `Modal.jsx` for messages
- [ ] Apply TailwindCSS classes from `examplecode.html`

### Step 2.3: Implement File Selection

- [ ] Add file browse button with IPC to open system dialog
- [ ] Implement drag-and-drop area with visual feedback
- [ ] Add file type validation (mp3, wav, m4a, etc.)
- [ ] Update UI with selected file name and metadata
- [ ] Show file size and duration if available
- [ ] Implement file removal functionality
- [ ] Enable/disable Start Transcription button based on valid selection
- [ ] Add error handling for invalid files

### Step 2.4: Implement Tab Navigation

- [ ] Set up state management for active view
- [ ] Implement view switching in `App.jsx`
- [ ] Style active navigation link
- [ ] Update header title based on current view

### Step 2.5: Implement Transcription UI Elements

- [ ] Add state variables for status, progress, and output
- [ ] Implement progress bar
- [ ] Add Copy Text button functionality
- [ ] Add Save As button (placeholder)
- [ ] Style output textarea as read-only
- [ ] Implement message modal for notifications

## Phase 3: Backend Core - Audio Processing

### Step 3.1: Setup Worker Thread for Background Tasks

- [ ] Create worker thread setup in `main.js`
- [ ] Set up IPC between main and worker
- [ ] Create `audioWorker.js`
- [ ] Implement basic worker communication test

### Step 3.2: `ffmpeg` Integration

- [ ] Create `src/main/audioConverter.js`
- [ ] Implement audio conversion function with proper error handling
- [ ] Support conversion to 16-bit, 16kHz mono WAV format
- [ ] Add progress event emitters for conversion progress
- [ ] Implement cleanup of temporary files
- [ ] Add support for multiple audio formats (mp3, wav, m4a, etc.)
- [ ] Implement audio duration detection
- [ ] Add validation for input/output file paths

### Step 3.3: Integrate `ffmpeg` with Worker Thread

- [ ] Update `audioWorker.js` to handle conversion tasks
- [ ] Implement progress reporting
- [ ] Add error handling and forwarding
- [ ] Test end-to-end file conversion

## Phase 4: Backend Core - Transcription Engine

### Step 4.1: `whisper.cpp` Integration

- [ ] Create `src/main/transcriber.js`
- [ ] Implement transcription function with proper error handling
- [ ] Set up child process for `whisper.cpp` with proper arguments
- [ ] Add support for different whisper.cpp models
- [ ] Implement progress tracking for transcription
- [ ] Add timeout handling for long-running transcriptions
- [ ] Implement cleanup of temporary files
- [ ] Add validation for model files and input audio

### Step 4.2: Integrate `whisper.cpp` with Worker Thread

- [ ] Update `audioWorker.js` for transcription
- [ ] Implement progress reporting
- [ ] Add error handling and forwarding
- [ ] Test end-to-end transcription

### Step 4.3: Implement Output Parsing

- [ ] Add output parsing logic
- [ ] Format transcription results
- [ ] Handle timestamps if needed

## Phase 5: Connect Frontend to Backend

### Step 5.1: Implement Main Process IPC Handlers

- [ ] Add file dialog IPC
- [ ] Add file operations IPC
- [ ] Add worker management IPC

### Step 5.2: Implement Renderer Process IPC

- [ ] Set up IPC calls in React components
- [ ] Connect UI actions to backend
- [ ] Implement progress updates

### Step 5.3: Implement Error Handling

- [ ] Add React error boundaries around main components
- [ ] Implement user-friendly error messages in the UI
- [ ] Add error logging to file
- [ ] Implement error recovery where possible
- [ ] Add error reporting for failed operations
- [ ] Create error codes/messages for common issues
- [ ] Add retry mechanisms for transient failures

## Phase 6: Model Management

### Step 6.1: Model Downloader

- [ ] Implement model download functionality with progress tracking
- [ ] Add checksum verification for downloaded models
- [ ] Support resumable downloads
- [ ] Add model validation after download
- [ ] Implement download queue for multiple models
- [ ] Add error handling for download failures
- [ ] Store models in application data directory
- [ ] Add support for custom model repositories

### Step 6.2: Model Selection

- [ ] Add model selection UI
- [ ] Implement model switching
- [ ] Add model info display

## Phase 7: Build, Packaging, and Testing

### Step 7.1: Package Dependencies

- [ ] Bundle `ffmpeg`
- [ ] Bundle `whisper.cpp`
- [ ] Include base models

### Step 7.2: Create Installers

- [ ] Set up Electron Builder
- [ ] Create macOS app
- [ ] Create Windows installer
- [ ] Create Linux packages

### Step 7.3: Testing and Quality Assurance

- [ ] Set up Jest/Vitest testing framework
- [ ] Write unit tests for utility functions
- [ ] Write component tests for React components
- [ ] Write integration tests for main processes
- [ ] Test on different platforms (macOS, Windows, Linux)
- [ ] Perform accessibility testing
- [ ] Test with different audio formats and sizes
- [ ] Perform performance testing
- [ ] Create test automation scripts
- [ ] Document test cases and results
