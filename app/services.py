from datetime import datetime, timezone
from app.utils import generate_short_id, is_valid_url
from threading import Lock
from datetime import datetime

# In-memory storage with analytics
url_store = {}
lock = Lock()

def shorten_url(long_url):
    if not is_valid_url(long_url):
        return None, "Invalid URL"

    with lock:
        # Check if URL already exists
        for short, data in url_store.items():
            if data["url"] == long_url:
                return short, None

        # Generate unique short code
        short_code = generate_short_id()
        while short_code in url_store:
            short_code = generate_short_id()

        url_store[short_code] = {
            "url": long_url,
            "clicks": 0,
            "created_at": datetime.now(timezone.utc).isoformat()

        }
        return short_code, None

def get_long_url(short_code):
    with lock:
        data = url_store.get(short_code)
        if data:
            data["clicks"] += 1
            return data["url"]
        return None

def get_stats(short_code):
    with lock:
        data = url_store.get(short_code)
        if not data:
            return None
        return {
            "url": data["url"],
            "clicks": data["clicks"],
            "created_at": data["created_at"]
        }
