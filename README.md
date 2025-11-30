# BOT-ME - AI Chatbot with GUI

A modern, interactive AI chatbot application built with Python, featuring a beautiful GUI interface powered by Tkinter and Google's Gemini 2.5 Flash AI model.

![BOT-ME](chatbotimage.png)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## 🌟 Overview

BOT-ME is an AI-powered chatbot application that provides an intuitive graphical user interface for conversing with Google's Gemini 2.5 Flash language model. The application features a custom-designed interface with background imagery, syntax-highlighted text, and real-time AI responses.

## ✨ Features

- **Modern GUI Interface**: Clean, dark-themed interface with custom background image
- **Real-time AI Responses**: Powered by Google Gemini 2.5 Flash for intelligent conversations
- **Threaded Processing**: Non-blocking UI that remains responsive during API calls
- **Syntax Highlighting**: Color-coded messages for better readability
  - User messages: Cyan blue with dark blue background
  - Bot responses: Green with dark green background
  - Errors: Red with dark red background
- **Multi-line Input**: Support for Enter (send) and Shift+Enter (new line)
- **Chat History**: Scrollable chat display to review conversation history
- **Clear Function**: Quick button to clear chat and start fresh
- **Full Screen**: Maximized window for optimal viewing experience

## 🛠️ Tech Stack

### Core Technologies

1. **Python 3.13.5**
   - Primary programming language
   - Provides the runtime environment for the application

2. **Tkinter**
   - Python's standard GUI toolkit
   - Used for creating all UI elements (windows, frames, buttons, text areas)
   - Handles event binding and user interactions
   - Provides the `scrolledtext` widget for chat display

3. **Google Generative AI (google-generativeai)**
   - Official Python SDK for Google's Gemini AI models
   - Provides access to Gemini 2.5 Flash language model
   - Handles API authentication and request management
   - Maintains conversation context through chat sessions

4. **PIL (Pillow)**
   - Python Imaging Library
   - Used for loading and processing the background image
   - Handles image resizing to fit different screen resolutions
   - Converts images to Tkinter-compatible format (ImageTk.PhotoImage)

5. **Threading**
   - Python's built-in threading module
   - Prevents UI freezing during API calls
   - Runs AI response generation in background threads
   - Ensures smooth user experience

### Development Environment

- **Virtual Environment (venv)**: Isolated Python environment for dependency management
- **VS Code**: Primary development IDE
- **PowerShell**: Terminal for running commands and scripts

## 📦 Prerequisites

Before running this application, ensure you have:

1. **Python 3.13.5 or higher** installed on your system
2. **Google Gemini API Key**: Obtain from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Internet Connection**: Required for API calls to Google's servers
4. **Background Image**: `chatbotimage.png` in the project directory

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
cd "c:\Users\Mrityunjay Shandilya\OneDrive\Documents\VS CODE Python\Project"
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` prefix in your terminal prompt.

### Step 4: Install Dependencies

```powershell
pip install google-generativeai Pillow
```

### Step 5: Configure API Key

Open `main.py` and replace the API key on line 7:

```python
api_key = "YOUR_API_KEY_HERE"
```

### Step 6: Add Background Image

Ensure `chatbotimage.png` is in the project directory, or replace it with your preferred image.

## 💻 Usage

### Running the Application

With the virtual environment activated:

```powershell
python main.py
```

Or directly from VS Code: Press `F5` or click the Run button.

### Using the Chatbot

1. **Starting a Conversation**
   - Type your message in the input field at the bottom
   - Press `Enter` to send (or click the "Send" button)
   - Use `Shift+Enter` for multi-line messages

2. **Viewing Responses**
   - Bot responses appear in green text
   - Your messages appear in cyan blue
   - Errors (if any) appear in red

3. **Clearing Chat**
   - Click the "Clear" button to reset the conversation
   - Note: This only clears the display, not the AI's conversation memory

4. **Closing the Application**
   - Click the window's close button (X)
   - Or press `Alt+F4`

## 📁 Project Structure

```
Project/
│
├── venv/                      # Virtual environment directory
│   ├── Scripts/              # Python executables and activation scripts
│   └── Lib/                  # Installed packages
│
├── main.py                   # Main application file
├── chatbotimage.png          # Background image for GUI
└── README.md                 # This file
```

## 🔍 How It Works

### 1. Application Initialization

```python
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat()
```

- Configures the Google AI SDK with your API key
- Initializes the Gemini 2.5 Flash model
- Starts a persistent chat session for conversation context

### 2. GUI Setup (`BotMeGUI.__init__`)

**Window Configuration**
```python
self.root.geometry("1920x1080")
self.root.state('zoomed')
```
- Sets initial window size
- Maximizes window to full screen

**Background Image Loading**
```python
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
self.bg_photo = ImageTk.PhotoImage(bg_image)
```
- Opens the background image using PIL
- Resizes to match screen dimensions
- Converts to Tkinter-compatible format
- Stores reference to prevent garbage collection

**UI Components**
- **Header Frame**: Displays "BOT-ME" title and subtitle
- **Chat Display**: `ScrolledText` widget with custom color tags
- **Input Field**: Multi-line text entry with key bindings
- **Buttons**: Send and Clear buttons for user actions

### 3. Message Sending Process

**User Input Handling**
```python
def send_message(self):
    user_input = self.input_field.get("1.0", tk.END).strip()
    self.add_message("You", user_input, "user")
    self.send_button.config(state=tk.DISABLED, text="Sending...")
