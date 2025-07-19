"""
End-to-end tests for Israeli Land Authority API client
Tests actual API calls to verify functionality
"""

import pytest
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List

from src.remy_mcp.client import IsraeliLandAPI


class TestIsraeliLandAPIE2E:
    """End-to-end tests for the API client"""

    @pytest.mark.e2e
    @pytest.mark.api
    def test_api_client_initialization(self, api_client):
        """Test API client can be initialized properly"""
        assert api_client is not None
        assert api_client.BASE_URL == "https://apps.land.gov.il/MichrazimSite/api"
        assert api_client.rate_limit_delay == 0.1
        assert api_client.session is not None

    @pytest.mark.e2e
    @pytest.mark.api
    def test_search_tenders_basic(self, api_client, rate_limiter, test_data_validator):
        """Test basic tender search functionality"""
        rate_limiter()
        
        # Test basic search - get first 5 results
        results = api_client.search_tenders(page_size=5)
        
        assert results is not None
        assert test_data_validator["search"](results)
        
        # Extract actual tender list
        tender_list = results if isinstance(results, list) else results.get("results", [])
        assert len(tender_list) <= 5
        
        # Validate each tender has required fields
        for tender in tender_list:
            assert "MichrazID" in tender
            assert isinstance(tender["MichrazID"], int)

    @pytest.mark.e2e
    @pytest.mark.api
    def test_search_active_tenders(self, api_client, rate_limiter, test_data_validator):
        """Test searching for only active tenders"""
        rate_limiter()
        
        results = api_client.search_tenders(active_only=True, page_size=10)
        
        assert results is not None
        assert test_data_validator["search"](results)
        
        tender_list = results if isinstance(results, list) else results.get("results", [])
        
        # All returned tenders should be active (status check if available)
        for tender in tender_list:
            assert "MichrazID" in tender
            # Note: We can't easily verify "active" status without knowing
            # the exact status codes, but the API should filter correctly

    @pytest.mark.e2e
    @pytest.mark.api
    def test_search_by_tender_types(self, api_client, rate_limiter, test_data_validator):
        """Test searching by specific tender types"""
        rate_limiter()
        
        # Search for regular public tenders (type 1)
        results = api_client.search_tenders(tender_types=[1], page_size=5)
        
        assert results is not None
        assert test_data_validator["search"](results)
        
        tender_list = results if isinstance(results, list) else results.get("results", [])
        
        # Verify results contain the expected tender type
        for tender in tender_list:
            assert "MichrazID" in tender
            # Note: API should filter by tender type, but we'd need to check
            # KodSugMichraz field to verify (if present in response)

    @pytest.mark.e2e
    @pytest.mark.api
    def test_search_by_region(self, api_client, rate_limiter, test_data_validator):
        """Test searching by region"""
        rate_limiter()
        
        # Search in Tel Aviv region (region 4)
        results = api_client.search_tenders(regions=[4], page_size=5)
        
        assert results is not None
        assert test_data_validator["search"](results)

    @pytest.mark.e2e
    @pytest.mark.api
    def test_search_with_date_range(self, api_client, rate_limiter, test_data_validator):
        """Test searching with date range filters"""
        rate_limiter()
        
        # Search for tenders published in the last 30 days
        date_from = datetime.now() - timedelta(days=30)
        
        results = api_client.search_tenders(
            publication_date_from=date_from,
            page_size=5
        )
        
        assert results is not None
        assert test_data_validator["search"](results)

    @pytest.mark.e2e
    @pytest.mark.api
    def test_search_with_settlement_code(self, api_client, rate_limiter, test_data_validator, known_settlement_codes):
        """Test searching by settlement code (Kod Yeshuv)"""
        rate_limiter()
        
        # Use first known settlement code
        settlement_code = list(known_settlement_codes.values())[0]
        
        results = api_client.search_tenders(
            kod_yeshuv=settlement_code,
            page_size=5
        )
        
        assert results is not None
        assert test_data_validator["search"](results)

    @pytest.mark.e2e
    @pytest.mark.api
    @pytest.mark.slow
    def test_get_tender_details(self, api_client, rate_limiter, sample_tender_id):
        """Test getting detailed tender information"""
        rate_limiter()
        
        # First, search for any tender to get a valid ID
        search_results = api_client.search_tenders(page_size=1)
        
        if isinstance(search_results, list) and search_results:
            tender_id = search_results[0]["MichrazID"]
        elif isinstance(search_results, dict) and search_results.get("results"):
            tender_id = search_results["results"][0]["MichrazID"]
        else:
            pytest.skip("No tenders found to test details endpoint")
        
        rate_limiter()
        
        # Get details for the found tender
        details = api_client.get_tender_details(tender_id)
        
        assert details is not None
        assert isinstance(details, dict)
        assert "MichrazID" in details
        assert details["MichrazID"] == tender_id

    @pytest.mark.e2e
    @pytest.mark.api
    @pytest.mark.slow
    def test_get_tender_map_details(self, api_client, rate_limiter):
        """Test getting tender map/geographic details"""
        rate_limiter()
        
        # First, search for any tender to get a valid ID
        search_results = api_client.search_tenders(page_size=1)
        
        if isinstance(search_results, list) and search_results:
            tender_id = search_results[0]["MichrazID"]
        elif isinstance(search_results, dict) and search_results.get("results"):
            tender_id = search_results["results"][0]["MichrazID"]
        else:
            pytest.skip("No tenders found to test map details endpoint")
        
        rate_limiter()
        
        # Get map details for the found tender
        map_details = api_client.get_tender_map_details(tender_id)
        
        # Map details might be empty for some tenders, so we just check it doesn't error
        assert map_details is not None
        assert isinstance(map_details, dict)

    @pytest.mark.e2e
    @pytest.mark.api
    def test_get_active_tenders_method(self, api_client, rate_limiter, test_data_validator):
        """Test the dedicated get_active_tenders method"""
        rate_limiter()
        
        results = api_client.get_active_tenders()
        
        assert results is not None
        assert test_data_validator["search"](results)

    @pytest.mark.e2e
    @pytest.mark.api
    def test_get_recent_results(self, api_client, rate_limiter, test_data_validator):
        """Test getting recent tender results"""
        rate_limiter()
        
        results = api_client.get_recent_results(days=30)
        
        assert results is not None
        assert test_data_validator["search"](results)

    @pytest.mark.e2e
    @pytest.mark.api
    def test_search_by_type_method(self, api_client, rate_limiter, test_data_validator):
        """Test the dedicated search_by_type method"""
        rate_limiter()
        
        results = api_client.search_by_type(tender_types=[1, 2])
        
        assert results is not None
        assert test_data_validator["search"](results)

    @pytest.mark.e2e
    @pytest.mark.api
    def test_search_by_location_method(self, api_client, rate_limiter, test_data_validator, known_settlement_codes):
        """Test the dedicated search_by_location method"""
        rate_limiter()
        
        # Use first known settlement code
        settlement_code = list(known_settlement_codes.values())[0]
        
        results = api_client.search_by_location(settlement_code=settlement_code)
        
        assert results is not None
        assert test_data_validator["search"](results)

    @pytest.mark.e2e
    @pytest.mark.api
    def test_rate_limiting(self, api_client):
        """Test that rate limiting is working"""
        # Create client with longer delay for this test
        test_client = IsraeliLandAPI(rate_limit_delay=1.0)
        
        start_time = time.time()
        
        # Make two consecutive calls
        test_client.search_tenders(page_size=1)
        test_client.search_tenders(page_size=1)
        
        end_time = time.time()
        
        # Should take at least 1 second due to rate limiting
        assert end_time - start_time >= 1.0

    @pytest.mark.e2e
    @pytest.mark.api
    def test_error_handling_invalid_tender_id(self, api_client, rate_limiter):
        """Test error handling for invalid tender ID"""
        rate_limiter()
        
        # Use an obviously invalid tender ID
        result = api_client.get_tender_details(-1)
        
        # API doesn't raise exception but returns structured error response
        assert result is not None
        assert isinstance(result, dict)
        
        # Check for error indication in response
        if "MessageDetails" in result:
            # Hebrew message: "המכרז לא קיים" = "The tender does not exist"
            assert result["MessageDetails"]["messageCode"] == 1
            assert "לא קיים" in result["MessageDetails"]["messageText"]
        else:
            # Alternatively, check for empty/null values indicating no tender found
            assert result.get("MichrazID") in [0, None] or result.get("MichrazName") is None

    @pytest.mark.e2e
    @pytest.mark.api
    def test_hebrew_text_handling(self, api_client, rate_limiter, test_data_validator):
        """Test that Hebrew text in responses is handled correctly"""
        rate_limiter()
        
        results = api_client.search_tenders(page_size=5)
        
        assert results is not None
        assert test_data_validator["search"](results)
        
        tender_list = results if isinstance(results, list) else results.get("results", [])
        
        # Check that Hebrew text fields are properly encoded
        for tender in tender_list:
            if "Shchuna" in tender and tender["Shchuna"]:
                # Should be able to encode/decode Hebrew text
                hebrew_text = tender["Shchuna"]
                assert isinstance(hebrew_text, str)
                # Verify it can be encoded to UTF-8
                hebrew_text.encode("utf-8")

    @pytest.mark.e2e
    @pytest.mark.api
    def test_large_result_set(self, api_client, rate_limiter, test_data_validator):
        """Test handling larger result sets"""
        rate_limiter()
        
        # Request larger page size
        results = api_client.search_tenders(page_size=100)
        
        assert results is not None
        assert test_data_validator["search"](results)
        
        tender_list = results if isinstance(results, list) else results.get("results", [])
        
        # Should get results up to page size limit
        assert len(tender_list) <= 100

    @pytest.mark.e2e
    @pytest.mark.api
    def test_pagination(self, api_client, rate_limiter, test_data_validator):
        """Test pagination functionality"""
        rate_limiter()
        
        # Get first page
        page1 = api_client.search_tenders(page_size=5, page_number=1)
        
        rate_limiter()
        
        # Get second page
        page2 = api_client.search_tenders(page_size=5, page_number=2)
        
        assert page1 is not None
        assert page2 is not None
        assert test_data_validator["search"](page1)
        assert test_data_validator["search"](page2)
        
        # Extract tender lists
        list1 = page1 if isinstance(page1, list) else page1.get("results", [])
        list2 = page2 if isinstance(page2, list) else page2.get("results", [])
        
        # Pages should have different content (if there are enough results)
        if list1 and list2:
            ids1 = {tender["MichrazID"] for tender in list1}
            ids2 = {tender["MichrazID"] for tender in list2}
            # Should have different tender IDs (assuming enough data)
            assert len(ids1.intersection(ids2)) == 0 or len(list1) + len(list2) < 10

    @pytest.mark.e2e
    @pytest.mark.api
    def test_comprehensive_search_filters(self, api_client, rate_limiter, test_data_validator):
        """Test comprehensive search with multiple filters"""
        rate_limiter()
        
        # Complex search with multiple filters
        results = api_client.search_tenders(
            tender_types=[1, 2],
            regions=[4, 5],  # Tel Aviv and Jerusalem
            active_only=True,
            page_size=10,
            has_results=False  # Only tenders without results yet
        )
        
        assert results is not None
        assert test_data_validator["search"](results)