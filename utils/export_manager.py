"""
Export manager for handling PNG and SVG export functionality
"""

import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
from xml.dom import minidom

class ExportManager:
    """Handles exporting designs to various formats"""
    
    def __init__(self):
        """Initialize export manager"""
        self.default_width = 800
        self.default_height = 600
        self.default_background = "#ffffff"
        self.export_quality = 95
        self.svg_precision = 2
    
    def export_png(self, canvas_widget, file_path, background_color=None):
        """Export canvas as PNG image"""
        try:
            # Get canvas dimensions and content
            canvas = canvas_widget.canvas
            
            # Update canvas to ensure all items are drawn
            canvas.update()
            
            # Get the bounding box of all items
            bbox = self._get_canvas_bbox(canvas)
            if not bbox:
                # If no items, use default size
                bbox = (0, 0, self.default_width, self.default_height)
            
            # Add padding
            padding = 20
            x1, y1, x2, y2 = bbox
            x1 -= padding
            y1 -= padding
            x2 += padding
            y2 += padding
            
            width = int(x2 - x1)
            height = int(y2 - y1)
            
            # Create PIL image
            bg_color = background_color or self.default_background
            image = Image.new("RGB", (width, height), bg_color)
            draw = ImageDraw.Draw(image)
            
            # Get all canvas items and draw them
            self._draw_canvas_items_to_image(canvas, draw, x1, y1)
            
            # Save the image
            image.save(file_path, "PNG", quality=self.export_quality, optimize=True)
            return True
            
        except Exception as e:
            raise Exception(f"Failed to export PNG: {str(e)}")
    
    def export_svg(self, design_data, file_path):
        """Export design as SVG"""
        try:
            components = design_data.get("components", [])
            
            if not components:
                # Create empty SVG
                bbox = (0, 0, self.default_width, self.default_height)
            else:
                # Calculate bounding box from components
                bbox = self._get_components_bbox(components)
            
            # Add padding
            padding = 20
            x1, y1, x2, y2 = bbox
            x1 -= padding
            y1 -= padding
            x2 += padding
            y2 += padding
            
            width = int(x2 - x1)
            height = int(y2 - y1)
            
            # Create SVG root element
            svg = ET.Element("svg")
            svg.set("xmlns", "http://www.w3.org/2000/svg")
            svg.set("width", str(width))
            svg.set("height", str(height))
            svg.set("viewBox", f"0 0 {width} {height}")
            
            # Add background
            bg_rect = ET.SubElement(svg, "rect")
            bg_rect.set("x", "0")
            bg_rect.set("y", "0")
            bg_rect.set("width", str(width))
            bg_rect.set("height", str(height))
            bg_rect.set("fill", self.default_background)
            
            # Convert components to SVG elements
            for component in components:
                self._component_to_svg(component, svg, x1, y1)
            
            # Write SVG to file
            self._write_svg_file(svg, file_path)
            return True
            
        except Exception as e:
            raise Exception(f"Failed to export SVG: {str(e)}")
    
    def _get_canvas_bbox(self, canvas):
        """Get bounding box of all canvas items"""
        try:
            # Get all items except grid
            items = [item for item in canvas.find_all() if "grid" not in canvas.gettags(item)]
            
            if not items:
                return None
            
            # Calculate overall bounding box
            min_x = min_y = float('inf')
            max_x = max_y = float('-inf')
            
            for item in items:
                bbox = canvas.bbox(item)
                if bbox:
                    x1, y1, x2, y2 = bbox
                    min_x = min(min_x, x1)
                    min_y = min(min_y, y1)
                    max_x = max(max_x, x2)
                    max_y = max(max_y, y2)
            
            if min_x == float('inf'):
                return None
                
            return (min_x, min_y, max_x, max_y)
            
        except Exception:
            return None
    
    def _get_components_bbox(self, components):
        """Get bounding box of all components"""
        if not components:
            return (0, 0, self.default_width, self.default_height)
        
        min_x = min(comp['x'] for comp in components)
        min_y = min(comp['y'] for comp in components)
        max_x = max(comp['x'] + comp['width'] for comp in components)
        max_y = max(comp['y'] + comp['height'] for comp in components)
        
        return (min_x, min_y, max_x, max_y)
    
    def _draw_canvas_items_to_image(self, canvas, draw, offset_x, offset_y):
        """Draw canvas items to PIL image"""
        # Get all items except grid and selection handles
        items = canvas.find_all()
        
        for item in items:
            tags = canvas.gettags(item)
            
            # Skip grid, selection handles, and borders
            if any(tag in tags for tag in ["grid", "selection_handle", "selection_border"]):
                continue
            
            item_type = canvas.type(item)
            
            try:
                if item_type == "rectangle":
                    self._draw_rectangle_to_image(canvas, item, draw, offset_x, offset_y)
                elif item_type == "text":
                    self._draw_text_to_image(canvas, item, draw, offset_x, offset_y)
                elif item_type == "arc":
                    self._draw_arc_to_image(canvas, item, draw, offset_x, offset_y)
                elif item_type == "line":
                    self._draw_line_to_image(canvas, item, draw, offset_x, offset_y)
            except Exception as e:
                print(f"Warning: Failed to draw item {item}: {e}")
                continue
    
    def _draw_rectangle_to_image(self, canvas, item, draw, offset_x, offset_y):
        """Draw rectangle item to PIL image"""
        coords = canvas.coords(item)
        if len(coords) >= 4:
            x1, y1, x2, y2 = coords[:4]
            x1 -= offset_x
            y1 -= offset_y
            x2 -= offset_x
            y2 -= offset_y
            
            # Get colors
            fill_color = canvas.itemcget(item, "fill") or None
            outline_color = canvas.itemcget(item, "outline") or None
            width = int(canvas.itemcget(item, "width") or 1)
            
            # Draw rectangle
            draw.rectangle(
                [(x1, y1), (x2, y2)],
                fill=fill_color,
                outline=outline_color,
                width=width
            )
    
    def _draw_text_to_image(self, canvas, item, draw, offset_x, offset_y):
        """Draw text item to PIL image"""
        coords = canvas.coords(item)
        if len(coords) >= 2:
            x, y = coords[:2]
            x -= offset_x
            y -= offset_y
            
            text = canvas.itemcget(item, "text")
            fill_color = canvas.itemcget(item, "fill") or "#000000"
            font_spec = canvas.itemcget(item, "font")
            
            # Parse font
            try:
                if font_spec:
                    font_parts = font_spec.split()
                    font_family = font_parts[0] if font_parts else "Arial"
                    font_size = int(font_parts[1]) if len(font_parts) > 1 else 12
                    font_weight = "bold" if "bold" in font_spec.lower() else "normal"
                else:
                    font_family = "Arial"
                    font_size = 12
                    font_weight = "normal"
                
                # Try to load font (fallback to default if not available)
                try:
                    if font_weight == "bold":
                        font = ImageFont.truetype(f"{font_family}-Bold.ttf", font_size)
                    else:
                        font = ImageFont.truetype(f"{font_family}.ttf", font_size)
                except:
                    try:
                        font = ImageFont.load_default()
                    except:
                        font = None
                
                draw.text((x, y), text, fill=fill_color, font=font)
                
            except Exception as e:
                # Fallback to basic text drawing
                draw.text((x, y), text, fill=fill_color)
    
    def _draw_arc_to_image(self, canvas, item, draw, offset_x, offset_y):
        """Draw arc item to PIL image (for rounded corners)"""
        coords = canvas.coords(item)
        if len(coords) >= 4:
            x1, y1, x2, y2 = coords[:4]
            x1 -= offset_x
            y1 -= offset_y
            x2 -= offset_x
            y2 -= offset_y
            
            fill_color = canvas.itemcget(item, "fill") or None
            outline_color = canvas.itemcget(item, "outline") or None
            
            # Draw as ellipse (simplified)
            draw.ellipse(
                [(x1, y1), (x2, y2)],
                fill=fill_color,
                outline=outline_color
            )
    
    def _draw_line_to_image(self, canvas, item, draw, offset_x, offset_y):
        """Draw line item to PIL image"""
        coords = canvas.coords(item)
        if len(coords) >= 4:
            # Adjust coordinates
            adjusted_coords = []
            for i in range(0, len(coords), 2):
                if i + 1 < len(coords):
                    x = coords[i] - offset_x
                    y = coords[i + 1] - offset_y
                    adjusted_coords.extend([x, y])
            
            if len(adjusted_coords) >= 4:
                fill_color = canvas.itemcget(item, "fill") or "#000000"
                width = int(canvas.itemcget(item, "width") or 1)
                
                draw.line(adjusted_coords, fill=fill_color, width=width)
    
    def _component_to_svg(self, component, svg_parent, offset_x, offset_y):
        """Convert a component to SVG element"""
        comp_type = component.get("type", "rectangle")
        x = component.get("x", 0) - offset_x
        y = component.get("y", 0) - offset_y
        width = component.get("width", 100)
        height = component.get("height", 50)
        
        if comp_type == "rectangle":
            self._create_svg_rectangle(svg_parent, component, x, y, width, height)
        elif comp_type == "button":
            self._create_svg_button(svg_parent, component, x, y, width, height)
        elif comp_type == "input":
            self._create_svg_input(svg_parent, component, x, y, width, height)
        elif comp_type == "text":
            self._create_svg_text(svg_parent, component, x, y, width, height)
    
    def _create_svg_rectangle(self, parent, component, x, y, width, height):
        """Create SVG rectangle element"""
        rect = ET.SubElement(parent, "rect")
        rect.set("x", str(round(x, self.svg_precision)))
        rect.set("y", str(round(y, self.svg_precision)))
        rect.set("width", str(round(width, self.svg_precision)))
        rect.set("height", str(round(height, self.svg_precision)))
        
        # Style attributes
        fill_color = component.get("fill_color", "#e5e7eb")
        border_color = component.get("border_color", "#6b7280")
        border_width = component.get("border_width", 2)
        corner_radius = component.get("corner_radius", 0)
        
        if fill_color:
            rect.set("fill", fill_color)
        if border_color and border_width > 0:
            rect.set("stroke", border_color)
            rect.set("stroke-width", str(border_width))
        if corner_radius > 0:
            rect.set("rx", str(corner_radius))
            rect.set("ry", str(corner_radius))
    
    def _create_svg_button(self, parent, component, x, y, width, height):
        """Create SVG button element"""
        # Button background
        self._create_svg_rectangle(parent, component, x, y, width, height)
        
        # Button text
        text = component.get("text", "Button")
        if text:
            text_elem = ET.SubElement(parent, "text")
            text_elem.set("x", str(round(x + width/2, self.svg_precision)))
            text_elem.set("y", str(round(y + height/2, self.svg_precision)))
            text_elem.set("text-anchor", "middle")
            text_elem.set("dominant-baseline", "central")
            
            # Text style
            text_color = component.get("text_color", "#ffffff")
            font_size = component.get("font_size", 12)
            font_weight = component.get("font_weight", "bold")
            font_family = component.get("font_family", "Arial")
            
            text_elem.set("fill", text_color)
            text_elem.set("font-size", str(font_size))
            text_elem.set("font-weight", font_weight)
            text_elem.set("font-family", font_family)
            text_elem.text = text
    
    def _create_svg_input(self, parent, component, x, y, width, height):
        """Create SVG input field element"""
        # Input background
        self._create_svg_rectangle(parent, component, x, y, width, height)
        
        # Input text or placeholder
        text = component.get("text") or component.get("placeholder_text", "")
        if text:
            text_elem = ET.SubElement(parent, "text")
            text_elem.set("x", str(round(x + 12, self.svg_precision)))  # Left padding
            text_elem.set("y", str(round(y + height/2, self.svg_precision)))
            text_elem.set("dominant-baseline", "central")
            
            # Text style
            if component.get("text"):
                text_color = component.get("text_color", "#374151")
            else:
                text_color = component.get("placeholder_color", "#9ca3af")
            
            font_size = component.get("font_size", 12)
            font_family = component.get("font_family", "Arial")
            
            text_elem.set("fill", text_color)
            text_elem.set("font-size", str(font_size))
            text_elem.set("font-family", font_family)
            text_elem.text = text
    
    def _create_svg_text(self, parent, component, x, y, width, height):
        """Create SVG text element"""
        text = component.get("text", "Text Label")
        if not text:
            return
        
        text_elem = ET.SubElement(parent, "text")
        
        # Position based on alignment
        text_align = component.get("text_align", "left")
        if text_align == "center":
            text_x = x + width/2
            text_elem.set("text-anchor", "middle")
        elif text_align == "right":
            text_x = x + width - 5
            text_elem.set("text-anchor", "end")
        else:  # left
            text_x = x + 5
            text_elem.set("text-anchor", "start")
        
        text_elem.set("x", str(round(text_x, self.svg_precision)))
        text_elem.set("y", str(round(y + height/2, self.svg_precision)))
        text_elem.set("dominant-baseline", "central")
        
        # Text style
        text_color = component.get("text_color", "#374151")
        font_size = component.get("font_size", 14)
        font_weight = component.get("font_weight", "normal")
        font_family = component.get("font_family", "Arial")
        
        text_elem.set("fill", text_color)
        text_elem.set("font-size", str(font_size))
        text_elem.set("font-weight", font_weight)
        text_elem.set("font-family", font_family)
        text_elem.text = text
    
    def _write_svg_file(self, svg_element, file_path):
        """Write SVG element to file with proper formatting"""
        # Convert to string with pretty formatting
        rough_string = ET.tostring(svg_element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Remove extra blank lines
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        pretty_xml = '\n'.join(lines)
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
    
    def export_pdf(self, design_data, file_path):
        """Export design as PDF (requires reportlab)"""
        try:
            # Try to import reportlab
            from reportlab.pdfgen import canvas as pdf_canvas
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.colors import HexColor
            
            components = design_data.get("components", [])
            
            if not components:
                bbox = (0, 0, self.default_width, self.default_height)
            else:
                bbox = self._get_components_bbox(components)
            
            # Create PDF
            c = pdf_canvas.Canvas(file_path, pagesize=A4)
            page_width, page_height = A4
            
            # Calculate scale to fit page
            content_width = bbox[2] - bbox[0]
            content_height = bbox[3] - bbox[1]
            
            scale_x = (page_width - 40) / content_width  # 20pt margin on each side
            scale_y = (page_height - 40) / content_height
            scale = min(scale_x, scale_y, 1.0)  # Don't scale up
            
            # Draw components
            for component in components:
                self._draw_component_to_pdf(c, component, bbox, scale, page_height)
            
            c.save()
            return True
            
        except ImportError:
            raise Exception("PDF export requires reportlab library. Install with: pip install reportlab")
        except Exception as e:
            raise Exception(f"Failed to export PDF: {str(e)}")
    
    def _draw_component_to_pdf(self, canvas, component, bbox, scale, page_height):
        """Draw component to PDF canvas"""
        # This is a simplified implementation
        # You would expand this for full PDF support
        x = (component.get("x", 0) - bbox[0]) * scale + 20
        y = page_height - ((component.get("y", 0) - bbox[1]) * scale + 20)
        width = component.get("width", 100) * scale
        height = component.get("height", 50) * scale
        
        comp_type = component.get("type", "rectangle")
        
        if comp_type in ["rectangle", "button", "input"]:
            # Draw rectangle
            fill_color = component.get("fill_color", "#ffffff")
            border_color = component.get("border_color", "#000000")
            
            try:
                canvas.setFillColor(HexColor(fill_color))
                canvas.setStrokeColor(HexColor(border_color))
            except:
                canvas.setFillColor("white")
                canvas.setStrokeColor("black")
            
            canvas.rect(x, y - height, width, height, fill=1, stroke=1)
        
        # Draw text if present
        text = component.get("text", "")
        if text:
            try:
                text_color = component.get("text_color", "#000000")
                canvas.setFillColor(HexColor(text_color))
            except:
                canvas.setFillColor("black")
            
            font_size = component.get("font_size", 12) * scale
            canvas.setFont("Helvetica", max(6, font_size))
            
            text_x = x + width/2
            text_y = y - height/2
            canvas.drawCentredText(text_x, text_y, text)
