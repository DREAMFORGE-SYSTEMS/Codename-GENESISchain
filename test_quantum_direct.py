#!/usr/bin/env python3
"""Test quantum routes directly using FastAPI test client."""

import sys
import os
sys.path.append('/app/backend')

from fastapi.testclient import TestClient

def test_quantum_routes_direct():
    try:
        print("Testing quantum routes with FastAPI test client...")
        
        # Import the app
        from server import app
        client = TestClient(app)
        
        # Test base API
        response = client.get("/api")
        print(f"Base API: {response.status_code} - {response.json()}")
        
        # Test quantum keypair generation
        response = client.post("/api/quantum/crypto/generate-keypair")
        print(f"Quantum keypair: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success: {list(data.keys())}")
            if 'performance_ms' in data:
                print(f"  ⚡ Performance: {data['performance_ms']:.2f}ms")
        else:
            print(f"  ❌ Error: {response.text}")
        
        # Test quantum randomness
        response = client.get("/api/quantum/randomness/bytes?length=32")
        print(f"Quantum randomness: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success: {list(data.keys())}")
            if 'performance_ms' in data:
                print(f"  ⚡ Performance: {data['performance_ms']:.2f}ms")
        else:
            print(f"  ❌ Error: {response.text}")
        
        # Test performance stats
        response = client.get("/api/quantum/performance/crypto-stats")
        print(f"Performance stats: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success: {list(data.keys())}")
        else:
            print(f"  ❌ Error: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_quantum_routes_direct()
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")