# PromptLab AI Coding Standards

This document provides coding standards and conventions for the PromptLab project. Follow these guidelines when contributing code or using AI assistants.

---

## Project Overview

PromptLab is a FastAPI-based REST API for managing AI prompt templates. The codebase emphasizes:
- Clean, readable code
- Comprehensive documentation
- Type safety with Python type hints
- RESTful API design principles

---

## Python Style Guide

### General Rules

- Follow **PEP 8** style guidelines
- Maximum line length: **100 characters**
- Use **4 spaces** for indentation (no tabs)
- Use **snake_case** for functions and variables
- Use **PascalCase** for classes
- Use **UPPER_CASE** for constants

### Type Hints

Always use type hints for function parameters and return values:

```python
# Good
def get_prompt(prompt_id: str) -> Optional[Prompt]:
    return storage.get_prompt(prompt_id)

# Bad
def get_prompt(prompt_id):
    return storage.get_prompt(prompt_id)
```

### Imports

Organize imports in this order:
1. Standard library imports
2. Third-party imports (FastAPI, Pydantic, etc.)
3. Local application imports

```python
# Standard library
from datetime import datetime
from typing import Optional, List

# Third-party
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Local
from app.models import Prompt, PromptCreate
from app.storage import storage
```

---

## Documentation Standards

### Docstring Format

Use **Google-style docstrings** for all functions, classes, and modules:

```python
def create_prompt(prompt_data: PromptCreate) -> Prompt:
    """Create a new prompt.
    
    Args:
        prompt_data: The prompt data (title, content, description, collection_id).
        
    Returns:
        Prompt: The newly created prompt with generated ID and timestamps.
        
    Raises:
        HTTPException: 400 if collection_id is invalid.
        
    Examples:
        >>> data = PromptCreate(title="Test", content="Content")
        >>> prompt = create_prompt(data)
    """
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)
```

### Docstring Requirements

- **Module docstrings**: Every Python file must have a module-level docstring
- **Class docstrings**: Include purpose and attributes with types
- **Function docstrings**: Include Args, Returns, Raises, and Examples sections
- **Type hints in docstrings**: Use format `name (type): description`
- **Examples section**: Use "Examples:" (plural), not "Example:"

### Class Documentation

```python
class Prompt(PromptBase):
    """Complete prompt model with metadata.
    
    Represents a full prompt object as stored and returned by the API.
    Includes auto-generated ID and timestamps in addition to base fields.
    
    Attributes:
        id (str): Unique identifier (auto-generated UUID4).
        created_at (datetime): Timestamp when prompt was created.
        updated_at (datetime): Timestamp when prompt was last updated.
    """
```

---

## FastAPI Conventions

### Endpoint Structure

```python
@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a specific prompt by ID.
    
    Args:
        prompt_id: The unique identifier of the prompt.
        
    Returns:
        Prompt: The requested prompt object.
        
    Raises:
        HTTPException: 404 if prompt not found.
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt
```

### HTTP Status Codes

Use appropriate status codes:
- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid input or business logic error
- **404 Not Found**: Resource doesn't exist
- **422 Unprocessable Entity**: Validation error (handled by Pydantic)

### Error Handling

Always use `HTTPException` for API errors:

```python
# Good
if not prompt:
    raise HTTPException(status_code=404, detail="Prompt not found")

# Bad
if not prompt:
    return {"error": "Not found"}
```

Error messages should be:
- Clear and descriptive
- User-friendly
- Consistent across the API

---

## Pydantic Models

### Model Organization

- **Base models**: Shared fields (e.g., `PromptBase`)
- **Create models**: For POST requests (e.g., `PromptCreate`)
- **Update models**: For PUT requests (e.g., `PromptUpdate`)
- **Patch models**: For PATCH requests with optional fields (e.g., `PromptPatch`)
- **Response models**: Complete objects with metadata (e.g., `Prompt`)

### Field Definitions

Always include:
- Field descriptions
- Validation constraints
- Default values where appropriate

```python
class PromptBase(BaseModel):
    """Base model for prompt data with common fields.
    
    Attributes:
        title (str): The prompt title (1-200 characters).
        content (str): The actual prompt text with optional template variables.
        description (Optional[str]): Optional description (max 500 chars).
        collection_id (Optional[str]): Optional ID linking to a collection.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Prompt title")
    content: str = Field(..., min_length=1, description="Prompt content with optional {{variables}}")
    description: Optional[str] = Field(None, max_length=500, description="Optional prompt description")
    collection_id: Optional[str] = Field(None, description="ID of the collection this prompt belongs to")
```

---

## Testing Standards

### Test Organization

- Place tests in `backend/tests/`
- Use `test_*.py` naming convention
- Group tests by functionality using classes

```python
class TestPrompts:
    def test_create_prompt(self, client):
        """Test creating a new prompt."""
        # Test implementation
        
    def test_get_prompt_not_found(self, client):
        """Test getting a non-existent prompt returns 404."""
        # Test implementation
```

### Test Requirements

- Write tests for all new features
- Test both success and error cases
- Use pytest fixtures for test data
- Aim for **80%+ code coverage**
- Use descriptive test names that explain what is being tested

### Test Structure

Follow the Arrange-Act-Assert pattern:

```python
def test_create_prompt(self, client, sample_prompt_data):
    # Arrange
    data = sample_prompt_data
    
    # Act
    response = client.post("/prompts", json=data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]
```

---

