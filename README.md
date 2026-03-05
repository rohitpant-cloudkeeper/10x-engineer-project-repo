# PromptLab API

> A professional REST API platform for managing AI prompt templates with version control, collections, and smart search capabilities.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Educational-orange.svg)](LICENSE)

---

## Table of Contents

- [What is PromptLab?](#what-is-promptlab)
- [Key Features](#key-features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Data Models](#data-models)
- [Code Examples](#code-examples)
- [Project Structure](#project-structure)
- [Development Guide](#development-guide)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## What is PromptLab?

PromptLab is a **centralized prompt management system** designed for AI engineers and teams working with Large Language Models (LLMs). Think of it as "Postman for Prompts" - a professional workspace where you can:

- **Store** prompt templates with dynamic variables
- **Organize** prompts into collections by project or use case
- **Search** and filter prompts efficiently
- **Collaborate** with your team on prompt engineering
- **Iterate** on prompts without losing track of what works

### Why PromptLab?

As AI applications grow, managing prompts becomes challenging:
- ❌ Prompts scattered across files, notebooks, and chat histories
- ❌ No version control for prompt iterations
- ❌ Difficult to share prompts across teams
- ❌ Hard to find the right prompt when you need it

PromptLab solves these problems with a RESTful API that integrates seamlessly into your workflow.

### Use Cases

- **AI Application Development**: Centralized prompt storage for LLM-powered apps
- **Prompt Engineering Teams**: Collaborate on prompt templates across projects
- **Research & Experimentation**: Track different prompt variations and results
- **Production Systems**: Manage prompts for deployed AI services
- **Educational Projects**: Learn prompt engineering best practices

---

## Key Features

### 🎯 Core Functionality
- **Template Variables**: Use placeholders like `{{user_input}}`, `{{context}}` for dynamic content
- **Collections**: Organize prompts by project, team, or use case
- **Smart Search**: Find prompts by title, description, or collection
- **Flexible Updates**: Support for both full (PUT) and partial (PATCH) updates

### ⚡ Technical Highlights
- **Fast & Lightweight**: In-memory storage with O(1) lookups
- **RESTful API**: Standard HTTP methods and status codes
- **Auto-Generated Docs**: Interactive Swagger UI and ReDoc
- **Type Safety**: Pydantic models with automatic validation
- **Comprehensive Testing**: 80%+ test coverage
- **Production Ready**: Error handling, CORS support, health checks

### 🔧 Developer Experience
- **Easy Integration**: Works with any language or framework
- **Clear Error Messages**: Detailed validation feedback
- **Hot Reload**: Development server with automatic reloading
- **Extensible**: Easy to add database backends or new features

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| **Python** | 3.10 or higher | `python3 --version` |
| **pip** | Latest | `pip3 --version` |
| **Git** | Any recent version | `git --version` |
| **Virtual Environment** | Built-in with Python | `python3 -m venv --help` |

### Optional Tools
- **curl** or **Postman**: For testing API endpoints
- **HTTPie**: User-friendly HTTP client (`pip install httpie`)
- **Docker**: For containerized deployment (Week 3+)

---

## Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/rohitpant-cloudkeeper/10x-engineer-project-repo.git

# Navigate to the project directory
cd 10x-engineer-project-repo

# Checkout the Week-2 branch (if not already on it)
git checkout Week-2
```

### Step 2: Set Up Python Virtual Environment

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

**Note**: You should see `(venv)` in your terminal prompt when the virtual environment is active.

### Step 3: Install Dependencies

```bash
# Ensure you're in the backend directory with venv activated
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Expected packages**:
- `fastapi==0.109.0` - Web framework
- `uvicorn==0.27.0` - ASGI server
- `pydantic==2.10.4` - Data validation
- `pytest==7.4.4` - Testing framework
- `httpx==0.26.0` - HTTP client for tests
- `pytest-cov==4.1.0` - Coverage reporting

### Step 4: Verify Installation

```bash
# Run tests to verify everything is working
pytest tests/ -v

# You should see all tests passing
```

---

## Quick Start

### Starting the Server

```bash
# Ensure you're in the backend directory with venv activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start the development server
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

**Server Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Access Points

Once the server is running, you can access:

| Resource | URL | Description |
|----------|-----|-------------|
| **API Base** | http://localhost:8000 | Root endpoint |
| **Health Check** | http://localhost:8000/health | API status |
| **Interactive Docs** | http://localhost:8000/docs | Swagger UI (recommended) |
| **Alternative Docs** | http://localhost:8000/redoc | ReDoc interface |

### Your First API Call

```bash
# Check if the API is running
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","version":"0.1.0"}
```

### Using the Interactive Documentation

1. Open http://localhost:8000/docs in your browser
2. You'll see all available endpoints with descriptions
3. Click on any endpoint to expand it
4. Click "Try it out" to test the endpoint
5. Fill in parameters and click "Execute"
6. View the response below

This is the easiest way to explore and test the API!

---

## API Reference

### Base URL
```
http://localhost:8000
```

### Response Format
All responses are in JSON format with appropriate HTTP status codes.

### HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| `200` | OK | Successful GET, PUT, PATCH requests |
| `201` | Created | Successful POST requests |
| `204` | No Content | Successful DELETE requests |
| `400` | Bad Request | Invalid input data or validation errors |
| `404` | Not Found | Resource doesn't exist |
| `422` | Unprocessable Entity | Request validation failed |
| `500` | Internal Server Error | Server-side errors |

---

### Health Check

#### Check API Health
```http
GET /health
```

Returns the API health status and version information.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

**Use Case**: Monitoring, health checks in production, CI/CD pipelines.

---

### Prompt Endpoints

#### List All Prompts
```http
GET /prompts
```

Retrieve all prompts with optional filtering and search.

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | No | Filter by collection ID |
| `search` | string | No | Search in title and description |

**Response** (200 OK):
```json
{
  "prompts": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Code Review Prompt",
      "content": "Review the following code:\n\n{{code}}",
      "description": "AI-powered code review",
      "collection_id": "abc123",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ],
  "total": 1
}
```

**Examples**:
```bash
# Get all prompts
curl http://localhost:8000/prompts

# Filter by collection
curl "http://localhost:8000/prompts?collection_id=abc123"

# Search prompts
curl "http://localhost:8000/prompts?search=code"

# Combine filters
curl "http://localhost:8000/prompts?collection_id=abc123&search=review"
```

---

#### Get Single Prompt
```http
GET /prompts/{prompt_id}
```

Retrieve a specific prompt by its ID.

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | Unique prompt identifier |

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Code Review Prompt",
  "content": "Review the following code:\n\n{{code}}",
  "description": "AI-powered code review",
  "collection_id": "abc123",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Prompt not found"
}
```

**Example**:
```bash
curl http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000
```

---

#### Create Prompt
```http
POST /prompts
```

Create a new prompt. ID and timestamps are auto-generated.

**Request Body**:
```json
{
  "title": "Code Review Prompt",
  "content": "Review the following code:\n\n{{code}}\n\nProvide feedback on:\n- Code quality\n- Best practices\n- Potential bugs",
  "description": "AI-powered code review assistant",
  "collection_id": "abc123"
}
```

**Field Validation**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | Yes | 1-200 characters |
| `content` | string | Yes | Minimum 1 character |
| `description` | string | No | Maximum 500 characters |
| `collection_id` | string | No | Must be valid collection ID |

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Code Review Prompt",
  "content": "Review the following code:\n\n{{code}}\n\nProvide feedback on:\n- Code quality\n- Best practices\n- Potential bugs",
  "description": "AI-powered code review assistant",
  "collection_id": "abc123",
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T10:30:00.123456"
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "Collection not found"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code Review Prompt",
    "content": "Review this code: {{code}}",
    "description": "AI code review"
  }'
```

---

#### Update Prompt (Full)
```http
PUT /prompts/{prompt_id}
```

Completely replace a prompt. All fields must be provided.

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | Unique prompt identifier |

**Request Body** (all fields required):
```json
{
  "title": "Updated Code Review",
  "content": "New content with {{variables}}",
  "description": "Updated description",
  "collection_id": null
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated Code Review",
  "content": "New content with {{variables}}",
  "description": "Updated description",
  "collection_id": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:45:00"
}
```

**Example**:
```bash
curl -X PUT http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content",
    "description": "Updated description",
    "collection_id": null
  }'
```

---

#### Update Prompt (Partial)
```http
PATCH /prompts/{prompt_id}
```

Update only specific fields. Omitted fields remain unchanged.

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | Unique prompt identifier |

**Request Body** (all fields optional):
```json
{
  "title": "New Title Only"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "New Title Only",
  "content": "Original content unchanged",
  "description": "Original description unchanged",
  "collection_id": "abc123",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T12:00:00"
}
```

**Examples**:
```bash
# Update only title
curl -X PATCH http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title"}'

# Update multiple fields
curl -X PATCH http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Title",
    "description": "New description"
  }'

# Remove from collection
curl -X PATCH http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{"collection_id": null}'
```

---

#### Delete Prompt
```http
DELETE /prompts/{prompt_id}
```

Permanently delete a prompt. This operation cannot be undone.

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | Unique prompt identifier |

**Response** (204 No Content):
```
(Empty response body)
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Prompt not found"
}
```

**Example**:
```bash
curl -X DELETE http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000
```

---

### Collection Endpoints

#### List All Collections
```http
GET /collections
```

Retrieve all collections.

**Response** (200 OK):
```json
{
  "collections": [
    {
      "id": "abc123",
      "name": "Development",
      "description": "Prompts for development tasks",
      "created_at": "2024-01-15T09:00:00"
    },
    {
      "id": "xyz789",
      "name": "Marketing",
      "description": "Marketing and content prompts",
      "created_at": "2024-01-15T09:15:00"
    }
  ],
  "total": 2
}
```

**Example**:
```bash
curl http://localhost:8000/collections
```

---

#### Get Single Collection
```http
GET /collections/{collection_id}
```

Retrieve a specific collection by its ID.

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | Yes | Unique collection identifier |

**Response** (200 OK):
```json
{
  "id": "abc123",
  "name": "Development",
  "description": "Prompts for development tasks",
  "created_at": "2024-01-15T09:00:00"
}
```

**Example**:
```bash
curl http://localhost:8000/collections/abc123
```

---

#### Create Collection
```http
POST /collections
```

Create a new collection. ID and timestamp are auto-generated.

**Request Body**:
```json
{
  "name": "Development",
  "description": "Prompts for development tasks"
}
```

**Field Validation**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | Yes | 1-100 characters |
| `description` | string | No | Maximum 500 characters |

**Response** (201 Created):
```json
{
  "id": "abc123",
  "name": "Development",
  "description": "Prompts for development tasks",
  "created_at": "2024-01-15T09:00:00.123456"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/collections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Development",
    "description": "Prompts for development tasks"
  }'
