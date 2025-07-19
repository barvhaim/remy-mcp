"""
Example usage of the Israeli Land Authority MCP Server
"""

from israeli_land_api import IsraeliLandAPI
from models import TENDER_TYPES, REGIONS, LAND_USES


def demonstrate_api_client():
    """Demonstrate the API client functionality"""
    print("Israeli Land Authority API Client Demo")
    print("=" * 40)

    # Initialize client
    api = IsraeliLandAPI()

    print("\n1. Reference Data:")
    print("Tender Types:")
    for tender_type in TENDER_TYPES[:3]:  # Show first 3
        print(f"  {tender_type.id}: {tender_type.name_english}")

    print("\nRegions:")
    for region in REGIONS:
        print(f"  {region.id}: {region.name_english}")

    print("\nLand Uses:")
    for land_use in LAND_USES[:3]:  # Show first 3
        print(f"  {land_use.id}: {land_use.name_english}")

    print("\n2. API Usage Examples:")
    print("To search for active tenders:")
    print("  results = api.search_tenders(active_only=True)")

    print("\nTo search by location:")
    print("  results = api.search_by_location(region='תל אביב')")

    print("\nTo get tender details:")
    print("  details = api.get_tender_details(michraz_id=20250001)")

    print("\n3. MCP Server Functions Available:")
    functions = [
        "search_tenders - Comprehensive tender search",
        "get_tender_details - Detailed tender information",
        "get_active_tenders - Currently active tenders",
        "search_by_location - Location-based searches",
        "search_by_type - Type and purpose searches",
        "get_recent_results - Recent tender results",
        "get_tender_map_details - Geographic data",
        "get_tender_types - Reference data for types",
        "get_regions - Reference data for regions",
        "get_land_uses - Reference data for land uses",
        "get_server_info - Server information",
    ]

    for func in functions:
        print(f"  • {func}")

    print(f"\n4. Rate Limiting:")
    print(f"  • Default delay: {api.rate_limit_delay} seconds between requests")
    print(f"  • Retry strategy: 3 attempts with backoff")
    print(f"  • Session configured with required headers")

    print("\n5. Data Format:")
    print("  • Hebrew text in UTF-8 encoding")
    print("  • Dates in Israeli timezone (UTC+3)")
    print("  • All responses include success/error status")
    print("  • Structured Pydantic models for type safety")


def show_mcp_server_info():
    """Show information about running the MCP server"""
    print("\n" + "=" * 40)
    print("MCP Server Usage")
    print("=" * 40)

    print("\nTo start the MCP server:")
    print("  python main.py")

    print("\nThe server provides Model Context Protocol access to:")
    print("  • Israeli Land Authority (רמ״י) public tender data")
    print("  • Comprehensive search and filtering capabilities")
    print("  • Real-time access to active tenders")
    print("  • Historical data and results")
    print("  • Geographic and mapping information")

    print("\nConnect via MCP client using:")
    print("  Server transport: python main.py")
    print("  Working directory: /path/to/remy-mcp")


if __name__ == "__main__":
    demonstrate_api_client()
    show_mcp_server_info()
