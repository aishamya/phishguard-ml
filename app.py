import streamlit as st
import joblib
import pandas as pd
import numpy as np
import cv2
import html

from src.feature_engineering import extract_url_features


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PHISHGUARD | AI Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    model = joblib.load(
        "models/phishguard_model.joblib"
    )

    feature_names = joblib.load(
        "models/feature_names.joblib"
    )

    return model, feature_names


model, feature_names = load_model()


# =========================================================
# HTML HELPER
# =========================================================

def html_block(content):
    st.html(content)


# =========================================================
# CSS
# =========================================================

html_block("""
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap'
);

html,
body {
    margin: 0 !important;
    padding: 0 !important;
}

.stApp {

    background:
        radial-gradient(
            circle at 10% 15%,
            rgba(139,92,246,0.14),
            transparent 27%
        ),

        radial-gradient(
            circle at 90% 20%,
            rgba(34,211,238,0.10),
            transparent 25%
        ),

        radial-gradient(
            circle at 50% 90%,
            rgba(139,92,246,0.08),
            transparent 30%
        ),

        #030305 !important;

    color: white !important;

    font-family:
        'Inter',
        sans-serif !important;
}


/* =====================================================
   ANIMATED GRID
   ===================================================== */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    background-image:

        linear-gradient(
            rgba(139,92,246,0.055) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(34,211,238,0.045) 1px,
            transparent 1px
        );

    background-size:
        65px 65px,
        65px 65px;

    animation:
        gridMove 16s linear infinite;

    pointer-events: none;

    z-index: 0;
}


/* =====================================================
   PERSPECTIVE FLOOR
   ===================================================== */

.stApp::after {

    content: "";

    position: fixed;

    inset: -50%;

    background-image:

        linear-gradient(
            rgba(255,255,255,0.018) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,255,255,0.018) 1px,
            transparent 1px
        );

    background-size:
        130px 130px,
        130px 130px;

    transform:
        perspective(500px)
        rotateX(62deg)
        translateY(20%);

    animation:
        floorMove 12s linear infinite;

    opacity: 0.5;

    pointer-events: none;

    z-index: 1;
}


/* =====================================================
   MOVING SCAN LINE
   ===================================================== */

body::before {

    content: "";

    position: fixed;

    top: -5px;

    left: 0;

    width: 100%;

    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #22d3ee,
            #8b5cf6,
            transparent
        );

    box-shadow:
        0 0 15px #22d3ee,
        0 0 35px #8b5cf6;

    z-index: 999;

    pointer-events: none;

    animation:
        scanScreen 7s linear infinite;
}


/* =====================================================
   ANIMATIONS
   ===================================================== */

@keyframes gridMove {

    from {
        background-position:
            0 0,
            0 0;
    }

    to {
        background-position:
            65px 65px,
            -65px 65px;
    }
}


@keyframes floorMove {

    from {
        background-position:
            0 0,
            0 0;
    }

    to {
        background-position:
            0 130px,
            130px 0;
    }
}


@keyframes scanScreen {

    0% {
        transform: translateY(0);
        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    50% {
        opacity: 1;
    }

    100% {
        transform: translateY(100vh);
        opacity: 0;
    }
}


@keyframes float {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-14px);
    }
}


@keyframes pulse {

    0%,
    100% {
        opacity: 0.5;
        transform: scale(1);
    }

    50% {
        opacity: 1;
        transform: scale(1.12);
    }
}


@keyframes reveal {

    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}


/* =====================================================
   HIDE STREAMLIT CHROME
   ===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* =====================================================
   NAVBAR
   ===================================================== */

.navbar {

    position: relative;

    z-index: 10;

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding:
        24px 7vw;

    border-bottom:
        1px solid
        rgba(255,255,255,0.07);

    background:
        rgba(3,3,5,0.45);

    backdrop-filter:
        blur(12px);
}


.logo {

    font-family:
        'Space Mono',
        monospace;

    font-size: 18px;

    font-weight: 700;

    letter-spacing: 3px;
}


.logo span {
    color: #8b5cf6;
}


.nav-status {

    display: flex;

    align-items: center;

    gap: 9px;

    font-family:
        'Space Mono',
        monospace;

    font-size: 10px;

    letter-spacing: 1.5px;

    color:
        rgba(255,255,255,0.45);
}


.status-dot {

    width: 7px;

    height: 7px;

    border-radius: 50%;

    background: #22c55e;

    box-shadow:
        0 0 10px #22c55e;

    animation:
        pulse 1.7s infinite;
}


/* =====================================================
   HERO
   ===================================================== */

.hero {

    position: relative;

    z-index: 5;

    min-height: 620px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    padding:
        80px 7vw;

    overflow: hidden;
}


.hero-orb {

    position: absolute;

    border-radius: 50%;

    filter: blur(75px);

    pointer-events: none;
}


.orb-one {

    width: 230px;

    height: 230px;

    background:
        rgba(139,92,246,0.13);

    top: 12%;

    right: 8%;

    animation:
        float 7s ease-in-out infinite;
}


.orb-two {

    width: 180px;

    height: 180px;

    background:
        rgba(34,211,238,0.10);

    bottom: 12%;

    left: 5%;

    animation:
        float 9s ease-in-out infinite reverse;
}


.hero-kicker {

    font-family:
        'Space Mono',
        monospace;

    font-size: 11px;

    letter-spacing: 4px;

    color: #22d3ee;

    margin-bottom: 25px;

    animation:
        reveal 0.8s ease both;
}


.hero-title {

    max-width: 1050px;

    font-size:
        clamp(50px, 8vw, 110px);

    line-height: 0.91;

    font-weight: 900;

    letter-spacing: -5px;

    margin: 0;

    animation:
        reveal 0.9s ease 0.15s both;
}


.hero-title span {

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #c084fc,
            #22d3ee
        );

    -webkit-background-clip: text;

    background-clip: text;

    color: transparent;
}


.hero-description {

    max-width: 680px;

    margin-top: 35px;

    font-size: 16px;

    line-height: 1.8;

    color:
        rgba(255,255,255,0.55);

    animation:
        reveal 0.9s ease 0.3s both;
}


/* =====================================================
   THINK
   ===================================================== */

.think-section {

    position: relative;

    z-index: 5;

    padding:
        110px 7vw;

    border-top:
        1px solid
        rgba(255,255,255,0.06);

    border-bottom:
        1px solid
        rgba(255,255,255,0.06);
}


.section-kicker {

    font-family:
        'Space Mono',
        monospace;

    font-size: 11px;

    letter-spacing: 3px;

    color: #8b5cf6;

    margin-bottom: 20px;
}


.section-title {

    font-size:
        clamp(40px, 6vw, 76px);

    line-height: 0.95;

    font-weight: 900;

    letter-spacing: -3px;

    margin: 0;
}


.section-title span {
    color: #8b5cf6;
}


.section-description {

    max-width: 760px;

    margin-top: 28px;

    font-size: 16px;

    line-height: 1.8;

    color:
        rgba(255,255,255,0.52);
}


/* =====================================================
   URL SECTION
   ===================================================== */

.analysis-section {

    position: relative;

    z-index: 5;

    padding:
        85px 7vw 45px;
}


/* =====================================================
   TEXT INPUT
   ===================================================== */

div[data-baseweb="input"] {

    background:
        rgba(255,255,255,0.035) !important;

    border:
        1px solid
        rgba(139,92,246,0.30) !important;

    border-radius:
        10px !important;
}


div[data-baseweb="input"]:focus-within {

    border-color:
        #8b5cf6 !important;

    box-shadow:
        0 0 20px
        rgba(139,92,246,0.15) !important;
}


input {

    color: #000000 !important;

    background:
        transparent !important;
}


/* =====================================================
   BUTTON
   ===================================================== */

.stButton > button {

    min-height: 48px;

    border:
        1px solid
        rgba(139,92,246,0.5) !important;

    border-radius:
        8px !important;

    background:
        linear-gradient(
            90deg,
            rgba(139,92,246,0.18),
            rgba(34,211,238,0.10)
        ) !important;

    color: white !important;

    font-family:
        'Space Mono',
        monospace !important;

    font-size: 11px !important;

    font-weight: 700 !important;

    letter-spacing: 2px !important;

    transition:
        all 0.25s ease !important;
}


.stButton > button:hover {

    border-color:
        #22d3ee !important;

    box-shadow:
        0 0 25px
        rgba(34,211,238,0.16) !important;

    transform:
        translateY(-2px);
}


/* =====================================================
   QR SECTION
   ===================================================== */

.qr-section {

    position: relative;

    z-index: 5;

    padding:
        105px 7vw 65px;

    border-top:
        1px solid
        rgba(255,255,255,0.06);

    overflow: hidden;
}


.qr-section::before {

    content: "";

    position: absolute;

    width: 450px;

    height: 450px;

    right: -150px;

    top: -80px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(34,211,238,0.10),
            transparent 65%
        );

    animation:
        pulse 5s infinite;
}


.qr-kicker {

    position: relative;

    z-index: 2;

    font-family:
        'Space Mono',
        monospace;

    font-size: 11px;

    letter-spacing: 3px;

    color: #22d3ee;

    margin-bottom: 22px;
}


.qr-title {

    position: relative;

    z-index: 2;

    font-size:
        clamp(42px, 6vw, 78px);

    line-height: 0.94;

    font-weight: 900;

    letter-spacing: -4px;
}


.qr-title span {

    color: #22d3ee;

    text-shadow:
        0 0 30px
        rgba(34,211,238,0.3);
}


.qr-description {

    position: relative;

    z-index: 2;

    max-width: 720px;

    margin-top: 28px;

    font-size: 16px;

    line-height: 1.8;

    color:
        rgba(255,255,255,0.50);
}


/* =====================================================
   QR FILE UPLOADER
   ===================================================== */

[data-testid="stFileUploader"] {

    position: relative;

    z-index: 10;

    margin:
        0 7vw 55px;
}


[data-testid="stFileUploaderDropzone"] {

    background:
        rgba(255,255,255,0.025) !important;

    border:
        1px dashed
        rgba(34,211,238,0.55) !important;

    border-radius:
        14px !important;

    min-height:
        150px !important;

    transition:
        all 0.25s ease;
}


[data-testid="stFileUploaderDropzone"]:hover {

    border-color:
        #22d3ee !important;

    background:
        rgba(34,211,238,0.035) !important;
}


[data-testid="stFileUploaderDropzone"] button {

    background:
        #ffffff !important;

    color:
        #000000 !important;

    border:
        none !important;

    border-radius:
        7px !important;

    min-height:
        40px !important;

    padding:
        0 18px !important;

    font-family:
        'Inter',
        sans-serif !important;

    font-size:
        12px !important;

    font-weight:
        800 !important;

    text-transform:
        uppercase !important;

    letter-spacing:
        1px !important;
}


[data-testid="stFileUploaderDropzone"] button p {

    color:
        #000000 !important;

    font-size:
        12px !important;

    font-weight:
        800 !important;

    text-transform:
        uppercase !important;

    margin:
        0 !important;
}


[data-testid="stFileUploaderDropzone"] button svg {

    color:
        #000000 !important;
}


/* =====================================================
   RESULT CARDS
   ===================================================== */

.result-card {

    margin:
        30px 7vw 0;

    padding:
        30px;

    border-radius:
        16px;

    background:
        rgba(255,255,255,0.025);

    border:
        1px solid
        rgba(255,255,255,0.08);
}


.result-danger {

    border-color:
        rgba(255,77,109,0.40);

    box-shadow:
        0 0 35px
        rgba(255,77,109,0.08);
}


.result-safe {

    border-color:
        rgba(34,197,94,0.35);

    box-shadow:
        0 0 35px
        rgba(34,197,94,0.06);
}


.result-title {

    font-family:
        'Space Mono',
        monospace;

    font-size: 18px;

    letter-spacing: 2px;

    font-weight: 700;

    margin-bottom: 15px;
}


/* =====================================================
   RESULT SECTION TITLES
   ===================================================== */

.result-section-title {

    margin:
        35px 7vw 15px;

    font-family:
        'Space Mono',
        monospace;

    font-size: 13px;

    letter-spacing: 2px;

    color: #8b5cf6;

    font-weight: 700;
}


/* =====================================================
   METRICS
   ===================================================== */

.metric-grid {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 15px;

    margin:
        25px 7vw 0;
}


.metric {

    padding: 22px;

    border:
        1px solid
        rgba(255,255,255,0.07);

    background:
        rgba(255,255,255,0.025);

    border-radius: 12px;
}


.metric-label {

    font-family:
        'Space Mono',
        monospace;

    font-size: 9px;

    letter-spacing: 1.5px;

    color:
        rgba(255,255,255,0.38);

    margin-bottom: 10px;
}


.metric-value {

    font-size: 28px;

    font-weight: 800;
}


/* =====================================================
   ANALYZED URL
   ===================================================== */

.analyzed-url {

    margin:
        30px 7vw 0;

    padding: 22px;

    border-radius: 12px;

    background:
        rgba(255,255,255,0.025);

    border:
        1px solid
        rgba(255,255,255,0.07);
}


.analyzed-label {

    font-family:
        'Space Mono',
        monospace;

    font-size: 9px;

    letter-spacing: 2px;

    color:
        rgba(255,255,255,0.35);

    margin-bottom: 10px;
}


.analyzed-value {

    font-family:
        'Space Mono',
        monospace;

    font-size: 13px;

    color: #67e8f9;

    overflow-wrap: anywhere;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {

    position: relative;

    z-index: 5;

    padding:
        60px 7vw;

    border-top:
        1px solid
        rgba(255,255,255,0.06);

    display: flex;

    justify-content: space-between;

    flex-wrap: wrap;

    gap: 30px;

    color:
        rgba(255,255,255,0.35);

    font-family:
        'Space Mono',
        monospace;

    font-size: 10px;

    letter-spacing: 1px;
}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 900px) {

    .metric-grid {

        grid-template-columns:
            repeat(2, 1fr);

    }
}


@media (max-width: 700px) {

    .hero {

        min-height: 560px;

        padding:
            70px 6vw;
    }

    .hero-title {

        letter-spacing:
            -3px;
    }

    .think-section,
    .analysis-section,
    .qr-section {

        padding:
            75px 6vw;
    }

    [data-testid="stFileUploader"] {

        margin-left: 6vw;

        margin-right: 6vw;
    }

    .metric-grid {

        grid-template-columns:
            1fr;

        margin-left: 6vw;

        margin-right: 6vw;
    }

    .result-card,
    .analyzed-url,
    .result-section-title {

        margin-left: 6vw;

        margin-right: 6vw;
    }
}

</style>
""")


