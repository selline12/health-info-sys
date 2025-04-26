from flask import Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

main_bp = Blueprint('main', __name__)

# Swagger configuration
SWAGGER_URL = '/api/v1/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Health Information System API"
    }
)

@main_bp.route('/')
def root():
    return jsonify({
        'message': 'Welcome to Health Information System API',
        'version': 'v1',
        'endpoints': {
            'clients': '/api/v1/clients',
            'programs': '/api/v1/programs',
            'auth': '/api/v1/auth/login',
            'docs': '/api/v1/docs'
        }
    })

@main_bp.route('/api')
def api_info():
    return jsonify({
        'message': 'Welcome to Health Information System API',
        'version': 'v1',
        'endpoints': {
            'clients': '/api/v1/clients',
            'programs': '/api/v1/programs',
            'auth': '/api/v1/auth/login',
            'docs': '/api/v1/docs'
        }
    }) 