import os
from dotenv import load_dotenv

load_dotenv()

# Aiven MySQL Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'kodbank')
}

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'kodbank_signing_key_2024')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRY_HOURS = 24
