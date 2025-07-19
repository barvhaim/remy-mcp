"""
Main MCP Server entry point for Israeli Land Authority data
"""

from fastmcp import FastMCP
from .client.israeli_land_api import IsraeliLandAPI
from .tools import register_tools
from .resources import register_resources


def create_server() -> FastMCP:
    """Create and configure the MCP server"""
    # Initialize MCP server
    mcp = FastMCP("Israeli Land Authority")

    # Initialize API client
    api_client = IsraeliLandAPI()

    # Register tools and resources
    register_tools(mcp, api_client)
    register_resources(mcp)

    return mcp


def main():
    """Main entry point"""
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
