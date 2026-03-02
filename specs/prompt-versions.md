# Feature Specification: Prompt Version Tracking

**Status:** Proposed  
**Priority:** High  
**Estimated Effort:** Medium  
**Target Release:** Week 3

---

## Overview

Implement version tracking for prompts to maintain a complete history of changes. This allows users to view previous versions, compare changes, and revert to earlier versions if needed.

### Problem Statement

Currently, when a prompt is updated, the previous version is lost. Users cannot:
- See what a prompt looked like before changes
- Track who made changes and when
- Revert to a previous version if a change was incorrect
- Compare different versions side-by-side

### Proposed Solution

Add a versioning system that automatically creates a new version entry whenever a prompt is updated. Each version stores the complete prompt state at that point in time.

---

## User Stories

### User Story 1: Automatic Version Creation

**As a** prompt engineer  
**I want** versions to be created automatically when I update a prompt  
**So that** I don't have to manually manage version history

**Acceptance Criteria:**
- [ ] When a prompt is updated via PUT or PATCH, a new version is created
- [ ] The version includes the complete prompt state (title, content, description)
- [ ] Version number increments automatically (1, 2, 3, ...)
- [ ] Original prompt's `updated_at` timestamp is updated
- [ ] Version creation happens transparently without extra API calls

### User Story 2: View Version History

**As a** prompt engineer  
**I want to** view all versions of a prompt  
**So that** I can see how it evolved over time

**Acceptance Criteria:**
- [ ] API endpoint returns all versions for a specific prompt
- [ ] Versions are sorted by version number (newest first)
- [ ] Each version shows: version number, content, timestamp
- [ ] Response includes total version count
- [ ] Empty history returns empty list (not an error)

### User Story 3: View Specific Version

**As a** prompt engineer  
**I want to** view a specific version of a prompt  
**So that** I can see exactly what it looked like at that point

**Acceptance Criteria:**
- [ ] API endpoint accepts prompt ID and version number
- [ ] Returns complete version data
- [ ] Returns 404 if version doesn't exist
- [ ] Version data includes all prompt fields as they were

### User Story 4: Revert to Previous Version

**As a** prompt engineer  
**I want to** revert a prompt to a previous version  
**So that** I can undo unwanted changes

