# Israeli Land Authority MCP Server - Test Suite

This directory contains comprehensive end-to-end (E2E) tests for the Israeli Land Authority MCP Server. The test suite validates API functionality, MCP protocol implementation, performance characteristics, and error handling.

## Test Structure

### Test Categories

- **Unit Tests**: Fast tests with no external dependencies (marked with `@pytest.mark.unit`)
- **API Tests**: Integration tests that require API access (marked with `@pytest.mark.api`)
- **MCP Tests**: Tests for MCP server functionality (marked with `@pytest.mark.mcp`)
- **Performance Tests**: Load and timing tests (marked with `@pytest.mark.performance`)
- **E2E Tests**: Full end-to-end integration tests (marked with `@pytest.mark.e2e`)
- **Slow Tests**: Long-running tests (marked with `@pytest.mark.slow`)

### Test Files

- `test_api_client_e2e.py` - API client functionality and integration
- `test_mcp_server_e2e.py` - MCP protocol and server testing
- `test_performance_e2e.py` - Performance and load testing
- `conftest.py` - Test fixtures and configuration
- `utils.py` - Test utilities and helpers

## Running Tests

### Prerequisites

```bash
# Install dependencies
uv sync

# Ensure Python 3.11+ is installed
python --version
```

### Using the Test Runner

The project includes a comprehensive test runner script:

```bash
# Run all available test types
python scripts/run_tests.py validate    # Validate environment
python scripts/run_tests.py unit        # Fast unit tests
python scripts/run_tests.py api         # API integration tests
python scripts/run_tests.py mcp         # MCP server tests
python scripts/run_tests.py performance # Performance tests
python scripts/run_tests.py e2e         # All E2E tests
python scripts/run_tests.py smoke       # Quick smoke tests
python scripts/run_tests.py coverage    # Tests with coverage report
```

### Command Line Options

```bash
# Skip slow tests
python scripts/run_tests.py e2e --skip-slow

# Enable verbose output
python scripts/run_tests.py api --verbose
```

### Direct pytest Usage

```bash
# Run specific test categories
uv run pytest -m "unit"
uv run pytest -m "api and not slow"
uv run pytest -m "e2e"

# Run specific test files
uv run pytest tests/test_api_client_e2e.py
uv run pytest tests/test_mcp_server_e2e.py -v

# Run with coverage
uv run pytest --cov=src/remy_mcp --cov-report=html

# Run specific tests
uv run pytest -k "test_search_tenders_basic"
```

## Test Configuration

### Environment Setup

Tests automatically detect and adapt to the environment:

- **API Available**: Full tests run against live Israeli Land Authority API
- **API Unavailable**: Tests use mock data or are skipped appropriately
- **Rate Limiting**: Automatic delays prevent overwhelming the API

### Configuration Options

The test framework supports several configuration options via `tests/utils.py`:

```python
# Test configuration
{
    "api_timeout": 30,           # API request timeout
    "rate_limit_delay": 1.0,     # Delay between API calls  
    "max_retries": 3,            # Maximum retry attempts
    "skip_slow_tests": False,    # Skip long-running tests
    "use_mock_data": False,      # Use mock instead of real API
    "test_data_cache_ttl": 300   # Cache TTL in seconds
}
```

## Test Features

### API Testing

- **Basic Functionality**: Search, details, and map endpoints
- **Parameter Validation**: Complex search filters and date ranges
- **Settlement Conversion**: Hebrew name to kod_yeshuv conversion
- **Hebrew Text Handling**: UTF-8 encoding validation
- **Error Recovery**: API failure handling and recovery
- **Pagination**: Multi-page result testing

### MCP Protocol Testing

- **Tool Functionality**: All 11 MCP tools tested
- **Resource Access**: 7 MCP resources validated
- **Data Structure**: Response format validation
- **Error Handling**: Tool error scenarios
- **Integration**: Complex multi-tool workflows

