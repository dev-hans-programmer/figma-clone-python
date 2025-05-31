"""
Text label component implementation
"""

from .base_component import BaseComponent

class TextLabelComponent(BaseComponent):
    """Text label UI component"""
    
    def __init__(self, x=0, y=0, width=100, height=30):
        """Initialize text label component"""
        super().__init__(x, y, width, height)
        self.fill_color = ""  # Transparent background
        self.border_color = ""  # No border
        self.border_width = 0
        self.text_color = "#374151"
        self.font_size = 14
        self.text_align = "left"  # left, center, right
    
    def get_component_type(self):
        """Return component type"""
        return "text"
    
    def get_default_text(self):
        """Return default text"""
        return "Text Label"
    
    def draw(self, canvas):
        """Draw the text label on canvas"""
        # Clear previous drawings
        self.delete_from_canvas(canvas)
        
        # Draw background if fill color is set
        if self.fill_color:
            x1, y1 = self.x, self.y
            x2, y2 = self.x + self.width, self.y + self.height
            
            bg_id = canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=self.fill_color,
                outline=self.border_color if self.border_color else "",
                width=self.border_width,
                tags=("component", self.id, "background")
            )
            self.canvas_items.append(bg_id)
        
        # Draw text
        if self.text:
            # Calculate text position based on alignment
            if self.text_align == "center":
                text_x = self.x + self.width // 2
                anchor = "center"
            elif self.text_align == "right":
                text_x = self.x + self.width - 5  # Right padding
                anchor = "e"
            else:  # left
                text_x = self.x + 5  # Left padding
                anchor = "w"
            
            text_y = self.y + self.height // 2
            
            font_style = f"{self.font_family} {self.font_size}"
            if self.font_weight == "bold":
                font_style += " bold"
            
            text_id = canvas.create_text(
                text_x, text_y,
                text=self.text,
                fill=self.text_color,
                font=font_style,
                anchor=anchor,
                tags=("component", self.id, "text")
            )
            self.canvas_items.append(text_id)
        
        # Draw selection handles if selected
        if self.selected:
            self._draw_selection_handles(canvas)
    
    def _draw_selection_handles(self, canvas):
        """Draw selection handles around the component"""
        handle_size = 6
        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.width, self.y + self.height
        
        # Corner handles
        handles = [
            (x1 - handle_size//2, y1 - handle_size//2),
            (x2 - handle_size//2, y1 - handle_size//2),
            (x1 - handle_size//2, y2 - handle_size//2),
            (x2 - handle_size//2, y2 - handle_size//2),
        ]
        
        for hx, hy in handles:
            handle_id = canvas.create_rectangle(
                hx, hy, hx + handle_size, hy + handle_size,
                fill="white",
                outline="#2563eb",
                width=2,
                tags=("selection_handle", self.id)
            )
            self.canvas_items.append(handle_id)
        
        # Selection border (dotted line around text area)
        border_id = canvas.create_rectangle(
            x1 - 1, y1 - 1, x2 + 1, y2 + 1,
            fill="",
            outline="#2563eb",
            width=1,
            dash=(3, 3),
            tags=("selection_border", self.id)
        )
        self.canvas_items.append(border_id)
    
    def resize(self, width, height):
        """Resize the text component (adjust text area)"""
        # For text components, we might want to auto-adjust size based on content
        super().resize(width, height)
    
    def auto_resize_to_text(self, canvas):
        """Auto-resize the component to fit the text"""
        if self.text:
            # Create temporary text item to measure size
            temp_font = f"{self.font_family} {self.font_size}"
            if self.font_weight == "bold":
                temp_font += " bold"
            
            temp_id = canvas.create_text(
                0, 0, text=self.text, font=temp_font
            )
            bbox = canvas.bbox(temp_id)
            canvas.delete(temp_id)
            
            if bbox:
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Add padding
                self.width = text_width + 10
                self.height = text_height + 10
    
    def to_dict(self):
        """Convert component to dictionary"""
        data = super().to_dict()
        data['text_align'] = self.text_align
        return data
    
    def from_dict(self, data):
        """Load component from dictionary"""
        super().from_dict(data)
        self.text_align = data.get('text_align', self.text_align)
