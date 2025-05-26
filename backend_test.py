#!/usr/bin/env python3
"""
Backend Test Suite for Quantum Routes Performance Optimization Testing
Testing quantum routes at current paths to validate performance optimizations.
"""

import requests
import json
import time
import base64
import os
from typing import Dict, Any, List

# Get backend URL from environment
BACKEND_URL = "https://54afd158-c35e-4697-9ab5-92696b33d177.preview.emergentagent.com"

class QuantumRoutesPerformanceTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.test_results = []
        self.performance_metrics = {}
        
    def log_result(self, test_name: str, success: bool, details: str, performance_ms: float = None):
        """Log test result"""
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
        print(f"{status}: {test_name}{perf_info}")
        if not success:
            print(f"   Details: {details}")
    
    def test_quantum_crypto_at_current_paths(self):
        """Test quantum crypto endpoints at /quantum/crypto/... paths"""
        print("\n=== TESTING QUANTUM CRYPTO AT CURRENT PATHS ===")
        
        # Test 1: Generate Keypair
        try:
            start_time = time.time()
            response = requests.post(f"{self.base_url}/quantum/crypto/generate-keypair", 
                                   json={}, timeout=30)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                if "public_key" in data and "private_key" in data and "performance_ms" in data:
                    self.log_result(
                        "Quantum Keypair Generation", 
                        True, 
                        f"Generated keypair with optimized performance. API performance: {data.get('performance_ms', 'N/A')}ms",
                        data.get('performance_ms', request_time)
                    )
                    # Store keys for next tests
                    self.test_public_key = data["public_key"]
                    self.test_private_key = data["private_key"]
                    return True
                else:
                    self.log_result("Quantum Keypair Generation", False, f"Missing required fields in response: {data}")
            else:
                self.log_result("Quantum Keypair Generation", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("Quantum Keypair Generation", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_quantum_signing_at_current_paths(self):
        """Test quantum signing at /quantum/crypto/sign"""
        print("\n=== TESTING QUANTUM SIGNING AT CURRENT PATHS ===")
        
        if not hasattr(self, 'test_private_key'):
            self.log_result("Quantum Message Signing", False, "No private key available from keypair generation")
            return False
        
        try:
            test_message = "Performance optimized quantum signature test message"
            start_time = time.time()
            response = requests.post(f"{self.base_url}/quantum/crypto/sign", 
                                   json={
                                       "message": test_message,
                                       "private_key": self.test_private_key
                                   }, timeout=30)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                if "signature" in data and "performance_ms" in data:
                    self.log_result(
                        "Quantum Message Signing", 
                        True, 
                        f"Signed message with optimized performance. API performance: {data.get('performance_ms', 'N/A')}ms",
                        data.get('performance_ms', request_time)
                    )
                    # Store signature for verification test
                    self.test_signature = data["signature"]
                    self.test_message = test_message
                    return True
                else:
                    self.log_result("Quantum Message Signing", False, f"Missing required fields in response: {data}")
            else:
                self.log_result("Quantum Message Signing", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("Quantum Message Signing", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_quantum_verification_at_current_paths(self):
        """Test quantum signature verification at /quantum/crypto/verify"""
        print("\n=== TESTING QUANTUM VERIFICATION AT CURRENT PATHS ===")
        
        if not hasattr(self, 'test_signature') or not hasattr(self, 'test_public_key'):
            self.log_result("Quantum Signature Verification", False, "No signature or public key available from previous tests")
            return False
        
        try:
            start_time = time.time()
            response = requests.post(f"{self.base_url}/quantum/crypto/verify", 
                                   json={
                                       "message": self.test_message,
                                       "signature": self.test_signature,
                                       "public_key": self.test_public_key
                                   }, timeout=30)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                if "is_valid" in data and "performance_ms" in data:
                    if data["is_valid"]:
                        self.log_result(
                            "Quantum Signature Verification", 
                            True, 
                            f"Verified signature with optimized performance. API performance: {data.get('performance_ms', 'N/A')}ms",
                            data.get('performance_ms', request_time)
                        )
                        return True
                    else:
                        self.log_result("Quantum Signature Verification", False, "Valid signature was incorrectly rejected")
                else:
                    self.log_result("Quantum Signature Verification", False, f"Missing required fields in response: {data}")
            else:
                self.log_result("Quantum Signature Verification", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("Quantum Signature Verification", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_quantum_randomness_at_current_paths(self):
        """Test quantum randomness endpoints at /quantum/randomness/... paths"""
        print("\n=== TESTING QUANTUM RANDOMNESS AT CURRENT PATHS ===")
        
        # Test 1: Random Bytes
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/quantum/randomness/bytes?length=64", timeout=30)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                if "random_bytes" in data and "performance_ms" in data:
                    # Verify it's valid base64
                    try:
                        decoded = base64.b64decode(data["random_bytes"])
                        if len(decoded) == 64:
                            self.log_result(
                                "Quantum Random Bytes", 
                                True, 
                                f"Generated 64 random bytes with optimized performance. API performance: {data.get('performance_ms', 'N/A')}ms",
                                data.get('performance_ms', request_time)
                            )
                        else:
                            self.log_result("Quantum Random Bytes", False, f"Wrong byte length: {len(decoded)} != 64")
                    except Exception as e:
                        self.log_result("Quantum Random Bytes", False, f"Invalid base64 encoding: {str(e)}")
                else:
                    self.log_result("Quantum Random Bytes", False, f"Missing required fields in response: {data}")
            else:
                self.log_result("Quantum Random Bytes", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("Quantum Random Bytes", False, f"Request failed: {str(e)}")
        
        # Test 2: Random Integer
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/quantum/randomness/int?min_value=1&max_value=1000", timeout=30)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                if "random_int" in data and "performance_ms" in data:
                    random_int = data["random_int"]
                    if 1 <= random_int <= 1000:
                        self.log_result(
                            "Quantum Random Integer", 
                            True, 
                            f"Generated random int {random_int} with optimized performance. API performance: {data.get('performance_ms', 'N/A')}ms",
                            data.get('performance_ms', request_time)
                        )
                    else:
                        self.log_result("Quantum Random Integer", False, f"Random int {random_int} out of range [1, 1000]")
                else:
                    self.log_result("Quantum Random Integer", False, f"Missing required fields in response: {data}")
            else:
                self.log_result("Quantum Random Integer", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("Quantum Random Integer", False, f"Request failed: {str(e)}")
        
        # Test 3: Random Float
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/quantum/randomness/float", timeout=30)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                if "random_float" in data and "performance_ms" in data:
                    random_float = data["random_float"]
                    if 0.0 <= random_float <= 1.0:
                        self.log_result(
                            "Quantum Random Float", 
                            True, 
                            f"Generated random float {random_float:.6f} with optimized performance. API performance: {data.get('performance_ms', 'N/A')}ms",
                            data.get('performance_ms', request_time)
                        )
                    else:
                        self.log_result("Quantum Random Float", False, f"Random float {random_float} out of range [0.0, 1.0]")
                else:
                    self.log_result("Quantum Random Float", False, f"Missing required fields in response: {data}")
            else:
                self.log_result("Quantum Random Float", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("Quantum Random Float", False, f"Request failed: {str(e)}")
    
    def test_performance_monitoring_at_current_paths(self):
        """Test performance monitoring endpoints at /quantum/performance/... paths"""
        print("\n=== TESTING PERFORMANCE MONITORING AT CURRENT PATHS ===")
        
        # Test 1: Crypto Performance Stats
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/quantum/performance/crypto-stats", timeout=30)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Crypto Performance Stats", 
                    True, 
                    f"Retrieved crypto performance statistics: {json.dumps(data, indent=2)[:200]}...",
                    request_time
                )
            else:
                self.log_result("Crypto Performance Stats", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("Crypto Performance Stats", False, f"Request failed: {str(e)}")
        
        # Test 2: Crypto Benchmark
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/quantum/performance/benchmark-crypto", timeout=60)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Crypto Performance Benchmark", 
                    True, 
                    f"Completed crypto benchmark: {json.dumps(data, indent=2)[:200]}...",
                    request_time
                )
            else:
                self.log_result("Crypto Performance Benchmark", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("Crypto Performance Benchmark", False, f"Request failed: {str(e)}")
        
        # Test 3: Randomness Benchmark
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/quantum/performance/benchmark-randomness", timeout=60)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Randomness Performance Benchmark", 
                    True, 
                    f"Completed randomness benchmark: {json.dumps(data, indent=2)[:200]}...",
                    request_time
                )
            else:
                self.log_result("Randomness Performance Benchmark", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("Randomness Performance Benchmark", False, f"Request failed: {str(e)}")
    
    def test_api_quantum_paths(self):
        """Test if quantum routes are also accessible at /api/quantum/... paths"""
        print("\n=== TESTING API QUANTUM PATHS ===")
        
        # Test if routes are accessible at /api/quantum/... paths
        try:
            response = requests.post(f"{self.base_url}/api/quantum/crypto/generate-keypair", 
                                   json={}, timeout=30)
            
            if response.status_code == 200:
                self.log_result(
                    "API Quantum Path Accessibility", 
                    True, 
                    "Quantum routes are accessible at /api/quantum/... paths"
                )
            elif response.status_code == 404:
                self.log_result(
                    "API Quantum Path Accessibility", 
                    False, 
                    "Quantum routes are NOT accessible at /api/quantum/... paths (404 Not Found)"
                )
            else:
                self.log_result(
                    "API Quantum Path Accessibility", 
                    False, 
                    f"Unexpected response at /api/quantum/... path: HTTP {response.status_code}"
                )
        except Exception as e:
            self.log_result("API Quantum Path Accessibility", False, f"Request failed: {str(e)}")
    
    def run_all_tests(self):
        """Run all quantum performance tests"""
        print(f"🧪 QUANTUM ROUTES PERFORMANCE TESTING")
        print(f"Backend URL: {self.base_url}")
        print(f"Testing quantum routes at current paths to validate performance optimizations")
        print("=" * 80)
        
        # Test current quantum paths
        crypto_success = self.test_quantum_crypto_at_current_paths()
        if crypto_success:
            self.test_quantum_signing_at_current_paths()
            self.test_quantum_verification_at_current_paths()
        
        self.test_quantum_randomness_at_current_paths()
        self.test_performance_monitoring_at_current_paths()
        
        # Test API paths
        self.test_api_quantum_paths()
        
        # Summary
        print("\n" + "=" * 80)
        print("🏁 QUANTUM PERFORMANCE TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Performance Analysis
        performance_tests = [r for r in self.test_results if r["performance_ms"] is not None and r["success"]]
        if performance_tests:
            print(f"\n📊 PERFORMANCE METRICS:")
            for test in performance_tests:
                print(f"  {test['test']}: {test['performance_ms']:.2f}ms")
            
            avg_performance = sum(t["performance_ms"] for t in performance_tests) / len(performance_tests)
            print(f"\n⚡ Average Performance: {avg_performance:.2f}ms")
        
        # Critical Issues
        critical_failures = [r for r in self.test_results if not r["success"]]
        if critical_failures:
            print(f"\n🚨 CRITICAL ISSUES:")
            for failure in critical_failures:
                print(f"  ❌ {failure['test']}: {failure['details']}")
        
        return passed_tests, failed_tests, self.test_results

def main():
    """Main test execution"""
    tester = QuantumRoutesPerformanceTester()
    passed, failed, results = tester.run_all_tests()
    
    # Exit with appropriate code
    if failed > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()