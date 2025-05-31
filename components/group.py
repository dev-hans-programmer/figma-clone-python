"""
Group component for organizing multiple components together
"""

from .base_component import BaseComponent
import uuid

class GroupComponent(BaseComponent):
    """Group component that contains multiple child components"""
    
    def __init__(self, components=None, x=0, y=0):
        """Initialize group component"""
        self.children = components or []
        
        # Calculate bounds from children
        if self.children:
            bounds = self._calculate_bounds()
            super().__init__(bounds[0], bounds[1], bounds[2], bounds[3])
        else:
            super().__init__(x, y, 100, 100)
        
        self.group_id = str(uuid.uuid4())
        self.is_group = True
    
    def get_component_type(self):
        """Return component type"""
        return "group"
    
    def get_default_text(self):
        """Return default text"""
        return f"Group ({len(self.children)} items)"
    
    def _calculate_bounds(self):
        """Calculate the bounding box of all child components"""
        if not self.children:
            return 0, 0, 100, 100
        
        min_x = min(child.x for child in self.children)
        min_y = min(child.y for child in self.children)
        max_x = max(child.x + child.width for child in self.children)
        max_y = max(child.y + child.height for child in self.children)
        
        return min_x, min_y, max_x - min_x, max_y - min_y
    
    def update_bounds(self):
        """Update group bounds based on children"""
        if self.children:
            bounds = self._calculate_bounds()
            self.x, self.y, self.width, self.height = bounds
    
    def add_child(self, component):
        """Add a component to the group"""
        if component not in self.children:
            self.children.append(component)
            component.parent_group = self
            self.update_bounds()
    
    def remove_child(self, component):
        """Remove a component from the group"""
        if component in self.children:
            self.children.remove(component)
            if hasattr(component, 'parent_group'):
                component.parent_group = None
            self.update_bounds()
    
    def draw(self, canvas):
        """Draw the group (just a selection outline when selected)"""
        # Clear previous canvas items
        for item_id in self.canvas_items:
            try:
                canvas.delete(item_id)
            except:
                pass
        self.canvas_items.clear()
        
        # Draw children first
        for child in self.children:
            child.draw(canvas)
        
        # Draw group selection if selected
        if self.selected:
            self._draw_selection_outline(canvas)
    
    def _draw_selection_outline(self, canvas):
        """Draw selection outline around the entire group"""
        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.width, self.y + self.height
        
        # Group selection border (dashed line)
        border_id = canvas.create_rectangle(
            x1 - 2, y1 - 2, x2 + 2, y2 + 2,
            fill="",
            outline="#10b981",
            width=2,
            dash=(5, 5),
            tags=("group_selection", self.id)
        )
        self.canvas_items.append(border_id)
        
        # Group handles (larger than individual component handles)
        handle_size = 8
        handles = [
            (x1 - handle_size//2, y1 - handle_size//2),  # Top-left
            (x2 - handle_size//2, y1 - handle_size//2),  # Top-right
            (x1 - handle_size//2, y2 - handle_size//2),  # Bottom-left
            (x2 - handle_size//2, y2 - handle_size//2),  # Bottom-right
        ]
        
        for hx, hy in handles:
            handle_id = canvas.create_rectangle(
                hx, hy, hx + handle_size, hy + handle_size,
                fill="#10b981",
                outline="white",
                width=2,
                tags=("selection_handle", self.id)
            )
            self.canvas_items.append(handle_id)
    
    def move(self, dx, dy):
        """Move the group and all its children"""
        # Move all children
        for child in self.children:
            child.move(dx, dy)
        
        # Update group position
        super().move(dx, dy)
    
    def resize(self, width, height):
        """Resize the group (scales all children proportionally)"""
        if not self.children or self.width == 0 or self.height == 0:
            return
        
        # Calculate scale factors
        scale_x = width / self.width
        scale_y = height / self.height
        
        # Store original group position
        group_x, group_y = self.x, self.y
        
        # Scale and reposition children
        for child in self.children:
            # Calculate relative position within group
            rel_x = (child.x - group_x) / self.width
            rel_y = (child.y - group_y) / self.height
            rel_w = child.width / self.width
            rel_h = child.height / self.height
            
            # Apply scaling
            new_x = group_x + rel_x * width
            new_y = group_y + rel_y * height
            new_w = rel_w * width
            new_h = rel_h * height
            
            child.set_position(new_x, new_y)
            child.resize(max(10, new_w), max(10, new_h))
        
        # Update group size
        self.width = width
        self.height = height
    
    def is_point_inside(self, x, y):
        """Check if point is inside any child component"""
        for child in self.children:
            if child.is_point_inside(x, y):
                return True
        return False
    
    def ungroup(self):
        """Ungroup and return the child components"""
        children = self.children.copy()
        for child in children:
            if hasattr(child, 'parent_group'):
                child.parent_group = None
        self.children.clear()
        return children
    
    def to_dict(self):
        """Convert group to dictionary for serialization"""
        data = super().to_dict()
        data.update({
            'group_id': self.group_id,
            'children': [child.to_dict() for child in self.children]
        })
        return data
    
    def from_dict(self, data):
        """Load group from dictionary"""
        super().from_dict(data)
        self.group_id = data.get('group_id', str(uuid.uuid4()))
        # Note: Children will be reconstructed by the canvas manager
    
    def clone(self):
        """Create a copy of the group with cloned children"""
        cloned_children = [child.clone() for child in self.children]
        cloned_group = GroupComponent(cloned_children, self.x + 20, self.y + 20)
        return cloned_group