# =========================================================
# FEATURE PREPARATION
# =========================================================

def prepare_features(features):

    if isinstance(features, pd.DataFrame):

        feature_df = features.copy()

    elif isinstance(features, dict):

        feature_df = pd.DataFrame(
            [features]
        )

    else:

        feature_df = pd.DataFrame(
            [features],
            columns=feature_names
        )


    for feature in feature_names:

        if feature not in feature_df.columns:

            feature_df[feature] = 0


    feature_df = feature_df[
        feature_names
    ]


    feature_df = feature_df.replace(
        [np.inf, -np.inf],
        0
    ).fillna(0)


    return feature_df


# =========================================================
# RISK SCORE
# SAME LOGIC AS YOUR OLD CODE
# =========================================================

def calculate_risk_score(features):

    score = 0

    signals = []


    if features.get("has_ip", 0) == 1:

        score += 25

        signals.append(
            "Uses an IP address instead of a domain name."
        )


    if features.get("has_at", 0) == 1:

        score += 20

        signals.append(
            "Contains an @ symbol."
        )


    keyword_count = features.get(
        "suspicious_keyword_count",
        0
    )


    if keyword_count >= 3:

        score += 25

        signals.append(
            f"Contains {keyword_count} suspicious "
            "security-related keywords."
        )

    elif keyword_count >= 1:

        score += 10

        signals.append(
            f"Contains {keyword_count} suspicious "
            "security-related keyword."
        )


    if features.get(
        "url_length",
        0
    ) >= 100:

        score += 15

        signals.append(
            "Unusually long URL."
        )


    if features.get(
        "subdomain_count",
        0
    ) >= 3:

        score += 10

        signals.append(
            "Multiple subdomains detected."
        )


    if features.get(
        "query_parameter_count",
        0
    ) >= 3:

        score += 5

        signals.append(
            "Multiple query parameters."
        )


    if features.get(
        "has_https",
        0
    ) == 0:

        score += 10

        signals.append(
            "URL does not use HTTPS."
        )


    score = min(
        score,
        100
    )


    if score >= 70:

        risk_level = "HIGH"

    elif score >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"


    return (
        score,
        risk_level,
        signals
    )


