"""
Pytest configuration and fixtures for E2E tests
"""

import pytest
import asyncio
import time
from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock

from src.remy_mcp.client import IsraeliLandAPI
from src.remy_mcp.server import create_server
from src.remy_mcp.models import KOD_YESHUV_SETTLEMENTS


@pytest.fixture
def api_client():
    """Create API client instance for testing"""
    return IsraeliLandAPI(rate_limit_delay=0.1)  # Faster for tests


@pytest.fixture
def mcp_server():
    """Create MCP server instance for testing"""
    return create_server()


@pytest.fixture
def sample_tender_id():
    """Sample tender ID for testing (should exist in real API)"""
    # This should be updated with a real tender ID that exists
    return 20250001


@pytest.fixture
def sample_settlement_names():
    """Sample settlement names for testing"""
    return [
        "תל אביב",
        "ירושלים", 
        "חיפה",
        "באר שבע",
        "נתניה"
    ]


@pytest.fixture
def sample_search_params():
    """Sample search parameters for testing"""
    return {
        "active_only": True,
        "max_results": 5,
        "tender_types": [1, 2],  # Regular public and target price
        "regions": [4],  # Tel Aviv region
    }


@pytest.fixture
def rate_limiter():
    """Helper to ensure we don't exceed API rate limits during tests"""
    last_call_time = {"time": 0}
    
    def wait_for_rate_limit(min_delay: float = 1.0):
        current_time = time.time()
        time_since_last = current_time - last_call_time["time"]
        if time_since_last < min_delay:
            time.sleep(min_delay - time_since_last)
        last_call_time["time"] = time.time()
    
    return wait_for_rate_limit


@pytest.fixture
def test_data_validator():
    """Helper to validate API response data structure"""
    def validate_tender_data(tender: Dict[str, Any]) -> bool:
        """Validate basic tender data structure"""
        required_fields = ["MichrazID"]
        optional_fields = [
            "MichrazName", "KodMerchav", "StatusMichraz", 
            "KodYeudMichraz", "KodYeshuv", "Shchuna",
            "PirsumDate", "SgiraDate", "VaadaDate"
        ]
        
        # Check required fields
        for field in required_fields:
            if field not in tender:
                return False
                
        # Check data types for key fields
        if not isinstance(tender.get("MichrazID"), int):
            return False
            
        return True
    
    def validate_search_response(response: Dict[str, Any]) -> bool:
        """Validate search response structure"""
        if not isinstance(response, (list, dict)):
            return False
            
        if isinstance(response, list):
            return all(validate_tender_data(tender) for tender in response)
        
        # If dict, check for results array
        if "results" in response:
            return all(validate_tender_data(tender) for tender in response["results"])
            
        return True
    
    return {
        "tender": validate_tender_data,
        "search": validate_search_response
    }


@pytest.fixture(scope="session")
def test_config():
    """Test configuration settings"""
    return {
        "api_timeout": 30,
        "max_retries": 3,
        "rate_limit_delay": 1.0,
        "test_timeout": 60,
        "skip_slow_tests": False,  # Set to True to skip slow E2E tests
    }


@pytest.fixture
def known_settlement_codes():
    """Known settlement codes for testing"""
    # Get first few settlements from our reference data
    return {
        settlement.name_hebrew: settlement.kod_yeshuv 
        for settlement in KOD_YESHUV_SETTLEMENTS[:10]
    }


@pytest.fixture
def mock_response_data():
    """Mock response data for testing when API is unavailable"""
    return {
        "search_response": [
            {
                "MichrazID": 20250001,
                "MichrazName": "1/2025",
                "KodMerchav": 4,
                "StatusMichraz": 1,
                "KodYeudMichraz": 1,
                "KodYeshuv": 5000,
                "KodSugMichraz": 1,
                "Shchuna": "test neighborhood",
                "PirsumDate": "2025-01-01T00:00:00+03:00",
                "SgiraDate": "2025-03-01T12:00:00+03:00",
                "VaadaDate": "2025-03-15T00:00:00+03:00",
                "YechidotDiur": 50
            }
        ],
        "details_response": {
            "MichrazID": 20250001,
            "MichrazName": "1/2025",
            "Divur": "Test tender remarks",
            "Comments": "Test comments",
            "TokefArvut": "2025-06-01T00:00:00+03:00",
            "SchumArvut": 100000.0
        },
        "map_response": {
            "MichrazID": 20250001,
            "coordinates": {"lat": 32.0853, "lng": 34.7818},
            "map_data": {"zoom": 15}
        }
    }


# Async test support
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Skip markers for different test types
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "api: marks tests that require API access"
    )
    config.addinivalue_line(
        "markers", "mcp: marks tests for MCP server functionality"
    )