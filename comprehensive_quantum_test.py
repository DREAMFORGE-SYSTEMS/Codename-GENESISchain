#!/usr/bin/env python3
"""
COMPREHENSIVE Performance-Optimized Quantum Testing Suite
Testing ALL Phase 1 optimization features including batch operations and monitoring.
"""

import requests
import json
import time
import base64
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://54afd158-c35e-4697-9ab5-92696b33d177.preview.emergentagent.com"

class ComprehensiveQuantumTester:
    """Complete test suite for all performance-optimized quantum features."""
    
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
    
    def test_batch_verification(self):
        """Test optimized batch verification (10x faster target)."""
        try:
            # Generate multiple keypairs and signatures for batch testing
            keypairs = []
            signatures = []
            test_message = "Batch verification test message"
            
            # Generate 5 keypairs and signatures
            for i in range(5):
                # Generate keypair
                response = requests.post(f"{self.base_url}/crypto/generate-keypair")
                if response.status_code == 200:
                    keypair = response.json()
                    keypairs.append(keypair)
                    
                    # Sign message
                    sign_payload = {
                        "message": test_message,
                        "private_key": keypair["private_key"]
                    }
                    sign_response = requests.post(f"{self.base_url}/crypto/sign", json=sign_payload)
                    if sign_response.status_code == 200:
                        signatures.append(sign_response.json()["signature"])
            
            if len(keypairs) == 5 and len(signatures) == 5:
                # Prepare batch verification request
                verifications = []
                for i in range(5):
                    verifications.append({
                        "message": test_message,
                        "signature": signatures[i],
                        "public_key": keypairs[i]["public_key"]
                    })
                
                batch_payload = {"verifications": verifications}
                
                start_time = time.time()
                response = requests.post(f"{self.base_url}/crypto/batch-verify", json=batch_payload)
                request_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if "results" in data and "total_performance_ms" in data:
                        total_performance_ms = data["total_performance_ms"]
                        results = data["results"]
                        average_performance_ms = data.get("average_performance_ms", 0)
                        
                        # Target: 10x faster than individual verifications
                        # Individual target was 0.5ms, so batch should be < 0.05ms per verification
                        if average_performance_ms < 0.05 and all(results):
                            self.log_result(
                                "Optimized Batch Verification",
                                True,
                                f"Batch verified 5 signatures in {total_performance_ms:.3f}ms (avg: {average_performance_ms:.3f}ms per signature, target: <0.05ms)",
                                total_performance_ms
                            )
                        elif not all(results):
                            self.log_result(
                                "Optimized Batch Verification",
                                False,
                                f"Some valid signatures incorrectly rejected: {results}"
                            )
                        else:
                            self.log_result(
                                "Optimized Batch Verification",
                                False,
                                f"Performance target missed: {average_performance_ms:.3f}ms per signature (target: <0.05ms)",
                                total_performance_ms
                            )
                    else:
                        self.log_result(
                            "Optimized Batch Verification",
                            False,
                            "Missing results or performance metrics in response"
                        )
                else:
                    self.log_result(
                        "Optimized Batch Verification",
                        False,
                        f"HTTP {response.status_code}: {response.text}"
                    )
            else:
                self.log_result(
                    "Optimized Batch Verification",
                    False,
                    f"Failed to generate test data: {len(keypairs)} keypairs, {len(signatures)} signatures"
                )
        except Exception as e:
            self.log_result(
                "Optimized Batch Verification",
                False,
                f"Exception: {str(e)}"
            )
    
    def test_batch_randomness(self):
        """Test optimized batch randomness generation (10x faster target)."""
        try:
            # Prepare batch request
            batch_requests = [
                {"type": "int", "min": 1, "max": 100},
                {"type": "bytes", "length": 16},
                {"type": "float"},
                {"type": "int", "min": 500, "max": 1000},
                {"type": "bytes", "length": 8}
            ]
            
            payload = {"requests": batch_requests}
            
            start_time = time.time()
            response = requests.post(f"{self.base_url}/randomness/batch", json=payload)
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                if "results" in data and "total_performance_ms" in data:
                    total_performance_ms = data["total_performance_ms"]
                    results = data["results"]
                    average_performance_ms = data.get("average_performance_ms", 0)
                    
                    # Validate results
                    if len(results) == 5:
                        # Target: 10x faster than individual operations
                        # Individual target was ~0.5ms, so batch should be < 0.05ms per operation
                        if average_performance_ms < 0.05:
                            self.log_result(
                                "Optimized Batch Randomness",
                                True,
                                f"Generated 5 random values in {total_performance_ms:.3f}ms (avg: {average_performance_ms:.3f}ms per operation, target: <0.05ms)",
                                total_performance_ms
                            )
                        else:
                            self.log_result(
                                "Optimized Batch Randomness",
                                False,
                                f"Performance target missed: {average_performance_ms:.3f}ms per operation (target: <0.05ms)",
                                total_performance_ms
                            )
                    else:
                        self.log_result(
                            "Optimized Batch Randomness",
                            False,
                            f"Incorrect number of results: {len(results)} (expected: 5)"
                        )
                else:
                    self.log_result(
                        "Optimized Batch Randomness",
                        False,
                        "Missing results or performance metrics in response"
                    )
            else:
                self.log_result(
                    "Optimized Batch Randomness",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Optimized Batch Randomness",
                False,
                f"Exception: {str(e)}"
            )
    
    def test_performance_crypto_stats(self):
        """Test crypto performance statistics endpoint."""
        try:
            response = requests.get(f"{self.base_url}/performance/crypto-stats")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for expected performance metrics
                expected_fields = ["total_operations", "cache_hit_rate_256", "cache_hit_rate_512", "estimated_speedup"]
                if all(field in data for field in expected_fields):
                    self.log_result(
                        "Performance Monitoring - Crypto Stats",
                        True,
                        f"Retrieved crypto stats: {data.get('total_operations', 0)} operations, cache hit rates: {data.get('cache_hit_rate_256', 0):.2%}/{data.get('cache_hit_rate_512', 0):.2%}"
                    )
                else:
                    missing_fields = [f for f in expected_fields if f not in data]
                    self.log_result(
                        "Performance Monitoring - Crypto Stats",
                        False,
                        f"Missing expected fields: {missing_fields}"
                    )
            else:
                self.log_result(
                    "Performance Monitoring - Crypto Stats",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Performance Monitoring - Crypto Stats",
                False,
                f"Exception: {str(e)}"
            )
    
    def test_performance_benchmark_crypto(self):
        """Test crypto performance benchmark endpoint."""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/performance/benchmark-crypto")
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for expected benchmark metrics
                expected_fields = ["keypairs_per_second", "signatures_per_second", "verifications_per_second", "all_verifications_passed"]
                if all(field in data for field in expected_fields):
                    keypairs_per_sec = data["keypairs_per_second"]
                    signatures_per_sec = data["signatures_per_second"]
                    verifications_per_sec = data["verifications_per_second"]
                    all_passed = data["all_verifications_passed"]
                    
                    if all_passed and keypairs_per_sec > 1000:  # Expect >1000 keypairs/sec for 3x improvement
                        self.log_result(
                            "Performance Benchmark - Crypto",
                            True,
                            f"Benchmark completed: {keypairs_per_sec:.0f} keypairs/sec, {signatures_per_sec:.0f} signatures/sec, {verifications_per_sec:.0f} verifications/sec",
                            request_time
                        )
                    else:
                        self.log_result(
                            "Performance Benchmark - Crypto",
                            False,
                            f"Performance below expectations: {keypairs_per_sec:.0f} keypairs/sec (target: >1000), all_passed: {all_passed}"
                        )
                else:
                    missing_fields = [f for f in expected_fields if f not in data]
                    self.log_result(
                        "Performance Benchmark - Crypto",
                        False,
                        f"Missing expected fields: {missing_fields}"
                    )
            else:
                self.log_result(
                    "Performance Benchmark - Crypto",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Performance Benchmark - Crypto",
                False,
                f"Exception: {str(e)}"
            )
    
    def test_performance_benchmark_randomness(self):
        """Test randomness performance benchmark endpoint."""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/performance/benchmark-randomness")
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for expected benchmark metrics
                expected_fields = ["optimized_bytes_per_second", "optimized_ints_per_second", "estimated_speedup"]
                if all(field in data for field in expected_fields):
                    bytes_per_sec = data["optimized_bytes_per_second"]
                    ints_per_sec = data["optimized_ints_per_second"]
                    
                    if bytes_per_sec > 2000:  # Expect >2000 bytes/sec for 3-5x improvement
                        self.log_result(
                            "Performance Benchmark - Randomness",
                            True,
                            f"Benchmark completed: {bytes_per_sec:.0f} bytes/sec, {ints_per_sec:.0f} ints/sec",
                            request_time
                        )
                    else:
                        self.log_result(
                            "Performance Benchmark - Randomness",
                            False,
                            f"Performance below expectations: {bytes_per_sec:.0f} bytes/sec (target: >2000)"
                        )
                else:
                    missing_fields = [f for f in expected_fields if f not in data]
                    self.log_result(
                        "Performance Benchmark - Randomness",
                        False,
                        f"Missing expected fields: {missing_fields}"
                    )
            else:
                self.log_result(
                    "Performance Benchmark - Randomness",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_result(
                "Performance Benchmark - Randomness",
                False,
                f"Exception: {str(e)}"
            )
    
    def run_comprehensive_tests(self):
        """Run comprehensive performance-optimized quantum tests."""
        print("🚀 COMPREHENSIVE PERFORMANCE-OPTIMIZED QUANTUM TESTING")
        print("=" * 80)
        print("Testing ALL Phase 1 optimization features including batch operations")
        print()
        
        # Test batch operations
        print("🔄 TESTING BATCH OPERATIONS (10x FASTER TARGET)")
        print("-" * 60)
        self.test_batch_verification()
        self.test_batch_randomness()
        print()
        
        # Test performance monitoring
        print("📈 TESTING PERFORMANCE MONITORING & BENCHMARKS")
        print("-" * 60)
        self.test_performance_crypto_stats()
        self.test_performance_benchmark_crypto()
        self.test_performance_benchmark_randomness()
        print()
        
        # Summary
        self.print_comprehensive_summary()
    
    def print_comprehensive_summary(self):
        """Print comprehensive test summary."""
        print("=" * 80)
        print("🏁 COMPREHENSIVE PHASE 1 TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        # Categorize tests
        batch_tests = [r for r in self.test_results if "Batch" in r["test"]]
        monitoring_tests = [r for r in self.test_results if "Performance" in r["test"] or "Benchmark" in r["test"]]
        
        batch_success = all(r["success"] for r in batch_tests)
        monitoring_success = all(r["success"] for r in monitoring_tests)
        
        print("🎯 COMPREHENSIVE PHASE 1 VALIDATION:")
        print(f"✅ Batch Operations (10x faster): {'PASS' if batch_success else 'FAIL'}")
        print(f"✅ Performance Monitoring: {'PASS' if monitoring_success else 'FAIL'}")
        
        overall_success = batch_success and monitoring_success
        print()
        print(f"🏆 COMPREHENSIVE PHASE 1 STATUS: {'✅ SUCCESS' if overall_success else '❌ INCOMPLETE'}")
        
        if overall_success:
            print("🎉 ALL Phase 1 performance optimizations validated successfully!")
            print("🚀 Phase 1 - Performance Optimization is COMPLETE!")
            print("🔄 Ready to proceed to Phase 2 (Reliability & Scalability)")
        else:
            print("⚠️  Some advanced Phase 1 features need attention")
            
            if failed_tests > 0:
                print("\n❌ FAILED TESTS:")
                for result in self.test_results:
                    if not result["success"]:
                        print(f"  - {result['test']}: {result['details']}")
        
        print("=" * 80)


def main():
    """Main test execution."""
    tester = ComprehensiveQuantumTester()
    tester.run_comprehensive_tests()


if __name__ == "__main__":
    main()