#!/usr/bin/env python3
"""
Quick test to demonstrate the signature verification bug
"""

import requests
import json

BACKEND_URL = "https://54afd158-c35e-4697-9ab5-92696b33d177.preview.emergentagent.com"

def test_obvious_invalid_signature():
    """Test with obviously invalid signature to confirm the bug"""
    print("Testing with obviously invalid signature...")
    
    # Generate a keypair
    keypair_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/generate-keypair")
    keypair = keypair_response.json()
    
    # Test with completely invalid signature
    verify_payload = {
        "message": "test message",
        "signature": "obviously_invalid_signature_that_should_fail",
        "public_key": keypair["public_key"]
    }
    
    verify_response = requests.post(
        f"{BACKEND_URL}/api/quantum/crypto/verify",
        json=verify_payload
    )
    
    result = verify_response.json()
    print(f"Result for obviously invalid signature: {result}")
    
    if result.get("is_valid", False):
        print("❌ BUG CONFIRMED: Obviously invalid signature accepted as valid!")
    else:
        print("✅ Good: Obviously invalid signature correctly rejected")

if __name__ == "__main__":
    test_obvious_invalid_signature()