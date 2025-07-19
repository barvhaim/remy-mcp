"""
Server information resources
"""

import json


def register_server_resources(mcp):
    """Register server information resources"""

    @mcp.resource("remy://server-info")
    def get_server_info_resource() -> str:
        """
        Get information about the MCP server and its capabilities as a resource

        Returns server metadata, available functions, and usage guidelines.
        """
        server_info = {
            "name": "Israeli Land Authority MCP Server",
            "description": "Provides access to רמ״י (Israeli Land Authority) public tender data",
            "version": "1.0.0",
            "capabilities": [
                "Search land tenders with comprehensive filtering",
                "Get detailed tender information",
                "Location-based searches",
                "Type and purpose-based searches",
                "Recent results monitoring",
                "Geographic mapping data",
                "Reference data via resources for types, regions, and land uses",
            ],
            "resources": [
                "remy://tender-types - All tender types reference data",
                "remy://regions - All Israeli regions reference data",
                "remy://land-uses - All land use categories reference data",
                "remy://tender-statuses - All tender status types reference data",
                "remy://priority-populations - All priority population codes reference data",
                "remy://settlements - All settlements with Kod Yeshuv codes",
                "remy://server-info - Server capabilities and metadata",
            ],
            "tools": [
                "search_tenders - Dynamic tender search with filtering",
                "get_tender_details - Get specific tender details",
                "get_active_tenders - Get currently active tenders",
                "search_by_type - Search by tender type or purpose",
                "get_recent_results - Get recent tender results",
                "get_tender_map_details - Get geographic mapping data",
                "get_kod_yeshuv - Convert settlement name to code (with fuzzy matching)",
            ],
            "data_source": "Israeli Land Authority (apps.land.gov.il)",
            "language_support": "Hebrew and English",
            "rate_limiting": "Implemented with 1-second delays",
            "notes": [
                "Hebrew text is supported for settlement and neighborhood searches",
                "Dates are in Israeli timezone (UTC+3)",
                "Some fields may be null depending on tender status",
                "API returns maximum 10,000 results per request",
                "Static reference data is now available as resources for better performance",
            ],
        }
        return json.dumps(server_info, ensure_ascii=False, indent=2)
