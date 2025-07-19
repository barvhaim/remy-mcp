"""
Performance and load tests for the Israeli Land Authority API
"""

import pytest
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

from src.remy_mcp.client import IsraeliLandAPI
from tests.utils import (
    PerformanceTracker, 
    timed_api_call, 
    APITestHelper,
    requires_api_access,
    skip_if_slow
)


class TestPerformanceE2E:
    """Performance tests for API client"""

    @pytest.mark.e2e
    @pytest.mark.slow
    @requires_api_access
    def test_api_response_times(self):
        """Test API response times are within acceptable limits"""
        api_client = IsraeliLandAPI(rate_limit_delay=1.1)  # Slightly above 1 second
        tracker = PerformanceTracker()
        
        # Test multiple calls
        for i in range(5):
            with timed_api_call(tracker):
                results = api_client.search_tenders(page_size=5)
                assert results is not None
        
        stats = tracker.get_stats()
        
        # Response times should be reasonable
        assert stats["avg_response_time"] < 10.0, f"Average response time too high: {stats['avg_response_time']}"
        assert stats["max_response_time"] < 30.0, f"Max response time too high: {stats['max_response_time']}"
        assert stats["error_rate"] == 0.0, f"Unexpected errors: {stats['error_rate']}"

    @pytest.mark.e2e
    @pytest.mark.slow
    @requires_api_access
    def test_rate_limiting_effectiveness(self):
        """Test that rate limiting properly enforces delays"""
        api_client = IsraeliLandAPI(rate_limit_delay=2.0)
        
        start_time = time.time()
        
        # Make 3 consecutive calls
        for i in range(3):
            api_client.search_tenders(page_size=1)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should take at least 4 seconds (2 delays between 3 calls)
        assert total_time >= 4.0, f"Rate limiting not working: {total_time} seconds"
        
        # But not too much longer (allowing for API response time)
        assert total_time < 10.0, f"Rate limiting too aggressive: {total_time} seconds"

    @pytest.mark.e2e
    @pytest.mark.slow
    @requires_api_access 
    def test_concurrent_request_handling(self):
        """Test handling of concurrent requests with rate limiting"""
        def make_api_call(client_id: int) -> Dict[str, Any]:
            """Make an API call and return timing info"""
            api_client = IsraeliLandAPI(rate_limit_delay=1.0)
            start_time = time.time()
            
            try:
                results = api_client.search_tenders(page_size=2)
                end_time = time.time()
                
                return {
                    "client_id": client_id,
                    "success": True,
                    "duration": end_time - start_time,
                    "result_count": len(results) if isinstance(results, list) else len(results.get("results", []))
                }
            except Exception as e:
                end_time = time.time()
                return {
                    "client_id": client_id,
                    "success": False,
                    "duration": end_time - start_time,
                    "error": str(e)
                }
        
        # Test with 3 concurrent requests
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_api_call, i) for i in range(3)]
            results = [future.result() for future in as_completed(futures)]
        
        # All requests should succeed
        successful_results = [r for r in results if r["success"]]
        assert len(successful_results) == 3, f"Some requests failed: {results}"
        
        # Check timing - each should be properly rate limited
        durations = [r["duration"] for r in successful_results]
        avg_duration = statistics.mean(durations)
        
        # Average should be reasonable (rate limiting + API response time)
        assert avg_duration >= 1.0, "Rate limiting not applied to concurrent requests"
        assert avg_duration < 15.0, f"Concurrent requests too slow: {avg_duration}"

    @pytest.mark.e2e
    @pytest.mark.slow
    @requires_api_access
    def test_large_result_set_performance(self):
        """Test performance with larger result sets"""
        api_client = IsraeliLandAPI(rate_limit_delay=0.5)
        tracker = PerformanceTracker()
        
        # Test with different page sizes
        page_sizes = [10, 50, 100]
        
        for page_size in page_sizes:
            with timed_api_call(tracker):
                results = api_client.search_tenders(page_size=page_size)
                assert results is not None
                
                # Verify we got results up to the requested size
                result_list = results if isinstance(results, list) else results.get("results", [])
                assert len(result_list) <= page_size
        
        stats = tracker.get_stats()
        
        # Larger results shouldn't be dramatically slower
        assert stats["max_response_time"] < 20.0, f"Large result sets too slow: {stats['max_response_time']}"

    @pytest.mark.e2e
    @pytest.mark.slow
    @requires_api_access
    def test_details_endpoint_performance(self):
        """Test performance of tender details endpoint"""
        helper = APITestHelper(rate_limit_delay=1.1)
        
        # Get a sample tender ID
        tender_id = helper.get_sample_tender_id()
        if not tender_id:
            pytest.skip("No tender ID available for testing")
        
        tracker = PerformanceTracker()
        
        # Test details endpoint multiple times
        for i in range(3):
            with timed_api_call(tracker):
                details = helper.api_client.get_tender_details(tender_id)
                assert details is not None
                assert "MichrazID" in details
        
        stats = tracker.get_stats()
        
        # Details endpoint should be reasonably fast
        assert stats["avg_response_time"] < 8.0, f"Details endpoint too slow: {stats['avg_response_time']}"
        assert stats["error_rate"] == 0.0, "Details endpoint errors"

    @pytest.mark.e2e
    @pytest.mark.slow
    @requires_api_access
    def test_map_endpoint_performance(self):
        """Test performance of map details endpoint"""
        helper = APITestHelper(rate_limit_delay=1.1)
        
        # Get a sample tender ID
        tender_id = helper.get_sample_tender_id()
        if not tender_id:
            pytest.skip("No tender ID available for testing")
        
        tracker = PerformanceTracker()
        
        # Test map endpoint
        for i in range(2):  # Fewer iterations as this might be slower
            with timed_api_call(tracker):
                map_details = helper.api_client.get_tender_map_details(tender_id)
                # Map details might be empty, but should not error
                assert map_details is not None
        
        stats = tracker.get_stats()
        
        # Map endpoint might be slower, but should still be reasonable
        assert stats["avg_response_time"] < 15.0, f"Map endpoint too slow: {stats['avg_response_time']}"

    @pytest.mark.e2e
    @pytest.mark.slow
    @requires_api_access
    def test_search_with_complex_filters_performance(self):
        """Test performance with complex search filters"""
        api_client = IsraeliLandAPI(rate_limit_delay=1.1)
        tracker = PerformanceTracker()
        
        # Complex search parameters
        complex_searches = [
            {
                "tender_types": [1, 2, 3],
                "regions": [4, 5],
                "active_only": True,
                "page_size": 20
            },
            {
                "tender_types": [1],
                "priority_populations": [1, 3, 6],
                "quick_search": True,
                "page_size": 15
            },
            {
                "regions": [4],
                "tender_statuses": [1],
                "page_size": 10
            }
        ]
        
        for search_params in complex_searches:
            with timed_api_call(tracker):
                results = api_client.search_tenders(**search_params)
                assert results is not None
        
        stats = tracker.get_stats()
        
        # Complex searches might be slower but should still be acceptable
        assert stats["avg_response_time"] < 12.0, f"Complex searches too slow: {stats['avg_response_time']}"
        assert stats["error_rate"] == 0.0, "Complex search errors"

    @pytest.mark.e2e
    @pytest.mark.slow
    @requires_api_access
    def test_pagination_performance(self):
        """Test performance of pagination"""
        api_client = IsraeliLandAPI(rate_limit_delay=1.1)
        tracker = PerformanceTracker()
        
        # Test multiple pages
        for page_num in range(1, 4):  # Test first 3 pages
            with timed_api_call(tracker):
                results = api_client.search_tenders(
                    page_size=10,
                    page_number=page_num
                )
                assert results is not None
        
        stats = tracker.get_stats()
        
        # Pagination performance should be consistent
        response_times = tracker.call_times
        if len(response_times) >= 3:
            # Check that later pages aren't significantly slower
            time_variance = statistics.stdev(response_times)
            avg_time = statistics.mean(response_times)
            
            # Variance should be reasonable (not more than 50% of average)
            assert time_variance < avg_time * 0.5, f"High pagination variance: {time_variance}"

    @pytest.mark.e2e
    @pytest.mark.slow 
    @requires_api_access
    def test_error_recovery_performance(self):
        """Test performance of error recovery mechanisms"""
        api_client = IsraeliLandAPI(rate_limit_delay=0.5)
        
        # Test with invalid parameters that should cause errors
        start_time = time.time()
        
        try:
            # This should fail quickly
            api_client.get_tender_details(-1)
        except Exception:
            pass  # Expected
        
        error_time = time.time() - start_time
        
        # Error handling should be fast (not timing out)
        assert error_time < 5.0, f"Error handling too slow: {error_time}"
        
        # After error, normal requests should still work
        start_time = time.time()
        results = api_client.search_tenders(page_size=1)
        recovery_time = time.time() - start_time
        
        assert results is not None
        assert recovery_time < 10.0, f"Recovery after error too slow: {recovery_time}"

    @pytest.mark.e2e
    @pytest.mark.slow
    @requires_api_access
    def test_memory_usage_with_large_results(self):
        """Test memory usage doesn't grow excessively with large results"""
        import psutil
        import os
        
        api_client = IsraeliLandAPI(rate_limit_delay=1.1)
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Make several requests for larger datasets
        for i in range(3):
            results = api_client.search_tenders(page_size=100)
            assert results is not None
            
            # Clear reference to results
            del results
        
        # Check memory usage after
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100, f"Excessive memory usage: {memory_increase}MB increase"

    @pytest.mark.e2e
    @pytest.mark.slow
    @skip_if_slow
    def test_sustained_load_performance(self):
        """Test performance under sustained load"""
        api_client = IsraeliLandAPI(rate_limit_delay=1.0)
        tracker = PerformanceTracker()
        
        # Run sustained requests for 2 minutes
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < 120:  # 2 minutes
            with timed_api_call(tracker):
                try:
                    results = api_client.search_tenders(page_size=5)
                    assert results is not None
                    request_count += 1
                except Exception as e:
                    # Allow some errors under sustained load
                    tracker.record_call(0, 0, True)
        
        stats = tracker.get_stats()
        
        # Should have made reasonable number of requests
        assert request_count >= 90, f"Too few requests completed: {request_count}"
        
        # Error rate should be low
        assert stats["error_rate"] <= 0.1, f"High error rate under load: {stats['error_rate']}"
        
        # Performance should remain stable
        response_times = tracker.call_times
        if len(response_times) >= 10:
            first_half = response_times[:len(response_times)//2]
            second_half = response_times[len(response_times)//2:]
            
            avg_first = statistics.mean(first_half)
            avg_second = statistics.mean(second_half)
            
            # Performance shouldn't degrade significantly over time
            degradation = (avg_second - avg_first) / avg_first if avg_first > 0 else 0
            assert degradation < 0.5, f"Performance degraded under load: {degradation * 100}%"