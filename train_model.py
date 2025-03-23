import numpy as np
import tensorflow as tf
from tensorflow import keras
import pickle

# Load processed data
X = np.load("X.npy")
y = np.load("y.npy")

# Define the Neural Network
model = keras.Sequential([
    keras.layers.Dense(128, activation="relu", input_shape=(X.shape[1],)),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(len(y), activation="softmax")  # Output layer (one neuron per recipe)
])

# Compile the model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Train the model
model.fit(X, y, epochs=10, batch_size=8, validation_split=0.2)

# Save the trained model
model.save("recipe_model.h5")
print("✅ Model training complete!")
