# app/main.py
# app/main.py
from flask import Flask
from app.routes import bp as routes_bp

app = Flask(__name__)
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

