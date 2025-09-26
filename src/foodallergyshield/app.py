"""
Allergy Database — a small Kivy app for beginners

This module implements a simple cross-platform application that stores
food allergy information in a local SQLite database. The goal of this
walkthrough is to give a plain-language overview so beginners can
quickly understand how the app is organized and how the pieces fit.

High-level flow (plain language):
- The program starts by creating an App object (AllergyDatabaseApp).
- The app loads the UI layout from `food_allergy_shield.kv` which defines
    the visual screens (Main, Add, List, Search).
- When the user adds data in the Add screen, the UI code reads the
    form inputs and calls the DatabaseManager to insert or update rows.
- The List screen asks the DatabaseManager for all rows and builds a
    scrollable list the user can edit or delete.
- The Search screen asks the DatabaseManager for matching rows and
    shows compact results.

Files of interest:
- `food_allergy_shield.kv` — the visual layout (buttons, forms, ids).
- `database_manager.py` — the database logic (CRUD operations).
- `app.py` — ties UI and database together and contains
    the Screen classes used by the GUI.

Run locally:
        python -m foodallergyshield

Data shapes (what gets passed around)
------------------------------------
- Allergy row (tuple returned by DatabaseManager queries):
    (id, allergen_name, danger_level, symptoms, ingredients, source, notes, created_date)
    - id: int (primary key assigned by SQLite)
    - allergen_name: str (name of the allergen, UNIQUE)
    - danger_level: int (1-4 scale where 4 is most dangerous)
    - symptoms: str (free text describing symptoms)
    - ingredients: str (common ingredients that may contain the allergen)
    - source: str (where the info came from, e.g., 'Doctor', 'Label')
    - notes: str (additional notes)
    - created_date: timestamp (when the row was inserted)

DatabaseManager methods (inputs and outputs)
-------------------------------------------
- DatabaseManager(db_name: str = 'allergies.db')
    - creates/uses the given SQLite file to store allergy rows.

- add_allergy(allergen_name: str, danger_level: int, symptoms: str,
    ingredients: str, source: str, notes: str) -> bool
    - Inserts a new allergy row. Returns True on success, False on failure
        (for example if the allergen_name already exists).

- get_all_allergies() -> list[tuple]
    - Returns a list of allergy rows (see row shape above).

- get_allergy(allergy_id: int) -> tuple | None
    - Returns a single row for the given id, or None if not found.

- update_allergy(allergy_id: int, allergen_name: str, danger_level: int,
    symptoms: str, ingredients: str, source: str, notes: str) -> bool
    - Updates the row with the given id. Returns True if update succeeded.

- search_allergies(search_term: str) -> list[tuple]
    - Case-insensitive search against allergen_name and ingredients.

- delete_allergy(allergy_id: int) -> bool
    - Deletes the row with the id; returns True on success.

How the UI and database connect
-------------------------------
- The Screen classes (AllergyEntryScreen, AllergyListScreen, SearchScreen)
    call DatabaseManager methods when the user performs actions.
- For example, AllergyEntryScreen.add_allergy() reads form fields and
    calls add_allergy() or update_allergy() depending on whether the
    user is creating a new row or editing an existing one.

Food Allergy Shield - Main application file for Briefcase packaging.

This module implements a simple cross-platform application that stores
food allergy information in a local SQLite database. The goal of this
walkthrough is to give a plain-language overview so beginners can
quickly understand how the app is organized and how the pieces fit.

High-level flow (plain language):
- The program starts by creating an App object (AllergyDatabaseApp).
- The app loads the UI layout from `food_allergy_shield.kv` which defines
    the visual screens (Main, Add, List, Search).
- When the user adds data in the Add screen, the UI code reads the
    form inputs and calls the DatabaseManager to insert or update rows.
- The List screen asks the DatabaseManager for all rows and builds a
    scrollable list the user can edit or delete.
- The Search screen asks the DatabaseManager for matching rows and
    shows compact results.

Files of interest:
- `food_allergy_shield.kv` — the visual layout (buttons, forms, ids).
- `database_manager.py` — the database logic (CRUD operations).
- `app.py` — ties UI and database together and contains
    the Screen classes used by the GUI.
"""

import csv
import os
from pathlib import Path

# pip install kivy
# Kivy imports: these provide UI widgets and app lifecycle functions
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
from kivy.properties import BooleanProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.checkbox import CheckBox
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

# Import the refactored DatabaseManager from its own module
try:
    from .database_manager import DatabaseManager
except ImportError:
    from database_manager import DatabaseManager


