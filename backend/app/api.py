"""FastAPI routes for PromptLab.

This module defines all HTTP endpoints for the PromptLab API using FastAPI.
It handles request validation, business logic, and response formatting for
prompts and collections management.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    Tag, TagList,
    PromptVersion, PromptVersionList, VersionComparison,
    get_current_time
)
from app.storage import storage
from app.utils import (
    sort_prompts_by_date, filter_prompts_by_collection, search_prompts,
    normalize_tags
)
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check API health and version.
    
    Returns basic health status and version information. Useful for
    monitoring and ensuring the API is running correctly.
    
    Returns:
        HealthResponse: Object containing status and version.
        
    Examples:
        >>> response = client.get("/health")
        >>> response.json()
        {'status': 'healthy', 'version': '0.1.0'}
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Helper Functions ==============

def create_prompt_version(prompt: Prompt) -> PromptVersion:
    """Create a version from the current prompt state.
    
    Args:
        prompt: The prompt to create a version from.
        
    Returns:
        PromptVersion: The created version object.
    """
    version = PromptVersion(
        prompt_id=prompt.id,
        version=prompt.version,
        title=prompt.title,
        content=prompt.content,
        description=prompt.description,
        collection_id=prompt.collection_id,
        tags=prompt.tags.copy() if prompt.tags else []
    )
    return storage.create_version(version)
def _handle_tag_updates(old_tags: list[str], new_tags: list[str]) -> list[str]:
    """Handle tag updates by managing usage counts.

    Decrements usage count for removed tags and increments for new tags.
    Returns the normalized list of new tags.

    Args:
        old_tags: List of existing tags on the prompt.
        new_tags: List of new tags to apply (will be normalized).

    Returns:
        list[str]: Normalized and deduplicated list of new tags.

    Examples:
        >>> normalized = _handle_tag_updates(["old-tag"], ["new-tag", "python"])
        >>> # old-tag usage decremented, new-tag and python usage incremented
    """
    # Normalize and deduplicate new tags
    normalized_tags = normalize_tags(new_tags)

    # Remove old tags (decrement usage)
    for tag in old_tags:
        storage.update_tag_usage(tag, -1)

    # Add new tags (increment usage)
    for tag in normalized_tags:
        storage.create_or_update_tag(tag)

    return normalized_tags



# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[str] = None
):
    """List all prompts with optional filtering.
    
    Retrieves all prompts from storage, optionally filtered by collection,
    search query, or tags. Results are sorted by creation date (newest first).
    
    Args:
        collection_id: Optional collection ID to filter prompts.
        search: Optional search query to filter by title or description.
        tags: Optional comma-separated list of tags (AND logic).
        
    Returns:
        PromptList: Object containing list of prompts and total count.
        
    Examples:
        >>> # Get all prompts
        >>> response = client.get("/prompts")
        >>> 
        >>> # Filter by collection
        >>> response = client.get("/prompts?collection_id=abc123")
        >>> 
        >>> # Search prompts
        >>> response = client.get("/prompts?search=code+review")
        >>> 
        >>> # Filter by tags
        >>> response = client.get("/prompts?tags=python,testing")
    """
    prompts = storage.get_all_prompts()
    
    # Filter by tags if specified (AND logic)
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        prompts = storage.get_prompts_by_tags(tag_list)
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a specific prompt by ID.
    
    Args:
        prompt_id: The unique identifier of the prompt.
        
    Returns:
        Prompt: The requested prompt object.
        
    Raises:
        HTTPException: 404 if prompt not found.
        
    Examples:
        >>> response = client.get("/prompts/abc123")
        >>> prompt = response.json()
        >>> print(prompt['title'])
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.
    
    Creates a new prompt with auto-generated ID and timestamps. If a
    collection_id is provided, validates that the collection exists.
    
    Args:
        prompt_data: The prompt data (title, content, description, collection_id).
        
    Returns:
        Prompt: The newly created prompt with generated ID and timestamps.
        
    Raises:
        HTTPException: 400 if collection_id is invalid.
        
    Examples:
        >>> data = {
        ...     "title": "Code Review",
        ...     "content": "Review this: {{code}}",
        ...     "description": "AI code review prompt"
        ... }
        >>> response = client.post("/prompts", json=data)
        >>> response.status_code
        201
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Normalize and deduplicate tags
    normalized_tags = normalize_tags(prompt_data.tags)
    
    # Create prompt with normalized tags
    prompt_dict = prompt_data.model_dump()
    prompt_dict['tags'] = normalized_tags
    prompt = Prompt(**prompt_dict)
    
    # Update tag usage counts
    for tag in normalized_tags:
        storage.create_or_update_tag(tag)
    
    created_prompt = storage.create_prompt(prompt)
    
    # Create initial version
    create_prompt_version(created_prompt)
    
    return created_prompt


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Fully update an existing prompt.
    
    Replaces all fields of the prompt with new values. All fields must be
    provided. The updated_at timestamp is automatically updated.
    
    Args:
        prompt_id: The unique identifier of the prompt to update.
        prompt_data: Complete prompt data with all fields.
        
    Returns:
        Prompt: The updated prompt object.
        
    Raises:
        HTTPException: 404 if prompt not found, 400 if collection_id is invalid.
        
    Examples:
        >>> data = {
        ...     "title": "Updated Title",
        ...     "content": "Updated content",
        ...     "description": "Updated description",
        ...     "collection_id": None
        ... }
        >>> response = client.put("/prompts/abc123", json=data)
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Handle tag updates
    normalized_tags = _handle_tag_updates(existing.tags, prompt_data.tags)
    
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        tags=normalized_tags,
        version=existing.version + 1,
        version_count=existing.version_count + 1,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    # Save updated prompt
    result = storage.update_prompt(prompt_id, updated_prompt)
    
    # Create new version
    create_prompt_version(updated_prompt)
    
    return result


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """Partially update an existing prompt.
    
    Updates only the fields provided in the request. Omitted fields remain
    unchanged. The updated_at timestamp is automatically updated.
    
    Args:
        prompt_id: The unique identifier of the prompt to update.
        prompt_data: Partial prompt data with only fields to update.
        
    Returns:
        Prompt: The updated prompt object.
        
    Raises:
        HTTPException: 404 if prompt not found, 400 if collection_id is invalid.
        
    Examples:
        >>> # Update only the title
        >>> data = {"title": "New Title"}
        >>> response = client.patch("/prompts/abc123", json=data)
        >>> 
        >>> # Update multiple fields
        >>> data = {"title": "New Title", "description": "New description"}
        >>> response = client.patch("/prompts/abc123", json=data)
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id is not None:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Only update fields that are provided (not None)
    update_data = prompt_data.model_dump(exclude_unset=True)
    
    # Handle tags if provided
    if 'tags' in update_data:
        normalized_tags = _handle_tag_updates(existing.tags, update_data['tags'])
        update_data['tags'] = normalized_tags
    
    updated_prompt = Prompt(
        id=existing.id,
        title=update_data.get('title', existing.title),
        content=update_data.get('content', existing.content),
        description=update_data.get('description', existing.description),
        collection_id=update_data.get('collection_id', existing.collection_id),
        tags=update_data.get('tags', existing.tags),
        version=existing.version + 1,
        version_count=existing.version_count + 1,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    result = storage.update_prompt(prompt_id, updated_prompt)
    
    # Create new version
    create_prompt_version(updated_prompt)
    
    return result


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by ID.
    
    Permanently removes the prompt from storage. This operation cannot be undone.
    Decrements usage count for all tags associated with the prompt.
    
    Args:
        prompt_id: The unique identifier of the prompt to delete.
        
    Returns:
        None: Returns 204 No Content on success.
        
    Raises:
        HTTPException: 404 if prompt not found.
        
    Examples:
        >>> response = client.delete("/prompts/abc123")
        >>> response.status_code
        204
    """
    # Get prompt to access its tags before deletion
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Decrement usage count for all tags
    for tag in prompt.tags:
        storage.update_tag_usage(tag, -1)
    
    # Delete all versions
    storage.delete_versions_for_prompt(prompt_id)
    
    # Delete the prompt
    storage.delete_prompt(prompt_id)
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections.
    
    Retrieves all collections from storage.
    
    Returns:
        CollectionList: Object containing list of collections and total count.
        
    Examples:
        >>> response = client.get("/collections")
        >>> collections = response.json()['collections']
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a specific collection by ID.
    
    Args:
        collection_id: The unique identifier of the collection.
        
    Returns:
        Collection: The requested collection object.
        
    Raises:
        HTTPException: 404 if collection not found.
        
    Examples:
        >>> response = client.get("/collections/xyz789")
        >>> collection = response.json()
        >>> print(collection['name'])
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.
    
    Creates a new collection with auto-generated ID and timestamp.
    
    Args:
        collection_data: The collection data (name, description).
        
    Returns:
        Collection: The newly created collection with generated ID and timestamp.
        
    Examples:
        >>> data = {
        ...     "name": "Development",
        ...     "description": "Prompts for development tasks"
        ... }
        >>> response = client.post("/collections", json=data)
        >>> response.status_code
        201
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection by ID.
    
    Permanently removes the collection from storage. All prompts in this
    collection will have their collection_id set to None (uncategorized).
    This operation cannot be undone.
    
    Args:
        collection_id: The unique identifier of the collection to delete.
        
    Returns:
        None: Returns 204 No Content on success.
        
    Raises:
        HTTPException: 404 if collection not found.
        
    Note:
        Prompts in the deleted collection are not deleted, only uncategorized.
        
    Examples:
        >>> response = client.delete("/collections/xyz789")
        >>> response.status_code
        204
    """
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Handle prompts that belong to this collection
    # Set their collection_id to None instead of deleting them
    prompts_in_collection = storage.get_prompts_by_collection(collection_id)
    for prompt in prompts_in_collection:
        prompt.collection_id = None
        storage.update_prompt(prompt.id, prompt)
    
    return None


# ============== Tag Endpoints ==============

@app.get("/tags", response_model=TagList)
def list_tags(search: Optional[str] = None):
    """List all tags with optional search.
    
    Retrieves all tags from storage, optionally filtered by search query.
    Results are sorted alphabetically by tag name.
    
    Args:
        search: Optional search query to filter tags by name (partial match).
        
    Returns:
        TagList: Object containing list of tags and total count.
        
    Examples:
        >>> # Get all tags
        >>> response = client.get("/tags")
        >>> 
        >>> # Search tags
        >>> response = client.get("/tags?search=python")
    """
    tags = storage.get_all_tags()
    
    # Filter by search if specified
    if search:
        search_lower = search.lower()
        tags = [t for t in tags if search_lower in t.name]
    
    return TagList(tags=tags, total=len(tags))


@app.get("/tags/popular", response_model=TagList)
def get_popular_tags(limit: int = 10):
    """Get popular tags sorted by usage count.
    
    Retrieves tags sorted by usage count in descending order.
    
    Args:
        limit: Maximum number of tags to return (default: 10).
        
    Returns:
        TagList: Object containing list of popular tags and total count.
        
    Examples:
        >>> response = client.get("/tags/popular?limit=5")
    """
    tags = storage.get_all_tags()
    # Sort by usage count descending
    tags = sorted(tags, key=lambda t: t.usage_count, reverse=True)
    # Limit results
    tags = tags[:limit]
    
    return TagList(tags=tags, total=len(tags))


@app.get("/tags/{tag_name}", response_model=Tag)
def get_tag(tag_name: str):
    """Retrieve a specific tag by name.
    
    Args:
        tag_name: The tag name to retrieve.
        
    Returns:
        Tag: The requested tag object with usage count.
        
    Raises:
        HTTPException: 404 if tag not found.
        
    Examples:
        >>> response = client.get("/tags/python")
        >>> tag = response.json()
        >>> print(tag['usage_count'])
    """
    tag = storage.get_tag(tag_name)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


# ============== Version Endpoints ==============

@app.get("/prompts/{prompt_id}/versions", response_model=PromptVersionList)
def list_prompt_versions(
    prompt_id: str,
    limit: int = 50,
    offset: int = 0
):
    """List all versions of a prompt.
    
    Retrieves version history for a specific prompt, sorted by version number
    (newest first). Supports pagination.
    
    Args:
        prompt_id: The unique identifier of the prompt.
        limit: Maximum number of versions to return (default: 50).
        offset: Number of versions to skip (default: 0).
        
    Returns:
        PromptVersionList: Object containing versions, total count, and prompt ID.
        
    Raises:
        HTTPException: 404 if prompt not found.
        
    Examples:
        >>> response = client.get("/prompts/abc123/versions")
        >>> response = client.get("/prompts/abc123/versions?limit=10&offset=5")
    """
    # Verify prompt exists
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Get all versions
    all_versions = storage.get_versions(prompt_id)
    total = len(all_versions)
    
    # Apply pagination
    versions = all_versions[offset:offset + limit]
    
    return PromptVersionList(
        versions=versions,
        total=total,
        prompt_id=prompt_id
    )


@app.get("/prompts/{prompt_id}/versions/compare", response_model=VersionComparison)
def compare_versions(
    prompt_id: str,
    from_version: int = Query(..., alias="from"),
    to_version: int = Query(..., alias="to")
):
    """Compare two versions of a prompt.
    
    Args:
        prompt_id: The unique identifier of the prompt.
        from_version: First version number (query parameter: from).
        to_version: Second version number (query parameter: to).
        
    Returns:
        VersionComparison: Object containing both versions and changes.
        
    Raises:
        HTTPException: 404 if prompt or either version not found.
        
    Examples:
        >>> response = client.get("/prompts/abc123/versions/compare?from=1&to=3")
    """
    # Verify prompt exists
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Get both versions
    v1 = storage.get_version(prompt_id, from_version)
    if not v1:
        raise HTTPException(status_code=404, detail=f"Version {from_version} not found")
    
    v2 = storage.get_version(prompt_id, to_version)
    if not v2:
        raise HTTPException(status_code=404, detail=f"Version {to_version} not found")
    
    # Detect changes
    changes = {
        "title": "changed" if v1.title != v2.title else "unchanged",
        "content": "changed" if v1.content != v2.content else "unchanged",
        "description": "changed" if v1.description != v2.description else "unchanged",
        "collection_id": "changed" if v1.collection_id != v2.collection_id else "unchanged",
        "tags": "changed" if v1.tags != v2.tags else "unchanged"
    }
    
    return VersionComparison(
        prompt_id=prompt_id,
        from_version=v1,
        to_version=v2,
        changes=changes
    )


@app.get("/prompts/{prompt_id}/versions/{version}", response_model=PromptVersion)
def get_prompt_version(prompt_id: str, version: int):
    """Get a specific version of a prompt.
    
    Args:
        prompt_id: The unique identifier of the prompt.
        version: The version number to retrieve.
        
    Returns:
        PromptVersion: The requested version object.
        
    Raises:
        HTTPException: 404 if prompt or version not found.
        
    Examples:
        >>> response = client.get("/prompts/abc123/versions/2")
    """
    # Verify prompt exists
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Get version
    prompt_version = storage.get_version(prompt_id, version)
    if not prompt_version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    return prompt_version


@app.post("/prompts/{prompt_id}/versions/{version}/revert", response_model=Prompt)
def revert_to_version(prompt_id: str, version: int):
    """Revert a prompt to a previous version.
    
    Creates a new version with the content from the specified version.
    Does not delete any history.
    
    Args:
        prompt_id: The unique identifier of the prompt.
        version: The version number to revert to.
        
    Returns:
        Prompt: The updated prompt object with new version number.
        
    Raises:
        HTTPException: 404 if prompt or version not found.
        HTTPException: 400 if trying to revert to current version.
        
    Examples:
        >>> response = client.post("/prompts/abc123/versions/2/revert")
    """
    # Verify prompt exists
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Check if reverting to current version
    if version == existing.version:
        raise HTTPException(
            status_code=400,
            detail="Already on this version. Cannot revert to current version."
        )
    
    # Get version to revert to
    target_version = storage.get_version(prompt_id, version)
    if not target_version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    # Update tag usage counts
    # Remove old tags
    for tag in existing.tags:
        storage.update_tag_usage(tag, -1)
    # Add tags from target version
    for tag in target_version.tags:
        storage.create_or_update_tag(tag)
    
    # Create updated prompt with content from target version
    reverted_prompt = Prompt(
        id=existing.id,
        title=target_version.title,
        content=target_version.content,
        description=target_version.description,
        collection_id=target_version.collection_id,
        tags=target_version.tags.copy() if target_version.tags else [],
        version=existing.version + 1,
        version_count=existing.version_count + 1,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    # Save updated prompt
    result = storage.update_prompt(prompt_id, reverted_prompt)
    
    # Create new version
    create_prompt_version(reverted_prompt)
    
    return result
