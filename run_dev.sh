#!/bin/bash
# Unix/Linux shell script for running Food Allergy Shield in development mode

echo "🚀 Starting Food Allergy Shield in development mode..."
echo

# Check if we're in the right directory
if [ ! -f "src/foodallergyshield/food_allergy_shield.py" ]; then
    echo "❌ Error: Cannot find src/foodallergyshield/food_allergy_shield.py"
    echo "💡 Make sure you're running this from the project root directory"
    exit 1
fi

# Copy database if needed
if [ -f "data/food_allergies.db" ] && [ ! -f "src/foodallergyshield/food_allergies.db" ]; then
    echo "📋 Copying database for development..."
    cp "data/food_allergies.db" "src/foodallergyshield/food_allergies.db"
fi

# Run the development script
python3 run_dev.py

# Check exit status
if [ $? -ne 0 ]; then
    echo
    echo "❌ Application exited with an error"
    read -p "Press Enter to continue..."
fi