```
- Retrieves text from input field
- Displays user message in chat
- Disables send button to prevent duplicate sends

**Threaded API Call**
```python
thread = threading.Thread(target=self.get_bot_response, args=(user_input,))
thread.daemon = True
thread.start()
```
- Creates a new thread for API call
- Daemon thread ensures proper cleanup on exit
- Prevents UI freezing during network operations

**Response Processing**
```python
def get_bot_response(self, user_input):
    try:
        response = chat.send_message(user_input)
        self.root.after(0, self.add_message, "BOT-ME", response.text, "bot")
    except Exception as e:
        self.root.after(0, self.add_message, "Error", str(e), "error")
```
- Sends message to Gemini API
- Uses `root.after()` to safely update GUI from thread
- Handles errors gracefully with error messages

### 4. Message Display

**Text Formatting**
```python
self.chat_display.tag_config("user", foreground="#00d4ff", 
                             background="#2d2d4d", 
                             font=("Consolas", 12, "bold"))
```
- Applies color tags for different message types
- Adds background highlights for better visibility
- Uses monospace font for consistency

**Dynamic Updates**
```python
def add_message(self, sender, message, tag):
    self.chat_display.config(state=tk.NORMAL)
    self.chat_display.insert(tk.END, f"{sender}: ", tag)
    self.chat_display.insert(tk.END, f"{message}\n\n", "text")
    self.chat_display.see(tk.END)
    self.chat_display.config(state=tk.DISABLED)
```
- Temporarily enables text widget for editing
- Inserts formatted message
- Scrolls to show latest message
- Disables editing to prevent user modifications

## ⚙️ Configuration

### Customizing the Appearance

**Change Window Size**
```python
self.root.geometry("1920x1080")  # Width x Height
```

**Modify Colors**
```python
# User message color
self.chat_display.tag_config("user", foreground="#00d4ff")

# Bot message color
self.chat_display.tag_config("bot", foreground="#00ff88")

# Background color
self.chat_display = scrolledtext.ScrolledText(..., bg="#8B7BA8")
```

**Change Font**
```python
self.chat_display = scrolledtext.ScrolledText(..., 
                    font=("Consolas", 12, "bold"))
```

### Using a Different AI Model

Replace the model name in line 11:
```python
model = genai.GenerativeModel("gemini-pro")  # or other available models
```

### Changing the Background Image

Replace `chatbotimage.png` with your image file, or update the path in line 22:
```python
bg_image_path = os.path.join(os.path.dirname(__file__), "your_image.png")
```

## 🐛 Troubleshooting

### Issue: API Key Error
**Error**: `Invalid API key provided`
**Solution**: Verify your API key in `main.py` and ensure it's valid from Google AI Studio

### Issue: Module Not Found
**Error**: `ModuleNotFoundError: No module named 'google.generativeai'`
**Solution**: 
```powershell
pip install google-generativeai Pillow
```

### Issue: Virtual Environment Not Activating
**Error**: `running scripts is disabled on this system`
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Background Image Not Showing
**Error**: Purple background instead of image
**Solution**: Ensure `chatbotimage.png` exists in the project directory

### Issue: Window Too Small
**Solution**: The window should auto-maximize. If not, manually maximize or check:
```python
self.root.state('zoomed')  # This line should be present
```

### Issue: Slow Response Times
**Possible Causes**:
- Slow internet connection
- Google API server load
- Large conversation history

**Solutions**:
- Check your internet speed
- Clear chat and start a new conversation
- Try during off-peak hours

## 🔐 Security Notes

- **Never commit your API key** to version control
- Consider using environment variables for sensitive data:
```python
import os
api_key = os.getenv("GEMINI_API_KEY")
```
- Keep your virtual environment's `venv/` folder in `.gitignore`

## 📝 License

This project is created for educational purposes. Please ensure you comply with Google's Gemini API terms of service when using this application.

## 🤝 Contributing

Feel free to fork this project and make improvements! Some ideas:
- Add conversation history export
- Implement dark/light theme toggle
- Add voice input/output capabilities
- Create conversation templates
- Add multi-language support

## 📧 Contact

For questions or support, please contact the project maintainer.

---

**Created by**: Mrityunjay Shandilya  
**Last Updated**: November 30, 2025  
**Version**: 1.0.0
#   b o t - m e  
 