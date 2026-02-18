def detect_platform(url):
    """
    Detects the platform from the given URL.
    Returns: 'youtube', 'instagram', 'x', or 'unsupported'
    """
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "instagram.com" in url:
        return "instagram"
    elif "x.com" in url or "twitter.com" in url:
        return "x"
    else:
        return "unsupported"
