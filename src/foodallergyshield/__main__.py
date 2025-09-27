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
    try:
        return AllergyDatabaseApp()
    except Exception as e:
        print(f"Error creating app: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    try:
        app = main()
        app.run()
    except Exception as e:
        print(f"Error running app: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")  # Keep console open to see errors