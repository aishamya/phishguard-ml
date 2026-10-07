from urllib.parse import urlparse
import ipaddress
import re
import math
from collections import Counter


SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "verification",
    "account",
    "update",
    "secure",
    "security",
    "signin",
    "bank",
    "password",
    "confirm",
    "wallet",
    "payment"
]


def calculate_entropy(text):
    if not text:
        return 0.0

    counts = Counter(text)
    length = len(text)
    entropy = 0.0

    for count in counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy


def extract_url_features(url):
    url = str(url).strip()

    # Make sure the URL has a scheme for parsing
    url_for_parsing = url

    if not re.match(
        r"^[a-zA-Z][a-zA-Z0-9+.-]*://",
        url_for_parsing
    ):
        url_for_parsing = "http://" + url_for_parsing

    try:
        parsed = urlparse(url_for_parsing)
    except Exception:
        parsed = urlparse("http://")

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    hostname = hostname.lower()

    # Check whether hostname is an IP address
    has_ip = 0

    try:
        ipaddress.ip_address(hostname)
        has_ip = 1
    except ValueError:
        has_ip = 0

    # Count suspicious keywords
    url_lower = url.lower()

    suspicious_keyword_count = sum(
        1
        for keyword in SUSPICIOUS_KEYWORDS
        if keyword in url_lower
    )

    # Count subdomains
    hostname_parts = hostname.split(".") if hostname else []

    # Do not count "www" as a subdomain
    if hostname_parts and hostname_parts[0] == "www":
        hostname_parts = hostname_parts[1:]

    if len(hostname_parts) > 2:
        subdomain_count = len(hostname_parts) - 2
    else:
        subdomain_count = 0

    # Count query parameters
    if query:
        query_parameter_count = len(
            [item for item in query.split("&") if item]
        )
    else:
        query_parameter_count = 0

    # Domain-level features
    domain_letter_count = sum(
        char.isalpha() for char in hostname
    )

    domain_digit_count = sum(
        char.isdigit() for char in hostname
    )

    domain_hyphen_count = hostname.count("-")

    domain_special_char_count = len(
        re.findall(r"[^a-zA-Z0-9.-]", hostname)
    )

    # Domain entropy
    domain_entropy = calculate_entropy(hostname)

    # Final 20 features
    features = {
        "url_length": len(url),
        "domain_length": len(hostname),
        "path_length": len(path),
        "dot_count": url.count("."),
        "slash_count": url.count("/"),
        "hyphen_count": url.count("-"),
        "underscore_count": url.count("_"),
        "digit_count": sum(
            char.isdigit() for char in url
        ),
        "special_char_count": len(
            re.findall(r"[^a-zA-Z0-9]", url)
        ),
        "has_at": int("@" in url),
        "has_ip": has_ip,
        "has_https": int(
            parsed.scheme.lower() == "https"
        ),
        "suspicious_keyword_count": suspicious_keyword_count,
        "subdomain_count": subdomain_count,
        "query_parameter_count": query_parameter_count,
        "domain_letter_count": domain_letter_count,
        "domain_digit_count": domain_digit_count,
        "domain_hyphen_count": domain_hyphen_count,
        "domain_special_char_count": domain_special_char_count,
        "domain_entropy": domain_entropy
    }

    return features