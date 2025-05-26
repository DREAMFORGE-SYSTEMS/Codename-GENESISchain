#!/usr/bin/env python3
"""Debug script to check quantum routes availability."""

import sys
import os
sys.path.append('/app/backend')

def test_quantum_routes():
    try:
        print("Testing quantum routes import...")
        
        # Test individual imports
        from randomness.optimized_quantum_randomness import create_optimized_randomness_generator
        print("✅ Optimized randomness import OK")
        
        from crypto.optimized_quantum_resistant import get_optimized_crypto
        print("✅ Optimized crypto import OK")
        
        from accountability.ledger import AccountabilityLedger
        print("✅ Accountability ledger import OK")
        
        # Test quantum routes import
        from api.quantum_routes import router as quantum_router
        print(f"✅ Quantum router import OK - {len(quantum_router.routes)} routes")
        
        # Test main API router import
        from api.routes import api_router
        print(f"✅ Main API router import OK - {len(api_router.routes)} total routes")
        
        # Check if quantum routes are in main router
        quantum_routes = [r for r in api_router.routes if '/quantum' in r.path]
        print(f"✅ Quantum routes in main router: {len(quantum_routes)}")
        
        # Test server import
        from server import app
        print("✅ Server app import OK")
        
        # Check if API router is included in app
        app_routes = [r for r in app.routes if hasattr(r, 'path') and '/api' in r.path]
        print(f"✅ API routes in app: {len(app_routes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_quantum_routes()
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")