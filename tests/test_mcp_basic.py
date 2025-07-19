"""
Basic MCP server tests - simplified version for initial validation
"""

import pytest
import asyncio


class TestMCPBasic:
    """Basic tests for MCP server creation and structure"""

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_server_creation(self, mcp_server):
        """Test MCP server can be created successfully"""
        assert mcp_server is not None
        assert mcp_server.name == "Israeli Land Authority"

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_server_has_tools(self, mcp_server):
        """Test server has registered tools"""
        # Run async method in event loop
        async def check_tools():
            tools = await mcp_server.get_tools()
            return tools
        
        tools = asyncio.run(check_tools())
        assert isinstance(tools, dict)
        assert len(tools) > 0
        
        # Check for expected tools
        tool_names = list(tools.keys())
        expected_tools = [
            "search_tenders",
            "get_tender_details", 
            "get_active_tenders",
            "search_by_location",
            "search_by_type",
            "get_recent_results",
            "get_tender_map_details",
            "get_kod_yeshuv"
        ]
        
        found_tools = []
        for expected in expected_tools:
            for tool_name in tool_names:
                if expected in tool_name:
                    found_tools.append(expected)
                    break
        
        assert len(found_tools) >= 6, f"Expected at least 6 tools, found: {found_tools}"

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_server_has_resources(self, mcp_server):
        """Test server has registered resources"""
        # Run async method in event loop
        async def check_resources():
            resources = await mcp_server.get_resources()
            return resources
        
        resources = asyncio.run(check_resources())
        assert isinstance(resources, dict)
        assert len(resources) > 0
        
        # Check for expected resources
        resource_names = list(resources.keys())
        expected_resources = [
            "tender-types",
            "regions", 
            "land-uses",
            "tender-statuses",
            "priority-populations",
            "settlements"
        ]
        
        found_resources = []
        for expected in expected_resources:
            for resource_name in resource_names:
                if expected in resource_name:
                    found_resources.append(expected)
                    break
        
        assert len(found_resources) >= 4, f"Expected at least 4 resources, found: {found_resources}"

    @pytest.mark.e2e
    @pytest.mark.mcp
    def test_tool_structure(self, mcp_server):
        """Test tools have proper structure"""
        async def check_tool_structure():
            tools = await mcp_server.get_tools()
            if not tools:
                return False
                
            # Check first tool structure
            first_tool = next(iter(tools.values()))
            return hasattr(first_tool, 'name') and hasattr(first_tool, 'description')
        
        has_structure = asyncio.run(check_tool_structure())
        assert has_structure, "Tools should have name and description attributes"

    @pytest.mark.e2e  
    @pytest.mark.mcp
    def test_resource_structure(self, mcp_server):
        """Test resources have proper structure"""
        async def check_resource_structure():
            resources = await mcp_server.get_resources()
            if not resources:
                return False
                
            # Check first resource structure  
            first_resource = next(iter(resources.values()))
            return hasattr(first_resource, 'uri')
        
        has_structure = asyncio.run(check_resource_structure())
        assert has_structure, "Resources should have uri attribute"