# =========================================================
# ANALYZE URL
# =========================================================

def analyze_url(url):

    features = extract_url_features(
        url
    )


    feature_df = prepare_features(
        features
    )


    prediction = int(
        model.predict(
            feature_df
        )[0]
    )


    probabilities = model.predict_proba(
        feature_df
    )[0]


    classes = list(
        model.classes_
    )


    class_probabilities = dict(
        zip(
            classes,
            probabilities
        )
    )


    phishing_probability = float(
        class_probabilities.get(
            1,
            class_probabilities.get(
                "1",
                0
            )
        )
    )


    legitimate_probability = float(
        class_probabilities.get(
            0,
            class_probabilities.get(
                "0",
                0
            )
        )
    )


    # =====================================================
    # OLD FEATURE-BASED RISK SYSTEM
    # =====================================================

    if isinstance(features, pd.DataFrame):

        raw_features = (
            features.iloc[0].to_dict()
        )

    else:

        raw_features = dict(
            features
        )


    risk_score, risk_level, signals = (
        calculate_risk_score(
            raw_features
        )
    )


    return {

        "url":
            url,

        "prediction":
            prediction,

        "phishing_probability":
            phishing_probability,

        "legitimate_probability":
            legitimate_probability,

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "signals":
            signals,

        "features":
            raw_features

    }