class UIConfig:
    """Small helper to store UI settings that depend on platform.

    This keeps UI values (like whether we're on mobile) in one place so
    other code can read them instead of checking `platform` everywhere.
    """

    def __init__(self):
        # Detect whether we are running on a mobile platform.
        self.is_mobile = platform in ("android", "ios")
        # Detect common desktop platforms.
        self.is_desktop = platform in ("win", "linux", "macosx")

        # If we're on desktop, set a reasonable window size for testing.
        if self.is_desktop:
            Window.size = (800, 600)

        # How long to show success popups before auto-dismissing (seconds).
        self.success_popup_timeout = 2.5

    def get_popup_size(self):
        """Return a size_hint tuple appropriate for popups.

        The returned tuple is suitable for Kivy's `size_hint` property.

        Returns:
            tuple: (width_hint: float, height_hint: float)
        """
        # Mobile devices benefit from larger popups so they are easy to
        # read and press; desktop can be smaller.
        if self.is_mobile:
            return (0.9, 0.7)
        return (0.6, 0.4)


# ---------------------------------------------------------------------------
# Shared UI Helper
# ---------------------------------------------------------------------------
def build_allergy_row(
    *,
    context: str,
    app,
    allergy_tuple,
    row_index: int,
    is_mobile: bool,
    show_edit_delete: bool = False,
    on_edit=None,
    on_delete=None,
    preview_mode: str = "symptoms_first",
):
    """Build a dynamic allergy/search row widget used by list & search screens.

    Parameters:
        context (str): 'list' or 'search' (affects which fields emphasized).
        app (App): Running Kivy app (provides ui_config).
        allergy_tuple (tuple): Row from DB.
        row_index (int): Index for striping.
        is_mobile (bool): Layout sizing toggle.
        show_edit_delete (bool): Whether to include Edit/Delete buttons.
        on_edit (callable|None): Callback receiving allergy_id when Edit pressed.
        on_delete (callable|None): Callback receiving allergy_id when Delete pressed.
        preview_mode (str): 'symptoms_first' or 'ingredients_first'.

    Returns:
        BoxLayout: Fully configured container.
    """
    (
        allergy_id,
        name,
        danger_level,
        symptoms,
        ingredients,
        source,
        notes,
        created_date,
    ) = allergy_tuple

    header_h = (
        dp(56)
        if is_mobile and context == "list"
        else (
            dp(50) if is_mobile else (dp(40) if context == "list" else dp(38))
        )
    )
    body_font = sp(11)

    container = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        spacing=dp(4),
        size_hint_x=1,
        padding=(dp(6), dp(4)),
    )

    # Background & danger bar
    level_colors = {
        1: (0.4, 0.9, 0.4, 1),
        2: (0.95, 0.95, 0.4, 1),
        3: (1, 0.65, 0.35, 1),
        4: (1, 0.35, 0.35, 1),
    }
    with container.canvas.before:
        Color(rgba=(1, 1, 1, 0.06) if row_index % 2 == 0 else (1, 1, 1, 0.12))
        bg = RoundedRectangle(
            radius=[dp(6)], pos=container.pos, size=container.size
        )
        Color(rgba=level_colors.get(danger_level, (0.7, 0.7, 0.7, 1)))
        bar = RoundedRectangle(
            radius=[dp(4)],
            pos=(container.x, container.y),
            size=(dp(6), container.height),
        )

    def _update_bg(*_):
        bg.pos = container.pos
        bg.size = container.size
        bar.pos = (container.x, container.y)
        bar.size = (dp(6), container.height)

    container.bind(pos=_update_bg, size=_update_bg)

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

    header = BoxLayout(
        orientation="horizontal",
        size_hint_y=None,
        height=header_h,
        spacing=dp(6),
    )

    name_label = Label(
        text=name,
        font_size=sp(14),
        bold=True,
        halign="left",
        valign="middle",
        size_hint_x=1,
    )
    name_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))  # type: ignore[attr-defined]
    header.add_widget(name_label)

    # Danger badge shorter for search context
    if context == "list":
        badge_text = f"Level {danger_level}: {danger_texts[danger_level]}"
        badge_width = dp(140) if is_mobile else dp(160)
    else:
        badge_text = f"Lvl {danger_level}"
        badge_width = dp(70)
    danger_badge = Button(
        text=badge_text,
        size_hint=(None, None),
        width=badge_width,
        height=header_h,
        background_color=danger_colors[danger_level],
        font_size=sp(12 if context == "list" else 11),
    )
    header.add_widget(danger_badge)

    # Optional Edit/Delete
    if show_edit_delete:
        delete_btn = Button(
            text="Delete",
            size_hint=(None, None),
            width=dp(70),
            height=header_h,
            background_color=[1, 0.3, 0.3, 1],
            font_size=sp(12),
        )
        if on_delete:
            delete_btn.bind(on_press=lambda _x: on_delete(allergy_id))  # type: ignore[attr-defined]
        header.add_widget(delete_btn)

        edit_btn = Button(
            text="Edit",
            size_hint=(None, None),
            width=dp(70),
            height=header_h,
            background_color=[0.3, 0.6, 1, 1],
            font_size=sp(12),
        )
        if on_edit:
            edit_btn.bind(on_press=lambda _x: on_edit(allergy_id))  # type: ignore[attr-defined]
        header.add_widget(edit_btn)

    toggle_btn = Button(
        text="More",
        size_hint=(None, None),
        width=dp(70),
        height=header_h,
        font_size=sp(12),
    )
    header.add_widget(toggle_btn)
    container.add_widget(header)

    # Build lines
    if preview_mode == "symptoms_first":
        parts_full = [
            f'Symptoms: {symptoms or "None specified"}',
            f'Ingredients: {ingredients or "None specified"}',
        ]
    else:
        parts_full = [f'Ingredients: {ingredients or "None specified"}']
        if symptoms:
            parts_full.append(f"Symptoms: {symptoms}")
    if source:
        parts_full.append(f"Source: {source}")
    if notes:
        parts_full.append(f"Notes: {notes}")
    full_text = "\n".join(parts_full)
    preview_text = parts_full[0]

    details_label = Label(
        text=preview_text,
        font_size=body_font,
        halign="left",
        valign="top",
        size_hint_y=None,
    )

    def _layout_details(*_):
        avail_w = max(10, container.width - dp(12))
        details_label.text_size = (avail_w, None)
        details_label.texture_update()
        details_label.height = details_label.texture_size[1]
        container.height = header.height + details_label.height + dp(12)

    details_label.bind(texture_size=lambda *a: _layout_details())  # type: ignore[attr-defined]
    container.bind(width=lambda *a: _layout_details())
    container.add_widget(details_label)

    state = {"expanded": False}

    def toggle_row(_btn):
        state["expanded"] = not state["expanded"]
        if state["expanded"]:
            details_label.text = full_text
            toggle_btn.text = "Less"
        else:
            details_label.text = preview_text
            toggle_btn.text = "More"
        _layout_details()

    toggle_btn.bind(on_press=toggle_row)  # type: ignore[attr-defined]

    container.height = header_h + dp(50)
    return container


