from flask import Flask, request, render_template, send_from_directory, url_for, abort
import numpy as np
import pickle
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load TF-IDF vectorizer
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Load updated recipes dataset
df = pd.read_csv("recipes.csv")

# ✅ Correct dataset path
DATASET_PATH = os.path.abspath("dataset/food-101/images")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_recipe', methods=["POST"])
def get_recipe():
    try:
        print("\n🟢 Received a request to /get_recipe")

        # Get user input
        ingredients = request.form.get("ingredients", "").strip()
        diet = request.form.get("diet", "all").strip().lower()  # Default to 'all'
        print(f"📝 User Input: {ingredients}, Diet Preference: {diet}")

        # Convert input ingredients into a TF-IDF vector
        X_input = vectorizer.transform([ingredients])

        # Compute cosine similarity
        similarities = cosine_similarity(X_input, vectorizer.transform(df["ingredients"]))[0]

        # Get top 3 recipes
        top_indices = np.argsort(similarities)[-3:][::-1]
        print(f"🔍 Top 3 Similar Recipe Indices: {top_indices}")

        recipes = []
        for idx in top_indices:
            if 0 <= idx < len(df):
                recommended_recipe = df.iloc[idx]["recipe"]
                recommended_image = df.iloc[idx]["image_url"]
                recommended_ingredients = df.iloc[idx]["ingredients"]
                dietary = df.iloc[idx].get("dietary", "all").lower()

                # ✅ Check dietary preference
                if diet != "all" and dietary != diet:
                    print(f"🚫 Skipping {recommended_recipe} due to dietary mismatch ({dietary} != {diet})")
                    continue

                # ✅ Fix Image Path: Ensure the image exists
                image_parts = recommended_image.split("/")[-2:]  # Extract folder & file name
                local_image_path = os.path.join(DATASET_PATH, *image_parts)

                if not os.path.exists(local_image_path):
                    print(f"🚨 Missing Image: {local_image_path} - Using default image")
                    recommended_image = url_for("static", filename="images/default.jpg")
                else:
                    recommended_image = url_for("serve_image", category=image_parts[0], filename=image_parts[1])

                recipes.append({
                    "title": recommended_recipe,
                    "image_url": recommended_image,
                    "ingredients": recommended_ingredients,
                    "dietary": dietary
                })
                print(f"🍏 Recipe: {recommended_recipe}, 🏷️ Dietary: {dietary}, 🖼️ Image: {recommended_image}")

        if not recipes:
            return render_template("result.html", error="❌ No matching recipes found.")

        return render_template("result.html", recipes=recipes)

    except Exception as e:
        print(f"❌ Error in /get_recipe: {str(e)}")
        return render_template("result.html", error=f"❌ Error: {str(e)}")

# ✅ Route to serve images from dataset
@app.route('/dataset/food-101/images/<category>/<filename>')
def serve_image(category, filename):
    """ Serve images safely from dataset/food-101/images/ """
    image_dir = os.path.join(DATASET_PATH, category)
    image_path = os.path.join(image_dir, filename)

    print(f"🔍 Checking Image Path: {image_path}")

    if os.path.exists(image_path):
        return send_from_directory(image_dir, filename)
    else:
        print(f"🚨 Image Not Found: {image_path}")
        return abort(404, description="Image not found")  # Return 404 error

# ✅ Fix `view_process` to accept correct `recipe_name`
@app.route('/process/<recipe_name>')
def view_process(recipe_name):
    """ Fetch the cooking process from recipes.csv """
    formatted_name = recipe_name.replace("_", " ").strip().lower()
    print(f"🔍 Looking for recipe process: {formatted_name}")

    # Normalize recipe names for comparison
    df["recipe_normalized"] = df["recipe"].str.replace("_", " ").str.strip().str.lower()

    # Retrieve recipe details
    recipe_data = df[df["recipe_normalized"] == formatted_name]

    if not recipe_data.empty:
        process_steps = recipe_data.iloc[0]["instructions"]

        # ✅ Ensure instructions are not empty or NaN
        if pd.isna(process_steps) or process_steps.strip() == "":
            process_steps = ["❌ No instructions available."]
        else:
            process_steps = process_steps.split(" | ")  # Convert text to list
        
        print(f"✅ Found instructions for {formatted_name}: {process_steps}")
    else:
        process_steps = ["❌ No instructions available for this recipe."]
        print(f"🚨 No instructions found for {formatted_name}")

    return render_template("process.html", recipe_name=recipe_name, process=process_steps)

if __name__ == "__main__":
    app.run(debug=True)
