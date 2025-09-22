"""
The main entry point for the Food Allergy Shield application.
"""
# Import from the app module which now contains the main application
try:
    from .app import AllergyDatabaseApp
except ImportError:
    # Fallback import if relative import fails
    from app import AllergyDatabaseApp


def main():
    """
    The main entry point for the application.
    """
    return AllergyDatabaseApp()


if __name__ == '__main__':
    app = main()
    app.run()
    app.run()