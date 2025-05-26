"""
PERFORMANCE-OPTIMIZED Quantum Blockchain Features Testing

This test suite validates the Phase 1 - Performance Optimization implementation
for quantum blockchain features including:
1. Optimized crypto operations with performance timing
2. Optimized randomness generation with performance timing  
3. Batch operations for improved efficiency
4. Performance monitoring endpoints

Expected Results:
- All endpoints should work correctly with valid results
- Performance timing should be included showing faster execution (performance_ms field)
- Batch operations should be significantly faster than individual calls
- Security should be maintained (valid signatures verify as true, invalid as false)
"""

import pytest
import requests
import json
import time
import base64
import os
from typing import Dict, Any, List

# Get the backend URL from frontend .env file
BACKEND_URL = "https://54afd158-c35e-4697-9ab5-92696b33d177.preview.emergentagent.com"

class TestPerformanceOptimizedQuantumCrypto:
    """Test Performance-Optimized Quantum Cryptography Operations"""
    
    def setup_method(self):
        """Setup before each test"""
        self.base_url = BACKEND_URL
        
    def test_optimized_crypto_generate_keypair_with_performance(self):
        """Test optimized keypair generation with performance timing"""
        print("\n=== Testing Optimized Crypto - Generate Keypair ===")
        
        response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields
        assert "public_key" in data
        assert "private_key" in data
        assert "performance_ms" in data
        
        # Verify data validity
        assert data["public_key"] is not None
        assert data["private_key"] is not None
        assert isinstance(data["performance_ms"], (int, float))
        assert data["performance_ms"] > 0
        
        print(f"✅ Keypair generated successfully")
        print(f"   Public key length: {len(data['public_key'])}")
        print(f"   Private key length: {len(data['private_key'])}")
        print(f"   Performance: {data['performance_ms']:.2f}ms")
        
        return data
        
    def test_optimized_crypto_sign_with_performance(self):
        """Test optimized message signing with performance timing"""
        print("\n=== Testing Optimized Crypto - Sign Message ===")
        
        # First generate a keypair
        keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        assert keypair_response.status_code == 200
        keypair = keypair_response.json()
        
        # Test signing
        test_message = "Performance test message for signing"
        sign_payload = {
            "message": test_message,
            "private_key": keypair["private_key"]
        }
        
        response = requests.post(f"{self.base_url}/api/quantum/crypto/sign", json=sign_payload)
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields
        assert "signature" in data
        assert "performance_ms" in data
        
        # Verify data validity
        assert data["signature"] is not None
        assert isinstance(data["performance_ms"], (int, float))
        assert data["performance_ms"] > 0
        
        print(f"✅ Message signed successfully")
        print(f"   Signature length: {len(data['signature'])}")
        print(f"   Performance: {data['performance_ms']:.2f}ms")
        
        return {
            "message": test_message,
            "signature": data["signature"],
            "public_key": keypair["public_key"],
            "performance_ms": data["performance_ms"]
        }
        
    def test_optimized_crypto_verify_with_performance(self):
        """Test optimized signature verification with performance timing"""
        print("\n=== Testing Optimized Crypto - Verify Signature ===")
        
        # First generate keypair and sign a message
        keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        assert keypair_response.status_code == 200
        keypair = keypair_response.json()
        
        test_message = "Performance test message for verification"
        sign_payload = {
            "message": test_message,
            "private_key": keypair["private_key"]
        }
        
        sign_response = requests.post(f"{self.base_url}/api/quantum/crypto/sign", json=sign_payload)
        assert sign_response.status_code == 200
        signature_data = sign_response.json()
        
        # Test verification
        verify_payload = {
            "message": test_message,
            "signature": signature_data["signature"],
            "public_key": keypair["public_key"]
        }
        
        response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields
        assert "is_valid" in data
        assert "performance_ms" in data
        
        # Verify data validity
        assert data["is_valid"] is True  # Should be valid signature
        assert isinstance(data["performance_ms"], (int, float))
        assert data["performance_ms"] > 0
        
        print(f"✅ Signature verified successfully")
        print(f"   Is valid: {data['is_valid']}")
        print(f"   Performance: {data['performance_ms']:.2f}ms")
        
        return data
        
    def test_optimized_crypto_batch_verify(self):
        """Test batch signature verification for improved performance"""
        print("\n=== Testing Optimized Crypto - Batch Verify ===")
        
        # Generate multiple keypairs and signatures for batch testing
        verification_requests = []
        
        for i in range(3):  # Test with 3 verifications as requested
            # Generate keypair
            keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
            assert keypair_response.status_code == 200
            keypair = keypair_response.json()
            
            # Sign message
            test_message = f"Batch test message {i+1}"
            sign_payload = {
                "message": test_message,
                "private_key": keypair["private_key"]
            }
            
            sign_response = requests.post(f"{self.base_url}/api/quantum/crypto/sign", json=sign_payload)
            assert sign_response.status_code == 200
            signature_data = sign_response.json()
            
            # Add to batch verification request
            verification_requests.append({
                "message": test_message,
                "signature": signature_data["signature"],
                "public_key": keypair["public_key"]
            })
        
        # Perform batch verification
        batch_payload = {
            "verifications": verification_requests
        }
        
        response = requests.post(f"{self.base_url}/api/quantum/crypto/batch-verify", json=batch_payload)
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields
        assert "results" in data
        assert "total_performance_ms" in data
        assert "average_performance_ms" in data
        
        # Verify data validity
        assert len(data["results"]) == 3
        assert all(result is True for result in data["results"])  # All should be valid
        assert isinstance(data["total_performance_ms"], (int, float))
        assert isinstance(data["average_performance_ms"], (int, float))
        assert data["total_performance_ms"] > 0
        assert data["average_performance_ms"] > 0
        
        print(f"✅ Batch verification completed successfully")
        print(f"   Verifications: {len(data['results'])}")
        print(f"   All valid: {all(data['results'])}")
        print(f"   Total performance: {data['total_performance_ms']:.2f}ms")
        print(f"   Average performance: {data['average_performance_ms']:.2f}ms")
        
        return data