# =========================================================
# QR DECODER
# =========================================================

def decode_qr(uploaded_file):

    try:

        file_bytes = np.asarray(
            bytearray(
                uploaded_file.getvalue()
            ),
            dtype=np.uint8
        )


        image = cv2.imdecode(
            file_bytes,
            cv2.IMREAD_COLOR
        )


        if image is None:

            return None, None


        detector = cv2.QRCodeDetector()


        data, points, _ = (
            detector.detectAndDecode(
                image
            )
        )


        if data:

            return data.strip(), image


        return None, image


    except Exception:

        return None, None


# =========================================================
# DISPLAY COMPLETE ANALYSIS RESULT
# =========================================================

def display_analysis_result(
    url,
    result
):

    prediction = result[
        "prediction"
    ]

    phishing_probability = result[
        "phishing_probability"
    ]

    legitimate_probability = result[
        "legitimate_probability"
    ]

    risk_score = result[
        "risk_score"
    ]

    risk_level = result[
        "risk_level"
    ]

    signals = result[
        "signals"
    ]

    features = result[
        "features"
    ]


    safe_url = html.escape(
        url
    )


    # =====================================================
    # RESULT HEADER
    # =====================================================

    if prediction == 1:

        html_block(f"""

        <div class="result-card result-danger">

            <div class="result-title"
                 style="color:#ff4d6d;">

                ⚠ PHISHING DETECTED

            </div>

            <div style="
                color:rgba(255,255,255,0.55);
                line-height:1.7;
                font-size:14px;
            ">

                PhishGuard identified suspicious
                characteristics associated with
                phishing URLs.

            </div>

        </div>

        """)

    else:

        html_block(f"""

        <div class="result-card result-safe">

            <div class="result-title"
                 style="color:#22c55e;">

                ✓ URL CLASSIFIED AS LEGITIMATE

            </div>

            <div style="
                color:rgba(255,255,255,0.55);
                line-height:1.7;
                font-size:14px;
            ">

                The model found the URL structurally
                consistent with legitimate web addresses.

            </div>

        </div>

        """)


    # =====================================================
    # ANALYZED URL
    # =====================================================

    html_block(f"""

    <div class="analyzed-url">

        <div class="analyzed-label">
            ANALYZED DESTINATION
        </div>

        <div class="analyzed-value">
            {safe_url}
        </div>

    </div>

    """)


    # =====================================================
    # SECURITY ASSESSMENT
    # =====================================================

    html_block("""

    <div class="result-section-title">
        SECURITY ASSESSMENT
    </div>

    """)


    html_block(f"""

    <div class="metric-grid">

        <div class="metric">

            <div class="metric-label">
                PHISHING PROBABILITY
            </div>

            <div class="metric-value">
                {phishing_probability:.2%}
            </div>

        </div>


        <div class="metric">

            <div class="metric-label">
                LEGITIMATE PROBABILITY
            </div>

            <div class="metric-value">
                {legitimate_probability:.2%}
            </div>

        </div>


        <div class="metric">

            <div class="metric-label">
                RISK SCORE
            </div>

            <div class="metric-value">
                {risk_score}/100
            </div>

        </div>


        <div class="metric">

            <div class="metric-label">
                RISK LEVEL
            </div>

            <div class="metric-value">
                {risk_level}
            </div>

        </div>

    </div>

    """)


    # =====================================================
    # MODEL CONFIDENCE
    # =====================================================

    html_block("""

    <div class="result-section-title">
        MODEL CONFIDENCE
    </div>

    """)


    st.progress(
        phishing_probability
    )


    st.caption(
        "Random Forest phishing probability: "
        f"{phishing_probability:.2%}"
    )


    # =====================================================
    # SECURITY SIGNALS
    # =====================================================

    html_block("""

    <div class="result-section-title">
        SECURITY SIGNALS
    </div>

    """)


    if signals:

        for signal in signals:

            html_block(f"""

            <div style="

                margin:
                    8px 7vw;

                padding:
                    13px 17px;

                background:
                    rgba(255,77,109,0.05);

                border:
                    1px solid
                    rgba(255,77,109,0.22);

                border-left:
                    4px solid
                    #ff5964;

                border-radius:
                    10px;

                color:
                    rgba(255,255,255,0.85);

                font-size:
                    14px;

            ">

                ⚠️ {html.escape(signal)}

            </div>

            """)

    else:

        html_block("""

        <div style="

            margin:
                8px 7vw;

            padding:
                13px 17px;

            background:
                rgba(34,197,94,0.05);

            border:
                1px solid
                rgba(34,197,94,0.20);

            border-left:
                4px solid
                #22c55e;

            border-radius:
                10px;

            color:
                rgba(255,255,255,0.85);

        ">

            ✓ No major heuristic security signals detected.

        </div>

        """)


    # =====================================================
    # WHY WAS THIS FLAGGED?
    # =====================================================

    html_block("""

    <div class="result-section-title">
        WHY WAS THIS FLAGGED?
    </div>

    """)


    explanation_parts = []


    if features.get(
        "suspicious_keyword_count",
        0
    ) > 0:

        explanation_parts.append(
            "suspicious security-related keywords"
        )


    if features.get(
        "url_length",
        0
    ) >= 100:

        explanation_parts.append(
            "an unusually long URL"
        )


    if features.get(
        "has_ip",
        0
    ) == 1:

        explanation_parts.append(
            "an IP address instead of a domain"
        )


    if features.get(
        "has_at",
        0
    ) == 1:

        explanation_parts.append(
            "an @ symbol"
        )


    if features.get(
        "subdomain_count",
        0
    ) >= 3:

        explanation_parts.append(
            "multiple subdomains"
        )


    if prediction == 1:

        if explanation_parts:

            st.info(
                "The model classified this URL as phishing. "
                "Potentially suspicious characteristics include "
                + ", ".join(
                    explanation_parts
                )
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
            "The model classified this URL as legitimate based "
            "on the structural characteristics extracted from "
            "the URL. No classification guarantees that a "
            "website is completely safe."
        )


    # =====================================================
    # EXTRACTED URL FEATURES
    # =====================================================

    with st.expander(
        "📊 VIEW EXTRACTED URL FEATURES"
    ):

        feature_df = pd.DataFrame(
            {
                "Feature":
                    list(
                        features.keys()
                    ),

                "Value":
                    list(
                        features.values()
                    )
            }
        )


        st.dataframe(
            feature_df,
            use_container_width=True,
            hide_index=True
        )


    # =====================================================
    # MODEL INFORMATION
    # =====================================================

    with st.expander(
        "🤖 MODEL INFORMATION"
    ):

        # -----------------------------------------------
        # FEATURE IMPORTANCE GRAPH
        # -----------------------------------------------

        if hasattr(
            model,
            "feature_importances_"
        ):

            importance_df = pd.DataFrame(
                {
                    "Feature":
                        feature_names,

                    "Importance":
                        model.feature_importances_
                }
            )


            importance_df = (
                importance_df
                .sort_values(
                    "Importance",
                    ascending=False
                )
            )


            st.markdown(
                "**Feature Importance**"
            )


            st.bar_chart(
                importance_df.set_index(
                    "Feature"
                )
            )


        # -----------------------------------------------
        # MODEL DETAILS
        # -----------------------------------------------

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


