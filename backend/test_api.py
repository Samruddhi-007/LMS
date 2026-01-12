"""
Quick API Test Script
Run this to verify the backend is working
"""
import requests
import json

API_BASE = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get("http://localhost:8000/health")
    print(f"✅ Health: {response.json()}")
    return response.status_code == 200

def test_create_organization():
    """Test creating an organization"""
    print("\n🔍 Testing create organization...")
    
    data = {
        "lab_name": "Test Laboratory",
        "lab_address": "123 Main Street, Test Building",
        "lab_state": "Maharashtra",
        "lab_district": "Mumbai",
        "lab_city": "Mumbai",
        "lab_pin_code": "400001"
    }
    
    try:
        response = requests.post(f"{API_BASE}/organizations", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Organization created!")
            print(f"   ID: {result['id']}")
            print(f"   Name: {result['lab_name']}")
            return result['id']
        else:
            print(f"❌ Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_get_organization(org_id):
    """Test getting an organization"""
    print(f"\n🔍 Testing get organization {org_id}...")
    
    try:
        response = requests.get(f"{API_BASE}/organizations/{org_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Organization retrieved!")
            print(f"   Name: {result['lab_name']}")
            print(f"   Address: {result['lab_address']}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Backend API Test")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Backend is not running!")
        print("   Start it with: uvicorn app.main:app --host 0.0.0.0 --port 8000")
        exit(1)
    
    # Test 2: Create organization
    org_id = test_create_organization()
    if not org_id:
        print("\n❌ Failed to create organization!")
        exit(1)
    
    # Test 3: Get organization
    if not test_get_organization(org_id):
        print("\n❌ Failed to retrieve organization!")
        exit(1)
    
    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)
    print("\n💡 Your backend is working correctly!")
    print("   The issue is likely in the frontend integration.")
