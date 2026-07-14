#!/usr/bin/env python3
import sys
import subprocess
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# 1. Dependency Check and Auto-Install for pynput
try:
    from pynput import keyboard
except ImportError:
    print("pynput is not installed. Attempting to install...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--user", "--break-system-packages", "pynput"
        ])
        from pynput import keyboard
        print("Successfully installed pynput.")
    except Exception as e:
        print(f"Failed to auto-install pynput: {e}")
        sys.exit(1)

# All important cheats database
CHEATS = [
    {"action": "Full Health", "code": "aspirine", "hotkey": "<alt>+<shift>+h", "key_desc": "Alt+Shift+H"},
    {"action": "Full Armor", "code": "preciousprotection", "hotkey": "<alt>+<shift>+a", "key_desc": "Alt+Shift+A"},
    {"action": "Weapon Set 1 (Light)", "code": "thugstools", "hotkey": "<alt>+<shift>+1", "key_desc": "Alt+Shift+1"},
    {"action": "Weapon Set 2 (Medium)", "code": "professionaltools", "hotkey": "<alt>+<shift>+2", "key_desc": "Alt+Shift+2"},
    {"action": "Weapon Set 3 (Heavy)", "code": "nuttertools", "hotkey": "<alt>+<shift>+3", "key_desc": "Alt+Shift+3"},
    {"action": "Lower Wanted Level", "code": "leavemealone", "hotkey": "<alt>+<shift>+l", "key_desc": "Alt+Shift+L"},
    {"action": "Raise Wanted Level", "code": "youwonttakemealive", "hotkey": "<alt>+<shift>+u", "key_desc": "Alt+Shift+U"},
    {"action": "Spawn Rhino (Tank)", "code": "panzer", "hotkey": "<alt>+<shift>+t", "key_desc": "Alt+Shift+T"},
    {"action": "Spawn Sabre Turbo", "code": "gettherefast", "hotkey": "<alt>+<shift>+c", "key_desc": "Alt+Shift+C"},
    {"action": "Spawn Hotring Racer", "code": "getthereamazinglyfast", "hotkey": "<alt>+<shift>+r", "key_desc": "Alt+Shift+R"},
    {"action": "Spawn Love Fist Limo", "code": "rockandrollcar", "hotkey": "<alt>+<shift>+o", "key_desc": "Alt+Shift+O"},
    {"action": "Drive on Water", "code": "seaways", "hotkey": "<alt>+<shift>+w", "key_desc": "Alt+Shift+W"},
    {"action": "Flying Cars", "code": "comeflywithme", "hotkey": "<alt>+<shift>+f", "key_desc": "Alt+Shift+F"},
    {"action": "Perfect Handling", "code": "gripiseverything", "hotkey": "<alt>+<shift>+g", "key_desc": "Alt+Shift+G"},
    {"action": "Blow Up All Cars", "code": "bigbang", "hotkey": "<alt>+<shift>+b", "key_desc": "Alt+Shift+B"},
    {"action": "Clear Weather", "code": "alovelyday", "hotkey": "<alt>+<shift>+k", "key_desc": "Alt+Shift+K"},
    {"action": "Speed Up Game", "code": "ontherunway", "hotkey": "<alt>+<shift>+s", "key_desc": "Alt+Shift+S"},
    {"action": "Slow Down Game", "code": "booooooring", "hotkey": "<alt>+<shift>+m", "key_desc": "Alt+Shift+M"},
]

# Web browser keywords for safety filter
BROWSER_KEYWORDS = [
    "chrome", "firefox", "brave", "opera", "chromium", "vivaldi", 
    "edge", "safari", "waterfox", "librewolf", "epiphany", "web"
]

# Viewport size for the compact scrolling list
VIEWPORT_SIZE = 5