# ---------------------------------------------------------------------------
# Screen Classes
# ---------------------------------------------------------------------------
class MainScreen(Screen):
    """Main menu screen"""

    def on_kv_post(self, base_widget=None):
        """Accept the KV lifecycle call; no ids to cache on the main screen.

        Parameters:
            base_widget (Widget|None): Root widget passed by Kivy's lifecycle.

        Returns:
            None
        """
        return

    def go_to_add(self):
        """Switch to the Add Allergy screen.

        Returns:
            None
        """
        self.manager.current = "add_allergy"

    def go_to_list(self):
        self.manager.current = "allergy_list"

    def go_to_search(self):
        self.manager.current = "search"

    def go_to_maintenance(self):
        self.manager.current = "maintenance"

    def exit_app(self):
        App.get_running_app().stop()


class DatabaseMaintenanceScreen(Screen):

    def export_csv(self):
        app = App.get_running_app()  # type: ignore[attr-defined]

        # Layout: [filename row], [buttons]
        content = BoxLayout(
            orientation="vertical", spacing=dp(10), padding=dp(10)
        )

        # Row for filename input
        filename_row = BoxLayout(
            size_hint_y=None, height=dp(40), spacing=dp(10)
        )
        filename_row.add_widget(
            Label(text="File name:", size_hint_x=None, width=dp(100))
        )
        filename_input = TextInput(
            text="allergies_export", multiline=False, size_hint_x=1
        )
        filename_row.add_widget(filename_input)
        content.add_widget(filename_row)

        btn_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        export_btn = Button(
            text="Export",
            background_color=(0.3, 0.8, 0.3, 1),
            size_hint_x=None,
            width=dp(120),
        )
        cancel_btn = Button(
            text="Cancel",
            background_color=(0.7, 0.7, 0.7, 1),
            size_hint_x=None,
            width=dp(120),
        )
        btn_row.add_widget(export_btn)
        btn_row.add_widget(cancel_btn)
        content.add_widget(btn_row)
        popup = Popup(title="Export CSV", content=content, size_hint=(0.9, 0.9))

        def do_export(instance=None):
            filename = filename_input.text.strip()
            if not filename:
                self.show_popup(
                    "Error", "Please enter a file name.", auto_dismiss=2
                )
                return
            if not filename.lower().endswith(".csv"):
                filename += ".csv"
            export_file = os.path.join(os.getcwd(), filename)
            try:
                allergies = app.db_manager.get_all_allergies()
                headers = [
                    "id",
                    "allergen_name",
                    "danger_level",
                    "symptoms",
                    "ingredients",
                    "source",
                    "notes",
                    "created_date",
                ]
                with open(export_file, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    for row in allergies:
                        writer.writerow(row)
                popup.dismiss()
                self.show_popup(
                    "Export Complete",
                    f"Exported {len(allergies)} rows to:\n{export_file}",
                    auto_dismiss=3,
                )
            except Exception as e:
                popup.dismiss()
                self.show_popup("Error", f"Export failed: {e}", auto_dismiss=3)

        export_btn.bind(on_press=do_export)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def open_import_dialog(self):
        """Open a dialog for importing CSV files into the database."""
        app = App.get_running_app()  # type: ignore[attr-defined]
        content = BoxLayout(
            orientation="vertical", spacing=dp(10), padding=dp(10)
        )
        start_path = os.getcwd()
        filechooser = FileChooserListView(path=start_path, size_hint=(1, 0.75))
        filechooser.filters = []
        content.add_widget(filechooser)
        dup_row = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        dup_row.add_widget(
            Label(text="On duplicate:", size_hint_x=None, width=dp(110))
        )
        dup_spinner = Spinner(
            text="skip",
            values=("skip", "update"),
            size_hint_x=None,
            width=dp(120),
        )
        dup_row.add_widget(dup_spinner)
        content.add_widget(dup_row)
        btn_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        import_btn = Button(
            text="Import",
            background_color=(0.3, 0.8, 0.3, 1),
            size_hint_x=None,
            width=dp(120),
        )
        cancel_btn = Button(
            text="Cancel",
            background_color=(0.7, 0.7, 0.7, 1),
            size_hint_x=None,
            width=dp(120),
        )
        btn_row.add_widget(import_btn)
        btn_row.add_widget(cancel_btn)
        content.add_widget(btn_row)
        popup = Popup(title="Import CSV", content=content, size_hint=(0.9, 0.9))

        def do_import(instance=None):
            selected = filechooser.selection
            if not selected:
                self.show_popup("Error", "Please select a CSV file to import.")
                return
            file_path = selected[0]
            on_dup = dup_spinner.text.strip().lower() or "skip"
            summary = app.db_manager.import_from_csv(
                file_path, on_duplicate=on_dup
            )
            popup.dismiss()
            msg = f"Imported: {summary.get('imported',0)}\nUpdated: {summary.get('updated',0)}\nSkipped: {summary.get('skipped',0)}"
            errors = summary.get("errors", [])
            if errors:
                msg += "\nErrors:\n" + "\n".join(errors[:10])
            self.show_popup("Import Summary", msg, auto_dismiss=3)
            try:
                app.root.get_screen("allergy_list").refresh_list()
            except Exception:
                pass

        filechooser.bind(
            on_submit=lambda fc, selection, touch: (
                do_import() if selection else None
            )
        )
        import_btn.bind(on_press=do_import)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def go_back(self):
        """Navigate back to the main screen."""
        self.manager.current = "main"

    def show_popup(self, title, message, auto_dismiss=None):
        """Show a popup with a message."""
        app = App.get_running_app()
        popup_size = app.ui_config.get_popup_size()
        popup = Popup(
            title=title, content=Label(text=message), size_hint=popup_size
        )
        popup.open()
        # Always auto-dismiss after N seconds if requested
        if auto_dismiss:
            try:
                Clock.schedule_once(lambda dt: popup.dismiss(), auto_dismiss)
            except Exception:
                pass


class AllergyEntryScreen(Screen):
    """Screen for adding new allergy entries"""

    # Track whether the form is currently in 'edit' mode. The KV uses this
    # to show/hide the Cancel Edit button.
    is_editing = BooleanProperty(False)

    def on_kv_post(self, base_widget=None):
        """Called after the KV language has been applied to this Screen.

        Parameters:
            base_widget (Widget|None): The root widget passed by Kivy's
                lifecycle. Defaults to None when called programmatically.

        Side effects:
            Caches commonly used widget ids onto the Python object for
            convenient attribute access (for example, self.allergen_input).
        """
        # We copy commonly used widgets from `self.ids` to attributes to make
        # the later code easier to read (so we can write self.allergen_input
        # instead of self.ids.allergen_input everywhere).
        try:
            self.allergen_input = self.ids.allergen_input
            self.danger_spinner = self.ids.danger_spinner
            self.symptoms_input = self.ids.symptoms_input
            self.ingredients_input = self.ids.ingredients_input
            self.source_input = self.ids.source_input
            self.notes_input = self.ids.notes_input
        except Exception:
            # If the KV file doesn't provide the ids yet, we quietly ignore
            # the error. This keeps import-time checks from failing.
            pass

    def add_allergy(self):
        """Read the Add form and either insert a new allergy or update an existing one.

        Behavior:
            - Validates required fields (allergen name and danger level).
            - Converts the danger spinner text into an integer danger level.
            - If the form is in edit mode, calls DatabaseManager.update_allergy().
            - Otherwise, calls DatabaseManager.add_allergy().
            - Shows a success or error popup and clears the form on success.

        Returns:
            None: This method performs UI updates and database side-effects.
        """
        app = App.get_running_app()
        allergen_name = self.ids.allergen_input.text.strip()
        danger_text = self.ids.danger_spinner.text
        symptoms = self.ids.symptoms_input.text.strip()
        ingredients = self.ids.ingredients_input.text.strip()
        source = self.ids.source_input.text.strip()
        notes = self.ids.notes_input.text.strip()

        # Basic validation: ensure an allergen name and danger level are set.
        if not allergen_name or danger_text == "Select Level":
            self.show_popup(
                "Error", "Please enter allergen name and select danger level."
            )
            return

        # Convert the spinner text like '2 - Moderate' into an integer level.
        danger_level = int(danger_text.split(" - ")[0])

        # If we're currently editing, update the existing record.
        if hasattr(self, "current_edit_id") and self.current_edit_id:
            updated = app.db_manager.update_allergy(
                self.current_edit_id,
                allergen_name,
                danger_level,
                symptoms,
                ingredients,
                source,
                notes,
            )

            if updated:
                # Notify user, reset edit state, and clear the form.
                self.show_popup(
                    "Success",
                    f'Allergy "{allergen_name}" updated successfully!',
                )
                self.current_edit_id = None
                self.ids.add_button.text = "Add Allergy"
                try:
                    self.is_editing = False
                except Exception:
                    pass
                self.clear_form()
            else:
                # Update failed for some reason.
                self.show_popup("Error", "Failed to update allergy.")
        else:
            # Not editing: insert a new row into the database.
            success = app.db_manager.add_allergy(
                allergen_name,
                danger_level,
                symptoms,
                ingredients,
                source,
                notes,
            )

            if success:
                self.show_popup(
                    "Success", f'Allergy "{allergen_name}" added successfully!'
                )
                try:
                    self.is_editing = False
                except Exception:
                    pass
                self.clear_form()
            else:
                # IntegrityError likely: allergen name must be unique.
                self.show_popup(
                    "Error",
                    f'Allergen "{allergen_name}" already exists in the database.',
                )

    def load_for_edit(self, allergy_id):
        """Load a single allergy by id and populate the Add form for editing.

        Parameters:
            allergy_id (int): Primary key of the allergy to load.

        Side effects:
            - Prefills the Add form fields with the row data.
            - Sets internal edit state (self.current_edit_id and self.is_editing)
            - Switches the ScreenManager to the Add screen.

        Returns:
            None
        """
        app = App.get_running_app()
        row = app.db_manager.get_allergy(allergy_id)
        if not row:
            self.show_popup("Error", "Failed to load allergy for editing.")
            return

        (
            _id,
            name,
            danger_level,
            symptoms,
            ingredients,
            source,
            notes,
            created_date,
        ) = row

        # Prefill the form fields so the user can edit them.
        self.ids.allergen_input.text = name
        danger_text_map = {
            1: "1 - Mild",
            2: "2 - Moderate",
            3: "3 - Severe",
            4: "4 - Life-threatening",
        }
        self.ids.danger_spinner.text = danger_text_map.get(
            danger_level, "Select Level"
        )
        self.ids.symptoms_input.text = symptoms or ""
        self.ids.ingredients_input.text = ingredients or ""
        self.ids.source_input.text = source or ""
        self.ids.notes_input.text = notes or ""

        # Mark that we are editing and switch to the Add screen so the user
        # sees the prefilled form.
        self.current_edit_id = allergy_id
        self.ids.add_button.text = "Save Changes"
        self.is_editing = True
        self.manager.current = "add_allergy"

    def cancel_edit(self):
        """Cancel any in-progress edit and reset the Add form to an empty state.

        Side effects:
            - Clears internal edit identifiers (self.current_edit_id).
            - Resets the Add button label and editing flag.
            - Clears the form inputs.

        Returns:
            None
        """
        # Clear edit state if present
        if hasattr(self, "current_edit_id"):
            self.current_edit_id = None
        # Reset the add button label
        try:
            self.ids.add_button.text = "Add Allergy"
        except Exception:
            pass
        # Turn off editing flag
        try:
            self.is_editing = False
        except Exception:
            pass
        # Clear the form contents
        self.clear_form()

    def clear_form(self):
        """Clear all input fields on the Add form so a new entry can be added.

        Returns:
            None
        """
        self.ids.allergen_input.text = ""
        self.ids.danger_spinner.text = "Select Level"
        self.ids.symptoms_input.text = ""
        self.ids.ingredients_input.text = ""
        self.ids.source_input.text = ""
        self.ids.notes_input.text = ""

    def open_import_dialog(self):
        """Open a file chooser popup so the user can select a CSV to import.

        The popup provides a simple FileChooserListView and Import/Cancel
        buttons. When the user confirms, the CSV is passed to
        DatabaseManager.import_from_csv() and a brief summary popup is shown.
        """
        app = App.get_running_app()

        content = BoxLayout(
            orientation="vertical", spacing=dp(10), padding=dp(10)
        )

        # Start in the current working directory so folders are visible on Windows
        start_path = os.getcwd()
        filechooser = FileChooserListView(path=start_path, size_hint=(1, 0.75))
        # Avoid aggressive filters that can hide folders on some platforms
        # Use an empty list for no filters (FileChooser doesn't accept None)
        filechooser.filters = []
        content.add_widget(filechooser)

        # Duplicate-handling spinner
        dup_row = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        dup_row.add_widget(
            Label(text="On duplicate:", size_hint_x=None, width=dp(110))
        )
        dup_spinner = Spinner(
            text="skip",
            values=("skip", "update"),
            size_hint_x=None,
            width=dp(120),
        )
        dup_row.add_widget(dup_spinner)
        content.add_widget(dup_row)

        # Buttons
        btn_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        import_btn = Button(
            text="Import",
            background_color=(0.3, 0.8, 0.3, 1),
            size_hint_x=None,
            width=dp(120),
        )
        cancel_btn = Button(
            text="Cancel",
            background_color=(0.7, 0.7, 0.7, 1),
            size_hint_x=None,
            width=dp(120),
        )
        btn_row.add_widget(import_btn)
        btn_row.add_widget(cancel_btn)
        content.add_widget(btn_row)

        popup = Popup(title="Import CSV", content=content, size_hint=(0.9, 0.9))

        def do_import(instance=None):
            selected = filechooser.selection
            if not selected:
                self.show_popup("Error", "Please select a CSV file to import.")
                return
            file_path = selected[0]
            on_dup = dup_spinner.text.strip().lower() or "skip"
            summary = app.db_manager.import_from_csv(
                file_path, on_duplicate=on_dup
            )
            popup.dismiss()
            # Build a small summary message
            msg = f"Imported: {summary.get('imported',0)}\nUpdated: {summary.get('updated',0)}\nSkipped: {summary.get('skipped',0)}"
            errors = summary.get("errors", [])
            if errors:
                msg += "\nErrors:\n" + "\n".join(errors[:10])
            self.show_popup("Import Summary", msg)
            # Refresh the list to show any newly imported rows
            try:
                self.manager.get_screen("allergy_list").refresh_list()
            except Exception:
                pass

        # Double-click (on_submit) or buttons trigger the import
        filechooser.bind(
            on_submit=lambda fc, selection, touch: (
                do_import() if selection else None
            )
        )
        import_btn.bind(on_press=do_import)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())

        popup.open()

    def go_back(self):
        """Switch back to the main menu screen.

        Returns:
            None
        """
        self.manager.current = "main"

    def show_popup(self, title, message):
        """Show a small popup message to the user.

        Parameters:
            title (str): Title text shown in the popup window.
            message (str): Message body shown inside the popup.

        Behavior:
            - Opens a non-blocking Popup with the provided title and message.
            - If the title starts with 'Success' (case-insensitive), the
              popup will auto-dismiss after a short timeout (UIConfig).

        Returns:
            None
        """
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
                    lambda dt: popup.dismiss(),
                    app.ui_config.success_popup_timeout,
                )
            except Exception:
                pass


