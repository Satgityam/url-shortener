# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need


# app/utils.py
import string
import random
import re

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def is_valid_url(url):
    pattern = re.compile(
        r'^(https?://)?'                  # http:// or https://
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}' # domain
        r'(:\d+)?'                        # optional port
        r'(\/\S*)?$'                      # path
    )
    return re.match(pattern, url) is not None

