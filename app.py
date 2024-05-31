from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta

from test import test_bp
from auth import auth_bp
from products import products_bp
from transactions import transactions_bp

app = Flask(__name__)

# Flask-JWT-Extended configuration
app.config["JWT_SECRET_KEY"] = "mySecretKey"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

# Blueprint diregister
app.register_blueprint(test_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(products_bp, url_prefix="/api/products")
app.register_blueprint(transactions_bp, url_prefix="/api/transactions")

if __name__ == "__main__":
    app.run(debug=True)
