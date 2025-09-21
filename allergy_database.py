import sqlite3
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
from kivy.lang import Builder

# ---------------------------------------------------------------------------
# Beginner-friendly overview
#
# This file implements a small Kivy application that stores food allergies
# in a local SQLite database. It uses Kivy's ScreenManager to show multiple
# screens (Main menu, Add entry, List entries, and Search). The user
# interface layout lives in `allergy_database.kv` (the KV language file)
# and the Python code implements the logic and database operations.
#
# Key concepts for beginners:
# - Screen: a 'page' of UI (like a window or view). We switch screens
#   using a ScreenManager.
# - ids: widgets defined in the KV file have ids accessible as `self.ids` in
#   the matching Screen instance. We sometimes cache them in on_kv_post.
# - Database: this app uses sqlite3 with a simple table called 'allergies'.
# - Popup: small message windows we use to show success or error messages.
#
# To run this app: open a terminal in the project folder and run
#    python allergy_database.py
#
# ---------------------------------------------------------------------------


class UIConfig:
    """Configuration class for platform-specific UI settings"""

    def __init__(self):
        self.is_mobile = platform in ("android", "ios")
        self.is_desktop = platform in ("win", "linux", "macosx")

        # Set window size for desktop
        if self.is_desktop:
            Window.size = (800, 600)
        # Timeout for success popups (seconds)
        self.success_popup_timeout = 2.5

    def get_popup_size(self):
        """Get appropriate popup size for platform"""
        if self.is_mobile:
            return (0.9, 0.7)
        return (0.6, 0.4)


