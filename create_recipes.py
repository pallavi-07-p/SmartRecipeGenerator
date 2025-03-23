import pandas as pd

# Load recipes from CSV
df = pd.read_csv("recipes.csv")

# Write to recipes.txt including ingredients and instructions
with open("recipes.txt", "w", encoding="utf-8") as file:
    for index, row in df.iterrows():
        recipe = row["recipe"]
        ingredients = row["ingredients"]
        instructions = row["instructions"]
        
        # Write recipe details in a readable format
        file.write(f"{recipe} | Ingredients: {ingredients} | Instructions: {instructions}\n")

print("✅ recipes.txt created successfully with cooking instructions.")