```

---

#### Delete Collection
```http
DELETE /collections/{collection_id}
```

Permanently delete a collection. Prompts in this collection will be uncategorized (collection_id set to null), but not deleted.

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | Yes | Unique collection identifier |

**Response** (204 No Content):
```
(Empty response body)
```

**Important**: Prompts in the deleted collection are NOT deleted, only uncategorized.

**Example**:
```bash
curl -X DELETE http://localhost:8000/collections/abc123
```

---

## Data Models

### Prompt Model

Complete prompt object with all fields:

```json
{
  "id": "string (UUID)",
  "title": "string (1-200 chars)",
  "content": "string (min 1 char)",
  "description": "string | null (max 500 chars)",
  "collection_id": "string | null",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

**Field Descriptions**:
- `id`: Auto-generated UUID4 identifier
- `title`: Short, descriptive name for the prompt
- `content`: The actual prompt text, can include template variables like `{{variable}}`
- `description`: Optional longer description of the prompt's purpose
- `collection_id`: Optional reference to a collection (null if uncategorized)
- `created_at`: Timestamp when prompt was created (UTC)
- `updated_at`: Timestamp of last update (UTC)

**Template Variables**:
Use double curly braces for variables: `{{variable_name}}`

Examples:
- `{{user_input}}` - User-provided input
- `{{context}}` - Contextual information
- `{{code}}` - Code snippet
- `{{language}}` - Programming language

---

### Collection Model

Complete collection object:

```json
{
  "id": "string (UUID)",
  "name": "string (1-100 chars)",
  "description": "string | null (max 500 chars)",
  "created_at": "datetime (ISO 8601)"
}
```

**Field Descriptions**:
- `id`: Auto-generated UUID4 identifier
- `name`: Collection name (e.g., "Development", "Marketing")
- `description`: Optional description of the collection's purpose
- `created_at`: Timestamp when collection was created (UTC)

---

### Response Models

#### PromptList Response
```json
{
  "prompts": [/* array of Prompt objects */],
  "total": 0
}
```

#### CollectionList Response
```json
{
  "collections": [/* array of Collection objects */],
  "total": 0
}
```

#### Health Response
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

## Code Examples

### Python Examples

#### Using `requests` library

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a collection
collection_data = {
    "name": "AI Development",
    "description": "Prompts for AI development tasks"
}
response = requests.post(f"{BASE_URL}/collections", json=collection_data)
collection = response.json()
print(f"Created collection: {collection['id']}")

# Create a prompt
prompt_data = {
    "title": "Code Review Assistant",
    "content": "Review the following {{language}} code:\n\n{{code}}\n\nProvide feedback on:\n1. Code quality\n2. Best practices\n3. Potential bugs\n4. Performance improvements",
    "description": "AI-powered code review with specific focus areas",
    "collection_id": collection['id']
}
response = requests.post(f"{BASE_URL}/prompts", json=prompt_data)
prompt = response.json()
print(f"Created prompt: {prompt['id']}")

# List all prompts in the collection
response = requests.get(f"{BASE_URL}/prompts", params={"collection_id": collection['id']})
prompts = response.json()
print(f"Found {prompts['total']} prompts in collection")

# Search prompts
response = requests.get(f"{BASE_URL}/prompts", params={"search": "code review"})
results = response.json()
print(f"Search found {results['total']} prompts")

# Update prompt title
update_data = {"title": "Enhanced Code Review Assistant"}
response = requests.patch(f"{BASE_URL}/prompts/{prompt['id']}", json=update_data)
updated_prompt = response.json()
print(f"Updated prompt title: {updated_prompt['title']}")

# Delete prompt
response = requests.delete(f"{BASE_URL}/prompts/{prompt['id']}")
print(f"Deleted prompt: {response.status_code == 204}")
```

---

#### Using `httpx` library (async)

```python
import httpx
import asyncio

BASE_URL = "http://localhost:8000"

async def main():
    async with httpx.AsyncClient() as client:
        # Create a prompt
        prompt_data = {
            "title": "SQL Query Generator",
            "content": "Generate a SQL query to {{action}} from table {{table}} where {{condition}}",
            "description": "Dynamic SQL query generation"
        }
        response = await client.post(f"{BASE_URL}/prompts", json=prompt_data)
        prompt = response.json()
        print(f"Created: {prompt['title']}")
        
        # Get the prompt
        response = await client.get(f"{BASE_URL}/prompts/{prompt['id']}")
        retrieved = response.json()
        print(f"Retrieved: {retrieved['title']}")
        
        # List all prompts
        response = await client.get(f"{BASE_URL}/prompts")
        all_prompts = response.json()
        print(f"Total prompts: {all_prompts['total']}")

asyncio.run(main())
```

---

### JavaScript/Node.js Examples

#### Using `fetch` API

```javascript
const BASE_URL = 'http://localhost:8000';

// Create a collection
async function createCollection() {
  const response = await fetch(`${BASE_URL}/collections`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'Marketing',
      description: 'Marketing and content prompts'
    })
  });
  const collection = await response.json();
  console.log('Created collection:', collection.id);
  return collection;
}

