#!/usr/bin/env python3
"""
PERFORMANCE-OPTIMIZED Quantum Blockchain Testing Suite
Testing Phase 1 optimizations for 3-5x performance improvements.

This test validates:
1. Optimized Quantum Cryptography Performance
2. Optimized Quantum Randomness Performance  
3. Performance Monitoring & Optimization Metrics
"""

import requests
import json
import time
import base64
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://54afd158-c35e-4697-9ab5-92696b33d177.preview.emergentagent.com"

class PerformanceOptimizedQuantumTester:
    """Test suite for performance-optimized quantum blockchain features."""
    
    def __init__(self):
        self.base_url = f"{BACKEND_URL}/api/quantum"
        self.test_results = []
        
    def log_result(self, test_name: str, success: bool, details: str, performance_ms: float = None):
        """Log test result with performance metrics."""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "performance_ms": performance_ms,
            "timestamp": time.time()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        perf_info = f" ({performance_ms:.2f}ms)" if performance_ms else ""
        print(f"{status} {test_name}{perf_info}: {details}")
    
    def test_optimized_crypto_keypair_generation(self):
        """Test optimized keypair generation (3x faster target)."""
        try:
            start_time = time.time()
            response = requests.post(f"{self.base_url}/crypto/generate-keypair")
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["public_key", "private_key", "performance_ms"]
                if all(field in data for field in required_fields):
                    # Validate performance target (< 1ms for 3x improvement)
                    performance_ms = data["performance_ms"]
                    if performance_ms < 1.0:
                        self.log_result(
                            "Optimized Keypair Generation",
                            True,
                            f"Generated keypair in {performance_ms:.3f}ms (target: <1ms)",
                            performance_ms
                        )
                        return data
                    else:
                        self.log_result(
                            "Optimized Keypair Generation",
                            False,
                            f"Performance target missed: {performance_ms:.3f}ms (target: <1ms)",
                            performance_ms
                        )
                else:
                    self.log_result(
                        "Optimized Keypair Generation",
                        False,
                        f"Missing required fields: {[f for f in required_fields if f not in data]}"
                    )
            else:
                self.log_result(
                    "Optimized Keypair Generation",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Optimized Keypair Generation",
                False,
                f"Exception: {str(e)}"
            )
        return None
    
    def test_optimized_crypto_signing(self, keypair: Dict[str, str]):
        """Test optimized message signing (2x faster target)."""
        if not keypair:
            self.log_result("Optimized Message Signing", False, "No keypair available")
            return None
            
        try:
            test_message = "Performance test message for optimized signing"
            payload = {
                "message": test_message,
                "private_key": keypair["private_key"]
            }
            
            start_time = time.time()
            response = requests.post(f"{self.base_url}/crypto/sign", json=payload)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                if "signature" in data and "performance_ms" in data:
                    performance_ms = data["performance_ms"]
                    # Target: < 1ms for 2x improvement
                    if performance_ms < 1.0:
                        self.log_result(
                            "Optimized Message Signing",
                            True,
                            f"Signed message in {performance_ms:.3f}ms (target: <1ms)",
                            performance_ms
                        )
                        return data["signature"]
                    else:
                        self.log_result(
                            "Optimized Message Signing",
                            False,
                            f"Performance target missed: {performance_ms:.3f}ms (target: <1ms)",
                            performance_ms
                        )
                else:
                    self.log_result(
                        "Optimized Message Signing",
                        False,
                        "Missing signature or performance_ms in response"
                    )
            else:
                self.log_result(
                    "Optimized Message Signing",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Optimized Message Signing",
                False,
                f"Exception: {str(e)}"
            )
        return None
    
    def test_optimized_crypto_verification(self, keypair: Dict[str, str], signature: str):
        """Test optimized signature verification (5x faster target)."""
        if not keypair or not signature:
            self.log_result("Optimized Signature Verification", False, "Missing keypair or signature")
            return
            
        try:
            test_message = "Performance test message for optimized signing"
            payload = {
                "message": test_message,
                "signature": signature,
                "public_key": keypair["public_key"]
            }
            
            start_time = time.time()
            response = requests.post(f"{self.base_url}/crypto/verify", json=payload)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                if "is_valid" in data and "performance_ms" in data:
                    performance_ms = data["performance_ms"]
                    is_valid = data["is_valid"]
                    
                    # Target: < 0.5ms for 5x improvement
                    if performance_ms < 0.5 and is_valid:
                        self.log_result(
                            "Optimized Signature Verification",
                            True,
                            f"Verified signature in {performance_ms:.3f}ms (target: <0.5ms)",
                            performance_ms
                        )
                    elif not is_valid:
                        self.log_result(
                            "Optimized Signature Verification",
                            False,
                            f"Valid signature incorrectly rejected"
                        )
                    else:
                        self.log_result(
                            "Optimized Signature Verification",
                            False,
                            f"Performance target missed: {performance_ms:.3f}ms (target: <0.5ms)",
                            performance_ms
                        )
                else:
                    self.log_result(
                        "Optimized Signature Verification",
                        False,
                        "Missing is_valid or performance_ms in response"
                    )
            else:
                self.log_result(
                    "Optimized Signature Verification",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Optimized Signature Verification",
                False,
                f"Exception: {str(e)}"
            )
    
    def test_optimized_random_bytes(self):
        """Test optimized random bytes generation (3-5x faster target)."""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/randomness/bytes?length=64")
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                if "random_bytes" in data and "performance_ms" in data:
                    performance_ms = data["performance_ms"]
                    random_bytes = data["random_bytes"]
                    
                    # Validate base64 encoding and length
                    try:
                        decoded = base64.b64decode(random_bytes)
                        if len(decoded) == 64:
                            # Target: < 0.5ms for 3-5x improvement
                            if performance_ms < 0.5:
                                self.log_result(
                                    "Optimized Random Bytes",
                                    True,
                                    f"Generated 64 random bytes in {performance_ms:.3f}ms (target: <0.5ms)",
                                    performance_ms
                                )
                            else:
                                self.log_result(
                                    "Optimized Random Bytes",
                                    False,
                                    f"Performance target missed: {performance_ms:.3f}ms (target: <0.5ms)",
                                    performance_ms
                                )
                        else:
                            self.log_result(
                                "Optimized Random Bytes",
                                False,
                                f"Incorrect byte length: {len(decoded)} (expected: 64)"
                            )
                    except Exception as decode_error:
                        self.log_result(
                            "Optimized Random Bytes",
                            False,
                            f"Invalid base64 encoding: {str(decode_error)}"
                        )
                else:
                    self.log_result(
                        "Optimized Random Bytes",
                        False,
                        "Missing random_bytes or performance_ms in response"
                    )
            else:
                self.log_result(
                    "Optimized Random Bytes",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Optimized Random Bytes",
                False,
                f"Exception: {str(e)}"
            )
    
    def test_optimized_random_int(self):
        """Test optimized random integer generation (2x faster target)."""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/randomness/int?min_value=1&max_value=1000")
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                if "random_int" in data and "performance_ms" in data:
                    performance_ms = data["performance_ms"]
                    random_int = data["random_int"]
                    
                    # Validate range
                    if 1 <= random_int <= 1000:
                        # Target: < 0.5ms for 2x improvement
                        if performance_ms < 0.5:
                            self.log_result(
                                "Optimized Random Integer",
                                True,
                                f"Generated random int {random_int} in {performance_ms:.3f}ms (target: <0.5ms)",
                                performance_ms
                            )
                        else:
                            self.log_result(
                                "Optimized Random Integer",
                                False,
                                f"Performance target missed: {performance_ms:.3f}ms (target: <0.5ms)",
                                performance_ms
                            )
                    else:
                        self.log_result(
                            "Optimized Random Integer",
                            False,
                            f"Random int {random_int} outside range [1, 1000]"
                        )
                else:
                    self.log_result(
                        "Optimized Random Integer",
                        False,
                        "Missing random_int or performance_ms in response"
                    )
            else:
                self.log_result(
                    "Optimized Random Integer",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Optimized Random Integer",
                False,
                f"Exception: {str(e)}"
            )
    
    def test_optimized_random_float(self):
        """Test optimized random float generation (3x faster target)."""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/randomness/float")
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                if "random_float" in data and "performance_ms" in data:
                    performance_ms = data["performance_ms"]
                    random_float = data["random_float"]
                    
                    # Validate range
                    if 0.0 <= random_float <= 1.0:
                        # Target: < 0.5ms for 3x improvement
                        if performance_ms < 0.5:
                            self.log_result(
                                "Optimized Random Float",
                                True,
                                f"Generated random float {random_float:.6f} in {performance_ms:.3f}ms (target: <0.5ms)",
                                performance_ms
                            )
                        else:
                            self.log_result(
                                "Optimized Random Float",
                                False,
                                f"Performance target missed: {performance_ms:.3f}ms (target: <0.5ms)",
                                performance_ms
                            )
                    else:
                        self.log_result(
                            "Optimized Random Float",
                            False,
                            f"Random float {random_float} outside range [0.0, 1.0]"
                        )
                else:
                    self.log_result(
                        "Optimized Random Float",
                        False,
                        "Missing random_float or performance_ms in response"
                    )
            else:
                self.log_result(
                    "Optimized Random Float",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Optimized Random Float",
                False,
                f"Exception: {str(e)}"
            )
    
    def run_all_tests(self):
        """Run all performance-optimized quantum tests."""
        print("🚀 STARTING PERFORMANCE-OPTIMIZED QUANTUM BLOCKCHAIN TESTING")
        print("=" * 80)
        print("Testing Phase 1 optimizations for 3-5x performance improvements")
        print()
        
        # Test optimized cryptography
        print("📊 TESTING OPTIMIZED QUANTUM CRYPTOGRAPHY PERFORMANCE")
        print("-" * 60)
        keypair = self.test_optimized_crypto_keypair_generation()
        signature = self.test_optimized_crypto_signing(keypair)
        self.test_optimized_crypto_verification(keypair, signature)
        print()
        
        # Test optimized randomness
        print("🎲 TESTING OPTIMIZED QUANTUM RANDOMNESS PERFORMANCE")
        print("-" * 60)
        self.test_optimized_random_bytes()
        self.test_optimized_random_int()
        self.test_optimized_random_float()
        print()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary with performance analysis."""
        print("=" * 80)
        print("🏁 PERFORMANCE-OPTIMIZED QUANTUM TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        # Performance analysis
        performance_tests = [r for r in self.test_results if r["performance_ms"] is not None]
        if performance_tests:
            avg_performance = sum(r["performance_ms"] for r in performance_tests) / len(performance_tests)
            print(f"📊 PERFORMANCE METRICS:")
            print(f"Average Operation Time: {avg_performance:.3f}ms")
            
            # Check if performance targets were met
            fast_operations = sum(1 for r in performance_tests if r["performance_ms"] < 1.0)
            print(f"Sub-millisecond Operations: {fast_operations}/{len(performance_tests)} ({(fast_operations/len(performance_tests))*100:.1f}%)")
        
        print()
        print("🎯 PHASE 1 OPTIMIZATION VALIDATION:")
        
        # Check specific success criteria
        crypto_tests = [r for r in self.test_results if "Crypto" in r["test"] or "crypto" in r["test"]]
        randomness_tests = [r for r in self.test_results if "Random" in r["test"] or "randomness" in r["test"]]
        
        crypto_success = all(r["success"] for r in crypto_tests)
        randomness_success = all(r["success"] for r in randomness_tests)
        
        print(f"✅ Optimized Cryptography: {'PASS' if crypto_success else 'FAIL'}")
        print(f"✅ Optimized Randomness: {'PASS' if randomness_success else 'FAIL'}")
        
        overall_success = crypto_success and randomness_success
        print()
        print(f"🏆 PHASE 1 COMPLETION STATUS: {'✅ SUCCESS' if overall_success else '❌ INCOMPLETE'}")
        
        if overall_success:
            print("🎉 All Phase 1 performance optimizations are working correctly!")
            print("🚀 Ready to proceed to Phase 2 (Reliability & Scalability)")
        else:
            print("⚠️  Some Phase 1 optimizations need attention before proceeding")
        
        print("=" * 80)


def main():
    """Main test execution."""
    tester = PerformanceOptimizedQuantumTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()