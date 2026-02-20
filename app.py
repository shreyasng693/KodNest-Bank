from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
import uuid
from datetime import datetime, timedelta
import hashlib

from config import DB_CONFIG, JWT_SECRET_KEY, JWT_ALGORITHM
from database import get_db_connection, init_database
from jwt_utils import generate_token, verify_token

app = Flask(__name__, static_folder='static')
CORS(app, supports_credentials=True, origins=['http://127.0.0.1:5000', 'http://localhost:5000'])

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Helper function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Helper function to verify password
def verify_password(password, hashed):
    return hash_password(password) == hashed

# Route: Initialize Database
@app.route('/init', methods=['GET'])
def init():
    """Initialize the database tables"""
    if init_database():
        return jsonify({'status': 'success', 'message': 'Database initialized successfully!'})
    return jsonify({'status': 'error', 'message': 'Failed to initialize database'}), 500

# Route: Register
@app.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    required_fields = ['uid', 'username', 'email', 'password', 'phone']
    for field in required_fields:
        if field not in data:
            return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM KodUser WHERE username = %s OR email = %s", 
                       (data['username'], data['email']))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return jsonify({'status': 'error', 'message': 'Username or email already exists'}), 400
        
        hashed_password = hash_password(data['password'])
        role = data.get('role', 'Customer')
        
        cursor.execute("""
            INSERT INTO KodUser (uid, username, email, password, balance, phone, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (data['uid'], data['username'], data['email'], hashed_password, 
              100000.00, data['phone'], role))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'success', 
            'message': 'Registration successful!',
            'data': {
                'uid': data['uid'],
                'username': data['username'],
                'email': data['email'],
                'balance': 100000.00
            }
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Route: Login
@app.route('/login', methods=['POST'])
def login():
    """Login user and generate JWT token"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'status': 'error', 'message': 'Username and password required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM KodUser WHERE username = %s", (data['username'],))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
        
        if not verify_password(data['password'], user['password']):
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
        
        token = generate_token(user['username'], user['role'], user['uid'])
        
        tid = str(uuid.uuid4())
        expiry = datetime.utcnow() + timedelta(hours=24)
        
        cursor.execute("""
            INSERT INTO UserToken (tid, token, uid, expiry)
            VALUES (%s, %s, %s, %s)
        """, (tid, token, user['uid'], expiry))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        response = make_response(jsonify({
            'status': 'success',
            'message': 'Login successful!',
            'token': token,
            'data': {
                'username': user['username'],
                'role': user['role'],
                'uid': user['uid']
            }
        }))
        
        # Set cookie with proper settings for cross-origin
        response.set_cookie('jwt_token', token, httponly=True, samesite=None, 
                           expires=datetime.utcnow() + timedelta(hours=24), path='/')
        
        return response
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Route: Get Balance
@app.route('/getBalance', methods=['POST'])
def get_balance():
    """Get user balance - requires JWT token verification"""
    token = request.cookies.get('jwt_token')
    
    if not token:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    
    if not token:
        return jsonify({'status': 'error', 'message': 'No token provided'}), 401
    
    payload = verify_token(token)
    if not payload:
        return jsonify({'status': 'error', 'message': 'Invalid or expired token'}), 401
    
    username = payload.get('sub')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT uid, username, email, balance FROM KodUser WHERE username = %s", 
                       (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        return jsonify({
            'status': 'success',
            'message': f'Your balance is: {user["balance"]}',
            'data': {
                'username': user['username'],
                'balance': float(user['balance'])
            }
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Route: Logout
@app.route('/logout', methods=['POST'])
def logout():
    """Logout user and invalidate token"""
    token = request.cookies.get('jwt_token')
    
    if token:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM UserToken WHERE token = %s", (token,))
                conn.commit()
                cursor.close()
                conn.close()
            except:
                pass
    
    response = make_response(jsonify({'status': 'success', 'message': 'Logged out successfully'}))
    response.set_cookie('jwt_token', '', expires=0)
    return response

# Route: Verify Token
@app.route('/verify', methods=['GET'])
def verify():
    """Verify if token is valid"""
    token = request.cookies.get('jwt_token')
    
    if not token:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    
    if not token:
        return jsonify({'status': 'error', 'valid': False}), 401
    
    payload = verify_token(token)
    if not payload:
        return jsonify({'status': 'error', 'valid': False}), 401
    
    return jsonify({
        'status': 'success',
        'valid': True,
        'data': {
            'username': payload.get('sub'),
            'role': payload.get('role'),
            'uid': payload.get('uid')
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
