# Feature Specification: Tagging System

**Status:** Proposed  
**Priority:** High  
**Estimated Effort:** Medium  
**Target Release:** Week 3

---

## Overview

Implement a flexible tagging system that allows users to add multiple tags to prompts for better organization, discovery, and filtering. Tags complement collections by providing a many-to-many relationship between prompts and categories.

### Problem Statement

Currently, prompts can only belong to one collection at a time. This limits organization because:
- A prompt might fit multiple categories
- Users can't filter by multiple criteria simultaneously
- Discovery is limited to collection-based browsing
- No way to categorize by topic, language, use case, etc.

### Proposed Solution

Add a tagging system where:
- Each prompt can have multiple tags
- Tags are simple string labels (e.g., "python", "code-review", "beginner")
- Users can filter prompts by one or more tags
- Tags are created automatically when first used
- Popular tags can be suggested to users

---

## User Stories

### User Story 1: Add Tags to Prompt

**As a** prompt engineer  
**I want to** add multiple tags to a prompt  
**So that** I can categorize it in multiple ways

**Acceptance Criteria:**
- [ ] Can add tags when creating a prompt
- [ ] Can add tags when updating a prompt
- [ ] Tags are case-insensitive (stored lowercase)
- [ ] Duplicate tags are automatically removed
- [ ] Tags can contain letters, numbers, and hyphens
- [ ] Maximum 10 tags per prompt
- [ ] Each tag is 1-30 characters

### User Story 2: Remove Tags from Prompt

**As a** prompt engineer  
**I want to** remove tags from a prompt  
**So that** I can keep tags relevant and up-to-date

**Acceptance Criteria:**
- [ ] Can remove individual tags via PATCH endpoint
- [ ] Can remove all tags by setting tags to empty array
- [ ] Removing a tag doesn't delete it from the system
- [ ] Other prompts with the same tag are unaffected

### User Story 3: Filter Prompts by Tags

**As a** prompt engineer  
**I want to** filter prompts by one or more tags  
**So that** I can find relevant prompts quickly

**Acceptance Criteria:**
- [ ] Can filter by single tag: `/prompts?tags=python`
- [ ] Can filter by multiple tags: `/prompts?tags=python,code-review`
- [ ] Multiple tags use AND logic (prompt must have all tags)
- [ ] Returns empty list if no prompts match
- [ ] Works with other filters (collection_id, search)

### User Story 4: List All Tags

**As a** prompt engineer  
**I want to** see all available tags  
**So that** I can discover existing tags and maintain consistency

**Acceptance Criteria:**
- [ ] API endpoint returns all unique tags
- [ ] Tags are sorted alphabetically
- [ ] Each tag shows usage count (how many prompts)
- [ ] Can filter tags by minimum usage count
- [ ] Empty system returns empty list

### User Story 5: Search Tags

**As a** prompt engineer  
**I want to** search for tags by name  
**So that** I can find relevant tags quickly

**Acceptance Criteria:**
- [ ] Can search tags by partial name match
- [ ] Search is case-insensitive
- [ ] Returns tags sorted by relevance (exact match first)
- [ ] Shows usage count for each tag

---

## Data Model Changes

### New Model: Tag

```python
class Tag(BaseModel):
    """A tag for categorizing prompts.
    
    Attributes:
        name (str): Tag name (lowercase, 1-30 chars).
        usage_count (int): Number of prompts using this tag.
        created_at (datetime): When tag was first used.
    """
    name: str = Field(..., min_length=1, max_length=30, pattern="^[a-z0-9-]+$")
    usage_count: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=get_current_time)
```

### Changes to Existing Models

**PromptBase Model:**
- Add `tags` field (List[str]) - list of tag names

```python
class PromptBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list, max_items=10)  # New field
```

**PromptCreate Model:**
- Inherits `tags` from PromptBase
- Tags are validated and normalized on creation

**PromptUpdate Model:**
- Inherits `tags` from PromptBase
- Can update tags with full replacement

**PromptPatch Model:**
- Add optional `tags` field for partial updates

```python
class PromptPatch(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: Optional[List[str]] = Field(None, max_items=10)  # New field
```

---

## API Endpoints

### 1. Create Prompt with Tags

**Endpoint:** `POST /prompts`

**Request Body:**

```json
{
  "title": "Python Code Review",
  "content": "Review this Python code: {{code}}",
  "description": "AI code review for Python",
  "collection_id": "col-uuid",
  "tags": ["python", "code-review", "quality-assurance"]
}
```

**Response:** `201 Created`

```json
{
  "id": "prompt-uuid",
  "title": "Python Code Review",
  "content": "Review this Python code: {{code}}",
  "description": "AI code review for Python",
  "collection_id": "col-uuid",
  "tags": ["python", "code-review", "quality-assurance"],
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

**Validation:**
- Tags are converted to lowercase
- Duplicate tags are removed
- Invalid characters are rejected (422 error)
- Maximum 10 tags enforced

---

### 2. Update Prompt Tags (Partial)

**Endpoint:** `PATCH /prompts/{prompt_id}`

**Request Body:**

```json
{
  "tags": ["python", "advanced", "code-review"]
}
```

**Response:** `200 OK`

Returns updated prompt with new tags.

---

### 3. Filter Prompts by Tags

**Endpoint:** `GET /prompts?tags={tag1},{tag2}`

**Query Parameters:**
- `tags` (string, optional): Comma-separated list of tags

**Examples:**

```bash
# Single tag
GET /prompts?tags=python

