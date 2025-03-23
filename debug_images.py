import pandas as pd

# Load the dataset
df = pd.read_csv("recipes.csv")

# Check if 'instructions' column exists
print("Columns in CSV:", df.columns)

# Check if "apple_pie" exists
recipe_name = "apple_pie"
recipe_data = df[df["recipe"].str.lower().str.strip() == recipe_name.strip()]

if not recipe_data.empty:
    instructions = recipe_data["instructions"].values[0]
    print("✅ Found Instructions:", instructions.split(" | "))
else:
    print("🚨 No Instructions Found")







