# PromptLab

![CI Pipeline](https://github.com/rohitpant-cloudkeeper/10x-engineer-project-repo/workflows/CI%20Pipeline/badge.svg?branch=Week-3)
![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)
![Tests](https://img.shields.io/badge/tests-220%20passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)

**Your AI Prompt Engineering Platform**

A professional tool for AI engineers to store, organize, and manage prompt templates. Think of it as "Postman for Prompts" - a workspace where teams can collaborate on AI prompts.

---

## Overview

PromptLab is a REST API platform designed to solve a common problem in AI development: managing and organizing prompt templates. As AI applications grow, teams often struggle with scattered prompts across files, notebooks, and chat histories. PromptLab provides a centralized, version-controlled system for prompt management.

### Why PromptLab?

Working with AI models means crafting, testing, and iterating on prompts. PromptLab helps you:

- **Centralize**: Keep all your prompts in one place instead of scattered across files
- **Collaborate**: Share prompts with your team through collections
- **Reuse**: Store templates with variables like `{{user_input}}` for dynamic content
- **Discover**: Search and filter prompts to find what you need quickly
- **Iterate**: Update prompts without losing track of what works

### Key Features

- 📝 **Template Variables**: Store prompts with placeholders (`{{input}}`, `{{context}}`) for dynamic content
- 📁 **Collections**: Organize prompts by project, use case, or team
- 🏷️ **Tagging System**: Add multiple tags to prompts for flexible categorization and filtering
- 📜 **Version Tracking**: Automatic version history for all prompt changes with compare and revert capabilities
- 🔍 **Smart Search**: Find prompts by title, description, collection, or tags
- ⚡ **Fast & Lightweight**: In-memory storage with extensibility to databases
- 🔄 **Flexible Updates**: Full (PUT) or partial (PATCH) updates supported
- 📚 **Interactive Docs**: Auto-generated API documentation with Swagger UI
- ✅ **Production Ready**: Comprehensive test coverage (99%) and CI/CD pipeline
- 🚀 **Easy Integration**: RESTful API works with any language or framework

### Use Cases

- **AI Application Development**: Store and manage prompts for your LLM-powered apps
- **Prompt Engineering Teams**: Collaborate on prompt templates across projects
- **Research & Experimentation**: Keep track of different prompt variations
- **Production Systems**: Centralized prompt management for deployed AI services

---

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10 or higher
- pip (Python package manager)
- Git
- Virtual environment tool (venv)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rohitpant-cloudkeeper/10x-engineer-project-repo.git
cd 10x-engineer-project-repo
```

### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Quick Start

### Running the Server

```bash
cd backend
source venv/bin/activate
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- API Base: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Running Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Running Tests with Coverage

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Returns API health status and version.

### Prompts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prompts` | List all prompts (supports filtering and search) |
| GET | `/prompts/{id}` | Get a specific prompt by ID |
| POST | `/prompts` | Create a new prompt |
| PUT | `/prompts/{id}` | Update a prompt (full update) |
| PATCH | `/prompts/{id}` | Partially update a prompt |
| DELETE | `/prompts/{id}` | Delete a prompt |

### Collections

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/collections` | List all collections |
| GET | `/collections/{id}` | Get a specific collection by ID |
| POST | `/collections` | Create a new collection |
| DELETE | `/collections/{id}` | Delete a collection |

### Tags

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tags` | List all tags (supports search) |
| GET | `/tags/{name}` | Get a specific tag by name |
| GET | `/tags/popular` | Get popular tags sorted by usage |

### Version History

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prompts/{id}/versions` | List all versions of a prompt |
| GET | `/prompts/{id}/versions/{version}` | Get a specific version |
| POST | `/prompts/{id}/versions/{version}/revert` | Revert to a previous version |
| GET | `/prompts/{id}/versions/compare` | Compare two versions |

### Example Usage

#### Create a Prompt

```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code Review Prompt",
    "content": "Review the following code and provide feedback:\n\n{{code}}",
    "description": "A prompt for AI code review",
    "tags": ["python", "code-review", "quality"]
  }'
```

#### List Prompts with Filtering

```bash
# Get all prompts
curl "http://localhost:8000/prompts"

# Filter by collection
curl "http://localhost:8000/prompts?collection_id=abc123"

# Search prompts
curl "http://localhost:8000/prompts?search=code"

# Filter by single tag
curl "http://localhost:8000/prompts?tags=python"

# Filter by multiple tags (AND logic - must have all tags)
curl "http://localhost:8000/prompts?tags=python,code-review"

# Combine filters
curl "http://localhost:8000/prompts?tags=python&search=review&collection_id=abc123"
```

#### Working with Tags

```bash
# List all tags
curl "http://localhost:8000/tags"

# Search tags
curl "http://localhost:8000/tags?search=python"

# Get specific tag details
curl "http://localhost:8000/tags/python"

# Get popular tags
curl "http://localhost:8000/tags/popular?limit=10"

# Add tags to existing prompt (PATCH)
curl -X PATCH "http://localhost:8000/prompts/{id}" \
  -H "Content-Type: application/json" \
  -d '{
    "tags": ["python", "testing", "advanced"]
  }'