class AllergyListScreen(Screen):
    """Screen for viewing and managing allergy entries"""

    def on_kv_post(self, base_widget=None):
        """Called after KV for this screen; cache the layout container id.

        Parameters:
            base_widget (Widget|None): The root widget provided by Kivy's lifecycle.

        Side effects:
            Caches the `list_layout` id as `self.list_layout` for later use.
        """
        try:
            self.list_layout = self.ids.list_layout
        except Exception:
            pass

    def open_import_dialog(self):
        """Open a file chooser popup so the user can select a CSV to import.

        The popup provides a simple FileChooserListView and Import/Cancel
        buttons. When the user confirms, the CSV is passed to
        DatabaseManager.import_from_csv() and a brief summary popup is shown.
        """
        app = App.get_running_app()

        content = BoxLayout(
            orientation="vertical", spacing=dp(10), padding=dp(10)
        )
        filechooser = FileChooserListView(
            path=".", filters=["*.csv"], size_hint_y=0.8
        )
        content.add_widget(filechooser)

        # Optional small spinner to allow the user to choose behavior
        # for duplicates (skip or update). Defaults to skip.
        dup_row = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        dup_row.add_widget(
            Label(text="On duplicate:", size_hint_x=None, width=dp(110))
        )
        dup_spinner = Spinner(text="skip", values=("skip", "update"))
        dup_row.add_widget(dup_spinner)
        content.add_widget(dup_row)

        btn_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        import_btn = Button(text="Import", background_color=(0.3, 0.8, 0.3, 1))
        cancel_btn = Button(text="Cancel", background_color=(0.7, 0.7, 0.7, 1))
        btn_row.add_widget(import_btn)
        btn_row.add_widget(cancel_btn)
        content.add_widget(btn_row)

        popup = Popup(
            title="Import CSV",
            content=content,
            size_hint=app.ui_config.get_popup_size(),
        )

        def do_import(instance):
            selected = filechooser.selection
            if not selected:
                self.show_popup("Error", "Please select a CSV file to import.")
                return
            file_path = selected[0]
            on_dup = dup_spinner.text.strip().lower() or "skip"
            summary = app.db_manager.import_from_csv(
                file_path, on_duplicate=on_dup
            )
            popup.dismiss()
            # Build a small summary message
            msg = f"Imported: {summary.get('imported',0)}\nUpdated: {summary.get('updated',0)}\nSkipped: {summary.get('skipped',0)}"
            errors = summary.get("errors", [])
            if errors:
                msg += "\nErrors:\n" + "\n".join(errors[:5])
            self.show_popup("Import Summary", msg)
            # Refresh the list to show any newly imported rows
            self.refresh_list()

        import_btn.bind(on_press=do_import)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())

        popup.open()

    def on_enter(self):
        """Called when the screen becomes visible; refresh the list view.

        Side effects:
            Calls refresh_list() to rebuild the on-screen list from the DB.
        """
        self.refresh_list()

    def refresh_list(self):
        """Reload all allergy rows from the database and rebuild the list UI.

        Behavior:
            - Clears existing widgets from the list container.
            - Requests all allergies from DatabaseManager and creates a
              widget for each row.

        Returns:
            None
        """
        app = App.get_running_app()
        self.ids.list_layout.clear_widgets()
        danger_level = None
        try:
            sel = self.ids.list_danger_filter.text  # type: ignore[attr-defined]
            if sel and sel != "All Levels":
                danger_level = int(sel)
        except Exception:
            pass
        allergies = app.db_manager.get_all_allergies(danger_level)

        if not allergies:
            no_data = Label(
                text="No allergies in database",
                size_hint_y=None,
                height=dp(40),
                font_size=sp(12),
            )
            self.ids.list_layout.add_widget(no_data)
            return

        for idx, allergy in enumerate(allergies):
            allergy_widget = self.create_allergy_widget(allergy, row_index=idx)
            self.ids.list_layout.add_widget(allergy_widget)

    def create_allergy_widget(self, allergy, row_index: int = 0):
        app = App.get_running_app()  # type: ignore[attr-defined]
        is_mobile = getattr(app, "ui_config", None) and app.ui_config.is_mobile  # type: ignore[attr-defined]

        def _on_edit(aid):
            app.root.get_screen("add_allergy").load_for_edit(aid)  # type: ignore[attr-defined]

        return build_allergy_row(
            context="list",
            app=app,
            allergy_tuple=allergy,
            row_index=row_index,
            is_mobile=bool(is_mobile),
            show_edit_delete=True,
            on_edit=_on_edit,
            on_delete=lambda aid: self.delete_allergy(aid),
            preview_mode="symptoms_first",
        )

    def delete_allergy(self, allergy_id):
        """Ask the user to confirm deleting an allergy, then delete it.

        Parameters:
            allergy_id (int): Primary key of the allergy to delete.

        Behavior:
            - Shows a confirmation popup. If the user confirms, calls
              DatabaseManager.delete_allergy() and refreshes the list.

        Returns:
            None
        """
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
        """Return to the main menu screen.

        Returns:
            None
        """
        self.manager.current = "main"

    def show_popup(self, title, message):
        """Show a simple popup message (non-blocking).

        Parameters:
            title (str): Title for the popup window.
            message (str): Message body for the popup.

        Returns:
            None
        """
        app = App.get_running_app()
        popup_size = app.ui_config.get_popup_size()
        popup = Popup(
            title=title, content=Label(text=message), size_hint=popup_size
        )
        popup.open()


