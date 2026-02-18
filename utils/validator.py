def validate_url(url):
    """
    Validates if the input string is a valid URL.
    """
    if not url:
        return False
    return url.startswith("http://") or url.startswith("https://")
