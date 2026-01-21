# This file makes the folder a Python package.
# You can also initialize package-level variables or imports here if needed.
# Routes initialization - import auth blueprint
from .cars import cars_bp
from .auth import auth_bp

try:
    from .orders import orders_bp
except ImportError:
    print("Warning: orders_bp not available")

__all__ = ['cars_bp', 'auth_bp', 'orders_bp']