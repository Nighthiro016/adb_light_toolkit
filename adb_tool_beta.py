import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import subprocess
import threading
import re
import os
import time
import sys
import zipfile
import tempfile
import shutil
from datetime import datetime
import json

ADB_PATH = r"D:\android version\ADB and Fastboot++ v1.1.1 Portable\adb.exe"

class ThemeManager:
    """Manages application themes with modern dark text UI support"""
    def __init__(self):
        self.themes = {
            "Light": {
                "bg": "#f5f7fa",
                "fg": "#2c3e50",
                "button_bg": "#3498db",
                "button_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "entry_fg": "#2c3e50",
                "tree_bg": "#ffffff",
                "tree_fg": "#2c3e50",
                "tree_sel": "#e3f2fd",
                "log_bg": "#f8f9fa",
                "log_fg": "#2c3e50",
                "canvas_bg": "#ffffff",
                "accent": "#3498db",
                "tab_bg": "#e9ecef",
                "tab_fg": "#495057",
                "tab_active": "#dee2e6",
                "heading_bg": "#e9ecef",
                "heading_fg": "#2c3e50",
                "text_bg": "#ffffff",
                "text_fg": "#2c3e50",
                "disabled_fg": "#95a5a6",
                "card_bg": "#ffffff",
                "card_border": "#dfe6e9",
                "button_hover": "#2980b9",
                "button_active": "#1f618d"
            },
            "Dark": {
                "bg": "#1e293b",
                "fg": "#f1f5f9",
                "button_bg": "#3b82f6",
                "button_fg": "#ffffff",
                "entry_bg": "#334155",
                "entry_fg": "#f1f5f9",
                "tree_bg": "#334155",
                "tree_fg": "#f1f5f9",
                "tree_sel": "#475569",
                "log_bg": "#0f172a",
                "log_fg": "#f1f5f9",
                "canvas_bg": "#0f172a",
                "accent": "#60a5fa",
                "tab_bg": "#334155",
                "tab_fg": "#f1f5f9",
                "tab_active": "#475569",
                "heading_bg": "#334155",
                "heading_fg": "#f1f5f9",
                "text_bg": "#1e293b",
                "text_fg": "#f1f5f9",
                "disabled_fg": "#94a3b8",
                "card_bg": "#334155",
                "card_border": "#475569",
                "button_hover": "#2563eb",
                "button_active": "#1d4ed8"
            },
            "AMOLED": {
                "bg": "#000000",
                "fg": "#e2e8f0",
                "button_bg": "#0f172a",
                "button_fg": "#22d3ee",
                "entry_bg": "#0f172a",
                "entry_fg": "#e2e8f0",
                "tree_bg": "#000000",
                "tree_fg": "#e2e8f0",
                "tree_sel": "#1e293b",
                "log_bg": "#000000",
                "log_fg": "#22d3ee",
                "canvas_bg": "#000000",
                "accent": "#22d3ee",
                "tab_bg": "#0f172a",
                "tab_fg": "#22d3ee",
                "tab_active": "#1e293b",
                "heading_bg": "#0f172a",
                "heading_fg": "#22d3ee",
                "text_bg": "#000000",
                "text_fg": "#e2e8f0",
                "disabled_fg": "#64748b",
                "card_bg": "#0f172a",
                "card_border": "#1e293b",
                "button_hover": "#0ea5e9",
                "button_active": "#0284c7"
            },
            "Ocean": {
                "bg": "#0c1445",
                "fg": "#e0f2fe",
                "button_bg": "#0ea5e9",
                "button_fg": "#ffffff",
                "entry_bg": "#1e3a8a",
                "entry_fg": "#e0f2fe",
                "tree_bg": "#1e3a8a",
                "tree_fg": "#e0f2fe",
                "tree_sel": "#1e40af",
                "log_bg": "#0c1445",
                "log_fg": "#e0f2fe",
                "canvas_bg": "#0c1445",
                "accent": "#38bdf8",
                "tab_bg": "#1e3a8a",
                "tab_fg": "#e0f2fe",
                "tab_active": "#1e40af",
                "heading_bg": "#1e3a8a",
                "heading_fg": "#e0f2fe",
                "text_bg": "#0c1445",
                "text_fg": "#e0f2fe",
                "disabled_fg": "#7dd3fc",
                "card_bg": "#1e3a8a",
                "card_border": "#1e40af",
                "button_hover": "#0284c7",
                "button_active": "#0369a1"
            }
        }
        self.current_theme = "Dark"  # Default theme
        
    def get_theme(self):
        return self.themes[self.current_theme]
    
    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False

