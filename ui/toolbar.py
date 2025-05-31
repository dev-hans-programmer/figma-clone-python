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
        
        # Group button
        self.group_btn = ctk.CTkButton(
            self, text="Group", width=60,
            command=self.group_components
        )
        self.group_btn.grid(row=0, column=16, padx=5, pady=5)
        
        # Ungroup button
        self.ungroup_btn = ctk.CTkButton(
            self, text="Ungroup", width=70,
            command=self.ungroup_component
        )
        self.ungroup_btn.grid(row=0, column=17, padx=5, pady=5)
        
        # Auto-save toggle button
        self.auto_save_btn = ctk.CTkButton(
            self, text="Auto-save ✓" if hasattr(self.main_window, 'auto_save_enabled') and self.main_window.auto_save_enabled else "Auto-save", 
            width=80,
            command=self.toggle_auto_save
        )
        self.auto_save_btn.grid(row=0, column=18, padx=5, pady=5)
        
        # Export button
        self.export_btn = ctk.CTkButton(
            self, text="Export", width=70,
            command=self.main_window.export_design
        )
        self.export_btn.grid(row=0, column=19, padx=5, pady=5)
    
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
    
    def group_components(self):
        """Group selected components"""
        if hasattr(self.main_window, 'canvas_manager'):
            group = self.main_window.canvas_manager.group_selected_components()
            if group:
                print(f"Grouped {len(group.children)} components")
            else:
                print("Select at least 2 components to group")
    
    def ungroup_component(self):
        """Ungroup selected component"""
        if hasattr(self.main_window, 'canvas_manager'):
            selected = self.main_window.canvas_manager.selected_component
            if selected and hasattr(selected, 'is_group') and selected.is_group:
                children = self.main_window.canvas_manager.ungroup_component(selected)
                print(f"Ungrouped component into {len(children)} items")
            else:
                print("Select a group to ungroup")
    
    def toggle_auto_save(self):
        """Toggle auto-save functionality"""
        self.main_window.toggle_auto_save()
        # Update button text
        self.auto_save_btn.configure(
            text="Auto-save ✓" if self.main_window.auto_save_enabled else "Auto-save"
        )
    
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
            "• Export as PNG/SVG\n"
            "• Auto-save functionality\n\n"
            "Built with Python and CustomTkinter"
        )
