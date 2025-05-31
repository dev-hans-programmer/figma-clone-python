"""
Application settings management
"""

import json
import os
from pathlib import Path

class AppSettings:
    """Manages application settings and preferences"""
    
    def __init__(self):
        """Initialize settings manager"""
        self.settings_dir = self._get_settings_directory()
        self.settings_file = os.path.join(self.settings_dir, "settings.json")
        
        # Default settings
        self.default_settings = {
            "appearance": {
                "theme": "dark",
                "color_scheme": "blue",
                "window_geometry": "1400x900",
                "window_state": "normal"
            },
            "canvas": {
                "grid_size": 20,
                "show_grid": True,
                "snap_to_grid": True,
                "canvas_width": 800,
                "canvas_height": 600,
                "background_color": "#f8fafc",
                "grid_color": "#e2e8f0"
            },
            "editor": {
                "auto_save": True,
                "auto_save_interval": 300,  # seconds
                "backup_count": 5,
                "default_component_colors": {
                    "rectangle": {"fill": "#e5e7eb", "border": "#6b7280"},
                    "button": {"fill": "#3b82f6", "border": "#1e40af", "text": "#ffffff"},
                    "input": {"fill": "#ffffff", "border": "#d1d5db", "text": "#374151"},
                    "text": {"fill": "", "border": "", "text": "#374151"}
                }
            },
            "export": {
                "default_format": "png",
                "png_quality": 95,
                "svg_precision": 2,
                "include_metadata": True,
                "default_export_path": ""
            },
            "recent_files": {
                "max_files": 10,
                "files": []
            },
            "ui": {
                "show_properties_panel": True,
                "show_component_palette": True,
                "properties_panel_width": 250,
                "component_palette_width": 200,
                "toolbar_visible": True
            },
            "shortcuts": {
                "new_file": "Ctrl+N",
                "open_file": "Ctrl+O",
                "save_file": "Ctrl+S",
                "save_as": "Ctrl+Shift+S",
                "export": "Ctrl+E",
                "undo": "Ctrl+Z",
                "redo": "Ctrl+Y",
                "delete": "Delete",
                "select_all": "Ctrl+A",
                "copy": "Ctrl+C",
                "paste": "Ctrl+V",
                "duplicate": "Ctrl+D"
            }
        }
        
        # Load settings
        self.settings = self.load_settings()
    
    def _get_settings_directory(self):
        """Get the settings directory path"""
        # Use user's home directory for settings
        if os.name == 'nt':  # Windows
            settings_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "MiniFigma")
        else:  # macOS and Linux
            settings_dir = os.path.join(os.path.expanduser("~"), ".config", "minifigma")
        
        # Create directory if it doesn't exist
        Path(settings_dir).mkdir(parents=True, exist_ok=True)
        return settings_dir
    
    def load_settings(self):
        """Load settings from file"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                
                # Merge with defaults (in case new settings were added)
                return self._merge_settings(self.default_settings, loaded_settings)
            
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.default_settings.copy()
        
        return self.default_settings.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def _merge_settings(self, default, loaded):
        """Recursively merge loaded settings with defaults"""
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_settings(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, key_path, default=None):
        """Get setting value using dot notation (e.g., 'canvas.grid_size')"""
        keys = key_path.split('.')
        value = self.settings
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path, value):
        """Set setting value using dot notation"""
        keys = key_path.split('.')
        setting = self.settings
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in setting:
                setting[key] = {}
            setting = setting[key]
        
        # Set the value
        setting[keys[-1]] = value
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.default_settings.copy()
        return self.save_settings()
    
    def reset_section(self, section):
        """Reset a specific section to defaults"""
        if section in self.default_settings:
            self.settings[section] = self.default_settings[section].copy()
            return self.save_settings()
        return False
    
    # Convenience methods for common settings
    def get_theme(self):
        """Get current theme"""
        return self.get("appearance.theme", "dark")
    
    def set_theme(self, theme):
        """Set current theme"""
        self.set("appearance.theme", theme)
        self.save_settings()
    
    def get_window_geometry(self):
        """Get window geometry"""
        return self.get("appearance.window_geometry", "1400x900")
    
    def set_window_geometry(self, geometry):
        """Set window geometry"""
        self.set("appearance.window_geometry", geometry)
        self.save_settings()
    
    def get_grid_settings(self):
        """Get grid settings"""
        return {
            "size": self.get("canvas.grid_size", 20),
            "show": self.get("canvas.show_grid", True),
            "snap": self.get("canvas.snap_to_grid", True)
        }
    
    def set_grid_settings(self, size=None, show=None, snap=None):
        """Set grid settings"""
        if size is not None:
            self.set("canvas.grid_size", size)
        if show is not None:
            self.set("canvas.show_grid", show)
        if snap is not None:
            self.set("canvas.snap_to_grid", snap)
        self.save_settings()
    
    def add_recent_file(self, file_path):
        """Add file to recent files list"""
        recent_files = self.get("recent_files.files", [])
        max_files = self.get("recent_files.max_files", 10)
        
        # Remove if already exists
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # Add to beginning
        recent_files.insert(0, file_path)
        
        # Limit list size
        recent_files = recent_files[:max_files]
        
        self.set("recent_files.files", recent_files)
        self.save_settings()
    
    def get_recent_files(self):
        """Get recent files list"""
        recent_files = self.get("recent_files.files", [])
        
        # Filter out files that no longer exist
        existing_files = [f for f in recent_files if os.path.exists(f)]
        
        # Update the list if files were removed
        if len(existing_files) != len(recent_files):
            self.set("recent_files.files", existing_files)
            self.save_settings()
        
        return existing_files
    
    def get_component_defaults(self, component_type):
        """Get default colors for a component type"""
        return self.get(f"editor.default_component_colors.{component_type}", {})
    
    def set_component_defaults(self, component_type, colors):
        """Set default colors for a component type"""
        self.set(f"editor.default_component_colors.{component_type}", colors)
        self.save_settings()
    
    def get_export_settings(self):
        """Get export settings"""
        return {
            "format": self.get("export.default_format", "png"),
            "quality": self.get("export.png_quality", 95),
            "precision": self.get("export.svg_precision", 2),
            "metadata": self.get("export.include_metadata", True),
            "path": self.get("export.default_export_path", "")
        }
    
    def set_export_settings(self, **kwargs):
        """Set export settings"""
        for key, value in kwargs.items():
            if key in ["format", "quality", "precision", "metadata", "path"]:
                setting_key = {
                    "format": "export.default_format",
                    "quality": "export.png_quality", 
                    "precision": "export.svg_precision",
                    "metadata": "export.include_metadata",
                    "path": "export.default_export_path"
                }[key]
                self.set(setting_key, value)
        self.save_settings()
    
    def import_settings(self, file_path):
        """Import settings from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            # Validate and merge
            self.settings = self._merge_settings(self.default_settings, imported_settings)
            return self.save_settings()
        
        except Exception as e:
            print(f"Error importing settings: {e}")
            return False
    
    def export_settings(self, file_path):
        """Export current settings to a file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return False
    
    def get_ui_settings(self):
        """Get UI layout settings"""
        return {
            "properties_panel": self.get("ui.show_properties_panel", True),
            "component_palette": self.get("ui.show_component_palette", True),
            "properties_width": self.get("ui.properties_panel_width", 250),
            "palette_width": self.get("ui.component_palette_width", 200),
            "toolbar": self.get("ui.toolbar_visible", True)
        }
    
    def set_ui_settings(self, **kwargs):
        """Set UI layout settings"""
        for key, value in kwargs.items():
            if key in ["properties_panel", "component_palette", "properties_width", "palette_width", "toolbar"]:
                setting_key = {
                    "properties_panel": "ui.show_properties_panel",
                    "component_palette": "ui.show_component_palette",
                    "properties_width": "ui.properties_panel_width",
                    "palette_width": "ui.component_palette_width",
                    "toolbar": "ui.toolbar_visible"
                }[key]
                self.set(setting_key, value)
        self.save_settings()