class TestPerformanceOptimizedQuantumRandomness:
    """Test Performance-Optimized Quantum Randomness Generation"""
    
    def setup_method(self):
        """Setup before each test"""
        self.base_url = BACKEND_URL
        
    def test_optimized_randomness_bytes_with_performance(self):
        """Test optimized random bytes generation with performance timing"""
        print("\n=== Testing Optimized Randomness - Generate Bytes ===")
        
        response = requests.get(f"{self.base_url}/api/quantum/randomness/bytes?length=64")
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields
        assert "random_bytes" in data
        assert "performance_ms" in data
        
        # Verify data validity
        assert data["random_bytes"] is not None
        random_bytes = base64.b64decode(data["random_bytes"])
        assert len(random_bytes) == 64  # Should be 64 bytes as requested
        assert isinstance(data["performance_ms"], (int, float))
        assert data["performance_ms"] > 0
        
        print(f"✅ Random bytes generated successfully")
        print(f"   Bytes length: {len(random_bytes)}")
        print(f"   Base64 length: {len(data['random_bytes'])}")
        print(f"   Performance: {data['performance_ms']:.2f}ms")
        
        return data
        
    def test_optimized_randomness_int_with_performance(self):
        """Test optimized random integer generation with performance timing"""
        print("\n=== Testing Optimized Randomness - Generate Integer ===")
        
        response = requests.get(f"{self.base_url}/api/quantum/randomness/int?min_value=1&max_value=1000")
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields
        assert "random_int" in data
        assert "performance_ms" in data
        
        # Verify data validity
        assert isinstance(data["random_int"], int)
        assert 1 <= data["random_int"] <= 1000
        assert isinstance(data["performance_ms"], (int, float))
        assert data["performance_ms"] > 0
        
        print(f"✅ Random integer generated successfully")
        print(f"   Random int: {data['random_int']}")
        print(f"   Performance: {data['performance_ms']:.2f}ms")
        
        return data
        
    def test_optimized_randomness_float_with_performance(self):
        """Test optimized random float generation with performance timing"""
        print("\n=== Testing Optimized Randomness - Generate Float ===")
        
        response = requests.get(f"{self.base_url}/api/quantum/randomness/float")
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields
        assert "random_float" in data
        assert "performance_ms" in data
        
        # Verify data validity
        assert isinstance(data["random_float"], float)
        assert 0.0 <= data["random_float"] <= 1.0
        assert isinstance(data["performance_ms"], (int, float))
        assert data["performance_ms"] > 0
        
        print(f"✅ Random float generated successfully")
        print(f"   Random float: {data['random_float']}")
        print(f"   Performance: {data['performance_ms']:.2f}ms")
        
        return data
        
    def test_optimized_randomness_batch_generation(self):
        """Test batch random generation for improved performance"""
        print("\n=== Testing Optimized Randomness - Batch Generation ===")
        
        # Create batch request with multiple random generation requests
        batch_requests = [
            {"type": "bytes", "length": 32},
            {"type": "int", "min_value": 1, "max_value": 100},
            {"type": "float"},
            {"type": "bytes", "length": 16},
            {"type": "int", "min_value": 500, "max_value": 1000}
        ]
        
        batch_payload = {
            "requests": batch_requests
        }
        
        response = requests.post(f"{self.base_url}/api/quantum/randomness/batch", json=batch_payload)
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields
        assert "results" in data
        assert "total_performance_ms" in data
        assert "average_performance_ms" in data
        
        # Verify data validity
        assert len(data["results"]) == len(batch_requests)
        assert isinstance(data["total_performance_ms"], (int, float))
        assert isinstance(data["average_performance_ms"], (int, float))
        assert data["total_performance_ms"] > 0
        assert data["average_performance_ms"] > 0
        
        print(f"✅ Batch random generation completed successfully")
        print(f"   Requests processed: {len(data['results'])}")
        print(f"   Total performance: {data['total_performance_ms']:.2f}ms")
        print(f"   Average performance: {data['average_performance_ms']:.2f}ms")
        
        return data

