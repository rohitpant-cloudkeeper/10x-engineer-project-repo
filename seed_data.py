#!/usr/bin/env python3
"""
Seed script to populate PromptLab with sample data
Creates collections and prompts using the backend API
"""

import requests
import json
from typing import List, Dict

API_BASE_URL = "http://localhost:8000"

# Sample collections
COLLECTIONS = [
    {
        "name": "Code Review",
        "description": "Prompts for reviewing and analyzing code quality"
    },
    {
        "name": "Documentation",
        "description": "Prompts for generating technical documentation"
    },
    {
        "name": "Testing",
        "description": "Prompts for creating and improving tests"
    },
    {
        "name": "Debugging",
        "description": "Prompts for troubleshooting and fixing bugs"
    },
    {
        "name": "Refactoring",
        "description": "Prompts for improving code structure and design"
    }
]

# Sample prompts with their collection, tags, and content
PROMPTS = [
    # Code Review Collection
    {
        "title": "Python Code Review",
        "content": "Review the following Python code and provide feedback on:\n\n1. Code quality and readability\n2. Performance optimizations\n3. Security concerns\n4. Best practices\n\nCode:\n{{code}}",
        "description": "Comprehensive Python code review prompt",
        "collection": "Code Review",
        "tags": ["python", "code-review", "quality"]
    },
    {
        "title": "JavaScript Code Review",
        "content": "Analyze this JavaScript code and suggest improvements:\n\n{{code}}\n\nFocus on:\n- ES6+ features usage\n- Async/await patterns\n- Error handling\n- Performance",
        "description": "JavaScript code review with modern practices",
        "collection": "Code Review",
        "tags": ["javascript", "code-review", "es6"]
    },
    {
        "title": "React Component Review",
        "content": "Review this React component for:\n\n{{component_code}}\n\n- Component structure\n- Hooks usage\n- Performance optimization\n- Accessibility\n- Props validation",
        "description": "React component code review",
        "collection": "Code Review",
        "tags": ["react", "javascript", "frontend", "code-review"]
    },
    {
        "title": "SQL Query Review",
        "content": "Review this SQL query for optimization:\n\n{{query}}\n\nCheck for:\n- Index usage\n- Join efficiency\n- Query performance\n- Security (SQL injection)",
        "description": "SQL query optimization review",
        "collection": "Code Review",
        "tags": ["sql", "database", "performance", "code-review"]
    },
    {
        "title": "API Design Review",
        "content": "Review this API design:\n\n{{api_spec}}\n\nEvaluate:\n- RESTful principles\n- Endpoint naming\n- HTTP methods usage\n- Response structure\n- Error handling",
        "description": "REST API design review",
        "collection": "Code Review",
        "tags": ["api", "rest", "design", "code-review"]
    },
    {
        "title": "Security Code Review",
        "content": "Perform a security review of this code:\n\n{{code}}\n\nCheck for:\n- Input validation\n- Authentication/Authorization\n- Data encryption\n- Common vulnerabilities (OWASP Top 10)",
        "description": "Security-focused code review",
        "collection": "Code Review",
        "tags": ["security", "code-review", "owasp"]
    },
    {
        "title": "TypeScript Code Review",
        "content": "Review this TypeScript code:\n\n{{code}}\n\nFocus on:\n- Type safety\n- Interface design\n- Generic usage\n- Type guards",
        "description": "TypeScript code review",
        "collection": "Code Review",
        "tags": ["typescript", "code-review", "types"]
    },
    {
        "title": "CSS/SCSS Review",
        "content": "Review this stylesheet:\n\n{{styles}}\n\nCheck for:\n- BEM methodology\n- Responsive design\n- Performance\n- Browser compatibility",
        "description": "CSS/SCSS code review",
        "collection": "Code Review",
        "tags": ["css", "scss", "frontend", "code-review"]
    },
    {
        "title": "Docker Configuration Review",
        "content": "Review this Dockerfile:\n\n{{dockerfile}}\n\nEvaluate:\n- Image size optimization\n- Security best practices\n- Layer caching\n- Multi-stage builds",
        "description": "Docker configuration review",
        "collection": "Code Review",
        "tags": ["docker", "devops", "code-review"]
    },
    {
        "title": "Git Commit Review",
        "content": "Review these git commits:\n\n{{commits}}\n\nCheck:\n- Commit message quality\n- Atomic commits\n- Branch strategy\n- Code organization",
        "description": "Git commit history review",
        "collection": "Code Review",
        "tags": ["git", "version-control", "code-review"]
    },
    
    # Documentation Collection
    {
        "title": "API Documentation Generator",
        "content": "Generate comprehensive API documentation for:\n\n{{endpoint_code}}\n\nInclude:\n- Endpoint description\n- Request/response examples\n- Parameters\n- Error codes\n- Authentication requirements",
        "description": "Generate API endpoint documentation",
        "collection": "Documentation",
        "tags": ["api", "documentation", "openapi"]
    },
    {
        "title": "Function Documentation",
        "content": "Write detailed documentation for this function:\n\n{{function_code}}\n\nInclude:\n- Purpose and usage\n- Parameters with types\n- Return value\n- Examples\n- Edge cases",
        "description": "Generate function docstrings",
        "collection": "Documentation",
        "tags": ["documentation", "docstring", "python"]
    },
    {
        "title": "README Generator",
        "content": "Create a comprehensive README.md for this project:\n\n{{project_info}}\n\nInclude:\n- Project overview\n- Installation instructions\n- Usage examples\n- API reference\n- Contributing guidelines",
        "description": "Generate project README",
        "collection": "Documentation",
        "tags": ["documentation", "readme", "markdown"]
    },
    {
        "title": "Class Documentation",
        "content": "Document this class:\n\n{{class_code}}\n\nProvide:\n- Class purpose\n- Constructor parameters\n- Method descriptions\n- Usage examples\n- Inheritance information",
        "description": "Generate class documentation",
        "collection": "Documentation",
        "tags": ["documentation", "oop", "class"]
    },
    {
        "title": "Architecture Documentation",
        "content": "Create architecture documentation for:\n\n{{system_description}}\n\nInclude:\n- System overview\n- Component diagram\n- Data flow\n- Technology stack\n- Deployment architecture",
        "description": "Generate system architecture docs",
        "collection": "Documentation",
        "tags": ["documentation", "architecture", "design"]
    },
    {
        "title": "Database Schema Documentation",
        "content": "Document this database schema:\n\n{{schema}}\n\nInclude:\n- Table descriptions\n- Column definitions\n- Relationships\n- Indexes\n- Constraints",
        "description": "Generate database documentation",
        "collection": "Documentation",
        "tags": ["documentation", "database", "schema"]
    },
    {
        "title": "CLI Tool Documentation",
        "content": "Create documentation for this CLI tool:\n\n{{cli_code}}\n\nInclude:\n- Command syntax\n- Options and flags\n- Usage examples\n- Configuration\n- Troubleshooting",
        "description": "Generate CLI documentation",
        "collection": "Documentation",
        "tags": ["documentation", "cli", "command-line"]
    },
    {
        "title": "Configuration Documentation",
        "content": "Document this configuration file:\n\n{{config}}\n\nExplain:\n- Each configuration option\n- Default values\n- Valid ranges\n- Examples\n- Environment variables",
        "description": "Generate config documentation",
        "collection": "Documentation",
        "tags": ["documentation", "configuration", "setup"]
    },
    {
        "title": "Changelog Generator",
        "content": "Generate a changelog from these commits:\n\n{{commits}}\n\nFormat:\n- Version number\n- Release date\n- Added features\n- Bug fixes\n- Breaking changes",
        "description": "Generate changelog from commits",
        "collection": "Documentation",
        "tags": ["documentation", "changelog", "release"]
    },
    {
        "title": "Tutorial Creator",
        "content": "Create a step-by-step tutorial for:\n\n{{topic}}\n\nInclude:\n- Prerequisites\n- Step-by-step instructions\n- Code examples\n- Screenshots/diagrams\n- Common pitfalls",
        "description": "Generate tutorial documentation",
        "collection": "Documentation",
        "tags": ["documentation", "tutorial", "guide"]
    },
    
    # Testing Collection
    {
        "title": "Unit Test Generator",
        "content": "Generate unit tests for this function:\n\n{{function_code}}\n\nCreate tests for:\n- Happy path\n- Edge cases\n- Error conditions\n- Boundary values\n- Mock dependencies",
        "description": "Generate comprehensive unit tests",
        "collection": "Testing",
        "tags": ["testing", "unit-test", "pytest"]
    },
    {
        "title": "Integration Test Creator",
        "content": "Create integration tests for:\n\n{{component_code}}\n\nTest:\n- Component interactions\n- API calls\n- Database operations\n- External services\n- Error scenarios",
        "description": "Generate integration tests",
        "collection": "Testing",
        "tags": ["testing", "integration-test", "api"]
    },
    {
        "title": "Test Data Generator",
        "content": "Generate test data for:\n\n{{schema}}\n\nCreate:\n- Valid test cases\n- Invalid test cases\n- Edge cases\n- Realistic data\n- Performance test data",
        "description": "Generate test data fixtures",
        "collection": "Testing",
        "tags": ["testing", "test-data", "fixtures"]
    },
    {
        "title": "E2E Test Scenarios",
        "content": "Create end-to-end test scenarios for:\n\n{{feature_description}}\n\nInclude:\n- User flows\n- Test steps\n- Expected results\n- Setup/teardown\n- Data requirements",
        "description": "Generate E2E test scenarios",
        "collection": "Testing",
        "tags": ["testing", "e2e", "selenium"]
    },
    {
        "title": "API Test Cases",
        "content": "Generate API test cases for:\n\n{{endpoint}}\n\nTest:\n- Valid requests\n- Invalid inputs\n- Authentication\n- Rate limiting\n- Response validation",
        "description": "Generate API test cases",
        "collection": "Testing",
        "tags": ["testing", "api", "rest"]
    },
    {
        "title": "Performance Test Script",
        "content": "Create performance tests for:\n\n{{system}}\n\nInclude:\n- Load testing scenarios\n- Stress testing\n- Spike testing\n- Endurance testing\n- Metrics to measure",
        "description": "Generate performance test scripts",
        "collection": "Testing",
        "tags": ["testing", "performance", "load-test"]
    },
    {
        "title": "Security Test Cases",
        "content": "Generate security test cases for:\n\n{{application}}\n\nTest for:\n- SQL injection\n- XSS vulnerabilities\n- CSRF protection\n- Authentication bypass\n- Authorization issues",
        "description": "Generate security test cases",
        "collection": "Testing",
        "tags": ["testing", "security", "penetration"]
    },
    {
        "title": "Mock Data Creator",
        "content": "Create mock data for testing:\n\n{{interface}}\n\nGenerate:\n- Mock objects\n- Stub responses\n- Fake data\n- Test doubles\n- Spy functions",
        "description": "Generate mock data and stubs",
        "collection": "Testing",
        "tags": ["testing", "mocking", "stub"]
    },
    {
        "title": "Regression Test Suite",
        "content": "Create regression tests for:\n\n{{bug_fix}}\n\nInclude:\n- Bug reproduction steps\n- Fix verification\n- Related scenarios\n- Boundary conditions\n- Prevention tests",
        "description": "Generate regression test suite",
        "collection": "Testing",
        "tags": ["testing", "regression", "bug-fix"]
    },
    {
        "title": "Accessibility Test Cases",
        "content": "Generate accessibility test cases for:\n\n{{component}}\n\nTest:\n- Keyboard navigation\n- Screen reader support\n- Color contrast\n- ARIA labels\n- Focus management",
        "description": "Generate accessibility tests",
        "collection": "Testing",
        "tags": ["testing", "accessibility", "a11y"]
    },
    
    # Debugging Collection
    {
        "title": "Debug Error Message",
        "content": "Help debug this error:\n\nError: {{error_message}}\n\nStack trace:\n{{stack_trace}}\n\nCode context:\n{{code}}\n\nProvide:\n- Root cause analysis\n- Potential fixes\n- Prevention strategies",
        "description": "Debug and explain error messages",
        "collection": "Debugging",
        "tags": ["debugging", "error", "troubleshooting"]
    },
    {
        "title": "Performance Issue Debugger",
        "content": "Analyze this performance issue:\n\n{{slow_code}}\n\nProfile data:\n{{profile}}\n\nIdentify:\n- Bottlenecks\n- Memory leaks\n- Inefficient algorithms\n- Optimization opportunities",
        "description": "Debug performance issues",
        "collection": "Debugging",
        "tags": ["debugging", "performance", "optimization"]
    },
    {
        "title": "Memory Leak Detector",
        "content": "Help find memory leaks in:\n\n{{code}}\n\nMemory profile:\n{{memory_data}}\n\nCheck for:\n- Unreleased resources\n- Circular references\n- Event listener leaks\n- Cache issues",
        "description": "Detect and fix memory leaks",
        "collection": "Debugging",
        "tags": ["debugging", "memory", "leak"]
    },
    {
        "title": "Race Condition Debugger",
        "content": "Debug this race condition:\n\n{{concurrent_code}}\n\nSymptoms:\n{{symptoms}}\n\nAnalyze:\n- Shared state access\n- Synchronization issues\n- Thread safety\n- Deadlock potential",
        "description": "Debug concurrency issues",
        "collection": "Debugging",
        "tags": ["debugging", "concurrency", "race-condition"]
    },
    {
        "title": "API Integration Debugger",
        "content": "Debug this API integration issue:\n\nAPI call:\n{{api_call}}\n\nResponse:\n{{response}}\n\nError:\n{{error}}\n\nCheck:\n- Request format\n- Authentication\n- Rate limits\n- Response parsing",
        "description": "Debug API integration problems",
        "collection": "Debugging",
        "tags": ["debugging", "api", "integration"]
    },
    {
        "title": "Database Query Debugger",
        "content": "Debug this database query:\n\n{{query}}\n\nError/Issue:\n{{issue}}\n\nAnalyze:\n- Query syntax\n- Performance\n- Locks/deadlocks\n- Data integrity",
        "description": "Debug database queries",
        "collection": "Debugging",
        "tags": ["debugging", "database", "sql"]
    },
    {
        "title": "Frontend Bug Debugger",
        "content": "Debug this frontend issue:\n\nComponent:\n{{component}}\n\nBehavior:\n{{bug_description}}\n\nConsole errors:\n{{console_errors}}\n\nCheck:\n- State management\n- Event handlers\n- Rendering issues\n- Browser compatibility",
        "description": "Debug frontend bugs",
        "collection": "Debugging",
        "tags": ["debugging", "frontend", "react"]
    },
    {
        "title": "Network Issue Debugger",
        "content": "Debug this network issue:\n\nRequest:\n{{request}}\n\nNetwork error:\n{{error}}\n\nAnalyze:\n- CORS issues\n- Timeout problems\n- SSL/TLS errors\n- Proxy configuration",
        "description": "Debug network problems",
        "collection": "Debugging",
        "tags": ["debugging", "network", "http"]
    },
    {
        "title": "Build Error Debugger",
        "content": "Debug this build error:\n\nBuild command:\n{{command}}\n\nError output:\n{{error}}\n\nCheck:\n- Dependencies\n- Configuration\n- Environment variables\n- Build tools",
        "description": "Debug build and compilation errors",
        "collection": "Debugging",
        "tags": ["debugging", "build", "compilation"]
    },
    {
        "title": "Test Failure Debugger",
        "content": "Debug this failing test:\n\nTest:\n{{test_code}}\n\nFailure:\n{{failure_message}}\n\nAnalyze:\n- Test logic\n- Timing issues\n- Mock setup\n- Environment differences",
        "description": "Debug failing tests",
        "collection": "Debugging",
        "tags": ["debugging", "testing", "failure"]
    },
    
    # Refactoring Collection
    {
        "title": "Code Simplification",
        "content": "Simplify this code:\n\n{{complex_code}}\n\nRefactor to:\n- Reduce complexity\n- Improve readability\n- Remove duplication\n- Follow SOLID principles",
        "description": "Simplify complex code",
        "collection": "Refactoring",
        "tags": ["refactoring", "clean-code", "simplification"]
    },
    {
        "title": "Extract Function Refactoring",
        "content": "Refactor this code by extracting functions:\n\n{{code}}\n\nIdentify:\n- Reusable logic\n- Single responsibility violations\n- Long methods\n- Naming opportunities",
        "description": "Extract functions from code",
        "collection": "Refactoring",
        "tags": ["refactoring", "functions", "clean-code"]
    },
    {
        "title": "Design Pattern Application",
        "content": "Apply appropriate design patterns to:\n\n{{code}}\n\nCurrent issues:\n{{issues}}\n\nSuggest:\n- Suitable patterns\n- Implementation approach\n- Benefits\n- Trade-offs",
        "description": "Apply design patterns",
        "collection": "Refactoring",
        "tags": ["refactoring", "design-patterns", "architecture"]
    },
    {
        "title": "Dependency Injection Refactoring",
        "content": "Refactor to use dependency injection:\n\n{{tightly_coupled_code}}\n\nImprove:\n- Testability\n- Flexibility\n- Decoupling\n- Maintainability",
        "description": "Implement dependency injection",
        "collection": "Refactoring",
        "tags": ["refactoring", "dependency-injection", "solid"]
    },
    {
        "title": "Error Handling Improvement",
        "content": "Improve error handling in:\n\n{{code}}\n\nEnhance:\n- Exception handling\n- Error messages\n- Recovery strategies\n- Logging",
        "description": "Refactor error handling",
        "collection": "Refactoring",
        "tags": ["refactoring", "error-handling", "exceptions"]
    },
    {
        "title": "Type Safety Refactoring",
        "content": "Add type safety to:\n\n{{untyped_code}}\n\nAdd:\n- Type annotations\n- Interfaces\n- Type guards\n- Generic types",
        "description": "Add type safety to code",
        "collection": "Refactoring",
        "tags": ["refactoring", "typescript", "types"]
    },
    {
        "title": "Async/Await Conversion",
        "content": "Convert callbacks/promises to async/await:\n\n{{callback_code}}\n\nImprove:\n- Readability\n- Error handling\n- Flow control\n- Maintainability",
        "description": "Convert to async/await",
        "collection": "Refactoring",
        "tags": ["refactoring", "async", "javascript"]
    },
    {
        "title": "Class to Functional Refactoring",
        "content": "Refactor this class to functional style:\n\n{{class_code}}\n\nConvert to:\n- Pure functions\n- Immutable data\n- Composition\n- Functional patterns",
        "description": "Convert OOP to functional",
        "collection": "Refactoring",
        "tags": ["refactoring", "functional", "paradigm"]
    },
    {
        "title": "Database Query Optimization",
        "content": "Optimize these database queries:\n\n{{queries}}\n\nImprove:\n- Query performance\n- Index usage\n- N+1 problems\n- Batch operations",
        "description": "Optimize database queries",
        "collection": "Refactoring",
        "tags": ["refactoring", "database", "optimization"]
    },
    {
        "title": "Component Decomposition",
        "content": "Break down this large component:\n\n{{large_component}}\n\nCreate:\n- Smaller components\n- Reusable pieces\n- Clear responsibilities\n- Better composition",
        "description": "Decompose large components",
        "collection": "Refactoring",
        "tags": ["refactoring", "components", "react"]
    }
]


