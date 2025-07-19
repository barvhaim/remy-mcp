"""
Test utilities and helpers for E2E testing
"""

import time
import json
import requests
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from contextlib import contextmanager

from src.remy_mcp.client import IsraeliLandAPI


class APITestHelper:
    """Helper class for API testing utilities"""
    
    def __init__(self, rate_limit_delay: float = 1.0):
        self.api_client = IsraeliLandAPI(rate_limit_delay=rate_limit_delay)
        self.last_call_time = 0.0
        
    def wait_for_rate_limit(self, min_delay: float = 1.0):
        """Ensure minimum delay between API calls"""
        current_time = time.time()
        time_since_last = current_time - self.last_call_time
        if time_since_last < min_delay:
            time.sleep(min_delay - time_since_last)
        self.last_call_time = time.time()
    
    def get_sample_tender_id(self) -> Optional[int]:
        """Get a sample tender ID for testing"""
        try:
            self.wait_for_rate_limit()
            results = self.api_client.search_tenders(page_size=1)
            
            if isinstance(results, list) and results:
                return results[0]["MichrazID"]
            elif isinstance(results, dict) and results.get("results"):
                return results["results"][0]["MichrazID"]
            
            return None
        except Exception:
            return None
    
    def is_api_available(self) -> bool:
        """Check if the API is available and responding"""
        try:
            self.wait_for_rate_limit()
            response = requests.get(
                f"{self.api_client.BASE_URL}/SearchApi/Search",
                headers=self.api_client.REQUIRED_HEADERS,
                timeout=10
            )
            return response.status_code in [200, 405]  # 405 for wrong method but API is up
        except Exception:
            return False
    
    def get_sample_data_for_validation(self) -> Dict[str, Any]:
        """Get sample data for validation testing"""
        try:
            self.wait_for_rate_limit()
            results = self.api_client.search_tenders(page_size=3)
            
            sample_data = {
                "search_results": results,
                "has_data": bool(results)
            }
            
            # Try to get details for first tender
            if isinstance(results, list) and results:
                tender_id = results[0]["MichrazID"]
            elif isinstance(results, dict) and results.get("results"):
                tender_id = results["results"][0]["MichrazID"]
            else:
                return sample_data
                
            self.wait_for_rate_limit()
            try:
                details = self.api_client.get_tender_details(tender_id)
                sample_data["details_sample"] = details
            except Exception:
                pass
                
            return sample_data
            
        except Exception:
            return {"search_results": [], "has_data": False}


class DataValidator:
    """Utilities for validating API response data"""
    
    @staticmethod
    def validate_tender_basic_structure(tender: Dict[str, Any]) -> bool:
        """Validate basic tender data structure"""
        required_fields = ["MichrazID"]
        
        for field in required_fields:
            if field not in tender:
                return False
                
        # Check data types
        if not isinstance(tender.get("MichrazID"), int):
            return False
            
        # Optional fields should have correct types if present
        optional_int_fields = ["KodMerchav", "StatusMichraz", "KodYeudMichraz", "KodYeshuv"]
        for field in optional_int_fields:
            if field in tender and tender[field] is not None:
                if not isinstance(tender[field], int):
                    return False
                    
        return True
    
    @staticmethod
    def validate_search_response(response: Any) -> bool:
        """Validate search response structure"""
        if response is None:
            return False
            
        if isinstance(response, list):
            return all(DataValidator.validate_tender_basic_structure(t) for t in response)
        
        if isinstance(response, dict):
            if "results" in response:
                return all(DataValidator.validate_tender_basic_structure(t) for t in response["results"])
            # Single tender response
            return DataValidator.validate_tender_basic_structure(response)
            
        return False
    
    @staticmethod
    def validate_hebrew_text_encoding(text: str) -> bool:
        """Validate Hebrew text can be properly encoded/decoded"""
        try:
            # Should be able to encode to UTF-8
            encoded = text.encode("utf-8")
            # Should be able to decode back
            decoded = encoded.decode("utf-8")
            return decoded == text
        except Exception:
            return False
    
    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        """Validate Israeli date format"""
        try:
            # Should be in ISO format with timezone
            if "T" in date_str and ("+03:00" in date_str or "+02:00" in date_str):
                datetime.fromisoformat(date_str.replace("+03:00", "").replace("+02:00", ""))
                return True
            return False
        except Exception:
            return False


class PerformanceTracker:
    """Track performance metrics during testing"""
    
    def __init__(self):
        self.call_times = []
        self.response_sizes = []
        self.error_count = 0
        
    def record_call(self, duration: float, response_size: int = 0, error: bool = False):
        """Record a single API call"""
        self.call_times.append(duration)
        self.response_sizes.append(response_size)
        if error:
            self.error_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        if not self.call_times:
            return {"no_data": True}
            
        return {
            "total_calls": len(self.call_times),
            "avg_response_time": sum(self.call_times) / len(self.call_times),
            "max_response_time": max(self.call_times),
            "min_response_time": min(self.call_times),
            "avg_response_size": sum(self.response_sizes) / len(self.response_sizes) if self.response_sizes else 0,
            "error_rate": self.error_count / len(self.call_times),
            "calls_per_second": len(self.call_times) / sum(self.call_times) if sum(self.call_times) > 0 else 0
        }