class TestPerformanceMonitoringEndpoints:
    """Test Performance Monitoring Endpoints"""
    
    def setup_method(self):
        """Setup before each test"""
        self.base_url = BACKEND_URL
        
    def test_crypto_performance_stats(self):
        """Test crypto performance statistics endpoint"""
        print("\n=== Testing Performance Monitoring - Crypto Stats ===")
        
        response = requests.get(f"{self.base_url}/api/quantum/performance/crypto-stats")
        assert response.status_code == 200
        data = response.json()
        
        # Verify response is valid JSON and contains performance data
        assert isinstance(data, dict)
        
        print(f"✅ Crypto performance stats retrieved successfully")
        print(f"   Stats keys: {list(data.keys())}")
        
        return data
        
    def test_crypto_benchmark(self):
        """Test crypto performance benchmark endpoint"""
        print("\n=== Testing Performance Monitoring - Crypto Benchmark ===")
        
        response = requests.get(f"{self.base_url}/api/quantum/performance/benchmark-crypto")
        assert response.status_code == 200
        data = response.json()
        
        # Verify response contains benchmark results
        assert isinstance(data, dict)
        
        print(f"✅ Crypto benchmark completed successfully")
        print(f"   Benchmark keys: {list(data.keys())}")
        
        return data
        
    def test_randomness_benchmark(self):
        """Test randomness performance benchmark endpoint"""
        print("\n=== Testing Performance Monitoring - Randomness Benchmark ===")
        
        response = requests.get(f"{self.base_url}/api/quantum/performance/benchmark-randomness")
        assert response.status_code == 200
        data = response.json()
        
        # Verify response contains benchmark results
        assert isinstance(data, dict)
        
        print(f"✅ Randomness benchmark completed successfully")
        print(f"   Benchmark keys: {list(data.keys())}")
        
        return data

