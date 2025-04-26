from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db, limiter
from ..models.models import Client, HealthProgram, ClientProgram
import redis
from datetime import datetime
import json

clients_bp = Blueprint('clients', __name__)

def get_redis_client():
    try:
        return redis.Redis(
            host=current_app.config['REDIS_HOST'],
            port=current_app.config['REDIS_PORT'],
            db=0,
            decode_responses=True
        )
    except redis.ConnectionError as e:
        current_app.logger.error(f"Redis connection error: {e}")
        return None

@clients_bp.route('/api/v1/clients/', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_clients():
    try:
        redis_client = get_redis_client()
        cache_key = 'clients_list'
        
        # Try to get from cache first
        if redis_client:
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return jsonify(json.loads(cached_data))
        
        # If not in cache, get from database
        clients = Client.query.all()
        result = [{
            'id': client.id,
            'name': client.name,
            'date_of_birth': client.date_of_birth.isoformat() if client.date_of_birth else None,
            'contact_info': client.contact_info
        } for client in clients]
        
        # Cache the result
        if redis_client:
            try:
                redis_client.setex(cache_key, 300, json.dumps(result))  # Cache for 5 minutes
            except redis.RedisError as e:
                current_app.logger.error(f"Redis cache error: {e}")
        
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error in get_clients: {e}")
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/api/v1/clients/', methods=['POST'])
@jwt_required()
@limiter.limit("20 per minute")
def create_client():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
            
        client = Client(
            name=data['name'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None,
            contact_info=data.get('contact_info')
        )
        db.session.add(client)
        db.session.commit()
        
        # Clear the cache
        redis_client = get_redis_client()
        if redis_client:
            redis_client.delete('clients_list')
            
        return jsonify({
            'id': client.id,
            'name': client.name,
            'message': 'Client created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/api/v1/clients/<int:client_id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_client(client_id):
    try:
        client = Client.query.get_or_404(client_id)
        return jsonify({
            'id': client.id,
            'name': client.name,
            'date_of_birth': client.date_of_birth.isoformat() if client.date_of_birth else None,
            'contact_info': client.contact_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/api/v1/clients/<int:client_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("20 per minute")
def delete_client(client_id):
    try:
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        
        # Clear the cache
        redis_client = get_redis_client()
        if redis_client:
            redis_client.delete('clients_list')
            
        return jsonify({'message': 'Client deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 