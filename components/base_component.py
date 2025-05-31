"""
Base component class for all UI elements
"""

import uuid
from abc import ABC, abstractmethod

class BaseComponent(ABC):
    """Base class for all UI components"""
    
    def __init__(self, x=0, y=0, width=100, height=50):
        """Initialize base component"""
        self.id = str(uuid.uuid4())
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False
        self.canvas_items = []  # Store tkinter canvas item IDs
        
        # Visual properties
        self.fill_color = "#3b82f6"
        self.border_color = "#1e40af"
        self.border_width = 2
        self.text_color = "#ffffff"
        self.font_family = "Arial"
        self.font_size = 12
        self.font_weight = "normal"
        
        # Component properties
        self.text = self.get_default_text()
        self.corner_radius = 0
        self.opacity = 1.0
        
    @abstractmethod
    def get_component_type(self):
        """Return the component type string"""
        pass
    
    @abstractmethod
    def get_default_text(self):
        """Return default text for the component"""
        pass
    
    @abstractmethod
    def draw(self, canvas):
        """Draw the component on the canvas"""
        pass
    
    def is_point_inside(self, x, y):
        """Check if a point is inside the component"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def move(self, dx, dy):
        """Move the component by the given offset"""
        self.x += dx
        self.y += dy
    
    def resize(self, width, height):
        """Resize the component"""
        self.width = max(10, width)  # Minimum width
        self.height = max(10, height)  # Minimum height
    
    def set_position(self, x, y):
        """Set the component position"""
        self.x = x
        self.y = y
    
    def get_bounds(self):
        """Get component bounds as (x, y, width, height)"""
        return (self.x, self.y, self.width, self.height)
    
    def get_center(self):
        """Get component center point"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def select(self):
        """Select the component"""
        self.selected = True
    
    def deselect(self):
        """Deselect the component"""
        self.selected = False
    
    def delete_from_canvas(self, canvas):
        """Remove component from canvas"""
        for item_id in self.canvas_items:
            canvas.delete(item_id)
        self.canvas_items.clear()
    
    def to_dict(self):
        """Convert component to dictionary for serialization"""
        return {
            'id': self.id,
            'type': self.get_component_type(),
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'text': self.text,
            'fill_color': self.fill_color,
            'border_color': self.border_color,
            'border_width': self.border_width,
            'text_color': self.text_color,
            'font_family': self.font_family,
            'font_size': self.font_size,
            'font_weight': self.font_weight,
            'corner_radius': self.corner_radius,
            'opacity': self.opacity
        }
    
    def from_dict(self, data):
        """Load component from dictionary"""
        self.id = data.get('id', self.id)
        self.x = data.get('x', self.x)
        self.y = data.get('y', self.y)
        self.width = data.get('width', self.width)
        self.height = data.get('height', self.height)
        self.text = data.get('text', self.text)
        self.fill_color = data.get('fill_color', self.fill_color)
        self.border_color = data.get('border_color', self.border_color)
        self.border_width = data.get('border_width', self.border_width)
        self.text_color = data.get('text_color', self.text_color)
        self.font_family = data.get('font_family', self.font_family)
        self.font_size = data.get('font_size', self.font_size)
        self.font_weight = data.get('font_weight', self.font_weight)
        self.corner_radius = data.get('corner_radius', self.corner_radius)
        self.opacity = data.get('opacity', self.opacity)
    
    def clone(self):
        """Create a copy of the component"""
        clone_data = self.to_dict()
        clone_data['id'] = str(uuid.uuid4())  # New ID for clone
        clone_data['x'] += 20  # Offset position
        clone_data['y'] += 20
        
        # Create new instance of the same type
        component_class = self.__class__
        clone = component_class()
        clone.from_dict(clone_data)
        return clone
