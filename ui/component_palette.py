"""
Component palette for adding UI elements
"""

import customtkinter as ctk

class ComponentPalette(ctk.CTkFrame):
    """Component palette for UI elements"""
    
    def __init__(self, parent, main_window):
        """Initialize the component palette"""
        super().__init__(parent)
        self.main_window = main_window
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup component palette UI"""
        # Title
        title = ctk.CTkLabel(
            self, text="Components", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 20), padx=10)
        
        # Basic shapes section
        shapes_frame = ctk.CTkFrame(self)
        shapes_frame.pack(fill="x", padx=10, pady=5)
        
        shapes_label = ctk.CTkLabel(
            shapes_frame, text="Basic Shapes",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        shapes_label.pack(pady=(10, 5))
        
        # Rectangle button
        self.rect_btn = ctk.CTkButton(
            shapes_frame,
            text="Rectangle",
            width=160,
            height=40,
            command=lambda: self.add_component("rectangle")
        )
        self.rect_btn.pack(pady=5, padx=10)
        
        # UI controls section
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        controls_label = ctk.CTkLabel(
            controls_frame, text="UI Controls",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        controls_label.pack(pady=(10, 5))
        
        # Button component
        self.button_btn = ctk.CTkButton(
            controls_frame,
            text="Button",
            width=160,
            height=40,
            fg_color="#3b82f6",
            command=lambda: self.add_component("button")
        )
        self.button_btn.pack(pady=5, padx=10)
        
        # Input field component
        self.input_btn = ctk.CTkButton(
            controls_frame,
            text="Input Field",
            width=160,
            height=40,
            fg_color="#10b981",
            command=lambda: self.add_component("input")
        )
        self.input_btn.pack(pady=5, padx=10)
        
        # Text section
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(fill="x", padx=10, pady=5)
        
        text_label = ctk.CTkLabel(
            text_frame, text="Text Elements",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        text_label.pack(pady=(10, 5))
        
        # Text label component
        self.text_btn = ctk.CTkButton(
            text_frame,
            text="Text Label",
            width=160,
            height=40,
            fg_color="#8b5cf6",
            command=lambda: self.add_component("text")
        )
        self.text_btn.pack(pady=5, padx=10)
        
        # Add spacer
        spacer = ctk.CTkFrame(self, height=20, fg_color="transparent")
        spacer.pack(fill="x")
        
        # Quick actions section
        actions_frame = ctk.CTkFrame(self)
        actions_frame.pack(fill="x", padx=10, pady=5)
        
        actions_label = ctk.CTkLabel(
            actions_frame, text="Quick Actions",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        actions_label.pack(pady=(10, 5))
        
        # Clear canvas
        self.clear_btn = ctk.CTkButton(
            actions_frame,
            text="Clear Canvas",
            width=160,
            height=35,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.clear_canvas
        )
        self.clear_btn.pack(pady=5, padx=10)
        
        # Select all
        self.select_all_btn = ctk.CTkButton(
            actions_frame,
            text="Select All",
            width=160,
            height=35,
            fg_color="#6b7280",
            command=self.select_all_components
        )
        self.select_all_btn.pack(pady=5, padx=10)
        
        # Component templates section
        templates_frame = ctk.CTkFrame(self)
        templates_frame.pack(fill="x", padx=10, pady=5)
        
        templates_label = ctk.CTkLabel(
            templates_frame, text="Templates",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        templates_label.pack(pady=(10, 5))
        
        # Login form template
        self.login_template_btn = ctk.CTkButton(
            templates_frame,
            text="Login Form",
            width=160,
            height=35,
            fg_color="#f59e0b",
            command=self.create_login_template
        )
        self.login_template_btn.pack(pady=5, padx=10)
        
        # Card template
        self.card_template_btn = ctk.CTkButton(
            templates_frame,
            text="Card Layout",
            width=160,
            height=35,
            fg_color="#06b6d4",
            command=self.create_card_template
        )
        self.card_template_btn.pack(pady=5, padx=10)
        
        # Bottom spacer
        bottom_spacer = ctk.CTkFrame(self, fg_color="transparent")
        bottom_spacer.pack(fill="both", expand=True)
    
    def add_component(self, component_type):
        """Add a component to the canvas"""
        # Calculate position to place component in center of visible area
        canvas_widget = self.main_window.design_canvas.canvas
        canvas_width = canvas_widget.winfo_width()
        canvas_height = canvas_widget.winfo_height()
        
        # Get scroll position
        scroll_x = canvas_widget.canvasx(canvas_width // 2)
        scroll_y = canvas_widget.canvasy(canvas_height // 2)
        
        # Add some randomness to avoid overlapping
        import random
        offset_x = random.randint(-50, 50)
        offset_y = random.randint(-50, 50)
        
        x = max(50, scroll_x + offset_x)
        y = max(50, scroll_y + offset_y)
        
        component = self.main_window.add_component(component_type)
        if component:
            component.set_position(x, y)
            component.draw(canvas_widget)
            self.main_window.select_component(component)
    
    def clear_canvas(self):
        """Clear all components from canvas"""
        from tkinter import messagebox
        
        if self.main_window.canvas_manager.components:
            result = messagebox.askyesno(
                "Clear Canvas",
                "Are you sure you want to clear all components from the canvas?"
            )
            if result:
                self.main_window.canvas_manager.clear_canvas()
                self.main_window.properties_panel.clear_selection()
                self.main_window.mark_modified()
    
    def select_all_components(self):
        """Select all components (for future multi-selection feature)"""
        # For now, just show a message
        from tkinter import messagebox
        messagebox.showinfo(
            "Select All",
            f"Total components: {len(self.main_window.canvas_manager.components)}"
        )
    
    def create_login_template(self):
        """Create a login form template"""
        canvas_manager = self.main_window.canvas_manager
        canvas_widget = self.main_window.design_canvas.canvas
        
        # Calculate center position
        canvas_width = canvas_widget.winfo_width()
        canvas_height = canvas_widget.winfo_height()
        center_x = canvas_widget.canvasx(canvas_width // 2)
        center_y = canvas_widget.canvasy(canvas_height // 2)
        
        # Create login form components
        form_x = center_x - 150
        form_y = center_y - 120
        
        # Background rectangle
        bg_rect = canvas_manager.add_component("rectangle", form_x - 20, form_y - 20)
        if bg_rect:
            bg_rect.resize(340, 280)
            bg_rect.fill_color = "#ffffff"
            bg_rect.border_color = "#e5e7eb"
            bg_rect.corner_radius = 8
            bg_rect.draw(canvas_widget)
        
        # Title
        title = canvas_manager.add_component("text", form_x + 120, form_y)
        if title:
            title.text = "Login"
            title.font_size = 24
            title.font_weight = "bold"
            title.text_color = "#1f2937"
            title.text_align = "center"
            title.resize(100, 40)
            title.draw(canvas_widget)
        
        # Email input
        email_label = canvas_manager.add_component("text", form_x, form_y + 50)
        if email_label:
            email_label.text = "Email"
            email_label.font_size = 14
            email_label.text_color = "#374151"
            email_label.resize(100, 25)
            email_label.draw(canvas_widget)
        
        email_input = canvas_manager.add_component("input", form_x, form_y + 75)
        if email_input:
            email_input.resize(300, 40)
            email_input.placeholder_text = "Enter your email"
            email_input.draw(canvas_widget)
        
        # Password input
        password_label = canvas_manager.add_component("text", form_x, form_y + 125)
        if password_label:
            password_label.text = "Password"
            password_label.font_size = 14
            password_label.text_color = "#374151"
            password_label.resize(100, 25)
            password_label.draw(canvas_widget)
        
        password_input = canvas_manager.add_component("input", form_x, form_y + 150)
        if password_input:
            password_input.resize(300, 40)
            password_input.placeholder_text = "Enter your password"
            password_input.draw(canvas_widget)
        
        # Login button
        login_btn = canvas_manager.add_component("button", form_x, form_y + 200)
        if login_btn:
            login_btn.text = "Sign In"
            login_btn.resize(300, 45)
            login_btn.fill_color = "#3b82f6"
            login_btn.text_color = "#ffffff"
            login_btn.font_weight = "bold"
            login_btn.draw(canvas_widget)
        
        self.main_window.mark_modified()
    
    def create_card_template(self):
        """Create a card layout template"""
        canvas_manager = self.main_window.canvas_manager
        canvas_widget = self.main_window.design_canvas.canvas
        
        # Calculate center position
        canvas_width = canvas_widget.winfo_width()
        canvas_height = canvas_widget.winfo_height()
        center_x = canvas_widget.canvasx(canvas_width // 2)
        center_y = canvas_widget.canvasy(canvas_height // 2)
        
        # Create card components
        card_x = center_x - 160
        card_y = center_y - 120
        
        # Card background
        card_bg = canvas_manager.add_component("rectangle", card_x, card_y)
        if card_bg:
            card_bg.resize(320, 240)
            card_bg.fill_color = "#ffffff"
            card_bg.border_color = "#e5e7eb"
            card_bg.corner_radius = 12
            card_bg.draw(canvas_widget)
        
        # Image placeholder
        image_placeholder = canvas_manager.add_component("rectangle", card_x + 20, card_y + 20)
        if image_placeholder:
            image_placeholder.resize(280, 120)
            image_placeholder.fill_color = "#f3f4f6"
            image_placeholder.border_color = "#d1d5db"
            image_placeholder.corner_radius = 8
            image_placeholder.draw(canvas_widget)
        
        # Image text
        image_text = canvas_manager.add_component("text", card_x + 160, card_y + 80)
        if image_text:
            image_text.text = "Image"
            image_text.font_size = 16
            image_text.text_color = "#9ca3af"
            image_text.text_align = "center"
            image_text.resize(80, 30)
            image_text.draw(canvas_widget)
        
        # Card title
        card_title = canvas_manager.add_component("text", card_x + 20, card_y + 160)
        if card_title:
            card_title.text = "Card Title"
            card_title.font_size = 18
            card_title.font_weight = "bold"
            card_title.text_color = "#1f2937"
            card_title.resize(200, 30)
            card_title.draw(canvas_widget)
        
        # Card description
        card_desc = canvas_manager.add_component("text", card_x + 20, card_y + 190)
        if card_desc:
            card_desc.text = "This is a description of the card content."
            card_desc.font_size = 14
            card_desc.text_color = "#6b7280"
            card_desc.resize(200, 25)
            card_desc.draw(canvas_widget)
        
        # Action button
        action_btn = canvas_manager.add_component("button", card_x + 220, card_y + 185)
        if action_btn:
            action_btn.text = "Action"
            action_btn.resize(80, 35)
            action_btn.fill_color = "#10b981"
            action_btn.text_color = "#ffffff"
            action_btn.font_size = 12
            action_btn.draw(canvas_widget)
        
        self.main_window.mark_modified()
