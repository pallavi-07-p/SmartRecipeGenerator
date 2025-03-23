import pandas as pd
import os

# Define paths for Food-101 dataset
IMAGE_BASE_PATH = "dataset/food-101/images/"
META_PATH = "dataset/food-101/meta/"

# Ensure recipes.txt exists
if not os.path.exists("recipes.txt"):
    print("❌ Error: recipes.txt not found!")
    exit()

# ✅ Step 1: Load Image Mappings with Validation
image_mappings = {}

for category in os.listdir(IMAGE_BASE_PATH):  # Loop through categories
    category_path = os.path.join(IMAGE_BASE_PATH, category)
    if os.path.isdir(category_path):
        valid_images = [img for img in os.listdir(category_path) if img.endswith(".jpg")]
        image_mappings[category] = valid_images[:100]  # Keep only first 100 images

# ✅ Step 2: Load Recipes from `recipes.txt`
recipes = []
with open("recipes.txt", "r") as file:
    for line in file:
        parts = line.strip().split(" ", 1)
        if len(parts) == 2:
            food, ingredients = parts

            # ✅ Step 3: Assign a Valid Image from Food-101
            image_url = "/static/images/default.jpg"  # Default image
            if food in image_mappings and image_mappings[food]:  # Ensure images exist
                for image_filename in image_mappings[food]:  # Check for a valid image
                    image_path = os.path.join(IMAGE_BASE_PATH, food, image_filename)
                    if os.path.exists(image_path):
                        image_url = f"/dataset/food-101/images/{food}/{image_filename}"
                        break  # Use the first valid image
                else:
                    print(f"🚨 No valid images found for: {food}, using default.")

            # ✅ Step 4: Classify Recipe by Dietary Type
            ingredients_lower = ingredients.lower()
            if any(x in ingredients_lower for x in ["chicken", "beef", "pork", "fish", "shrimp", "bacon"]):
                dietary = "non-veg"
            elif any(x in ingredients_lower for x in ["wheat", "flour", "barley", "rye"]):
                dietary = "gluten-free"
            else:
                dietary = "vegetarian"

            # ✅ Step 5: Auto-Generate Cooking Steps
            cooking_steps = [
                f"Gather all ingredients: {ingredients}.",
                "Preheat oven or prepare a cooking pan.",
                "Prepare the ingredients by chopping, mixing, or seasoning as needed.",
                "Cook the ingredients using the appropriate method (baking, frying, steaming, etc.).",
                "Adjust seasonings to taste and allow the dish to rest if needed.",
                "Serve hot and enjoy!"
            ]

            # ✅ Step 6: Save the Recipe Data
            recipes.append({
                "recipe": food,
                "ingredients": ingredients,
                "image_url": image_url,
                "dietary": dietary,
                "instructions": " | ".join(cooking_steps)  # Store as a single text field
            })

# ✅ Step 7: Convert to DataFrame and Save to `recipes.csv`
df = pd.DataFrame(recipes)
df.to_csv("recipes.csv", index=False)

print("✅ recipes.csv updated with valid images, dietary info & cooking steps!")