# =========================================================
# NAVBAR
# =========================================================

html_block("""

<div class="navbar">

    <div class="logo">
        PHISH<span>GUARD</span>
    </div>

    <div class="nav-status">

        <div class="status-dot"></div>

        AI SECURITY ENGINE ONLINE

    </div>

</div>

""")


# =========================================================
# HERO
# =========================================================

html_block("""

<section class="hero">

    <div class="hero-orb orb-one"></div>

    <div class="hero-orb orb-two"></div>

    <div class="hero-kicker">
        AI-POWERED URL SECURITY
    </div>

    <h1 class="hero-title">

        THE INTERNET<br>

        ISN'T ALWAYS<br>

        <span>
            WHAT IT SEEMS.
        </span>

    </h1>

    <div class="hero-description">

        PhishGuard uses machine learning and URL
        intelligence to identify suspicious destinations
        before you interact with them.

    </div>

</section>

""")


# =========================================================
# THINK SECTION
# =========================================================

html_block("""

<section class="think-section">

    <div class="section-kicker">
        THINK BEFORE YOU CLICK.
    </div>

    <h2 class="section-title">

        TRUST IS EASY<br>

        TO <span>FAKE.</span>

    </h2>

    <div class="section-description">

        Phishing attacks often rely on familiar-looking
        links designed to create urgency and trust.
        PhishGuard examines URL structure and machine
        learning signals before you interact with the
        destination.

    </div>

</section>

""")


