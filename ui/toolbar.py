"""
Main toolbar for the application
"""

import customtkinter as ctk
from tkinter import messagebox

class Toolbar(ctk.CTkFrame):
    """Main application toolbar"""
    
    def __init__(self, parent, main_window):
        """Initialize the toolbar"""
        super().__init__(parent)
        self.main_window = main_window
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup toolbar UI"""
        # Configure grid
        self.grid_columnconfigure(10, weight=1)  # Spacer column
        
        # File operations
        self.new_btn = ctk.CTkButton(
            self, text="New", width=60,
            command=self.main_window.new_file
        )
        self.new_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.open_btn = ctk.CTkButton(
            self, text="Open", width=60,
            command=self.main_window.open_file
        )
        self.open_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.save_btn = ctk.CTkButton(
            self, text="Save", width=60,
            command=self.main_window.save_file
        )
        self.save_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Separator
        separator1 = ctk.CTkFrame(self, width=2, height=30, fg_color="gray")
        separator1.grid(row=0, column=3, padx=10, pady=5)
        
        # Edit operations
        self.undo_btn = ctk.CTkButton(
            self, text="Undo", width=60,
            command=self.main_window.undo
        )
        self.undo_btn.grid(row=0, column=4, padx=5, pady=5)
        
        self.redo_btn = ctk.CTkButton(
            self, text="Redo", width=60,
            command=self.main_window.redo
        )
        self.redo_btn.grid(row=0, column=5, padx=5, pady=5)
        
        # Separator
        separator2 = ctk.CTkFrame(self, width=2, height=30, fg_color="gray")
        separator2.grid(row=0, column=6, padx=10, pady=5)
        
        # Alignment tools
        self.align_left_btn = ctk.CTkButton(
            self, text="⫷", width=40,
            command=lambda: self.main_window.canvas_manager.align_components("left")
        )
        self.align_left_btn.grid(row=0, column=7, padx=2, pady=5)
        
        self.align_center_btn = ctk.CTkButton(
            self, text="⫸", width=40,
            command=lambda: self.main_window.canvas_manager.align_components("center_horizontal")
        )
        self.align_center_btn.grid(row=0, column=8, padx=2, pady=5)
        
        self.align_right_btn = ctk.CTkButton(
            self, text="⫷", width=40,
            command=lambda: self.main_window.canvas_manager.align_components("right")
        )
        self.align_right_btn.grid(row=0, column=9, padx=2, pady=5)
        
        # Spacer
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.grid(row=0, column=10, sticky="ew")
        
        # View controls
        self.grid_btn = ctk.CTkButton(
            self, text="Grid", width=60,
            command=self.toggle_grid
        )
        self.grid_btn.grid(row=0, column=11, padx=5, pady=5)
        
        self.zoom_label = ctk.CTkLabel(self, text="100%")
        self.zoom_label.grid(row=0, column=12, padx=5, pady=5)
        
        self.zoom_in_btn = ctk.CTkButton(
            self, text="+", width=30,
            command=lambda: self.zoom(1.2)
        )
        self.zoom_in_btn.grid(row=0, column=13, padx=2, pady=5)
        
        self.zoom_out_btn = ctk.CTkButton(
            self, text="-", width=30,
            command=lambda: self.zoom(0.8)
        )
        self.zoom_out_btn.grid(row=0, column=14, padx=2, pady=5)
        
        self.zoom_reset_btn = ctk.CTkButton(
            self, text="100%", width=50,
            command=self.reset_zoom
        )
        self.zoom_reset_btn.grid(row=0, column=15, padx=5, pady=5)
        
        # Export button
        self.export_btn = ctk.CTkButton(
            self, text="Export", width=70,
            command=self.main_window.export_design
        )
        self.export_btn.grid(row=0, column=16, padx=5, pady=5)
    
    def toggle_grid(self):
        """Toggle grid visibility"""
        if hasattr(self.main_window, 'design_canvas'):
            self.main_window.design_canvas.toggle_grid()
            # Update button text based on grid state
            grid_visible = self.main_window.design_canvas.show_grid
            self.grid_btn.configure(text="Grid ✓" if grid_visible else "Grid")
    
    def zoom(self, factor):
        """Zoom the canvas"""
        if hasattr(self.main_window, 'design_canvas'):
            self.main_window.design_canvas.zoom(factor)
            self.update_zoom_label()
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        if hasattr(self.main_window, 'design_canvas'):
            self.main_window.design_canvas.reset_zoom()
            self.update_zoom_label()
    
    def update_zoom_label(self):
        """Update zoom percentage label"""
        if hasattr(self.main_window, 'design_canvas'):
            zoom_percent = int(self.main_window.design_canvas.zoom_level * 100)
            self.zoom_label.configure(text=f"{zoom_percent}%")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Mini Figma",
            "Mini Figma - UI Wireframe Designer\n\n"
            "A simple tool for creating UI wireframes and mockups.\n\n"
            "Features:\n"
            "• Drag-and-drop UI components\n"
            "• Resize and move elements\n"
            "• Save/load designs\n"
            "• Export as PNG/SVG\n\n"
            "Built with Python and CustomTkinter"
        )
