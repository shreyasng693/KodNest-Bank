import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def init_database():
    """Initialize database and create tables if they don't exist"""
    # First connect without database to create it
    config = DB_CONFIG.copy()
    db_name = config.pop('database')
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        # Create KodUser table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS KodUser (
                uid VARCHAR(50) PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                balance DECIMAL(15, 2) DEFAULT 100000.00,
                phone VARCHAR(20),
                role VARCHAR(20) DEFAULT 'Customer'
            )
        """)
        
        # Create UserToken table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserToken (
                tid VARCHAR(50) PRIMARY KEY,
                token TEXT NOT NULL,
                uid VARCHAR(50),
                expiry DATETIME NOT NULL,
                FOREIGN KEY (uid) REFERENCES KodUser(uid)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
        return True
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
        return False

def execute_query(query, params=None, fetch=False):
    """Execute a database query"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            result = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None
