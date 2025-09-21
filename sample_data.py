#!/usr/bin/env python3
"""
Sample data script for the Allergy Database application.
This script adds some common allergies to the database for testing purposes.
"""

import sqlite3
import os

def add_sample_data():
    """Add sample allergy data to the database"""
    db_name = "allergies.db"
    
    # Sample allergy data
    sample_allergies = [
        {
            'allergen_name': 'Peanuts',
            'danger_level': 4,
            'symptoms': 'Anaphylaxis, difficulty breathing, swelling of face and throat, hives, rapid pulse',
            'ingredients': 'Peanut oil, peanut flour, peanut butter, groundnuts, arachis oil, mixed nuts',
            'notes': 'Carry EpiPen at all times. Avoid all products processed in facilities that handle peanuts.'
        },
        {
            'allergen_name': 'Milk',
            'danger_level': 2,
            'symptoms': 'Stomach pain, bloating, diarrhea, nausea, gas',
            'ingredients': 'Lactose, casein, whey, butter, cream, cheese, yogurt, milk powder',
            'notes': 'Lactose-free alternatives available. Severity varies with amount consumed.'
        },
        {
            'allergen_name': 'Shellfish',
            'danger_level': 3,
            'symptoms': 'Hives, vomiting, difficulty swallowing, abdominal pain, dizziness',
            'ingredients': 'Shrimp, crab, lobster, crawfish, mollusks, oysters, clams, mussels',
            'notes': 'Cross-contamination risk high in seafood restaurants. Often develops in adulthood.'
        },
        {
            'allergen_name': 'Tree Nuts',
            'danger_level': 4,
            'symptoms': 'Anaphylaxis, swelling, difficulty breathing, skin reactions',
            'ingredients': 'Almonds, walnuts, pecans, cashews, pistachios, brazil nuts, hazelnuts, macadamia nuts',
            'notes': 'Different tree nuts may cause different severities. Some people allergic to only specific nuts.'
        },
        {
            'allergen_name': 'Eggs',
            'danger_level': 2,
            'symptoms': 'Skin rash, stomach upset, respiratory problems, runny nose',
            'ingredients': 'Albumin, egg whites, egg yolks, mayonnaise, meringue, custard, lecithin',
            'notes': 'Often outgrown by adolescence. Some people can tolerate baked eggs but not raw.'
        },
        {
            'allergen_name': 'Soy',
            'danger_level': 1,
            'symptoms': 'Mild stomach upset, skin irritation, runny nose',
            'ingredients': 'Soy sauce, tofu, tempeh, soy milk, soy protein, edamame, miso',
            'notes': 'Common in processed foods. Often mild reactions. Check labels carefully.'
        },
        {
            'allergen_name': 'Wheat',
            'danger_level': 2,
            'symptoms': 'Digestive issues, skin problems, respiratory symptoms, headache',
            'ingredients': 'Wheat flour, gluten, bread, pasta, cereals, crackers, beer',
            'notes': 'Different from celiac disease. May be able to tolerate other grains like rice and corn.'
        },
        {
            'allergen_name': 'Fish',
            'danger_level': 3,
            'symptoms': 'Hives, swelling, gastrointestinal problems, respiratory issues',
            'ingredients': 'Salmon, tuna, cod, halibut, anchovies, fish sauce, worcestershire sauce',
            'notes': 'May be allergic to specific types of fish only. Cross-contamination risk in restaurants.'
        },
        {
            'allergen_name': 'Sesame',
            'danger_level': 3,
            'symptoms': 'Anaphylaxis, hives, difficulty breathing, gastrointestinal symptoms',
            'ingredients': 'Sesame seeds, tahini, sesame oil, hummus, halva, some bread toppings',
            'notes': 'Increasingly recognized allergen. Now required to be labeled in many countries.'
        },
        {
            'allergen_name': 'Strawberries',
            'danger_level': 1,
            'symptoms': 'Oral allergy syndrome, mild hives, itchy mouth and throat',
            'ingredients': 'Fresh strawberries, strawberry flavoring, strawberry jam, smoothies',
            'notes': 'Often part of oral allergy syndrome. May be related to birch pollen allergy.'
        }
    ]
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
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
        
        # Insert sample data
        added_count = 0
        for allergy in sample_allergies:
            try:
                cursor.execute('''
                    INSERT INTO allergies (allergen_name, danger_level, symptoms, ingredients, notes)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    allergy['allergen_name'],
                    allergy['danger_level'],
                    allergy['symptoms'],
                    allergy['ingredients'],
                    allergy['notes']
                ))
                added_count += 1
                print(f"✓ Added: {allergy['allergen_name']}")
            except sqlite3.IntegrityError:
                print(f"⚠ Skipped: {allergy['allergen_name']} (already exists)")
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ Successfully added {added_count} new allergies to the database!")
        print(f"📊 Database file: {os.path.abspath(db_name)}")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")

def show_database_contents():
    """Display current contents of the database"""
    db_name = "allergies.db"
    
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM allergies')
        count = cursor.fetchone()[0]
        
        print(f"\n📋 Current database contains {count} allergies:")
        
        cursor.execute('SELECT allergen_name, danger_level FROM allergies ORDER BY danger_level DESC, allergen_name')
        allergies = cursor.fetchall()
        
        danger_labels = {1: 'Mild', 2: 'Moderate', 3: 'Severe', 4: 'Life-threatening'}
        
        for name, level in allergies:
            print(f"  • {name} (Level {level}: {danger_labels[level]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == '__main__':
    print("🏥 Food Allergy Database - Sample Data Setup")
    print("=" * 50)
    
    add_sample_data()
    show_database_contents()
    
    print("\n🚀 You can now run the main application:")
    print("   python allergy_database.py")
