# app/routes.py
from flask import Blueprint, request, jsonify, redirect
from app.services import shorten_url, get_long_url


bp = Blueprint("routes", __name__)



from app.services import shorten_url, get_long_url, get_stats

@bp.route("/api/stats/<short_code>", methods=["GET"])
def stats(short_code):
    data = get_stats(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404
    return jsonify(data), 200


@bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "URL Shortener API"})

# @bp.route("/api/shorten", methods=["POST"])
# def api_shorten():
#     data = request.get_json()
#     long_url = data.get("url")

#     if not long_url:
#         return jsonify({"error": "Missing 'url' in request"}), 400

#     short_id = shorten_url(long_url)
#     return jsonify({"short_url": f"http://localhost:5000/{short_id}"}), 200

@bp.route("/api/shorten", methods=["POST"])
def api_shorten():
    data = request.get_json()
    long_url = data.get("url")

    if not long_url:
        return jsonify({"error": "Missing 'url' in request"}), 400

    short_code, error = shorten_url(long_url)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 200


@bp.route("/<short_id>", methods=["GET"])
def redirect_to_url(short_id):
    long_url = get_long_url(short_id)
    if long_url:
        return redirect(long_url)
    return jsonify({"error": "Short URL not found"}), 404


