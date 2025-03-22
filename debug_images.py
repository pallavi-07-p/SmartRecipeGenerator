import pandas as pd

# Load the recipes dataset
df = pd.read_csv("recipes.csv")

# Convert all recipe names to lowercase for comparison
df["recipe"] = df["recipe"].str.lower()

# Search for "bread_pudding"
recipe_name = "bread_pudding"

# Check if the recipe exists
recipe_data = df[df["recipe"] == recipe_name]

if not recipe_data.empty:
    print(f"✅ Recipe Found: {recipe_name}")
    print("📜 Instructions:", recipe_data["instructions"].values[0])
else:
    print(f"🚨 ERROR: Recipe '{recipe_name}' NOT FOUND in recipes.csv")