```

#### Partial Update with PATCH

```bash
curl -X PATCH "http://localhost:8000/prompts/{id}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title"
  }'
```

---

## Tagging System

PromptLab includes a powerful tagging system that allows you to categorize prompts with multiple labels for better organization and discovery.

### Tag Features

- **Multiple Tags per Prompt**: Add up to 10 tags to each prompt
- **Automatic Normalization**: Tags are automatically converted to lowercase with spaces replaced by hyphens
- **Usage Tracking**: See how many prompts use each tag
- **Flexible Filtering**: Filter prompts by one or more tags using AND logic
- **Tag Search**: Search for tags by name to discover existing tags
- **Popular Tags**: View most-used tags to understand common categories

### Tag Validation Rules

- Tags must be 1-30 characters long
- Only lowercase letters, numbers, and hyphens allowed
- Spaces are automatically replaced with hyphens
- Invalid characters are removed during normalization
- Duplicate tags are automatically removed

### Tag Examples

```bash
# Valid tags (after normalization)
"Python" → "python"
"Code Review" → "code-review"
"AI/ML" → "aiml"
"python-3.11" → "python-3-11"

# Creating a prompt with tags
{
  "title": "Python Testing Guide",
  "content": "Write unit tests for: {{code}}",
  "tags": ["Python", "Testing", "Unit Tests"]
}
# Tags stored as: ["python", "testing", "unit-tests"]
```

### Tag Filtering

Tags use AND logic when filtering - prompts must have ALL specified tags:

```bash
# Find prompts with BOTH "python" AND "testing" tags
curl "http://localhost:8000/prompts?tags=python,testing"

# Combine with other filters
curl "http://localhost:8000/prompts?tags=python,advanced&search=async&collection_id=abc123"
```

### Tag Management

Tags are created automatically when first used and deleted automatically when no longer in use:

```bash
# Create prompt with new tags (tags created automatically)
POST /prompts {"tags": ["new-tag", "another-tag"]}

# View all tags with usage counts
GET /tags

# Get popular tags
GET /tags/popular?limit=5

# Search for specific tags
GET /tags?search=python
```

---

## Version Tracking

PromptLab automatically tracks the complete history of every prompt, allowing you to view past versions, compare changes, and revert to previous states.

### Version Features

- **Automatic Versioning**: Every prompt update (PUT/PATCH) creates a new version
- **Complete History**: View all versions of a prompt sorted by version number
- **Version Comparison**: Compare any two versions to see what changed
- **Easy Revert**: Restore a prompt to any previous version
- **Pagination Support**: Efficiently browse through version history
- **No Data Loss**: Reverting creates a new version, preserving all history

### How Versioning Works

1. **Initial Version**: When you create a prompt, version 1 is automatically created
2. **Auto-Increment**: Each update (PUT/PATCH) increments the version number
3. **Full Snapshot**: Each version stores the complete prompt state (title, content, description, tags, collection)
4. **Revert Creates New Version**: Reverting to v2 doesn't delete v3+, it creates a new version with v2's content

### Version Examples

```bash
# Create a prompt (creates version 1)
POST /prompts
{
  "title": "Original Title",
  "content": "Original content"
}

# Update the prompt (creates version 2)
PUT /prompts/{id}
{
  "title": "Updated Title",
  "content": "Updated content"
}

# List all versions
GET /prompts/{id}/versions
# Returns: [v2, v1] (newest first)

# Get specific version
GET /prompts/{id}/versions/1
# Returns: Original version with "Original Title"

# Compare versions
GET /prompts/{id}/versions/compare?from=1&to=2
# Returns: Both versions + changes summary

# Revert to version 1 (creates version 3 with v1 content)
POST /prompts/{id}/versions/1/revert
# Result: v3 with "Original Title" and "Original content"
```

### Version API Endpoints

```bash
# List all versions (with pagination)
curl "http://localhost:8000/prompts/{id}/versions?limit=10&offset=0"

# Get a specific version
curl "http://localhost:8000/prompts/{id}/versions/2"

# Compare two versions
curl "http://localhost:8000/prompts/{id}/versions/compare?from=1&to=3"