class SearchScreen(Screen):
    """Screen for searching allergies by ingredients"""

    def on_kv_post(self, base_widget=None):
        """Cache search-related ids and bind the search box change event.

        Parameters:
            base_widget (Widget|None): Root widget passed by Kivy's lifecycle.

        Side effects:
            Binds the search input text change to on_search_text_change so
            searches run automatically as the user types.
        """
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
        """Called when the search input text changes; schedule a delayed search.

        Parameters:
            instance (Widget): The TextInput instance raising the event.
            value (str): The new text value.

        Returns:
            None
        """
        Clock.unschedule(self.delayed_search)
        if value.strip():
            Clock.schedule_once(self.delayed_search, 0.5)
        else:
            self.clear_results()

    def delayed_search(self, dt):
        """Helper scheduled by the clock to run a search after a short delay.

        Parameters:
            dt (float): Time delta passed by the scheduler.

        Returns:
            None
        """
        self.search_allergies()

    def search_allergies(self):
        """Run a search using the DatabaseManager and display the results.

        Behavior:
            - Reads the search input, performs a DB search, and updates the
              results area by calling display_results().

        Returns:
            None
        """
        app = App.get_running_app()
        search_term = self.ids.search_input.text.strip()

        if not search_term:
            self.clear_results()
            return

        danger_level = None
        try:
            sel = self.ids.search_danger_filter.text  # type: ignore[attr-defined]
            if sel and sel != "All Levels":
                danger_level = int(sel)
        except Exception:
            pass
        allergies = app.db_manager.search_allergies(search_term, danger_level)
        self.display_results(allergies, search_term)

    def display_results(self, allergies, search_term):
        """Show search results in the results area; update a small label.

        Parameters:
            allergies (list[tuple]): Rows returned from DatabaseManager.search_allergies().
            search_term (str): The term that was searched for (used in labels).

        Returns:
            None
        """
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

        for idx, allergy in enumerate(allergies):
            result_widget = self.create_search_result_widget(
                allergy, row_index=idx
            )
            self.ids.results_layout.add_widget(result_widget)

    def create_search_result_widget(self, allergy, row_index: int = 0):
        app = App.get_running_app()  # type: ignore[attr-defined]
        is_mobile = getattr(app, "ui_config", None) and app.ui_config.is_mobile  # type: ignore[attr-defined]
        return build_allergy_row(
            context="search",
            app=app,
            allergy_tuple=allergy,
            row_index=row_index,
            is_mobile=bool(is_mobile),
            show_edit_delete=False,
            preview_mode="ingredients_first",
        )

    def on_pre_enter(self, *args):
        """Focus the search input automatically when the screen is shown.

        Returns:
            None
        """
        try:
            # Delay one frame so TextInput is ready
            Clock.schedule_once(
                lambda *_: setattr(self.ids.search_input, "focus", True), 0
            )
        except Exception:
            pass

    def clear_results(self):
        """Clear the search results and reset the label text.

        Returns:
            None
        """
        self.ids.results_layout.clear_widgets()
        self.ids.results_label.text = "Enter search term above"

    def go_back(self):
        """Return to the main menu screen from the search view.

        Returns:
            None
        """
        self.manager.current = "main"