// Create a prompt
async function createPrompt(collectionId) {
  const response = await fetch(`${BASE_URL}/prompts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: 'Blog Post Generator',
      content: 'Write a blog post about {{topic}} targeting {{audience}}. Include:\n- Introduction\n- Main points\n- Conclusion\n- Call to action',
      description: 'Generate engaging blog posts',
      collection_id: collectionId
    })
  });
  const prompt = await response.json();
  console.log('Created prompt:', prompt.id);
  return prompt;
}

// Search prompts
async function searchPrompts(query) {
  const response = await fetch(`${BASE_URL}/prompts?search=${encodeURIComponent(query)}`);
  const results = await response.json();
  console.log(`Found ${results.total} prompts`);
  return results.prompts;
}

// Update prompt
async function updatePrompt(promptId, updates) {
  const response = await fetch(`${BASE_URL}/prompts/${promptId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  });
  const updated = await response.json();
  console.log('Updated prompt:', updated.title);
  return updated;
}

// Main execution
(async () => {
  const collection = await createCollection();
  const prompt = await createPrompt(collection.id);
  await searchPrompts('blog');
  await updatePrompt(prompt.id, { title: 'Advanced Blog Post Generator' });
})();
```

---

### cURL Examples

#### Complete Workflow

```bash
# 1. Check API health
curl http://localhost:8000/health

