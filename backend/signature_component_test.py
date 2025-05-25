#!/usr/bin/env python3
"""
Test to understand exactly what the verification function is checking
"""

import requests
import base64

BACKEND_URL = "https://54afd158-c35e-4697-9ab5-92696b33d177.preview.emergentagent.com"

def test_signature_components():
    """Test what happens when we modify different parts of the signature"""
    print("Testing signature component validation...")
    
    # Generate keypair and sign a message
    keypair_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/generate-keypair")
    keypair = keypair_response.json()
    
    message = "test message"
    sign_payload = {
        "message": message,
        "private_key": keypair["private_key"]
    }
    
    sign_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/sign", json=sign_payload)
    signature_data = sign_response.json()
    original_signature = signature_data["signature"]
    
    print(f"Original signature length: {len(original_signature)}")
    
    # Decode the signature to understand its structure
    decoded_sig = base64.b64decode(original_signature)
    print(f"Decoded signature length: {len(decoded_sig)} bytes")
    
    # According to the code:
    # signature_core = signature[:64]     # SHA3-512 output
    # entropy_component = signature[64:96] # SHA3-256 output  
    # stored_message_hash = signature[96:128] # SHA3-256 output
    
    signature_core = decoded_sig[:64]
    entropy_component = decoded_sig[64:96]
    stored_message_hash = decoded_sig[96:128]
    
    print(f"Signature core: {len(signature_core)} bytes")
    print(f"Entropy component: {len(entropy_component)} bytes") 
    print(f"Stored message hash: {len(stored_message_hash)} bytes")
    
    # Test 1: Modify signature core (first 64 bytes)
    print("\n1. Testing with modified signature core...")
    modified_sig1 = bytearray(decoded_sig)
    modified_sig1[0] = (modified_sig1[0] + 1) % 256
    modified_signature1 = base64.b64encode(bytes(modified_sig1)).decode('utf-8')
    
    verify_payload = {
        "message": message,
        "signature": modified_signature1,
        "public_key": keypair["public_key"]
    }
    
    verify_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/verify", json=verify_payload)
    result1 = verify_response.json()
    print(f"Modified signature core result: {result1}")
    
    # Test 2: Modify entropy component (bytes 64-96)
    print("\n2. Testing with modified entropy component...")
    modified_sig2 = bytearray(decoded_sig)
    modified_sig2[70] = (modified_sig2[70] + 1) % 256  # Modify entropy component
    modified_signature2 = base64.b64encode(bytes(modified_sig2)).decode('utf-8')
    
    verify_payload["signature"] = modified_signature2
    verify_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/verify", json=verify_payload)
    result2 = verify_response.json()
    print(f"Modified entropy component result: {result2}")
    
    # Test 3: Modify stored message hash (bytes 96-128)
    print("\n3. Testing with modified message hash...")
    modified_sig3 = bytearray(decoded_sig)
    modified_sig3[100] = (modified_sig3[100] + 1) % 256  # Modify message hash
    modified_signature3 = base64.b64encode(bytes(modified_sig3)).decode('utf-8')
    
    verify_payload["signature"] = modified_signature3
    verify_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/verify", json=verify_payload)
    result3 = verify_response.json()
    print(f"Modified message hash result: {result3}")
    
    # Test 4: Use different message (should fail message hash check)
    print("\n4. Testing with different message...")
    verify_payload = {
        "message": "different message",
        "signature": original_signature,
        "public_key": keypair["public_key"]
    }
    
    verify_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/verify", json=verify_payload)
    result4 = verify_response.json()
    print(f"Different message result: {result4}")

if __name__ == "__main__":
    test_signature_components()