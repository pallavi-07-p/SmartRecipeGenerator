import pandas as pd

# Load recipes from CSV
df = pd.read_csv("recipes.csv")

# Write to recipes.txt including ingredients and instructions
with open("recipes.txt", "w", encoding="utf-8") as file:
    for index, row in df.iterrows():
        recipe = str(row["recipe"]).strip()
        
        # Convert NaN values to 'Not available' and ensure values are strings
        ingredients = str(row["ingredients"]).strip() if pd.notna(row["ingredients"]) else "Not available"
        instructions = str(row["instructions"]).strip() if pd.notna(row["instructions"]) else "Not available"
        
        # Write recipe details in a readable format
        file.write(f"{recipe} | Ingredients: {ingredients} | Instructions: {instructions}\n")

print("✅ recipes.txt created successfully with cooking instructions.")