# 2. Create a collection
curl -X POST http://localhost:8000/collections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Data Science",
    "description": "Prompts for data analysis and ML"
  }'
# Save the collection ID from response

# 3. Create a prompt in the collection
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Data Analysis Assistant",
    "content": "Analyze the following dataset:\n\n{{dataset}}\n\nProvide insights on:\n- Trends\n- Anomalies\n- Recommendations",
    "description": "AI-powered data analysis",
    "collection_id": "YOUR_COLLECTION_ID"
  }'
# Save the prompt ID from response

# 4. List all prompts
curl http://localhost:8000/prompts

# 5. Filter prompts by collection
curl "http://localhost:8000/prompts?collection_id=YOUR_COLLECTION_ID"

# 6. Search prompts
curl "http://localhost:8000/prompts?search=analysis"

# 7. Get specific prompt
curl http://localhost:8000/prompts/YOUR_PROMPT_ID

# 8. Update prompt (partial)
curl -X PATCH http://localhost:8000/prompts/YOUR_PROMPT_ID \
  -H "Content-Type: application/json" \
  -d '{"title": "Advanced Data Analysis Assistant"}'

# 9. Update prompt (full)
curl -X PUT http://localhost:8000/prompts/YOUR_PROMPT_ID \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete Data Analysis",
    "content": "New content",
    "description": "New description",
    "collection_id": null
  }'