# =========================================================
# URL INPUT
# =========================================================

html_block("""

<section class="analysis-section">
</section>

""")


url = st.text_input(

    "URL",

    placeholder="https://example.com",

    label_visibility="collapsed",

    key="url_input"
)


if st.button(
    "ANALYZE URL",
    key="analyze_url_button"
):

    if not url.strip():

        st.warning(
            "Please enter a URL first."
        )

    else:

        clean_url = url.strip()


        if not clean_url.startswith(
            (
                "http://",
                "https://"
            )
        ):

            clean_url = (
                "https://"
                + clean_url
            )


        try:

            with st.spinner(
                "Analyzing destination..."
            ):

                result = analyze_url(
                    clean_url
                )


            display_analysis_result(
                clean_url,
                result
            )


        except Exception as e:

            st.error(
                f"Unable to analyze this URL: {e}"
            )


# =========================================================
# QR SECTION
# =========================================================

html_block("""

<section class="qr-section">

    <div class="qr-kicker">
        ANOTHER ATTACK SURFACE
    </div>

    <div class="qr-title">

        GOT A <span>QR CODE?</span><br>

        SCAN IT BEFORE<br>

        YOU OPEN IT.

    </div>

    <div class="qr-description">

        QR codes can hide suspicious destinations
        just like ordinary links. Upload the QR image
        and PhishGuard will decode the destination
        before checking it for potential threats.

    </div>

</section>

""")