@contextmanager
def timed_api_call(tracker: PerformanceTracker):
    """Context manager to time API calls"""
    start_time = time.time()
    error_occurred = False
    response_size = 0
    
    try:
        yield
    except Exception as e:
        error_occurred = True
        raise
    finally:
        duration = time.time() - start_time
        tracker.record_call(duration, response_size, error_occurred)


class MockDataGenerator:
    """Generate mock data for testing when API is unavailable"""
    
    @staticmethod
    def generate_mock_tender(tender_id: int = None) -> Dict[str, Any]:
        """Generate a mock tender for testing"""
        if tender_id is None:
            tender_id = 20250000 + (int(time.time()) % 10000)
            
        return {
            "MichrazID": tender_id,
            "MichrazName": f"{tender_id % 1000}/2025",
            "KodMerchav": (tender_id % 6) + 1,
            "StatusMichraz": (tender_id % 3) + 1,
            "KodYeudMichraz": (tender_id % 9) + 1,
            "KodYeshuv": 5000 + (tender_id % 100),
            "KodSugMichraz": (tender_id % 9) + 1,
            "Shchuna": "שכונה לדוגמה",
            "PirsumDate": "2025-01-01T00:00:00+03:00",
            "SgiraDate": "2025-03-01T12:00:00+03:00",
            "VaadaDate": "2025-03-15T00:00:00+03:00",
            "YechidotDiur": (tender_id % 50) + 10
        }
    
    @staticmethod
    def generate_mock_search_results(count: int = 5) -> List[Dict[str, Any]]:
        """Generate mock search results"""
        return [
            MockDataGenerator.generate_mock_tender(20250000 + i)
            for i in range(count)
        ]
    
    @staticmethod
    def generate_mock_details(tender_id: int) -> Dict[str, Any]:
        """Generate mock tender details"""
        basic = MockDataGenerator.generate_mock_tender(tender_id)
        basic.update({
            "Divur": "הערות לדוגמה על המכרז",
            "Comments": "הערות נוספות",
            "TokefArvut": "2025-06-01T00:00:00+03:00",
            "SchumArvut": 100000.0 + (tender_id % 50000),
            "TokefArvutSarvan": "2025-07-01T00:00:00+03:00",
            "SumArvutSarvan": 50000.0 + (tender_id % 25000)
        })
        return basic


class TestConfigManager:
    """Manage test configuration and environment settings"""
    
    def __init__(self):
        self.config = {
            "api_timeout": 30,
            "rate_limit_delay": 1.0,
            "max_retries": 3,
            "skip_slow_tests": False,
            "use_mock_data": False,
            "test_data_cache_ttl": 300  # 5 minutes
        }
        self._cached_data = {}
        self._cache_times = {}
    
    def get_config(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value
    
    def cache_test_data(self, key: str, data: Any):
        """Cache test data with TTL"""
        self._cached_data[key] = data
        self._cache_times[key] = time.time()
    
    def get_cached_data(self, key: str) -> Optional[Any]:
        """Get cached test data if still valid"""
        if key not in self._cached_data:
            return None
            
        cache_time = self._cache_times.get(key, 0)
        ttl = self.config.get("test_data_cache_ttl", 300)
        
        if time.time() - cache_time > ttl:
            # Cache expired
            del self._cached_data[key]
            del self._cache_times[key]
            return None
            
        return self._cached_data[key]
    
    def should_skip_slow_tests(self) -> bool:
        """Check if slow tests should be skipped"""
        return self.config.get("skip_slow_tests", False)
    
    def should_use_mock_data(self) -> bool:
        """Check if mock data should be used instead of real API"""
        return self.config.get("use_mock_data", False)


# Global test configuration instance
test_config = TestConfigManager()


def requires_api_access(test_func: Callable) -> Callable:
    """Decorator to skip tests that require API access when unavailable"""
    def wrapper(*args, **kwargs):
        if test_config.should_use_mock_data():
            # Skip or modify test for mock data
            return test_func(*args, **kwargs)
            
        helper = APITestHelper()
        if not helper.is_api_available():
            import pytest
            pytest.skip("API not available for testing")
            
        return test_func(*args, **kwargs)
    
    return wrapper


def skip_if_slow(test_func: Callable) -> Callable:
    """Decorator to skip slow tests based on configuration"""
    def wrapper(*args, **kwargs):
        if test_config.should_skip_slow_tests():
            import pytest
            pytest.skip("Slow tests disabled")
            
        return test_func(*args, **kwargs)
    
    return wrapper