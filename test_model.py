import joblib
import pandas as pd

from src.feature_engineering import extract_url_features


# Load model and feature names
model = joblib.load("models/phishguard_model.joblib")
feature_names = joblib.load("models/feature_names.joblib")


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

legitimate_probability = class_probabilities.get(0, 0)
phishing_probability = class_probabilities.get(1, 0)


# Display result
result = "PHISHING" if prediction == 1 else "LEGITIMATE"

print("\n" + "=" * 50)
print("PHISHGUARD URL ANALYSIS")
print("=" * 50)

print(f"URL: {test_url}")
print(f"Prediction: {result}")
print(f"Legitimate Probability: {legitimate_probability:.2%}")
print(f"Phishing Probability: {phishing_probability:.2%}")

print("\nExtracted Features:")
for name, value in features.items():
    print(f"{name}: {value}")

print("=" * 50)