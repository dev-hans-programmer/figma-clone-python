"""
Input field component implementation
"""

from .base_component import BaseComponent

class InputFieldComponent(BaseComponent):
    """Input field UI component"""
    
    def __init__(self, x=0, y=0, width=200, height=36):
        """Initialize input field component"""
        super().__init__(x, y, width, height)
        self.fill_color = "#ffffff"
        self.border_color = "#d1d5db"
        self.text_color = "#374151"
        self.corner_radius = 4
        self.placeholder_text = "Enter text..."
        self.placeholder_color = "#9ca3af"
    
    def get_component_type(self):
        """Return component type"""
        return "input"
    
    def get_default_text(self):
        """Return default text"""
        return ""
    
    def draw(self, canvas):
        """Draw the input field on canvas"""
        # Clear previous drawings
        self.delete_from_canvas(canvas)
        
        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.width, self.y + self.height
        
        # Draw input background
        if self.corner_radius > 0:
            # Draw rounded rectangle
            r = min(self.corner_radius, self.width // 2, self.height // 2)
            
            # Main rectangle
            rect_id = canvas.create_rectangle(
                x1 + r, y1, x2 - r, y2,
                fill=self.fill_color,
                outline=self.border_color,
                width=self.border_width,
                tags=("component", self.id)
            )
            self.canvas_items.append(rect_id)
            
            # Horizontal bars
            rect_id = canvas.create_rectangle(
                x1, y1 + r, x2, y2 - r,
                fill=self.fill_color,
                outline="",
                tags=("component", self.id)
            )
            self.canvas_items.append(rect_id)
            
            # Corner arcs
            corners = [
                (x1, y1, x1 + 2*r, y1 + 2*r, 90, 90),
                (x2 - 2*r, y1, x2, y1 + 2*r, 0, 90),
                (x1, y2 - 2*r, x1 + 2*r, y2, 180, 90),
                (x2 - 2*r, y2 - 2*r, x2, y2, 270, 90)
            ]
            
            for corner in corners:
                arc_id = canvas.create_arc(
                    corner[0], corner[1], corner[2], corner[3],
                    start=corner[4], extent=corner[5],
                    fill=self.fill_color,
                    outline=self.border_color,
                    width=self.border_width,
                    style="pieslice",
                    tags=("component", self.id)
                )
                self.canvas_items.append(arc_id)
        else:
            rect_id = canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=self.fill_color,
                outline=self.border_color,
                width=self.border_width,
                tags=("component", self.id)
            )
            self.canvas_items.append(rect_id)
        
        # Draw text or placeholder
        text_to_show = self.text if self.text else self.placeholder_text
        text_color = self.text_color if self.text else self.placeholder_color
        
        if text_to_show:
            # Left-aligned text with padding
            text_x = self.x + 12  # Left padding
            text_y = self.y + self.height // 2
            
            font_style = f"{self.font_family} {self.font_size}"
            
            text_id = canvas.create_text(
                text_x, text_y,
                text=text_to_show,
                fill=text_color,
                font=font_style,
                anchor="w",  # West (left) alignment
                tags=("component", self.id, "text")
            )
            self.canvas_items.append(text_id)
        
        # Draw cursor if has text (visual indicator)
        if self.text:
            cursor_x = self.x + 12 + len(self.text) * 7  # Approximate cursor position
            cursor_y1 = self.y + 8
            cursor_y2 = self.y + self.height - 8
            
            cursor_id = canvas.create_line(
                cursor_x, cursor_y1, cursor_x, cursor_y2,
                fill=self.text_color,
                width=1,
                tags=("component", self.id, "cursor")
            )
            self.canvas_items.append(cursor_id)
        
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
        
        # Selection border
        border_id = canvas.create_rectangle(
            x1 - 1, y1 - 1, x2 + 1, y2 + 1,
            fill="",
            outline="#2563eb",
            width=2,
            dash=(5, 5),
            tags=("selection_border", self.id)
        )
        self.canvas_items.append(border_id)
    
    def to_dict(self):
        """Convert component to dictionary"""
        data = super().to_dict()
        data['placeholder_text'] = self.placeholder_text
        data['placeholder_color'] = self.placeholder_color
        return data
    
    def from_dict(self, data):
        """Load component from dictionary"""
        super().from_dict(data)
        self.placeholder_text = data.get('placeholder_text', self.placeholder_text)
        self.placeholder_color = data.get('placeholder_color', self.placeholder_color)
