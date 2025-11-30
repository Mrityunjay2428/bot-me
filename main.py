import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from PIL import Image, ImageTk
import os
import api

genai.configure(api_key=api.API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat()

class BotMeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BOT-ME - AI Chatbot")
        self.root.geometry("1920x1080")
        self.root.state('zoomed')  # Maximize window on Windows
        
        # Load and set background image
        bg_image_path = os.path.join(os.path.dirname(__file__), "chatbotimage.png")
        if os.path.exists(bg_image_path):
            bg_image = Image.open(bg_image_path)
            # Resize to fit screen
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            bg_label = tk.Label(root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.root.configure(bg="#8B7BA8")  # Fallback purple color
        
        # Header with semi-transparency
        header_frame = tk.Frame(root, bg="#1e1e1e", height=60)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="BOT-ME", font=("Arial", 24, "bold"), 
                               bg="#1e1e1e", fg="#00ff88")
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        subtitle_label = tk.Label(header_frame, text="Powered by Google Gemini 2.5 Flash", 
                                  font=("Arial", 10), bg="#1e1e1e", fg="#888888")
        subtitle_label.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Chat display area with transparent background
        chat_frame = tk.Frame(root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        chat_frame.configure(bg='#8B7BA8')
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, 
                                                       font=("Consolas", 12, "bold"),
                                                       bg="#8B7BA8", fg="#ffffff",
                                                       insertbackground="#ffffff",
                                                       state=tk.DISABLED,
                                                       relief=tk.FLAT,
                                                       borderwidth=0,
                                                       highlightthickness=0)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure tags for colored text with background highlights
        self.chat_display.tag_config("user", foreground="#00d4ff", font=("Consolas", 12, "bold"), 
                                     background="#2d2d4d", spacing1=5, spacing3=5)
        self.chat_display.tag_config("bot", foreground="#00ff88", font=("Consolas", 12, "bold"), 
                                     background="#2d4d2d", spacing1=5, spacing3=5)
        self.chat_display.tag_config("error", foreground="#ff4444", font=("Consolas", 12, "bold"), 
                                     background="#4d2d2d", spacing1=5, spacing3=5)
        self.chat_display.tag_config("text", foreground="#ffffff")
        
        # Input area with semi-transparent background
        input_frame = tk.Frame(root, bg="#1e1e1e")
        input_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        self.input_field = tk.Text(input_frame, height=3, font=("Arial", 11),
                                   bg="#2d2d2d", fg="#ffffff",
                                   insertbackground="#ffffff", wrap=tk.WORD,
                                   relief=tk.FLAT, borderwidth=5)
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self.send_message_enter)
        self.input_field.bind("<Shift-Return>", lambda e: None)
        
        button_frame = tk.Frame(input_frame, bg="#1e1e1e")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.send_button = tk.Button(button_frame, text="Send", command=self.send_message,
                                     font=("Arial", 11, "bold"), bg="#00ff88", fg="#000000",
                                     activebackground="#00d4aa", width=8, cursor="hand2")
        self.send_button.pack(pady=(0, 5))
        
        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_chat,
                                      font=("Arial", 11), bg="#ff4444", fg="#ffffff",
                                      activebackground="#cc0000", width=8, cursor="hand2")
        self.clear_button.pack()
        
        # Welcome message
        self.add_message("BOT-ME", "Hello! I'm BOT-ME, your AI assistant. How can I help you today?", "bot")
        
    def add_message(self, sender, message, tag):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n", "text")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message_enter(self, event):
        if not event.state & 0x1:  # Check if Shift is not pressed
            self.send_message()
            return "break"
    
    def send_message(self):
        user_input = self.input_field.get("1.0", tk.END).strip()
        
        if not user_input:
            messagebox.showwarning("Empty Message", "Please enter a message!")
            return
        
        # Display user message
        self.add_message("You", user_input, "user")
        self.input_field.delete("1.0", tk.END)
        
        # Disable send button while processing
        self.send_button.config(state=tk.DISABLED, text="Sending...")
        
        # Send message in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.get_bot_response, args=(user_input,))
        thread.daemon = True
        thread.start()
    
    def get_bot_response(self, user_input):
        try:
            response = chat.send_message(user_input)
            self.root.after(0, self.add_message, "BOT-ME", response.text, "bot")
        except Exception as e:
            self.root.after(0, self.add_message, "Error", str(e), "error")
        finally:
            self.root.after(0, self.enable_send_button)
    
    def enable_send_button(self):
        self.send_button.config(state=tk.NORMAL, text="Send")
    
    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_message("BOT-ME", "Chat cleared. How can I help you?", "bot")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotMeGUI(root)
    root.mainloop()