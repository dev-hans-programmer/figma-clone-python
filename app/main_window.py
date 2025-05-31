"""
Main application window and controller
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import threading
import time

from ui.toolbar import Toolbar
from ui.component_palette import ComponentPalette
from ui.properties_panel import PropertiesPanel
from canvas.design_canvas import DesignCanvas
from canvas.canvas_manager import CanvasManager
from utils.file_manager import FileManager
from utils.export_manager import ExportManager
from config.settings import AppSettings
from config.themes import AppThemes

class MainWindow:
    """Main application window class"""
    
    def __init__(self):
        """Initialize the main window"""
        # Set appearance mode and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Mini Figma - UI Wireframe Designer")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Initialize managers
        self.file_manager = FileManager()
        self.export_manager = ExportManager()
        self.canvas_manager = CanvasManager()
        self.app_settings = AppSettings()
        
        # Current file path
        self.current_file = None
        self.is_modified = False
        
        # Auto-save functionality
        self.auto_save_enabled = self.app_settings.get("editor.auto_save", True)
        auto_save_interval_setting = self.app_settings.get("editor.auto_save_interval", 300)
        self.auto_save_interval = auto_save_interval_setting if isinstance(auto_save_interval_setting, (int, float)) else 300
        self.auto_save_thread = None
        self.auto_save_running = False
        self.last_auto_save_time = time.time()
        
        # Auto-save file path
        self.auto_save_dir = os.path.join(self.app_settings.settings_dir, "autosave")
        os.makedirs(self.auto_save_dir, exist_ok=True)
        self.auto_save_file = os.path.join(self.auto_save_dir, "autosave.json")
        
        # Setup the UI
        self.setup_ui()
        self.setup_bindings()
        
        # Check for auto-save recovery
        self.check_auto_save_recovery()
        
        # Start auto-save if enabled
        if self.auto_save_enabled:
            self.start_auto_save()
        
        # Update window title
        self.update_title()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create toolbar
        self.toolbar = Toolbar(self.root, self)
        self.toolbar.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # Create component palette (left panel)
        self.component_palette = ComponentPalette(self.root, self)
        self.component_palette.grid(row=1, column=0, sticky="nsew", padx=(5, 2), pady=5)
        
        # Create main canvas area
        self.canvas_frame = ctk.CTkFrame(self.root)
        self.canvas_frame.grid(row=1, column=1, sticky="nsew", padx=2, pady=5)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Create design canvas
        self.design_canvas = DesignCanvas(self.canvas_frame, self)
        self.design_canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Set canvas manager reference
        self.canvas_manager.set_canvas(self.design_canvas)
        
        # Create properties panel (right panel)
        self.properties_panel = PropertiesPanel(self.root, self)
        self.properties_panel.grid(row=1, column=2, sticky="nsew", padx=(2, 5), pady=5)
        
        # Configure column weights
        self.root.grid_columnconfigure(0, weight=0, minsize=200)  # Component palette
        self.root.grid_columnconfigure(1, weight=1, minsize=600)  # Canvas
        self.root.grid_columnconfigure(2, weight=0, minsize=250)  # Properties panel
    
    def setup_bindings(self):
        """Setup keyboard bindings and events"""
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-S>', lambda e: self.save_as_file())
        self.root.bind('<Control-e>', lambda e: self.export_design())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Delete>', lambda e: self.delete_selected())
        
        # Window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def new_file(self):
        """Create a new design file"""
        if self.is_modified:
            if not self.confirm_discard_changes():
                return
        
        self.canvas_manager.clear_canvas()
        self.current_file = None
        self.is_modified = False
        self.update_title()
        self.properties_panel.clear_selection()
    
    def open_file(self):
        """Open an existing design file"""
        if self.is_modified:
            if not self.confirm_discard_changes():
                return
        
        file_path = filedialog.askopenfilename(
            title="Open Design File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                design_data = self.file_manager.load_design(file_path)
                self.canvas_manager.load_design(design_data)
                self.current_file = file_path
                self.is_modified = False
                self.update_title()
                self.properties_panel.clear_selection()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")
    
    def save_file(self):
        """Save the current design"""
        if self.current_file:
            try:
                design_data = self.canvas_manager.get_design_data()
                self.file_manager.save_design(design_data, self.current_file)
                self.is_modified = False
                self.update_title()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """Save the current design with a new name"""
        file_path = filedialog.asksaveasfilename(
            title="Save Design As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                design_data = self.canvas_manager.get_design_data()
                self.file_manager.save_design(design_data, file_path)
                self.current_file = file_path
                self.is_modified = False
                self.update_title()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def export_design(self):
        """Export the design as PNG or SVG"""
        file_path = filedialog.asksaveasfilename(
            title="Export Design",
            filetypes=[("PNG files", "*.png"), ("SVG files", "*.svg")]
        )
        
        if file_path:
            try:
                if file_path.lower().endswith('.png'):
                    self.export_manager.export_png(self.design_canvas, file_path)
                elif file_path.lower().endswith('.svg'):
                    design_data = self.canvas_manager.get_design_data()
                    self.export_manager.export_svg(design_data, file_path)
                
                messagebox.showinfo("Success", "Design exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export design: {e}")
    
    def undo(self):
        """Undo the last action"""
        self.canvas_manager.undo()
        self.mark_modified()
    
    def redo(self):
        """Redo the last undone action"""
        self.canvas_manager.redo()
        self.mark_modified()
    
    def delete_selected(self):
        """Delete the selected component"""
        if self.canvas_manager.selected_component:
            self.canvas_manager.delete_component(self.canvas_manager.selected_component)
            self.properties_panel.clear_selection()
            self.mark_modified()
    
    def add_component(self, component_type):
        """Add a new component to the canvas"""
        component = self.canvas_manager.add_component(component_type)
        if component:
            self.mark_modified()
            return component
        return None
    
    def select_component(self, component):
        """Select a component"""
        self.canvas_manager.select_component(component)
        self.properties_panel.update_selection(component)
    

    
    def confirm_discard_changes(self):
        """Ask user to confirm discarding unsaved changes"""
        result = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes. Do you want to save them?"
        )
        if result is True:  # Yes - save
            self.save_file()
            return not self.is_modified  # Return False if save failed
        elif result is False:  # No - discard
            return True
        else:  # Cancel
            return False
    
    def on_closing(self):
        """Handle window closing event"""
        if self.is_modified:
            if not self.confirm_discard_changes():
                return
        
        # Stop auto-save thread
        self.stop_auto_save()
        
        # Clean up auto-save file if no unsaved changes
        if not self.is_modified and os.path.exists(self.auto_save_file):
            try:
                os.remove(self.auto_save_file)
            except:
                pass  # Ignore cleanup errors
        
        self.root.destroy()
    
    def start_auto_save(self):
        """Start the auto-save thread"""
        if not self.auto_save_running:
            self.auto_save_running = True
            self.auto_save_thread = threading.Thread(target=self._auto_save_worker, daemon=True)
            self.auto_save_thread.start()
    
    def stop_auto_save(self):
        """Stop the auto-save thread"""
        self.auto_save_running = False
        if self.auto_save_thread and self.auto_save_thread.is_alive():
            self.auto_save_thread.join(timeout=1.0)
    
    def _auto_save_worker(self):
        """Auto-save worker thread"""
        while self.auto_save_running:
            try:
                time.sleep(10)  # Check every 10 seconds
                
                if not self.auto_save_running:
                    break
                
                current_time = time.time()
                time_since_last_save = current_time - self.last_auto_save_time
                
                # Only auto-save if there are modifications and enough time has passed
                if (self.is_modified and 
                    time_since_last_save >= float(self.auto_save_interval) and
                    self.canvas_manager.components):  # Only save if there are components
                    
                    self.root.after(0, self._perform_auto_save)
                    self.last_auto_save_time = current_time
                    
            except Exception as e:
                print(f"Auto-save error: {e}")
                continue
    
    def _perform_auto_save(self):
        """Perform the actual auto-save operation (runs on main thread)"""
        try:
            design_data = self.canvas_manager.get_design_data()
            
            # Add metadata for auto-save
            auto_save_data = {
                "metadata": {
                    "version": "1.0",
                    "auto_save": True,
                    "original_file": self.current_file,
                    "timestamp": time.time(),
                    "app_name": "Mini Figma - UI Wireframe Designer"
                },
                "design": design_data
            }
            
            # Save to auto-save file
            with open(self.auto_save_file, 'w', encoding='utf-8') as f:
                json.dump(auto_save_data, f, indent=2, ensure_ascii=False)
            
            # Update title to show auto-save status
            self.update_title()
            
        except Exception as e:
            print(f"Auto-save failed: {e}")
    
    def check_auto_save_recovery(self):
        """Check if there's an auto-save file to recover"""
        if os.path.exists(self.auto_save_file):
            try:
                with open(self.auto_save_file, 'r', encoding='utf-8') as f:
                    auto_save_data = json.load(f)
                
                metadata = auto_save_data.get("metadata", {})
                if metadata.get("auto_save"):
                    # Show recovery dialog
                    result = messagebox.askyesno(
                        "Auto-save Recovery",
                        "An auto-saved file was found. This might contain unsaved work from a previous session.\n\n"
                        "Would you like to recover it?",
                        icon="question"
                    )
                    
                    if result:
                        # Load the auto-saved design
                        design_data = auto_save_data.get("design", {})
                        self.canvas_manager.load_design(design_data)
                        
                        # Set as modified and update title
                        original_file = metadata.get("original_file")
                        if original_file and os.path.exists(original_file):
                            self.current_file = original_file
                        
                        self.is_modified = True
                        self.update_title()
                        
                        messagebox.showinfo(
                            "Recovery Complete",
                            "Your work has been recovered from the auto-save file."
                        )
                    else:
                        # User declined recovery, remove auto-save file
                        os.remove(self.auto_save_file)
                        
            except Exception as e:
                print(f"Auto-save recovery error: {e}")
                # If recovery fails, remove the corrupted auto-save file
                try:
                    os.remove(self.auto_save_file)
                except:
                    pass
    
    def toggle_auto_save(self):
        """Toggle auto-save functionality"""
        self.auto_save_enabled = not self.auto_save_enabled
        self.app_settings.set("editor.auto_save", self.auto_save_enabled)
        self.app_settings.save_settings()
        
        if self.auto_save_enabled:
            self.start_auto_save()
            messagebox.showinfo("Auto-save", "Auto-save has been enabled.")
        else:
            self.stop_auto_save()
            messagebox.showinfo("Auto-save", "Auto-save has been disabled.")
    
    def set_auto_save_interval(self, interval_minutes):
        """Set auto-save interval in minutes"""
        self.auto_save_interval = interval_minutes * 60  # Convert to seconds
        self.app_settings.set("editor.auto_save_interval", self.auto_save_interval)
        self.app_settings.save_settings()
    
    def mark_modified(self):
        """Mark the design as modified"""
        self.is_modified = True
        self.update_title()
        # Reset auto-save timer when content is modified
        self.last_auto_save_time = time.time()
    
    def update_title(self):
        """Update the window title"""
        title = "Mini Figma - UI Wireframe Designer"
        if self.current_file:
            filename = os.path.basename(self.current_file)
            title = f"{filename} - {title}"
        if self.is_modified:
            title = f"*{title}"
        
        # Add auto-save indicator if auto-save is enabled
        if self.auto_save_enabled and os.path.exists(self.auto_save_file):
            title += " [Auto-saved]"
            
        self.root.title(title)

    def run(self):
        """Start the application"""
        self.root.mainloop()
