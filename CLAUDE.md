# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**remy-mcp** is a Model Context Protocol (MCP) server that provides programmatic access to Israeli Land Authority public tender data. The project enables applications to search, monitor, and analyze land tenders from Israel's government APIs.

## Development Environment

### Python Environment
- **Python Version**: 3.11+ (specified in pyproject.toml)
- **Package Manager**: `uv` (preferred over pip)
- **Virtual Environment**: Managed by uv

### Dependencies
- **fastmcp**: MCP server framework (≥2.10.5)
- **requests**: HTTP client for API calls (≥2.32.4)
- **pydantic**: Data validation and models (≥2.11.7)
- **black**: Code formatting (≥25.1.0)

### Common Commands

```bash
# Install dependencies
uv sync

# Format code
uv run black .

# Run the application
uv run python main.py
# or
uv run remy-mcp

# Install new dependency
uv add package-name

# Run tests
uv run pytest
```

## Code Architecture

### Project Structure
```
src/remy_mcp/
├── __init__.py                 # Package metadata
├── server.py                   # Main server entry point
├── client/                     # API client layer
│   ├── __init__.py
│   └── israeli_land_api.py     # HTTP client for Israeli Land Authority APIs
├── models/                     # Data models
│   ├── __init__.py
│   ├── tender_models.py        # Core tender data models
│   ├── reference_models.py     # Reference data (types, regions, etc.)
│   └── arg_models.py          # MCP function argument models
├── tools/                      # MCP tools (dynamic operations)
│   ├── __init__.py
│   ├── tender_tools.py         # Tender search and details tools
│   └── settlement_tools.py     # Settlement lookup tools
├── resources/                  # MCP resources (static data)
│   ├── __init__.py
│   ├── reference_resources.py  # Reference data resources
│   └── server_resources.py     # Server info resources
└── utils/                      # Utility functions
    ├── __init__.py
    └── settlement_utils.py     # Settlement conversion utilities

examples/                       # Usage examples
tests/                         # Test suite
├── unit/                      # Unit tests
└── integration/               # Integration tests
docs/                          # API documentation
data/                          # Reference data
```

### Architecture Components

1. **Server Layer** (`server.py`): FastMCP server initialization and configuration
2. **API Client Layer** (`client/`): HTTP client for Israeli Land Authority APIs
3. **Data Models** (`models/`): Pydantic models for validation and type safety
4. **MCP Tools** (`tools/`): Dynamic operations exposed as MCP tools
5. **MCP Resources** (`resources/`): Static reference data exposed as MCP resources
6. **Utilities** (`utils/`): Helper functions and data conversions

## Israeli Land Authority API

### Base Configuration
- **Base URL**: `https://apps.land.gov.il/MichrazimSite/api`
- **Required Headers**:
  ```python
  headers = {
      'User-Agent': 'datagov-external-client',
      'Content-Type': 'application/json',
      'Origin': 'https://apps.land.gov.il',
      'Referer': 'https://apps.land.gov.il/MichrazimSite/'
  }
  ```

### Key Endpoints
1. **Search**: `POST /SearchApi/Search` - Search all tenders
2. **Details**: `GET /MichrazDetailsApi/Get?michrazID={id}` - Get tender details
3. **Map Details**: `GET /MichrazDetailsApi/GetMichrazMapaDetails?michrazID={id}` - Geographic data

### Core MCP Functions to Implement
- `search_tenders()`: Comprehensive tender search with filters
- `get_tender_details()`: Detailed tender information
- `get_active_tenders()`: Currently active tenders only
- `get_recent_results()`: Recent tender outcomes
- `search_by_location()`: Geographic-based searches
- `search_by_type()`: Type-specific tender searches

## Data Considerations

### Hebrew Text Handling
- All API responses include Hebrew text in UTF-8 encoding
- Field names and values use Hebrew terminology
- Dates are in Israeli timezone (UTC+3)

### Rate Limiting
- Unknown rate limits - implement conservative delays between requests
- Cache reference data (regions, tender types, land uses)
- Consider implementing request queuing

### API Limitations
- **No Server-Side Pagination**: The API ignores pageSize and pageNumber parameters
- **Client-Side Pagination**: Our implementation retrieves all results then slices them
- **Performance Impact**: Large searches may be slow due to full result retrieval

### Data Types
- **Tender Types**: 9 categories from regular public to lottery-based
- **Regions**: 6 geographical divisions (Jerusalem, Tel Aviv, Haifa, etc.)
- **Land Uses**: 9 categories from residential to mining
- **Statuses**: Published, Cancelled, Winners Not Yet Announced

## Development Guidelines

### Code Style
- Use `uv run black .` for formatting
- Follow FastMCP patterns for MCP server implementation
- Proper error handling implemented for API failures
- Pydantic models used for data validation and type safety

### Testing and Validation
```bash
# Format code
uv run black .

# Test basic functionality
python example_usage.py

# Run the MCP server
python main.py
```

### Implementation Status
✅ **Completed Implementation**:
1. ✅ API client with all endpoints (`israeli_land_api.py`)
2. ✅ Comprehensive Pydantic data models (`models.py`)
3. ✅ Full FastMCP server with 11 functions (`mcp_server.py`)
4. ✅ Rate limiting and error handling
5. ✅ Reference data for types, regions, land uses
6. ✅ Hebrew text support and timezone handling
7. ✅ Complete documentation and examples

### MCP Server Functions

**Tools (Dynamic Operations):**
- `search_tenders` - Comprehensive search with filtering
- `get_tender_details` - Detailed tender information
- `get_active_tenders` - Currently active tenders
- `search_by_type` - Type/purpose searches
- `get_recent_results` - Recent tender outcomes
- `get_tender_map_details` - Geographic mapping data
- `get_kod_yeshuv` - Convert settlement name to code (with fuzzy matching)

**Resources (Static Reference Data):**
- `remy://tender-types` - All tender types reference data
- `remy://regions` - All Israeli regions reference data
- `remy://land-uses` - All land use categories reference data
- `remy://tender-statuses` - All tender status types reference data
- `remy://priority-populations` - All priority population codes reference data
- `remy://settlements` - All settlements with Kod Yeshuv codes
- `remy://server-info` - Server capabilities and metadata

## Production Ready

The MCP server is fully implemented and ready for use:
- Complete API client with rate limiting
- Structured error handling and logging
- Hebrew text encoding support
- Israeli timezone (UTC+3) handling
- Type-safe Pydantic models
- Comprehensive documentation
- Example usage and testing scripts