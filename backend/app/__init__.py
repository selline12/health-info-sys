from flask import Flask, jsonify
from .extensions import db, jwt, cors, limiter
from .routes.auth import auth_bp
from .routes.clients import clients_bp
from .routes.main import main_bp, swaggerui_blueprint, SWAGGER_URL
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/health_info.log',
                                         maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Health Info System startup')

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    limiter.init_app(app)

    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return {"error": "Missing Authorization Header", "message": "Please login to access this resource"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return {"error": "Invalid Token", "message": "Please login again"}, 401

    @jwt.expired_token_loader
    def expired_token_callback(callback):
        return {"error": "Token Expired", "message": "Please login again"}, 401

    # Global error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found", "message": "The requested resource was not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error('Server Error: %s', error)
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        app.logger.error('Unhandled Exception: %s', e)
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(clients_bp, url_prefix='/api/v1/clients')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        from .models.models import User
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

    return app 