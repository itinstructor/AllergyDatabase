import sqlite3
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout


class UIConfig:
    """Configuration class for platform-specific UI settings"""
    
    def __init__(self):
        self.is_mobile = platform in ('android', 'ios')
        self.is_desktop = platform in ('win', 'linux', 'macosx')
        
        # Set window size for desktop only - avoid setting on mobile
        if self.is_desktop:
            Window.size = (800, 600)
            # Only set minimum size if greater than 0
            if Window.size[0] > 0 and Window.size[1] > 0:
                Window.minimum_width = 600
                Window.minimum_height = 400
        elif self.is_mobile:
            # For mobile, let the system handle window sizing
            # Don't set any window constraints
            pass
        
        # Enhanced mobile-first measurements
        if self.is_mobile:
            self.padding = dp(20)  # Increased padding for mobile
            self.spacing = dp(20)  # Increased spacing
            self.button_height = dp(70)  # Larger touch targets
            self.input_height = dp(60)   # Larger input fields
            self.title_font_size = sp(28)  # Larger titles
            self.button_font_size = sp(18) # Larger button text
            self.label_font_size = sp(16)  # Larger labels
            self.header_height = dp(100)   # Taller headers
            self.min_touch_size = dp(60)   # Larger minimum touch
            self.success_popup_timeout = 2.5
        else:
            self.padding = dp(20)
            self.spacing = dp(10)
            self.button_height = dp(40)
            self.input_height = dp(35)
            self.title_font_size = sp(20)
            self.button_font_size = sp(14)
            self.label_font_size = sp(12)
            self.header_height = dp(50)
            self.min_touch_size = dp(32)
            self.success_popup_timeout = 2.5
    
    def get_responsive_cols(self, default_cols=2):
        """Get responsive column count based on screen width"""
        # To simplify the UI code and ensure consistency across platforms,
        # we will now always use a single-column layout. This avoids complex,
        # duplicated layout logic in the Python code. For more complex
        # responsive layouts, the KV language approach is recommended.
        return 1
    
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
        
        # Create allergies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS allergies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                allergen_name TEXT NOT NULL UNIQUE,
                danger_level INTEGER NOT NULL,
                symptoms TEXT,
                ingredients TEXT,
                notes TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_allergy(self, allergen_name, danger_level, symptoms, ingredients, notes):
        """Add a new allergy entry to the database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO allergies (allergen_name, danger_level, symptoms, ingredients, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (allergen_name, danger_level, symptoms, ingredients, notes))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Allergen already exists
        except Exception as e:
            print(f"Error adding allergy: {e}")
            return False
    
    def get_all_allergies(self):
        """Retrieve all allergies from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM allergies ORDER BY danger_level DESC, allergen_name')
        allergies = cursor.fetchall()
        
        conn.close()
        return allergies
    
    def search_allergies(self, search_term):
        """Search for allergies by allergen name or ingredients"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        search_term = f"%{search_term.lower()}%"
        cursor.execute('''
            SELECT * FROM allergies 
            WHERE LOWER(allergen_name) LIKE ? OR LOWER(ingredients) LIKE ?
            ORDER BY danger_level DESC, allergen_name
        ''', (search_term, search_term))
        
        allergies = cursor.fetchall()
        conn.close()
        return allergies
    
    def delete_allergy(self, allergy_id):
        """Delete an allergy entry by ID"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM allergies WHERE id = ?', (allergy_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting allergy: {e}")
            return False
    
    def update_allergy(self, allergy_id, allergen_name, danger_level, symptoms, ingredients, notes):
        """Update an existing allergy entry"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE allergies 
                SET allergen_name = ?, danger_level = ?, symptoms = ?, ingredients = ?, notes = ?
                WHERE id = ?
            ''', (allergen_name, danger_level, symptoms, ingredients, notes, allergy_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating allergy: {e}")
            return False


class ResponsiveButton(Button):
    """A custom button that applies responsive font and height from UIConfig."""
    def __init__(self, ui_config, **kwargs):
        # Allow font_size and height to be overridden by kwargs
        if 'font_size' not in kwargs:
            kwargs['font_size'] = ui_config.button_font_size
        if 'height' not in kwargs:
            kwargs['height'] = ui_config.button_height
        kwargs.setdefault('size_hint_y', None)
        super().__init__(**kwargs)

class ResponsiveLabel(Label):
    """A custom label that applies responsive font size from UIConfig."""
    def __init__(self, ui_config, **kwargs):
        if 'font_size' not in kwargs:
            kwargs['font_size'] = ui_config.label_font_size
        # Set defaults that are common in this app, but allow overriding
        kwargs.setdefault('valign', 'middle')
        super().__init__(**kwargs)

class ResponsiveTextInput(TextInput):
    """A custom TextInput that applies responsive font and height from UIConfig."""
    def __init__(self, ui_config, **kwargs):
        if 'font_size' not in kwargs:
            kwargs['font_size'] = ui_config.label_font_size
        if 'height' not in kwargs:
            kwargs['height'] = ui_config.input_height
        kwargs.setdefault('size_hint_y', None)
        super().__init__(**kwargs)

class ResponsiveSpinner(Spinner):
    """A custom Spinner that applies responsive font and height from UIConfig."""
    def __init__(self, ui_config, **kwargs):
        if 'font_size' not in kwargs:
            kwargs['font_size'] = ui_config.label_font_size
        if 'height' not in kwargs:
            kwargs['height'] = ui_config.input_height
        kwargs.setdefault('size_hint_y', None)
        super().__init__(**kwargs)


class AllergyEntryScreen(Screen):
    """Screen for adding new allergy entries"""
    
    def __init__(self, db_manager, ui_config, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.ui_config = ui_config
        self._ui_built = False  # Flag to ensure UI is built only once

    def on_pre_enter(self, *args):
        """Build UI only on first entry to prevent duplication."""
        if not self._ui_built:
            self.build_ui()
            self._ui_built = True

    def on_kv_post(self, base_widget=None):
        """Called after KV is applied to ensure ids are available; attach refs."""
        # Attach ids to instance attributes for convenience
        try:
            self.allergen_input = self.ids.allergen_input
            self.danger_spinner = self.ids.danger_spinner
            self.symptoms_input = self.ids.symptoms_input
            self.ingredients_input = self.ids.ingredients_input
            self.notes_input = self.ids.notes_input
        except Exception:
            pass
    
    def build_ui(self):
        # UI defined in KV. Attach id references if available.
        # This keeps Python as the controller only and avoids creating widgets
        # programmatically which previously caused duplication.
        try:
            self.allergen_input = self.ids.allergen_input
            self.danger_spinner = self.ids.danger_spinner
            self.symptoms_input = self.ids.symptoms_input
            self.ingredients_input = self.ids.ingredients_input
            self.notes_input = self.ids.notes_input
        except Exception:
            # ids may not be available yet depending on load order; it's fine
            # they'll be available once the KV is applied. on_pre_enter will
            # be called again if needed.
            pass
    
    def create_button_layout(self):
        """Create responsive button layout"""
        if self.ui_config.is_mobile:
            # Stack buttons vertically on mobile
            button_layout = BoxLayout(
                orientation='vertical', 
                size_hint_y=None, 
                height=self.ui_config.button_height * 3 + self.ui_config.spacing * 2, 
                spacing=self.ui_config.spacing
            )
        else:
            # Horizontal layout for desktop
            button_layout = BoxLayout(
                size_hint_y=None, 
                height=self.ui_config.button_height, 
                spacing=self.ui_config.spacing
            )
        
        add_btn = ResponsiveButton(
            self.ui_config,
            text='Add Allergy',
            background_color=(0.2, 0.7, 0.3, 1)  # Green for primary action
        )
        add_btn.bind(on_press=self.add_allergy)
        button_layout.add_widget(add_btn)
        
        clear_btn = ResponsiveButton(
            self.ui_config,
            text='Clear Form',
            background_color=(0.9, 0.6, 0.2, 1)  # Orange for secondary action
        )
        clear_btn.bind(on_press=self.clear_form)
        button_layout.add_widget(clear_btn)
        
        back_btn = ResponsiveButton(
            self.ui_config,
            text='Back to Main',
            background_color=(0.6, 0.6, 0.6, 1)  # Gray for navigation
        )
        back_btn.bind(on_press=self.go_back)
        button_layout.add_widget(back_btn)
        
        return button_layout
    
    def add_allergy(self, instance=None):
        allergen_name = self.allergen_input.text.strip()
        danger_text = self.danger_spinner.text
        symptoms = self.symptoms_input.text.strip()
        ingredients = self.ingredients_input.text.strip()
        notes = self.notes_input.text.strip()
        
        if not allergen_name or danger_text == 'Select Level':
            self.show_popup('Error', 'Please enter allergen name and select danger level.')
            return
        
        # Extract danger level number
        danger_level = int(danger_text.split(' - ')[0])
        
        success = self.db_manager.add_allergy(allergen_name, danger_level, symptoms, ingredients, notes)
        
        if success:
            self.show_popup('Success', f'Allergy "{allergen_name}" added successfully!')
            self.clear_form()
        else:
            self.show_popup('Error', f'Allergen "{allergen_name}" already exists in the database.')
    
    def clear_form(self, instance=None):
        self.allergen_input.text = ''
        self.danger_spinner.text = 'Select Level'
        self.symptoms_input.text = ''
        self.ingredients_input.text = ''
        self.notes_input.text = ''
    
    def go_back(self, instance=None):
        self.manager.current = 'main'
    
    def show_popup(self, title, message):
        popup_size = self.ui_config.get_popup_size()
        popup = Popup(title=title, content=Label(text=message), size_hint=popup_size)
        popup.open()
        # Auto-dismiss success messages after a short interval for better UX
        try:
            if isinstance(title, str) and title.strip().lower().startswith('success'):
                try:
                    timeout = float(self.ui_config.success_popup_timeout)
                except Exception:
                    timeout = 2.5
                Clock.schedule_once(lambda dt: popup.dismiss(), timeout)
        except Exception:
            pass


class AllergyListScreen(Screen):
    """Screen for viewing and managing allergy entries"""
    
    def __init__(self, db_manager, ui_config, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.ui_config = ui_config
        self._ui_built = False

    def on_pre_enter(self, *args):
        """Build UI on first entry and refresh list."""
        if not self._ui_built:
            self.build_ui()
            self._ui_built = True
        self.refresh_list()

    def on_kv_post(self, base_widget=None):
        """Attach the list container id after KV is applied."""
        try:
            self.list_layout = self.ids.list_layout
        except Exception:
            pass

    def build_ui(self):
        # UI defined in KV. Wire id for list container to avoid building here.
        try:
            self.list_layout = self.ids.list_layout
        except Exception:
            pass

    def create_header_layout(self):
        """Create responsive header layout"""
        if self.ui_config.is_mobile:
            # Stack header elements vertically on mobile
            header_layout = BoxLayout(
                orientation='vertical', 
                size_hint_y=None, 
                height=self.ui_config.header_height + self.ui_config.button_height + self.ui_config.spacing, 
                spacing=self.ui_config.spacing
            )
            
            title = ResponsiveLabel(
                self.ui_config,
                text='Allergy Database',
                font_size=self.ui_config.title_font_size,
                height=self.ui_config.header_height,
                bold=True,
                halign='center'
            )
            header_layout.add_widget(title)
            
            # Button row
            button_row = BoxLayout(size_hint_y=None, height=self.ui_config.button_height, spacing=self.ui_config.spacing)
        else:
            # Horizontal layout for desktop
            header_layout = BoxLayout(
                size_hint_y=None, 
                height=self.ui_config.header_height, 
                spacing=self.ui_config.spacing
            )
            
            title = ResponsiveLabel(
                self.ui_config,
                text='Allergy Database',
                font_size=self.ui_config.title_font_size,
                bold=True
            )
            header_layout.add_widget(title)
            button_row = header_layout
        
        refresh_btn = ResponsiveButton(
            self.ui_config,
            text='Refresh', 
            size_hint_x=None, 
            width=dp(100)
        )
        refresh_btn.bind(on_press=self.refresh_list)
        button_row.add_widget(refresh_btn)
        
        back_btn = ResponsiveButton(
            self.ui_config,
            text='Back', 
            size_hint_x=None, 
            width=dp(100)
        )
        back_btn.bind(on_press=self.go_back)
        button_row.add_widget(back_btn)
        
        if self.ui_config.is_mobile:
            header_layout.add_widget(button_row)
        
        return header_layout
    
    def refresh_list(self, instance=None):
        # When repopulating the list, always clear previous widgets to avoid duplicates
        try:
            self.list_layout.clear_widgets()
        except Exception:
            # If list_layout is not attached yet, nothing to clear
            pass
        allergies = self.db_manager.get_all_allergies()
        
        if not allergies:
            no_data = ResponsiveLabel(self.ui_config, text='No allergies in database', height=dp(40), halign='center')
            self.list_layout.add_widget(no_data)
            return
        
        for allergy in allergies:
            allergy_widget = self.create_allergy_widget(allergy)
            self.list_layout.add_widget(allergy_widget)
    
    def create_allergy_widget(self, allergy):
        allergy_id, name, danger_level, symptoms, ingredients, notes, created_date = allergy
        
        # Responsive height based on platform
        widget_height = dp(140) if self.ui_config.is_mobile else dp(120)
        
        # Use a RelativeLayout to overlay an invisible button for press events
        root_widget = RelativeLayout(size_hint_y=None, height=widget_height)

        # Main container for the visible content
        container = BoxLayout(
            orientation='vertical', 
            size_hint_y=None, 
            height=widget_height, 
            spacing=dp(5)
        )
        
        # Header with name and danger level indicator
        header = BoxLayout(size_hint_y=None, height=self.ui_config.button_height)
        
        danger_colors = {1: [0.5, 1, 0.5, 1], 2: [1, 1, 0.5, 1], 3: [1, 0.7, 0.5, 1], 4: [1, 0.5, 0.5, 1]}
        danger_texts = {1: 'MILD', 2: 'MODERATE', 3: 'SEVERE', 4: 'LIFE-THREATENING'}
        
        name_label = ResponsiveLabel(
            self.ui_config,
            text=f'{name}',
            font_size=self.ui_config.button_font_size,
            bold=True,
            height=self.ui_config.button_height
        )
        header.add_widget(name_label)
        
        # Responsive button width
        button_width = dp(150) if self.ui_config.is_mobile else dp(200)
        
        danger_btn = ResponsiveButton(
            self.ui_config,
            text=f'Level {danger_level}: {danger_texts[danger_level]}',
            size_hint_x=None, 
            width=button_width,
            background_color=danger_colors[danger_level],
            font_size=self.ui_config.label_font_size
        )
        header.add_widget(danger_btn)
        
        container.add_widget(header)
        
        # Details with responsive text size
        details = f'Symptoms: {symptoms or "None specified"}\n'
        details += f'Ingredients: {ingredients or "None specified"}'
        if notes:
            details += f'\nNotes: {notes}'
        
        details_height = widget_height - self.ui_config.button_height - dp(10)
        details_label = ResponsiveLabel(
            self.ui_config,
            text=details,
            valign='top',
            height=details_height,
            markup=True
        )
        details_label.bind(size=details_label.setter('text_size'))
        container.add_widget(details_label)
        
        # Add an invisible button over the top for actions. Tapping the item
        # will now initiate the delete confirmation process.
        action_button = Button(
            background_color=(0, 0, 0, 0),  # Transparent background
            on_press=lambda x: self.delete_allergy(allergy_id)
        )
        
        root_widget.add_widget(container)
        root_widget.add_widget(action_button)
        return root_widget
    
    def delete_allergy(self, allergy_id):
        def confirm_delete(instance):
            if self.db_manager.delete_allergy(allergy_id):
                self.refresh_list()
                popup.dismiss()
            else:
                popup.dismiss()
                self.show_popup('Error', 'Failed to delete allergy.')
        
        content = BoxLayout(orientation='vertical', spacing=self.ui_config.spacing)
        content.add_widget(ResponsiveLabel(
            self.ui_config,
            text='Are you sure you want to delete this allergy?',
            halign='center'
        ))
        
        button_layout = BoxLayout(
            size_hint_y=None, 
            height=self.ui_config.button_height, 
            spacing=self.ui_config.spacing
        )
        
        yes_btn = ResponsiveButton(
            self.ui_config,
            text='Yes'
        )
        yes_btn.bind(on_press=confirm_delete)
        button_layout.add_widget(yes_btn)
        
        no_btn = ResponsiveButton(
            self.ui_config,
            text='No'
        )
        no_btn.bind(on_press=lambda x: popup.dismiss())
        button_layout.add_widget(no_btn)
        
        content.add_widget(button_layout)
        
        popup_size = self.ui_config.get_popup_size()
        popup = Popup(title='Confirm Delete', content=content, size_hint=popup_size)
        popup.open()
    
    def go_back(self, instance=None):
        self.manager.current = 'main'
    
    def show_popup(self, title, message):
        popup_size = self.ui_config.get_popup_size()
        popup = Popup(title=title, content=Label(text=message), size_hint=popup_size)
        popup.open()
        # Auto-dismiss success messages to avoid lingering notifications
        try:
            if isinstance(title, str) and title.strip().lower().startswith('success'):
                try:
                    timeout = float(self.ui_config.success_popup_timeout)
                except Exception:
                    timeout = 2.5
                Clock.schedule_once(lambda dt: popup.dismiss(), timeout)
        except Exception:
            pass


class SearchScreen(Screen):
    """Screen for searching allergies by ingredients"""
    
    def __init__(self, db_manager, ui_config, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.ui_config = ui_config
        # Defer UI construction until screen is shown to avoid duplicate widgets
        self._ui_built = False

    def on_pre_enter(self, *args):
        """Build UI on first entry and clear previous results."""
        if not self._ui_built:
            self.build_ui()
            self._ui_built = True
        # Clear results each time the user navigates to search
        self.clear_results()

    def on_kv_post(self, base_widget=None):
        """Attach search and results ids and ensure binding."""
        try:
            self.search_input = self.ids.search_input
            self.results_layout = self.ids.results_layout
            self.results_label = self.ids.results_label
            # Bind text change if it's not already bound in KV
            try:
                self.search_input.bind(text=self.on_search_text_change)
            except Exception:
                pass
        except Exception:
            pass
    
    def build_ui(self):
        # UI defined in KV. Attach ids for search input and results.
        try:
            self.search_input = self.ids.search_input
            self.results_layout = self.ids.results_layout
            self.results_label = self.ids.results_label
            # Make sure search_input binds to text change if not already bound in KV
            try:
                self.search_input.bind(text=self.on_search_text_change)
            except Exception:
                pass
        except Exception:
            pass
    
    def create_search_layout(self):
        """Create responsive search input layout"""
        if self.ui_config.is_mobile:
            # Stack search elements vertically on mobile
            search_layout = BoxLayout(
                orientation='vertical', 
                size_hint_y=None, 
                height=self.ui_config.input_height * 2 + self.ui_config.spacing * 2, 
                spacing=self.ui_config.spacing
            )
            
            # Search input row
            input_row = BoxLayout(size_hint_y=None, height=self.ui_config.input_height, spacing=self.ui_config.spacing)
            input_row.add_widget(ResponsiveLabel(
                self.ui_config,
                text='Search:',
                size_hint_x=None,
                width=dp(80)
            ))
            
            self.search_input = ResponsiveTextInput(
                self.ui_config,
                multiline=False,
                hint_text='Enter allergen name or ingredient...'
            )
            self.search_input.bind(text=self.on_search_text_change)
            input_row.add_widget(self.search_input)
            
            search_layout.add_widget(input_row)
            
            # Button row
            button_row = BoxLayout(size_hint_y=None, height=self.ui_config.button_height, spacing=self.ui_config.spacing)
        else:
            # Horizontal layout for desktop
            search_layout = BoxLayout(
                size_hint_y=None, 
                height=self.ui_config.input_height, 
                spacing=self.ui_config.spacing
            )
            
            search_layout.add_widget(ResponsiveLabel(
                self.ui_config,
                text='Search:',
                size_hint_x=None,
                width=dp(80)
            ))
            
            self.search_input = ResponsiveTextInput(
                self.ui_config,
                multiline=False,
                hint_text='Enter allergen name or ingredient...'
            )
            self.search_input.bind(text=self.on_search_text_change)
            search_layout.add_widget(self.search_input)
            button_row = search_layout

        search_btn = ResponsiveButton(
            self.ui_config,
            text='Search', 
            size_hint_x=None, 
            width=dp(100)
        )
        search_btn.bind(on_press=self.search_allergies)
        button_row.add_widget(search_btn)
        
        back_btn = ResponsiveButton(
            self.ui_config,
            text='Back', 
            size_hint_x=None, 
            width=dp(100)
        )
        back_btn.bind(on_press=self.go_back)
        button_row.add_widget(back_btn)
        
        if self.ui_config.is_mobile:
            search_layout.add_widget(button_row)
        
        return search_layout
    
    def on_search_text_change(self, instance, value):
        # Auto-search as user types (with a small delay)
        Clock.unschedule(self.delayed_search)
        if value.strip():
            Clock.schedule_once(self.delayed_search, 0.5)
        else:
            self.clear_results()
    
    def delayed_search(self, dt):
        self.search_allergies()
    
    def search_allergies(self, instance=None):
        search_term = self.search_input.text.strip()
        
        if not search_term:
            self.clear_results()
            return
        
        allergies = self.db_manager.search_allergies(search_term)
        self.display_results(allergies, search_term)
    
    def display_results(self, allergies, search_term):
        self.results_layout.clear_widgets()
        
        if not allergies:
            self.results_label.text = f'No results found for "{search_term}"'
            no_results = ResponsiveLabel(self.ui_config, text='No matching allergies found', height=dp(40), halign='center')
            self.results_layout.add_widget(no_results)
            return
        
        self.results_label.text = f'Found {len(allergies)} result(s) for "{search_term}"'
        
        for allergy in allergies:
            allergy_widget = self.create_search_result_widget(allergy, search_term)
            self.results_layout.add_widget(allergy_widget)
    
    def create_search_result_widget(self, allergy, search_term):
        allergy_id, name, danger_level, symptoms, ingredients, notes, created_date = allergy
        
        container = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), spacing=dp(5))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(30))
        
        danger_colors = {1: [0.5, 1, 0.5, 1], 2: [1, 1, 0.5, 1], 3: [1, 0.7, 0.5, 1], 4: [1, 0.5, 0.5, 1]}
        danger_texts = {1: 'MILD', 2: 'MODERATE', 3: 'SEVERE', 4: 'LIFE-THREATENING'}
        
        name_label = ResponsiveLabel(self.ui_config, text=f'{name}', font_size='16sp', bold=True, height=dp(30))
        header.add_widget(name_label)
        
        danger_label = ResponsiveLabel(
            self.ui_config,
            text=f'Level {danger_level}: {danger_texts[danger_level]}',
            color=danger_colors[danger_level],
            size_hint_x=None, width=dp(200),
            height=dp(30)
        )
        header.add_widget(danger_label)
        
        container.add_widget(header)
        
        # Highlight matching text
        details = f'Ingredients: {ingredients or "None specified"}'
        if symptoms:
            details += f'\nSymptoms: {symptoms}'
        
        details_label = ResponsiveLabel(
            self.ui_config,
            text=details,
            valign='top',
            height=dp(65)
        )
        details_label.bind(size=details_label.setter('text_size'))
        container.add_widget(details_label)
        
        return container
    
    def clear_results(self):
        try:
            self.results_layout.clear_widgets()
        except Exception:
            pass
        self.results_label.text = 'Enter search term above'
    
    def go_back(self, instance=None):
        self.manager.current = 'main'


class MainScreen(Screen):
    """Main menu screen"""
    
    def __init__(self, ui_config, **kwargs):
        super().__init__(**kwargs)
        self.ui_config = ui_config
        # Defer UI construction until screen is shown to avoid duplicate widgets
        self._ui_built = False

    def on_pre_enter(self, *args):
        """Build UI on first entry."""
        if not self._ui_built:
            self.build_ui()
            self._ui_built = True

    def on_kv_post(self, base_widget=None):
        """Optional hook if we need to attach ids for MainScreen later."""
        # No id wiring required for MainScreen at the moment
        return
    
    def build_ui(self):
        # UI defined in KV. MainScreen buttons and layout are provided there.
        # Nothing to build programmatically here. If needed, we could attach
        # any dynamic references via self.ids.
        try:
            # Optionally access title or other ids here, e.g. self.ids.main_title
            pass
        except Exception:
            pass
    
    def go_to_add(self, instance=None):
        self.manager.current = 'add_allergy'
    
    def go_to_list(self, instance=None):
        self.manager.current = 'allergy_list'
    
    def go_to_search(self, instance=None):
        self.manager.current = 'search'
    
    def exit_app(self, instance=None):
        App.get_running_app().stop()


class AllergyDatabaseApp(App):
    """Main application class"""
    
    def build(self):
        # Initialize UI configuration
        self.ui_config = UIConfig()
        
        # Initialize database
        self.db_manager = DatabaseManager()
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens with UI configuration
        sm.add_widget(MainScreen(self.ui_config, name='main'))
        sm.add_widget(AllergyEntryScreen(self.db_manager, self.ui_config, name='add_allergy'))
        sm.add_widget(AllergyListScreen(self.db_manager, self.ui_config, name='allergy_list'))
        sm.add_widget(SearchScreen(self.db_manager, self.ui_config, name='search'))
        
        return sm
    
    def on_start(self):
        """Called when the app starts"""
        # Set app title
        if hasattr(Window, 'set_title'):
            Window.set_title('Food Allergy Database')
    
    def on_pause(self):
        """Called when the app is paused (Android)"""
        return True
    
    def on_resume(self):
        """Called when the app is resumed (Android)"""
        pass


if __name__ == '__main__':
    AllergyDatabaseApp().run()