**Acceptance Criteria:**
- [ ] API endpoint accepts prompt ID and version number to revert to
- [ ] Creates a new version with the old content (doesn't delete history)
- [ ] Updates the current prompt with the old version's data
- [ ] Returns the updated prompt
- [ ] Returns 404 if version doesn't exist

### User Story 5: Compare Versions

**As a** prompt engineer  
**I want to** compare two versions of a prompt  
**So that** I can see what changed between them

**Acceptance Criteria:**
- [ ] API endpoint accepts prompt ID and two version numbers
- [ ] Returns both versions' data
- [ ] Optionally includes a diff of changes
- [ ] Returns 404 if either version doesn't exist

---

## Data Model Changes

### New Model: PromptVersion

```python
class PromptVersion(BaseModel):
    """A historical version of a prompt.
    
    Attributes:
        id (str): Unique version identifier (UUID).
        prompt_id (str): ID of the parent prompt.
        version (int): Version number (1, 2, 3, ...).
        title (str): Prompt title at this version.
        content (str): Prompt content at this version.
        description (Optional[str]): Prompt description at this version.
        collection_id (Optional[str]): Collection ID at this version.
        created_at (datetime): When this version was created.
        created_by (Optional[str]): User who created this version (future).
    """
    id: str = Field(default_factory=generate_id)
    prompt_id: str
    version: int
    title: str
    content: str
    description: Optional[str] = None
    collection_id: Optional[str] = None
    created_at: datetime = Field(default_factory=get_current_time)
    created_by: Optional[str] = None  # For future authentication
```

### Changes to Existing Models

**Prompt Model:**
- Add `version` field (int) - current version number
- Add `version_count` field (int) - total number of versions

```python
class Prompt(PromptBase):
    id: str = Field(default_factory=generate_id)
    version: int = Field(default=1, description="Current version number")
    version_count: int = Field(default=1, description="Total number of versions")
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)
```

---

## API Endpoints

### 1. List Prompt Versions

**Endpoint:** `GET /prompts/{prompt_id}/versions`

**Description:** Retrieve all versions of a specific prompt.

**Path Parameters:**
- `prompt_id` (string, required): The prompt's unique identifier

**Query Parameters:**
- `limit` (int, optional): Maximum number of versions to return (default: 50)
- `offset` (int, optional): Number of versions to skip (default: 0)

**Response:** `200 OK`

```json
{
  "versions": [
    {
      "id": "ver-uuid-3",
      "prompt_id": "prompt-uuid",
      "version": 3,
      "title": "Code Review v3",
      "content": "Review and explain: {{code}}",
      "description": "Enhanced version",
      "collection_id": "col-uuid",
      "created_at": "2024-01-15T12:00:00Z",
      "created_by": null
    },
    {
      "id": "ver-uuid-2",
      "prompt_id": "prompt-uuid",
      "version": 2,
      "title": "Code Review v2",
      "content": "Review this: {{code}}",
      "description": "Updated version",
      "collection_id": "col-uuid",
      "created_at": "2024-01-15T11:00:00Z",
      "created_by": null
    }
  ],
  "total": 3,
  "prompt_id": "prompt-uuid"
}
```

**Error Responses:**
- `404 Not Found`: Prompt doesn't exist

---

### 2. Get Specific Version

**Endpoint:** `GET /prompts/{prompt_id}/versions/{version}`

**Description:** Retrieve a specific version of a prompt.

**Path Parameters:**
- `prompt_id` (string, required): The prompt's unique identifier
- `version` (int, required): The version number

**Response:** `200 OK`

```json
{
  "id": "ver-uuid-2",
  "prompt_id": "prompt-uuid",
  "version": 2,
  "title": "Code Review v2",
  "content": "Review this: {{code}}",
  "description": "Updated version",
  "collection_id": "col-uuid",
  "created_at": "2024-01-15T11:00:00Z",
  "created_by": null
}
```

**Error Responses:**
- `404 Not Found`: Prompt or version doesn't exist

---

### 3. Revert to Version

**Endpoint:** `POST /prompts/{prompt_id}/versions/{version}/revert`

**Description:** Revert a prompt to a specific version.

**Path Parameters:**
- `prompt_id` (string, required): The prompt's unique identifier
- `version` (int, required): The version number to revert to

**Response:** `200 OK`

```json
{
  "id": "prompt-uuid",
  "title": "Code Review v2",
  "content": "Review this: {{code}}",
  "description": "Updated version",
  "collection_id": "col-uuid",
  "version": 4,
  "version_count": 4,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T13:00:00Z"
}
```

**Behavior:**
- Creates a new version (version 4) with content from version 2
- Updates the current prompt with the old content
- Preserves all history (doesn't delete versions)

**Error Responses:**
- `404 Not Found`: Prompt or version doesn't exist

---

### 4. Compare Versions

**Endpoint:** `GET /prompts/{prompt_id}/versions/compare?from={v1}&to={v2}`

**Description:** Compare two versions of a prompt.

**Path Parameters:**
- `prompt_id` (string, required): The prompt's unique identifier

**Query Parameters:**
- `from` (int, required): First version number
- `to` (int, required): Second version number

**Response:** `200 OK`

```json
{
  "prompt_id": "prompt-uuid",
  "from_version": {
    "version": 1,
    "title": "Code Review",
    "content": "Review: {{code}}",
    "description": "Original",
    "created_at": "2024-01-15T10:00:00Z"
  },
  "to_version": {
    "version": 3,
    "title": "Code Review v3",
    "content": "Review and explain: {{code}}",
    "description": "Enhanced version",
    "created_at": "2024-01-15T12:00:00Z"
  },
  "changes": {
    "title": "changed",
    "content": "changed",
    "description": "changed",
    "collection_id": "unchanged"
  }
}
```

**Error Responses:**
- `404 Not Found`: Prompt or either version doesn't exist

---

## Storage Changes

### New Storage Methods

```python
class Storage:
    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._versions: Dict[str, List[PromptVersion]] = {}  # New
    
    # Version operations
    def create_version(self, version: PromptVersion) -> PromptVersion:
        """Store a new prompt version."""
        
    def get_versions(self, prompt_id: str) -> List[PromptVersion]:
        """Get all versions for a prompt."""
        
    def get_version(self, prompt_id: str, version: int) -> Optional[PromptVersion]:
        """Get a specific version."""
        
    def get_version_count(self, prompt_id: str) -> int:
        """Get total version count for a prompt."""
```

---

## Implementation Strategy

### Phase 1: Data Model (Week 3, Day 1)
1. Create `PromptVersion` model
2. Update `Prompt` model with version fields
3. Add version storage to `Storage` class
4. Write unit tests for models

### Phase 2: Version Creation (Week 3, Day 2)
1. Modify `update_prompt()` to create versions
2. Modify `patch_prompt()` to create versions
3. Ensure version numbers increment correctly
4. Write tests for automatic version creation

### Phase 3: Read Operations (Week 3, Day 3)
1. Implement `GET /prompts/{id}/versions`
2. Implement `GET /prompts/{id}/versions/{version}`
3. Write tests for read operations

### Phase 4: Revert Operation (Week 3, Day 4)
1. Implement `POST /prompts/{id}/versions/{version}/revert`
2. Ensure new version is created on revert
3. Write tests for revert operation

### Phase 5: Compare Operation (Week 3, Day 5)
1. Implement `GET /prompts/{id}/versions/compare`
2. Add diff logic for changes
3. Write tests for compare operation

---

## Edge Cases and Considerations

### Edge Case 1: First Version
**Scenario:** When a prompt is created, should it have version 1?  
**Solution:** Yes, create version 1 on prompt creation.

### Edge Case 2: Deleting a Prompt
**Scenario:** What happens to versions when a prompt is deleted?  
**Solution:** Delete all versions when prompt is deleted (cascade delete).

### Edge Case 3: Reverting to Current Version
**Scenario:** User tries to revert to the current version.  
**Solution:** Return 400 Bad Request with message "Already on this version".

### Edge Case 4: Large Version History
**Scenario:** A prompt has 1000+ versions.  
**Solution:** Implement pagination with `limit` and `offset` parameters.

### Edge Case 5: Concurrent Updates
**Scenario:** Two users update the same prompt simultaneously.  
**Solution:** Last write wins (acceptable for MVP). Future: optimistic locking.

### Edge Case 6: Version Gaps
**Scenario:** Can version numbers have gaps (1, 2, 4, 5)?  
**Solution:** No, versions are sequential. Always increment by 1.

---

## Testing Requirements

### Unit Tests
- [ ] Test `PromptVersion` model validation
- [ ] Test version creation on update
- [ ] Test version number incrementing
- [ ] Test version retrieval

### Integration Tests
- [ ] Test GET /prompts/{id}/versions endpoint
- [ ] Test GET /prompts/{id}/versions/{version} endpoint
- [ ] Test POST /prompts/{id}/versions/{version}/revert endpoint
- [ ] Test GET /prompts/{id}/versions/compare endpoint
- [ ] Test version creation on PUT and PATCH
- [ ] Test cascade delete of versions

### Edge Case Tests
- [ ] Test reverting to current version (should fail)
- [ ] Test getting non-existent version (should 404)
- [ ] Test comparing same version (should work)
- [ ] Test version history pagination

---

## Future Enhancements

### Version 2.0 Features
- **Version Labels:** Allow naming versions (e.g., "Production", "Draft")
- **Version Branching:** Create branches from versions
- **Diff Visualization:** Show line-by-line diffs
- **Version Approval:** Require approval before promoting versions
- **Audit Trail:** Track who viewed/reverted versions

### Performance Optimizations
- **Version Pruning:** Auto-delete old versions after N days
- **Compression:** Compress old version content
- **Lazy Loading:** Load versions on-demand, not with prompt

---

## Success Metrics

- [ ] Users can view version history for any prompt
- [ ] Users can revert to previous versions
- [ ] Version creation is automatic and transparent
- [ ] No data loss when updating prompts
- [ ] API response times remain under 200ms

---

## Open Questions

1. Should we limit the number of versions stored per prompt?
2. Should version comparison include a visual diff?
3. Should we allow deleting individual versions?
4. Should we track who created each version (requires auth)?

---

**Document Version:** 1.0  
**Last Updated:** 2024-01-15  
**Author:** PromptLab Team
