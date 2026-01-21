from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

try:
    from routes.cars import cars_bp
    from routes.auth import auth_bp
    from routes.orders import orders_bp
    from routes.messages import messages_bp  # Import messages blueprint
    from routes.admin import admin_bp  # Import admin blueprint
    HAS_ORDERS = True
except ImportError as e:
    print(f"Warning: Could not import all blueprints: {e}")
    try:
        from routes.cars import cars_bp
        from routes.auth import auth_bp
        from routes.messages import messages_bp  # Import messages blueprint
        from routes.admin import admin_bp  # Import admin blueprint
        HAS_ORDERS = False
    except ImportError as e2:
        print(f"Error importing core blueprints: {e2}")
        raise

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)  # ✅ รองรับ credential และ preflight

JWTManager(app)

# เชื่อมต่อ MongoDB ด้วย mongoengine โดยตรง
try:
    connect(
        db=app.config.get("MONGODB_SETTINGS", {}).get("db", "MyCarsWed"),
        host=app.config.get("MONGODB_SETTINGS", {}).get("host", "localhost"),
        port=app.config.get("MONGODB_SETTINGS", {}).get("port", 27017)
    )
    print("✓ MongoDB connected successfully")
except Exception as e:
    print(f"✗ MongoDB connection error: {e}")

# Register Blueprints
app.register_blueprint(cars_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(messages_bp)  # Register messages blueprint
app.register_blueprint(admin_bp)  # Register admin blueprint with /api/admin prefix

if HAS_ORDERS:
    app.register_blueprint(orders_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)