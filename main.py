import webview
import os
import subprocess
import tempfile
import shutil
import json
import uuid
import time
from datetime import datetime

# --- Configuration for Bundled whisper.cpp ---
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
BUNDLED_WHISPER_CPP_DIR = os.path.join(APP_ROOT, 'vendor', 'whisper_cpp')
WHISPER_EXECUTABLE_NAME = 'whisper-cli' # Name of the compiled whisper.cpp CLI executable
WHISPER_MODEL_NAME = "ggml-base.en.bin" # Or any other model you've bundled
BUNDLED_FFMPEG_DIR = os.path.join(APP_ROOT, 'vendor', 'ffmpeg')
FFMPEG_EXECUTABLE_NAME = 'ffmpeg' # Name of the ffmpeg executable

# --- Transcription Storage ---
TRANSCRIPTIONS_FILE = os.path.join(APP_ROOT, 'transcriptions.json')

def load_transcriptions():
    """Load transcriptions from JSON file."""
    if os.path.exists(TRANSCRIPTIONS_FILE):
        try:
            with open(TRANSCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading transcriptions: {e}")
            return []
    return []

def save_transcriptions(transcriptions):
    """Save transcriptions to JSON file."""
    try:
        with open(TRANSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(transcriptions, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving transcriptions: {e}")

def generate_transcription_id():
    """Generate a unique ID for a transcription."""
    return str(uuid.uuid4())

class Api:
    
    def __init__(self):
        self.window = None # Will be set by pywebview later
    def open_file_dialog(self):
        """
        Opens a native file dialog and returns the selected file path(s).
        JavaScript can call this as window.pywebview.api.open_file_dialog()
        """
        if not self.window:
            print("Error: Window object not available in API when trying to open dialog.")
            # Optionally, you could raise an error or return a specific error message to JS
            return None

        # Define file types for the dialog. Adjust as needed.
        file_types = (
            'Audio Files (*.wav;*.mp3;*.m4a;*.aac;*.ogg;*.flac;*.aif;*.aiff;*.wma;*.opus;*.wv;*.ape;*.mpc;*.amr;*.au;*.gsm;*.mka)',
            'All files (*.*)'
        )
        
        # create_file_dialog returns a tuple of selected file paths or None
        result = self.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        
        if result and len(result) > 0:
            selected_file = result[0] # We asked for single selection
            print(f"Python: File selected via dialog: {selected_file}")
            return selected_file # Return the path to JavaScript
        else:
            print("Python: No file selected or dialog cancelled.")
            return None

    def _call_javascript(self, function_name, *args):
        if not self.window:
            print(f"Python Error: Window not available to call JS function {function_name}")
            return
        try:
            # Construct the JS call string properly escaping arguments
            js_args_list = []
            for arg in args:
                if isinstance(arg, str):
                    # Escape backslashes, then single quotes, then double quotes, then newlines for JS string literal
                    escaped_arg = arg.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')
                    js_args_list.append(f"'{escaped_arg}'")
                else:
                    js_args_list.append(str(arg)) # Numbers, booleans (True/False -> true/false in JS)
            js_args_str = ', '.join(js_args_list)
            js_code = f"{function_name}({js_args_str});"
            # print(f"Python: Calling JS: {js_code}") # For debugging JS calls
            self.window.evaluate_js(js_code)
        except Exception as e:
            print(f"Python Error calling JS {function_name}: {e}")

    def start_transcription(self, original_file_path):
        if not original_file_path:
            self._call_javascript('transcriptionError', 'No file path provided.')
            return None

        # Paths to executables and models
        ffmpeg_executable_path = os.path.join(BUNDLED_FFMPEG_DIR, FFMPEG_EXECUTABLE_NAME)
        # Fallback for ffmpeg path
        if not (os.path.exists(ffmpeg_executable_path) and os.access(ffmpeg_executable_path, os.X_OK)):
            alt_ffmpeg_path = os.path.join(APP_ROOT, 'vendor', 'ffmpeg', FFMPEG_EXECUTABLE_NAME)
            if os.path.exists(alt_ffmpeg_path) and os.access(alt_ffmpeg_path, os.X_OK):
                ffmpeg_executable_path = alt_ffmpeg_path
                print(f"Python: Using ffmpeg from {ffmpeg_executable_path}")
            else:
                error_msg = f"FFmpeg executable not found or not executable at {ffmpeg_executable_path} or {alt_ffmpeg_path}. Ensure it's in 'vendor/ffmpeg' and executable."
                print(f"Python Error: {error_msg}")
                self._call_javascript('transcriptionError', error_msg)
                return None

        whisper_executable = os.path.join(BUNDLED_WHISPER_CPP_DIR, WHISPER_EXECUTABLE_NAME)
        whisper_model = os.path.join(BUNDLED_WHISPER_CPP_DIR, 'models', WHISPER_MODEL_NAME)

        # Check existence of whisper components
        if not os.path.exists(whisper_executable):
            error_msg = f"Whisper.cpp executable not found at {whisper_executable}. Ensure it's in 'vendor/whisper_cpp'."
            print(f"Python Error: {error_msg}")
            self._call_javascript('transcriptionError', error_msg)
            return None
        if not os.path.exists(whisper_model):
            error_msg = f"Whisper model not found at {whisper_model}. Ensure it's in 'vendor/whisper_cpp/models'."
            print(f"Python Error: {error_msg}")
            self._call_javascript('transcriptionError', error_msg)
            return None

        # Main transcription process
        try:
            self._call_javascript('updateTranscriptionProgress', 'Processing file...', 0, 'Step 1/3: Preparing Audio')
            print(f"Python: Starting transcription for: {original_file_path}")

            if not os.path.isfile(original_file_path):
                error_msg = f"Invalid file path received: {original_file_path}"
                print(f"Python Error: {error_msg}")
                self._call_javascript('transcriptionError', error_msg)
                return None

            with tempfile.TemporaryDirectory() as temp_dir:
                base_name = os.path.splitext(os.path.basename(original_file_path))[0]
                converted_wav_path = os.path.join(temp_dir, f"{base_name}.wav")

                self._call_javascript('updateTranscriptionProgress', 'Converting to WAV...', 25, 'Step 1/3: Converting Audio (FFmpeg)')

                ffmpeg_command = [
                    ffmpeg_executable_path,
                    '-i', original_file_path,
                    '-ar', '16000',
                    '-ac', '1',
                    '-c:a', 'pcm_s16le',
                    converted_wav_path,
                    '-y'
                ]
                print(f"Python: Running FFmpeg: {' '.join(ffmpeg_command)}")
                try:
                    ffmpeg_process = subprocess.run(ffmpeg_command, capture_output=True, text=True, check=True, timeout=300)
                except subprocess.CalledProcessError as e:
                    error_msg = f"FFmpeg conversion failed. Return code: {e.returncode}\nFFmpeg stderr: {e.stderr.strip()}"
                    print(f"Python Error: {error_msg}")
                    self._call_javascript('transcriptionError', error_msg)
                    return None
                except subprocess.TimeoutExpired:
                    error_msg = "FFmpeg conversion timed out after 5 minutes."
                    print(f"Python Error: {error_msg}")
                    self._call_javascript('transcriptionError', error_msg)
                    return None
                
                self._call_javascript('updateTranscriptionProgress', 'Conversion complete. Starting transcription...', 50, 'Step 2/3: Starting Transcription (Whisper.cpp)')

                whisper_command = [
                    whisper_executable,
                    '-m', whisper_model,
                    '-f', converted_wav_path,
                    '-otxt',
                    '-nt',
                ]
                print(f"Python: Running whisper.cpp: {' '.join(whisper_command)}")
                process = subprocess.Popen(whisper_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                transcription_output, whisper_stderr = process.communicate(timeout=600)

                if process.returncode != 0:
                    detailed_error_info = f"Return code: {process.returncode}"
                    stdout_content = transcription_output.strip() if transcription_output else "(empty stdout)"
                    stderr_content = whisper_stderr.strip() if whisper_stderr else "(empty stderr)"
                    detailed_error_info += f"\nStdout: {stdout_content}"
                    detailed_error_info += f"\nStderr: {stderr_content}"
                    error_msg_console = f"whisper.cpp failed. Details:\n{detailed_error_info}"
                    print(f"Python Error: {error_msg_console}")
                    js_error_msg = f"Transcription failed (Whisper.cpp error code {process.returncode})."
                    if whisper_stderr and whisper_stderr.strip():
                        js_error_msg = f"Whisper.cpp error: {whisper_stderr.strip()}"
                    elif transcription_output and transcription_output.strip():
                        js_error_msg = f"Whisper.cpp message: {transcription_output.strip()}"
                    self._call_javascript('transcriptionError', js_error_msg)
                    return None

                self._call_javascript('updateTranscriptionProgress', 'Transcription complete!', 100, 'Step 3/3: Complete')
                print(f"Python: Transcription successful.")

                # Auto-save the completed transcription
                try:
                    saved_id = self.save_transcription(original_file_path, transcription_output.strip())
                    if saved_id:
                        print(f"Python: Auto-saved transcription with ID: {saved_id}")
                        # Optionally notify frontend about the save
                        # self._call_javascript('transcriptionSaved', saved_id)
                except Exception as e:
                    print(f"Python Error auto-saving transcription: {e}")
                    # Don't fail the transcription if saving fails

                return transcription_output.strip()

        except subprocess.TimeoutExpired:
            error_msg = "Transcription process timed out."
            print(f"Python Error: {error_msg}")
            self._call_javascript('transcriptionError', error_msg)
            return None
        except Exception as e:
            error_msg = f"An unexpected error occurred during transcription: {str(e)}"
            print(f"Python Error: {error_msg}")
            self._call_javascript('transcriptionError', error_msg)
            return None

    def save_transcription(self, file_path, transcription_text, metadata=None):
        """Save a completed transcription to the JSON storage."""
        try:
            transcriptions = load_transcriptions()

            # Get file info
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

            # Create transcription entry
            transcription_entry = {
                'id': generate_transcription_id(),
                'file_name': file_name,
                'file_path': file_path,
                'file_size': file_size,
                'transcription': transcription_text,
                'timestamp': datetime.now().isoformat(),
                'metadata': metadata or {}
            }

            transcriptions.append(transcription_entry)
            save_transcriptions(transcriptions)

            print(f"Python: Saved transcription for {file_name} with ID {transcription_entry['id']}")
            return transcription_entry['id']
        except Exception as e:
            print(f"Python Error saving transcription: {e}")
            return None

    def get_transcriptions(self):
        """Get all saved transcriptions."""
        try:
            transcriptions = load_transcriptions()
            # Sort by timestamp, newest first
            transcriptions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return transcriptions
        except Exception as e:
            print(f"Python Error loading transcriptions: {e}")
            return []

    def delete_transcription(self, transcription_id):
        """Delete a transcription by ID."""
        try:
            transcriptions = load_transcriptions()

            # Find and remove the transcription
            for i, transcription in enumerate(transcriptions):
                if transcription.get('id') == transcription_id:
                    deleted_transcription = transcriptions.pop(i)
                    save_transcriptions(transcriptions)
                    print(f"Python: Deleted transcription {transcription_id} for file {deleted_transcription.get('file_name')}")
                    return True

            print(f"Python: Transcription with ID {transcription_id} not found")
            return False
        except Exception as e:
            print(f"Python Error deleting transcription: {e}")
            return False

    def get_transcription_by_id(self, transcription_id):
        """Get a specific transcription by ID."""
        try:
            transcriptions = load_transcriptions()
            for transcription in transcriptions:
                if transcription.get('id') == transcription_id:
                    return transcription
            return None
        except Exception as e:
            print(f"Python Error getting transcription by ID: {e}")
            return None

    def log_js_message(self, message):
        """Receives a message from JavaScript and prints it to the Python console."""
        print(f"JS LOG: {message}")

# Get the absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(script_dir, 'web_view.html')

if __name__ == '__main__':
    api_instance = Api() # Create an instance of our API
    
    # Create a webview window and pass the API instance
    # pywebview will automatically make api_instance.window available if js_api is set
    window = webview.create_window(
        'Transcription App',
        f'file://{html_file_path}',
        width=1200,
        height=800,
        resizable=True,
        js_api=api_instance # Make the Api class methods available to JavaScript
    )
    api_instance.window = window # Explicitly assign window for clarity and immediate use if needed before start
    webview.start(debug=True)
