# Guided Lab: Food Allergy Database (short exercise)

This quick guided lab is designed for community college students to learn by doing. Each task is small and focuses on a practical change to the app.

Prerequisites

- Have Python and Kivy installed and the project open.
- Be able to run the app with: `python allergy_database.py`

Tasks (approx 20-40 minutes total)

1. Add a "Source" text field to the Add form

- Objective: Add a small text field named `source` to the Add Allergy form so the user can note where they found the info (e.g., "Doctor", "Label").
- Steps:
  - Edit `allergy_database.kv`: in the GridLayout form add a new `CommonLabel` with text "Source:" and a `CommonTextInput` below it with `id: source_input`.
  - Edit `DatabaseManager.init_database` to add a new column `source TEXT` to the `allergies` table (you can skip migration; for the lab it's fine to delete `allergies.db` and let the app recreate it).
  - Update `DatabaseManager.add_allergy` to accept the `source` value and store it.
  - In `AllergyEntryScreen.add_allergy`, read `self.ids.source_input.text` and pass it into the DB call.
- Verify: Run the app, add an entry with Source, and open `allergies.db` with sqlite3 or a browser to see the column.

2. Change the success popup text format

- Objective: Make success popups show a slightly friendlier message: "Saved — &lt;Allergen&gt; added!" instead of the current text.
- Steps:
  - Open `allergy_database.py` and find where the ``show_popup('Success', ...)`` call is made after insert success.
  - Modify the string to: `f"Saved — {allergen_name} added!"` and save.
- Verify: Run app, add an allergy and watch the popup message change and auto-dismiss after ~2.5s.

3. Add a new danger level option

- Objective: Add a new danger level ("0 - Unknown") so users can mark unspecified danger.
- Steps:
  - Edit `allergy_database.kv` and add the value `"0 - Unknown"` to the `Spinner` values for `danger_spinner`.
  - Edit any code that assumes danger levels start at 1 (for this lab you can allow 0; the list view will still display "Level 0: UNKNOWN").
- Verify: Run the app, use the new spinner value, add an allergy with 0, and view it in the list.

Extra credit

- Add an edit flow: let users tap a list item to open the Add screen pre-filled and then save edits.
- Add simple validation that ingredients must be shorter than 1000 characters.

Submit

- Prepare a short README note describing which task you completed and one screenshot showing the updated UI.

Good luck — ask if you want step-by-step help for any of these tasks!
