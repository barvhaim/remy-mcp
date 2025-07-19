"""
MCP Resources for Israeli Land Authority server
"""

from .reference_resources import register_reference_resources
from .server_resources import register_server_resources


def register_resources(mcp):
    """Register all MCP resources"""
    register_reference_resources(mcp)
    register_server_resources(mcp)
