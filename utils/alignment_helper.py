"""
Alignment helper utilities for component positioning and distribution
"""

import math

class AlignmentHelper:
    """Helper class for component alignment and distribution operations"""
    
    def __init__(self):
        """Initialize alignment helper"""
        self.snap_threshold = 10  # Pixels for snap-to-align
        self.grid_size = 20
    
    def align_components(self, components, alignment_type):
        """Align multiple components based on alignment type"""
        if len(components) < 2:
            return False
        
        if alignment_type == "left":
            return self._align_left(components)
        elif alignment_type == "right":
            return self._align_right(components)
        elif alignment_type == "top":
            return self._align_top(components)
        elif alignment_type == "bottom":
            return self._align_bottom(components)
        elif alignment_type == "center_horizontal":
            return self._align_center_horizontal(components)
        elif alignment_type == "center_vertical":
            return self._align_center_vertical(components)
        elif alignment_type == "center_both":
            return self._align_center_both(components)
        
        return False
    
    def _align_left(self, components):
        """Align components to the leftmost edge"""
        leftmost_x = min(comp.x for comp in components)
        for comp in components:
            comp.set_position(leftmost_x, comp.y)
        return True
    
    def _align_right(self, components):
        """Align components to the rightmost edge"""
        rightmost_x = max(comp.x + comp.width for comp in components)
        for comp in components:
            comp.set_position(rightmost_x - comp.width, comp.y)
        return True
    
    def _align_top(self, components):
        """Align components to the topmost edge"""
        topmost_y = min(comp.y for comp in components)
        for comp in components:
            comp.set_position(comp.x, topmost_y)
        return True
    
    def _align_bottom(self, components):
        """Align components to the bottommost edge"""
        bottommost_y = max(comp.y + comp.height for comp in components)
        for comp in components:
            comp.set_position(comp.x, bottommost_y - comp.height)
        return True
    
    def _align_center_horizontal(self, components):
        """Align components horizontally to their center"""
        # Find the average center X position
        center_x = sum(comp.x + comp.width // 2 for comp in components) / len(components)
        for comp in components:
            comp.set_position(center_x - comp.width // 2, comp.y)
        return True
    
    def _align_center_vertical(self, components):
        """Align components vertically to their center"""
        # Find the average center Y position
        center_y = sum(comp.y + comp.height // 2 for comp in components) / len(components)
        for comp in components:
            comp.set_position(comp.x, center_y - comp.height // 2)
        return True
    
    def _align_center_both(self, components):
        """Align components to both horizontal and vertical center"""
        self._align_center_horizontal(components)
        self._align_center_vertical(components)
        return True
    
    def distribute_components(self, components, distribution_type):
        """Distribute components evenly"""
        if len(components) < 3:
            return False
        
        if distribution_type == "horizontal":
            return self._distribute_horizontal(components)
        elif distribution_type == "vertical":
            return self._distribute_vertical(components)
        elif distribution_type == "horizontal_centers":
            return self._distribute_horizontal_centers(components)
        elif distribution_type == "vertical_centers":
            return self._distribute_vertical_centers(components)
        
        return False
    
    def _distribute_horizontal(self, components):
        """Distribute components horizontally with equal spacing"""
        # Sort by X position
        sorted_components = sorted(components, key=lambda c: c.x)
        
        first_comp = sorted_components[0]
        last_comp = sorted_components[-1]
        
        # Calculate total available space
        total_width = (last_comp.x + last_comp.width) - first_comp.x
        total_component_width = sum(comp.width for comp in sorted_components)
        available_space = total_width - total_component_width
        
        if len(sorted_components) <= 1:
            return False
        
        spacing = available_space / (len(sorted_components) - 1)
        
        # Position components
        current_x = first_comp.x
        for i, comp in enumerate(sorted_components):
            if i > 0:  # Don't move the first component
                comp.set_position(current_x, comp.y)
            current_x = comp.x + comp.width + spacing
        
        return True
    
    def _distribute_vertical(self, components):
        """Distribute components vertically with equal spacing"""
        # Sort by Y position
        sorted_components = sorted(components, key=lambda c: c.y)
        
        first_comp = sorted_components[0]
        last_comp = sorted_components[-1]
        
        # Calculate total available space
        total_height = (last_comp.y + last_comp.height) - first_comp.y
        total_component_height = sum(comp.height for comp in sorted_components)
        available_space = total_height - total_component_height
        
        if len(sorted_components) <= 1:
            return False
        
        spacing = available_space / (len(sorted_components) - 1)
        
        # Position components
        current_y = first_comp.y
        for i, comp in enumerate(sorted_components):
            if i > 0:  # Don't move the first component
                comp.set_position(comp.x, current_y)
            current_y = comp.y + comp.height + spacing
        
        return True
    
    def _distribute_horizontal_centers(self, components):
        """Distribute component centers horizontally"""
        # Sort by center X position
        sorted_components = sorted(components, key=lambda c: c.x + c.width // 2)
        
        first_center = sorted_components[0].x + sorted_components[0].width // 2
        last_center = sorted_components[-1].x + sorted_components[-1].width // 2
        
        total_distance = last_center - first_center
        
        if len(sorted_components) <= 1:
            return False
        
        spacing = total_distance / (len(sorted_components) - 1)
        
        # Position components
        for i, comp in enumerate(sorted_components[1:-1], 1):  # Skip first and last
            target_center_x = first_center + i * spacing
            new_x = target_center_x - comp.width // 2
            comp.set_position(new_x, comp.y)
        
        return True
    
    def _distribute_vertical_centers(self, components):
        """Distribute component centers vertically"""
        # Sort by center Y position
        sorted_components = sorted(components, key=lambda c: c.y + c.height // 2)
        
        first_center = sorted_components[0].y + sorted_components[0].height // 2
        last_center = sorted_components[-1].y + sorted_components[-1].height // 2
        
        total_distance = last_center - first_center
        
        if len(sorted_components) <= 1:
            return False
        
        spacing = total_distance / (len(sorted_components) - 1)
        
        # Position components
        for i, comp in enumerate(sorted_components[1:-1], 1):  # Skip first and last
            target_center_y = first_center + i * spacing
            new_y = target_center_y - comp.height // 2
            comp.set_position(comp.x, new_y)
        
        return True
    
    def snap_to_grid(self, component, grid_size=None):
        """Snap component position to grid"""
        if grid_size is None:
            grid_size = self.grid_size
        
        snapped_x = round(component.x / grid_size) * grid_size
        snapped_y = round(component.y / grid_size) * grid_size
        
        component.set_position(snapped_x, snapped_y)
        return True
    
    def snap_to_components(self, target_component, other_components, snap_distance=None):
        """Snap component to nearby components"""
        if snap_distance is None:
            snap_distance = self.snap_threshold
        
        target_bounds = target_component.get_bounds()
        tx, ty, tw, th = target_bounds
        
        snap_x = None
        snap_y = None
        
        for other in other_components:
            if other == target_component:
                continue
            
            other_bounds = other.get_bounds()
            ox, oy, ow, oh = other_bounds
            
            # Check for horizontal alignment opportunities
            # Left edges
            if abs(tx - ox) <= snap_distance:
                snap_x = ox
            # Right edges
            elif abs((tx + tw) - (ox + ow)) <= snap_distance:
                snap_x = (ox + ow) - tw
            # Left to right edge
            elif abs(tx - (ox + ow)) <= snap_distance:
                snap_x = ox + ow
            # Right to left edge
            elif abs((tx + tw) - ox) <= snap_distance:
                snap_x = ox - tw
            
            # Check for vertical alignment opportunities
            # Top edges
            if abs(ty - oy) <= snap_distance:
                snap_y = oy
            # Bottom edges
            elif abs((ty + th) - (oy + oh)) <= snap_distance:
                snap_y = (oy + oh) - th
            # Top to bottom edge
            elif abs(ty - (oy + oh)) <= snap_distance:
                snap_y = oy + oh
            # Bottom to top edge
            elif abs((ty + th) - oy) <= snap_distance:
                snap_y = oy - th
        
        # Apply snapping
        new_x = snap_x if snap_x is not None else tx
        new_y = snap_y if snap_y is not None else ty
        
        if snap_x is not None or snap_y is not None:
            target_component.set_position(new_x, new_y)
            return True
        
        return False
    
    def auto_arrange_components(self, components, arrangement_type="grid"):
        """Auto-arrange components in different layouts"""
        if not components:
            return False
        
        if arrangement_type == "grid":
            return self._arrange_grid(components)
        elif arrangement_type == "horizontal":
            return self._arrange_horizontal(components)
        elif arrangement_type == "vertical":
            return self._arrange_vertical(components)
        elif arrangement_type == "circle":
            return self._arrange_circle(components)
        
        return False
    
    def _arrange_grid(self, components, cols=None):
        """Arrange components in a grid layout"""
        if not components:
            return False
        
        # Calculate optimal number of columns
        if cols is None:
            cols = max(1, int(math.sqrt(len(components))))
        
        # Find the largest component for spacing
        max_width = max(comp.width for comp in components)
        max_height = max(comp.height for comp in components)
        
        spacing_x = max_width + 20
        spacing_y = max_height + 20
        
        # Starting position (top-left of first component or default)
        start_x = components[0].x if components else 100
        start_y = components[0].y if components else 100
        
        # Arrange components
        for i, comp in enumerate(components):
            row = i // cols
            col = i % cols
            
            new_x = start_x + col * spacing_x
            new_y = start_y + row * spacing_y
            
            comp.set_position(new_x, new_y)
        
        return True
    
    def _arrange_horizontal(self, components):
        """Arrange components horizontally"""
        if not components:
            return False
        
        # Sort by current Y position to maintain relative vertical order
        sorted_components = sorted(components, key=lambda c: c.x)
        
        spacing = 20
        current_x = sorted_components[0].x
        
        for comp in sorted_components:
            comp.set_position(current_x, comp.y)
            current_x += comp.width + spacing
        
        return True
    
    def _arrange_vertical(self, components):
        """Arrange components vertically"""
        if not components:
            return False
        
        # Sort by current X position to maintain relative horizontal order
        sorted_components = sorted(components, key=lambda c: c.y)
        
        spacing = 20
        current_y = sorted_components[0].y
        
        for comp in sorted_components:
            comp.set_position(comp.x, current_y)
            current_y += comp.height + spacing
        
        return True
    
    def _arrange_circle(self, components):
        """Arrange components in a circular pattern"""
        if not components:
            return False
        
        # Calculate center point
        center_x = sum(comp.x + comp.width // 2 for comp in components) / len(components)
        center_y = sum(comp.y + comp.height // 2 for comp in components) / len(components)
        
        # Calculate radius based on number of components
        radius = max(100, len(components) * 30)
        
        # Place components around the circle
        angle_step = 2 * math.pi / len(components)
        
        for i, comp in enumerate(components):
            angle = i * angle_step
            new_x = center_x + radius * math.cos(angle) - comp.width // 2
            new_y = center_y + radius * math.sin(angle) - comp.height // 2
            
            comp.set_position(new_x, new_y)
        
        return True
    
    def get_alignment_guides(self, target_component, other_components):
        """Get alignment guide lines for visual feedback"""
        if not target_component or not other_components:
            return []
        
        guides = []
        target_bounds = target_component.get_bounds()
        tx, ty, tw, th = target_bounds
        
        # Target component edges and center
        target_left = tx
        target_right = tx + tw
        target_top = ty
        target_bottom = ty + th
        target_center_x = tx + tw // 2
        target_center_y = ty + th // 2
        
        for other in other_components:
            if other == target_component:
                continue
            
            other_bounds = other.get_bounds()
            ox, oy, ow, oh = other_bounds
            
            # Other component edges and center
            other_left = ox
            other_right = ox + ow
            other_top = oy
            other_bottom = oy + oh
            other_center_x = ox + ow // 2
            other_center_y = oy + oh // 2
            
            # Vertical guides (for horizontal alignment)
            if abs(target_left - other_left) <= self.snap_threshold:
                guides.append({
                    'type': 'vertical',
                    'x': other_left,
                    'y1': min(target_top, other_top) - 10,
                    'y2': max(target_bottom, other_bottom) + 10,
                    'label': 'Left align'
                })
            
            if abs(target_right - other_right) <= self.snap_threshold:
                guides.append({
                    'type': 'vertical',
                    'x': other_right,
                    'y1': min(target_top, other_top) - 10,
                    'y2': max(target_bottom, other_bottom) + 10,
                    'label': 'Right align'
                })
            
            if abs(target_center_x - other_center_x) <= self.snap_threshold:
                guides.append({
                    'type': 'vertical',
                    'x': other_center_x,
                    'y1': min(target_top, other_top) - 10,
                    'y2': max(target_bottom, other_bottom) + 10,
                    'label': 'Center align'
                })
            
            # Horizontal guides (for vertical alignment)
            if abs(target_top - other_top) <= self.snap_threshold:
                guides.append({
                    'type': 'horizontal',
                    'y': other_top,
                    'x1': min(target_left, other_left) - 10,
                    'x2': max(target_right, other_right) + 10,
                    'label': 'Top align'
                })
            
            if abs(target_bottom - other_bottom) <= self.snap_threshold:
                guides.append({
                    'type': 'horizontal',
                    'y': other_bottom,
                    'x1': min(target_left, other_left) - 10,
                    'x2': max(target_right, other_right) + 10,
                    'label': 'Bottom align'
                })
            
            if abs(target_center_y - other_center_y) <= self.snap_threshold:
                guides.append({
                    'type': 'horizontal',
                    'y': other_center_y,
                    'x1': min(target_left, other_left) - 10,
                    'x2': max(target_right, other_right) + 10,
                    'label': 'Middle align'
                })
        
        return guides
