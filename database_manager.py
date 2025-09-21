import sqlite3
import csv
from typing import Dict, Any


class DatabaseManager:
    """Handles all database operations for the allergy database.

    Data shape (rows returned by SELECT):
    (id: int, allergen_name: str, danger_level: int, symptoms: str|
     None, ingredients: str|None, source: str|None, notes: str|None,
     created_date: str)

    The methods below use simple Python primitives and SQLite types
    so they are easy to test and teach in a classroom setting.
    """

    def __init__(self, db_name="allergies.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Initialize the database and create tables if they don't exist.

        Ensures the `allergies` table exists with the expected columns.
        If the `source` column is missing (older DB), the method will
        attempt to ALTER the table to add it. Non-fatal exceptions are
        printed as warnings so the app can continue running in most cases.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
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

                cursor.execute("PRAGMA table_info(allergies)")
                cols = [row[1] for row in cursor.fetchall()]
                if "source" not in cols:
                    cursor.execute(
                        "ALTER TABLE allergies ADD COLUMN source TEXT"
                    )
        except Exception as e:
            print(f"Database migration warning: {e}")

    def add_allergy(
        self, allergen_name, danger_level, symptoms, ingredients, source, notes
    ):
        """Add a new allergy entry to the database.

        Parameters:
            allergen_name (str): Human-readable name of the allergen. Must be unique.
            danger_level (int): Numeric danger rating (higher = more dangerous).
            symptoms (str|None): Comma-separated or free text of symptoms.
            ingredients (str|None): Ingredients list or text to search.
            source (str|None): Where the information came from (label, website, etc.).
            notes (str|None): Free-text notes.

        Returns:
            bool: True on success, False on failure (for example, when the
            allergen_name would violate the UNIQUE constraint).
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO allergies (allergen_name, danger_level, symptoms, ingredients, source, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        allergen_name,
                        danger_level,
                        symptoms,
                        ingredients,
                        source,
                        notes,
                    ),
                )
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding allergy: {e}")
            return False

    def get_allergy(self, allergy_id):
        """Return a single allergy row by id or None.

        Parameters:
            allergy_id (int): The primary key id of the allergy to retrieve.

        Returns:
            tuple|None: A tuple matching the data shape described in the
            class docstring, or None if the row was not found or an error
            occurred.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, allergen_name, danger_level, symptoms, ingredients, source, notes, created_date FROM allergies WHERE id = ?",
                    (allergy_id,),
                )
                row = cursor.fetchone()
            return row
        except Exception as e:
            print(f"Error getting allergy: {e}")
            return None

    def update_allergy(
        self,
        allergy_id,
        allergen_name,
        danger_level,
        symptoms,
        ingredients,
        source,
        notes,
    ):
        """Update an existing allergy row.

        Parameters:
            allergy_id (int): Primary key id of the row to update.
            allergen_name (str): New allergen name (should remain unique).
            danger_level (int): New danger rating.
            symptoms (str|None): New symptoms text.
            ingredients (str|None): New ingredients text.
            source (str|None): New source text.
            notes (str|None): New notes text.

        Returns:
            bool: True if the update succeeded, False on error.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE allergies
                    SET allergen_name = ?, danger_level = ?, symptoms = ?, ingredients = ?, source = ?, notes = ?
                    WHERE id = ?
                    """,
                    (
                        allergen_name,
                        danger_level,
                        symptoms,
                        ingredients,
                        source,
                        notes,
                        allergy_id,
                    ),
                )
            return True
        except Exception as e:
            print(f"Error updating allergy: {e}")
            return False

    def get_all_allergies(self, danger_level: int | None = None):
        """Retrieve all allergies, optionally filtering by danger_level.

        Parameters:
            danger_level (int|None): If provided, only rows with this
                danger_level are returned.

        Returns:
            list[tuple]: Rows matching the query.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if danger_level is None:
                cursor.execute(
                    "SELECT id, allergen_name, danger_level, symptoms, ingredients, source, notes, created_date "
                    "FROM allergies ORDER BY danger_level DESC, allergen_name"
                )
            else:
                cursor.execute(
                    "SELECT id, allergen_name, danger_level, symptoms, ingredients, source, notes, created_date "
                    "FROM allergies WHERE danger_level = ? ORDER BY danger_level DESC, allergen_name",
                    (danger_level,),
                )
            return cursor.fetchall()

    def search_allergies(self, search_term: str, danger_level: int | None = None):
        """Search allergies by name/ingredients with optional danger_level filter.

        Parameters:
            search_term (str): Partial term (case-insensitive) to match.
            danger_level (int|None): Optional danger level to restrict results.

        Returns:
            list[tuple]: Matching rows.
        """
        pattern = f"%{search_term.lower()}%"
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if danger_level is None:
                cursor.execute(
                    """
                    SELECT id, allergen_name, danger_level, symptoms, ingredients, source, notes, created_date
                    FROM allergies
                    WHERE LOWER(allergen_name) LIKE ? OR LOWER(ingredients) LIKE ?
                    ORDER BY danger_level DESC, allergen_name
                    """,
                    (pattern, pattern),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, allergen_name, danger_level, symptoms, ingredients, source, notes, created_date
                    FROM allergies
                    WHERE danger_level = ? AND (LOWER(allergen_name) LIKE ? OR LOWER(ingredients) LIKE ?)
                    ORDER BY danger_level DESC, allergen_name
                    """,
                    (danger_level, pattern, pattern),
                )
            return cursor.fetchall()

    def import_from_csv(
        self, file_path: str, on_duplicate: str = "skip"
    ) -> Dict[str, Any]:
        """Import allergy rows from a CSV file into the database.

        Parameters:
            file_path (str): Path to the CSV file to import. The CSV should
                have a header row. Supported column names (case-insensitive):
                allergen_name, danger_level, symptoms, ingredients, source, notes
            on_duplicate (str): How to handle rows where allergen_name already
                exists. Supported values:
                  - 'skip' (default): do not change existing row and count as skipped
                  - 'update': update the existing row with the CSV values

        Returns:
            dict: A summary with keys: imported (int), updated (int), skipped (int), errors (list).
        """
        summary = {"imported": 0, "updated": 0, "skipped": 0, "errors": []}

        try:
            with open(file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                if not reader.fieldnames:
                    summary["errors"].append("CSV file has no header row")
                    return summary

                # Normalize fieldnames to lowercase for flexible headers
                field_map = {name.lower(): name for name in reader.fieldnames}

                for row_number, row in enumerate(reader, start=2):
                    try:
                        # Extract fields with flexible header names
                        allergen_name = row.get(
                            field_map.get("allergen_name", ""), ""
                        ).strip()
                        if not allergen_name:
                            summary["errors"].append(
                                f"Row {row_number}: missing allergen_name"
                            )
                            continue

                        danger_raw = row.get(
                            field_map.get("danger_level", ""), ""
                        ).strip()
                        try:
                            danger_level = int(danger_raw) if danger_raw else 1
                        except ValueError:
                            danger_level = 1

                        symptoms = (
                            row.get(field_map.get("symptoms", ""), "").strip()
                            or None
                        )
                        ingredients = (
                            row.get(
                                field_map.get("ingredients", ""), ""
                            ).strip()
                            or None
                        )
                        source = (
                            row.get(field_map.get("source", ""), "").strip()
                            or None
                        )
                        notes = (
                            row.get(field_map.get("notes", ""), "").strip()
                            or None
                        )

                        # Attempt to insert; if duplicate and on_duplicate == 'update', perform update
                        added = False
                        try:
                            added = self.add_allergy(
                                allergen_name,
                                danger_level,
                                symptoms,
                                ingredients,
                                source,
                                notes,
                            )
                        except Exception:
                            # add_allergy already catches exceptions and returns False
                            added = False

                        if added:
                            summary["imported"] += 1
                        else:
                            # If the row already exists (unique constraint), handle according to on_duplicate
                            if on_duplicate == "update":
                                # Find existing row id
                                with sqlite3.connect(self.db_name) as conn:
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        "SELECT id FROM allergies WHERE LOWER(allergen_name) = ?",
                                        (allergen_name.lower(),),
                                    )
                                    existing = cursor.fetchone()
                                if existing:
                                    existing_id = existing[0]
                                    ok = self.update_allergy(
                                        existing_id,
                                        allergen_name,
                                        danger_level,
                                        symptoms,
                                        ingredients,
                                        source,
                                        notes,
                                    )
                                    if ok:
                                        summary["updated"] += 1
                                    else:
                                        summary["errors"].append(
                                            f"Row {row_number}: failed to update existing allergen '{allergen_name}'"
                                        )
                                else:
                                    # No existing row found but add failed: count as skipped
                                    summary["skipped"] += 1
                            else:
                                summary["skipped"] += 1

                    except Exception as e:
                        summary["errors"].append(f"Row {row_number}: {e}")

        except FileNotFoundError:
            summary["errors"].append(f"File not found: {file_path}")
        except Exception as e:
            summary["errors"].append(str(e))

        return summary

    def delete_allergy(self, allergy_id):
        """Delete an allergy entry by ID.

        Parameters:
            allergy_id (int): Primary key id of the allergy to delete.

        Returns:
            bool: True if deletion succeeded, False on error.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM allergies WHERE id = ?", (allergy_id,)
                )
            return True
        except Exception as e:
            print(f"Error deleting allergy: {e}")
            return False
