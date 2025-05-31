"""
Mini Figma - UI Wireframe Designer
Main entry point for the application
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main_window import MainWindow

def main():
    """Main entry point for the application"""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
