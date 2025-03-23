import pandas as pd

# Load the dataset
df = pd.read_csv("recipes.csv")

# Check for missing instructions
missing_instructions = df[df["instructions"].isna() | (df["instructions"].str.strip() == "")]
if missing_instructions.empty:
    print("✅ All recipes have instructions!")
else:
    print("🚨 Some recipes are missing instructions:")
    print(missing_instructions[["recipe", "instructions"]])