def create_collections() -> Dict[str, str]:
    """Create collections and return mapping of name to ID"""
    print("Creating collections...")
    collection_map = {}
    
    for collection in COLLECTIONS:
        try:
            response = requests.post(
                f"{API_BASE_URL}/collections",
                json=collection
            )
            response.raise_for_status()
            data = response.json()
            collection_map[collection["name"]] = data["id"]
            print(f"✓ Created collection: {collection['name']}")
        except Exception as e:
            print(f"✗ Failed to create collection {collection['name']}: {e}")
    
    return collection_map


def create_prompts(collection_map: Dict[str, str]):
    """Create prompts with their collections and tags"""
    print("\nCreating prompts...")
    created_count = 0
    
    for prompt_data in PROMPTS:
        try:
            # Get collection ID
            collection_name = prompt_data.pop("collection")
            collection_id = collection_map.get(collection_name)
            
            # Prepare prompt data
            prompt = {
                "title": prompt_data["title"],
                "content": prompt_data["content"],
                "description": prompt_data["description"],
                "collection_id": collection_id,
                "tags": prompt_data["tags"]
            }
            
            response = requests.post(
                f"{API_BASE_URL}/prompts",
                json=prompt
            )
            response.raise_for_status()
            created_count += 1
            print(f"✓ Created prompt: {prompt['title']}")
        except Exception as e:
            print(f"✗ Failed to create prompt {prompt_data.get('title', 'Unknown')}: {e}")
    
    print(f"\n✓ Successfully created {created_count} prompts!")


def main():
    print("=" * 60)
    print("PromptLab Data Seeding Script")
    print("=" * 60)
    print(f"\nAPI Base URL: {API_BASE_URL}")
    print(f"Collections to create: {len(COLLECTIONS)}")
    print(f"Prompts to create: {len(PROMPTS)}")
    print("\nStarting data seeding...\n")
    
    try:
        # Test API connection
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        print("✓ API is reachable\n")
    except Exception as e:
        print(f"✗ Cannot reach API at {API_BASE_URL}")
        print(f"Error: {e}")
        print("\nMake sure the backend is running on port 8000")
        return
    
    # Create collections
    collection_map = create_collections()
    
    if not collection_map:
        print("\n✗ No collections were created. Aborting.")
        return
    
    # Create prompts
    create_prompts(collection_map)
    
    print("\n" + "=" * 60)
    print("Data seeding completed!")
    print("=" * 60)
    print(f"\nCreated:")
    print(f"  - {len(collection_map)} collections")
    print(f"  - {len(PROMPTS)} prompts")
    print("\nYou can now view them at http://localhost:5173")


if __name__ == "__main__":
    main()
