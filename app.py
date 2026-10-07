import streamlit as st
import joblib
import pandas as pd

from src.feature_engineering import extract_url_features


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PhishGuard | URL Security",
    page_icon="🛡️",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0b0f14;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

.hero {
    text-align: center;
    padding: 30px 0 20px 0;
}

.hero-title {
    font-size: 52px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 20px;
    color: #9aa4b2;
}

.tagline {
    font-size: 15px;
    color: #00d4ff;
    letter-spacing: 3px;
    font-weight: 600;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 12px;
}

.signal {
    background: #151b23;
    border: 1px solid #26303c;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 8px 0;
}

.safe-signal {
    background: #101a18;
    border: 1px solid #1d5147;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 8px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    model = joblib.load("models/phishguard_model.joblib")
    feature_names = joblib.load("models/feature_names.joblib")
    return model, feature_names


model, feature_names = load_model()


# =========================================================
# RISK SCORE
# =========================================================

def calculate_risk_score(features):

    score = 0
    signals = []

    if features["has_ip"] == 1:
        score += 25
        signals.append(
            "Uses an IP address instead of a domain name"
        )

    if features["has_at"] == 1:
        score += 20
        signals.append(
            "Contains an @ symbol"
        )

    keyword_count = features["suspicious_keyword_count"]

    if keyword_count >= 3:
        score += 25
        signals.append(
            f"Contains {keyword_count} suspicious security-related keywords"
        )

    elif keyword_count >= 1:
        score += 10
        signals.append(
            f"Contains {keyword_count} suspicious security-related keyword"
        )

    if features["url_length"] >= 100:
        score += 15
        signals.append(
            "Unusually long URL"
        )

    if features["subdomain_count"] >= 3:
        score += 10
        signals.append(
            "Multiple subdomains detected"
        )

    if features["query_parameter_count"] >= 3:
        score += 5
        signals.append(
            "Multiple query parameters"
        )

    if features["has_https"] == 0:
        score += 10
        signals.append(
            "URL does not use HTTPS"
        )

    score = min(score, 100)

    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return score, risk_level, signals


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-title">🛡️ PHISHGUARD</div>

<div class="hero-subtitle">
Explainable Phishing URL Detection
</div>

<br>

<div class="tagline">
DETECT · EXPLAIN · PROTECT
</div>

</div>
""", unsafe_allow_html=True)


st.markdown(
    "Enter a URL below. PhishGuard analyzes its structural and security "
    "characteristics using a machine-learning model."
)


# =========================================================
# URL INPUT
# =========================================================

url = st.text_input(
    "URL TO ANALYZE",
    placeholder="https://example.com/login",
    label_visibility="visible"
)


analyze = st.button(
    "🔍  ANALYZE URL",
    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    if not url.strip():

        st.warning("Please enter a URL.")

    else:

        # -------------------------------------------------
        # Feature extraction
        # -------------------------------------------------

        features = extract_url_features(url)

        input_df = pd.DataFrame(
            [features],
            columns=feature_names
        )

        # -------------------------------------------------
        # Model prediction
        # -------------------------------------------------

        prediction = model.predict(input_df)[0]

        probabilities = model.predict_proba(input_df)[0]

        class_probabilities = dict(
            zip(model.classes_, probabilities)
        )

        legitimate_probability = class_probabilities.get(0, 0)
        phishing_probability = class_probabilities.get(1, 0)

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        if prediction == 1:
            result = "PHISHING"
        else:
            result = "LEGITIMATE"

        # -------------------------------------------------
        # Risk score
        # -------------------------------------------------

        risk_score, risk_level, signals = calculate_risk_score(
            features
        )

        # =================================================
        # RESULT
        # =================================================

        st.divider()

        if result == "PHISHING":

            st.error(
                "🚨 PHISHING URL DETECTED"
            )

        else:

            st.success(
                "✅ URL CLASSIFIED AS LEGITIMATE"
            )

        st.markdown(
            f"**Analyzed URL:** `{url}`"
        )


        # =================================================
        # MAIN METRICS
        # =================================================

        st.markdown(
            '<div class="section-title">Security Assessment</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Phishing Probability",
                f"{phishing_probability:.2%}"
            )

        with col2:

            st.metric(
                "Risk Score",
                f"{risk_score}/100"
            )

        with col3:

            st.metric(
                "Risk Level",
                risk_level
            )


        # =================================================
        # PROBABILITY
        # =================================================

        st.markdown(
            '<div class="section-title">Model Confidence</div>',
            unsafe_allow_html=True
        )

        st.progress(
            float(phishing_probability)
        )

        st.caption(
            f"Model phishing probability: "
            f"{phishing_probability:.2%}"
        )


        # =================================================
        # SECURITY SIGNALS
        # =================================================

        st.markdown(
            '<div class="section-title">🔍 Security Signals</div>',
            unsafe_allow_html=True
        )

        if signals:

            for signal in signals:

                st.markdown(
                    f"""
                    <div class="signal">
                    ⚠️ {signal}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.markdown(
                """
                <div class="safe-signal">
                ✓ No major heuristic security signals detected.
                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # WHY WAS IT FLAGGED?
        # =================================================

        st.markdown(
            '<div class="section-title">💡 Why was this flagged?</div>',
            unsafe_allow_html=True
        )

        if result == "PHISHING":

            explanation_parts = []

            if features["suspicious_keyword_count"] > 0:
                explanation_parts.append(
                    "suspicious security-related keywords"
                )

            if features["url_length"] >= 100:
                explanation_parts.append(
                    "an unusually long URL"
                )

            if features["has_ip"] == 1:
                explanation_parts.append(
                    "an IP address instead of a domain"
                )

            if features["has_at"] == 1:
                explanation_parts.append(
                    "an @ symbol"
                )

            if features["subdomain_count"] >= 3:
                explanation_parts.append(
                    "multiple subdomains"
                )

            if explanation_parts:

                st.info(
                    "The model classified this URL as phishing. "
                    "Potentially suspicious characteristics include "
                    + ", ".join(explanation_parts)
                    + "."
                )

            else:

                st.info(
                    "The machine-learning model identified this URL "
                    "as phishing based on the combination of extracted "
                    "URL characteristics."
                )

        else:

            st.info(
                "The model classified this URL as legitimate based on "
                "the structural characteristics extracted from the URL. "
                "No classification guarantees that a website is completely safe."
            )


        # =================================================
        # FEATURE DETAILS
        # =================================================

        with st.expander("📊 View extracted URL features"):

            feature_df = pd.DataFrame(
                {
                    "Feature": list(features.keys()),
                    "Value": list(features.values())
                }
            )

            st.dataframe(
                feature_df,
                use_container_width=True,
                hide_index=True
            )


        # =================================================
        # MODEL INFORMATION
        # =================================================

        with st.expander("🤖 About the model"):

            st.write(
                "**Model:** Random Forest"
            )

            st.write(
                "**Features:** 20 URL-based features"
            )

            st.write(
                "**Accuracy:** 89.04%"
            )

            st.write(
                "**Precision:** 93.42%"
            )

            st.write(
                "**Recall:** 88.66%"
            )

            st.write(
                "**F1 Score:** 90.98%"
            )

            st.caption(
                "Metrics are based on the held-out test set used during model evaluation."
            )
            st.write("### Feature Importance")

            importance_df = pd.DataFrame({
                "Feature": feature_names,
                "Importance": model.feature_importances_
            })

            importance_df = importance_df.sort_values(
                "Importance",
                ascending=False
            )

            st.bar_chart(
                importance_df.set_index("Feature")
            )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "PHISHGUARD • Explainable Phishing URL Detection • "
    "Machine Learning + URL Security Analysis"
)