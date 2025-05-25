#!/usr/bin/env python3
"""
Focused test for Quantum Cryptography Signature Verification
Tests the FIXED verification functionality to ensure it works correctly.
"""

import requests
import json
import time
import base64

# Backend URL
BACKEND_URL = "https://54afd158-c35e-4697-9ab5-92696b33d177.preview.emergentagent.com"

def test_signature_verification_comprehensive():
    """
    Comprehensive test for quantum signature verification.
    Tests multiple scenarios to ensure the fix is working correctly.
    """
    print("=" * 80)
    print("QUANTUM CRYPTOGRAPHY SIGNATURE VERIFICATION TEST")
    print("=" * 80)
    
    # Test messages for verification
    test_messages = [
        "Hello, quantum world!",
        "This is a test message for quantum cryptography",
        "政治透明度很重要",  # Chinese characters
        "🔐 Quantum security test 🔐",  # Emojis
        "A" * 1000,  # Long message
        "",  # Empty message
        "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?",
        "Multi\nline\nmessage\ntest"
    ]
    
    valid_signature_results = []
    invalid_signature_results = []
    
    print(f"\n1. TESTING VALID SIGNATURES ({len(test_messages)} different messages)")
    print("-" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: Message = '{message[:50]}{'...' if len(message) > 50 else ''}'")
        
        try:
            # Step 1: Generate keypair
            keypair_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/generate-keypair")
            if keypair_response.status_code != 200:
                print(f"❌ Failed to generate keypair: {keypair_response.status_code}")
                continue
                
            keypair = keypair_response.json()
            print(f"   ✅ Keypair generated")
            
            # Step 2: Sign the message
            sign_payload = {
                "message": message,
                "private_key": keypair["private_key"]
            }
            
            sign_response = requests.post(
                f"{BACKEND_URL}/api/quantum/crypto/sign",
                json=sign_payload
            )
            
            if sign_response.status_code != 200:
                print(f"❌ Failed to sign message: {sign_response.status_code}")
                continue
                
            signature_data = sign_response.json()
            print(f"   ✅ Message signed")
            
            # Step 3: Verify the signature (VALID case)
            verify_payload = {
                "message": message,
                "signature": signature_data["signature"],
                "public_key": keypair["public_key"]
            }
            
            verify_response = requests.post(
                f"{BACKEND_URL}/api/quantum/crypto/verify",
                json=verify_payload
            )
            
            if verify_response.status_code != 200:
                print(f"❌ Failed to verify signature: {verify_response.status_code}")
                continue
                
            verify_result = verify_response.json()
            is_valid = verify_result.get("is_valid", False)
            
            if is_valid:
                print(f"   ✅ Signature verification: VALID (Expected: VALID)")
                valid_signature_results.append(True)
            else:
                print(f"   ❌ Signature verification: INVALID (Expected: VALID) - BUG!")
                valid_signature_results.append(False)
                
        except Exception as e:
            print(f"❌ Error in test {i}: {str(e)}")
            valid_signature_results.append(False)
    
    print(f"\n2. TESTING INVALID SIGNATURES (Modified signatures)")
    print("-" * 60)
    
    # Test invalid signatures by modifying valid signatures
    for i, message in enumerate(test_messages[:4], 1):  # Test first 4 messages for invalid cases
        print(f"\nInvalid Test {i}: Message = '{message[:50]}{'...' if len(message) > 50 else ''}'")
        
        try:
            # Generate keypair and sign message
            keypair_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/generate-keypair")
            keypair = keypair_response.json()
            
            sign_payload = {
                "message": message,
                "private_key": keypair["private_key"]
            }
            
            sign_response = requests.post(
                f"{BACKEND_URL}/api/quantum/crypto/sign",
                json=sign_payload
            )
            signature_data = sign_response.json()
            
            # Modify the signature to make it invalid
            original_signature = signature_data["signature"]
            
            # Decode, modify a byte, and re-encode
            try:
                decoded_sig = base64.b64decode(original_signature)
                modified_sig = bytearray(decoded_sig)
                if len(modified_sig) > 0:
                    modified_sig[0] = (modified_sig[0] + 1) % 256  # Change first byte
                invalid_signature = base64.b64encode(bytes(modified_sig)).decode('utf-8')
            except:
                # If base64 decode fails, just modify the string
                invalid_signature = original_signature[:-1] + "X"
            
            print(f"   ✅ Created invalid signature")
            
            # Verify the invalid signature
            verify_payload = {
                "message": message,
                "signature": invalid_signature,
                "public_key": keypair["public_key"]
            }
            
            verify_response = requests.post(
                f"{BACKEND_URL}/api/quantum/crypto/verify",
                json=verify_payload
            )
            
            verify_result = verify_response.json()
            is_valid = verify_result.get("is_valid", True)  # Default to True to catch bugs
            
            if not is_valid:
                print(f"   ✅ Invalid signature verification: INVALID (Expected: INVALID)")
                invalid_signature_results.append(True)
            else:
                print(f"   ❌ Invalid signature verification: VALID (Expected: INVALID) - BUG!")
                invalid_signature_results.append(False)
                
        except Exception as e:
            print(f"❌ Error in invalid test {i}: {str(e)}")
            invalid_signature_results.append(False)
    
    # Test with wrong public key
    print(f"\nInvalid Test 5: Wrong public key")
    try:
        # Generate two different keypairs
        keypair1_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/generate-keypair")
        keypair1 = keypair1_response.json()
        
        keypair2_response = requests.post(f"{BACKEND_URL}/api/quantum/crypto/generate-keypair")
        keypair2 = keypair2_response.json()
        
        # Sign with keypair1
        message = "Test message for wrong key"
        sign_payload = {
            "message": message,
            "private_key": keypair1["private_key"]
        }
        
        sign_response = requests.post(
            f"{BACKEND_URL}/api/quantum/crypto/sign",
            json=sign_payload
        )
        signature_data = sign_response.json()
        
        # Verify with keypair2's public key (wrong key)
        verify_payload = {
            "message": message,
            "signature": signature_data["signature"],
            "public_key": keypair2["public_key"]  # Wrong public key!
        }
        
        verify_response = requests.post(
            f"{BACKEND_URL}/api/quantum/crypto/verify",
            json=verify_payload
        )
        
        verify_result = verify_response.json()
        is_valid = verify_result.get("is_valid", True)
        
        if not is_valid:
            print(f"   ✅ Wrong key verification: INVALID (Expected: INVALID)")
            invalid_signature_results.append(True)
        else:
            print(f"   ❌ Wrong key verification: VALID (Expected: INVALID) - BUG!")
            invalid_signature_results.append(False)
            
    except Exception as e:
        print(f"❌ Error in wrong key test: {str(e)}")
        invalid_signature_results.append(False)
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    valid_passed = sum(valid_signature_results)
    valid_total = len(valid_signature_results)
    invalid_passed = sum(invalid_signature_results)
    invalid_total = len(invalid_signature_results)
    
    print(f"\nValid Signature Tests: {valid_passed}/{valid_total} passed")
    print(f"Invalid Signature Tests: {invalid_passed}/{invalid_total} passed")
    print(f"Overall Success Rate: {(valid_passed + invalid_passed)}/{(valid_total + invalid_total)} ({((valid_passed + invalid_passed)/(valid_total + invalid_total)*100):.1f}%)")
    
    if valid_passed == valid_total and invalid_passed == invalid_total:
        print("\n🎉 ALL TESTS PASSED! Quantum signature verification is working correctly.")
        return True
    else:
        print(f"\n❌ SOME TESTS FAILED!")
        if valid_passed < valid_total:
            print(f"   - {valid_total - valid_passed} valid signatures incorrectly rejected")
        if invalid_passed < invalid_total:
            print(f"   - {invalid_total - invalid_passed} invalid signatures incorrectly accepted")
        return False

if __name__ == "__main__":
    success = test_signature_verification_comprehensive()
    exit(0 if success else 1)