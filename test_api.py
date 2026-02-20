"""
Kodbank API Test Script
Run this script to test all API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_init():
    """Test database initialization"""
    print("\n=== Testing /init endpoint ===")
    response = requests.get(f"{BASE_URL}/init")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("\n=== Testing /register endpoint ===")
    
    # Test 1: Valid registration
    user_data = {
        "uid": "1",
        "username": "testuser",
        "email": "test@kod.in",
        "password": "password123",
        "phone": "9876543210",
        "role": "Customer"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    print(f"\nTest 1 - Valid Registration:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Duplicate username
    response2 = requests.post(f"{BASE_URL}/register", json=user_data)
    print(f"\nTest 2 - Duplicate Username:")
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.json()}")
    
    # Test 3: Missing required fields
    invalid_data = {"username": "newuser"}
    response3 = requests.post(f"{BASE_URL}/register", json=invalid_data)
    print(f"\nTest 3 - Missing Required Fields:")
    print(f"Status: {response3.status_code}")
    print(f"Response: {response3.json()}")
    
    return response.status_code == 201

def test_login():
    """Test user login"""
    print("\n=== Testing /login endpoint ===")
    
    # Test 1: Valid login
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    session = requests.Session()
    response = session.post(f"{BASE_URL}/login", json=login_data)
    print(f"\nTest 1 - Valid Login:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Cookies: {session.cookies.get_dict()}")
    
    # Test 2: Invalid password
    wrong_password = {"username": "testuser", "password": "wrongpass"}
    response2 = session.post(f"{BASE_URL}/login", json=wrong_password)
    print(f"\nTest 2 - Invalid Password:")
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.json()}")
    
    # Test 3: Non-existent user
    nonexistent = {"username": "nonexistent", "password": "pass"}
    response3 = session.post(f"{BASE_URL}/login", json=nonexistent)
    print(f"\nTest 3 - Non-existent User:")
    print(f"Status: {response3.status_code}")
    print(f"Response: {response3.json()}")
    
    return response.status_code == 200

def test_get_balance():
    """Test get balance endpoint"""
    print("\n=== Testing /getBalance endpoint ===")
    
    session = requests.Session()
    
    # First login to get token
    login_data = {"username": "testuser", "password": "password123"}
    session.post(f"{BASE_URL}/login", json=login_data)
    
    # Test 1: With valid token (cookie)
    response = session.post(f"{BASE_URL}/getBalance")
    print(f"\nTest 1 - Valid Token:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Without token
    response2 = requests.post(f"{BASE_URL}/getBalance")
    print(f"\nTest 2 - Without Token:")
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.json()}")
    
    return response.status_code == 200

def test_verify():
    """Test token verification"""
    print("\n=== Testing /verify endpoint ===")
    
    session = requests.Session()
    login_data = {"username": "testuser", "password": "password123"}
    session.post(f"{BASE_URL}/login", json=login_data)
    
    # Test 1: With valid token
    response = session.get(f"{BASE_URL}/verify")
    print(f"\nTest 1 - Valid Token:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Without token
    response2 = requests.get(f"{BASE_URL}/verify")
    print(f"\nTest 2 - Without Token:")
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.json()}")
    
    return response.status_code == 200

def test_logout():
    """Test logout endpoint"""
    print("\n=== Testing /logout endpoint ===")
    
    session = requests.Session()
    login_data = {"username": "testuser", "password": "password123"}
    session.post(f"{BASE_URL}/login", json=login_data)
    
    # Test 1: Logout
    response = session.post(f"{BASE_URL}/logout")
    print(f"\nTest 1 - Logout:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Cookies after logout: {session.cookies.get_dict()}")
    
    # Test 2: Try to get balance after logout
    response2 = session.post(f"{BASE_URL}/getBalance")
    print(f"\nTest 2 - Get Balance After Logout:")
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.json()}")
    
    return response.status_code == 200

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("KODBANK API TEST SUITE")
    print("=" * 50)
    
    try:
        test_init()
        test_register()
        test_login()
        test_get_balance()
        test_verify()
        test_logout()
        
        print("\n" + "=" * 50)
        print("ALL TESTS COMPLETED!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to server!")
        print("Make sure the Flask server is running on localhost:5000")
    except Exception as e:
        print(f"\nERROR: {str(e)}")

if __name__ == "__main__":
    run_all_tests()
