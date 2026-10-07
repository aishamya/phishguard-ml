# 🛡️ PHISHGUARD — Explainable Phishing URL Detection

> Detect. Explain. Protect.

PhishGuard is an AI-powered phishing URL detection system that uses machine learning to identify suspicious URLs and explain why they may be dangerous.

## 🚀 Live Demo

Streamlit App: https://phishguard-ml-bvatrewbz...streamlit.app

## 🎯 Problem

Phishing attacks use deceptive URLs to trick users into revealing passwords, banking details, and other sensitive information.

PhishGuard goes beyond simply classifying a URL by explaining the security signals that make it suspicious.

## 💡 Solution

PhishGuard analyzes URL structure using 20 engineered features and a Random Forest machine learning model.

URL / QR Code
→ Feature Extraction
→ Random Forest Model
→ Phishing Probability
→ Risk Score
→ Explainable Security Result

## 🧠 Machine Learning

Dataset:
- 127,726 labelled URLs
- 79,622 phishing URLs
- 48,104 legitimate URLs
- 20 URL features
- 80/20 stratified train-test split

Models compared:
- Logistic Regression
- Decision Tree
- Random Forest

Final Model: Random Forest

Performance:
- Accuracy: 89.04%
- Precision: 93.42%
- Recall: 88.66%
- F1 Score: 90.98%

## 🔍 URL Features

The system analyzes:

- URL length
- Domain length
- Path length
- Dot count
- Slash count
- Hyphen count
- Digit count
- Special characters
- @ symbol
- IP address usage
- HTTPS usage
- Suspicious keywords
- Subdomain count
- Query parameters
- Domain character statistics
- Domain entropy

## 🛡️ Explainable Risk Analysis

PhishGuard generates a separate heuristic risk score from 0–100.

Security signals include:
- IP address in URL
- @ symbol
- Suspicious keywords
- Excessive URL length
- Multiple subdomains
- Multiple query parameters
- Lack of HTTPS

Risk levels:
- 0–39: LOW
- 40–69: MEDIUM
- 70–100: HIGH

The heuristic risk score is separate from the Random Forest phishing probability.

## 📱 QR Code Analysis

PhishGuard can decode QR codes containing URLs and analyze the extracted destination using the same phishing detection pipeline.

Upload QR Code
→ Decode Destination
→ Extract URL
→ Run ML Analysis
→ Display Security Result

## ✨ Key Features

- Real-time URL analysis
- Machine learning phishing detection
- Phishing and legitimate probabilities
- Risk score
- Security signals
- Explainable results
- QR-code URL analysis
- Feature importance
- Model performance information

## 🛠️ Tech Stack

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- OpenCV
- Joblib

## 📁 Project Structure

phishguard-ml/
- models/
  - feature_names.joblib
  - metadata.joblib
  - phishguard_model.joblib
- src/
  - feature_engineering.py
- app.py
- test_model.py
- requirements.txt
- README.md

## ⚙️ Run Locally

Clone the repository:

git clone https://github.com/aishamya/phishguard-ml.git

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

## 🧪 Safe Demo

Use this synthetic URL for demonstration:

http://secure-login-verify-account.example/login

The .example domain is used for safe demonstration purposes and does not represent a real phishing website.

## 🔐 Safety

PhishGuard analyzes URL characteristics without opening suspicious websites.

It is intended for educational and defensive cybersecurity purposes.

## ⚠️ Limitations

- URL-based detection cannot guarantee that a website is safe.
- New phishing techniques may not be represented in the training dataset.
- The system primarily analyzes URL-level characteristics.
- Predictions should be treated as a security aid rather than absolute proof.

## 🔮 Future Scope

- Real-time threat intelligence
- WHOIS and domain-age analysis
- DNS and certificate analysis
- Browser extension
- Shortened URL detection
- Continuously updated datasets
- Advanced explainability

## 👥 Team

PHISHGUARD

Built as a semester-end hackathon project focused on AI-powered cybersecurity and explainable machine learning.
