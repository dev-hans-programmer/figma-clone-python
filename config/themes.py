"""
Theme configuration for the application
"""

class AppThemes:
    """Manages application themes and color schemes"""
    
    def __init__(self):
        """Initialize theme manager"""
        self.themes = {
            "dark": {
                "name": "Dark",
                "description": "Dark theme with blue accents",
                "appearance_mode": "dark",
                "color_theme": "blue",
                "colors": {
                    "primary": "#3b82f6",
                    "primary_hover": "#2563eb",
                    "secondary": "#6b7280",
                    "secondary_hover": "#4b5563",
                    "success": "#10b981",
                    "success_hover": "#059669",
                    "warning": "#f59e0b",
                    "warning_hover": "#d97706",
                    "error": "#ef4444",
                    "error_hover": "#dc2626",
                    "background": "#1f2937",
                    "surface": "#374151",
                    "surface_variant": "#4b5563",
                    "on_background": "#f9fafb",
                    "on_surface": "#e5e7eb",
                    "border": "#6b7280",
                    "border_light": "#9ca3af",
                    "text_primary": "#f9fafb",
                    "text_secondary": "#d1d5db",
                    "text_disabled": "#9ca3af"
                },
                "canvas": {
                    "background": "#f8fafc",
                    "grid": "#e2e8f0",
                    "selection": "#3b82f6",
                    "selection_handles": "#2563eb",
                    "guides": "#8b5cf6"
                }
            },
            
            "light": {
                "name": "Light",
                "description": "Light theme with blue accents",
                "appearance_mode": "light",
                "color_theme": "blue",
                "colors": {
                    "primary": "#3b82f6",
                    "primary_hover": "#2563eb",
                    "secondary": "#6b7280",
                    "secondary_hover": "#4b5563",
                    "success": "#10b981",
                    "success_hover": "#059669",
                    "warning": "#f59e0b",
                    "warning_hover": "#d97706",
                    "error": "#ef4444",
                    "error_hover": "#dc2626",
                    "background": "#ffffff",
                    "surface": "#f9fafb",
                    "surface_variant": "#f3f4f6",
                    "on_background": "#111827",
                    "on_surface": "#374151",
                    "border": "#d1d5db",
                    "border_light": "#e5e7eb",
                    "text_primary": "#111827",
                    "text_secondary": "#4b5563",
                    "text_disabled": "#9ca3af"
                },
                "canvas": {
                    "background": "#ffffff",
                    "grid": "#f3f4f6",
                    "selection": "#3b82f6",
                    "selection_handles": "#2563eb",
                    "guides": "#8b5cf6"
                }
            },
            
            "dark_green": {
                "name": "Dark Green",
                "description": "Dark theme with green accents",
                "appearance_mode": "dark",
                "color_theme": "green",
                "colors": {
                    "primary": "#10b981",
                    "primary_hover": "#059669",
                    "secondary": "#6b7280",
                    "secondary_hover": "#4b5563",
                    "success": "#22c55e",
                    "success_hover": "#16a34a",
                    "warning": "#f59e0b",
                    "warning_hover": "#d97706",
                    "error": "#ef4444",
                    "error_hover": "#dc2626",
                    "background": "#1f2937",
                    "surface": "#374151",
                    "surface_variant": "#4b5563",
                    "on_background": "#f9fafb",
                    "on_surface": "#e5e7eb",
                    "border": "#6b7280",
                    "border_light": "#9ca3af",
                    "text_primary": "#f9fafb",
                    "text_secondary": "#d1d5db",
                    "text_disabled": "#9ca3af"
                },
                "canvas": {
                    "background": "#f8fafc",
                    "grid": "#e2e8f0",
                    "selection": "#10b981",
                    "selection_handles": "#059669",
                    "guides": "#8b5cf6"
                }
            },
            
            "dark_purple": {
                "name": "Dark Purple",
                "description": "Dark theme with purple accents",
                "appearance_mode": "dark",
                "color_theme": "dark-blue",
                "colors": {
                    "primary": "#8b5cf6",
                    "primary_hover": "#7c3aed",
                    "secondary": "#6b7280",
                    "secondary_hover": "#4b5563",
                    "success": "#10b981",
                    "success_hover": "#059669",
                    "warning": "#f59e0b",
                    "warning_hover": "#d97706",
                    "error": "#ef4444",
                    "error_hover": "#dc2626",
                    "background": "#1f2937",
                    "surface": "#374151",
                    "surface_variant": "#4b5563",
                    "on_background": "#f9fafb",
                    "on_surface": "#e5e7eb",
                    "border": "#6b7280",
                    "border_light": "#9ca3af",
                    "text_primary": "#f9fafb",
                    "text_secondary": "#d1d5db",
                    "text_disabled": "#9ca3af"
                },
                "canvas": {
                    "background": "#f8fafc",
                    "grid": "#e2e8f0",
                    "selection": "#8b5cf6",
                    "selection_handles": "#7c3aed",
                    "guides": "#3b82f6"
                }
            },
            
            "high_contrast": {
                "name": "High Contrast",
                "description": "High contrast theme for accessibility",
                "appearance_mode": "dark",
                "color_theme": "blue",
                "colors": {
                    "primary": "#ffffff",
                    "primary_hover": "#e5e7eb",
                    "secondary": "#000000",
                    "secondary_hover": "#1f2937",
                    "success": "#00ff00",
                    "success_hover": "#00cc00",
                    "warning": "#ffff00",
                    "warning_hover": "#cccc00",
                    "error": "#ff0000",
                    "error_hover": "#cc0000",
                    "background": "#000000",
                    "surface": "#1f2937",
                    "surface_variant": "#374151",
                    "on_background": "#ffffff",
                    "on_surface": "#ffffff",
                    "border": "#ffffff",
                    "border_light": "#d1d5db",
                    "text_primary": "#ffffff",
                    "text_secondary": "#ffffff",
                    "text_disabled": "#9ca3af"
                },
                "canvas": {
                    "background": "#ffffff",
                    "grid": "#000000",
                    "selection": "#ffff00",
                    "selection_handles": "#ff0000",
                    "guides": "#00ff00"
                }
            }
        }
        
        self.color_schemes = {
            "blue": {
                "name": "Blue",
                "primary": "#3b82f6",
                "secondary": "#1e40af"
            },
            "green": {
                "name": "Green", 
                "primary": "#10b981",
                "secondary": "#059669"
            },
            "dark-blue": {
                "name": "Dark Blue",
                "primary": "#1e40af",
                "secondary": "#1e3a8a"
            }
        }
    
    def get_theme(self, theme_name):
        """Get theme configuration by name"""
        return self.themes.get(theme_name, self.themes["dark"])
    
    def get_available_themes(self):
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def get_theme_info(self, theme_name):
        """Get basic info about a theme"""
        theme = self.get_theme(theme_name)
        return {
            "name": theme["name"],
            "description": theme["description"],
            "preview_color": theme["colors"]["primary"]
        }
    
    def get_color_schemes(self):
        """Get available color schemes"""
        return self.color_schemes
    
    def apply_theme_to_customtkinter(self, theme_name):
        """Apply theme to customtkinter (returns settings for manual application)"""
        theme = self.get_theme(theme_name)
        
        return {
            "appearance_mode": theme["appearance_mode"],
            "color_theme": theme["color_theme"]
        }
    
    def get_component_colors(self, theme_name):
        """Get component-specific colors for a theme"""
        theme = self.get_theme(theme_name)
        colors = theme["colors"]
        
        return {
            "rectangle": {
                "fill": colors["surface_variant"],
                "border": colors["border"],
                "text": colors["text_primary"]
            },
            "button": {
                "fill": colors["primary"],
                "border": colors["primary_hover"],
                "text": "#ffffff"
            },
            "input": {
                "fill": colors["background"],
                "border": colors["border"],
                "text": colors["text_primary"]
            },
            "text": {
                "fill": "",
                "border": "",
                "text": colors["text_primary"]
            }
        }
    
    def get_canvas_colors(self, theme_name):
        """Get canvas-specific colors for a theme"""
        theme = self.get_theme(theme_name)
        return theme["canvas"]
    
    def create_custom_theme(self, name, base_theme="dark", color_overrides=None):
        """Create a custom theme based on an existing theme"""
        base = self.get_theme(base_theme).copy()
        
        if color_overrides:
            base["colors"].update(color_overrides)
        
        base["name"] = name
        base["description"] = f"Custom theme based on {base_theme}"
        
        return base
    
    def validate_theme(self, theme_config):
        """Validate theme configuration"""
        required_keys = ["name", "appearance_mode", "color_theme", "colors", "canvas"]
        required_colors = [
            "primary", "secondary", "background", "surface", "on_background", 
            "on_surface", "text_primary", "border"
        ]
        required_canvas = ["background", "grid", "selection"]
        
        # Check top-level keys
        for key in required_keys:
            if key not in theme_config:
                return False, f"Missing required key: {key}"
        
        # Check required colors
        colors = theme_config.get("colors", {})
        for color in required_colors:
            if color not in colors:
                return False, f"Missing required color: {color}"
        
        # Check canvas colors
        canvas = theme_config.get("canvas", {})
        for color in required_canvas:
            if color not in canvas:
                return False, f"Missing required canvas color: {color}"
        
        # Validate color values (basic hex check)
        all_colors = {**colors, **canvas}
        for color_name, color_value in all_colors.items():
            if color_value and not self._is_valid_color(color_value):
                return False, f"Invalid color value for {color_name}: {color_value}"
        
        return True, "Valid theme configuration"
    
    def _is_valid_color(self, color_value):
        """Basic validation for color values"""
        if not color_value:  # Empty string is valid (transparent)
            return True
        
        # Check hex color format
        if color_value.startswith("#"):
            if len(color_value) in [4, 7, 9]:  # #RGB, #RRGGBB, #RRGGBBAA
                try:
                    int(color_value[1:], 16)
                    return True
                except ValueError:
                    return False
        
        # Check named colors (basic set)
        named_colors = [
            "red", "green", "blue", "yellow", "orange", "purple", "pink",
            "black", "white", "gray", "grey", "brown", "cyan", "magenta"
        ]
        
        return color_value.lower() in named_colors
    
    def export_theme(self, theme_name, file_path):
        """Export theme to JSON file"""
        import json
        
        theme = self.get_theme(theme_name)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(theme, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting theme: {e}")
            return False
    
    def import_theme(self, file_path):
        """Import theme from JSON file"""
        import json
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                theme_config = json.load(f)
            
            # Validate theme
            is_valid, message = self.validate_theme(theme_config)
            if not is_valid:
                return False, message
            
            # Generate unique name if needed
            theme_name = theme_config["name"]
            original_name = theme_name
            counter = 1
            
            while theme_name in self.themes:
                theme_name = f"{original_name}_{counter}"
                counter += 1
            
            theme_config["name"] = theme_name
            self.themes[theme_name] = theme_config
            
            return True, f"Theme imported as '{theme_name}'"
        
        except Exception as e:
            return False, f"Error importing theme: {e}"
    
    def get_theme_preview_data(self, theme_name):
        """Get data for theme preview"""
        theme = self.get_theme(theme_name)
        colors = theme["colors"]
        canvas = theme["canvas"]
        
        return {
            "background": colors["background"],
            "surface": colors["surface"],
            "primary": colors["primary"],
            "secondary": colors["secondary"],
            "text": colors["text_primary"],
            "canvas_bg": canvas["background"],
            "canvas_grid": canvas["grid"],
            "selection": canvas["selection"]
        }
