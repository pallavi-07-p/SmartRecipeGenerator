import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle

# Load dataset
df = pd.read_csv("recipes.csv")

# Convert ingredients into numerical vectors using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(df["ingredients"])

# Convert recipes into labels (using indices)
y = np.arange(len(df))

# Save vectorizer and processed data
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

np.save("X.npy", X.toarray())
np.save("y.npy", y)

print("✅ Data preprocessing complete!")
