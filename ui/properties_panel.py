"""
Properties panel for editing component properties
"""

import customtkinter as ctk
from tkinter import colorchooser

class PropertiesPanel(ctk.CTkFrame):
    """Properties panel for component editing"""
    
    def __init__(self, parent, main_window):
        """Initialize the properties panel"""
        super().__init__(parent)
        self.main_window = main_window
        self.current_component = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup properties panel UI"""
        # Configure scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Title
        self.title = ctk.CTkLabel(
            self.scrollable_frame, 
            text="Properties", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title.pack(pady=(10, 20))
        
        # No selection message
        self.no_selection_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Select a component\nto edit properties",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.no_selection_label.pack(pady=20)
        
        # Properties container (initially hidden)
        self.properties_container = ctk.CTkFrame(self.scrollable_frame)
        
        self.setup_properties_widgets()
    
    def setup_properties_widgets(self):
        """Setup all property editing widgets"""
        # Position section
        self.position_frame = ctk.CTkFrame(self.properties_container)
        self.position_frame.pack(fill="x", padx=5, pady=5)
        
        pos_label = ctk.CTkLabel(
            self.position_frame, 
            text="Position & Size",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        pos_label.pack(pady=(10, 5))
        
        # X position
        x_frame = ctk.CTkFrame(self.position_frame, fg_color="transparent")
        x_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(x_frame, text="X:", width=30).pack(side="left")
        self.x_entry = ctk.CTkEntry(x_frame, width=80)
        self.x_entry.pack(side="left", padx=(5, 0))
        self.x_entry.bind("<Return>", self.on_position_change)
        
        # Y position
        y_frame = ctk.CTkFrame(self.position_frame, fg_color="transparent")
        y_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(y_frame, text="Y:", width=30).pack(side="left")
        self.y_entry = ctk.CTkEntry(y_frame, width=80)
        self.y_entry.pack(side="left", padx=(5, 0))
        self.y_entry.bind("<Return>", self.on_position_change)
        
        # Width
        w_frame = ctk.CTkFrame(self.position_frame, fg_color="transparent")
        w_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(w_frame, text="W:", width=30).pack(side="left")
        self.width_entry = ctk.CTkEntry(w_frame, width=80)
        self.width_entry.pack(side="left", padx=(5, 0))
        self.width_entry.bind("<Return>", self.on_size_change)
        
        # Height
        h_frame = ctk.CTkFrame(self.position_frame, fg_color="transparent")
        h_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(h_frame, text="H:", width=30).pack(side="left")
        self.height_entry = ctk.CTkEntry(h_frame, width=80)
        self.height_entry.pack(side="left", padx=(5, 0))
        self.height_entry.bind("<Return>", self.on_size_change)
        
        # Add some space
        ctk.CTkFrame(self.position_frame, height=10, fg_color="transparent").pack()
        
        # Text section
        self.text_frame = ctk.CTkFrame(self.properties_container)
        self.text_frame.pack(fill="x", padx=5, pady=5)
        
        text_label = ctk.CTkLabel(
            self.text_frame, 
            text="Text Properties",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        text_label.pack(pady=(10, 5))
        
        # Text content
        text_content_frame = ctk.CTkFrame(self.text_frame, fg_color="transparent")
        text_content_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(text_content_frame, text="Text:").pack(anchor="w")
        self.text_entry = ctk.CTkEntry(text_content_frame, width=180)
        self.text_entry.pack(fill="x", pady=(2, 5))
        self.text_entry.bind("<Return>", self.on_text_change)
        
        # Font size
        font_size_frame = ctk.CTkFrame(self.text_frame, fg_color="transparent")
        font_size_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(font_size_frame, text="Font Size:", width=80).pack(side="left")
        self.font_size_var = ctk.StringVar(value="12")
        self.font_size_combo = ctk.CTkComboBox(
            font_size_frame,
            values=["8", "10", "12", "14", "16", "18", "20", "24", "28", "32"],
            variable=self.font_size_var,
            width=80,
            command=self.on_font_change
        )
        self.font_size_combo.pack(side="right")
        
        # Font weight
        font_weight_frame = ctk.CTkFrame(self.text_frame, fg_color="transparent")
        font_weight_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(font_weight_frame, text="Weight:", width=80).pack(side="left")
        self.font_weight_var = ctk.StringVar(value="normal")
        self.font_weight_combo = ctk.CTkComboBox(
            font_weight_frame,
            values=["normal", "bold"],
            variable=self.font_weight_var,
            width=80,
            command=self.on_font_change
        )
        self.font_weight_combo.pack(side="right")
        
        # Text alignment (for text components)
        text_align_frame = ctk.CTkFrame(self.text_frame, fg_color="transparent")
        text_align_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(text_align_frame, text="Align:", width=80).pack(side="left")
        self.text_align_var = ctk.StringVar(value="left")
        self.text_align_combo = ctk.CTkComboBox(
            text_align_frame,
            values=["left", "center", "right"],
            variable=self.text_align_var,
            width=80,
            command=self.on_text_align_change
        )
        self.text_align_combo.pack(side="right")
        
        # Add some space
        ctk.CTkFrame(self.text_frame, height=10, fg_color="transparent").pack()
        
        # Appearance section
        self.appearance_frame = ctk.CTkFrame(self.properties_container)
        self.appearance_frame.pack(fill="x", padx=5, pady=5)
        
        appearance_label = ctk.CTkLabel(
            self.appearance_frame, 
            text="Appearance",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        appearance_label.pack(pady=(10, 5))
        
        # Fill color
        fill_color_frame = ctk.CTkFrame(self.appearance_frame, fg_color="transparent")
        fill_color_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(fill_color_frame, text="Fill Color:", width=80).pack(side="left")
        self.fill_color_btn = ctk.CTkButton(
            fill_color_frame,
            text="",
            width=60,
            height=25,
            command=self.choose_fill_color
        )
        self.fill_color_btn.pack(side="right")
        
        # Border color
        border_color_frame = ctk.CTkFrame(self.appearance_frame, fg_color="transparent")
        border_color_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(border_color_frame, text="Border:", width=80).pack(side="left")
        self.border_color_btn = ctk.CTkButton(
            border_color_frame,
            text="",
            width=60,
            height=25,
            command=self.choose_border_color
        )
        self.border_color_btn.pack(side="right")
        
        # Text color
        text_color_frame = ctk.CTkFrame(self.appearance_frame, fg_color="transparent")
        text_color_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(text_color_frame, text="Text Color:", width=80).pack(side="left")
        self.text_color_btn = ctk.CTkButton(
            text_color_frame,
            text="",
            width=60,
            height=25,
            command=self.choose_text_color
        )
        self.text_color_btn.pack(side="right")
        
        # Border width
        border_width_frame = ctk.CTkFrame(self.appearance_frame, fg_color="transparent")
        border_width_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(border_width_frame, text="Border Width:", width=100).pack(side="left")
        self.border_width_var = ctk.StringVar(value="2")
        self.border_width_combo = ctk.CTkComboBox(
            border_width_frame,
            values=["0", "1", "2", "3", "4", "5"],
            variable=self.border_width_var,
            width=60,
            command=self.on_border_width_change
        )
        self.border_width_combo.pack(side="right")
        
        # Corner radius
        corner_radius_frame = ctk.CTkFrame(self.appearance_frame, fg_color="transparent")
        corner_radius_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(corner_radius_frame, text="Corner Radius:", width=100).pack(side="left")
        self.corner_radius_var = ctk.StringVar(value="0")
        self.corner_radius_combo = ctk.CTkComboBox(
            corner_radius_frame,
            values=["0", "2", "4", "6", "8", "10", "12", "16", "20"],
            variable=self.corner_radius_var,
            width=60,
            command=self.on_corner_radius_change
        )
        self.corner_radius_combo.pack(side="right")
        
        # Add some space
        ctk.CTkFrame(self.appearance_frame, height=10, fg_color="transparent").pack()
        
        # Actions section
        self.actions_frame = ctk.CTkFrame(self.properties_container)
        self.actions_frame.pack(fill="x", padx=5, pady=5)
        
        actions_label = ctk.CTkLabel(
            self.actions_frame, 
            text="Actions",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        actions_label.pack(pady=(10, 5))
        
        # Delete button
        self.delete_btn = ctk.CTkButton(
            self.actions_frame,
            text="Delete",
            width=160,
            height=35,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.delete_component
        )
        self.delete_btn.pack(pady=5, padx=10)
        
        # Duplicate button
        self.duplicate_btn = ctk.CTkButton(
            self.actions_frame,
            text="Duplicate",
            width=160,
            height=35,
            fg_color="#6b7280",
            command=self.duplicate_component
        )
        self.duplicate_btn.pack(pady=5, padx=10)
        
        # Add some space
        ctk.CTkFrame(self.actions_frame, height=10, fg_color="transparent").pack()
    
    def update_selection(self, component):
        """Update the properties panel with the selected component"""
        self.current_component = component
        
        if component:
            # Hide no selection message and show properties
            self.no_selection_label.pack_forget()
            self.properties_container.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Update all fields
            self.x_entry.delete(0, "end")
            self.x_entry.insert(0, str(int(component.x)))
            
            self.y_entry.delete(0, "end")
            self.y_entry.insert(0, str(int(component.y)))
            
            self.width_entry.delete(0, "end")
            self.width_entry.insert(0, str(int(component.width)))
            
            self.height_entry.delete(0, "end")
            self.height_entry.insert(0, str(int(component.height)))
            
            # Text properties
            self.text_entry.delete(0, "end")
            self.text_entry.insert(0, component.text)
            
            self.font_size_var.set(str(component.font_size))
            self.font_weight_var.set(component.font_weight)
            
            # Text alignment (only for text components)
            if hasattr(component, 'text_align'):
                self.text_align_var.set(component.text_align)
                self.text_align_combo.configure(state="normal")
            else:
                self.text_align_combo.configure(state="disabled")
            
            # Appearance
            self.fill_color_btn.configure(fg_color=component.fill_color or "#3b82f6")
            self.border_color_btn.configure(fg_color=component.border_color or "#1e40af")
            self.text_color_btn.configure(fg_color=component.text_color or "#ffffff")
            
            self.border_width_var.set(str(component.border_width))
            self.corner_radius_var.set(str(component.corner_radius))
            
        else:
            self.clear_selection()
    
    def clear_selection(self):
        """Clear the properties panel"""
        self.current_component = None
        self.properties_container.pack_forget()
        self.no_selection_label.pack(pady=20)
    
    def on_position_change(self, event=None):
        """Handle position change"""
        if not self.current_component:
            return
        
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            self.current_component.set_position(x, y)
            self.current_component.draw(self.main_window.design_canvas.canvas)
            self.main_window.mark_modified()
        except ValueError:
            pass  # Invalid input, ignore
    
    def on_size_change(self, event=None):
        """Handle size change"""
        if not self.current_component:
            return
        
        try:
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())
            self.current_component.resize(width, height)
            self.current_component.draw(self.main_window.design_canvas.canvas)
            self.main_window.mark_modified()
        except ValueError:
            pass  # Invalid input, ignore
    
    def on_text_change(self, event=None):
        """Handle text change"""
        if not self.current_component:
            return
        
        self.current_component.text = self.text_entry.get()
        self.current_component.draw(self.main_window.design_canvas.canvas)
        self.main_window.mark_modified()
    
    def on_font_change(self, value=None):
        """Handle font change"""
        if not self.current_component:
            return
        
        self.current_component.font_size = int(self.font_size_var.get())
        self.current_component.font_weight = self.font_weight_var.get()
        self.current_component.draw(self.main_window.design_canvas.canvas)
        self.main_window.mark_modified()
    
    def on_text_align_change(self, value=None):
        """Handle text alignment change"""
        if not self.current_component or not hasattr(self.current_component, 'text_align'):
            return
        
        self.current_component.text_align = self.text_align_var.get()
        self.current_component.draw(self.main_window.design_canvas.canvas)
        self.main_window.mark_modified()
    
    def on_border_width_change(self, value=None):
        """Handle border width change"""
        if not self.current_component:
            return
        
        self.current_component.border_width = int(self.border_width_var.get())
        self.current_component.draw(self.main_window.design_canvas.canvas)
        self.main_window.mark_modified()
    
    def on_corner_radius_change(self, value=None):
        """Handle corner radius change"""
        if not self.current_component:
            return
        
        self.current_component.corner_radius = int(self.corner_radius_var.get())
        self.current_component.draw(self.main_window.design_canvas.canvas)
        self.main_window.mark_modified()
    
    def choose_fill_color(self):
        """Choose fill color"""
        if not self.current_component:
            return
        
        color = colorchooser.askcolor(
            title="Choose Fill Color",
            initialcolor=self.current_component.fill_color
        )
        
        if color[1]:  # color[1] is the hex value
            self.current_component.fill_color = color[1]
            self.fill_color_btn.configure(fg_color=color[1])
            self.current_component.draw(self.main_window.design_canvas.canvas)
            self.main_window.mark_modified()
    
    def choose_border_color(self):
        """Choose border color"""
        if not self.current_component:
            return
        
        color = colorchooser.askcolor(
            title="Choose Border Color",
            initialcolor=self.current_component.border_color
        )
        
        if color[1]:
            self.current_component.border_color = color[1]
            self.border_color_btn.configure(fg_color=color[1])
            self.current_component.draw(self.main_window.design_canvas.canvas)
            self.main_window.mark_modified()
    
    def choose_text_color(self):
        """Choose text color"""
        if not self.current_component:
            return
        
        color = colorchooser.askcolor(
            title="Choose Text Color",
            initialcolor=self.current_component.text_color
        )
        
        if color[1]:
            self.current_component.text_color = color[1]
            self.text_color_btn.configure(fg_color=color[1])
            self.current_component.draw(self.main_window.design_canvas.canvas)
            self.main_window.mark_modified()
    
    def delete_component(self):
        """Delete the current component"""
        if self.current_component:
            self.main_window.canvas_manager.delete_component(self.current_component)
            self.clear_selection()
            self.main_window.mark_modified()
    
    def duplicate_component(self):
        """Duplicate the current component"""
        if self.current_component:
            clone = self.main_window.canvas_manager.duplicate_component(self.current_component)
            if clone:
                self.main_window.select_component(clone)
                self.main_window.mark_modified()
