from urllib.parse import urlparse
import ipaddress
import re


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


def extract_url_features(url):
    """
    Extract numerical security-related features from a URL.
    """

    # Convert to string and remove extra spaces
    url = str(url).strip()

    # Some dataset URLs don't contain http:// or https://
    # Add http:// temporarily so urlparse can identify the hostname.
    url_for_parsing = url

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url_for_parsing):
        url_for_parsing = "http://" + url_for_parsing

    try:
        parsed = urlparse(url_for_parsing)
        hostname = parsed.hostname or ""
        path = parsed.path or ""
        query = parsed.query or ""
    except Exception:
        hostname = ""
        path = ""
        query = ""

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
        1 for keyword in SUSPICIOUS_KEYWORDS
        if keyword in url_lower
    )

    # Estimate number of subdomains
    hostname_parts = hostname.split(".") if hostname else []

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

    # Build feature dictionary
    features = {
        "url_length": len(url),
        "domain_length": len(hostname),
        "path_length": len(path),

        "dot_count": url.count("."),
        "slash_count": url.count("/"),
        "hyphen_count": url.count("-"),
        "underscore_count": url.count("_"),
        "digit_count": sum(char.isdigit() for char in url),

        "special_char_count": len(
            re.findall(r"[^a-zA-Z0-9]", url)
        ),

        "has_at": int("@" in url),
        "has_ip": has_ip,
        "has_https": int(parsed.scheme.lower() == "https"),

        "suspicious_keyword_count": suspicious_keyword_count,
        "subdomain_count": subdomain_count,
        "query_parameter_count": query_parameter_count
    }

    return features