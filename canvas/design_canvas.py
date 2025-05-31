"""
Main design canvas for the UI wireframe designer
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas

class DesignCanvas(ctk.CTkFrame):
    """Main design canvas widget"""
    
    def __init__(self, parent, main_window):
        """Initialize the design canvas"""
        super().__init__(parent)
        
        self.main_window = main_window
        self.canvas_width = 800
        self.canvas_height = 600
        
        # Setup the canvas
        self.setup_canvas()
        self.setup_scrollbars()
        self.setup_bindings()
        
        # Drawing state
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_component = None
        self.is_resizing = False
        self.resize_handle = None
        
        # Grid settings
        self.grid_size = 20
        self.show_grid = True
        self.snap_to_grid = True
        
        # Zoom settings
        self.zoom_level = 1.0
        self.min_zoom = 0.25
        self.max_zoom = 4.0
        
        # Initial setup
        self.update_canvas_size()
        self.draw_grid()
    
    def setup_canvas(self):
        """Setup the main canvas widget"""
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create canvas
        self.canvas = Canvas(
            self,
            bg="#f8fafc",
            highlightthickness=0,
            scrollregion=(0, 0, self.canvas_width, self.canvas_height)
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
    
    def setup_scrollbars(self):
        """Setup scrollbars for the canvas"""
        # Vertical scrollbar
        self.v_scrollbar = ctk.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        
        # Horizontal scrollbar
        self.h_scrollbar = ctk.CTkScrollbar(
            self, orientation="horizontal", command=self.canvas.xview
        )
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)
    
    def setup_bindings(self):
        """Setup mouse and keyboard bindings"""
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        
        # Keyboard bindings
        self.canvas.bind("<Key>", self.on_key_press)
        self.canvas.focus_set()
    
    def on_click(self, event):
        """Handle mouse click events"""
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Check if clicking on a selection handle
        clicked_item = self.canvas.find_closest(canvas_x, canvas_y)[0]
        item_tags = self.canvas.gettags(clicked_item)
        
        if "selection_handle" in item_tags:
            # Get the component ID from the handle tags
            component_id = None
            for tag in item_tags:
                if tag not in ["selection_handle", "current"]:
                    component_id = tag
                    break
            
            if component_id:
                # Find the component with this ID
                for component in self.main_window.canvas_manager.components:
                    if hasattr(component, 'id') and component.id == component_id:
                        self.drag_component = component
                        self.is_resizing = True
                        self.resize_handle = clicked_item
                        self.drag_start_x = canvas_x
                        self.drag_start_y = canvas_y
                        return
        
        # Find component at click position
        component = self.main_window.canvas_manager.get_component_at_position(canvas_x, canvas_y)
        
        if component:
            # Check if Ctrl is held for multi-selection
            if event.state & 0x4:  # Ctrl key modifier
                # Multi-selection mode
                if component in self.main_window.canvas_manager.selected_components:
                    self.main_window.canvas_manager.remove_from_selection(component)
                else:
                    self.main_window.canvas_manager.add_to_selection(component)
                    if hasattr(self.main_window, 'properties_panel'):
                        self.main_window.properties_panel.update_selection(component)
            else:
                # Single selection mode
                self.main_window.canvas_manager.clear_multi_selection()
                self.main_window.select_component(component)
                self.is_dragging = True
                self.drag_component = component
                self.drag_start_x = canvas_x
                self.drag_start_y = canvas_y
        else:
            # Clear all selections
            self.main_window.canvas_manager.clear_selection()
            self.main_window.canvas_manager.clear_multi_selection()
            if hasattr(self.main_window, 'properties_panel'):
                self.main_window.properties_panel.clear_selection()
    
    def on_drag(self, event):
        """Handle mouse drag events"""
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        if self.is_resizing and self.resize_handle:
            self._handle_resize(canvas_x, canvas_y)
        elif self.is_dragging and self.drag_component:
            self._handle_component_drag(canvas_x, canvas_y)
    
    def on_release(self, event):
        """Handle mouse release events"""
        if self.is_dragging or self.is_resizing:
            # Mark as modified
            self.main_window.mark_modified()
        
        self.is_dragging = False
        self.is_resizing = False
        self.drag_component = None
        self.resize_handle = None
    
    def on_double_click(self, event):
        """Handle double-click events"""
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        component = self.main_window.canvas_manager.get_component_at_position(canvas_x, canvas_y)
        if component and hasattr(component, 'text'):
            # Open text editing dialog
            self._edit_component_text(component)
    
    def on_right_click(self, event):
        """Handle right-click context menu"""
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        component = self.main_window.canvas_manager.get_component_at_position(canvas_x, canvas_y)
        if component:
            self._show_context_menu(event, component)
    
    def on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming"""
        if event.state & 0x0004:  # Ctrl key pressed
            # Zoom in/out
            zoom_factor = 1.1 if event.delta > 0 else 0.9
            self.zoom(zoom_factor, event.x, event.y)
        else:
            # Scroll vertically
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def on_key_press(self, event):
        """Handle key press events"""
        if event.keysym == "Delete":
            self.main_window.delete_selected()
        elif event.keysym in ["Up", "Down", "Left", "Right"]:
            self._move_selected_component(event.keysym)
    
    def _handle_resize(self, canvas_x, canvas_y):
        """Handle component resizing"""
        if not self.drag_component:
            return
        
        component = self.drag_component
        dx = canvas_x - self.drag_start_x
        dy = canvas_y - self.drag_start_y
        
        # Simple resize from bottom-right corner
        new_width = max(20, component.width + dx)
        new_height = max(20, component.height + dy)
        
        # Apply grid snapping if enabled
        if self.snap_to_grid:
            grid_size = 20  # Use constant grid size for now
            new_width = round(new_width / grid_size) * grid_size
            new_height = round(new_height / grid_size) * grid_size
        
        # Apply changes
        component.resize(new_width, new_height)
        component.draw(self.canvas)
        
        # Update properties panel
        if hasattr(self.main_window, 'properties_panel'):
            self.main_window.properties_panel.update_selection(component)
        
        # Update drag start position for smooth resizing
        self.drag_start_x = canvas_x
        self.drag_start_y = canvas_y
    
    def _handle_component_drag(self, canvas_x, canvas_y):
        """Handle component dragging"""
        dx = canvas_x - self.drag_start_x
        dy = canvas_y - self.drag_start_y
        
        new_x = self.drag_component.x + dx
        new_y = self.drag_component.y + dy
        
        if self.snap_to_grid:
            new_x = round(new_x / self.grid_size) * self.grid_size
            new_y = round(new_y / self.grid_size) * self.grid_size
        
        self.drag_component.set_position(new_x, new_y)
        self.drag_component.draw(self.canvas)
        
        # Update properties panel
        self.main_window.properties_panel.update_selection(self.drag_component)
        
        self.drag_start_x = canvas_x
        self.drag_start_y = canvas_y
    
    def _move_selected_component(self, direction):
        """Move selected component with arrow keys"""
        component = self.main_window.canvas_manager.selected_component
        if not component:
            return
        
        step = self.grid_size if self.snap_to_grid else 5
        
        if direction == "Up":
            component.move(0, -step)
        elif direction == "Down":
            component.move(0, step)
        elif direction == "Left":
            component.move(-step, 0)
        elif direction == "Right":
            component.move(step, 0)
        
        component.draw(self.canvas)
        self.main_window.properties_panel.update_selection(component)
        self.main_window.mark_modified()
    
    def _edit_component_text(self, component):
        """Open text editing dialog for component"""
        from tkinter import simpledialog
        
        new_text = simpledialog.askstring(
            "Edit Text",
            "Enter new text:",
            initialvalue=component.text
        )
        
        if new_text is not None:
            component.text = new_text
            component.draw(self.canvas)
            self.main_window.properties_panel.update_selection(component)
            self.main_window.mark_modified()
    
    def _show_context_menu(self, event, component):
        """Show context menu for component"""
        context_menu = tk.Menu(self.canvas, tearoff=0)
        context_menu.add_command(
            label="Delete", 
            command=lambda: self.main_window.canvas_manager.delete_component(component)
        )
        context_menu.add_command(
            label="Duplicate", 
            command=lambda: self.main_window.canvas_manager.duplicate_component(component)
        )
        context_menu.add_separator()
        context_menu.add_command(
            label="Bring to Front", 
            command=lambda: self._bring_to_front(component)
        )
        context_menu.add_command(
            label="Send to Back", 
            command=lambda: self._send_to_back(component)
        )
        
        context_menu.tk_popup(event.x_root, event.y_root)
    
    def _bring_to_front(self, component):
        """Bring component to front"""
        # Redraw component last (on top)
        component.draw(self.canvas)
    
    def _send_to_back(self, component):
        """Send component to back"""
        # Move all canvas items to back
        for item_id in component.canvas_items:
            self.canvas.tag_lower(item_id)
    
    def draw_grid(self):
        """Draw grid on canvas"""
        if not self.show_grid:
            return
        
        self.canvas.delete("grid")
        
        grid_color = "#e2e8f0"
        
        # Draw vertical lines
        for x in range(0, self.canvas_width + 1, self.grid_size):
            self.canvas.create_line(
                x, 0, x, self.canvas_height,
                fill=grid_color, tags="grid"
            )
        
        # Draw horizontal lines
        for y in range(0, self.canvas_height + 1, self.grid_size):
            self.canvas.create_line(
                0, y, self.canvas_width, y,
                fill=grid_color, tags="grid"
            )
        
        # Move grid to back
        self.canvas.tag_lower("grid")
    
    def toggle_grid(self):
        """Toggle grid visibility"""
        self.show_grid = not self.show_grid
        if self.show_grid:
            self.draw_grid()
        else:
            self.canvas.delete("grid")
    
    def toggle_snap_to_grid(self):
        """Toggle snap to grid"""
        self.snap_to_grid = not self.snap_to_grid
    
    def zoom(self, factor, center_x=None, center_y=None):
        """Zoom the canvas"""
        new_zoom = self.zoom_level * factor
        new_zoom = max(self.min_zoom, min(self.max_zoom, new_zoom))
        
        if new_zoom != self.zoom_level:
            scale_factor = new_zoom / self.zoom_level
            self.zoom_level = new_zoom
            
            # Scale all canvas items
            if center_x is None:
                center_x = self.canvas.winfo_width() / 2
            if center_y is None:
                center_y = self.canvas.winfo_height() / 2
            
            self.canvas.scale("all", center_x, center_y, scale_factor, scale_factor)
            
            # Update scroll region
            self.update_canvas_size()
            self.draw_grid()
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        if self.zoom_level != 1.0:
            self.zoom(1.0 / self.zoom_level)
    
    def update_canvas_size(self):
        """Update canvas scroll region based on zoom"""
        scaled_width = int(self.canvas_width * self.zoom_level)
        scaled_height = int(self.canvas_height * self.zoom_level)
        self.canvas.configure(scrollregion=(0, 0, scaled_width, scaled_height))
    
    def clear(self):
        """Clear the canvas"""
        self.canvas.delete("all")
        self.draw_grid()
    
    def redraw_all_components(self):
        """Redraw all components on the canvas"""
        self.clear()
        for component in self.main_window.canvas_manager.components:
            component.draw(self.canvas)