# Revert to a previous version
curl -X POST "http://localhost:8000/prompts/{id}/versions/2/revert"
```

### Version Response Format

```json
{
  "versions": [
    {
      "id": "version-uuid",
      "prompt_id": "prompt-uuid",
      "version": 2,
      "title": "Updated Title",
      "content": "Updated content",
      "description": "Updated description",
      "collection_id": "collection-uuid",
      "tags": ["python", "updated"],
      "created_at": "2024-01-15T11:00:00Z"
    },
    {
      "id": "version-uuid",
      "prompt_id": "prompt-uuid",
      "version": 1,
      "title": "Original Title",
      "content": "Original content",
      "description": "Original description",
      "collection_id": null,
      "tags": ["python"],
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 2,
  "prompt_id": "prompt-uuid"
}
```

### Version Comparison

The compare endpoint shows which fields changed between versions:

```json
{
  "prompt_id": "prompt-uuid",
  "from_version": { /* version 1 data */ },
  "to_version": { /* version 2 data */ },
  "changes": {
    "title": "changed",
    "content": "changed",
    "description": "unchanged",
    "collection_id": "changed",
    "tags": "changed"
  }
}
```

---

## CI/CD Pipeline

PromptLab includes a comprehensive CI/CD pipeline using GitHub Actions that automatically runs on every push and pull request.

### Pipeline Features

- ✅ **Automated Testing**: Runs all 220 tests on Python 3.11 and 3.12
- ✅ **Coverage Enforcement**: Fails if coverage drops below 80% (current: 99%)
- ✅ **Code Quality**: Runs flake8, black, and isort checks
- ✅ **Mutation Testing**: Verifies test quality with mutation testing
- ✅ **Multi-Python**: Tests on multiple Python versions for compatibility
- ✅ **Artifacts**: Uploads coverage reports for review

### Pipeline Status

Check the current pipeline status with the badges at the top of this README or visit:
https://github.com/rohitpant-cloudkeeper/10x-engineer-project-repo/actions

### Running CI Locally

```bash
# Run tests with coverage
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80 -v

# Run mutation tests
python test_mutations_tags.py
python test_mutations_versions.py

# Run code quality checks
flake8 app/ tests/
black --check app/ tests/
isort --check-only app/ tests/
```

---

## Project Structure

```
promptlab/
├── README.md                    # This file
├── PROJECT_BRIEF.md             # Assignment details
├── GRADING_RUBRIC.md            # Grading criteria
│
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Package initialization
│   │   ├── api.py               # FastAPI routes and endpoints
│   │   ├── models.py            # Pydantic data models
│   │   ├── storage.py           # In-memory storage layer
│   │   └── utils.py             # Helper functions
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Test fixtures
│   │   └── test_api.py          # API endpoint tests
│   ├── main.py                  # Application entry point
│   ├── requirements.txt         # Python dependencies
│   └── venv/                    # Virtual environment (not in git)
│
├── docs/                        # Documentation files
├── specs/                       # Feature specifications
├── frontend/                    # Frontend (Week 4)
└── .github/                     # CI/CD workflows (Week 3)
```

---

## Development

### Setting Up Development Environment

1. Follow the installation steps above
2. Install development dependencies (if any)
3. Run tests to ensure everything works
4. Start the server with hot reload enabled

### Code Style

- Follow PEP 8 style guidelines for Python
- Use type hints for function parameters and return values
- Write docstrings for all functions and classes (Google style)
- Keep functions small and focused
- Write tests for new features

### Making Changes

1. Create a new branch for your feature
2. Make your changes
3. Run tests to ensure nothing breaks
4. Commit with meaningful messages
5. Push and create a pull request

---

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **Server**: Uvicorn 0.27.0
- **Validation**: Pydantic 2.10+
- **Testing**: pytest 7.4.4
- **HTTP Client**: httpx 0.26.0 (for testing)
- **Coverage**: pytest-cov 4.1.0

---

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/ -v`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Commit Message Convention

We follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

---

## Roadmap

- [x] Week 1: Backend Foundation (Bug fixes, PATCH endpoint)
- [x] Week 2: Documentation & Specifications
- [x] Week 3: Testing, Tagging & Version Tracking
  - [x] Comprehensive unit tests (220 tests, 99% coverage)
  - [x] Tagging system with filtering
  - [x] Version tracking with history and revert
  - [x] Mutation testing (100% kill rate for versions, 90.9% for tags)
  - [x] CI/CD pipeline with GitHub Actions
- [ ] Week 4: Full-Stack Integration (React frontend)

---

## License

This project is part of an educational assignment.

---

## Support

For questions or issues:
- Check the [PROJECT_BRIEF.md](PROJECT_BRIEF.md) for detailed instructions
- Review [GRADING_RUBRIC.md](GRADING_RUBRIC.md) for requirements
- Open an issue on GitHub
- Contact the course instructor

---

**Built with ❤️ as part of the 10x Engineer learning project**

