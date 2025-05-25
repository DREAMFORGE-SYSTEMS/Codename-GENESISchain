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

if __name__ == "__main__":
    pytest.main([__file__, "-v"])