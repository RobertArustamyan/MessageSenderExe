import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from typing import List
import threading
import queue
from datetime import datetime

# Import your existing modules
from CookieExtraction.cookie_extractor import CookieExtractor
from Messages.message_sender import Sender,CustomSender
from Messages.messages import Messages
from Messages.messages import MessageDatabase


class AutoAmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto.am Message Sender")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # Initialize database
        self.db = MessageDatabase()

        # Queue for thread communication
        self.queue = queue.Queue()

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Create main interface
        self.create_widgets()

        # Start queue processing
        self.process_queue()

    def create_widgets(self):
        """Create all UI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Auto.am Message Sender",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Configuration section
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)

        # Login and Password fields
        ttk.Label(config_frame, text="Login:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.login_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.login_var).grid(row=0, column=3, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(config_frame, text="Password:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.password_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.password_var, show='*').grid(row=1, column=3, sticky=(tk.W, tk.E),
                                                                               pady=2)

        # New cookies flag
        ttk.Label(config_frame, text="Extract New Cookies:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.new_cookies_var = tk.BooleanVar()
        ttk.Checkbutton(config_frame, variable=self.new_cookies_var).grid(row=0, column=1, sticky=tk.W, pady=2)

        # Headless options
        ttk.Label(config_frame, text="Cookie Extractor Headless:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.cookie_headless_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, variable=self.cookie_headless_var).grid(row=1, column=1, sticky=tk.W, pady=2)

        ttk.Label(config_frame, text="Message Sender Headless:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.sender_headless_var = tk.BooleanVar()
        ttk.Checkbutton(config_frame, variable=self.sender_headless_var).grid(row=2, column=1, sticky=tk.W, pady=2)

        ttk.Label(config_frame, text="Send to All:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.send_to_all_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, variable=self.send_to_all_var).grid(row=3, column=1, sticky=tk.W, pady=2)

        ttk.Label(config_frame, text="Test Mode:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.test_mode_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, variable=self.test_mode_var).grid(row=4, column=1, sticky=tk.W, pady=2)

        # Search parameters section
        search_frame = ttk.LabelFrame(main_frame, text="Search Parameters", padding="10")
        search_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(3, weight=1)

        # Category dropdown
        ttk.Label(search_frame, text="Category:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.category_var = tk.StringVar(value="passenger")
        categories = ["all", "passenger", "trucks", "motorcycles", "special", "buses", "trailers", "water"]
        category_combo = ttk.Combobox(search_frame, textvariable=self.category_var, values=categories, state="readonly")
        category_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(0, 10))

        # Page range
        ttk.Label(search_frame, text="Start Page:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.start_page_var = tk.StringVar(value="1")
        ttk.Entry(search_frame, textvariable=self.start_page_var, width=10).grid(row=0, column=3, sticky=tk.W, pady=2)

        ttk.Label(search_frame, text="End Page:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.end_page_var = tk.StringVar(value="1")
        ttk.Entry(search_frame, textvariable=self.end_page_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=2)

        # Price range
        ttk.Label(search_frame, text="Start Price ($):").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.start_price_var = tk.StringVar(value="10000")
        ttk.Entry(search_frame, textvariable=self.start_price_var, width=10).grid(row=1, column=3, sticky=tk.W, pady=2)

        ttk.Label(search_frame, text="End Price ($):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.end_price_var = tk.StringVar(value="150000")
        ttk.Entry(search_frame, textvariable=self.end_price_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=2)

        # Messages section
        messages_frame = ttk.LabelFrame(main_frame, text="Message Management", padding="10")
        messages_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        messages_frame.columnconfigure(0, weight=1)
        messages_frame.rowconfigure(1, weight=1)

        # Add message section
        add_frame = ttk.Frame(messages_frame)
        add_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        add_frame.columnconfigure(0, weight=1)

        ttk.Label(add_frame, text="Add New Message:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.new_message_var = tk.StringVar()
        message_entry = ttk.Entry(add_frame, textvariable=self.new_message_var)
        message_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)

        button_frame = ttk.Frame(add_frame)
        button_frame.grid(row=1, column=1, padx=(10, 0))

        ttk.Button(button_frame, text="Add", command=self.add_message).grid(row=0, column=0, padx=2)
        ttk.Button(button_frame, text="Remove", command=self.remove_message).grid(row=0, column=1, padx=2)

        # Messages list
        ttk.Label(messages_frame, text="Current Messages:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))

        # Listbox with scrollbar
        list_frame = ttk.Frame(messages_frame)
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.messages_listbox = tk.Listbox(list_frame, height=8)
        self.messages_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.messages_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.messages_listbox.configure(yscrollcommand=scrollbar.set)

        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        self.start_button = ttk.Button(control_frame, text="Start Process", command=self.start_process)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_process, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        # Status and log section
        status_frame = ttk.LabelFrame(main_frame, text="Status & Log", padding="10")
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, font=('Arial', 10, 'bold'))
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        # Log text area
        self.log_text = scrolledtext.ScrolledText(status_frame, height=10, width=80)
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for resizing
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(5, weight=1)

        # Load initial messages
        self.refresh_messages_list()

        # Bind Enter key to message entry
        message_entry.bind('<Return>', lambda e: self.add_message())

    def refresh_messages_list(self):
        """Refresh the messages listbox"""
        self.messages_listbox.delete(0, tk.END)
        for message in self.db.get_messages():
            self.messages_listbox.insert(tk.END, message)

    def add_message(self):
        """Add a new message to the database"""
        message = self.new_message_var.get().strip()
        if message:
            if self.db.add_message(message):
                self.new_message_var.set("")
                self.refresh_messages_list()
                self.log_message(f"Added message: {message}")
            else:
                messagebox.showwarning("Warning", "Message already exists or is empty")
        else:
            messagebox.showwarning("Warning", "Please enter a message")

    def remove_message(self):
        """Remove selected message from the database"""
        selection = self.messages_listbox.curselection()
        if selection:
            message = self.messages_listbox.get(selection[0])
            if self.db.remove_message(message):
                self.refresh_messages_list()
                self.log_message(f"Removed message: {message}")
            else:
                messagebox.showerror("Error", "Failed to remove message")
        else:
            messagebox.showwarning("Warning", "Please select a message to remove")

    def log_message(self, message: str):
        """Add a message to the log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

    def validate_inputs(self) -> bool:
        """Validate user inputs"""
        try:
            start_page = int(self.start_page_var.get())
            end_page = int(self.end_page_var.get())
            start_price = int(self.start_price_var.get())
            end_price = int(self.end_price_var.get())

            if start_page < 1 or end_page < 1:
                messagebox.showerror("Error", "Page numbers must be positive")
                return False

            if start_page > end_page:
                messagebox.showerror("Error", "Start page cannot be greater than end page")
                return False

            if start_price < 0 or end_price < 0:
                messagebox.showerror("Error", "Prices cannot be negative")
                return False

            if start_price > end_price:
                messagebox.showerror("Error", "Start price cannot be greater than end price")
                return False

            if not self.db.get_messages():
                messagebox.showerror("Error", "Please add at least one message")
                return False

            return True

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for pages and prices")
            return False

    def start_process(self):
        """Start the message sending process"""
        if not self.validate_inputs():
            return

        # Disable start button and enable stop button
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set("Processing...")

        # Clear log
        self.log_text.delete(1.0, tk.END)

        # Create and start worker thread
        self.worker_thread = threading.Thread(target=self.worker_function)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def worker_function(self):
        """Worker function that runs in a separate thread"""
        try:
            # Get parameters
            new_cookies = self.new_cookies_var.get()
            cookie_headless = self.cookie_headless_var.get()
            sender_headless = self.sender_headless_var.get()
            send_to_all = self.send_to_all_var.get()
            test_mode = self.test_mode_var.get()
            category = self.category_var.get()
            start_page = int(self.start_page_var.get())
            end_page = int(self.end_page_var.get())
            start_price = self.start_price_var.get()
            end_price = self.end_price_var.get()

            login = self.login_var.get()
            password = self.password_var.get()

            # Create Messages object with database messages
            messages = Messages()
            # Clear default messages and add from database
            messages._messages = self.db.get_messages()

            # Queue status update
            self.queue.put(("log", "Starting process..."))

            # Extract cookies if needed
            if new_cookies:
                self.queue.put(("log", "Extracting cookies..."))
                self.queue.put(("status", "Extracting cookies..."))

                extractor = CookieExtractor(headless=cookie_headless, additional_options=True, login=login,
                                            password=password)
                success = extractor.extract_cookies()

                if success:
                    self.queue.put(("log", "Cookies extracted successfully!"))
                else:
                    self.queue.put(("log", "Cookie extraction failed!"))
                    self.queue.put(("error", "Cookie extraction failed"))
                    return

            # Send messages
            self.queue.put(("log", "Starting message sending..."))
            self.queue.put(("status", "Sending messages..."))

            # Create a custom Sender class that can communicate with the GUI
            sender = CustomSender(
                headless=sender_headless,
                additional_options=True,
                progress_callback=self.update_progress
            )

            sender.send_message(
                cookies_path="AppData/cookies.pkl",
                category=category,
                start_page=start_page,
                end_page=end_page,
                start_price=start_price,
                end_price=end_price,
                messages=messages,
                send_to_all=send_to_all,
                test_mode=test_mode,
            )

            self.queue.put(("log", "Process completed successfully!"))
            self.queue.put(("status", "Completed"))
            self.queue.put(("complete", "Process completed successfully"))

        except Exception as e:
            self.queue.put(("log", f"Error: {str(e)}"))
            self.queue.put(("error", f"Process failed: {str(e)}"))

    def update_progress(self, message, status=None):
        """Callback function for progress updates"""
        self.queue.put(("log", message))
        if status:
            self.queue.put(("status", status))

    def stop_process(self):
        """Stop the current process"""
        # Note: This is a simple implementation. For proper thread termination,
        # you would need to implement a more sophisticated stopping mechanism
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Stopped")
        self.log_message("Process stopped by user")

    def process_queue(self):
        """Process messages from the worker thread"""
        try:
            while True:
                message_type, message = self.queue.get_nowait()

                if message_type == "log":
                    self.log_message(message)
                elif message_type == "status":
                    self.status_var.set(message)
                elif message_type == "error":
                    self.status_var.set("Error")
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    messagebox.showerror("Error", message)
                elif message_type == "complete":
                    self.status_var.set("Ready")
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    messagebox.showinfo("Success", message)

        except queue.Empty:
            pass

        # Schedule next queue check
        self.root.after(100, self.process_queue)



def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = AutoAmApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()