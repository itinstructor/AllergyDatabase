"""
Food Allergy Shield - Main application file for Briefcase packaging.
"""
import os
import sys
from pathlib import Path

# Import the core components
from .database_manager import DatabaseManager

# Import all the Kivy modules
import csv
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

# Get the KV file path relative to this module
KV_FILE = Path(__file__).parent / 'food_allergy_shield.kv'


class UIConfig:
    """Small helper to store UI settings that depend on platform."""

    def __init__(self):
        self.is_mobile = platform in ("android", "ios")
        self.is_desktop = platform in ("win", "linux", "macosx")

        if self.is_desktop:
            Window.size = (800, 600)

        self.success_popup_timeout = 2.5

    def get_popup_size(self):
        """Returns appropriate popup size based on platform."""
        if self.is_mobile:
            return (dp(280), dp(150))
        return (dp(300), dp(150))

    def get_content_padding(self):
        """Returns appropriate content padding based on platform."""
        if self.is_mobile:
            return dp(20)
        return dp(10)


class MessagePopup:
    """Helper class for showing popup messages."""

    def __init__(self, ui_config):
        self.ui_config = ui_config

    def show_message(self, title, message, auto_dismiss_timeout=None):
        """Shows a popup message with the given title and message."""
        popup_size = self.ui_config.get_popup_size()
        
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        label = Label(
            text=message,
            text_size=(popup_size[0] - dp(40), None),
            halign='center',
            valign='middle'
        )
        content.add_widget(label)
        
        close_button = Button(
            text='OK',
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(close_button)
        
        popup = Popup(
            title=title,
            content=content,
            size=popup_size,
            auto_dismiss=True
        )
        
        close_button.bind(on_press=popup.dismiss)
        popup.open()
        
        if auto_dismiss_timeout:
            Clock.schedule_once(lambda dt: popup.dismiss(), auto_dismiss_timeout)
        
        return popup


# Import all the screen classes from the original file
# (This is a simplified version - you'd need to copy all the screen classes)
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AllergyEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AllergyListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DatabaseMaintenanceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AllergyDatabaseApp(App):
    def build(self):
        self.ui_config = UIConfig()
        self.db_manager = DatabaseManager()
        
        # Load the KV file from the package directory
        Builder.load_file(str(KV_FILE))
        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(AllergyEntryScreen(name="add_allergy"))
        sm.add_widget(AllergyListScreen(name="allergy_list"))
        sm.add_widget(SearchScreen(name="search"))
        sm.add_widget(DatabaseMaintenanceScreen(name="maintenance"))
        return sm

    def on_start(self):
        """Called when the app starts."""
        if hasattr(Window, "set_title"):
            Window.set_title("Food Allergy Database")

    def on_pause(self):
        """Called when the app is paused (Android)."""
        return True

    def on_resume(self):
        """Called when the app is resumed (Android)."""
        pass


def main():
    """Main entry point for the application."""
    return AllergyDatabaseApp()


if __name__ == "__main__":
    app = main()
    app.run()