class DatabaseManager:
    """Handles all database operations for the allergy database"""

    def __init__(self, db_name="allergies.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create the table with the new `source` column included. If the
        # database already exists without the column, we'll add it below.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS allergies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                allergen_name TEXT NOT NULL UNIQUE,
                danger_level INTEGER NOT NULL,
                symptoms TEXT,
                ingredients TEXT,
                source TEXT,
                notes TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        # Run a migration step: if the column 'source' is missing (older DB),
        # add it. SQLite's ALTER TABLE will append the column at the end.
        try:
            cursor.execute("PRAGMA table_info(allergies)")
            cols = [row[1] for row in cursor.fetchall()]
            if "source" not in cols:
                cursor.execute("ALTER TABLE allergies ADD COLUMN source TEXT")
                conn.commit()
        except Exception as e:
            # Migration should not block the app; log and continue.
            print(f"Database migration warning: {e}")

        conn.close()

    def add_allergy(
        self, allergen_name, danger_level, symptoms, ingredients, source, notes
    ):
        """Add a new allergy entry to the database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO allergies (allergen_name, danger_level, symptoms, ingredients, source, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (allergen_name, danger_level, symptoms, ingredients, source, notes),
            )

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding allergy: {e}")
            return False

    def get_all_allergies(self):
        """Retrieve all allergies from the database"""
        # Open a connection, run a simple SELECT, and return the results.
        # We order by danger_level descending so more dangerous items appear first,
        # then by allergen_name to make results predictable.
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Explicitly select columns in the preferred order so Python unpacking
        # remains stable even if the underlying DB column order differs.
        cursor.execute(
            "SELECT id, allergen_name, danger_level, symptoms, ingredients, source, notes, created_date "
            "FROM allergies ORDER BY danger_level DESC, allergen_name"
        )
        allergies = cursor.fetchall()

        conn.close()
        return allergies

    def search_allergies(self, search_term):
        """Search for allergies by allergen name or ingredients"""
        # Make the search case-insensitive by comparing lowercased values
        # and using SQL LIKE with wildcards around the search term.
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        search_term = f"%{search_term.lower()}%"
        cursor.execute(
            """
            SELECT * FROM allergies 
            WHERE LOWER(allergen_name) LIKE ? OR LOWER(ingredients) LIKE ?
            ORDER BY danger_level DESC, allergen_name
        """,
            (search_term, search_term),
        )

        allergies = cursor.fetchall()
        conn.close()
        return allergies

    def delete_allergy(self, allergy_id):
        """Delete an allergy entry by ID"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # Execute a simple DELETE statement for the given row id.
            cursor.execute("DELETE FROM allergies WHERE id = ?", (allergy_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting allergy: {e}")
            return False


class AllergyEntryScreen(Screen):
    """Screen for adding new allergy entries"""

    def on_kv_post(self, base_widget=None):
        # Attach KV ids after the KV is applied. Accepts optional base_widget
        try:
            self.allergen_input = self.ids.allergen_input
            self.danger_spinner = self.ids.danger_spinner
            self.symptoms_input = self.ids.symptoms_input
            self.ingredients_input = self.ids.ingredients_input
            self.source_input = self.ids.source_input
            self.notes_input = self.ids.notes_input
        except Exception:
            pass

    def add_allergy(self):
        app = App.get_running_app()
        allergen_name = self.ids.allergen_input.text.strip()
        danger_text = self.ids.danger_spinner.text
        symptoms = self.ids.symptoms_input.text.strip()
        ingredients = self.ids.ingredients_input.text.strip()
        source = self.ids.source_input.text.strip()
        notes = self.ids.notes_input.text.strip()

        if not allergen_name or danger_text == "Select Level":
            self.show_popup(
                "Error", "Please enter allergen name and select danger level."
            )
            return

        danger_level = int(danger_text.split(" - ")[0])
        success = app.db_manager.add_allergy(
            allergen_name, danger_level, symptoms, ingredients, source, notes
        )

        if success:
            self.show_popup(
                "Success", f'Allergy "{allergen_name}" added successfully!'
            )
            self.clear_form()
        else:
            self.show_popup(
                "Error",
                f'Allergen "{allergen_name}" already exists in the database.',
            )

    def clear_form(self):
        self.ids.allergen_input.text = ""
        self.ids.danger_spinner.text = "Select Level"
        self.ids.symptoms_input.text = ""
        self.ids.ingredients_input.text = ""
        self.ids.source_input.text = ""
        self.ids.notes_input.text = ""

    def go_back(self):
        self.manager.current = "main"

    def show_popup(self, title, message):
        app = App.get_running_app()
        popup_size = app.ui_config.get_popup_size()
        popup = Popup(
            title=title, content=Label(text=message), size_hint=popup_size
        )
        popup.open()
        # If this is a success message, auto-close the popup after a short
        # timeout so the user doesn't have to click to dismiss it. We use a
        # small try/except to avoid crashing if something unexpected happens.
        if title.lower().startswith("success"):
            try:
                Clock.schedule_once(
                    lambda dt: popup.dismiss(), app.ui_config.success_popup_timeout
                )
            except Exception:
                pass


class AllergyListScreen(Screen):
    """Screen for viewing and managing allergy entries"""

    def on_kv_post(self, base_widget=None):
        try:
            self.list_layout = self.ids.list_layout
        except Exception:
            pass

    def on_enter(self):
        """Called when screen is entered"""
        self.refresh_list()

    def refresh_list(self):
        app = App.get_running_app()
        self.ids.list_layout.clear_widgets()
        allergies = app.db_manager.get_all_allergies()

        if not allergies:
            no_data = Label(
                text="No allergies in database",
                size_hint_y=None,
                height=dp(40),
                font_size=sp(12),
            )
            self.ids.list_layout.add_widget(no_data)
            return

        for allergy in allergies:
            allergy_widget = self.create_allergy_widget(allergy)
            self.ids.list_layout.add_widget(allergy_widget)

    def create_allergy_widget(self, allergy):
        app = App.get_running_app()
        (
            allergy_id,
            name,
            danger_level,
            symptoms,
            ingredients,
            source,
            notes,
            created_date,
        ) = allergy

        # Choose sizes that look good on mobile (bigger touch targets)
        # and slightly smaller on desktop.
        widget_height = dp(140) if app.ui_config.is_mobile else dp(120)
        button_height = dp(60) if app.ui_config.is_mobile else dp(40)

        # container will hold the full allergy entry UI (header + details).
        # We set size_hint_y=None and a fixed height so the ScrollView can
        # calculate how tall the content is.
        container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=widget_height,
            spacing=dp(5),
        )

        # Header
        header = BoxLayout(size_hint_y=None, height=button_height)

        danger_colors = {
            1: [0.5, 1, 0.5, 1],
            2: [1, 1, 0.5, 1],
            3: [1, 0.7, 0.5, 1],
            4: [1, 0.5, 0.5, 1],
        }
        danger_texts = {
            1: "MILD",
            2: "MODERATE",
            3: "SEVERE",
            4: "LIFE-THREATENING",
        }

        name_label = Label(text=f"{name}", font_size=sp(14), bold=True)
        header.add_widget(name_label)

        button_width = dp(150) if app.ui_config.is_mobile else dp(200)

        danger_btn = Button(
            text=f"Level {danger_level}: {danger_texts[danger_level]}",
            size_hint_x=None,
            width=button_width,
            background_color=danger_colors[danger_level],
            font_size=sp(12),
            size_hint_y=None,
            height=button_height,
        )
        header.add_widget(danger_btn)

        delete_btn = Button(
            text="Delete",
            size_hint_x=None,
            width=dp(80),
            background_color=[1, 0.3, 0.3, 1],
            font_size=sp(12),
            size_hint_y=None,
            height=button_height,
        )
        # Bind the delete button to call delete_allergy with the specific
        # allergy id. We use a small lambda wrapper because bind passes the
        # button instance first; delete_allergy only needs the id.
        delete_btn.bind(on_press=lambda x: self.delete_allergy(allergy_id))
        header.add_widget(delete_btn)

        container.add_widget(header)

        # Details
        details = f'Symptoms: {symptoms or "None specified"}\n'
        details += f'Ingredients: {ingredients or "None specified"}'
        if source:
            details += f"\nSource: {source}"
        if notes:
            details += f"\nNotes: {notes}"

        details_height = widget_height - button_height - dp(10)
        details_label = Label(
            text=details,
            text_size=(None, None),
            valign="top",
            size_hint_y=None,
            height=details_height,
            font_size=sp(11),
        )
        container.add_widget(details_label)

        return container

    def delete_allergy(self, allergy_id):
        app = App.get_running_app()

        # confirm_delete is called when the user presses the 'Yes' button
        # in the confirmation dialog. It performs the delete and then
        # refreshes the list view.
        def confirm_delete(instance):
            if app.db_manager.delete_allergy(allergy_id):
                self.refresh_list()
                popup.dismiss()
            else:
                popup.dismiss()
                # Show an error popup if deletion failed for some reason.
                self.show_popup("Error", "Failed to delete allergy.")

        spacing = dp(15) if app.ui_config.is_mobile else dp(10)
        button_height = dp(60) if app.ui_config.is_mobile else dp(40)

        content = BoxLayout(orientation="vertical", spacing=spacing)
        content.add_widget(
            Label(
                text="Are you sure you want to delete this allergy?",
                font_size=sp(12),
            )
        )

        button_layout = BoxLayout(
            size_hint_y=None, height=button_height, spacing=spacing
        )

        yes_btn = Button(
            text="Yes",
            font_size=sp(14),
            size_hint_y=None,
            height=button_height,
            background_color=[1, 0.3, 0.3, 1],
        )
        yes_btn.bind(on_press=confirm_delete)
        button_layout.add_widget(yes_btn)

        no_btn = Button(
            text="No",
            font_size=sp(14),
            size_hint_y=None,
            height=button_height,
            background_color=[0.7, 0.7, 0.7, 1],
        )
        no_btn.bind(on_press=lambda x: popup.dismiss())
        button_layout.add_widget(no_btn)

        content.add_widget(button_layout)

        popup_size = app.ui_config.get_popup_size()
        popup = Popup(
            title="Confirm Delete", content=content, size_hint=popup_size
        )
        popup.open()

    def go_back(self):
        self.manager.current = "main"

    def show_popup(self, title, message):
        app = App.get_running_app()
        popup_size = app.ui_config.get_popup_size()
        popup = Popup(
            title=title, content=Label(text=message), size_hint=popup_size
        )
        popup.open()


class SearchScreen(Screen):
    """Screen for searching allergies by ingredients"""

    def on_kv_post(self, base_widget=None):
        try:
            self.search_input = self.ids.search_input
            self.results_layout = self.ids.results_layout
            self.results_label = self.ids.results_label
            try:
                self.search_input.bind(text=self.on_search_text_change)
            except Exception:
                pass
        except Exception:
            pass

    def on_search_text_change(self, instance, value):
        Clock.unschedule(self.delayed_search)
        if value.strip():
            Clock.schedule_once(self.delayed_search, 0.5)
        else:
            self.clear_results()

    def delayed_search(self, dt):
        self.search_allergies()

    def search_allergies(self):
        app = App.get_running_app()
        search_term = self.ids.search_input.text.strip()

        if not search_term:
            self.clear_results()
            return

        allergies = app.db_manager.search_allergies(search_term)
        self.display_results(allergies, search_term)

    def display_results(self, allergies, search_term):
        app = App.get_running_app()
        self.ids.results_layout.clear_widgets()

        if not allergies:
            self.ids.results_label.text = (
                f'No results found for "{search_term}"'
            )
            no_results = Label(
                text="No matching allergies found",
                size_hint_y=None,
                height=dp(40),
                font_size=sp(12),
            )
            self.ids.results_layout.add_widget(no_results)
            return

        self.ids.results_label.text = (
            f'Found {len(allergies)} result(s) for "{search_term}"'
        )

        for allergy in allergies:
            result_widget = self.create_search_result_widget(allergy)
            self.ids.results_layout.add_widget(result_widget)

    def create_search_result_widget(self, allergy):
        app = App.get_running_app()
        (
            allergy_id,
            name,
            danger_level,
            symptoms,
            ingredients,
            source,
            notes,
            created_date,
        ) = allergy

        # Each search result is a compact vertical box showing the name,
        # danger level, and brief details. We keep a fixed height so the
        # ScrollView can calculate the total content height.
        container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(100),
            spacing=dp(5),
        )

        # Header
        header = BoxLayout(size_hint_y=None, height=dp(30))

        danger_colors = {
            1: [0.5, 1, 0.5, 1],
            2: [1, 1, 0.5, 1],
            3: [1, 0.7, 0.5, 1],
            4: [1, 0.5, 0.5, 1],
        }
        danger_texts = {
            1: "MILD",
            2: "MODERATE",
            3: "SEVERE",
            4: "LIFE-THREATENING",
        }

        name_label = Label(text=f"{name}", font_size=sp(14), bold=True)
        header.add_widget(name_label)

        danger_label = Label(
            text=f"Level {danger_level}: {danger_texts[danger_level]}",
            color=danger_colors[danger_level],
            size_hint_x=None,
            width=dp(200),
            font_size=sp(12),
        )
        header.add_widget(danger_label)

        container.add_widget(header)

        # Details
        details = f'Ingredients: {ingredients or "None specified"}'
        if source:
            details += f"\nSource: {source}"
        if symptoms:
            details += f"\nSymptoms: {symptoms}"

        details_label = Label(
            text=details,
            text_size=(None, None),
            valign="top",
            size_hint_y=None,
            height=dp(65),
            font_size=sp(11),
        )
        container.add_widget(details_label)

        return container

    def clear_results(self):
        self.ids.results_layout.clear_widgets()
        self.ids.results_label.text = "Enter search term above"

    def go_back(self):
        self.manager.current = "main"


class MainScreen(Screen):
    """Main menu screen"""

    def on_kv_post(self, base_widget=None):
        # No ids to attach for now, but accept the call from KV
        return

    def go_to_add(self):
        self.manager.current = "add_allergy"

    def go_to_list(self):
        self.manager.current = "allergy_list"

    def go_to_search(self):
        self.manager.current = "search"

    def exit_app(self):
        App.get_running_app().stop()


class AllergyDatabaseApp(App):
    """Main application class using KV styling"""

    def build(self):
        # Initialize configuration and database
        self.ui_config = UIConfig()
        self.db_manager = DatabaseManager()

        # Create screen manager
        # Ensure KV UI is loaded.
        Builder.load_file("allergy_database.kv")
        sm = ScreenManager()

        # Add screens
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(AllergyEntryScreen(name="add_allergy"))
        sm.add_widget(AllergyListScreen(name="allergy_list"))
        sm.add_widget(SearchScreen(name="search"))

        return sm

    def on_start(self):
        """Called when the app starts"""
        if hasattr(Window, "set_title"):
            Window.set_title("Food Allergy Database")

    def on_pause(self):
        """Called when the app is paused (Android)"""
        return True

    def on_resume(self):
        """Called when the app is resumed (Android)"""
        pass


if __name__ == "__main__":
    AllergyDatabaseApp().run()
