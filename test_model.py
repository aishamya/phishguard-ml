import os
import sys
import joblib
import pandas as pd


# Allow Python to find our feature extraction module
sys.path.append(os.path.abspath("src"))

from feature_engineering import extract_url_features


# Load trained model
model = joblib.load("models/phishguard_model.joblib")

# Load feature names used during training
feature_names = joblib.load("models/feature_names.joblib")

print("Model loaded successfully!")
print("Feature names loaded successfully!")


# Test URL
test_url = "https://www.wikipedia.org"

# Extract features
features = extract_url_features(test_url)

# Convert features into DataFrame
input_df = pd.DataFrame([features], columns=feature_names)


# Make prediction
prediction = model.predict(input_df)[0]

# Get probabilities
probabilities = model.predict_proba(input_df)[0]

class_probabilities = dict(
    zip(model.classes_, probabilities)
)

phishing_probability = class_probabilities.get(1, 0)
legitimate_probability = class_probabilities.get(0, 0)


# Display results
print("\nURL:", test_url)
print("Prediction:", "PHISHING" if prediction == 1 else "LEGITIMATE")
print("Phishing probability:", round(phishing_probability * 100, 2), "%")
print("Legitimate probability:", round(legitimate_probability * 100, 2), "%")

print("\nExtracted features:")
print(input_df.to_string(index=False))
print("\nFeature importance:")
for name, importance in zip(feature_names, model.feature_importances_):
    print(f"{name}: {importance:.4f}")