class AllergyDatabaseApp(App):
    """Main application class for Food Allergy Shield."""
    
    # Prevent automatic KV loading by Kivy
    kv = ""
    
    def __init__(self, **kwargs):
        """Initialize the app and set up ui_config early."""
        super().__init__(**kwargs)
        # Initialize ui_config before anything else
        self.ui_config = UIConfig()

    def build(self):
        """Build and return the root widget for the app."""
        # Determine database path for both development and packaged environments
        # Try to find database in multiple locations
        possible_db_paths = [
            Path(__file__).parent / "food_allergies.db",  # Same directory as app
            Path.cwd() / "food_allergies.db",  # Current working directory
            Path.cwd() / "data" / "food_allergies.db",  # Development data directory
        ]
        
        db_path = None
        for path in possible_db_paths:
            if path.exists():
                db_path = str(path)
                break
        
        # If no existing database found, use the default name (will be created)
        if db_path is None:
            db_path = "food_allergies.db"
            
        self.db_manager = DatabaseManager(db_path)
        
        # Now load KV file with app context available
        kv_file = Path(__file__).parent / "food_allergy_shield.kv"
        if kv_file.exists():
            Builder.load_file(str(kv_file))
        else:
            Builder.load_file("food_allergy_shield.kv")
            
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(AllergyEntryScreen(name="add_allergy"))
        sm.add_widget(AllergyListScreen(name="allergy_list"))
        sm.add_widget(SearchScreen(name="search"))
        sm.add_widget(DatabaseMaintenanceScreen(name="maintenance"))
        return sm

    def on_start(self):
        """Called when the app starts.

        Side effects:
            Sets the window title on supported desktop platforms.
        """
        if hasattr(Window, "set_title"):
            Window.set_title("Food Allergy Shield")

    def on_pause(self):
        """Called when the app is paused (Android).

        Returns:
            bool: True to indicate the app can be paused and resumed.
        """
        return True

    def on_resume(self):
        """Called when the app is resumed (Android).

        This is a lifecycle hook used by mobile platforms; no action is needed
        for this simple application, but the method is present for clarity.
        """
        pass


def main():
    """
    The main entry point for the application.
    """
    app = AllergyDatabaseApp()
    return app


if __name__ == '__main__':
    app = main()
    app.run()