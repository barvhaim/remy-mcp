"""
End-to-end tests for MCP server functionality
Tests the full MCP protocol implementation
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from typing import Dict, Any

from src.remy_mcp.server import create_server
from src.remy_mcp.models import (
    SearchTendersArgs,
    TenderDetailsArgs,
    TypeSearchArgs,
    RecentResultsArgs,
    KodYeshuvArgs,
    DateRange,
)


class TestMCPServerE2E:
    """End-to-end tests for MCP server tools and resources"""

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_server_creation(self, mcp_server):
        """Test MCP server can be created successfully"""
        assert mcp_server is not None
        assert mcp_server.name == "Israeli Land Authority"

    @pytest.mark.e2e
    @pytest.mark.mcp
    async def test_search_tenders_tool_basic(self, mcp_server, rate_limiter):
        """Test basic search_tenders tool functionality"""
        rate_limiter()

        # Create search arguments
        search_args = SearchTendersArgs(max_results=5, active_only=True)

        # Call the tool through MCP server
        # Note: This tests the MCP tool wrapper, not direct API calls
        # We'll mock the API client to avoid hitting real API in unit tests
        with patch(
            "src.remy_mcp.client.israeli_land_api.IsraeliLandAPI.search_tenders"
        ) as mock_search:
            mock_search.return_value = [
                {"MichrazID": 20250001, "MichrazName": "1/2025", "StatusMichraz": 1}
            ]

            # Get available tools
            tools = await mcp_server.get_tools()
            search_tool = None
            for tool_name, tool in tools.items():
                if "search_tenders" in tool_name:
                    search_tool = tool
                    break

            assert search_tool is not None
            # Test that the tool exists and has the expected structure
            assert search_tool.name
            assert search_tool.description

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_search_tenders_with_date_ranges(self, mcp_server):
        """Test search_tenders tool with date range filters"""
        search_args = SearchTendersArgs(
            submission_deadline=DateRange(from_date="01/01/25", to_date="31/12/25"),
            publication_date=DateRange(from_date="01/01/25"),
            max_results=3,
        )

        with patch(
            "src.remy_mcp.client.israeli_land_api.IsraeliLandAPI.search_tenders"
        ) as mock_search:
            mock_search.return_value = []

            search_tool = None
            for tool_name, tool_func in mcp_server._tools.items():
                if "search_tenders" in tool_name:
                    search_tool = tool_func
                    break

            result = search_tool(search_args)

            assert result["success"] is True
            assert "search_summary" in result
            assert (
                result["search_summary"]["new_features"]["enhanced_date_ranges"] is True
            )

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_search_tenders_settlement_conversion(self, mcp_server):
        """Test automatic settlement name to kod_yeshuv conversion"""
        search_args = SearchTendersArgs(
            settlement="תל אביב", max_results=3  # Tel Aviv in Hebrew
        )

        with patch(
            "src.remy_mcp.client.israeli_land_api.IsraeliLandAPI.search_tenders"
        ) as mock_search:
            mock_search.return_value = []

            search_tool = None
            for tool_name, tool_func in mcp_server._tools.items():
                if "search_tenders" in tool_name:
                    search_tool = tool_func
                    break

            result = search_tool(search_args)

            assert result["success"] is True
            # Check if settlement conversion occurred
            conversion_info = result["search_summary"]["settlement_conversion"]
            assert conversion_info["settlement_name_provided"] is True

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_get_tender_details_tool(self, mcp_server):
        """Test get_tender_details tool"""
        details_args = TenderDetailsArgs(michraz_id=20250001)

        with patch(
            "src.remy_mcp.client.israeli_land_api.IsraeliLandAPI.get_tender_details"
        ) as mock_details:
            mock_details.return_value = {
                "MichrazID": 20250001,
                "MichrazName": "1/2025",
                "Divur": "Test remarks",
            }

            details_tool = None
            for tool_name, tool_func in mcp_server._tools.items():
                if "get_tender_details" in tool_name:
                    details_tool = tool_func
                    break

            assert details_tool is not None
            result = details_tool(details_args)

            assert result["success"] is True
            assert result["tender_id"] == 20250001
            assert "details" in result

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_get_active_tenders_tool(self, mcp_server):
        """Test get_active_tenders tool"""
        with patch(
            "src.remy_mcp.client.israeli_land_api.IsraeliLandAPI.get_active_tenders"
        ) as mock_active:
            mock_active.return_value = [{"MichrazID": 20250001, "StatusMichraz": 1}]

            active_tool = None
            for tool_name, tool_func in mcp_server._tools.items():
                if "get_active_tenders" in tool_name:
                    active_tool = tool_func
                    break

            assert active_tool is not None
            result = active_tool(max_results=10)

            assert result["success"] is True
            assert "active_tenders" in result
            assert "count" in result

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_search_by_type_tool(self, mcp_server):
        """Test search_by_type tool"""
        type_args = TypeSearchArgs(
            tender_types=[1, 2], purpose="residential", active_only=True
        )

        with patch(
            "src.remy_mcp.client.israeli_land_api.IsraeliLandAPI.search_by_type"
        ) as mock_type_search:
            mock_type_search.return_value = []

            type_tool = None
            for tool_name, tool_func in mcp_server._tools.items():
                if "search_by_type" in tool_name:
                    type_tool = tool_func
                    break

            assert type_tool is not None
            result = type_tool(type_args)

            assert result["success"] is True
            assert "type_search" in result
            assert result["type_search"]["tender_types"] == [1, 2]

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_get_recent_results_tool(self, mcp_server):
        """Test get_recent_results tool"""
        results_args = RecentResultsArgs(days=30)

        with patch(
            "src.remy_mcp.client.israeli_land_api.IsraeliLandAPI.get_recent_results"
        ) as mock_recent:
            mock_recent.return_value = []

            recent_tool = None
            for tool_name, tool_func in mcp_server._tools.items():
                if "get_recent_results" in tool_name:
                    recent_tool = tool_func
                    break

            assert recent_tool is not None
            result = recent_tool(results_args)

            assert result["success"] is True
            assert result["days_back"] == 30
            assert "recent_results" in result

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_get_tender_map_details_tool(self, mcp_server):
        """Test get_tender_map_details tool"""
        map_args = TenderDetailsArgs(michraz_id=20250001)

        with patch(
            "src.remy_mcp.client.israeli_land_api.IsraeliLandAPI.get_tender_map_details"
        ) as mock_map:
            mock_map.return_value = {"coordinates": {"lat": 32.0, "lng": 34.0}}

            map_tool = None
            for tool_name, tool_func in mcp_server._tools.items():
                if "get_tender_map_details" in tool_name:
                    map_tool = tool_func
                    break

            assert map_tool is not None
            result = map_tool(map_args)

            assert result["success"] is True
            assert result["tender_id"] == 20250001
            assert "map_details" in result

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_get_kod_yeshuv_tool(self, mcp_server):
        """Test get_kod_yeshuv settlement lookup tool"""
        kod_args = KodYeshuvArgs(settlement_name="תל אביב")

        kod_tool = None
        for tool_name, tool_func in mcp_server._tools.items():
            if "get_kod_yeshuv" in tool_name:
                kod_tool = tool_func
                break

        assert kod_tool is not None
        result = kod_tool(kod_args)

        # This should work with real settlement data
        assert result["success"] is True
        if result["success"]:
            assert "kod_yeshuv" in result or "partial_matches" in result

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_tender_types_resource(self, mcp_server):
        """Test tender types resource"""
        # Access resources through MCP server
        tender_types_resource = None
        for resource_name, resource_func in mcp_server._resources.items():
            if "tender-types" in resource_name:
                tender_types_resource = resource_func
                break

        assert tender_types_resource is not None
        result = tender_types_resource()

        assert result is not None
        # Should be JSON string
        parsed = json.loads(result)
        assert "tender_types" in parsed
        assert isinstance(parsed["tender_types"], list)
        assert len(parsed["tender_types"]) > 0

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_regions_resource(self, mcp_server):
        """Test regions resource"""
        regions_resource = None
        for resource_name, resource_func in mcp_server._resources.items():
            if "regions" in resource_name:
                regions_resource = resource_func
                break

        assert regions_resource is not None
        result = regions_resource()

        parsed = json.loads(result)
        assert "regions" in parsed
        assert isinstance(parsed["regions"], list)
        # Should have 6 regions
        assert len(parsed["regions"]) == 6

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_land_uses_resource(self, mcp_server):
        """Test land uses resource"""
        land_uses_resource = None
        for resource_name, resource_func in mcp_server._resources.items():
            if "land-uses" in resource_name:
                land_uses_resource = resource_func
                break

        assert land_uses_resource is not None
        result = land_uses_resource()

        parsed = json.loads(result)
        assert "land_uses" in parsed
        assert isinstance(parsed["land_uses"], list)
        assert len(parsed["land_uses"]) > 0

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_tender_statuses_resource(self, mcp_server):
        """Test tender statuses resource"""
        statuses_resource = None
        for resource_name, resource_func in mcp_server._resources.items():
            if "tender-statuses" in resource_name:
                statuses_resource = resource_func
                break

        assert statuses_resource is not None
        result = statuses_resource()

        parsed = json.loads(result)
        assert "tender_statuses" in parsed
        assert isinstance(parsed["tender_statuses"], list)

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_priority_populations_resource(self, mcp_server):
        """Test priority populations resource"""
        populations_resource = None
        for resource_name, resource_func in mcp_server._resources.items():
            if "priority-populations" in resource_name:
                populations_resource = resource_func
                break

        assert populations_resource is not None
        result = populations_resource()

        parsed = json.loads(result)
        assert "priority_populations" in parsed
        assert isinstance(parsed["priority_populations"], list)
        # Should have 15 priority population categories
        assert len(parsed["priority_populations"]) == 15

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_settlements_resource(self, mcp_server):
        """Test settlements resource"""
        settlements_resource = None
        for resource_name, resource_func in mcp_server._resources.items():
            if "settlements" in resource_name:
                settlements_resource = resource_func
                break

        assert settlements_resource is not None
        result = settlements_resource()

        parsed = json.loads(result)
        assert "settlements" in parsed
        assert isinstance(parsed["settlements"], list)
        # Should have many settlements
        assert len(parsed["settlements"]) > 100

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_server_info_resource(self, mcp_server):
        """Test server info resource"""
        server_info_resource = None
        for resource_name, resource_func in mcp_server._resources.items():
            if "server-info" in resource_name:
                server_info_resource = resource_func
                break

        assert server_info_resource is not None
        result = server_info_resource()

        parsed = json.loads(result)
        assert "name" in parsed
        assert "version" in parsed
        assert "capabilities" in parsed
        assert "resources" in parsed
        assert "tools" in parsed
        assert parsed["name"] == "Israeli Land Authority MCP Server"

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_error_handling_in_tools(self, mcp_server):
        """Test error handling in MCP tools"""
        # Test with invalid tender ID
        details_args = TenderDetailsArgs(michraz_id=-1)

        with patch(
            "src.remy_mcp.client.israeli_land_api.IsraeliLandAPI.get_tender_details"
        ) as mock_details:
            mock_details.side_effect = Exception("API Error")

            details_tool = None
            for tool_name, tool_func in mcp_server._tools.items():
                if "get_tender_details" in tool_name:
                    details_tool = tool_func
                    break

            result = details_tool(details_args)

            assert result["success"] is False
            assert "error" in result
            assert result["tender_id"] == -1

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_hebrew_text_in_resources(self, mcp_server):
        """Test that Hebrew text is properly handled in resources"""
        # Test regions resource for Hebrew text
        regions_resource = None
        for resource_name, resource_func in mcp_server._resources.items():
            if "regions" in resource_name:
                regions_resource = resource_func
                break

        result = regions_resource()
        parsed = json.loads(result)

        # Find a region with Hebrew text
        found_hebrew = False
        for region in parsed["regions"]:
            if "name_hebrew" in region:
                hebrew_name = region["name_hebrew"]
                # Should be able to encode Hebrew text
                hebrew_name.encode("utf-8")
                found_hebrew = True
                break

        assert found_hebrew, "Should have Hebrew text in regions"

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_comprehensive_tool_integration(self, mcp_server, rate_limiter):
        """Test comprehensive integration of multiple tools"""
        rate_limiter()

        # Complex search
        search_args = SearchTendersArgs(
            tender_types=[1, 2],
            regions=[4],  # Tel Aviv
            active_only=True,
            max_results=3,
            priority_populations=[1, 3],  # Disabled and housing-deprived
        )

        with patch(
            "src.remy_mcp.client.israeli_land_api.IsraeliLandAPI.search_tenders"
        ) as mock_search:
            mock_search.return_value = [{"MichrazID": 20250001, "StatusMichraz": 1}]

            search_tool = None
            for tool_name, tool_func in mcp_server._tools.items():
                if "search_tenders" in tool_name:
                    search_tool = tool_func
                    break

            result = search_tool(search_args)

            assert result["success"] is True
            summary = result["search_summary"]
            assert summary["new_features"]["priority_populations"] is True
            assert summary["new_features"]["multiple_regions"] is True

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_resource_data_consistency(self, mcp_server):
        """Test that resource data is consistent and properly formatted"""
        resources_to_test = [
            "tender-types",
            "regions",
            "land-uses",
            "tender-statuses",
            "priority-populations",
        ]

        for resource_name in resources_to_test:
            resource_func = None
            for name, func in mcp_server._resources.items():
                if resource_name in name:
                    resource_func = func
                    break

            assert resource_func is not None, f"Resource {resource_name} not found"

            result = resource_func()
            assert result is not None

            # Should be valid JSON
            parsed = json.loads(result)
            assert isinstance(parsed, dict)

            # Should have a main data key
            data_keys = list(parsed.keys())
            assert len(data_keys) >= 1

            # Main data should be a list
            main_data = list(parsed.values())[0]
            assert isinstance(main_data, list)
