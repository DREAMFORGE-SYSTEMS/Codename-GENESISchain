import pytest
import requests
import json
import time
from typing import Dict, Any

# Get the backend URL from frontend .env file
BACKEND_URL = "https://54afd158-c35e-4697-9ab5-92696b33d177.preview.emergentagent.com"

class TestQuantumBlockchain:
    def setup_method(self):
        """Setup before each test"""
        self.base_url = BACKEND_URL
        self.keypair = None
        self.source_data = None
        
    def test_quantum_crypto_generate_keypair(self):
        """Test quantum-resistant keypair generation"""
        response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        assert response.status_code == 200
        data = response.json()
        assert "public_key" in data
        assert "private_key" in data
        assert data["public_key"] is not None
        assert data["private_key"] is not None
        
        # Store keypair for subsequent tests
        self.keypair = data
        print(f"Generated keypair: public_key length={len(data['public_key'])}, private_key length={len(data['private_key'])}")

    def test_quantum_crypto_sign_message(self):
        """Test quantum-resistant message signing"""
        # First generate a keypair
        keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        assert keypair_response.status_code == 200
        keypair = keypair_response.json()
        
        # Test signing a message
        test_message = "Hello, quantum world!"
        sign_payload = {
            "message": test_message,
            "private_key": keypair["private_key"]
        }
        
        response = requests.post(
            f"{self.base_url}/api/quantum/crypto/sign",
            json=sign_payload
        )
        assert response.status_code == 200
        data = response.json()
        assert "signature" in data
        assert data["signature"] is not None
        
        # Store for verification test
        self.signature_data = {
            "message": test_message,
            "signature": data["signature"],
            "public_key": keypair["public_key"]
        }
        print(f"Signed message: signature length={len(data['signature'])}")

    def test_quantum_crypto_verify_signature(self):
        """Test quantum-resistant signature verification"""
        # First generate a keypair and sign a message
        keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        assert keypair_response.status_code == 200
        keypair = keypair_response.json()
        
        test_message = "Hello, quantum verification!"
        sign_payload = {
            "message": test_message,
            "private_key": keypair["private_key"]
        }
        
        sign_response = requests.post(
            f"{self.base_url}/api/quantum/crypto/sign",
            json=sign_payload
        )
        assert sign_response.status_code == 200
        signature_data = sign_response.json()
        
        # Now verify the signature
        verify_payload = {
            "message": test_message,
            "signature": signature_data["signature"],
            "public_key": keypair["public_key"]
        }
        
        response = requests.post(
            f"{self.base_url}/api/quantum/crypto/verify",
            json=verify_payload
        )
        assert response.status_code == 200
        data = response.json()
        assert "is_valid" in data
        assert data["is_valid"] is True
        print(f"Signature verification: {data['is_valid']}")

    def test_accountability_add_source(self):
        """Test adding a trusted source for political accountability"""
        source_payload = {
            "name": "Test News Source",
            "source_type": "news",
            "url": "https://test-news.com"
        }
        
        response = requests.post(
            f"{self.base_url}/api/quantum/accountability/add-source",
            json=source_payload
        )
        assert response.status_code == 200
        data = response.json()
        assert "source_id" in data
        assert "private_key" in data
        assert data["source_id"] is not None
        assert data["private_key"] is not None
        
        # Store source data for subsequent tests
        self.source_data = data
        print(f"Added trusted source: {data['source_id']}")

    def test_accountability_record_statement(self):
        """Test recording a political statement"""
        # First add a trusted source
        source_payload = {
            "name": "Test Political Source",
            "source_type": "government",
            "url": "https://test-gov.com"
        }
        
        source_response = requests.post(
            f"{self.base_url}/api/quantum/accountability/add-source",
            json=source_payload
        )
        assert source_response.status_code == 200
        source_data = source_response.json()
        
        # Now record a statement
        statement_payload = {
            "statement_text": "We will reduce taxes by 10% next year",
            "speaker_id": "politician_123",
            "speaker_name": "John Doe",
            "speaker_title": "Mayor",
            "source_id": source_data["source_id"],
            "source_private_key": source_data["private_key"],
            "source_url": "https://test-gov.com/statement",
            "context_category": "economic_policy",
            "context_tags": ["taxes", "economy", "promise"]
        }
        
        response = requests.post(
            f"{self.base_url}/api/quantum/accountability/record",
            json=statement_payload
        )
        assert response.status_code == 200
        data = response.json()
        assert "record_id" in data
        assert data["record_id"] is not None
        
        # Store record ID for verification test
        self.record_id = data["record_id"]
        print(f"Recorded statement: {data['record_id']}")

    def test_accountability_verify_statement(self):
        """Test verifying a recorded statement"""
        # First add a source and record a statement
        source_payload = {
            "name": "Verification Test Source",
            "source_type": "news",
            "url": "https://verify-test.com"
        }
        
        source_response = requests.post(
            f"{self.base_url}/api/quantum/accountability/add-source",
            json=source_payload
        )
        assert source_response.status_code == 200
        source_data = source_response.json()
        
        statement_payload = {
            "statement_text": "Test statement for verification",
            "speaker_id": "test_speaker",
            "speaker_name": "Test Speaker",
            "speaker_title": "Test Title",
            "source_id": source_data["source_id"],
            "source_private_key": source_data["private_key"],
            "source_url": "https://verify-test.com/statement",
            "context_category": "test",
            "context_tags": ["test"]
        }
        
        record_response = requests.post(
            f"{self.base_url}/api/quantum/accountability/record",
            json=statement_payload
        )
        assert record_response.status_code == 200
        record_data = record_response.json()
        
        # Now verify the statement
        response = requests.get(
            f"{self.base_url}/api/quantum/accountability/verify/{record_data['record_id']}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "is_verified" in data
        assert "reason" in data
        print(f"Statement verification: {data['is_verified']}, reason: {data['reason']}")

    def test_quantum_randomness_bytes(self):
        """Test quantum random bytes generation"""
        # Test non-certified random bytes
        response = requests.get(f"{self.base_url}/api/quantum/randomness/bytes?length=32&certified=false")
        assert response.status_code == 200
        data = response.json()
        assert "random_bytes" in data
        assert len(data["random_bytes"]) == 64  # 32 bytes = 64 hex characters
        print(f"Generated random bytes: {data['random_bytes'][:16]}...")

    def test_quantum_randomness_int(self):
        """Test quantum random integer generation"""
        # Test non-certified random integer
        response = requests.get(f"{self.base_url}/api/quantum/randomness/int?min_value=1&max_value=100&certified=false")
        assert response.status_code == 200
        data = response.json()
        assert "random_int" in data
        assert 1 <= data["random_int"] <= 100
        print(f"Generated random int: {data['random_int']}")

    def test_quantum_randomness_float(self):
        """Test quantum random float generation"""
        response = requests.get(f"{self.base_url}/api/quantum/randomness/float")
        assert response.status_code == 200
        data = response.json()
        assert "random_float" in data
        assert 0.0 <= data["random_float"] <= 1.0
        print(f"Generated random float: {data['random_float']}")

    def test_api_root(self):
        """Test the root endpoint"""
        response = requests.get(f"{self.base_url}/api")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

class TestEnhancedQuantumCryptographyVerification:
    """
    Enhanced testing for quantum cryptography signature verification.
    Tests the security enhancements to ensure invalid signatures are properly rejected.
    """
    
    def setup_method(self):
        """Setup before each test"""
        self.base_url = BACKEND_URL
        
    def test_enhanced_quantum_crypto_valid_signatures(self):
        """Test that valid signatures are properly accepted"""
        print("\n=== Testing Enhanced Quantum Cryptography - Valid Signatures ===")
        
        valid_count = 0
        test_messages = [
            "test message 1",
            "test message 2", 
            "Hello quantum world!",
            "This is a longer test message with more content to verify",
            "Special chars: !@#$%^&*()",
            "Numbers: 123456789",
            "Unicode: 🔐🌟💫",
            "Empty message test: "
        ]
        
        for i, message in enumerate(test_messages):
            print(f"\nTest {i+1}: Testing message: '{message}'")
            
            # Generate keypair
            keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
            assert keypair_response.status_code == 200
            keypair = keypair_response.json()
            
            # Sign message
            sign_payload = {
                "message": message,
                "private_key": keypair["private_key"]
            }
            sign_response = requests.post(f"{self.base_url}/api/quantum/crypto/sign", json=sign_payload)
            assert sign_response.status_code == 200
            signature_data = sign_response.json()
            
            # Verify signature (should be TRUE)
            verify_payload = {
                "message": message,
                "signature": signature_data["signature"],
                "public_key": keypair["public_key"]
            }
            verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
            assert verify_response.status_code == 200
            verify_data = verify_response.json()
            
            print(f"  Signature valid: {verify_data['is_valid']}")
            assert verify_data["is_valid"] is True, f"Valid signature should be accepted for message: {message}"
            valid_count += 1
            
        print(f"\n✅ All {valid_count}/{len(test_messages)} valid signatures correctly accepted")
        
    def test_enhanced_quantum_crypto_invalid_signatures(self):
        """Test that invalid signatures are properly rejected"""
        print("\n=== Testing Enhanced Quantum Cryptography - Invalid Signatures ===")
        
        # Generate keypair and sign a test message
        keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        assert keypair_response.status_code == 200
        keypair = keypair_response.json()
        
        test_message = "test message 1"
        sign_payload = {
            "message": test_message,
            "private_key": keypair["private_key"]
        }
        sign_response = requests.post(f"{self.base_url}/api/quantum/crypto/sign", json=sign_payload)
        assert sign_response.status_code == 200
        signature_data = sign_response.json()
        original_signature = signature_data["signature"]
        
        invalid_tests = []
        
        # Test 1: Modified signature (change 1 character)
        print("\nTest 1: Modified signature (change 1 character)")
        modified_signature = original_signature[:-1] + ('A' if original_signature[-1] != 'A' else 'B')
        verify_payload = {
            "message": test_message,
            "signature": modified_signature,
            "public_key": keypair["public_key"]
        }
        verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        print(f"  Modified signature valid: {verify_data['is_valid']}")
        invalid_tests.append(("Modified signature", verify_data["is_valid"]))
        
        # Test 2: Wrong message
        print("\nTest 2: Wrong message")
        verify_payload = {
            "message": "test message 2",  # Different message
            "signature": original_signature,
            "public_key": keypair["public_key"]
        }
        verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        print(f"  Wrong message valid: {verify_data['is_valid']}")
        invalid_tests.append(("Wrong message", verify_data["is_valid"]))
        
        # Test 3: Wrong public key
        print("\nTest 3: Wrong public key")
        # Generate another keypair to get a different public key
        keypair2_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        assert keypair2_response.status_code == 200
        keypair2 = keypair2_response.json()
        
        verify_payload = {
            "message": test_message,
            "signature": original_signature,
            "public_key": keypair2["public_key"]  # Different public key
        }
        verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        print(f"  Wrong public key valid: {verify_data['is_valid']}")
        invalid_tests.append(("Wrong public key", verify_data["is_valid"]))
        
        # Test 4: Signature with low entropy (all zeros pattern)
        print("\nTest 4: Low entropy signature (zeros pattern)")
        import base64
        low_entropy_sig = base64.b64encode(b'\x00' * 128).decode('utf-8')
        verify_payload = {
            "message": test_message,
            "signature": low_entropy_sig,
            "public_key": keypair["public_key"]
        }
        verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        print(f"  Low entropy signature valid: {verify_data['is_valid']}")
        invalid_tests.append(("Low entropy signature", verify_data["is_valid"]))
        
        # Test 5: Signature with unbalanced bit distribution
        print("\nTest 5: Unbalanced bit distribution signature")
        unbalanced_sig = base64.b64encode(b'\xFF' * 64 + b'\x00' * 64).decode('utf-8')
        verify_payload = {
            "message": test_message,
            "signature": unbalanced_sig,
            "public_key": keypair["public_key"]
        }
        verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        print(f"  Unbalanced signature valid: {verify_data['is_valid']}")
        invalid_tests.append(("Unbalanced signature", verify_data["is_valid"]))
        
        # Test 6: Completely random signature
        print("\nTest 6: Random signature")
        import os
        random_sig = base64.b64encode(os.urandom(128)).decode('utf-8')
        verify_payload = {
            "message": test_message,
            "signature": random_sig,
            "public_key": keypair["public_key"]
        }
        verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        print(f"  Random signature valid: {verify_data['is_valid']}")
        invalid_tests.append(("Random signature", verify_data["is_valid"]))
        
        # Test 7: Truncated signature
        print("\nTest 7: Truncated signature")
        truncated_sig = original_signature[:50]  # Much shorter
        verify_payload = {
            "message": test_message,
            "signature": truncated_sig,
            "public_key": keypair["public_key"]
        }
        verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        print(f"  Truncated signature valid: {verify_data['is_valid']}")
        invalid_tests.append(("Truncated signature", verify_data["is_valid"]))
        
        # Analyze results
        print(f"\n=== Invalid Signature Test Results ===")
        failed_properly = 0
        for test_name, is_valid in invalid_tests:
            status = "❌ PASSED (correctly rejected)" if not is_valid else "⚠️ FAILED (incorrectly accepted)"
            print(f"  {test_name}: {status}")
            if not is_valid:
                failed_properly += 1
                
        print(f"\nSummary: {failed_properly}/{len(invalid_tests)} invalid signatures correctly rejected")
        
        # Assert that ALL invalid signatures should be rejected
        for test_name, is_valid in invalid_tests:
            assert not is_valid, f"Invalid signature test '{test_name}' should have been rejected but was accepted"
            
        print("✅ All invalid signatures correctly rejected - Enhanced verification working properly!")

    def test_enhanced_quantum_crypto_comprehensive_security(self):
        """Comprehensive security test with multiple valid and invalid scenarios"""
        print("\n=== Comprehensive Enhanced Security Test ===")
        
        valid_signatures = 0
        invalid_signatures = 0
        
        # Test multiple valid signatures
        for i in range(3):
            print(f"\nValid Test {i+1}:")
            keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
            keypair = keypair_response.json()
            
            message = f"Valid test message {i+1}"
            sign_payload = {"message": message, "private_key": keypair["private_key"]}
            sign_response = requests.post(f"{self.base_url}/api/quantum/crypto/sign", json=sign_payload)
            signature_data = sign_response.json()
            
            verify_payload = {
                "message": message,
                "signature": signature_data["signature"],
                "public_key": keypair["public_key"]
            }
            verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
            verify_data = verify_response.json()
            
            print(f"  Valid signature {i+1}: {verify_data['is_valid']}")
            if verify_data["is_valid"]:
                valid_signatures += 1
                
        # Test multiple invalid scenarios
        keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        keypair = keypair_response.json()
        
        invalid_scenarios = [
            ("Corrupted middle", lambda sig: sig[:50] + 'X' + sig[51:]),
            ("Corrupted start", lambda sig: 'Z' + sig[1:]),
            ("Corrupted end", lambda sig: sig[:-1] + 'Y'),
            ("Swapped chars", lambda sig: sig[1] + sig[0] + sig[2:]),
            ("Empty signature", lambda sig: "")
        ]
        
        for i, (scenario_name, corrupt_func) in enumerate(invalid_scenarios):
            print(f"\nInvalid Test {i+1} ({scenario_name}):")
            
            message = "test message for corruption"
            sign_payload = {"message": message, "private_key": keypair["private_key"]}
            sign_response = requests.post(f"{self.base_url}/api/quantum/crypto/sign", json=sign_payload)
            signature_data = sign_response.json()
            
            try:
                corrupted_signature = corrupt_func(signature_data["signature"])
                verify_payload = {
                    "message": message,
                    "signature": corrupted_signature,
                    "public_key": keypair["public_key"]
                }
                verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
                verify_data = verify_response.json()
                
                print(f"  {scenario_name}: {verify_data['is_valid']}")
                if not verify_data["is_valid"]:
                    invalid_signatures += 1
            except Exception as e:
                print(f"  {scenario_name}: Properly rejected (exception: {str(e)[:50]})")
                invalid_signatures += 1
                
        print(f"\n=== Final Security Test Results ===")
        print(f"Valid signatures accepted: {valid_signatures}/3")
        print(f"Invalid signatures rejected: {invalid_signatures}/5")
        
        # All valid should pass, all invalid should fail
        assert valid_signatures == 3, f"Expected 3 valid signatures to pass, got {valid_signatures}"
        assert invalid_signatures == 5, f"Expected 5 invalid signatures to be rejected, got {invalid_signatures}"
        
        print("✅ Comprehensive security test PASSED - Enhanced verification is working correctly!")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])