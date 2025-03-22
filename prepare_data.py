import pandas as pd
import os

# Define paths for Food-101 dataset
IMAGE_BASE_PATH = "dataset/food-101/images/"
META_PATH = "dataset/food-101/meta/"

# Ensure recipes.txt exists
if not os.path.exists("recipes.txt"):
    print("❌ Error: recipes.txt not found!")
    exit()

# ✅ **Step 1: Load Correct Image Mappings from train.txt and test.txt**
image_mappings = {}

for meta_file in ["train.txt", "test.txt"]:  # Load both training and test images
    meta_path = os.path.join(META_PATH, meta_file)
    if os.path.exists(meta_path):
        with open(meta_path, "r") as file:
            for line in file:
                line = line.strip()
                category, filename = line.split("/")  # Extract category and filename
                if category not in image_mappings:
                    image_mappings[category] = []
                image_mappings[category].append(filename + ".jpg")  # Add .jpg extension

# ✅ **Step 2: Load Recipes from recipes.txt**
recipes = []
with open("recipes.txt", "r") as file:
    for line in file:
        parts = line.strip().split(" ", 1)
        if len(parts) == 2:
            food, ingredients = parts

            # ✅ **Step 3: Assign the Correct Image from Food-101**
            if food in image_mappings and image_mappings[food]:  # Ensure images exist
                image_filename = image_mappings[food][0]  # Pick the first image in the list
                image_url = f"/dataset/food-101/images/{food}/{image_filename}"
            else:
                image_url = "/static/images/default.jpg"  # Default image if missing

            # ✅ **Step 4: Classify Recipe by Dietary Type**
            ingredients_lower = ingredients.lower()
            if any(x in ingredients_lower for x in ["chicken", "beef", "pork", "fish", "egg", "shrimp", "bacon"]):
                dietary = "non-veg"
            elif any(x in ingredients_lower for x in ["wheat", "flour", "barley", "rye"]):
                dietary = "gluten-free"
            else:
                dietary = "vegetarian"

            # ✅ **Step 5: Auto-Generate Cooking Steps**
            cooking_steps = [
                f"Gather all ingredients: {ingredients}.",
                "Preheat oven or prepare a cooking pan.",
                "Prepare the ingredients by chopping, mixing, or seasoning as needed.",
                "Cook the ingredients using the appropriate method (baking, frying, steaming, etc.).",
                "Adjust seasonings to taste and allow the dish to rest if needed.",
                "Serve hot and enjoy!"
            ]

            # ✅ **Step 6: Save the Recipe Data**
            recipes.append({
                "recipe": food,
                "ingredients": ingredients,
                "image_url": image_url,
                "dietary": dietary,
                "instructions": " | ".join(cooking_steps)  # Store as a single text field
            })

# ✅ **Step 7: Convert to DataFrame and Save to recipes.csv**
df = pd.DataFrame(recipes)
df.to_csv("recipes.csv", index=False)

print("✅ recipes.csv updated with correct Food-101 image filenames & cooking steps!")