# 10. Delete prompt
curl -X DELETE http://localhost:8000/prompts/YOUR_PROMPT_ID

# 11. Delete collection
curl -X DELETE http://localhost:8000/collections/YOUR_COLLECTION_ID
```

---

## Project Structure

```
promptlab/
│
├── README.md                    # This comprehensive documentation
├── PROJECT_BRIEF.md             # Assignment requirements and details
├── GRADING_RUBRIC.md            # Grading criteria and point breakdown
│
├── backend/                     # Backend API application
│   ├── app/                     # Main application package
│   │   ├── __init__.py          # Package initialization with version
│   │   ├── api.py               # FastAPI routes and endpoints (300+ lines)
│   │   ├── models.py            # Pydantic data models and validation
│   │   ├── storage.py           # In-memory storage implementation
│   │   └── utils.py             # Helper functions (sorting, filtering, search)
│   │
│   ├── tests/                   # Test suite
│   │   ├── __init__.py          # Test package initialization
│   │   ├── conftest.py          # Pytest fixtures and configuration
│   │   ├── test_api.py          # API endpoint tests (80+ tests)
│   │   ├── test_models.py       # Model validation tests
│   │   ├── test_storage.py      # Storage layer tests
│   │   └── test_utils.py        # Utility function tests
│   │
│   ├── main.py                  # Application entry point
│   ├── requirements.txt         # Python dependencies
│   ├── venv/                    # Virtual environment (not in git)
│   └── .gitignore               # Git ignore rules
│
├── docs/                        # Additional documentation
│   └── API_REFERENCE.md         # Detailed API documentation
│
├── specs/                       # Feature specifications
│   └── .gitkeep                 # Placeholder for future specs
│
├── frontend/                    # Frontend application (Week 4)
│   └── .gitkeep                 # Placeholder for future frontend
│
├── .github/                     # GitHub configuration
│   └── workflows/               # CI/CD workflows (Week 3)
│
└── .gitignore                   # Root git ignore rules
```

### Key Files Explained

#### `backend/app/api.py`
- Defines all HTTP endpoints using FastAPI
- Handles request validation and error responses
- Implements business logic for CRUD operations
- Includes comprehensive docstrings

#### `backend/app/models.py`
- Pydantic models for data validation
- Defines request/response schemas
- Enforces field constraints (length, type, etc.)
- Auto-generates API documentation

#### `backend/app/storage.py`
- In-memory storage implementation
- Dictionary-based data structures for O(1) lookups
- Thread-safe operations
- Easy to extend with database backends

#### `backend/app/utils.py`
- Helper functions for common operations
- Sorting, filtering, and search logic
- Content validation
- Variable extraction from templates

#### `backend/tests/`
- Comprehensive test suite with 80+ tests
- Tests for all endpoints and edge cases
- Fixtures for test data
- Coverage reporting

---

## Development Guide

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/10x-engineer-project-repo.git
   cd 10x-engineer-project-repo
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set Up Virtual Environment**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

### Development Workflow

1. **Start Development Server**
   ```bash
   uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
   ```
   The `--reload` flag enables hot reloading on code changes.

2. **Make Changes**
   - Edit code in `backend/app/`
   - Server automatically reloads
   - Test changes in browser or with curl

3. **Write Tests**
   - Add tests in `backend/tests/`
   - Follow existing test patterns
   - Aim for 80%+ coverage

4. **Run Tests**
   ```bash
   # Run all tests
   pytest tests/ -v
   
   # Run specific test file
   pytest tests/test_api.py -v
   
   # Run with coverage
   pytest tests/ --cov=app --cov-report=term-missing
   
   # Run specific test
   pytest tests/test_api.py::test_create_prompt -v
   ```

### Code Style Guidelines

#### Python (PEP 8)
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use snake_case for functions and variables
- Use PascalCase for classes
- Add docstrings to all functions and classes

#### Example Function
```python
def create_prompt(prompt_data: PromptCreate) -> Prompt:
    """Create a new prompt with auto-generated ID.
    
    Args:
        prompt_data: The prompt data to create.
        
    Returns:
        Prompt: The newly created prompt object.
        
    Raises:
        HTTPException: If collection_id is invalid.
    """
    # Implementation here
    pass
