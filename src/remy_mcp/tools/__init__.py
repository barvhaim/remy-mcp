"""
MCP Tools for Israeli Land Authority server
"""

from .tender_tools import register_tender_tools
from .settlement_tools import register_settlement_tools


def register_tools(mcp, api_client):
    """Register all MCP tools"""
    register_tender_tools(mcp, api_client)
    register_settlement_tools(mcp, api_client)
