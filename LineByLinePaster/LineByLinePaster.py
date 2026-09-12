import pyperclip
import pyautogui
import tkinter as tk
from tkinter import messagebox, scrolledtext
import win32clipboard
import win32com.client


class LineByLinePaster:
    def __init__(self, root):
        self.root = root
        self.root.title("Line-by-Line Paster")
        self.root.attributes("-topmost", True)  # Always on top
        self.table_data = []
        self.current_line = 0
        self.is_running = False

        # UI Setup
        self.label = tk.Label(root, text="Line-by-Line Paster", font=("Arial", 14))
        self.label.pack(pady=10)

        self.status = tk.Label(root, text="Waiting to start...", font=("Arial", 12))
        self.status.pack(pady=5)

        self.preview = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
        self.preview.pack(pady=5)

        self.start_button = tk.Button(root, text="Start", command=self.start, width=10)
        self.start_button.pack(pady=5)

        self.paste_button = tk.Button(root, text="Paste Line", command=self.paste_line, width=10, state="disabled")
        self.paste_button.pack(pady=5)

        self.previous_button = tk.Button(root, text="Previous Line", command=self.previous_line, width=10, state="disabled")
        self.previous_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop, width=10, state="disabled")
        self.stop_button.pack(pady=5)

    def read_excel_clipboard(self):
        """Read data directly from Excel clipboard."""
        excel = win32com.client.Dispatch("Excel.Application")
        clipboard_data = excel.Selection.Value
        self.table_data = []

        # Process data into rows and columns
        for row in clipboard_data:
            self.table_data.append([str(cell).strip() if cell is not None else "" for cell in row])

    def start(self):
        try:
            self.read_excel_clipboard()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read data from Excel clipboard: {e}")
            return

        if not self.table_data:
            messagebox.showerror("Error", "No data found in clipboard!")
            return

        self.current_line = 0
        self.is_running = True
        self.update_preview()
        self.status.config(text=f"Ready to paste line {self.current_line + 1}/{len(self.table_data)}")
        self.start_button.config(state="disabled")
        self.paste_button.config(state="normal")
        self.previous_button.config(state="normal")
        self.stop_button.config(state="normal")
        
        # Start the first pasting without waiting for another click
        self.show_message_and_paste()

    def show_message_and_paste(self):
        # Show the message before each line paste
        if pyautogui.confirm("Click in the writable field where you want to paste, then click OK to proceed.") == "OK":
            self.paste_line()

    def paste_line(self):
        if self.current_line < len(self.table_data):
            row = self.table_data[self.current_line]
            for i, cell in enumerate(row):
                pyperclip.copy(cell)  # Copy the full content of the cell
                pyautogui.hotkey("ctrl", "v")  # Paste into the active application
                if i < len(row) - 1:  # Only press Tab for cells before the last one
                    pyautogui.press("tab")
            pyautogui.press("enter")  # Confirm the line
            self.current_line += 1
            self.update_preview()
            self.update_status()

            # After pasting, show the message again for the next line
            self.show_message_and_paste()
        else:
            messagebox.showinfo("Info", "All lines have been processed.")

    def previous_line(self):
        if self.current_line > 0:
            self.current_line -= 1
            self.update_preview()
            self.update_status()
        else:
            messagebox.showinfo("Info", "Already at the first line.")

    def stop(self):
        self.is_running = False
        self.status.config(text="Stopped.")
        self.start_button.config(state="normal")
        self.paste_button.config(state="disabled")
        self.previous_button.config(state="disabled")
        self.stop_button.config(state="disabled")

    def update_preview(self):
        self.preview.delete("1.0", tk.END)
        if self.current_line < len(self.table_data):
            line_preview = " | ".join(self.table_data[self.current_line])
            self.preview.insert(tk.END, f"Current Line Preview:\n{line_preview}")
        else:
            self.preview.insert(tk.END, "All lines completed.")

    def update_status(self):
        if self.current_line < len(self.table_data):
            self.status.config(text=f"Ready to paste line {self.current_line + 1}/{len(self.table_data)}")
        else:
            self.status.config(text="All lines completed.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LineByLinePaster(root)
    root.mainloop()
