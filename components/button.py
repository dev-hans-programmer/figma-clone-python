"""
Button component implementation
"""

from .base_component import BaseComponent

class ButtonComponent(BaseComponent):
    """Button UI component"""
    
    def __init__(self, x=0, y=0, width=120, height=40):
        """Initialize button component"""
        super().__init__(x, y, width, height)
        self.fill_color = "#3b82f6"
        self.border_color = "#1e40af"
        self.text_color = "#ffffff"
        self.corner_radius = 6
        self.font_weight = "bold"
    
    def get_component_type(self):
        """Return component type"""
        return "button"
    
    def get_default_text(self):
        """Return default text"""
        return "Button"
    
    def draw(self, canvas):
        """Draw the button on canvas"""
        # Clear previous drawings
        self.delete_from_canvas(canvas)
        
        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.width, self.y + self.height
        
        # Draw button background
        if self.corner_radius > 0:
            # Draw rounded rectangle for button
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
        
        # Draw button text
        if self.text:
            cx = self.x + self.width // 2
            cy = self.y + self.height // 2
            
            font_style = f"{self.font_family} {self.font_size}"
            if self.font_weight == "bold":
                font_style += " bold"
            
            text_id = canvas.create_text(
                cx, cy,
                text=self.text,
                fill=self.text_color,
                font=font_style,
                anchor="center",
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
