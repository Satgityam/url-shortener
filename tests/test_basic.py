import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.main import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

# Test 1: Health Check
def test_health_check(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.get_json()["status"] == "healthy"

# Test 2: Shorten a Valid URL
def test_shorten_valid_url(client):
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    assert res.status_code == 200
    data = res.get_json()
    assert "short_code" in data
    assert "short_url" in data

# Test 3: Redirect to Original URL
def test_redirect_url(client):
    res = client.post("/api/shorten", json={"url": "https://example.com/test"})
    short_code = res.get_json()["short_code"]

    redirect = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect.status_code == 302
    assert redirect.headers["Location"] == "https://example.com/test"

# Test 4: Invalid URL Rejected
def test_invalid_url(client):
    res = client.post("/api/shorten", json={"url": "ht!tp:/invalid-url"})
    assert res.status_code == 400
    assert res.get_json()["error"] == "Invalid URL"

# Test 5: Get Analytics
def test_analytics(client):
    res = client.post("/api/shorten", json={"url": "https://trackme.com"})
    short_code = res.get_json()["short_code"]

    # Trigger some redirects
    client.get(f"/{short_code}")
    client.get(f"/{short_code}")

    stats = client.get(f"/api/stats/{short_code}")
    data = stats.get_json()

    assert stats.status_code == 200
    assert data["url"] == "https://trackme.com"
    assert data["clicks"] == 2
    assert "created_at" in data

# Test 6: Same URL returns same short code
def test_idempotent_shorten(client):
    url = "https://duplicate.com"
    res1 = client.post("/api/shorten", json={"url": url})
    res2 = client.post("/api/shorten", json={"url": url})
    assert res1.get_json()["short_code"] == res2.get_json()["short_code"]

# Test 7: Missing JSON body returns error
# Test 7: Missing JSON body returns error
def test_shorten_missing_json(client):
    res = client.post("/api/shorten", json={})
    assert res.status_code == 400
    assert res.get_json()["error"] == "Missing 'url' in request"


# Test 8: Invalid short code on redirect
def test_invalid_short_code_redirect(client):
    res = client.get("/doesnotexist")
    assert res.status_code == 404

# Test 9: Invalid short code for stats
def test_invalid_short_code_stats(client):
    res = client.get("/api/stats/fake123")
    assert res.status_code == 404
    assert res.get_json()["error"] == "Short code not found"
