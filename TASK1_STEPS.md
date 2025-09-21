Task 1: Add a ``source`` field (step-by-step guide)

Goal: Add a `source` field to the "Add Allergy" form, store it in the database, and display it in list and search results.

Files changed (high level):
- `allergy_database.kv` (added `source_input` form field)
- `allergy_database.py` (database schema migration, add_allergy signature, form handling, clear_form, and display code)

Step-by-step changes (what I changed and why)

1) KV: add the Source field to the form
- Location: inside the ScrollView form on `AllergyEntryScreen`.
- Change: inserted a labeled text input with id `source_input` and a short hint.
- Why: allows users to record where the allergy info came from (doctor, label, website).

2) Database: include `source` column
- Location: `DatabaseManager.init_database()`
- Changes:
  - CREATE TABLE includes `source TEXT`.
  - Migration step: if `source` is missing, run `ALTER TABLE allergies ADD COLUMN source TEXT`.
- Why: keep existing DBs working and add the new column to new DBs.

3) Python: accept and pass `source` through add_allergy
- Location: `DatabaseManager.add_allergy()` signature and INSERT statement now include `source`.
- Location: `AllergyEntryScreen.add_allergy()` reads `self.ids.source_input.text`, passes it to `db_manager.add_allergy()`.
- Why: persist the source string with the row.

4) Clear form: reset the `source_input` when clearing the form.

5) Display: show `source` in the entry details
- Location: `AllergyListScreen.create_allergy_widget()` and `SearchScreen.create_search_result_widget()`
- Change: unpacked the `source` column from the SELECT and included it in the `details` string.

Diff highlights (representative snippets)

- KV (added block):
  BoxLayout:
      orientation: 'vertical'
      spacing: dp(5)
      size_hint_y: None
      height: dp(70)

      CommonLabel:
          text: 'Source:'
          size_hint_y: None
          height: dp(30)
          halign: 'left'

      CommonTextInput:
          id: source_input
          multiline: False
          hint_text: 'e.g., Doctor, Label, Website'
          size_hint_y: None
          height: dp(35)

- Python (DB): added `source` column to CREATE and migration using PRAGMA table_info.
- Python (add_allergy):
    def add_allergy(self, allergen_name, danger_level, symptoms, ingredients, source, notes):
        INSERT INTO allergies (allergen_name, danger_level, symptoms, ingredients, source, notes)
        VALUES (?, ?, ?, ?, ?, ?)

- Python (AllergyEntryScreen): read `source` and pass it to db_manager
    source = self.ids.source_input.text.strip()


Testing notes

- I ran a lightweight import test (importing `allergy_database`) to ensure no syntax errors; import succeeded and Kivy initialized.
- Next step: run the full app (`python allergy_database.py`), create a new allergy with Source filled, then check "View All Allergies" and "Search" to see the Source printed in the details.

If you'd like, I can run the app here (it will open a window in the environment) or provide the exact commands to run locally.
