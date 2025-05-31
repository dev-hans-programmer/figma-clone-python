"""
Canvas manager for handling component operations
"""

from components.rectangle import RectangleComponent
from components.button import ButtonComponent
from components.input_field import InputFieldComponent
from components.text_label import TextLabelComponent
from components.group import GroupComponent

class CanvasManager:
    """Manages components on the design canvas"""
    
    def __init__(self):
        """Initialize canvas manager"""
        self.components = []
        self.selected_component = None
        self.selected_components = []  # For multi-selection
        self.canvas = None
        
        # Undo/Redo system
        self.history = []
        self.history_index = -1
        self.max_history = 50
        
        # Component factory
        self.component_classes = {
            'rectangle': RectangleComponent,
            'button': ButtonComponent,
            'input': InputFieldComponent,
            'text': TextLabelComponent,
            'group': GroupComponent
        }
    
    def set_canvas(self, canvas):
        """Set the design canvas reference"""
        self.canvas = canvas
    
    def add_component(self, component_type, x=100, y=100):
        """Add a new component to the canvas"""
        if component_type not in self.component_classes:
            return None
        
        # Save state for undo
        self._save_state()
        
        # Create component
        component_class = self.component_classes[component_type]
        component = component_class(x, y)
        
        # Add to components list
        self.components.append(component)
        
        # Draw on canvas
        if self.canvas:
            component.draw(self.canvas.canvas)
        
        return component
    
    def delete_component(self, component):
        """Delete a component from the canvas"""
        if component in self.components:
            # Save state for undo
            self._save_state()
            
            # Remove from canvas
            if self.canvas:
                component.delete_from_canvas(self.canvas.canvas)
            
            # Remove from components list
            self.components.remove(component)
            
            # Clear selection if this was selected
            if self.selected_component == component:
                self.selected_component = None
    
    def duplicate_component(self, component):
        """Duplicate a component"""
        if component in self.components:
            # Save state for undo
            self._save_state()
            
            # Create clone
            clone = component.clone()
            self.components.append(clone)
            
            # Draw on canvas
            if self.canvas:
                clone.draw(self.canvas.canvas)
            
            return clone
        return None
    
    def select_component(self, component):
        """Select a component"""
        # Deselect previous component
        if self.selected_component:
            self.selected_component.deselect()
            if self.canvas:
                self.selected_component.draw(self.canvas.canvas)
        
        # Select new component
        self.selected_component = component
        if component:
            component.select()
            if self.canvas:
                component.draw(self.canvas.canvas)
    
    def clear_selection(self):
        """Clear component selection"""
        if self.selected_component:
            self.selected_component.deselect()
            if self.canvas:
                self.selected_component.draw(self.canvas.canvas)
            self.selected_component = None
    
    def get_component_at_position(self, x, y):
        """Get component at the given position"""
        # Check components in reverse order (top to bottom)
        for component in reversed(self.components):
            if component.is_point_inside(x, y):
                return component
        return None
    
    def move_component(self, component, dx, dy):
        """Move a component by the given offset"""
        if component in self.components:
            component.move(dx, dy)
            if self.canvas:
                component.draw(self.canvas.canvas)
    
    def resize_component(self, component, width, height):
        """Resize a component"""
        if component in self.components:
            component.resize(width, height)
            if self.canvas:
                component.draw(self.canvas.canvas)
    
    def clear_canvas(self):
        """Clear all components from canvas"""
        # Save state for undo
        if self.components:
            self._save_state()
        
        # Clear components
        for component in self.components:
            if self.canvas:
                component.delete_from_canvas(self.canvas.canvas)
        
        self.components.clear()
        self.selected_component = None
    
    def get_design_data(self):
        """Get design data for saving"""
        return {
            'version': '1.0',
            'components': [component.to_dict() for component in self.components]
        }
    
    def load_design(self, design_data):
        """Load design from data"""
        # Clear current design
        self.clear_canvas()
        
        # Load components
        components_data = design_data.get('components', [])
        for comp_data in components_data:
            component_type = comp_data.get('type')
            if component_type in self.component_classes:
                component_class = self.component_classes[component_type]
                component = component_class()
                component.from_dict(comp_data)
                self.components.append(component)
                
                if self.canvas:
                    component.draw(self.canvas.canvas)
        
        # Clear history since we loaded a new design
        self.history.clear()
        self.history_index = -1
    
    def _save_state(self):
        """Save current state for undo system"""
        # Remove any states after current index
        self.history = self.history[:self.history_index + 1]
        
        # Add current state
        current_state = self.get_design_data()
        self.history.append(current_state)
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.history_index += 1
    
    def undo(self):
        """Undo the last action"""
        if self.history_index > 0:
            self.history_index -= 1
            state = self.history[self.history_index]
            self._restore_state(state)
    
    def redo(self):
        """Redo the last undone action"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            state = self.history[self.history_index]
            self._restore_state(state)
    
    def _restore_state(self, state):
        """Restore canvas to a previous state"""
        # Clear current components
        for component in self.components:
            if self.canvas:
                component.delete_from_canvas(self.canvas.canvas)
        
        self.components.clear()
        self.selected_component = None
        
        # Load state
        components_data = state.get('components', [])
        for comp_data in components_data:
            component_type = comp_data.get('type')
            if component_type in self.component_classes:
                component_class = self.component_classes[component_type]
                component = component_class()
                component.from_dict(comp_data)
                self.components.append(component)
                
                if self.canvas:
                    component.draw(self.canvas.canvas)
    
    def align_components(self, alignment_type):
        """Align selected components"""
        if len(self.components) < 2:
            return
        
        # Get all selected components (for now, just use all components)
        components_to_align = self.components.copy()
        
        if not components_to_align:
            return
        
        # Save state for undo
        self._save_state()
        
        if alignment_type == "left":
            leftmost_x = min(comp.x for comp in components_to_align)
            for comp in components_to_align:
                comp.set_position(leftmost_x, comp.y)
        
        elif alignment_type == "right":
            rightmost_x = max(comp.x + comp.width for comp in components_to_align)
            for comp in components_to_align:
                comp.set_position(rightmost_x - comp.width, comp.y)
        
        elif alignment_type == "top":
            topmost_y = min(comp.y for comp in components_to_align)
            for comp in components_to_align:
                comp.set_position(comp.x, topmost_y)
        
        elif alignment_type == "bottom":
            bottommost_y = max(comp.y + comp.height for comp in components_to_align)
            for comp in components_to_align:
                comp.set_position(comp.x, bottommost_y - comp.height)
        
        elif alignment_type == "center_horizontal":
            avg_x = sum(comp.x + comp.width // 2 for comp in components_to_align) // len(components_to_align)
            for comp in components_to_align:
                comp.set_position(avg_x - comp.width // 2, comp.y)
        
        elif alignment_type == "center_vertical":
            avg_y = sum(comp.y + comp.height // 2 for comp in components_to_align) // len(components_to_align)
            for comp in components_to_align:
                comp.set_position(comp.x, avg_y - comp.height // 2)
        
        # Redraw all components
        if self.canvas:
            for comp in components_to_align:
                comp.draw(self.canvas.canvas)
    
    def distribute_components(self, distribution_type):
        """Distribute components evenly"""
        if len(self.components) < 3:
            return
        
        # Save state for undo
        self._save_state()
        
        components_to_distribute = sorted(self.components, key=lambda c: c.x if distribution_type == "horizontal" else c.y)
        
        if distribution_type == "horizontal":
            first_x = components_to_distribute[0].x
            last_x = components_to_distribute[-1].x + components_to_distribute[-1].width
            total_width = last_x - first_x
            
            # Calculate spacing
            component_widths = sum(comp.width for comp in components_to_distribute)
            available_space = total_width - component_widths
            spacing = available_space / (len(components_to_distribute) - 1)
            
            # Position components
            current_x = first_x
            for comp in components_to_distribute:
                comp.set_position(current_x, comp.y)
                current_x += comp.width + spacing
        
        elif distribution_type == "vertical":
            first_y = components_to_distribute[0].y
            last_y = components_to_distribute[-1].y + components_to_distribute[-1].height
            total_height = last_y - first_y
            
            # Calculate spacing
            component_heights = sum(comp.height for comp in components_to_distribute)
            available_space = total_height - component_heights
            spacing = available_space / (len(components_to_distribute) - 1)
            
            # Position components
            current_y = first_y
            for comp in components_to_distribute:
                comp.set_position(comp.x, current_y)
                current_y += comp.height + spacing
        
        # Redraw all components
        if self.canvas:
            for comp in components_to_distribute:
                comp.draw(self.canvas.canvas)
    
    def add_to_selection(self, component):
        """Add a component to the multi-selection"""
        if component not in self.selected_components:
            self.selected_components.append(component)
            component.select()
    
    def remove_from_selection(self, component):
        """Remove a component from the multi-selection"""
        if component in self.selected_components:
            self.selected_components.remove(component)
            component.deselect()
    
    def clear_multi_selection(self):
        """Clear all multi-selected components"""
        for component in self.selected_components:
            component.deselect()
        self.selected_components.clear()
    
    def group_selected_components(self):
        """Group the currently selected components"""
        if len(self.selected_components) < 2:
            return None
        
        self._save_state()
        
        # Create group from selected components
        components_to_group = self.selected_components.copy()
        group = GroupComponent(components_to_group)
        
        # Remove individual components from main list
        for component in components_to_group:
            if component in self.components:
                self.components.remove(component)
        
        # Add group to components
        self.components.append(group)
        
        # Clear selection and select the new group
        self.clear_multi_selection()
        self.select_component(group)
        
        # Redraw canvas
        if self.canvas:
            self.canvas.redraw_all_components()
        
        return group
    
    def ungroup_component(self, group):
        """Ungroup a group component"""
        if not hasattr(group, 'is_group') or not group.is_group:
            return []
        
        self._save_state()
        
        # Get children before ungrouping
        children = group.ungroup()
        
        # Remove group from components
        if group in self.components:
            self.components.remove(group)
        
        # Add children back to components
        for child in children:
            self.components.append(child)
        
        # Clear selection
        self.clear_selection()
        
        # Redraw canvas
        if self.canvas:
            self.canvas.redraw_all_components()
        
        return children
    
    def is_component_grouped(self, component):
        """Check if a component is part of a group"""
        return hasattr(component, 'parent_group') and component.parent_group is not None
