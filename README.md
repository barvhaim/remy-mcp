# Israeli Land Authority (רמ״י) Unofficial MCP Server

[![Buy Me A Coffee](https://img.shields.io/badge/-Buy%20me%20a%20coffee-%23FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/barha)

A Model Context Protocol (MCP) server that provides programmatic access to Israeli Land Authority (רמ״י) public tender data.

## Features

- **Comprehensive Search**: Advanced filtering by type, location, status, and dates
- **Real-time Data**: Direct access to live government APIs
- **Hebrew Support**: Full Unicode support for Hebrew text and settlement names
- **MCP Protocol**: Optimized with tools for dynamic operations and resources for static data
- **Type Safety**: Full Pydantic model validation
- **Rate Limiting**: Built-in request throttling and retry logic

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd remy-mcp

# Install dependencies
uv sync
```

### Claude Desktop Integration

To add this server to Claude Desktop, update your MCP servers configuration:

**Configuration file location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

**Add this configuration:**
```json
{
  "mcpServers": {
    "israeli-land-authority": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/remy-mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

*Replace `/path/to/remy-mcp` with the actual path to your cloned repository.*

After adding the configuration and restarting Claude Desktop, you'll have access to all Israeli Land Authority functions directly within your conversations.

## Available Functions

### Tools (Dynamic Operations)
- **`search_tenders`** - Comprehensive search with filtering
- **`get_tender_details`** - Detailed tender information
- **`get_active_tenders`** - Currently active tenders
- **`search_by_type`** - Type/purpose searches
- **`get_recent_results`** - Recent tender outcomes
- **`get_tender_map_details`** - Geographic mapping data
- **`get_kod_yeshuv`** - Convert settlement name to code

### Resources (Static Reference Data)
- **`remy://tender-types`** - All tender types
- **`remy://regions`** - Israeli regions
- **`remy://land-uses`** - Land use categories
- **`remy://tender-statuses`** - Tender statuses
- **`remy://priority-populations`** - Priority population codes
- **`remy://settlements`** - All settlements with codes
- **`remy://server-info`** - Server capabilities

## Technical Details

### API Configuration
- **Base URL**: `https://apps.land.gov.il/MichrazimSite/api`
- **Rate Limiting**: 1-second delay between requests
- **Encoding**: UTF-8 for Hebrew text support

### Dependencies
- **Python**: 3.11+
- **FastMCP**: MCP server framework
- **Pydantic**: Data validation and modeling
- **Requests**: HTTP client with retry logic

### Data Handling
- Hebrew text in UTF-8 encoding
- Israeli timezone (UTC+3) for dates
- Structured responses with error handling
- Type-safe Pydantic models

## Development

### Code Formatting
```bash
uv run black .
```

### Testing
```bash
python example_usage.py
```

### Project Structure
```
src/remy_mcp/
├── server.py              # Main server entry point
├── client/                # API client layer
├── models/                # Data models and validation
├── tools/                 # MCP tools (dynamic operations)
├── resources/             # MCP resources (static data)
└── utils/                 # Helper utilities

examples/                  # Usage examples
tests/                    # Test suite
docs/                     # API documentation
data/                     # Reference data
```

## Data Source

This server accesses public data from the Israeli Land Authority (רשות מקרקעי ישראל) via their official APIs. All data is publicly available and no authentication is required.

**Official Website**: https://apps.land.gov.il/MichrazimSite/

## License

This project provides access to public government data for research and analysis purposes.
