"""
Rectangle component implementation
"""

from .base_component import BaseComponent

class RectangleComponent(BaseComponent):
    """Rectangle UI component"""
    
    def __init__(self, x=0, y=0, width=120, height=80):
        """Initialize rectangle component"""
        super().__init__(x, y, width, height)
        self.fill_color = "#e5e7eb"
        self.border_color = "#6b7280"
        self.corner_radius = 8
    
    def get_component_type(self):
        """Return component type"""
        return "rectangle"
    
    def get_default_text(self):
        """Return default text"""
        return ""
    
    def draw(self, canvas):
        """Draw the rectangle on canvas"""
        # Clear previous drawings
        self.delete_from_canvas(canvas)
        
        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.width, self.y + self.height
        
        # Draw main rectangle
        if self.corner_radius > 0:
            # Draw rounded rectangle using multiple canvas items
            r = min(self.corner_radius, self.width // 2, self.height // 2)
            
            # Main rectangle (without corners)
            rect_id = canvas.create_rectangle(
                x1 + r, y1, x2 - r, y2,
                fill=self.fill_color,
                outline=self.border_color,
                width=self.border_width,
                tags=("component", self.id)
            )
            self.canvas_items.append(rect_id)
            
            # Horizontal bars for rounded corners
            rect_id = canvas.create_rectangle(
                x1, y1 + r, x2, y2 - r,
                fill=self.fill_color,
                outline="",
                tags=("component", self.id)
            )
            self.canvas_items.append(rect_id)
            
            # Draw corner arcs
            corners = [
                (x1, y1, x1 + 2*r, y1 + 2*r, 90, 90),  # Top-left
                (x2 - 2*r, y1, x2, y1 + 2*r, 0, 90),   # Top-right
                (x1, y2 - 2*r, x1 + 2*r, y2, 180, 90), # Bottom-left
                (x2 - 2*r, y2 - 2*r, x2, y2, 270, 90)  # Bottom-right
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
            # Simple rectangle
            rect_id = canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=self.fill_color,
                outline=self.border_color,
                width=self.border_width,
                tags=("component", self.id)
            )
            self.canvas_items.append(rect_id)
        
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
            (x1 - handle_size//2, y1 - handle_size//2),  # Top-left
            (x2 - handle_size//2, y1 - handle_size//2),  # Top-right
            (x1 - handle_size//2, y2 - handle_size//2),  # Bottom-left
            (x2 - handle_size//2, y2 - handle_size//2),  # Bottom-right
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