# =========================================================
# QR UPLOAD
# =========================================================

uploaded_qr = st.file_uploader(

    "UPLOAD QR CODE",

    type=[
        "png",
        "jpg",
        "jpeg",
        "webp"
    ],

    key="qr_upload"
)


# =========================================================
# QR PROCESSING
# =========================================================

if uploaded_qr:

    decoded_url, qr_image = decode_qr(
        uploaded_qr
    )


    # =====================================================
    # IMAGE PREVIEW
    # =====================================================

    if qr_image is not None:

        col1, col2, col3 = st.columns(
            [1, 2, 1]
        )

        with col2:

            st.image(
                qr_image,
                caption="UPLOADED QR CODE",
                use_container_width=True
            )


    # =====================================================
    # QR DECODED
    # =====================================================

    if decoded_url:

        safe_decoded_url = html.escape(
            decoded_url
        )


        html_block(f"""

        <div style="

            margin:25px 7vw 0;

            padding:25px;

            border-radius:15px;

            border:
                1px solid
                rgba(34,211,238,0.30);

            background:
                rgba(34,211,238,0.035);

        ">

            <div style="

                font-family:
                    'Space Mono',
                    monospace;

                font-size:10px;

                letter-spacing:2px;

                color:#22d3ee;

                margin-bottom:12px;

            ">

                ✓ QR CODE DECODED

            </div>


            <div style="

                color:
                    rgba(255,255,255,0.45);

                font-size:11px;

                margin-bottom:8px;

            ">

                DESTINATION FOUND

            </div>


            <div style="

                color:#ffffff;

                font-family:
                    'Space Mono',
                    monospace;

                font-size:13px;

                overflow-wrap:anywhere;

            ">

                {safe_decoded_url}

            </div>

        </div>

        """)


        # =================================================
        # ONLY ANALYZE WEB URLS
        # =================================================

        if decoded_url.startswith(
            (
                "http://",
                "https://"
            )
        ):

            st.write("")


            if st.button(
                "ANALYZE QR DESTINATION",
                key="analyze_qr_button"
            ):

                try:

                    with st.spinner(
                        "Analyzing QR destination..."
                    ):

                        qr_result = analyze_url(
                            decoded_url
                        )


                    display_analysis_result(
                        decoded_url,
                        qr_result
                    )


                except Exception as e:

                    st.error(
                        "Unable to analyze QR "
                        f"destination: {e}"
                    )


        else:

            st.warning(
                "The QR code contains data, but "
                "it is not an HTTP/HTTPS web URL."
            )


    # =====================================================
    # QR NOT DETECTED
    # =====================================================

    else:

        st.error(
            "No QR code could be detected in this image."
        )

        st.info(
            "Upload a clear QR code image in "
            "PNG, JPG, JPEG or WEBP format."
        )


# =========================================================
# FOOTER
# =========================================================

html_block("""

<div class="footer">

    <div>
        PHISHGUARD // AI SECURITY
    </div>

    <div>
        PREDICT · DETECT · PROTECT
    </div>

</div>

""")