### Performance Testing

- **Response Times**: API latency monitoring
- **Rate Limiting**: Enforcement verification
- **Concurrent Requests**: Thread-safe operation
- **Large Result Sets**: Memory and performance with big data
- **Sustained Load**: Long-running stability testing
- **Memory Usage**: Memory leak detection

### Data Validation

- **Structure Validation**: Required fields and data types
- **Hebrew Text**: Encoding/decoding verification
- **Date Formats**: Israeli timezone handling
- **Reference Data**: Consistency checks
- **Settlement Data**: Kod Yeshuv validation

## Test Utilities

### Fixtures (`conftest.py`)

- `api_client`: Pre-configured API client with rate limiting
- `mcp_server`: MCP server instance for testing
- `rate_limiter`: Automatic API rate limiting
- `test_data_validator`: Data structure validation helpers

### Helper Classes (`utils.py`)

- `APITestHelper`: API testing utilities and sample data
- `DataValidator`: Response structure and content validation
- `PerformanceTracker`: Performance metrics collection
- `MockDataGenerator`: Mock data for offline testing
- `TestConfigManager`: Test configuration and caching

### Decorators

- `@requires_api_access`: Skip tests when API unavailable
- `@skip_if_slow`: Skip long-running tests when configured

## Interpreting Results

### Success Indicators

```bash
✓ API is available
✓ Package importable
✓ All tests passed
✓ Coverage report generated in htmlcov/index.html
```

### Common Warnings

```bash
⚠ API not available - some tests may be skipped
⚠ Slow tests disabled
⚠ Using mock data instead of live API
```

### Performance Metrics

The test suite tracks and validates:

- Average response time < 10 seconds
- Maximum response time < 30 seconds
- Error rate < 10% under load
- Memory usage increase < 100MB
- Rate limiting enforcement (minimum delays)

## Continuous Integration

### GitHub Actions Integration

The test suite is designed for CI/CD integration:

```yaml
# Example GitHub Actions step
- name: Run E2E Tests
  run: |
    python scripts/run_tests.py validate
    python scripts/run_tests.py unit
    python scripts/run_tests.py api --skip-slow
    python scripts/run_tests.py mcp
```

### Test Strategies by Environment

- **Local Development**: Full test suite with live API
- **Pull Requests**: Unit, API (without slow), and MCP tests
- **Main Branch**: Full test suite including performance tests
- **Production**: Smoke tests and basic validation

## Troubleshooting

### Common Issues

1. **API Rate Limiting**: Tests include automatic delays
2. **Hebrew Text Encoding**: Tests validate UTF-8 handling
3. **Network Timeouts**: Configurable timeout settings
4. **Memory Usage**: Performance tests monitor memory consumption

### Debug Mode

```bash
# Run with detailed logging
uv run pytest -s -v --log-cli-level=DEBUG

# Run single test for debugging
uv run pytest tests/test_api_client_e2e.py::TestAPIClientE2E::test_search_tenders_basic -s -v
```

### Mock Data Testing

When the API is unavailable, tests automatically use mock data:

```bash
# Force mock data usage
export REMY_USE_MOCK_DATA=true
python scripts/run_tests.py api
```

## Coverage Reports

HTML coverage reports are generated in `htmlcov/`:

```bash
python scripts/run_tests.py coverage
open htmlcov/index.html  # View coverage report
```

## Contributing

When adding new tests:

1. Use appropriate markers (`@pytest.mark.e2e`, `@pytest.mark.api`, etc.)
2. Include rate limiting for API tests
3. Add data validation for responses
4. Use fixtures for common setup
5. Include error scenarios
6. Document expected behavior

Example test:

```python
@pytest.mark.e2e
@pytest.mark.api
@requires_api_access
def test_new_functionality(self, api_client, rate_limiter):
    """Test description"""
    rate_limiter()
    
    result = api_client.new_method()
    assert result is not None
    # Add validation logic
```