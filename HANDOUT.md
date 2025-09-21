Kivy Concepts — One-page Handout

This one-page handout summarizes the key Kivy concepts used in the Allergy Database app.

1) KV Language (allergy_database.kv)
- Purpose: Describe UI layout, widget trees, and simple rules declaratively.
- Key ideas:
  - <RuleName@Widget>: creates a reusable template (like a small subclass).
  - ids: give widgets an id so Python can access them via self.ids.<id_name>.
  - on_kv_post: call a Python method after KV is applied to wire ids.
  - size_hint, size_hint_x/y: control whether a widget sizes relative to parent.
  - dp(), sp(): device-independent pixels and scaleable font sizes.

2) Screen & ScreenManager
- Screen: a page or view. Each screen is a Python class (Screen subclass).
- ScreenManager: switches between screens using self.manager.current = 'name'.
- Use Screen.name to register screens (sm.add_widget(Screen(name='main'))).

3) Widgets Used
- BoxLayout / GridLayout: simple layout containers (vertical/horizontal).
- Label: display text.
- Button: clickable control; use on_press or bind(on_press=handler).
- TextInput / Spinner: user input controls.
- ScrollView: make content scrollable on small screens.

4) App class
- The App subclass (AllergyDatabaseApp) is the app entry point.
- build() returns the root widget (ScreenManager here).
- on_start, on_pause, on_resume: lifecycle hooks for mobile/desktop.

5) ids & on_kv_post
- ids from KV are available as self.ids inside a Screen instance once KV is applied.
- on_kv_post(self, base_widget=None) is a good place to cache frequently used ids.

6) Popup & Clock
- Popup shows small modal messages. size_hint controls size on mobile/desktop.
- Clock.schedule_once schedules delayed actions (e.g., auto-dismiss a popup).

7) sqlite3 integration
- DatabaseManager wraps sqlite3 operations: create table, insert, select, delete.
- Keep database access in a separate class for clarity and testability.
- Simple migration strategy: PRAGMA table_info to inspect columns; ALTER TABLE ADD COLUMN when needed.

Tips for students
- Make small, local changes and run the app to see the result.
- Use Builder.load_file('allergy_database.kv') to ensure KV is loaded before screens are created.
- When debugging layout/sizing, try resizing the Window on desktop and inspect size_hint values.

Further reading
- Kivy docs: https://kivy.org/doc/stable/
- KV language guide: https://kivy.org/doc/stable/api-kivy.lang.html