class TestPerformanceOptimizedSecurity:
    """Test that security is maintained with performance optimizations"""
    
    def setup_method(self):
        """Setup before each test"""
        self.base_url = BACKEND_URL
        
    def test_optimized_crypto_security_maintained(self):
        """Test that cryptographic security is maintained with optimizations"""
        print("\n=== Testing Security Maintenance - Optimized Crypto ===")
        
        # Generate keypair and sign message
        keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        assert keypair_response.status_code == 200
        keypair = keypair_response.json()
        
        test_message = "Security test message"
        sign_payload = {
            "message": test_message,
            "private_key": keypair["private_key"]
        }
        
        sign_response = requests.post(f"{self.base_url}/api/quantum/crypto/sign", json=sign_payload)
        assert sign_response.status_code == 200
        signature_data = sign_response.json()
        
        # Test 1: Valid signature should verify as true
        verify_payload = {
            "message": test_message,
            "signature": signature_data["signature"],
            "public_key": keypair["public_key"]
        }
        
        verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        
        assert verify_data["is_valid"] is True
        print(f"✅ Valid signature correctly verified as: {verify_data['is_valid']}")
        
        # Test 2: Invalid signature should verify as false
        # Modify the signature slightly
        modified_signature = signature_data["signature"][:-1] + ('A' if signature_data["signature"][-1] != 'A' else 'B')
        
        invalid_verify_payload = {
            "message": test_message,
            "signature": modified_signature,
            "public_key": keypair["public_key"]
        }
        
        invalid_verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=invalid_verify_payload)
        assert invalid_verify_response.status_code == 200
        invalid_verify_data = invalid_verify_response.json()
        
        assert invalid_verify_data["is_valid"] is False
        print(f"✅ Invalid signature correctly verified as: {invalid_verify_data['is_valid']}")
        
        print("✅ Cryptographic security maintained with optimizations")

