# Israeli Land Authority MCP Server (רמ״י)

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

# Run the MCP server
uv run python main.py
# or
uv run remy-mcp
```

### Connect via MCP Client

Use any MCP-compatible client to connect:

```
Server transport: python main.py
Working directory: /path/to/remy-mcp
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

## Data Categories

### Tender Types (סוגי מכרזים)
1. **Regular Public Tender** (מכרז ציבורי רגיל)
2. **Target Price** (מחיר יעד)
3. **Reduced Price Housing** (דיור במחיר למשתכן)
4. **Initiative Tender** (מכרז יוזמה)
5. **Unspecified Plot Tender** (מכרז למגרש לא מיועד)
6. **Registration and Lottery** (רישום והגרלה)
7. **Rental Housing** (דיור להשכרה)
8. **Amidar Tenders** (מכרזי עמידר)
9. **Acre Development Company Tenders** (מכרזי חברת פיתוח עכו)

### Regions (אזורי ישראל)
- **Jerusalem** (ירושלים)
- **Tel Aviv** (תל אביב)
- **Haifa** (חיפה)
- **Center** (מרכז)
- **South** (דרום)
- **Judea and Samaria** (יהודה ושומרון)

### Land Use Types (ייעודי קרקע)
- Low-rise/Ground-attached Construction
- High-density Construction
- Commerce and/or Offices
- Hotels, Sports, Recreation, Tourism
- Residential mixed-use
- Mining and Quarrying
- Other categories

## Usage Examples

### Search Active Tenders
```python
# Via API client
from israeli_land_api import IsraeliLandAPI
api = IsraeliLandAPI()
results = api.search_tenders(active_only=True, max_results=50)
```

### Location-Based Search
```python
# Search tenders in Tel Aviv region
results = api.search_by_location(region="תל אביב")
```

### Get Tender Details
```python
# Get detailed information for a specific tender
details = api.get_tender_details(michraz_id=20250001)
```

## Technical Details

### API Configuration
- **Base URL**: `https://apps.land.gov.il/MichrazimSite/api`
- **Required Headers**: `User-Agent: datagov-external-client`
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