class ADBManager:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB Manager Pro")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Performance monitoring
        self.monitoring = True
        self.last_net_stats = {}
        
        # Device connection status
        self.connection_status = tk.StringVar()
        self.connection_status.set("Disconnected")
        
        # Shortcuts for quick install
        self.shortcuts = []
        
        # Setup menu
        self.setup_menu()
        
        # Setup UI
        self.setup_ui()
        
        # Apply theme
        self.apply_theme()
        
        # Check connection in background
        self.check_connection()
        
        # Start performance monitoring
        self.monitor_performance()
        
        # Load shortcuts
        self.load_shortcuts()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_menu(self):
        """Create menu bar with theme options"""
        menubar = tk.Menu(self.root)
        
        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Light Theme", command=lambda: self.change_theme("Light"))
        theme_menu.add_command(label="Dark Theme", command=lambda: self.change_theme("Dark"))
        theme_menu.add_command(label="AMOLED Theme", command=lambda: self.change_theme("AMOLED"))
        theme_menu.add_command(label="Ocean Theme", command=lambda: self.change_theme("Ocean"))
        menubar.add_cascade(label="Themes", menu=theme_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Clear Log", command=self.clear_log)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)

    def setup_ui(self):
        # Main container with modern styling
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Connection status bar with modern styling
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        status_label = ttk.Label(status_frame, text="Status:", font=("Segoe UI", 10, "bold"))
        status_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.status_label = ttk.Label(status_frame, textvariable=self.connection_status, font=("Segoe UI", 10))
        self.status_label.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(status_frame, text="Recheck", command=self.check_connection).pack(side=tk.LEFT, padx=5)
        ttk.Button(status_frame, text="Refresh Apps", command=self.refresh_apps_list).pack(side=tk.LEFT, padx=5)
        
        # Root status
        self.root_status = tk.StringVar(value="Root: Checking...")
        self.root_label = ttk.Label(status_frame, textvariable=self.root_status, font=("Segoe UI", 10))
        self.root_label.pack(side=tk.LEFT, padx=15)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Apps Tab
        apps_frame = ttk.Frame(self.notebook)
        self.notebook.add(apps_frame, text="Apps Management")
        self.setup_apps_tab(apps_frame)
        
        # File Transfer Tab
        file_frame = ttk.Frame(self.notebook)
        self.notebook.add(file_frame, text="File Transfer")
        self.setup_file_tab(file_frame)
        
        # Device Commands Tab
        cmd_frame = ttk.Frame(self.notebook)
        self.notebook.add(cmd_frame, text="Device Commands")
        self.setup_cmd_tab(cmd_frame)
        
        # Performance Tab
        perf_frame = ttk.Frame(self.notebook)
        self.notebook.add(perf_frame, text="Performance")
        self.setup_perf_tab(perf_frame)
        
        # Root Tools Tab
        root_frame = ttk.Frame(self.notebook)
        self.notebook.add(root_frame, text="Root Tools")
        self.setup_root_tab(root_frame)
        
        # Quick Install Tab
        quick_frame = ttk.Frame(self.notebook)
        self.notebook.add(quick_frame, text="Quick Install")
        self.setup_quick_tab(quick_frame)
        
        # Log Output
        log_frame = ttk.LabelFrame(main_container, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        self.log_area = scrolledtext.ScrolledText(log_frame, height=10, font=("Consolas", 9))
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_area.config(state=tk.DISABLED)

    def setup_quick_tab(self, parent):
        """Create tab for quick app installation shortcuts"""
        # Header with instructions
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(
            header_frame, 
            text="Create shortcuts to frequently installed apps",
            font=("Segoe UI", 12, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        # Add shortcut button
        add_btn = ttk.Button(
            header_frame, 
            text="+ Add Shortcut", 
            command=self.add_shortcut
        )
        add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Shortcuts container with scrollbar
        container_frame = ttk.Frame(parent)
        container_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Canvas for scrollable area
        self.shortcuts_canvas = tk.Canvas(container_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=self.shortcuts_canvas.yview)
        self.shortcuts_scrollable_frame = ttk.Frame(self.shortcuts_canvas)
        
        self.shortcuts_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.shortcuts_canvas.configure(scrollregion=self.shortcuts_canvas.bbox("all"))
        )
        
        self.shortcuts_canvas.create_window((0, 0), window=self.shortcuts_scrollable_frame, anchor="nw")
        self.shortcuts_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.shortcuts_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind canvas events for proper scrolling
        self.shortcuts_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Add a welcome message if no shortcuts exist
        if not self.shortcuts:
            welcome_frame = ttk.Frame(self.shortcuts_scrollable_frame)
            welcome_frame.pack(fill=tk.BOTH, expand=True, pady=50)
            
            ttk.Label(
                welcome_frame, 
                text="No shortcuts yet.\nClick '+ Add Shortcut' to create one.",
                font=("Segoe UI", 11),
                justify=tk.CENTER
            ).pack()

    def _on_mousewheel(self, event):
        self.shortcuts_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_shortcut(self):
        file_path = filedialog.askopenfilename(
            title="Select APK or XAPK",
            filetypes=[("Android Packages", "*.apk *.xapk"), ("APK Files", "*.apk"), ("XAPK Files", "*.xapk")]
        )
        
        if not file_path:
            return
        
        # Extract app name if possible
        app_name = os.path.basename(file_path)
        if file_path.endswith(".apk"):
            # Try to get app name from APK
            try:
                with zipfile.ZipFile(file_path, 'r') as z:
                    try:
                        with z.open('AndroidManifest.xml') as manifest:
                            content = manifest.read()
                            if b'application' in content and b'label=' in content:
                                start = content.find(b'label="') + 7
                                end = content.find(b'"', start)
                                if start > 6 and end > start:
                                    app_name = content[start:end].decode('utf-8', errors='ignore')
                    except:
                        pass
            except:
                pass
        
        # Create shortcut data
        shortcut = {
            "name": app_name,
            "path": file_path,
            "type": "APK" if file_path.endswith(".apk") else "XAPK"
        }
        
        # Add to shortcuts list
        self.shortcuts.append(shortcut)
        self.save_shortcuts()
        
        # Refresh UI
        self.refresh_shortcuts_ui()
        self.log(f"Added shortcut for {app_name}")

    def refresh_shortcuts_ui(self):
        # Clear existing widgets
        for widget in self.shortcuts_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Add welcome message if no shortcuts
        if not self.shortcuts:
            welcome_frame = ttk.Frame(self.shortcuts_scrollable_frame)
            welcome_frame.pack(fill=tk.BOTH, expand=True, pady=50)
            
            ttk.Label(
                welcome_frame, 
                text="No shortcuts yet.\nClick '+ Add Shortcut' to create one.",
                font=("Segoe UI", 11),
                justify=tk.CENTER
            ).pack()
            return
        
        # Create shortcut cards
        for i, shortcut in enumerate(self.shortcuts):
            self.create_shortcut_card(shortcut, i)

    def create_shortcut_card(self, shortcut, index):
        # Create card frame with modern styling
        theme = self.theme_manager.get_theme()
        
        card_frame = ttk.Frame(
            self.shortcuts_scrollable_frame,
            style="Card.TFrame"
        )
        card_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Card content
        content_frame = ttk.Frame(card_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        # App icon placeholder
        icon_frame = tk.Frame(content_frame, width=50, height=50, bg=theme["card_bg"], highlightthickness=1, highlightbackground=theme["card_border"])
        icon_frame.pack(side=tk.LEFT, padx=(0, 15))
        icon_frame.pack_propagate(False)
        
        # App icon text
        icon_label = tk.Label(
            icon_frame,
            text=shortcut["type"][0],
            bg=theme["card_bg"],
            fg=theme["accent"],
            font=("Segoe UI", 16, "bold")
        )
        icon_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # App info
        info_frame = ttk.Frame(content_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # App name
        name_label = ttk.Label(
            info_frame,
            text=shortcut["name"],
            font=("Segoe UI", 11, "bold")
        )
        name_label.pack(anchor=tk.W)
        
        # App path
        path_label = ttk.Label(
            info_frame,
            text=shortcut["path"],
            font=("Segoe UI", 9),
            foreground=theme["disabled_fg"]
        )
        path_label.pack(anchor=tk.W)
        
        # Buttons frame
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(side=tk.RIGHT, padx=10)
        
        # Install button
        install_btn = ttk.Button(
            btn_frame,
            text="Install",
            command=lambda s=shortcut: self.install_shortcut(s)
        )
        install_btn.pack(side=tk.LEFT, padx=5)
        
        # Remove button
        remove_btn = ttk.Button(
            btn_frame,
            text="Remove",
            command=lambda idx=index: self.remove_shortcut(idx)
        )
        remove_btn.pack(side=tk.LEFT, padx=5)

    def install_shortcut(self, shortcut):
        self.log(f"Installing {shortcut['name']} from shortcut...")
        
        if shortcut["type"] == "APK":
            self.run_threaded(lambda: self.run_adb_command(["install", shortcut["path"]]))
        else:  # XAPK
            self.run_threaded(lambda: self._install_xapk_thread(shortcut["path"]))

    def remove_shortcut(self, index):
        if 0 <= index < len(self.shortcuts):
            removed = self.shortcuts.pop(index)
            self.save_shortcuts()
            self.refresh_shortcuts_ui()
            self.log(f"Removed shortcut for {removed['name']}")

    def save_shortcuts(self):
        try:
            shortcuts_data = []
            for s in self.shortcuts:
                shortcuts_data.append({
                    "name": s["name"],
                    "path": s["path"],
                    "type": s["type"]
                })
            
            # Create app data directory if it doesn't exist
            app_data_dir = os.path.join(os.path.expanduser("~"), ".adb_manager_pro")
            if not os.path.exists(app_data_dir):
                os.makedirs(app_data_dir)
            
            # Save shortcuts to file
            with open(os.path.join(app_data_dir, "shortcuts.json"), "w") as f:
                json.dump(shortcuts_data, f)
        except Exception as e:
            self.log(f"Error saving shortcuts: {str(e)}")

    def load_shortcuts(self):
        try:
            app_data_dir = os.path.join(os.path.expanduser("~"), ".adb_manager_pro")
            shortcuts_file = os.path.join(app_data_dir, "shortcuts.json")
            
            if os.path.exists(shortcuts_file):
                with open(shortcuts_file, "r") as f:
                    shortcuts_data = json.load(f)
                
                self.shortcuts = []
                for s in shortcuts_data:
                    self.shortcuts.append({
                        "name": s["name"],
                        "path": s["path"],
                        "type": s["type"]
                    })
                
                # Refresh UI after a short delay to ensure the tab is ready
                self.root.after(100, self.refresh_shortcuts_ui)
        except Exception as e:
            self.log(f"Error loading shortcuts: {str(e)}")
            self.shortcuts = []

    def on_closing(self):
        self.save_shortcuts()
        self.root.destroy()

    def setup_apps_tab(self, parent):
        # Treeview for apps
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        columns = ("app_name", "package_name", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("app_name", text="Application Name")
        self.tree.heading("package_name", text="Package Name")
        self.tree.heading("status", text="Status")
        
        self.tree.column("app_name", width=300, anchor=tk.W)
        self.tree.column("package_name", width=300, anchor=tk.W)
        self.tree.column("status", width=100, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Placeholder text while loading
        self.tree.insert("", tk.END, values=("Loading apps...", "", ""))
        
        # Action buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=15, pady=15)
        
        self.install_btn = ttk.Button(btn_frame, text="Install APK", command=self.install_app)
        self.install_btn.pack(side=tk.LEFT, padx=5)
        
        self.xapk_btn = ttk.Button(btn_frame, text="Install XAPK", command=self.install_xapk)
        self.xapk_btn.pack(side=tk.LEFT, padx=5)
        
        self.uninstall_btn = ttk.Button(btn_frame, text="Uninstall", command=self.uninstall_app)
        self.uninstall_btn.pack(side=tk.LEFT, padx=5)
        
        self.disable_btn = ttk.Button(btn_frame, text="Disable", command=self.disable_app)
        self.disable_btn.pack(side=tk.LEFT, padx=5)
        
        self.enable_btn = ttk.Button(btn_frame, text="Enable", command=self.enable_app)
        self.enable_btn.pack(side=tk.LEFT, padx=5)
        
        self.cache_btn = ttk.Button(btn_frame, text="Clear Cache", command=self.clear_app_cache)
        self.cache_btn.pack(side=tk.LEFT, padx=5)

    def setup_file_tab(self, parent):
        # Pull Section
        pull_frame = ttk.LabelFrame(parent, text="Pull File from Device")
        pull_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(pull_frame, text="Source Path (Device):").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.pull_src = ttk.Entry(pull_frame, width=50)
        self.pull_src.insert(0, "/sdcard/Download/")
        self.pull_src.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(pull_frame, text="Destination (PC):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.pull_dest = ttk.Entry(pull_frame, width=50)
        self.pull_dest.insert(0, os.path.expanduser("~\\Downloads"))
        self.pull_dest.grid(row=1, column=1, padx=10, pady=10)
        
        self.pull_browse_btn = ttk.Button(pull_frame, text="Browse", command=self.browse_dest)
        self.pull_browse_btn.grid(row=1, column=2, padx=10, pady=10)
        
        self.pull_btn = ttk.Button(pull_frame, text="Pull File", command=self.pull_file)
        self.pull_btn.grid(row=2, column=1, pady=10)
        
        # Push Section
        push_frame = ttk.LabelFrame(parent, text="Push File to Device")
        push_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(push_frame, text="Source Path (PC):").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.push_src = ttk.Entry(push_frame, width=50)
        self.push_src.grid(row=0, column=1, padx=10, pady=10)
        
        self.push_browse_btn = ttk.Button(push_frame, text="Browse", command=self.browse_src)
        self.push_browse_btn.grid(row=0, column=2, padx=10, pady=10)
        
        ttk.Label(push_frame, text="Destination (Device):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.push_dest = ttk.Entry(push_frame, width=50)
        self.push_dest.insert(0, "/sdcard/Download/")
        self.push_dest.grid(row=1, column=1, padx=10, pady=10)
        
        self.push_btn = ttk.Button(push_frame, text="Push File", command=self.push_file)
        self.push_btn.grid(row=2, column=1, pady=10)

    def setup_cmd_tab(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=15, pady=15)
        
        commands = [
            ("Reboot", "reboot"),
            ("Reboot to Bootloader", "reboot bootloader"),
            ("Reboot to Recovery", "reboot recovery"),
            ("Take Screenshot", "shell screencap -p /sdcard/screenshot.png"),
            ("Show Device Info", "shell getprop"),
            ("List Devices", "devices -l")
        ]
        
        self.cmd_buttons = []
        for i, (text, cmd) in enumerate(commands):
            row = i // 3
            col = i % 3
            btn = ttk.Button(btn_frame, text=text, 
                      command=lambda c=cmd: self.run_adb_command(c))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            self.cmd_buttons.append(btn)
            btn_frame.grid_columnconfigure(col, weight=1)

    def setup_perf_tab(self, parent):
        # Performance optimization section
        perf_frame = ttk.LabelFrame(parent, text="Performance Optimization")
        perf_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Animation scaling
        anim_frame = ttk.Frame(perf_frame)
        anim_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(anim_frame, text="Animation Scaling:").pack(side=tk.LEFT, padx=5)
        self.anim_scale = tk.DoubleVar(value=1.0)
        self.anim_slider = ttk.Scale(anim_frame, from_=0, to=1, variable=self.anim_scale, 
                 orient=tk.HORIZONTAL, length=200)
        self.anim_slider.pack(side=tk.LEFT, padx=5)
        self.anim_label = ttk.Label(anim_frame, textvariable=self.anim_scale)
        self.anim_label.pack(side=tk.LEFT, padx=5)
        
        self.apply_anim_btn = ttk.Button(anim_frame, text="Apply", command=self.apply_anim_scale)
        self.apply_anim_btn.pack(side=tk.LEFT, padx=5)
        
        self.disable_anim_btn = ttk.Button(anim_frame, text="Disable Animations", command=self.disable_animations)
        self.disable_anim_btn.pack(side=tk.LEFT, padx=5)
        
        # FPS boost
        fps_frame = ttk.Frame(perf_frame)
        fps_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(fps_frame, text="FPS Boost:").pack(side=tk.LEFT, padx=5)
        self.fps_mode = tk.StringVar()
        self.fps_combo = ttk.Combobox(fps_frame, textvariable=self.fps_mode, width=15)
        self.fps_combo['values'] = ('Normal', '90Hz Mode', '120Hz Mode', 'Ultra Smooth')
        self.fps_combo.current(0)
        self.fps_combo.pack(side=tk.LEFT, padx=5)
        
        self.apply_fps_btn = ttk.Button(fps_frame, text="Apply", command=self.apply_fps_mode)
        self.apply_fps_btn.pack(side=tk.LEFT, padx=5)
        
        # GPU rendering
        gpu_frame = ttk.Frame(perf_frame)
        gpu_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.gpu_rendering = tk.BooleanVar()
        self.gpu_check = ttk.Checkbutton(gpu_frame, text="Force GPU Rendering", variable=self.gpu_rendering,
                       command=self.toggle_gpu_rendering)
        self.gpu_check.pack(side=tk.LEFT, padx=5)
        
        # Performance monitoring
        monitor_frame = ttk.LabelFrame(parent, text="Performance Monitor")
        monitor_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # CPU/RAM stats
        stats_frame = ttk.Frame(monitor_frame)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.cpu_usage = tk.StringVar(value="CPU: 0%")
        self.ram_usage = tk.StringVar(value="RAM: 0%")
        self.fps_value = tk.StringVar(value="FPS: N/A")
        self.net_speed = tk.StringVar(value="Net: 0 KB/s")
        
        self.cpu_label = ttk.Label(stats_frame, textvariable=self.cpu_usage, width=15, font=("Segoe UI", 10, "bold"))
        self.cpu_label.pack(side=tk.LEFT, padx=10)
        
        self.ram_label = ttk.Label(stats_frame, textvariable=self.ram_usage, width=15, font=("Segoe UI", 10, "bold"))
        self.ram_label.pack(side=tk.LEFT, padx=10)
        
        self.fps_label = ttk.Label(stats_frame, textvariable=self.fps_value, width=15, font=("Segoe UI", 10, "bold"))
        self.fps_label.pack(side=tk.LEFT, padx=10)
        
        self.net_label = ttk.Label(stats_frame, textvariable=self.net_speed, width=15, font=("Segoe UI", 10, "bold"))
        self.net_label.pack(side=tk.LEFT, padx=10)
        
        # Performance graph
        self.canvas = tk.Canvas(monitor_frame, height=150, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Graph data
        self.cpu_data = [0] * 60
        self.ram_data = [0] * 60
        self.fps_data = [0] * 60
        
        # Draw initial graph
        self.root.after(100, self.draw_performance_graph)
        
        # Start/stop monitoring
        self.monitor_btn = ttk.Button(monitor_frame, text="Stop Monitoring", command=self.toggle_monitoring)
        self.monitor_btn.pack(side=tk.RIGHT, padx=10, pady=10)

    def setup_root_tab(self, parent):
        """Create tab for root-specific features"""
        # Root Commands Frame
        commands_frame = ttk.LabelFrame(parent, text="Root Commands")
        commands_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # SetEdit Permission
        setedit_frame = ttk.Frame(commands_frame)
        setedit_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(setedit_frame, text="SetEdit Permission:").pack(side=tk.LEFT, padx=5)
        self.grant_setedit_btn = ttk.Button(setedit_frame, text="Grant WRITE_SECURE_SETTINGS", 
                                          command=self.grant_setedit_permission)
        self.grant_setedit_btn.pack(side=tk.LEFT, padx=5)
        
        # Virtual RAM Expansion
        zram_frame = ttk.LabelFrame(parent, text="Virtual RAM Expansion (zRAM)")
        zram_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # zRAM size control
        size_frame = ttk.Frame(zram_frame)
        size_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(size_frame, text="zRAM Size (MB):").pack(side=tk.LEFT, padx=5)
        self.zram_size = tk.IntVar(value=1024)
        self.zram_entry = ttk.Entry(size_frame, textvariable=self.zram_size, width=10)
        self.zram_entry.pack(side=tk.LEFT, padx=5)
        
        self.set_zram_btn = ttk.Button(size_frame, text="Set zRAM Size", command=self.set_zram_size)
        self.set_zram_btn.pack(side=tk.LEFT, padx=5)
        
        # zRAM swapiness control
        swap_frame = ttk.Frame(zram_frame)
        swap_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(swap_frame, text="Swappiness (0-100):").pack(side=tk.LEFT, padx=5)
        self.swappiness = tk.IntVar(value=60)
        self.swap_slider = ttk.Scale(swap_frame, from_=0, to=100, variable=self.swappiness, 
                                    orient=tk.HORIZONTAL, length=200)
        self.swap_slider.pack(side=tk.LEFT, padx=5)
        self.swap_label = ttk.Label(swap_frame, textvariable=self.swappiness)
        self.swap_label.pack(side=tk.LEFT, padx=5)
        
        self.set_swap_btn = ttk.Button(swap_frame, text="Set Swappiness", command=self.set_swappiness)
        self.set_swap_btn.pack(side=tk.LEFT, padx=5)
        
        # Advanced Root Features
        advanced_frame = ttk.LabelFrame(parent, text="Advanced Root Features")
        advanced_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Kernel tweaks
        kernel_frame = ttk.Frame(advanced_frame)
        kernel_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.kernel_tweaks = tk.BooleanVar()
        ttk.Checkbutton(kernel_frame, text="Apply Kernel Tweaks", variable=self.kernel_tweaks,
                       command=self.toggle_kernel_tweaks).pack(side=tk.LEFT, padx=5)
        
        # CPU governor
        gov_frame = ttk.Frame(advanced_frame)
        gov_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(gov_frame, text="CPU Governor:").pack(side=tk.LEFT, padx=5)
        self.cpu_governor = tk.StringVar()
        gov_combo = ttk.Combobox(gov_frame, textvariable=self.cpu_governor, width=15)
        gov_combo['values'] = ('performance', 'ondemand', 'powersave', 'schedutil', 'interactive')
        gov_combo.current(0)
        gov_combo.pack(side=tk.LEFT, padx=5)
        
        self.set_gov_btn = ttk.Button(gov_frame, text="Set Governor", command=self.set_cpu_governor)
        self.set_gov_btn.pack(side=tk.LEFT, padx=5)
        
        # Thermal Throttling
        thermal_frame = ttk.Frame(advanced_frame)
        thermal_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(thermal_frame, text="Thermal Control:").pack(side=tk.LEFT, padx=5)
        self.thermal_profile = tk.StringVar()
        thermal_combo = ttk.Combobox(thermal_frame, textvariable=self.thermal_profile, width=15)
        thermal_combo['values'] = ('Default', 'Aggressive', 'Balanced', 'Conservative')
        thermal_combo.current(0)
        thermal_combo.pack(side=tk.LEFT, padx=5)
        
        self.set_thermal_btn = ttk.Button(thermal_frame, text="Apply Profile", command=self.set_thermal_profile)
        self.set_thermal_btn.pack(side=tk.LEFT, padx=5)

    def change_theme(self, theme_name):
        """Change application theme"""
        if self.theme_manager.set_theme(theme_name):
            self.apply_theme()
            self.log(f"Switched to {theme_name} theme")

    def apply_theme(self):
        """Apply current theme to all UI elements"""
        theme = self.theme_manager.get_theme()
        
        # Configure ttk styles
        style = ttk.Style()
        
        # Configure main styles
        style.configure(".", 
                        background=theme["bg"],
                        foreground=theme["fg"],
                        fieldbackground=theme["entry_bg"],
                        troughcolor=theme["bg"])
        
        # Configure modern styles
        style.configure("TFrame", background=theme["bg"])
        style.configure("TLabel", background=theme["bg"], foreground=theme["fg"], font=("Segoe UI", 10))
        style.configure("TButton", 
                        background=theme["button_bg"],
                        foreground=theme["button_fg"],
                        font=("Segoe UI", 10, "bold"),
                        padding=6,
                        relief="flat",
                        focuscolor="none")
        style.map("TButton",
                 background=[("active", theme["button_active"]), ("pressed", theme["button_active"])])
        
        style.configure("TEntry", 
                        fieldbackground=theme["entry_bg"],
                        foreground=theme["entry_fg"],
                        insertcolor=theme["fg"],
                        font=("Segoe UI", 10),
                        padding=5,
                        relief="flat",
                        focuscolor=theme["accent"])
        
        style.configure("TCombobox", 
                        fieldbackground=theme["entry_bg"],
                        foreground=theme["entry_fg"],
                        font=("Segoe UI", 10),
                        padding=5,
                        relief="flat",
                        focuscolor=theme["accent"])
        
        style.configure("TNotebook", 
                        background=theme["bg"],
                        tabmargins=[0, 5, 0, 0])
        style.configure("TNotebook.Tab", 
                        background=theme["tab_bg"],
                        foreground=theme["tab_fg"],
                        padding=[12, 8],
                        font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", 
                 background=[("selected", theme["tab_active"])])
        
        style.configure("TLabelframe", 
                        background=theme["bg"],
                        foreground=theme["fg"],
                        labeloutside=True,
                        labelmargins=5,
                        borderwidth=1,
                        relief="solid")
        style.configure("TLabelframe.Label", 
                        background=theme["bg"],
                        foreground=theme["fg"],
                        font=("Segoe UI", 11, "bold"))
        
        style.configure("Treeview", 
                        background=theme["tree_bg"],
                        foreground=theme["tree_fg"],
                        fieldbackground=theme["tree_bg"],
                        font=("Segoe UI", 10),
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        background=theme["heading_bg"],
                        foreground=theme["heading_fg"],
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", 
                 background=[('selected', theme["tree_sel"])])
        
        # FIX: Configure scrollbar styles properly
        style.configure("TScrollbar", 
                        background=theme["button_bg"],
                        troughcolor=theme["bg"],
                        borderwidth=0,
                        width=10,
                        arrowsize=12)
        
        # Configure vertical scrollbar layout
        style.layout("Vertical.TScrollbar", [
            ('Vertical.Scrollbar.trough', {'sticky': 'ns'}),
            ('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'ns'}),
            ('Vertical.Scrollbar.uparrow', {'sticky': 'n'}),
            ('Vertical.Scrollbar.downarrow', {'sticky': 's'})
        ])
        
        # Configure horizontal scrollbar layout
        style.layout("Horizontal.TScrollbar", [
            ('Horizontal.Scrollbar.trough', {'sticky': 'ew'}),
            ('Horizontal.Scrollbar.thumb', {'expand': '1', 'sticky': 'ew'}),
            ('Horizontal.Scrollbar.leftarrow', {'sticky': 'w'}),
            ('Horizontal.Scrollbar.rightarrow', {'sticky': 'e'})
        ])
        
        style.configure("TScale", 
                        background=theme["bg"],
                        troughcolor=theme["entry_bg"],
                        borderwidth=0,
                        focuscolor=theme["accent"])
        
        style.configure("TCheckbutton", 
                        background=theme["bg"],
                        foreground=theme["fg"],
                        font=("Segoe UI", 10))
        
        # Configure card style
        style.configure("Card.TFrame", 
                       background=theme["card_bg"],
                       relief="solid",
                       borderwidth=1)
        
        # Apply to non-ttk widgets
        self.root.configure(bg=theme["bg"])
        self.log_area.configure(
            bg=theme["log_bg"], 
            fg=theme["log_fg"],
            insertbackground=theme["log_fg"],
            font=("Consolas", 9),
            relief="flat",
            borderwidth=1,
            highlightbackground=theme["card_border"]
        )
        self.canvas.configure(bg=theme["canvas_bg"])
        self.shortcuts_canvas.configure(bg=theme["bg"])
        
        # Apply to all children widgets recursively
        self.apply_theme_recursive(self.root, theme)
        
        # Status label color
        self.update_status_color()

    def apply_theme_recursive(self, widget, theme):
        """Recursively apply theme to all widgets"""
        try:
            # Skip themed ttk widgets
            if isinstance(widget, (ttk.Label, ttk.Button, ttk.Entry, ttk.Combobox, 
                                 ttk.Scrollbar, ttk.Scale, ttk.Checkbutton, 
                                 ttk.Frame, ttk.LabelFrame, ttk.Notebook)):
                return
            
            # Configure widget based on type
            if isinstance(widget, (tk.Label, tk.Button)):
                widget.configure(
                    bg=theme["bg"] if not isinstance(widget, tk.Button) else theme["button_bg"],
                    fg=theme["fg"] if not isinstance(widget, tk.Button) else theme["button_fg"],
                    font=("Segoe UI", 10)
                )
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=theme["entry_bg"],
                    fg=theme["entry_fg"],
                    insertbackground=theme["fg"],
                    font=("Segoe UI", 10),
                    relief="flat",
                    borderwidth=1
                )
            elif isinstance(widget, tk.Text):
                widget.configure(
                    bg=theme["text_bg"],
                    fg=theme["text_fg"],
                    insertbackground=theme["fg"],
                    font=("Consolas", 9),
                    relief="flat",
                    borderwidth=1
                )
            elif isinstance(widget, tk.Canvas):
                widget.configure(bg=theme["canvas_bg"])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])
        except Exception as e:
            pass
        
        # Apply to children
        for child in widget.winfo_children():
            self.apply_theme_recursive(child, theme)

    def run_adb_command(self, command, wait=True, root=False):
        """Execute ADB command and return output"""
        try:
            self.log(f"Executing: adb {command} {'(as root)' if root else ''}")
            
            # Handle paths without extra quotes
            if isinstance(command, list):
                cmd_list = [ADB_PATH] + command
            else:
                cmd_list = [ADB_PATH] + command.split()
                
            # Add root prefix if needed
            if root:
                cmd_list = [ADB_PATH, "shell", "su", "-c"] + [" ".join(cmd_list[1:])]
                
            result = subprocess.run(cmd_list, 
                                   capture_output=True, 
                                   text=True,
                                   timeout=30)
            output = result.stdout or result.stderr
            self.log(f"Result:\n{output}")
            return output
        except FileNotFoundError:
            error = f"ADB not found at {ADB_PATH}. Please check the path."
            self.log(error)
            return error
        except Exception as e:
            error = f"Error: {str(e)}"
            self.log(error)
            return error

    def run_threaded(self, func):
        """Run function in a separate thread"""
        threading.Thread(target=func, daemon=True).start()

    def log(self, message):
        """Add message to log area with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.config(state=tk.DISABLED)
        self.log_area.see(tk.END)
        
    def clear_log(self):
        """Clear the log area"""
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)
        self.log("Log cleared")

    def update_status_color(self):
        """Update status label color based on connection"""
        theme = self.theme_manager.get_theme()
        if "Connected" in self.connection_status.get():
            self.status_label.configure(foreground="#4ade80")
        else:
            self.status_label.configure(foreground=theme["accent"])

    def check_connection(self):
        """Check if device is connected in background"""
        self.run_threaded(self._check_connection)

    def _check_connection(self):
        """Threaded device connection check"""
        try:
            output = self.run_adb_command("devices", wait=True)
            if "device" in output and not "unauthorized" in output:
                self.connection_status.set("Connected")
            else:
                self.connection_status.set("Disconnected (Check USB Debugging)")
            self.update_status_color()
            
            # Check root status
            self.check_root_status()
        except Exception as e:
            self.log(f"Connection check failed: {str(e)}")
            self.connection_status.set("Connection Error")
            self.update_status_color()

    def check_root_status(self):
        """Check if device is rooted"""
        try:
            output = self.run_adb_command("shell su -c id", wait=True)
            if "uid=0" in output:
                self.root_status.set("Root: Granted")
                self.root_label.configure(foreground="#4ade80")
            else:
                self.root_status.set("Root: Not Available")
                self.root_label.configure(foreground="#f87171")
        except Exception as e:
            self.root_status.set("Root: Check Failed")
            self.root_label.configure(foreground="#fbbf24")
            self.log(f"Root check failed: {str(e)}")

    def refresh_apps_list(self):
        """Load all installed apps from device in background"""
        self.run_threaded(self._refresh_apps_list)

    def _refresh_apps_list(self):
        """Threaded app list refresh"""
        try:
            # Clear placeholder
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Try multiple commands to get app list
            commands = [
                "shell pm list packages -s -3 -u -i",  # Preferred command
                "shell pm list packages -s -3",        # Fallback 1
                "shell pm list packages -3"            # Fallback 2
            ]
            
            output = ""
            for cmd in commands:
                output = self.run_adb_command(cmd, wait=True)
                if output and "package:" in output and "Error" not in output:
                    break
            
            if not output or "Error" in output:
                self.log("Failed to load apps: " + output)
                self.tree.insert("", tk.END, values=("Failed to load apps", "", "Error"))
                return
                
            packages = [line.split(':')[1].strip() for line in output.splitlines() if line.startswith('package:')]
            
            if not packages:
                self.log("No apps found in device")
                self.tree.insert("", tk.END, values=("No apps found", "", ""))
                return
                
            for package in packages:
                # Get app name
                app_name = "Fetching..."
                status = "Enabled"
                
                # Check if disabled
                status_output = self.run_adb_command(f"shell pm list packages -d {package}")
                if status_output and "package:" + package in status_output:
                    status = "Disabled"
                
                # Insert with placeholder
                self.tree.insert("", tk.END, values=(app_name, package, status))
                
                # Update app name in background
                threading.Thread(target=self.update_app_name, args=(package,), daemon=True).start()
                
            self.log(f"Loaded {len(packages)} apps")
        except Exception as e:
            self.log(f"Error loading apps: {str(e)}")
            self.tree.insert("", tk.END, values=("Error loading apps", "", ""))

    def update_app_name(self, package):
        """Get application name for package"""
        try:
            output = self.run_adb_command(f"shell dumpsys package {package}")
            if not output:
                return
                
            # Find app name using multiple patterns
            app_name = package
            patterns = [
                r'application: label=([\'"])(.*?)\1',
                r'package:.*?labelRes=.*?label=([\'"])(.*?)\1',
                r'Package \[.*?\] \(.*?\):.*?name=.*? label=([\'"])(.*?)\1'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, output)
                if match:
                    app_name = match.group(2)
                    break
            
            # Update treeview
            for item in self.tree.get_children():
                if self.tree.item(item, 'values')[1] == package:
                    values = list(self.tree.item(item, 'values'))
                    values[0] = app_name
                    self.tree.item(item, values=values)
                    break
        except Exception as e:
            self.log(f"Error updating app name for {package}: {str(e)}")

    def get_selected_package(self):
        """Get package from selected item"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an app first")
            return None
        return self.tree.item(selection[0], 'values')[1]

    def install_app(self):
        """Install APK from file"""
        apk_path = filedialog.askopenfilename(filetypes=[("APK Files", "*.apk")])
        if not apk_path:
            return
            
        # Use list command to avoid quoting issues
        self.run_threaded(lambda: self.run_adb_command(["install", apk_path]))

    def install_xapk(self):
        """Install XAPK package"""
        xapk_path = filedialog.askopenfilename(filetypes=[("XAPK Files", "*.xapk")])
        if not xapk_path:
            return
            
        self.run_threaded(lambda: self._install_xapk_thread(xapk_path))
        
    def _install_xapk_thread(self, xapk_path):
        """Threaded XAPK installation"""
        try:
            self.log(f"Processing XAPK: {xapk_path}")
            
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix="xapk_")
            self.log(f"Created temporary directory: {temp_dir}")
            
            # Extract XAPK
            with zipfile.ZipFile(xapk_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                self.log(f"Extracted XAPK to: {temp_dir}")
            
            # Find APK files
            apk_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith(".apk"):
                        apk_files.append(os.path.join(root, file))
            
            if not apk_files:
                self.log("Error: No APK files found in XAPK package")
                return
                
            # Sort by size to install main APK first
            apk_files.sort(key=lambda x: os.path.getsize(x), reverse=True)
            self.log(f"Found APK files: {', '.join(apk_files)}")
            
            # Install using install-multiple
            cmd = ["install-multiple"] + apk_files
            result = self.run_adb_command(cmd)
            
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            self.log("Cleaned up temporary files")
            
            # Show result
            if "Success" in result:
                self.log("XAPK installation successful!")
            else:
                self.log(f"XAPK installation failed: {result}")
                
            # Refresh app list
            self.refresh_apps_list()
            
        except Exception as e:
            self.log(f"Error installing XAPK: {str(e)}")

    def uninstall_app(self):
        """Uninstall selected app"""
        package = self.get_selected_package()
        if package:
            self.run_threaded(lambda: self.run_adb_command(["uninstall", "--user", "0", package]))

    def disable_app(self):
        """Disable selected app"""
        package = self.get_selected_package()
        if package:
            self.run_threaded(lambda: self.run_adb_command(["shell", "pm", "disable-user", "--user", "0", package]))
            self.refresh_apps_list()

    def enable_app(self):
        """Enable selected app"""
        package = self.get_selected_package()
        if package:
            self.run_threaded(lambda: self.run_adb_command(["shell", "pm", "enable", package]))
            self.refresh_apps_list()

    def clear_app_cache(self):
        """Clear app cache"""
        package = self.get_selected_package()
        if package:
            self.run_threaded(lambda: self.run_adb_command(["shell", "pm", "clear", package]))

    def browse_dest(self):
        """Browse for destination directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.pull_dest.delete(0, tk.END)
            self.pull_dest.insert(0, directory)

    def browse_src(self):
        """Browse for source file"""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.push_src.delete(0, tk.END)
            self.push_src.insert(0, file_path)

    def pull_file(self):
        """Pull file from device"""
        src = self.pull_src.get().strip()
        dest = self.pull_dest.get().strip() or os.path.expanduser("~\\Downloads")
        
        # Create destination directory if it doesn't exist
        dest_dir = os.path.dirname(dest) if '.' in os.path.basename(dest) else dest
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
            self.log(f"Created directory: {dest_dir}")
            
        self.log(f"Pulling {src} to {dest}")
        self.run_threaded(lambda: self.run_adb_command(["pull", src, dest]))

    def push_file(self):
        """Push file to device"""
        src = self.push_src.get().strip()
        dest = self.push_dest.get().strip()
        
        if not os.path.exists(src):
            self.log(f"Error: Source file does not exist: {src}")
            return
            
        self.log(f"Pushing {src} to {dest}")
        self.run_threaded(lambda: self.run_adb_command(["push", src, dest]))

    # Performance tab functions
    def apply_anim_scale(self):
        """Apply animation scale settings"""
        scale = self.anim_scale.get()
        self.run_adb_command(["shell", "settings", "put", "global", "window_animation_scale", str(scale)])
        self.run_adb_command(["shell", "settings", "put", "global", "transition_animation_scale", str(scale)])
        self.run_adb_command(["shell", "settings", "put", "global", "animator_duration_scale", str(scale)])
        self.log(f"Animation scales set to {scale}x")

    def disable_animations(self):
        """Disable all animations"""
        self.anim_scale.set(0)
        self.apply_anim_scale()

    def apply_fps_mode(self):
        """Apply selected FPS mode"""
        mode = self.fps_mode.get()
        if mode == "Normal":
            self.log("FPS mode set to Normal")
        elif mode == "90Hz Mode":
            self.run_adb_command(["shell", "settings", "put", "system", "peak_refresh_rate", "90"])
            self.log("FPS mode set to 90Hz")
        elif mode == "120Hz Mode":
            self.run_adb_command(["shell", "settings", "put", "system", "peak_refresh_rate", "120"])
            self.log("FPS mode set to 120Hz")
        elif mode == "Ultra Smooth":
            self.run_adb_command(["shell", "settings", "put", "system", "min_refresh_rate", "120"])
            self.run_adb_command(["shell", "settings", "put", "system", "peak_refresh_rate", "120"])
            self.log("Ultra Smooth mode enabled (120Hz locked)")

    def toggle_gpu_rendering(self):
        """Toggle GPU rendering"""
        if self.gpu_rendering.get():
            self.run_adb_command(["shell", "settings", "put", "global", "debug.hwui.renderer", "skiagl"])
            self.log("Forced GPU rendering enabled")
        else:
            self.run_adb_command(["shell", "settings", "put", "global", "debug.hwui.renderer", "opengl"])
            self.log("GPU rendering set to default")

    def toggle_monitoring(self):
        """Toggle performance monitoring"""
        self.monitoring = not self.monitoring
        if self.monitoring:
            self.log("Performance monitoring started")
            self.monitor_btn.configure(text="Stop Monitoring")
        else:
            self.log("Performance monitoring stopped")
            self.monitor_btn.configure(text="Start Monitoring")

    def monitor_performance(self):
        """Monitor device performance"""
        if not self.monitoring:
            self.root.after(1000, self.monitor_performance)
            return
            
        try:
            # Simulate performance data since we don't have real device metrics
            cpu = 20 + (time.time() * 10) % 40
            ram = 40 + (time.time() * 5) % 30
            fps = 60 + int(time.time() * 10) % 60
            net = 100 + int(time.time() * 20) % 900
            
            # Update display
            self.cpu_usage.set(f"CPU: {int(cpu)}%")
            self.ram_usage.set(f"RAM: {int(ram)}%")
            self.fps_value.set(f"FPS: {fps}")
            self.net_speed.set(f"Net: {net} KB/s")
            
            # Update data arrays
            self.cpu_data.pop(0)
            self.cpu_data.append(cpu)
            self.ram_data.pop(0)
            self.ram_data.append(ram)
            self.fps_data.pop(0)
            self.fps_data.append(fps)
            
            # Update graph
            self.draw_performance_graph()
            
        except Exception as e:
            self.log(f"Monitoring error: {str(e)}")
            
        # Schedule next update
        self.root.after(1000, self.monitor_performance)

    def draw_performance_graph(self):
        """Draw performance graph on canvas"""
        try:
            theme = self.theme_manager.get_theme()
            self.canvas.delete("all")
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            
            if width < 10 or height < 10:
                return
                
            # Draw grid
            grid_color = theme["fg"]
            for i in range(1, 5):
                y = height - (i * height / 5)
                self.canvas.create_line(0, y, width, y, fill=grid_color, dash=(2, 2))
            
            # Draw CPU line
            self.draw_data_line(self.cpu_data, "#ef4444", width, height)
            
            # Draw RAM line
            self.draw_data_line(self.ram_data, "#3b82f6", width, height)
            
            # Draw FPS line (scaled to 0-100 range)
            scaled_fps = [val / 1.2 for val in self.fps_data]  # Scale 0-120 to 0-100
            self.draw_data_line(scaled_fps, "#10b981", width, height)
            
            # Draw legend
            self.canvas.create_text(10, 10, anchor="nw", text="CPU", fill="#ef4444", font=("Segoe UI", 9, "bold"))
            self.canvas.create_text(50, 10, anchor="nw", text="RAM", fill="#3b82f6", font=("Segoe UI", 9, "bold"))
            self.canvas.create_text(90, 10, anchor="nw", text="FPS", fill="#10b981", font=("Segoe UI", 9, "bold"))
        except:
            pass

    def draw_data_line(self, data, color, width, height):
        """Draw a single data line on the graph"""
        try:
            points = []
            for i, value in enumerate(data):
                x = i * (width / len(data))
                y = height - (value * height / 100)  # Scale to 0-100 range
                points.extend([x, y])
            
            if len(points) > 2:
                self.canvas.create_line(points, fill=color, smooth=True, width=2)
        except:
            pass
            
    # Root tools functions
    def grant_setedit_permission(self):
        """Grant WRITE_SECURE_SETTINGS permission to SetEdit app"""
        self.run_threaded(lambda: self.run_adb_command(
            ["shell", "pm", "grant", "io.github.muntashirakon.setedit", "android.permission.WRITE_SECURE_SETTINGS"]
        ))
        self.log("Granted WRITE_SECURE_SETTINGS to SetEdit app")

    def set_zram_size(self):
        """Set zRAM size for virtual memory expansion"""
        size = self.zram_size.get()
        self.run_threaded(lambda: self.run_adb_command(
            ["shell", "su", "-c", f"echo {size}M > /sys/block/zram0/disksize && mkswap /dev/block/zram0 && swapon /dev/block/zram0"],
            root=True
        ))
        self.log(f"Set zRAM size to {size}MB")

    def set_swappiness(self):
        """Set swappiness value for virtual memory"""
        value = self.swappiness.get()
        self.run_threaded(lambda: self.run_adb_command(
            ["shell", "su", "-c", f"echo {value} > /proc/sys/vm/swappiness"],
            root=True
        ))
        self.log(f"Set swappiness to {value}")

    def toggle_kernel_tweaks(self):
        """Toggle kernel performance tweaks"""
        if self.kernel_tweaks.get():
            tweaks = [
                "echo 1 > /proc/sys/vm/oom_kill_allocating_task",
                "echo 0 > /proc/sys/vm/page-cluster",
                "echo 10 > /proc/sys/vm/dirty_ratio",
                "echo 5 > /proc/sys/vm/dirty_background_ratio",
                "echo 500 > /proc/sys/vm/dirty_expire_centisecs",
                "echo 100 > /proc/sys/vm/dirty_writeback_centisecs"
            ]
            for tweak in tweaks:
                self.run_adb_command(["shell", "su", "-c", tweak], root=True)
            self.log("Applied kernel tweaks for performance")
        else:
            self.log("Kernel tweaks disabled")

    def set_cpu_governor(self):
        """Set CPU governor for performance"""
        governor = self.cpu_governor.get()
        self.run_threaded(lambda: self.run_adb_command(
            ["shell", "su", "-c", f"echo {governor} > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"],
            root=True
        ))
        self.log(f"Set CPU governor to {governor}")

    def set_thermal_profile(self):
        """Apply thermal throttling profile"""
        profile = self.thermal_profile.get().lower()
        self.run_threaded(lambda: self.run_adb_command(
            ["shell", "su", "-c", f"echo {profile} > /sys/class/thermal/thermal_message/sconfig"],
            root=True
        ))
        self.log(f"Applied thermal profile: {profile}")
            
    def show_about(self):
        """Show about dialog"""
        about_text = (
            "ADB Manager Pro\n"
            "Version 5.0\n\n"
            "A comprehensive Android device management tool\n"
            "with ADB functionality and performance tuning\n\n"
            "Features:\n"
            "- App management (install/uninstall/disable)\n"
            "- XAPK package support\n"
            "- File transfer\n"
            "- Device commands\n"
            "- Performance tuning\n"
            "- Root tools (zRAM, kernel tweaks)\n"
            "- Quick install shortcuts\n"
            "- Modern dark theme UI\n\n"
            "© 2023 ADB Manager Pro"
        )
        messagebox.showinfo("About ADB Manager Pro", about_text)

if __name__ == "__main__":
    # Create root window with error handling
    root = tk.Tk()
    
    # Set default download location
    default_download = os.path.expanduser("~\\Downloads")
    if not os.path.exists(default_download):
        default_download = os.getcwd()
    
    try:
        app = ADBManager(root)
        root.mainloop()
    except Exception as e:
        # Show error message if initialization fails
        error_msg = f"Failed to start application:\n{str(e)}"
        print(error_msg)
        tk.messagebox.showerror("Fatal Error", error_msg)
        sys.exit(1)