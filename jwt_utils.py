import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRY_HOURS

def generate_token(username, role, uid):
    """Generate JWT token with username as subject and role as claim"""
    payload = {
        'sub': username,
        'role': role,
        'uid': uid,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token):
    """Verify JWT token and return the payload if valid"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def decode_token(token):
    """Decode token without verification (for debugging)"""
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except:
        return None
