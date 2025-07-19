#!/usr/bin/env python3
"""
Test runner script for Israeli Land Authority MCP Server
Provides different test execution profiles and utilities
"""

import sys
import subprocess
import argparse
import time
from pathlib import Path
from typing import List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.utils import APITestHelper, test_config


class TestRunner:
    """Test runner with different execution profiles"""
    
    def __init__(self):
        self.project_root = project_root
        
    def run_command(self, cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run a command and return the result"""
        print(f"Running: {' '.join(cmd)}")
        return subprocess.run(cmd, cwd=self.project_root, check=check)
    
    def check_api_availability(self) -> bool:
        """Check if the API is available"""
        print("Checking API availability...")
        try:
            helper = APITestHelper()
            available = helper.is_api_available()
            if available:
                print("✓ API is available")
            else:
                print("✗ API is not available")
            return available
        except Exception as e:
            print(f"✗ Error checking API: {e}")
            return False
    
    def run_unit_tests(self) -> int:
        """Run fast unit tests only"""
        print("\n=== Running Unit Tests ===")
        cmd = [
            "uv", "run", "pytest", 
            "-m", "unit",
            "--tb=short",
            "-v"
        ]
        try:
            result = self.run_command(cmd, check=False)
            return result.returncode
        except Exception as e:
            print(f"Error running unit tests: {e}")
            return 1
    
    def run_api_tests(self, skip_slow: bool = False) -> int:
        """Run API integration tests"""
        print("\n=== Running API Tests ===")
        
        if not self.check_api_availability():
            print("API not available, using mock data")
            test_config.set_config("use_mock_data", True)
        
        markers = ["api"]
        if skip_slow:
            markers.append("not slow")
            test_config.set_config("skip_slow_tests", True)
        
        cmd = [
            "uv", "run", "pytest",
            "-m", " and ".join(markers),
            "--tb=short",
            "-v"
        ]
        
        try:
            result = self.run_command(cmd, check=False)
            return result.returncode
        except Exception as e:
            print(f"Error running API tests: {e}")
            return 1
    
    def run_mcp_tests(self) -> int:
        """Run MCP server tests"""
        print("\n=== Running MCP Server Tests ===")
        cmd = [
            "uv", "run", "pytest",
            "-m", "mcp",
            "--tb=short",
            "-v"
        ]
        
        try:
            result = self.run_command(cmd, check=False)
            return result.returncode
        except Exception as e:
            print(f"Error running MCP tests: {e}")
            return 1
    
    def run_performance_tests(self) -> int:
        """Run performance tests"""
        print("\n=== Running Performance Tests ===")
        
        if not self.check_api_availability():
            print("Skipping performance tests - API not available")
            return 0
        
        cmd = [
            "uv", "run", "pytest",
            "-m", "performance",
            "--tb=line",
            "-v",
            "--timeout=600"  # 10 minute timeout for performance tests
        ]
        
        try:
            result = self.run_command(cmd, check=False)
            return result.returncode
        except Exception as e:
            print(f"Error running performance tests: {e}")
            return 1
    
    def run_all_e2e_tests(self, skip_slow: bool = False) -> int:
        """Run all end-to-end tests"""
        print("\n=== Running All E2E Tests ===")
        
        api_available = self.check_api_availability()
        if not api_available:
            print("API not available, some tests will be skipped")
            test_config.set_config("use_mock_data", True)
        
        markers = ["e2e"]
        if skip_slow:
            markers.append("not slow")
            test_config.set_config("skip_slow_tests", True)
        
        cmd = [
            "uv", "run", "pytest",
            "-m", " and ".join(markers),
            "--tb=short",
            "-v"
        ]
        
        try:
            result = self.run_command(cmd, check=False)
            return result.returncode
        except Exception as e:
            print(f"Error running E2E tests: {e}")
            return 1
    
    def run_smoke_tests(self) -> int:
        """Run quick smoke tests to verify basic functionality"""
        print("\n=== Running Smoke Tests ===")
        
        # Run a subset of fast, critical tests
        cmd = [
            "uv", "run", "pytest",
            "-k", "test_api_client_initialization or test_server_creation",
            "--tb=line",
            "-v",
            "--maxfail=1"
        ]
        
        try:
            result = self.run_command(cmd, check=False)
            return result.returncode
        except Exception as e:
            print(f"Error running smoke tests: {e}")
            return 1
    
    def run_coverage_report(self) -> int:
        """Run tests with coverage reporting"""
        print("\n=== Running Tests with Coverage ===")
        
        # Install coverage if not available
        try:
            subprocess.run(["uv", "add", "--dev", "pytest-cov"], 
                         cwd=self.project_root, check=True)
        except subprocess.CalledProcessError:
            print("Could not install coverage tools")
        
        cmd = [
            "uv", "run", "pytest",
            "--cov=src/remy_mcp",
            "--cov-report=html",
            "--cov-report=term-missing",
            "-v"
        ]
        
        try:
            result = self.run_command(cmd, check=False)
            if result.returncode == 0:
                print("\nCoverage report generated in htmlcov/index.html")
            return result.returncode
        except Exception as e:
            print(f"Error running coverage: {e}")
            return 1
    
    def validate_test_environment(self) -> bool:
        """Validate the test environment is properly set up"""
        print("\n=== Validating Test Environment ===")
        
        # Check Python version
        print(f"Python version: {sys.version}")
        
        # Check if uv is available
        try:
            result = subprocess.run(["uv", "--version"], 
                                  capture_output=True, text=True)
            print(f"UV version: {result.stdout.strip()}")
        except FileNotFoundError:
            print("✗ UV not found")
            return False
        
        # Check if project dependencies are installed
        try:
            result = subprocess.run(["uv", "run", "python", "-c", 
                                   "import src.remy_mcp; print('✓ Package importable')"],
                                  cwd=self.project_root, 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout.strip())
            else:
                print("✗ Package not importable")
                return False
        except Exception as e:
            print(f"✗ Error checking package: {e}")
            return False
        
        # Check API availability
        api_available = self.check_api_availability()
        if not api_available:
            print("⚠ API not available - some tests may be skipped")
        
        return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Test runner for Israeli Land Authority MCP Server"
    )
    
    parser.add_argument(
        "test_type",
        choices=[
            "unit", "api", "mcp", "performance", 
            "e2e", "smoke", "coverage", "validate"
        ],
        help="Type of tests to run"
    )
    
    parser.add_argument(
        "--skip-slow",
        action="store_true",
        help="Skip slow running tests"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    # Set configuration based on arguments
    if args.skip_slow:
        test_config.set_config("skip_slow_tests", True)
    
    if args.verbose:
        print(f"Test configuration: {test_config.config}")
    
    # Validate environment first
    if args.test_type != "validate" and not runner.validate_test_environment():
        print("Environment validation failed")
        return 1
    
    # Run the requested tests
    start_time = time.time()
    
    if args.test_type == "unit":
        exit_code = runner.run_unit_tests()
    elif args.test_type == "api":
        exit_code = runner.run_api_tests(skip_slow=args.skip_slow)
    elif args.test_type == "mcp":
        exit_code = runner.run_mcp_tests()
    elif args.test_type == "performance":
        exit_code = runner.run_performance_tests()
    elif args.test_type == "e2e":
        exit_code = runner.run_all_e2e_tests(skip_slow=args.skip_slow)
    elif args.test_type == "smoke":
        exit_code = runner.run_smoke_tests()
    elif args.test_type == "coverage":
        exit_code = runner.run_coverage_report()
    elif args.test_type == "validate":
        success = runner.validate_test_environment()
        exit_code = 0 if success else 1
    else:
        print(f"Unknown test type: {args.test_type}")
        exit_code = 1
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nTest execution completed in {duration:.2f} seconds")
    print(f"Exit code: {exit_code}")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())