# Multiple tags (AND logic)
GET /prompts?tags=python,code-review

# Combined with other filters
GET /prompts?tags=python&collection_id=col-uuid&search=review
```

**Response:** `200 OK`

```json
{
  "prompts": [
    {
      "id": "prompt-uuid",
      "title": "Python Code Review",
      "tags": ["python", "code-review", "quality-assurance"],
      ...
    }
  ],
  "total": 1
}
```

---

### 4. List All Tags

**Endpoint:** `GET /tags`

**Query Parameters:**
- `min_usage` (int, optional): Minimum usage count (default: 1)
- `limit` (int, optional): Maximum tags to return (default: 100)
- `search` (string, optional): Search tags by name

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
    },
    {
      "name": "javascript",
      "usage_count": 8,
      "created_at": "2024-01-11T11:00:00Z"
    }
  ],
  "total": 3
}
```

---

### 5. Get Tag Details

**Endpoint:** `GET /tags/{tag_name}`

**Path Parameters:**
- `tag_name` (string, required): The tag name

**Response:** `200 OK`

```json
{
  "name": "python",
  "usage_count": 15,
  "created_at": "2024-01-10T09:00:00Z",
  "prompts": [
    {
      "id": "prompt-uuid-1",
      "title": "Python Code Review"
    },
    {
      "id": "prompt-uuid-2",
      "title": "Python Debugging"
    }
  ]
}
```

**Error Responses:**
- `404 Not Found`: Tag doesn't exist

---

### 6. Get Popular Tags

**Endpoint:** `GET /tags/popular?limit={n}`

**Query Parameters:**
- `limit` (int, optional): Number of tags to return (default: 10)

**Response:** `200 OK`

```json
{
  "tags": [
    {
      "name": "python",
      "usage_count": 15
    },
    {
      "name": "code-review",
      "usage_count": 12
    },
    {
      "name": "javascript",
      "usage_count": 8
    }
  ]
}
```

---

## Storage Changes

### New Storage Methods

```python
class Storage:
    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._tags: Dict[str, Tag] = {}  # New: tag_name -> Tag
    
    # Tag operations
    def get_all_tags(self) -> List[Tag]:
        """Get all tags sorted alphabetically."""
        
    def get_tag(self, tag_name: str) -> Optional[Tag]:
        """Get a specific tag by name."""
        
    def create_or_update_tag(self, tag_name: str) -> Tag:
        """Create tag if new, or increment usage count."""
        
    def update_tag_usage(self, tag_name: str, delta: int):
        """Update tag usage count (+1 or -1)."""
        
    def get_prompts_by_tag(self, tag_name: str) -> List[Prompt]:
        """Get all prompts with a specific tag."""
        
    def get_prompts_by_tags(self, tag_names: List[str]) -> List[Prompt]:
        """Get prompts that have ALL specified tags (AND logic)."""
```

---

## Tag Validation and Normalization

### Validation Rules

1. **Length:** 1-30 characters
2. **Characters:** Only lowercase letters, numbers, and hyphens
3. **Format:** Must match regex `^[a-z0-9-]+$`
4. **No spaces:** Use hyphens instead (e.g., "code-review")
5. **No special characters:** Only alphanumeric and hyphen

### Normalization Process

When a tag is submitted:

```python
def normalize_tag(tag: str) -> str:
    """Normalize a tag to standard format.
    
    1. Convert to lowercase
    2. Strip whitespace
    3. Replace spaces with hyphens
    4. Remove invalid characters
    5. Validate format
    """
    tag = tag.lower().strip()
    tag = tag.replace(" ", "-")
    tag = re.sub(r'[^a-z0-9-]', '', tag)
    
    if not re.match(r'^[a-z0-9-]+$', tag):
        raise ValueError(f"Invalid tag format: {tag}")
    
    if len(tag) < 1 or len(tag) > 30:
        raise ValueError(f"Tag length must be 1-30 characters: {tag}")
    
    return tag
```

### Examples

| Input | Normalized | Valid? |
|-------|------------|--------|
| "Python" | "python" | ✅ Yes |
| "Code Review" | "code-review" | ✅ Yes |
| "AI/ML" | "aiml" | ✅ Yes |
| "C++" | "c" | ⚠️ Yes (but loses meaning) |
| "test@tag" | "testtag" | ✅ Yes |
| "" | "" | ❌ No (too short) |
| "a" | "a" | ✅ Yes |

---

## Implementation Strategy

### Phase 1: Data Model (Week 3, Day 1)
1. Create `Tag` model
2. Add `tags` field to `Prompt` models
3. Add tag storage to `Storage` class
4. Write tag validation and normalization functions
5. Write unit tests for models

