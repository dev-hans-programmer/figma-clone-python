"""
File management utilities for saving and loading designs
"""

import json
import os
from datetime import datetime

class FileManager:
    """Handles file operations for design data"""
    
    def __init__(self):
        """Initialize file manager"""
        self.default_extension = ".json"
        self.file_version = "1.0"
    
    def save_design(self, design_data, file_path):
        """Save design data to a JSON file"""
        try:
            # Add metadata
            save_data = {
                "metadata": {
                    "version": self.file_version,
                    "created_at": datetime.now().isoformat(),
                    "app_name": "Mini Figma - UI Wireframe Designer"
                },
                "design": design_data
            }
            
            # Ensure directory exists
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            raise Exception(f"Failed to save design: {str(e)}")
    
    def load_design(self, file_path):
        """Load design data from a JSON file"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different file formats
            if "design" in data:
                # New format with metadata
                design_data = data["design"]
                metadata = data.get("metadata", {})
                
                # Check version compatibility
                file_version = metadata.get("version", "1.0")
                if file_version != self.file_version:
                    print(f"Warning: File version {file_version} may not be fully compatible")
                
            else:
                # Legacy format - assume the entire file is design data
                design_data = data
            
            # Validate design data
            if not isinstance(design_data, dict):
                raise ValueError("Invalid design data format")
            
            if "components" not in design_data:
                design_data["components"] = []
            
            return design_data
            
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to load design: {str(e)}")
    
    def export_to_json(self, design_data, file_path):
        """Export design data as a clean JSON file (without metadata)"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(design_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise Exception(f"Failed to export JSON: {str(e)}")
    
    def get_recent_files(self, max_files=10):
        """Get list of recently used files (placeholder for future implementation)"""
        # This would typically read from a settings file or registry
        # For now, return empty list
        return []
    
    def add_to_recent_files(self, file_path):
        """Add file to recent files list (placeholder for future implementation)"""
        # This would typically update a settings file or registry
        pass
    
    def create_backup(self, design_data, original_file_path):
        """Create a backup of the design file"""
        try:
            if not original_file_path:
                return False
            
            # Create backup filename
            directory = os.path.dirname(original_file_path)
            filename = os.path.basename(original_file_path)
            name, ext = os.path.splitext(filename)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{name}_backup_{timestamp}{ext}"
            backup_path = os.path.join(directory, "backups", backup_filename)
            
            # Create backups directory if it doesn't exist
            backup_dir = os.path.dirname(backup_path)
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Save backup
            self.save_design(design_data, backup_path)
            return backup_path
            
        except Exception as e:
            print(f"Warning: Failed to create backup: {str(e)}")
            return False
    
    def validate_design_data(self, design_data):
        """Validate design data structure"""
        try:
            if not isinstance(design_data, dict):
                return False, "Design data must be a dictionary"
            
            if "components" not in design_data:
                return False, "Missing 'components' field"
            
            components = design_data["components"]
            if not isinstance(components, list):
                return False, "'components' must be a list"
            
            # Validate each component
            required_fields = ['id', 'type', 'x', 'y', 'width', 'height']
            valid_types = ['rectangle', 'button', 'input', 'text']
            
            for i, component in enumerate(components):
                if not isinstance(component, dict):
                    return False, f"Component {i} must be a dictionary"
                
                # Check required fields
                for field in required_fields:
                    if field not in component:
                        return False, f"Component {i} missing required field '{field}'"
                
                # Check component type
                if component['type'] not in valid_types:
                    return False, f"Component {i} has invalid type '{component['type']}'"
                
                # Check numeric fields
                numeric_fields = ['x', 'y', 'width', 'height']
                for field in numeric_fields:
                    if not isinstance(component[field], (int, float)):
                        return False, f"Component {i} field '{field}' must be numeric"
            
            return True, "Valid design data"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def get_file_info(self, file_path):
        """Get information about a design file"""
        try:
            if not os.path.exists(file_path):
                return None
            
            # Get file stats
            stat = os.stat(file_path)
            
            # Try to load and analyze the file
            design_data = self.load_design(file_path)
            component_count = len(design_data.get("components", []))
            
            # Count components by type
            component_types = {}
            for component in design_data.get("components", []):
                comp_type = component.get("type", "unknown")
                component_types[comp_type] = component_types.get(comp_type, 0) + 1
            
            return {
                "file_path": file_path,
                "file_size": stat.st_size,
                "modified_time": datetime.fromtimestamp(stat.st_mtime),
                "component_count": component_count,
                "component_types": component_types,
                "is_valid": True
            }
            
        except Exception as e:
            return {
                "file_path": file_path,
                "error": str(e),
                "is_valid": False
            }
