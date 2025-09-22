"""
The main entry point for the Food Allergy Shield application.
"""
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
    return AllergyDatabaseApp()


if __name__ == '__main__':
    app = main()
    app.run()