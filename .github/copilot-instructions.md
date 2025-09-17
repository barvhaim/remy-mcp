# Israeli Land Authority MCP Server

**Always reference these instructions first and fall back to search or bash commands only when you encounter unexpected information that does not match the info here.**

The Israeli Land Authority MCP Server is a Python-based Model Context Protocol (MCP) server that provides programmatic access to Israeli Land Authority (רמ״י) public tender data. The project enables applications to search, monitor, and analyze land tenders from Israel's government APIs.

## Working Effectively

### Bootstrap and Setup
- Install uv package manager: `pip install uv`
- Install dependencies: `uv sync` - takes 30-60 seconds depending on network
- Validate installation: `uv run python scripts/run_tests.py validate` - completes in <1 second

### Development Commands
- Format code: `uv run black .` - completes in <1 second
- Run the MCP server: `uv run python main.py` (server starts immediately and displays branded interface)
- Test core functionality: `uv run python scripts/run_tests.py smoke` - completes in ~1 second

### Testing (NEVER CANCEL - Wait for completion)
- Basic validation: `uv run python scripts/run_tests.py validate` - 0.2 seconds
- Smoke tests: `uv run python scripts/run_tests.py smoke` - 1.2 seconds. NEVER CANCEL.
- MCP server tests: `uv run python scripts/run_tests.py mcp` - 1.6 seconds. NEVER CANCEL.
- API tests (offline/mock): `uv run python scripts/run_tests.py api --skip-slow` - 100 seconds (1m40s). NEVER CANCEL. Set timeout to 180+ seconds.
- E2E tests (offline): `uv run python scripts/run_tests.py e2e --skip-slow` - 100 seconds (1m40s). NEVER CANCEL. Set timeout to 180+ seconds.
- Performance tests: `uv run python scripts/run_tests.py performance` - skipped when API unavailable

### Key Technical Details
- **No Build Step**: This is a Python package, no compilation required
- **Python Version**: Requires Python 3.11+
- **Package Manager**: uv (preferred) or pip
- **MCP Framework**: Uses FastMCP 2.10.5
- **Main Entry Point**: `main.py` (the console script `uv run remy-mcp` has import issues)

## Validation Scenarios

### Basic Functionality Test
Always run this manual validation after making changes:

```bash
uv run python -c "
from src.remy_mcp.client.israeli_land_api import IsraeliLandAPI
from src.remy_mcp.server import create_server
import src.remy_mcp.models as models

# Test imports and instantiation
api = IsraeliLandAPI()
print(f'✓ API client created with rate limit: {api.rate_limit_delay}s')

server = create_server()
print(f'✓ MCP server created: {type(server)}')

# Test reference data
print(f'✓ Tender types: {len(models.TENDER_TYPES)}')
print(f'✓ Regions: {len(models.REGIONS)}')
print(f'✓ Land uses: {len(models.LAND_USES)}')
print('✓ All core components work correctly')
"
```

### MCP Server Startup Test
```bash
# Test server startup (should show branded interface)
timeout 10 uv run python main.py
# Expected: FastMCP 2.0 branded startup screen with "Israeli Land Authority" server name
```

### Test Environment Validation
```bash
# Always run before making changes
uv run python scripts/run_tests.py validate
# Expected: Python version, UV version, package importable, API availability check
```

## Project Structure

### Key Directories
- `src/remy_mcp/` - Main source code
  - `client/` - API client for Israeli Land Authority APIs
  - `models/` - Pydantic data models and reference data
  - `tools/` - MCP tools (dynamic operations)
  - `resources/` - MCP resources (static data)
  - `server.py` - Main MCP server entry point
- `tests/` - Comprehensive test suite (56 tests)
- `examples/` - Usage examples
- `scripts/` - Test runner and utilities

### Important Files
- `main.py` - Server entry point (WORKING)
- `pyproject.toml` - Project configuration and dependencies
- `pytest.ini` - Test configuration with markers
- `scripts/run_tests.py` - Comprehensive test runner

### Core Components
- **7 MCP Tools**: search_tenders, get_tender_details, get_active_tenders, search_by_type, get_recent_results, get_tender_map_details, get_kod_yeshuv
- **7 MCP Resources**: tender-types, regions, land-uses, tender-statuses, priority-populations, settlements, server-info
- **9 Tender Types**: Regular public to lottery-based
- **6 Regions**: Jerusalem, Tel Aviv, Haifa, etc.
- **9 Land Uses**: Residential to mining

## Common Issues and Workarounds

### Known Issues
- Console script `uv run remy-mcp` fails with "ModuleNotFoundError: No module named 'src'" - use `uv run python main.py` instead
- Some tests require pytest-asyncio plugin but it's not installed in dev dependencies
- API tests fail when external Israeli Land Authority API is not accessible (expected in CI/isolated environments)

### Test Failures (Expected)
- API integration tests fail without network access - this is normal
- Some MCP server tests have FastMCP API compatibility issues but basic functionality works
- Performance tests are skipped when API is unavailable

## External Dependencies

### Israeli Land Authority API
- **Base URL**: https://apps.land.gov.il/MichrazimSite/api
- **Required Headers**: User-Agent: 'datagov-external-client'
- **Rate Limiting**: 1-second delay between requests (configurable)
- **Encoding**: UTF-8 for Hebrew text support

### Critical Validation Steps
1. Always run `uv run python scripts/run_tests.py validate` first
2. Always test basic functionality with the manual validation script above
3. Always run `uv run black .` before committing (takes <1 second)
4. Always test MCP server startup with `timeout 10 uv run python main.py`

### Common Tasks Quick Reference

```bash
# Setup from scratch
pip install uv
uv sync
uv run python scripts/run_tests.py validate

# Development workflow
uv run black .                    # Format (0.8s)
uv run python main.py             # Test server startup
uv run python scripts/run_tests.py smoke  # Basic tests (1.2s)

# Before committing
uv run black .
uv run python scripts/run_tests.py validate
uv run python scripts/run_tests.py smoke

# Full test suite (when API available)
uv run python scripts/run_tests.py mcp     # 1.6s
uv run python scripts/run_tests.py api     # 100s - NEVER CANCEL
uv run python scripts/run_tests.py e2e     # 100s - NEVER CANCEL
```

### Integration with Claude Desktop
Users can integrate this server with Claude Desktop by adding the server configuration to their MCP settings. The server provides direct access to Israeli Land Authority tender data through the MCP protocol.

Always validate your changes work by running the manual functionality test and ensuring the MCP server starts correctly with its branded interface.