```

### Commit Message Convention

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes (formatting)
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat(api): add PATCH endpoint for partial updates"
git commit -m "fix(storage): handle null collection_id correctly"
git commit -m "docs(readme): add code examples section"
git commit -m "test(api): add tests for error cases"
```

---

## Testing

### Running Tests

```bash
# Activate virtual environment
cd backend
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_api.py -v

# Run specific test class
pytest tests/test_api.py::TestPrompts -v

# Run specific test
pytest tests/test_api.py::TestPrompts::test_create_prompt -v

# Run tests matching pattern
pytest tests/ -k "create" -v
```

### Test Coverage

Current test coverage: **80%+**

```bash
# Generate detailed coverage report
pytest tests/ --cov=app --cov-report=html

# Open coverage report in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── test_api.py           # API endpoint tests
│   ├── TestHealth        # Health check tests
│   ├── TestPrompts       # Prompt CRUD tests
│   ├── TestCollections   # Collection CRUD tests
│   ├── TestPromptPatch   # PATCH endpoint tests
│   ├── TestPromptValidation  # Validation tests
│   └── TestPromptFiltering   # Filter/search tests
├── test_models.py        # Model validation tests
├── test_storage.py       # Storage layer tests
└── test_utils.py         # Utility function tests
```

### Writing Tests

Example test:

```python
def test_create_prompt(client):
    """Test creating a new prompt."""
    # Arrange
    prompt_data = {
        "title": "Test Prompt",
        "content": "Test content with {{variable}}",
        "description": "Test description"
    }
    
    # Act
    response = client.post("/prompts", json=prompt_data)
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == prompt_data["title"]
    assert data["content"] == prompt_data["content"]
    assert "id" in data
    assert "created_at" in data
```

### Test Fixtures

Available fixtures in `conftest.py`:

```python
@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)

@pytest.fixture
def sample_prompt():
    """Sample prompt data for testing."""
    return {
        "title": "Sample Prompt",
        "content": "Sample content",
        "description": "Sample description"
    }

@pytest.fixture
def sample_collection():
    """Sample collection data for testing."""
    return {
        "name": "Sample Collection",
        "description": "Sample description"
    }
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: `ModuleNotFoundError: No module named 'fastapi'`

**Cause**: Dependencies not installed or virtual environment not activated.

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

#### Issue: `Address already in use` when starting server

**Cause**: Port 8000 is already in use by another process.

**Solution 1** - Use a different port:
```bash
uvicorn app.api:app --port 8001 --reload
```

**Solution 2** - Kill the process using port 8000:
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

#### Issue: Tests failing with `ImportError`

**Cause**: Running tests from wrong directory or PYTHONPATH not set.

**Solution**:
```bash
# Ensure you're in the backend directory
cd backend