class TestComprehensivePerformanceOptimization:
    """Comprehensive test of all performance-optimized features"""
    
    def setup_method(self):
        """Setup before each test"""
        self.base_url = BACKEND_URL
        
    def test_comprehensive_performance_optimization_validation(self):
        """
        Comprehensive test validating all Phase 1 - Performance Optimization features:
        1. All optimized endpoints work correctly
        2. Performance timing is included in responses
        3. Batch operations work correctly
        4. Performance monitoring endpoints function
        5. Security is maintained
        """
        print("\n" + "="*80)
        print("COMPREHENSIVE PERFORMANCE OPTIMIZATION VALIDATION")
        print("="*80)
        
        results = {
            "crypto_operations": {},
            "randomness_operations": {},
            "performance_monitoring": {},
            "security_validation": {},
            "batch_operations": {}
        }
        
        # 1. Test Optimized Crypto Operations
        print("\n1. TESTING OPTIMIZED CRYPTO OPERATIONS")
        print("-" * 50)
        
        # Keypair generation
        keypair_response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
        assert keypair_response.status_code == 200
        keypair_data = keypair_response.json()
        assert "performance_ms" in keypair_data
        results["crypto_operations"]["keypair_generation"] = {
            "success": True,
            "performance_ms": keypair_data["performance_ms"]
        }
        print(f"   ✅ Keypair generation: {keypair_data['performance_ms']:.2f}ms")
        
        # Message signing
        sign_payload = {
            "message": "Comprehensive test message",
            "private_key": keypair_data["private_key"]
        }
        sign_response = requests.post(f"{self.base_url}/api/quantum/crypto/sign", json=sign_payload)
        assert sign_response.status_code == 200
        sign_data = sign_response.json()
        assert "performance_ms" in sign_data
        results["crypto_operations"]["message_signing"] = {
            "success": True,
            "performance_ms": sign_data["performance_ms"]
        }
        print(f"   ✅ Message signing: {sign_data['performance_ms']:.2f}ms")
        
        # Signature verification
        verify_payload = {
            "message": "Comprehensive test message",
            "signature": sign_data["signature"],
            "public_key": keypair_data["public_key"]
        }
        verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        assert "performance_ms" in verify_data
        assert verify_data["is_valid"] is True
        results["crypto_operations"]["signature_verification"] = {
            "success": True,
            "performance_ms": verify_data["performance_ms"],
            "is_valid": verify_data["is_valid"]
        }
        print(f"   ✅ Signature verification: {verify_data['performance_ms']:.2f}ms")
        
        # 2. Test Optimized Randomness Operations
        print("\n2. TESTING OPTIMIZED RANDOMNESS OPERATIONS")
        print("-" * 50)
        
        # Random bytes
        bytes_response = requests.get(f"{self.base_url}/api/quantum/randomness/bytes?length=64")
        assert bytes_response.status_code == 200
        bytes_data = bytes_response.json()
        assert "performance_ms" in bytes_data
        results["randomness_operations"]["random_bytes"] = {
            "success": True,
            "performance_ms": bytes_data["performance_ms"]
        }
        print(f"   ✅ Random bytes generation: {bytes_data['performance_ms']:.2f}ms")
        
        # Random integer
        int_response = requests.get(f"{self.base_url}/api/quantum/randomness/int?min_value=1&max_value=1000")
        assert int_response.status_code == 200
        int_data = int_response.json()
        assert "performance_ms" in int_data
        results["randomness_operations"]["random_int"] = {
            "success": True,
            "performance_ms": int_data["performance_ms"]
        }
        print(f"   ✅ Random integer generation: {int_data['performance_ms']:.2f}ms")
        
        # Random float
        float_response = requests.get(f"{self.base_url}/api/quantum/randomness/float")
        assert float_response.status_code == 200
        float_data = float_response.json()
        assert "performance_ms" in float_data
        results["randomness_operations"]["random_float"] = {
            "success": True,
            "performance_ms": float_data["performance_ms"]
        }
        print(f"   ✅ Random float generation: {float_data['performance_ms']:.2f}ms")
        
        # 3. Test Batch Operations
        print("\n3. TESTING BATCH OPERATIONS")
        print("-" * 50)
        
        # Batch verification
        verification_requests = []
        for i in range(3):
            kp_resp = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair")
            kp_data = kp_resp.json()
            
            msg = f"Batch test message {i+1}"
            sign_resp = requests.post(f"{self.base_url}/api/quantum/crypto/sign", json={
                "message": msg,
                "private_key": kp_data["private_key"]
            })
            sign_data = sign_resp.json()
            
            verification_requests.append({
                "message": msg,
                "signature": sign_data["signature"],
                "public_key": kp_data["public_key"]
            })
        
        batch_verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/batch-verify", json={
            "verifications": verification_requests
        })
        assert batch_verify_response.status_code == 200
        batch_verify_data = batch_verify_response.json()
        assert "total_performance_ms" in batch_verify_data
        assert "average_performance_ms" in batch_verify_data
        assert all(batch_verify_data["results"])
        results["batch_operations"]["batch_verify"] = {
            "success": True,
            "total_performance_ms": batch_verify_data["total_performance_ms"],
            "average_performance_ms": batch_verify_data["average_performance_ms"],
            "verifications_count": len(batch_verify_data["results"])
        }
        print(f"   ✅ Batch verification: {batch_verify_data['total_performance_ms']:.2f}ms total, {batch_verify_data['average_performance_ms']:.2f}ms average")
        
        # Batch randomness
        batch_random_response = requests.post(f"{self.base_url}/api/quantum/randomness/batch", json={
            "requests": [
                {"type": "bytes", "length": 32},
                {"type": "int", "min_value": 1, "max_value": 100},
                {"type": "float"}
            ]
        })
        assert batch_random_response.status_code == 200
        batch_random_data = batch_random_response.json()
        assert "total_performance_ms" in batch_random_data
        assert "average_performance_ms" in batch_random_data
        results["batch_operations"]["batch_random"] = {
            "success": True,
            "total_performance_ms": batch_random_data["total_performance_ms"],
            "average_performance_ms": batch_random_data["average_performance_ms"],
            "requests_count": len(batch_random_data["results"])
        }
        print(f"   ✅ Batch randomness: {batch_random_data['total_performance_ms']:.2f}ms total, {batch_random_data['average_performance_ms']:.2f}ms average")
        
        # 4. Test Performance Monitoring
        print("\n4. TESTING PERFORMANCE MONITORING")
        print("-" * 50)
        
        # Crypto stats
        crypto_stats_response = requests.get(f"{self.base_url}/api/quantum/performance/crypto-stats")
        assert crypto_stats_response.status_code == 200
        results["performance_monitoring"]["crypto_stats"] = {"success": True}
        print(f"   ✅ Crypto performance stats")
        
        # Crypto benchmark
        crypto_benchmark_response = requests.get(f"{self.base_url}/api/quantum/performance/benchmark-crypto")
        assert crypto_benchmark_response.status_code == 200
        results["performance_monitoring"]["crypto_benchmark"] = {"success": True}
        print(f"   ✅ Crypto benchmark")
        
        # Randomness benchmark
        randomness_benchmark_response = requests.get(f"{self.base_url}/api/quantum/performance/benchmark-randomness")
        assert randomness_benchmark_response.status_code == 200
        results["performance_monitoring"]["randomness_benchmark"] = {"success": True}
        print(f"   ✅ Randomness benchmark")
        
        # 5. Test Security Maintenance
        print("\n5. TESTING SECURITY MAINTENANCE")
        print("-" * 50)
        
        # Valid signature test
        valid_verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=verify_payload)
        valid_verify_data = valid_verify_response.json()
        assert valid_verify_data["is_valid"] is True
        
        # Invalid signature test
        modified_signature = sign_data["signature"][:-1] + ('X' if sign_data["signature"][-1] != 'X' else 'Y')
        invalid_verify_payload = {
            "message": "Comprehensive test message",
            "signature": modified_signature,
            "public_key": keypair_data["public_key"]
        }
        invalid_verify_response = requests.post(f"{self.base_url}/api/quantum/crypto/verify", json=invalid_verify_payload)
        invalid_verify_data = invalid_verify_response.json()
        assert invalid_verify_data["is_valid"] is False
        
        results["security_validation"] = {
            "valid_signature_accepted": valid_verify_data["is_valid"],
            "invalid_signature_rejected": not invalid_verify_data["is_valid"]
        }
        print(f"   ✅ Valid signatures accepted: {valid_verify_data['is_valid']}")
        print(f"   ✅ Invalid signatures rejected: {not invalid_verify_data['is_valid']}")
        
        # Final Summary
        print("\n" + "="*80)
        print("PHASE 1 - PERFORMANCE OPTIMIZATION VALIDATION COMPLETE")
        print("="*80)
        print("✅ ALL PERFORMANCE-OPTIMIZED QUANTUM BLOCKCHAIN FEATURES WORKING CORRECTLY")
        print("\nKey Achievements:")
        print("• All optimized endpoints return valid results")
        print("• Performance timing included in all responses (performance_ms field)")
        print("• Batch operations working correctly and efficiently")
        print("• Performance monitoring endpoints functioning")
        print("• Cryptographic security maintained with optimizations")
        print("\nPhase 1 - Performance Optimization: ✅ SUCCESSFULLY IMPLEMENTED")
        
        return results

if __name__ == "__main__":
    pytest.main([__file__, "-v"])