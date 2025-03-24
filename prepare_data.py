import pandas as pd
import os

# Define paths for Food-101 dataset
IMAGE_BASE_PATH = "dataset/food-101/images/"
META_PATH = "dataset/food-101/meta/"

# Ensure recipes.txt exists
if not os.path.exists("recipes.txt"):
    print("❌ Error: recipes.txt not found!")
    exit()

# ✅ Load image mappings from train.txt and test.txt
image_mappings = {}

for meta_file in ["train.txt", "test.txt"]:  # Load both training and test images
    meta_path = os.path.join(META_PATH, meta_file)
    if os.path.exists(meta_path):
        with open(meta_path, "r") as file:
            for line in file:
                category, filename = line.strip().split("/")  # Extract category and filename
                image_mappings.setdefault(category, []).append(filename + ".jpg")

# ✅ Load Recipes from recipes.txt
recipes = []
with open("recipes.txt", "r") as file:
    for line in file:
        parts = line.strip().split(" | ")  # Correct separator for recipes.txt

        if len(parts) >= 2:  # Ensure we have at least a recipe name & ingredients
            food = parts[0].strip()  # Recipe name
            
            # ✅ Extract ingredients correctly
            ingredients_section = next((p for p in parts if p.startswith("Ingredients:")), "")
            ingredients = ingredients_section.replace("Ingredients:", "").strip()

            # Handle missing ingredients
            if not ingredients:
                ingredients = "Unknown"
        else:
            # If the format is incorrect, assign defaults
            food = line.strip()
            ingredients = "Unknown"

        # ✅ Assign the Correct Image from Food-101
        image_url = "/static/images/default.jpg"  # Default image
        if food in image_mappings and image_mappings[food]:  # Ensure images exist
            for image_filename in image_mappings[food]:  # Check for a valid image
                image_path = os.path.join(IMAGE_BASE_PATH, food, image_filename)
                if os.path.exists(image_path):
                    image_url = f"/dataset/food-101/images/{food}/{image_filename}"
                    break  # Use the first valid image
            else:
                print(f"🚨 No valid images found for: {food}, using default.")
        else:
            print(f"⚠️ No image mapping found for: {food}, using default.")

        # ✅ Classify Recipe by Dietary Type
        ingredients_lower = str(ingredients).lower() if pd.notna(ingredients) else "unknown"

        if any(x in ingredients_lower for x in ["chicken", "beef", "pork", "fish", "shrimp", "bacon"]):
            dietary = "non-veg"
        elif any(x in ingredients_lower for x in ["wheat", "flour", "barley", "rye"]):
            dietary = "gluten-free"
        else:
            dietary = "vegetarian"

        # ✅ Auto-Generate Cooking Steps
        cooking_steps = (
            "Gather all ingredients. | Preheat oven or prepare a cooking pan. | "
            "Prepare the ingredients by chopping, mixing, or seasoning as needed. | "
            "Cook the ingredients using the appropriate method (baking, frying, steaming, etc.). | "
            "Adjust seasonings to taste and allow the dish to rest if needed. | "
            "Serve hot and enjoy!"
        )

        # ✅ Store Data Correctly (No Duplicates!)
        recipes.append({
            "recipe": food,
            "ingredients": ingredients,  # ✅ Properly extracted ingredients
            "image_url": image_url,
            "dietary": dietary,
            "instructions": cooking_steps  # ✅ Only cooking steps here
        })

# ✅ Convert to DataFrame and Save to `recipes.csv`
df = pd.DataFrame(recipes, columns=["recipe", "ingredients", "image_url", "dietary", "instructions"])
df.to_csv("recipes.csv", index=False)

print("✅ recipes.csv updated with valid images, dietary info & cooking steps!")
