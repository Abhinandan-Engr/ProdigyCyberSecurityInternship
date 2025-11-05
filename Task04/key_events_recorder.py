# Task-04: Consent-based Keystroke Recorder (window-only; NOT system-wide)
# Requirements met: log keys pressed, save to a file, ethical + permission gate.
# Run: python key_events_recorder.py

import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

LOG_PATH = "key_log.txt"

class KeyRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task-04: Key Event Recorder (Window-only)")
        self.is_recording = False
        self.log_path = LOG_PATH

        # Header
        title = tk.Label(root, text="Key Event Recorder (Window-only, with consent)", font=("Segoe UI", 12, "bold"))
        title.pack(pady=(12, 6))

        # Consent gate
        self.var_consent = tk.BooleanVar(value=False)
        consent = tk.Checkbutton(
            root,
            text="I have explicit permission to record keys typed in THIS window.",
            variable=self.var_consent
        )
        consent.pack(pady=(0, 10))

        # Buttons
        btns = tk.Frame(root)
        btns.pack(pady=6)
        self.btn_start = tk.Button(btns, text="Start Recording", width=16, command=self.start_recording)
        self.btn_stop  = tk.Button(btns, text="Stop Recording",  width=16, command=self.stop_recording, state="disabled")
        self.btn_start.grid(row=0, column=0, padx=6)
        self.btn_stop.grid(row=0, column=1, padx=6)

        # Log file picker (optional)
        picker = tk.Frame(root)
        picker.pack(pady=(0, 8))
        tk.Label(picker, text="Log file:").grid(row=0, column=0, sticky="e", padx=(0,6))
        self.lbl_path = tk.Label(picker, text=self.log_path, fg="#555")
        self.lbl_path.grid(row=0, column=1, sticky="w")
        tk.Button(picker, text="Change…", command=self.change_path).grid(row=0, column=2, padx=6)

        # Status + live feed
        self.status = tk.Label(root, text="Status: Idle", fg="#444")
        self.status.pack(pady=(0, 6))

        self.feed = tk.Text(root, height=10, width=60, state="disabled")
        self.feed.pack(padx=10, pady=(0, 10))

        # Info
        info = (
            "Notes:\n"
            "• Recording works ONLY while this window is focused.\n"
            "• Purpose: educational demo with explicit consent.\n"
            "• Do not use to record other apps or people without permission."
        )
        tk.Label(root, text=info, justify="left", fg="#666").pack(padx=10, pady=(0,10))

        # Key binding (bound when recording)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def change_path(self):
        path = filedialog.asksaveasfilename(
            title="Choose log file",
            defaultextension=".txt",
            filetypes=[("Text files","*.txt"), ("All files","*.*")]
        )
        if path:
            self.log_path = path
            self.lbl_path.config(text=path)

    def start_recording(self):
        if not self.var_consent.get():
            messagebox.showwarning("Consent required", "Please tick the consent box before recording.")
            return
        self.is_recording = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.status.config(text="Status: Recording…", fg="green")
        # Bind keypress only now
        self.root.bind("<KeyPress>", self.on_key)

        # Create/append file header
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- Session start: {datetime.now().isoformat(timespec='seconds')} ---\n")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.btn_start.config(state="normal")
            self.btn_stop.config(state="disabled")
            self.status.config(text="Status: Stopped", fg="#444")
            # Unbind
            self.root.unbind("<KeyPress>")
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"--- Session end:   {datetime.now().isoformat(timespec='seconds')} ---\n")

    def on_key(self, event: tk.Event):
        if not self.is_recording:
            return
        key_sym = event.keysym           # e.g., a, A, space, Return
        key_code = event.keycode         # platform-specific code
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] key={key_sym!r} code={key_code}\n"

        # Append to file
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line)

        # Append to on-screen feed
        self.feed.config(state="normal")
        self.feed.insert("end", line)
        self.feed.see("end")
        self.feed.config(state="disabled")

    def on_close(self):
        self.stop_recording()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyRecorderApp(root)
    root.mainloop()
