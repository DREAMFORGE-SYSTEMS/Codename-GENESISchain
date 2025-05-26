#!/usr/bin/env python3
"""Debug route registration in detail."""

import sys
import os
sys.path.append('/app/backend')

def debug_route_registration():
    try:
        print("Debugging route registration...")
        
        # Import the app
        from server import app
        
        print(f"Total app routes: {len(app.routes)}")
        
        # Print all routes
        for i, route in enumerate(app.routes):
            if hasattr(route, 'path'):
                print(f"  {i}: {route.path} - {getattr(route, 'methods', 'N/A')}")
            else:
                print(f"  {i}: {type(route)} - {route}")
        
        # Check specifically for quantum routes
        quantum_routes = []
        for route in app.routes:
            if hasattr(route, 'path') and 'quantum' in route.path:
                quantum_routes.append(route)
        
        print(f"\nQuantum routes found: {len(quantum_routes)}")
        for route in quantum_routes:
            print(f"  - {route.path} {getattr(route, 'methods', 'N/A')}")
        
        # Check for API routes
        api_routes = []
        for route in app.routes:
            if hasattr(route, 'path') and '/api' in route.path:
                api_routes.append(route)
        
        print(f"\nAPI routes found: {len(api_routes)}")
        for route in api_routes:
            print(f"  - {route.path} {getattr(route, 'methods', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_route_registration()
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")