## Code Organization

### File Structure

```
backend/
├── app/
│   ├── __init__.py          # Package initialization with version
│   ├── api.py               # FastAPI routes and endpoints
│   ├── models.py            # Pydantic data models
│   ├── storage.py           # Data storage layer
│   └── utils.py             # Helper functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   └── test_api.py          # API endpoint tests
└── main.py                  # Application entry point
```

### Function Length

- Keep functions under **20 lines** when possible
- Extract complex logic into helper functions
- One function should do one thing

### Variable Naming

```python
# Good
prompt_id = "abc123"
user_input = request.json()
is_valid = validate_content(content)

# Bad
p = "abc123"
data = request.json()
flag = validate_content(content)
```

---

## API Design Principles

### RESTful Conventions

- Use plural nouns for resources: `/prompts`, `/collections`
- Use HTTP methods correctly: GET (read), POST (create), PUT (full update), PATCH (partial update), DELETE (remove)
- Return appropriate status codes
- Use query parameters for filtering: `/prompts?collection_id=123`

### Request/Response Format

- Always use JSON for request and response bodies
- Include timestamps in ISO 8601 format
- Use UUIDs for resource identifiers
- Return consistent error formats

### Endpoint Naming

```python
# Good
GET    /prompts              # List all prompts
GET    /prompts/{id}         # Get single prompt
POST   /prompts              # Create prompt
PUT    /prompts/{id}         # Full update
PATCH  /prompts/{id}         # Partial update
DELETE /prompts/{id}         # Delete prompt

# Bad
GET    /get_prompts
POST   /create_prompt
GET    /prompt/{id}
```

---

## Data Validation

### Input Validation

- Use Pydantic models for automatic validation
- Define constraints in Field definitions
- Validate business logic in endpoint functions

```python
# Model validation
title: str = Field(..., min_length=1, max_length=200)

# Business logic validation
if prompt_data.collection_id:
    collection = storage.get_collection(prompt_data.collection_id)
    if not collection:
        raise HTTPException(status_code=400, detail="Collection not found")
```

### Output Validation

- Always specify `response_model` in endpoint decorators
- Let Pydantic handle serialization
- Ensure timestamps are properly formatted

---

## Security Best Practices

### Current Implementation

- No authentication (development only)
- CORS enabled for all origins (development only)
- Input validation via Pydantic

### Production Considerations

When moving to production:
- Implement authentication (JWT, API keys, OAuth)
- Restrict CORS to specific origins
- Add rate limiting
- Implement request logging
- Use HTTPS only
- Validate and sanitize all inputs

---

## Performance Guidelines

### Database Queries

- Currently using in-memory storage
- When migrating to a database:
  - Use connection pooling
  - Implement pagination for list endpoints
  - Add indexes on frequently queried fields
  - Use async database drivers

### Response Optimization

- Return only necessary fields
- Implement pagination for large result sets
- Use appropriate HTTP caching headers

---

## Git Commit Conventions

Use conventional commit format:

```
type: brief description

- Detailed change 1
- Detailed change 2

Addresses Task X.Y: Description
```

### Commit Types

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `chore:` Maintenance tasks
- `style:` Code style changes (formatting)

### Examples

```
feat: implement PATCH endpoint for partial updates

- Add PromptPatch model with optional fields
- Implement patch_prompt endpoint
- Update only provided fields
- Update updated_at timestamp

Addresses Task 1.6: Missing PATCH endpoint
```

---

## Common Patterns

### Creating Resources

```python
@app.post("/resource", response_model=Resource, status_code=201)
def create_resource(data: ResourceCreate):
    """Create a new resource."""
    # Validate references
    if data.foreign_key:
        if not storage.get_related(data.foreign_key):
            raise HTTPException(status_code=400, detail="Related resource not found")
    
    # Create resource
    resource = Resource(**data.model_dump())
    return storage.create_resource(resource)
```

### Updating Resources

```python
@app.put("/resource/{id}", response_model=Resource)
def update_resource(id: str, data: ResourceUpdate):
    """Fully update a resource."""
    # Check existence
    existing = storage.get_resource(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Update with new data
    updated = Resource(
        id=existing.id,
        **data.model_dump(),
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    return storage.update_resource(id, updated)
```

### Partial Updates

```python
@app.patch("/resource/{id}", response_model=Resource)
def patch_resource(id: str, data: ResourcePatch):
    """Partially update a resource."""
    existing = storage.get_resource(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Only update provided fields
    update_data = data.model_dump(exclude_unset=True)
    
    updated = Resource(
        id=existing.id,
        field1=update_data.get('field1', existing.field1),
        field2=update_data.get('field2', existing.field2),
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    return storage.update_resource(id, updated)
```

---

## Don'ts - Common Mistakes to Avoid

❌ Don't use generic exception handling
❌ Don't return different response formats for the same endpoint
❌ Don't ignore type hints
❌ Don't skip docstrings
❌ Don't use mutable default arguments
❌ Don't hardcode configuration values
❌ Don't ignore validation errors
❌ Don't use `print()` for logging (use proper logging)
❌ Don't commit commented-out code
❌ Don't use `import *`

---

## Questions or Clarifications?

For questions about these standards:
1. Check existing code for examples
2. Review the PROJECT_BRIEF.md
3. Consult the API_REFERENCE.md
4. Ask in code reviews

---

**Last Updated:** 2024-01-15  
**Version:** 1.0.0