### Phase 2: Tag Management (Week 3, Day 2)
1. Update `create_prompt()` to handle tags
2. Update `update_prompt()` to handle tags
3. Update `patch_prompt()` to handle tags
4. Implement tag usage counting
5. Write tests for tag creation and updates

### Phase 3: Tag Filtering (Week 3, Day 3)
1. Modify `list_prompts()` to support tag filtering
2. Implement AND logic for multiple tags
3. Write tests for tag filtering

### Phase 4: Tag Endpoints (Week 3, Day 4)
1. Implement `GET /tags`
2. Implement `GET /tags/{name}`
3. Implement `GET /tags/popular`
4. Write tests for tag endpoints

### Phase 5: Tag Search (Week 3, Day 5)
1. Implement tag search functionality
2. Add tag suggestions
3. Write tests for tag search

---

## Edge Cases and Considerations

### Edge Case 1: Empty Tags Array
**Scenario:** User submits empty tags array `[]`  
**Solution:** Accept it, remove all tags from prompt.

### Edge Case 2: Duplicate Tags
**Scenario:** User submits `["python", "Python", "PYTHON"]`  
**Solution:** Normalize to `["python"]` (single tag).

### Edge Case 3: Invalid Tag Characters
**Scenario:** User submits `["C++", "AI/ML"]`  
**Solution:** Normalize to `["c", "aiml"]` or reject with 422 error.

### Edge Case 4: Too Many Tags
**Scenario:** User submits 15 tags (limit is 10)  
**Solution:** Return 422 validation error.

### Edge Case 5: Deleting Last Prompt with Tag
**Scenario:** Delete the only prompt using a tag  
**Solution:** Keep tag with usage_count=0, or delete tag automatically.

### Edge Case 6: Tag Name Conflicts
**Scenario:** Tags "ai" and "AI" are treated as same  
**Solution:** Correct, both normalize to "ai".

### Edge Case 7: Filtering by Non-Existent Tag
**Scenario:** Filter by tag that doesn't exist  
**Solution:** Return empty list (not an error).

---

## Testing Requirements

### Unit Tests
- [ ] Test tag normalization (lowercase, hyphen replacement)
- [ ] Test tag validation (length, characters)
- [ ] Test duplicate tag removal
- [ ] Test tag usage counting

### Integration Tests
- [ ] Test creating prompt with tags
- [ ] Test updating prompt tags (PUT and PATCH)
- [ ] Test filtering prompts by single tag
- [ ] Test filtering prompts by multiple tags (AND logic)
- [ ] Test GET /tags endpoint
- [ ] Test GET /tags/{name} endpoint
- [ ] Test GET /tags/popular endpoint
- [ ] Test tag search functionality

### Edge Case Tests
- [ ] Test empty tags array
- [ ] Test duplicate tags
- [ ] Test invalid tag characters
- [ ] Test too many tags (>10)
- [ ] Test tag normalization edge cases
- [ ] Test filtering by non-existent tag

---

## Search and Filter Combinations

### Supported Combinations

```bash
# Tags only
GET /prompts?tags=python

# Tags + Collection
GET /prompts?tags=python&collection_id=col-uuid

# Tags + Search
GET /prompts?tags=python&search=review

# Tags + Collection + Search
GET /prompts?tags=python,code-review&collection_id=col-uuid&search=advanced

# Multiple tags (AND logic)
GET /prompts?tags=python,advanced,code-review
# Returns prompts that have ALL three tags
```

### Filter Logic

```
Results = Prompts
  WHERE (tags CONTAINS ALL specified_tags)
  AND (collection_id = specified_collection OR no collection filter)
  AND (title/description CONTAINS search_term OR no search filter)
  ORDER BY created_at DESC
```

---

## Future Enhancements

### Version 2.0 Features
- **Tag Hierarchies:** Parent-child tag relationships (e.g., "python" > "python-3")
- **Tag Synonyms:** Map similar tags (e.g., "js" → "javascript")
- **Tag Colors:** Visual categorization with colors
- **Tag Descriptions:** Add descriptions to tags
- **Tag Suggestions:** AI-powered tag suggestions based on content
- **Tag Analytics:** Track tag usage over time

### Advanced Filtering
- **OR Logic:** Support filtering by any of multiple tags
- **NOT Logic:** Exclude prompts with certain tags
- **Tag Combinations:** Complex queries like "(python OR javascript) AND code-review"

---

## Success Metrics

- [ ] Users can add multiple tags to prompts
- [ ] Users can filter prompts by tags effectively
- [ ] Tag discovery is easy (list all tags, search tags)
- [ ] Tag usage is consistent (normalization works)
- [ ] API response times remain under 200ms

---

## Open Questions

1. Should we auto-delete tags with zero usage?
2. Should we limit the total number of unique tags in the system?
3. Should we allow tag renaming (affects all prompts)?
4. Should we support tag aliases/synonyms?
5. Should tags be case-sensitive or case-insensitive?

---

**Document Version:** 1.0  
**Last Updated:** 2024-01-15  
**Author:** PromptLab Team
