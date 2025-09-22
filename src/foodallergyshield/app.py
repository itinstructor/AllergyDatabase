"""
The main application module for Food Allergy Shield.
"""
import os
import sys
from pathlib import Path

# Import from the local package
try:
    from .food_allergy_shield import AllergyDatabaseApp
except ImportError:
    # Fallback import if relative import fails
    from food_allergy_shield import AllergyDatabaseApp


def main():
    """
    The main entry point for the application.
    """
    app = AllergyDatabaseApp()
    return app


if __name__ == '__main__':
    app = main()
    app.run()