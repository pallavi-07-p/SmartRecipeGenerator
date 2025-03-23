import pandas as pd

# Load recipes.csv
df = pd.read_csv("recipes.csv")

# Check if the 'instructions' column exists and print a sample
if "instructions" in df.columns:
    print("✅ 'instructions' column found!")
    print(df[["recipe", "instructions"]].head())  # Print first few rows
else:
    print("❌ 'instructions' column NOT found!")




