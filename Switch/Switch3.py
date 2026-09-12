import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import time
import keyboard
import threading
from tkinter import font as tkFont
import pygame  # For sound effects

class CommandExecutor:
    def __init__(self, master):
        self.master = master
        self.master.title("Command Executor - Neon UI")
        self.master.geometry("1200x800")
        self.master.configure(bg="#121212")  # Dark background for futuristic look

        # Initialize pygame for sound effects
        pygame.mixer.init()
        self.click_sound = None
        try:
            self.click_sound = pygame.mixer.Sound("click_sound.wav")
        except FileNotFoundError:
            print("Warning: 'click_sound.wav' not found. Sound effects will be disabled.")

        # Define neon colors and styles
        self.NEON_BLUE = "#00bcd4"
        self.NEON_GREEN = "#76ff03"
        self.HOVER_COLOR = "#ff4081"
        self.BACKGROUND_COLOR = "#121212"
        self.FONT = ("Orbitron", 12)

        # Custom Fonts
        self.title_font = tkFont.Font(family="Orbitron", size=24, weight="bold")
        self.button_font = tkFont.Font(family="Orbitron", size=10, weight="bold")  # Smaller font size for buttons
        self.label_font = tkFont.Font(family="Orbitron", size=12)

        # Initialize variables
        self.commands = []  # List of tuples: (command, duration, is_non_repeatable)
        self.predefined_commands = ["Space", "Enter", "Ctrl+C", "Ctrl+V", "Tab", "Alt+Tab", "Alt+Tab+Tab", "Alt+Tab+Tab+Tab"]
        self.is_running = False  # Track if commands are being executed
        self.floating_widget_visible = True  # Track floating widget visibility

        # Main Canvas and Scrollbar
        self.canvas = tk.Canvas(self.master, bg=self.BACKGROUND_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.BACKGROUND_COLOR)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Header Frame
        self.header_frame = tk.Frame(self.scrollable_frame, bg="#1A1A1A", bd=2, relief=tk.RIDGE)
        self.header_frame.pack(pady=20, padx=20, fill=tk.X)

        self.title_label = tk.Label(self.header_frame, text="Command Executor", bg="#1A1A1A", fg=self.NEON_BLUE, font=self.title_font)
        self.title_label.pack(pady=10)

        # Top Frame for Adding Commands
        self.add_command_frame = tk.Frame(self.scrollable_frame, bg="#1A1A1A", bd=2, relief=tk.RIDGE)
        self.add_command_frame.pack(pady=20, padx=20, fill=tk.X)

        self.command_label = tk.Label(self.add_command_frame, text="Command:", bg="#1A1A1A", fg=self.NEON_BLUE, font=self.label_font)
        self.command_label.grid(row=0, column=0, padx=10, pady=10)

        self.command_entry = tk.Entry(self.add_command_frame, width=20, bg="#2A2A2A", fg="#FFFFFF", insertbackground="white", font=self.label_font, bd=2, relief=tk.FLAT)
        self.command_entry.grid(row=0, column=1, padx=10, pady=10)

        self.duration_label = tk.Label(self.add_command_frame, text="Duration (s):", bg="#1A1A1A", fg=self.NEON_BLUE, font=self.label_font)
        self.duration_label.grid(row=0, column=2, padx=10, pady=10)

        self.duration_entry = tk.Entry(self.add_command_frame, width=10, bg="#2A2A2A", fg="#FFFFFF", insertbackground="white", font=self.label_font, bd=2, relief=tk.FLAT)
        self.duration_entry.grid(row=0, column=3, padx=10, pady=10)

        self.non_repeatable_var = tk.BooleanVar()
        self.non_repeatable_check = tk.Checkbutton(self.add_command_frame, text="Non-Repeatable", bg="#1A1A1A", fg=self.NEON_BLUE, font=self.label_font, variable=self.non_repeatable_var)
        self.non_repeatable_check.grid(row=0, column=4, padx=10, pady=10)

        self.add_command_button = self.create_animated_button(self.add_command_frame, "Add Custom Command", self.add_custom_command, row=0, column=5)

        self.predefined_label = tk.Label(self.add_command_frame, text="Predefined Commands:", bg="#1A1A1A", fg=self.NEON_BLUE, font=self.label_font)
        self.predefined_label.grid(row=1, column=0, padx=10, pady=10)

        self.predefined_var = tk.StringVar()
        self.predefined_menu = ttk.Combobox(self.add_command_frame, textvariable=self.predefined_var, values=self.predefined_commands, state="readonly", font=self.label_font, background="#2A2A2A", foreground="#FFFFFF")
        self.predefined_menu.grid(row=1, column=1, padx=10, pady=10)

        self.add_predefined_button = self.create_animated_button(self.add_command_frame, "Add Predefined Command", self.add_predefined_command, row=1, column=2)

        self.repetition_label = tk.Label(self.add_command_frame, text="Repetitions (for all commands):", bg="#1A1A1A", fg=self.NEON_BLUE, font=self.label_font)
        self.repetition_label.grid(row=1, column=3, padx=10, pady=10)

        self.repetition_entry = tk.Entry(self.add_command_frame, width=10, bg="#2A2A2A", fg="#FFFFFF", insertbackground="white", font=self.label_font, bd=2, relief=tk.FLAT)
        self.repetition_entry.grid(row=1, column=4, padx=10, pady=10)

        # Command List Display
        self.command_list_frame = tk.Frame(self.scrollable_frame, bg="#1A1A1A", bd=2, relief=tk.RIDGE)
        self.command_list_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.command_listbox = tk.Listbox(self.command_list_frame, width=80, height=15, bg="#2A2A2A", fg="#FFFFFF", font=self.label_font, bd=0, relief=tk.FLAT)
        self.command_listbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.command_list_scrollbar = tk.Scrollbar(self.command_list_frame)
        self.command_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.command_listbox.config(yscrollcommand=self.command_list_scrollbar.set)
        self.command_list_scrollbar.config(command=self.command_listbox.yview)

        # Buttons for Command List
        self.command_buttons_frame = tk.Frame(self.scrollable_frame, bg="#0A0A0A")
        self.command_buttons_frame.pack(pady=10, padx=20, fill=tk.X)

        self.start_button = self.create_animated_button(self.command_buttons_frame, "Start", self.start_execution, row=0, column=0)
        self.stop_button = self.create_animated_button(self.command_buttons_frame, "Stop", self.stop_execution, row=0, column=1)
        self.clear_button = self.create_animated_button(self.command_buttons_frame, "Clear List", self.clear_commands, row=0, column=2)
        self.move_up_button = self.create_animated_button(self.command_buttons_frame, "Move Up", self.move_command_up, row=0, column=3)
        self.move_down_button = self.create_animated_button(self.command_buttons_frame, "Move Down", self.move_command_down, row=0, column=4)
        self.import_button = self.create_animated_button(self.command_buttons_frame, "Import List", self.import_commands, row=0, column=5)
        self.export_button = self.create_animated_button(self.command_buttons_frame, "Export List", self.export_commands, row=0, column=6)

        # Floating Widget
        self.create_floating_widget()

    def create_animated_button(self, frame, text, command, row, column):
        """Create a button with neon hover effects."""
        button = tk.Button(frame, text=text, font=self.button_font, bg=self.NEON_BLUE, fg="white", relief="flat", bd=5,
                           width=15, height=1, command=lambda: [self.play_click_sound(), command()])  # Play sound on click
        button.grid(row=row, column=column, padx=5, pady=5)
        button.bind("<Enter>", lambda e: self.on_enter(button))
        button.bind("<Leave>", lambda e: self.on_leave(button))
        return button

    def play_click_sound(self):
        """Play the click sound if the sound file is available."""
        if self.click_sound:
            self.click_sound.play()

    def on_enter(self, button):
        """Change button color on hover."""
        button.config(bg=self.HOVER_COLOR, relief="raised")

    def on_leave(self, button):
        """Reset button color on leave."""
        button.config(bg=self.NEON_BLUE, relief="flat")

    def create_floating_widget(self):
        self.floating_window = tk.Toplevel(self.master)
        self.floating_window.title("Floating Widget")
        self.floating_window.geometry("150x60+1200+700")  # Position at bottom-right
        self.floating_window.attributes("-topmost", True)
        self.floating_window.overrideredirect(True)  # Remove window decorations
        self.floating_window.attributes("-alpha", 0.9)  # Semi-transparent
        self.floating_window.configure(bg="#1A1A1A")

        # Make the floating widget draggable
        def start_drag(event):
            self.floating_window._offset_x = event.x
            self.floating_window._offset_y = event.y

        def stop_drag(event):
            self.floating_window.geometry(f"+{event.x_root - self.floating_window._offset_x}+{event.y_root - self.floating_window._offset_y}")

        self.floating_window.bind("<ButtonPress-1>", start_drag)
        self.floating_window.bind("<B1-Motion>", stop_drag)

        # Add Start and Stop buttons to the floating widget
        self.floating_start_button = self.create_animated_button(self.floating_window, "Start", self.start_execution, row=0, column=0)
        self.floating_stop_button = self.create_animated_button(self.floating_window, "Stop", self.stop_execution, row=0, column=1)

        # Toggle Floating Widget Button
        self.toggle_floating_button = tk.Button(self.scrollable_frame, text="Toggle Floating Widget", command=self.toggle_floating_widget, bg="#AA00FF", fg="#0A0A0A", font=self.button_font, bd=0, relief=tk.FLAT, padx=10, pady=5)
        self.toggle_floating_button.pack(pady=10)

    def toggle_floating_widget(self):
        if self.floating_widget_visible:
            self.floating_window.withdraw()  # Hide the floating widget
            self.floating_widget_visible = False
        else:
            self.floating_window.deiconify()  # Show the floating widget
            self.floating_widget_visible = True

    # ======================== Command Management Methods ========================
    def add_custom_command(self):
        command = self.command_entry.get().strip()
        duration = self.duration_entry.get().strip()
        is_non_repeatable = self.non_repeatable_var.get()

        if not command or not duration:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            duration = float(duration)
        except ValueError:
            messagebox.showerror("Input Error", "Duration must be a number.")
            return

        self.commands.append((command, duration, is_non_repeatable))
        self.update_command_list()

    def add_predefined_command(self):
        command = self.predefined_var.get()
        duration = self.duration_entry.get().strip()
        is_non_repeatable = self.non_repeatable_var.get()

        if not command or not duration:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            duration = float(duration)
        except ValueError:
            messagebox.showerror("Input Error", "Duration must be a number.")
            return

        self.commands.append((command, duration, is_non_repeatable))
        self.update_command_list()

    def update_command_list(self):
        self.command_listbox.delete(0, tk.END)
        for command, duration, is_non_repeatable in self.commands:
            status = "[Non-Repeatable]" if is_non_repeatable else ""
            self.command_listbox.insert(tk.END, f"{command} | {duration}s {status}")

    def clear_commands(self):
        self.commands = []
        self.update_command_list()

    def move_command_up(self):
        selected = self.command_listbox.curselection()
        if not selected:
            return

        index = selected[0]
        if index == 0:
            return

        self.commands[index], self.commands[index - 1] = self.commands[index - 1], self.commands[index]
        self.update_command_list()
        self.command_listbox.select_set(index - 1)

    def move_command_down(self):
        selected = self.command_listbox.curselection()
        if not selected:
            return

        index = selected[0]
        if index == len(self.commands) - 1:
            return

        self.commands[index], self.commands[index + 1] = self.commands[index + 1], self.commands[index]
        self.update_command_list()
        self.command_listbox.select_set(index + 1)

    # ======================== Execution Methods ========================
    def start_execution(self):
        if not self.commands:
            messagebox.showerror("Execution Error", "No commands to execute.")
            return

        repetitions = self.repetition_entry.get().strip()
        if not repetitions:
            messagebox.showerror("Input Error", "Please enter the number of repetitions.")
            return

        try:
            repetitions = int(repetitions)
        except ValueError:
            messagebox.showerror("Input Error", "Repetitions must be an integer.")
            return

        self.is_running = True
        threading.Thread(target=self.execute_commands, args=(repetitions,), daemon=True).start()

    def stop_execution(self):
        self.is_running = False

    def execute_commands(self, repetitions):
        self.executed_non_repeatable_commands = set()  # Track non-repeatable commands
        for _ in range(repetitions):
            if not self.is_running:
                break
            for i, (command, duration, is_non_repeatable) in enumerate(self.commands):
                if not self.is_running:
                    break
                if is_non_repeatable and i in self.executed_non_repeatable_commands:
                    continue  # Skip non-repeatable commands that have already been executed
                self.execute_command(command, duration)
                if is_non_repeatable:
                    self.executed_non_repeatable_commands.add(i)  # Mark as executed

    def execute_command(self, command, duration):
        try:
            if "+" in command:
                keys = command.split("+")
                keyboard.press_and_release("+".join(keys))
            else:
                keyboard.press_and_release(command)
            time.sleep(duration)
        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed to execute {command}: {e}")

    # ======================== Import/Export Methods ========================
    def import_commands(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not filepath:
            return

        try:
            with open(filepath, "r") as file:
                self.commands = json.load(file)
            self.update_command_list()
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import commands: {e}")

    def export_commands(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not filepath:
            return

        try:
            with open(filepath, "w") as file:
                json.dump(self.commands, file)
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export commands: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CommandExecutor(root)
    root.mainloop()