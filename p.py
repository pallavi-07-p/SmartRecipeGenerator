import pandas as pd

df = pd.read_csv("recipes.csv")

# Print apple_pie details
print(df[df["recipe"] == "apple_pie"])