# Run tests with proper path
pytest tests/ -v

# Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/ -v
```

---

#### Issue: `404 Not Found` for all endpoints

**Cause**: Accessing wrong URL or server not running.

**Solution**:
1. Verify server is running: `curl http://localhost:8000/health`
2. Check server logs for errors
3. Ensure you're using correct base URL: `http://localhost:8000`

---

#### Issue: `422 Unprocessable Entity` when creating prompts

**Cause**: Request body doesn't match expected schema.

**Solution**:
1. Check required fields: `title` and `content` are required
2. Verify field constraints:
   - `title`: 1-200 characters
   - `content`: minimum 1 character
   - `description`: maximum 500 characters
3. Ensure JSON is properly formatted
4. Check API docs at http://localhost:8000/docs for exact schema

---

#### Issue: Virtual environment not activating on Windows

**Cause**: PowerShell execution policy restrictions.

**Solution**:
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
venv\Scripts\Activate.ps1
```

---

#### Issue: `Collection not found` error when creating prompt

**Cause**: Provided `collection_id` doesn't exist.

**Solution**:
1. Create collection first: `POST /collections`
2. Use the returned `id` in prompt creation
3. Or set `collection_id` to `null` for uncategorized prompts

---

### Getting Help

If you encounter issues not listed here:

1. **Check the logs**: Server logs often contain helpful error messages
2. **Review API docs**: http://localhost:8000/docs
3. **Run tests**: `pytest tests/ -v` to verify setup
4. **Check GitHub Issues**: Search for similar problems
5. **Ask for help**: Open a new issue with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version)
   - Relevant code snippets

---

## Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/10x-engineer-project-repo.git
   cd 10x-engineer-project-repo
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Your Changes**
   - Write clean, documented code
   - Follow the code style guidelines
   - Add tests for new features
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   cd backend
   source venv/bin/activate
   pytest tests/ -v --cov=app
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Describe your changes
   - Submit the PR

### Contribution Guidelines

#### Code Quality
- Write clean, readable code
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints

#### Testing
- Write tests for new features
- Ensure all tests pass
- Maintain or improve code coverage
- Test edge cases and error conditions

#### Documentation
- Update README.md if needed
- Add docstrings to new functions
- Update API documentation
- Include code examples

#### Commit Messages
- Use conventional commit format
- Write clear, descriptive messages
- Reference issues when applicable

### Areas for Contribution

- 🐛 **Bug Fixes**: Fix reported issues
- ✨ **New Features**: Add new functionality
- 📝 **Documentation**: Improve docs and examples
- 🧪 **Tests**: Add more test coverage
- 🎨 **UI/UX**: Improve API design
- ⚡ **Performance**: Optimize code
- 🔒 **Security**: Enhance security features

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow project guidelines

---

## Technology Stack

### Backend Framework
- **FastAPI 0.109.0**: Modern, fast web framework for building APIs
  - Automatic API documentation (Swagger UI, ReDoc)
  - Built-in data validation with Pydantic
  - Async support for high performance
  - Type hints for better IDE support

### Server
- **Uvicorn 0.27.0**: Lightning-fast ASGI server
  - Hot reload for development
  - Production-ready performance
  - WebSocket support
  - HTTP/2 support

### Data Validation
- **Pydantic 2.10+**: Data validation using Python type hints
  - Automatic request/response validation
  - Clear error messages
  - JSON schema generation
  - Type safety

### Testing
- **pytest 7.4.4**: Testing framework
  - Simple, powerful test syntax
  - Fixtures for test data
  - Parametrized testing
  - Plugin ecosystem

- **httpx 0.26.0**: HTTP client for testing
  - Async support
  - HTTP/2 support
  - Compatible with requests API

- **pytest-cov 4.1.0**: Coverage reporting
  - Line coverage
  - Branch coverage
  - HTML reports

### Storage
- **In-Memory**: Dictionary-based storage
  - Fast O(1) lookups
  - No external dependencies
  - Easy to extend with databases

### Future Enhancements
- **Database**: PostgreSQL, MongoDB, or SQLite
- **Authentication**: JWT tokens, OAuth2
- **Caching**: Redis for performance
- **Frontend**: React (Week 4)
- **Deployment**: Docker, Kubernetes

---

## Project Roadmap

### ✅ Week 1: Backend Foundation (Completed)
- [x] Fix existing bugs in CRUD operations
- [x] Implement PATCH endpoint for partial updates
- [x] Add comprehensive error handling
- [x] Write initial test suite

### ✅ Week 2: Documentation & Specifications (Current)
- [x] Create comprehensive README
- [x] Document all API endpoints
- [x] Add code examples in multiple languages
- [x] Write feature specifications
- [x] Create API reference documentation

### 🔄 Week 3: Testing & DevOps (Upcoming)
- [ ] Expand test coverage to 90%+
- [ ] Set up CI/CD pipeline with GitHub Actions
- [ ] Create Docker containers
- [ ] Add docker-compose for easy deployment
- [ ] Implement code quality checks (linting, formatting)
- [ ] Add performance benchmarks

### 📅 Week 4: Full-Stack Integration (Planned)
- [ ] Build React frontend
- [ ] Implement user interface for prompt management
- [ ] Add collection management UI
- [ ] Create search and filter interface
- [ ] Deploy full-stack application

---

## License

This project is part of an educational assignment for the 10x Engineer learning program.

### Educational Use
- This code is provided for learning purposes
- Feel free to study, modify, and experiment
- Use it as a reference for your own projects

### Attribution
If you use this code in your own projects, please provide attribution:
```
Based on PromptLab by [Your Name]
https://github.com/rohitpant-cloudkeeper/10x-engineer-project-repo
```

---

## Support and Resources

### Documentation
- **README.md**: This comprehensive guide (you are here!)
- **API Docs**: http://localhost:8000/docs (when server is running)
- **PROJECT_BRIEF.md**: Assignment requirements and details
- **GRADING_RUBRIC.md**: Grading criteria and point breakdown

### Getting Help
- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions and share ideas
- **Course Forum**: Connect with other students
- **Instructor**: Reach out for assignment-specific questions

### Useful Links
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [REST API Best Practices](https://restfulapi.net/)

---

## Acknowledgments

### Built With
- [FastAPI](https://fastapi.tiangolo.com/) - The web framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [Uvicorn](https://www.uvicorn.org/) - ASGI server
- [pytest](https://docs.pytest.org/) - Testing framework

### Inspiration
- Postman - API development platform
- Notion - Note-taking and organization
- GitHub Gists - Code snippet management

### Learning Resources
- 10x Engineer Program
- FastAPI Tutorial
- Python Documentation
- REST API Design Guidelines

---

## Contact

**Project Maintainer**: Rohit Pant  
**GitHub**: [@rohitpant-cloudkeeper](https://github.com/rohitpant-cloudkeeper)  
**Repository**: [10x-engineer-project-repo](https://github.com/rohitpant-cloudkeeper/10x-engineer-project-repo)

---

## Changelog

### Version 0.1.0 (Week 2)
- ✨ Comprehensive README with detailed documentation
- 📝 Complete API reference with examples
- 🔧 Code examples in Python, JavaScript, and cURL
- 📚 Development guide and contribution guidelines
- 🐛 Bug fixes and improvements from Week 1
- ✅ PATCH endpoint for partial updates
- 🧪 Expanded test suite

### Version 0.0.1 (Week 1)
- 🎉 Initial release
- ⚡ Basic CRUD operations for prompts
- 📁 Collection management
- 🔍 Search and filter functionality
- 🧪 Initial test suite

---

<div align="center">

**Built with ❤️ as part of the 10x Engineer learning project**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/rohitpant-cloudkeeper/10x-engineer-project-repo/issues) · [Request Feature](https://github.com/rohitpant-cloudkeeper/10x-engineer-project-repo/issues) · [Documentation](https://github.com/rohitpant-cloudkeeper/10x-engineer-project-repo/blob/main/README.md)

</div>
