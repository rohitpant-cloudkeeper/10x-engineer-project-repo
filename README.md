# PromptLab

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
- 🔍 **Smart Search**: Find prompts by title, description, or collection
- ⚡ **Fast & Lightweight**: In-memory storage with extensibility to databases
- 🔄 **Flexible Updates**: Full (PUT) or partial (PATCH) updates supported
- 📚 **Interactive Docs**: Auto-generated API documentation with Swagger UI
- ✅ **Production Ready**: Comprehensive test coverage and error handling
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

### Example Usage

#### Create a Prompt

```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code Review Prompt",
    "content": "Review the following code and provide feedback:\n\n{{code}}",
    "description": "A prompt for AI code review"
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
- [ ] Week 2: Documentation & Specifications
- [ ] Week 3: Testing & DevOps (CI/CD, Docker)
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