class CheatOverlay(tk.Toplevel):
    def __init__(self, parent, trainer):
        super().__init__(parent)
        self.trainer = trainer
        self.overrideredirect(True)       # Borderless window
        self.attributes("-topmost", True)   # Always stay on top of the game
        self.attributes("-alpha", 0.82)     # Higher transparency for gaming overlay
        self.configure(bg="#0c0c0e")
        
        # Position on the left middle of the screen (compact height)
        screen_height = self.winfo_screenheight()
        width = 270
        height = 320
        x = 30
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Tekken metal/blood red border
        border_frame = tk.Frame(self, bg="#ff0033", bd=3)
        border_frame.pack(fill=tk.BOTH, expand=True)
        
        inner_frame = tk.Frame(border_frame, bg="#0c0c0e")
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Header (Tekken style!)
        self.title_lbl = tk.Label(
            inner_frame, 
            text="TEKKEN CHEAT MENU", 
            font=("Impact", 13, "italic"), 
            fg="#ffcc00", # Flame yellow-orange
            bg="#0c0c0e",
            pady=6
        )
        self.title_lbl.pack(fill=tk.X)
        
        # Up Scroll Indicator
        self.up_indicator = tk.Label(
            inner_frame,
            text="▲",
            font=("Courier", 10, "bold"),
            fg="#222226", # Default dark/hidden
            bg="#0c0c0e"
        )
        self.up_indicator.pack(fill=tk.X)
        
        # List frame for the viewport
        self.labels = []
        self.list_frame = tk.Frame(inner_frame, bg="#0c0c0e")
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Draw viewport placeholders
        for i in range(VIEWPORT_SIZE):
            lbl = tk.Label(
                self.list_frame,
                text="",
                font=("Arial Black", 8, "bold"),
                fg="#ff9999", # Dim red/white
                bg="#0c0c0e",
                anchor="center",
                pady=4
            )
            lbl.pack(fill=tk.X, pady=1)
            self.labels.append(lbl)
            
        # Down Scroll Indicator
        self.down_indicator = tk.Label(
            inner_frame,
            text="▼",
            font=("Courier", 10, "bold"),
            fg="#222226", # Default dark/hidden
            bg="#0c0c0e"
        )
        self.down_indicator.pack(fill=tk.X)
        
        # Help Footer
        help_lbl = tk.Label(
            inner_frame,
            text="[▲/▼] NAVIGATE   [ENTER] SELECT",
            font=("Helvetica", 7, "bold"),
            fg="#6c6c7a",
            bg="#0c0c0e",
            pady=4
        )
        help_lbl.pack(fill=tk.X)
        
        # Scrolling states
        self.selected_index = 0
        self.scroll_start = 0
        
        # Draw the initial list viewport
        self.update_viewport()
        
        # Bind keyboard events inside the overlay
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.bind("<Return>", self.select_item)
        self.bind("<Escape>", self.hide_overlay)
        self.bind("`", self.hide_overlay)
        self.bind("<F1>", self.hide_overlay)

    def update_viewport(self):
        """Redraws the visible window of cheats and updates indicators."""
        # Handle scrolling logic
        if self.selected_index < self.scroll_start:
            self.scroll_start = self.selected_index
        elif self.selected_index >= self.scroll_start + VIEWPORT_SIZE:
            self.scroll_start = self.selected_index - VIEWPORT_SIZE + 1
            
        # Show glowing indicators if scrolling is available
        if self.scroll_start > 0:
            self.up_indicator.configure(fg="#ffcc00") # Flame yellow glow
        else:
            self.up_indicator.configure(fg="#222226") # Muted black-purple
            
        if self.scroll_start + VIEWPORT_SIZE < len(CHEATS):
            self.down_indicator.configure(fg="#ffcc00") # Flame yellow glow
        else:
            self.down_indicator.configure(fg="#222226") # Muted
            
        # Update text labels
        for i in range(VIEWPORT_SIZE):
            item_index = self.scroll_start + i
            if item_index < len(CHEATS):
                cheat = CHEATS[item_index]
                if item_index == self.selected_index:
                    # Highlight selected item like a Tekken bracket choice
                    self.labels[i].configure(
                        text=f"►  {cheat['action'].upper()}  ◄",
                        fg="#ffffff", 
                        bg="#ff3300", # Glowing hot orange selection
                        font=("Arial Black", 9, "bold")
                    )
                else:
                    # Normal item
                    self.labels[i].configure(
                        text=cheat['action'].upper(),
                        fg="#ff9999", # Blood-rose color
                        bg="#0c0c0e",
                        font=("Arial Black", 8, "bold")
                    )
            else:
                self.labels[i].configure(text="", bg="#0c0c0e")

    def move_up(self, event=None):
        self.selected_index = (self.selected_index - 1) % len(CHEATS)
        self.update_viewport()
        
    def move_down(self, event=None):
        self.selected_index = (self.selected_index + 1) % len(CHEATS)
        self.update_viewport()
        
    def select_item(self, event=None):
        selected_cheat = CHEATS[self.selected_index]
        self.hide_overlay()
        self.trainer.trigger_cheat_directly(selected_cheat)

    def show_overlay(self):
        # Set selection back to index 0 on open
        self.selected_index = 0
        self.scroll_start = 0
        self.update_viewport()
        
        self.deiconify()
        self.lift()
        self.focus_force()
        self.focus_set()
        
    def hide_overlay(self, event=None):
        self.withdraw()


class ViceCityCheatTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("GTA Vice City Cheat Trainer")
        self.root.geometry("660x780")
        self.root.configure(bg="#12072b")
        self.root.resizable(False, False)

        # State variables
        self.listener_active = tk.BooleanVar(value=True)
        self.browser_filter_active = tk.BooleanVar(value=True)
        self.hotkey_listener = None
        self.raw_key_listener = None
        
        # Setup Trainer UI
        self.setup_ui()
        
        # Setup Overlay Menu (starts hidden)
        self.overlay = CheatOverlay(self.root, self)
        self.overlay.withdraw()
        
        # Start Global Listeners
        self.start_listeners()

    def log(self, message):
        """Thread-safe logging utility."""
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}\n"
        
        def update_gui():
            self.log_area.insert(tk.END, formatted)
            self.log_area.see(tk.END)
            
        self.root.after(0, update_gui)

    def setup_ui(self):
        # Header Banner
        title_frame = tk.Frame(self.root, bg="#12072b", pady=10)
        title_frame.pack(fill=tk.X)
        
        title_lbl = tk.Label(
            title_frame, 
            text="★ VICE CITY CHEAT TRAINER ★", 
            font=("Helvetica", 18, "bold"), 
            fg="#ff007f", 
            bg="#12072b"
        )
        title_lbl.pack()
        
        subtitle_lbl = tk.Label(
            title_frame, 
            text="Shortcut Key Trainer & Left Side Menu Overlay", 
            font=("Helvetica", 10, "italic"), 
            fg="#00f0ff", 
            bg="#12072b"
        )
        subtitle_lbl.pack()

        # Cheat Grid Frame
        grid_frame = tk.LabelFrame(
            self.root, 
            text=" SHORTCUTS & ACTION LIST ", 
            font=("Helvetica", 10, "bold"),
            fg="#00f0ff", 
            bg="#1e0b3e", 
            bd=2, 
            relief=tk.GROOVE,
            padx=10, 
            pady=10
        )
        grid_frame.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)

        # Header Columns
        tk.Label(grid_frame, text="Action", font=("Helvetica", 9, "bold"), fg="#ffe5f2", bg="#1e0b3e", anchor="w").grid(row=0, column=0, sticky="ew", padx=5, pady=2)
        tk.Label(grid_frame, text="Hotkey", font=("Helvetica", 9, "bold"), fg="#ffe5f2", bg="#1e0b3e", anchor="w").grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        tk.Label(grid_frame, text="Cheat Code", font=("Helvetica", 9, "bold"), fg="#ffe5f2", bg="#1e0b3e", anchor="w").grid(row=0, column=2, sticky="ew", padx=5, pady=2)
        tk.Label(grid_frame, text="Manual", font=("Helvetica", 9, "bold"), fg="#ffe5f2", bg="#1e0b3e").grid(row=0, column=3, padx=5, pady=2)

        grid_frame.columnconfigure(0, weight=3)
        grid_frame.columnconfigure(1, weight=2)
        grid_frame.columnconfigure(2, weight=2)
        grid_frame.columnconfigure(3, weight=1)

        # Populate rows
        for idx, cheat in enumerate(CHEATS, start=1):
            bg_row = "#260f4d" if idx % 2 == 0 else "#1e0b3e"
            
            tk.Label(grid_frame, text=cheat["action"], font=("Helvetica", 8, "bold"), fg="#ffffff", bg=bg_row, anchor="w").grid(row=idx, column=0, sticky="ew", padx=5, pady=2)
            tk.Label(grid_frame, text=cheat["key_desc"], font=("Helvetica", 8, "bold"), fg="#ff007f", bg=bg_row, anchor="w").grid(row=idx, column=1, sticky="ew", padx=5, pady=2)
            tk.Label(grid_frame, text=cheat["code"].upper(), font=("Helvetica", 8), fg="#b6a2d9", bg=bg_row, anchor="w").grid(row=idx, column=2, sticky="ew", padx=5, pady=2)
            
            # Action button
            btn = tk.Button(
                grid_frame, 
                text="Send", 
                font=("Helvetica", 7, "bold"),
                fg="#ffffff", 
                bg="#ff007f", 
                activebackground="#00f0ff", 
                activeforeground="#12072b",
                bd=0, 
                padx=6,
                pady=1,
                cursor="hand2",
                command=lambda c=cheat: self.manual_trigger(c)
            )
            btn.grid(row=idx, column=3, padx=5, pady=1)

        # Controls
        control_frame = tk.Frame(self.root, bg="#12072b")
        control_frame.pack(padx=15, pady=5, fill=tk.X)

        # Browser Check Checkbox
        filter_chk = tk.Checkbutton(
            control_frame, 
            text="Only type when browser is active (Recommended)", 
            variable=self.browser_filter_active,
            font=("Helvetica", 9),
            fg="#ffe5f2", 
            bg="#12072b", 
            activebackground="#12072b", 
            activeforeground="#ff007f",
            selectcolor="#1e0b3e"
        )
        filter_chk.pack(side=tk.LEFT, pady=5)

        # Shortcuts Toggle Button
        self.toggle_btn = tk.Button(
            control_frame, 
            text="DISABLE HOTKEYS", 
            font=("Helvetica", 9, "bold"),
            fg="#12072b", 
            bg="#00f0ff", 
            activebackground="#ff007f", 
            activeforeground="#ffffff",
            bd=1, 
            padx=10, 
            pady=3,
            command=self.toggle_listeners
        )
        self.toggle_btn.pack(side=tk.RIGHT, pady=5)

        # Overlay Info Banner
        overlay_info = tk.Label(
            self.root,
            text="PRO-TIP: Press ` (Backtick) or F1 while gaming to open the menu on the left side!",
            font=("Helvetica", 9, "bold"),
            fg="#00f0ff",
            bg="#1e0b3e",
            pady=4
        )
        overlay_info.pack(fill=tk.X, padx=15, pady=3)

        # Logger Box Header
        log_lbl = tk.Label(
            self.root, 
            text="Trainer Activity Console Output", 
            font=("Helvetica", 9, "bold"), 
            fg="#b6a2d9", 
            bg="#12072b"
        )
        log_lbl.pack(anchor="w", padx=15, pady=(5, 0))

        # Logger Scroll Area
        self.log_area = scrolledtext.ScrolledText(
            self.root, 
            height=6, 
            bg="#0b031a", 
            fg="#00f0ff", 
            insertbackground="#00f0ff",
            font=("Courier", 8),
            bd=1,
            relief=tk.SOLID
        )
        self.log_area.pack(padx=15, pady=(2, 15), fill=tk.X)
        self.log_area.insert(tk.END, "=== VICE CITY CHEAT TRAINER ACTIVE ===\n")
        self.log_area.insert(tk.END, "[Overlay Info] Press ` (Backtick) or F1 to open the Left Menu Overlay.\n")

    def get_active_window_title(self):
        """Find the active window's title."""
        try:
            res = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowname"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                check=True
            )
            return res.stdout.strip()
        except Exception:
            return ""

    def is_browser_active(self):
        """Ensure simulated keystrokes are safe by target window checks."""
        title = self.get_active_window_title().lower()
        if not title:
            return False
        return any(kw in title for kw in BROWSER_KEYWORDS)

    def trigger_cheat_directly(self, cheat):
        """Initiates typing of the cheat code after returning focus to the game."""
        def execute_typing():
            # Wait for overlay menu to close completely and return focus to game
            time.sleep(0.15)
            
            # Safety Filter Check
            if self.browser_filter_active.get() and not self.is_browser_active():
                self.log(f"Canceled typing: Active window is not a web browser.")
                return

            self.log(f"Typing cheat: {cheat['code'].upper()} ({cheat['action']})")
            try:
                subprocess.run([
                    "xdotool", "type", 
                    "--clearmodifiers", 
                    "--delay", "30", 
                    cheat["code"]
                ], check=True)
                self.log(f"Typed cheat successfully.")
            except Exception as e:
                self.log(f"Error typing cheat: {e}")

        threading.Thread(target=execute_typing, daemon=True).start()

    def handle_global_shortcut(self, cheat):
        """Triggers standard hotkey combo activation."""
        if not self.listener_active.get():
            return
            
        # Check active window filter
        if self.browser_filter_active.get() and not self.is_browser_active():
            self.log(f"Ignored hotkey ({cheat['action']}): Focus is not on a web browser.")
            return

        self.log(f"Hotkey triggered: {cheat['action']}")
        self.trigger_cheat_directly(cheat)

    def manual_trigger(self, cheat):
        """Fires when clicking the manual Send buttons."""
        def delay_type():
            self.log(f"Manual send clicked. Click back into the game window within 2 seconds...")
            time.sleep(2)
            
            if self.browser_filter_active.get() and not self.is_browser_active():
                self.log("Manual send canceled: Active window is not a web browser.")
                return
                
            self.log(f"Typing cheat: {cheat['code'].upper()}")
            try:
                subprocess.run([
                    "xdotool", "type", 
                    "--clearmodifiers", 
                    "--delay", "30", 
                    cheat["code"]
                ], check=True)
                self.log("Manual cheat typed successfully.")
            except Exception as e:
                self.log(f"Error typing cheat: {e}")

        threading.Thread(target=delay_type, daemon=True).start()

    def on_raw_key_press(self, key):
        """Raw single key listener to open the overlay menu."""
        if not self.listener_active.get():
            return
            
        is_trigger = False
        try:
            # Check for backtick (grave tilde) key
            if key.char == '`':
                is_trigger = True
        except AttributeError:
            # Check for F1 key
            if key == keyboard.Key.f1:
                is_trigger = True
                
        if is_trigger:
            self.log("Toggle overlay menu requested.")
            # Trigger GUI update safely on the main thread
            self.root.after(0, self.toggle_overlay)

    def toggle_overlay(self):
        """Shows or hides the overlay."""
        if self.overlay.winfo_viewable():
            self.overlay.hide_overlay()
            self.log("Overlay menu hidden.")
        else:
            self.overlay.show_overlay()
            self.log("Overlay menu opened.")

    def start_listeners(self):
        """Initializes the background hotkeys and raw key listeners."""
        # 1. Combo hotkeys Map
        hotkeys_map = {}
        for cheat in CHEATS:
            # Bind lambda passing cheat
            hotkeys_map[cheat["hotkey"]] = lambda c=cheat: self.handle_global_shortcut(c)

        try:
            # Combo hotkey listener
            self.hotkey_listener = keyboard.GlobalHotKeys(hotkeys_map)
            self.hotkey_listener.start()

            # Raw key listener (for single key menu triggers like ` and F1)
            self.raw_key_listener = keyboard.Listener(on_press=self.on_raw_key_press)
            self.raw_key_listener.start()
            
            self.log("[System] Global key listeners successfully initiated.")
        except Exception as e:
            self.log(f"[Error] Failed to initiate listeners: {e}")
            messagebox.showerror(
                "Hotkey Listener Error", 
                f"Failed to start key listeners: {e}\nVerify keyboard/X11 permissions."
            )

    def stop_listeners(self):
        """Shutdown keyboard listeners."""
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            self.hotkey_listener = None
        if self.raw_key_listener:
            self.raw_key_listener.stop()
            self.raw_key_listener = None
        self.log("[System] Global key listeners terminated.")

    def toggle_listeners(self):
        """Interface toggle to enable/disable listeners."""
        if self.listener_active.get():
            self.listener_active.set(False)
            self.stop_listeners()
            self.toggle_btn.configure(
                text="ENABLE HOTKEYS", 
                bg="#ff007f", 
                fg="#ffffff"
            )
            self.log("[System] Global Trainer shortcuts DISABLED.")
        else:
            self.listener_active.set(True)
            self.start_listeners()
            self.toggle_btn.configure(
                text="DISABLE HOTKEYS", 
                bg="#00f0ff", 
                fg="#12072b"
            )
            self.log("[System] Global Trainer shortcuts ENABLED.")


if __name__ == "__main__":
    # Check for xdotool installation
    if subprocess.call(["which", "xdotool"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        print("Error: xdotool is not installed. Run 'sudo apt install xdotool' to install it.")
        sys.exit(1)

    root = tk.Tk()
    app = ViceCityCheatTrainer(root)
    
    # Handle window close nicely
    def on_closing():
        app.stop_listeners()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
