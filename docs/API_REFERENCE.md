# PromptLab API Reference

Complete API documentation for the PromptLab REST API.

**Base URL:** `http://localhost:8000`

**Version:** 0.1.0

---

## Table of Contents

- [Authentication](#authentication)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Health Check](#health-check)
- [Prompts](#prompts)
- [Collections](#collections)
- [Tags](#tags)
- [Version History](#version-history)

---

## Authentication

**Current Status:** No authentication required.

All endpoints are currently open and do not require authentication. In a production environment, you would implement authentication using:
- API Keys
- JWT tokens
- OAuth 2.0

---

## Response Format

All responses are returned in JSON format with appropriate HTTP status codes.

### Success Response Structure

```json
{
  "id": "string",
  "field1": "value1",
  "field2": "value2"
}
```

### List Response Structure

```json
{
  "items": [...],
  "total": 10
}
```

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request succeeded, no content to return |
| 400 | Bad Request | Invalid request data or parameters |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

### Common Error Examples

**404 Not Found:**
```json
{
  "detail": "Prompt not found"
}
```

**400 Bad Request:**
```json
{
  "detail": "Collection not found"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Health Check

### Check API Health

Check if the API is running and get version information.

**Endpoint:** `GET /health`

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

**Example Request:**

```bash
curl http://localhost:8000/health
```

**Example Response:**

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

## Prompts

### List All Prompts

Retrieve all prompts with optional filtering.

**Endpoint:** `GET /prompts`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_id | string | No | Filter by collection ID |
| search | string | No | Search in title and description |
| tags | string | No | Comma-separated list of tags (AND logic) |

**Response:** `200 OK`

```json
{
  "prompts": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Code Review Prompt",
      "content": "Review the following code:\n\n{{code}}",
      "description": "AI code review assistant",
      "collection_id": "660e8400-e29b-41d4-a716-446655440000",
      "tags": ["python", "code-review"],
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1
}
```

**Example Requests:**

```bash
# Get all prompts
curl http://localhost:8000/prompts

# Filter by collection
curl "http://localhost:8000/prompts?collection_id=660e8400-e29b-41d4-a716-446655440000"

# Search prompts
curl "http://localhost:8000/prompts?search=code+review"

# Filter by tags (single tag)
curl "http://localhost:8000/prompts?tags=python"

# Filter by multiple tags (AND logic)
curl "http://localhost:8000/prompts?tags=python,code-review"

# Combine filters
curl "http://localhost:8000/prompts?tags=python&collection_id=660e8400-e29b-41d4-a716-446655440000&search=review"
```

---

### Get Single Prompt

Retrieve a specific prompt by ID.

**Endpoint:** `GET /prompts/{prompt_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Response:** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Code Review Prompt",
  "content": "Review the following code:\n\n{{code}}",
  "description": "AI code review assistant",
  "collection_id": "660e8400-e29b-41d4-a716-446655440000",
  "tags": ["python", "code-review"],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**

- `404 Not Found` - Prompt does not exist

**Example Request:**

```bash
curl http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000
```

---

### Create Prompt

Create a new prompt.

**Endpoint:** `POST /prompts`

**Request Body:**

```json
{
  "title": "Code Review Prompt",
  "content": "Review the following code:\n\n{{code}}",
  "description": "AI code review assistant",
  "collection_id": "660e8400-e29b-41d4-a716-446655440000",
  "tags": ["python", "code-review"]
}
```

**Field Specifications:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| title | string | Yes | 1-200 chars | Prompt title |
| content | string | Yes | Min 1 char | Prompt content with optional {{variables}} |
| description | string | No | Max 500 chars | Optional description |
| collection_id | string | No | Valid UUID | Optional collection reference |
| tags | array | No | Max 10 tags, 1-30 chars each | Optional tags for categorization |

**Response:** `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Code Review Prompt",
  "content": "Review the following code:\n\n{{code}}",
  "description": "AI code review assistant",
  "collection_id": "660e8400-e29b-41d4-a716-446655440000",
  "tags": ["python", "code-review"],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**

- `400 Bad Request` - Invalid collection_id
- `422 Unprocessable Entity` - Validation error

**Example Request:**

```bash
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code Review Prompt",
    "content": "Review the following code:\n\n{{code}}",
    "description": "AI code review assistant"
  }'
```

---

### Update Prompt (Full)

Fully update an existing prompt. All fields must be provided.

**Endpoint:** `PUT /prompts/{prompt_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Request Body:**

```json
{
  "title": "Updated Code Review Prompt",
  "content": "Review this code and provide feedback:\n\n{{code}}",
  "description": "Enhanced AI code review assistant",
  "collection_id": null
}
```

**Response:** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated Code Review Prompt",
  "content": "Review this code and provide feedback:\n\n{{code}}",
  "description": "Enhanced AI code review assistant",
  "collection_id": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:45:00Z"
}
```

**Error Responses:**

- `404 Not Found` - Prompt does not exist
- `400 Bad Request` - Invalid collection_id
- `422 Unprocessable Entity` - Validation error

**Example Request:**

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

### Update Prompt (Partial)

Partially update an existing prompt. Only provided fields are updated.

**Endpoint:** `PATCH /prompts/{prompt_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Request Body:**

All fields are optional. Only include fields you want to update.

```json
{
  "title": "New Title"
}
```

**Response:** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "New Title",
  "content": "Review the following code:\n\n{{code}}",
  "description": "AI code review assistant",
  "collection_id": "660e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

**Error Responses:**

- `404 Not Found` - Prompt does not exist
- `400 Bad Request` - Invalid collection_id
- `422 Unprocessable Entity` - Validation error

**Example Requests:**

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
```

---

### Delete Prompt

Delete a prompt permanently.

**Endpoint:** `DELETE /prompts/{prompt_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Response:** `204 No Content`

No response body.

**Error Responses:**

- `404 Not Found` - Prompt does not exist

**Example Request:**

```bash
curl -X DELETE http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000
```

---

## Collections

### List All Collections

Retrieve all collections.

**Endpoint:** `GET /collections`

**Response:** `200 OK`

```json
{
  "collections": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "name": "Development",
      "description": "Prompts for development tasks",
      "created_at": "2024-01-15T09:00:00Z"
    }
  ],
  "total": 1
}
```

**Example Request:**

```bash
curl http://localhost:8000/collections
```

---

### Get Single Collection

Retrieve a specific collection by ID.

**Endpoint:** `GET /collections/{collection_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_id | string | Yes | Unique collection identifier |

**Response:** `200 OK`

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "name": "Development",
  "description": "Prompts for development tasks",
  "created_at": "2024-01-15T09:00:00Z"
}
```

**Error Responses:**

- `404 Not Found` - Collection does not exist

**Example Request:**

```bash
curl http://localhost:8000/collections/660e8400-e29b-41d4-a716-446655440000
```

---

### Create Collection

Create a new collection.

**Endpoint:** `POST /collections`

**Request Body:**

```json
{
  "name": "Development",
  "description": "Prompts for development tasks"
}
```

**Field Specifications:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| name | string | Yes | 1-100 chars | Collection name |
| description | string | No | Max 500 chars | Optional description |

**Response:** `201 Created`

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "name": "Development",
  "description": "Prompts for development tasks",
  "created_at": "2024-01-15T09:00:00Z"
}
```

**Error Responses:**

- `422 Unprocessable Entity` - Validation error

**Example Request:**

```bash
curl -X POST http://localhost:8000/collections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Development",
    "description": "Prompts for development tasks"
  }'
```

---

### Delete Collection

Delete a collection permanently. All prompts in this collection will have their `collection_id` set to `null` (uncategorized).

**Endpoint:** `DELETE /collections/{collection_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_id | string | Yes | Unique collection identifier |

**Response:** `204 No Content`

No response body.

**Error Responses:**

- `404 Not Found` - Collection does not exist

**Note:** Prompts belonging to the deleted collection are not deleted. They become uncategorized (collection_id = null).

**Example Request:**

```bash
curl -X DELETE http://localhost:8000/collections/660e8400-e29b-41d4-a716-446655440000
```

---

## Tags

### List All Tags

Retrieve all tags with optional search filtering.

**Endpoint:** `GET /tags`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| search | string | No | Search tags by name (partial match) |

**Response:** `200 OK`

```json
{
  "tags": [
    {
      "name": "python",
      "usage_count": 15,
      "created_at": "2024-01-10T09:00:00Z"
    },
    {
      "name": "code-review",
      "usage_count": 12,
      "created_at": "2024-01-10T10:00:00Z"
    }
  ],
  "total": 2
}
```

**Example Requests:**

```bash
# Get all tags
curl http://localhost:8000/tags

# Search tags
curl "http://localhost:8000/tags?search=python"
```

---

### Get Tag Details

Retrieve a specific tag by name.

**Endpoint:** `GET /tags/{tag_name}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tag_name | string | Yes | Tag name |

**Response:** `200 OK`

```json
{
  "name": "python",
  "usage_count": 15,
  "created_at": "2024-01-10T09:00:00Z"
}
```

**Error Responses:**

- `404 Not Found` - Tag does not exist

**Example Request:**

```bash
curl http://localhost:8000/tags/python
```

---

### Get Popular Tags

Retrieve popular tags sorted by usage count.

**Endpoint:** `GET /tags/popular`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of tags to return (default: 10) |

**Response:** `200 OK`

```json
{
  "tags": [
    {
      "name": "python",
      "usage_count": 15,
      "created_at": "2024-01-10T09:00:00Z"
    },
    {
      "name": "code-review",
      "usage_count": 12,
      "created_at": "2024-01-10T10:00:00Z"
    }
  ],
  "total": 2
}
```

**Example Request:**

```bash
curl "http://localhost:8000/tags/popular?limit=5"
```

---

## Version History

PromptLab automatically tracks the complete history of every prompt. Every update (PUT/PATCH) creates a new version, allowing you to view history, compare changes, and revert to previous states.

### List Prompt Versions

Retrieve all versions of a specific prompt.

**Endpoint:** `GET /prompts/{prompt_id}/versions`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum number of versions to return (default: 50) |
| offset | integer | No | Number of versions to skip (default: 0) |

**Response:** `200 OK`

```json
{
  "versions": [
    {
      "id": "version-uuid-2",
      "prompt_id": "prompt-uuid",
      "version": 2,
      "title": "Updated Title",
      "content": "Updated content",
      "description": "Updated description",
      "collection_id": "collection-uuid",
      "tags": ["python", "updated"],
      "created_at": "2024-01-15T11:00:00Z",
      "created_by": null
    },
    {
      "id": "version-uuid-1",
      "prompt_id": "prompt-uuid",
      "version": 1,
      "title": "Original Title",
      "content": "Original content",
      "description": "Original description",
      "collection_id": null,
      "tags": ["python"],
      "created_at": "2024-01-15T10:00:00Z",
      "created_by": null
    }
  ],
  "total": 2,
  "prompt_id": "prompt-uuid"
}
```

**Error Responses:**

- `404 Not Found` - Prompt does not exist

**Example Requests:**

```bash
# Get all versions
curl "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions"

# Get with pagination
curl "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions?limit=10&offset=5"
```

---

### Get Specific Version

Retrieve a specific version of a prompt by version number.

**Endpoint:** `GET /prompts/{prompt_id}/versions/{version}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |
| version | integer | Yes | Version number to retrieve |

**Response:** `200 OK`

```json
{
  "id": "version-uuid-1",
  "prompt_id": "prompt-uuid",
  "version": 1,
  "title": "Original Title",
  "content": "Original content",
  "description": "Original description",
  "collection_id": null,
  "tags": ["python"],
  "created_at": "2024-01-15T10:00:00Z",
  "created_by": null
}
```

**Error Responses:**

- `404 Not Found` - Prompt or version does not exist

**Example Request:**

```bash
curl "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions/1"
```

---

### Revert to Version

Revert a prompt to a previous version. This creates a new version with the content from the specified version, preserving all history.

**Endpoint:** `POST /prompts/{prompt_id}/versions/{version}/revert`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |
| version | integer | Yes | Version number to revert to |

**Response:** `200 OK`

Returns the updated prompt with a new version number.

```json
{
  "id": "prompt-uuid",
  "title": "Original Title",
  "content": "Original content",
  "description": "Original description",
  "collection_id": null,
  "tags": ["python"],
  "version": 3,
  "version_count": 3,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

**Error Responses:**

- `404 Not Found` - Prompt or version does not exist
- `400 Bad Request` - Trying to revert to current version

**Example Request:**

```bash
curl -X POST "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions/1/revert"
```

**Notes:**

- Reverting to version N creates a new version (N+1) with version N's content
- No history is deleted - all versions are preserved
- Cannot revert to the current version
- Tags and collection are also restored from the target version

---

### Compare Versions

Compare two versions of a prompt to see what changed.

**Endpoint:** `GET /prompts/{prompt_id}/versions/compare`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| from | integer | Yes | First version number |
| to | integer | Yes | Second version number |

**Response:** `200 OK`

```json
{
  "prompt_id": "prompt-uuid",
  "from_version": {
    "id": "version-uuid-1",
    "prompt_id": "prompt-uuid",
    "version": 1,
    "title": "Original Title",
    "content": "Original content",
    "description": "Original description",
    "collection_id": null,
    "tags": ["python"],
    "created_at": "2024-01-15T10:00:00Z",
    "created_by": null
  },
  "to_version": {
    "id": "version-uuid-2",
    "prompt_id": "prompt-uuid",
    "version": 2,
    "title": "Updated Title",
    "content": "Updated content",
    "description": "Original description",
    "collection_id": "collection-uuid",
    "tags": ["python", "updated"],
    "created_at": "2024-01-15T11:00:00Z",
    "created_by": null
  },
  "changes": {
    "title": "changed",
    "content": "changed",
    "description": "unchanged",
    "collection_id": "changed",
    "tags": "changed"
  }
}
```

**Error Responses:**

- `404 Not Found` - Prompt or either version does not exist

**Example Request:**

```bash
curl "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions/compare?from=1&to=2"
```

**Notes:**

- The `changes` object shows which fields changed between versions
- Values are either "changed" or "unchanged"
- Useful for understanding what was modified in an update

---

## Data Models

### Prompt Model

```json
{
  "id": "string (UUID)",
  "title": "string (1-200 chars)",
  "content": "string (min 1 char)",
  "description": "string | null (max 500 chars)",
  "collection_id": "string | null (UUID)",
  "tags": "array of strings (max 10, each 1-30 chars, lowercase alphanumeric and hyphens)",
  "version": "integer (current version number, starts at 1)",
  "version_count": "integer (total number of versions)",
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

**Tag Validation Rules:**
- Tags are automatically normalized to lowercase
- Spaces are replaced with hyphens
- Only alphanumeric characters and hyphens allowed
- Each tag must be 1-30 characters
- Maximum 10 tags per prompt
- Duplicate tags are automatically removed

**Version Tracking:**
- `version`: Current version number (increments with each update)
- `version_count`: Total number of versions created
- Every PUT/PATCH operation creates a new version
- Initial creation starts at version 1

### PromptVersion Model

```json
{
  "id": "string (UUID)",
  "prompt_id": "string (UUID)",
  "version": "integer (version number, must be positive)",
  "title": "string (1-200 chars)",
  "content": "string (min 1 char)",
  "description": "string | null (max 500 chars)",
  "collection_id": "string | null (UUID)",
  "tags": "array of strings (max 10, each 1-30 chars)",
  "created_at": "string (ISO 8601 datetime)",
  "created_by": "string | null (future: user who created this version)"
}
```

### Tag Model

```json
{
  "name": "string (1-30 chars, lowercase alphanumeric and hyphens)",
  "usage_count": "integer (non-negative)",
  "created_at": "string (ISO 8601 datetime)"
}
```

### Collection Model

```json
{
  "id": "string (UUID)",
  "name": "string (1-100 chars)",
  "description": "string | null (max 500 chars)",
  "created_at": "string (ISO 8601 datetime)"
}
```

---

## Rate Limiting

**Current Status:** No rate limiting implemented.

In a production environment, consider implementing rate limiting to prevent abuse:
- Per IP address
- Per API key
- Per user account

---

## Pagination

**Current Status:** No pagination implemented.

All list endpoints return all results. In a production environment with large datasets, implement pagination using:
- `limit` and `offset` query parameters
- Cursor-based pagination
- Page-based pagination

---

## Interactive Documentation

The API provides interactive documentation powered by Swagger UI:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These interfaces allow you to:
- Explore all endpoints
- Test API calls directly from the browser
- View request/response schemas
- See example values

---

## SDK and Client Libraries

**Current Status:** No official SDKs available.

You can use any HTTP client library to interact with the API:

**Python:**
```python
import requests

response = requests.get("http://localhost:8000/prompts")
prompts = response.json()
```

**JavaScript:**
```javascript
fetch('http://localhost:8000/prompts')
  .then(response => response.json())
  .then(data => console.log(data));
```

**cURL:**
```bash
curl http://localhost:8000/prompts
```

---

## Changelog

### Version 0.1.0 (Current)

- Initial API release
- CRUD operations for prompts
- CRUD operations for collections
- Tagging system with tag management
- Tag filtering with AND logic
- Automatic version tracking for all prompts
- Version history with pagination
- Version comparison
- Version revert functionality
- Search and filter functionality
- Partial update support (PATCH)
- Comprehensive test coverage (99%, 220 tests)
- CI/CD pipeline with GitHub Actions

---

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check the main README.md
- Review the PROJECT_BRIEF.md

---

**Last Updated:** 2024-01-15
