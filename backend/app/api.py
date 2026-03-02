"""FastAPI routes for PromptLab.

This module defines all HTTP endpoints for the PromptLab API using FastAPI.
It handles request validation, business logic, and response formatting for
prompts and collections management.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
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


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List all prompts with optional filtering.
    
    Retrieves all prompts from storage, optionally filtered by collection
    or search query. Results are sorted by creation date (newest first).
    
    Args:
        collection_id: Optional collection ID to filter prompts.
        search: Optional search query to filter by title or description.
        
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
    """
    prompts = storage.get_all_prompts()
    
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
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


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
    
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


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
    
    updated_prompt = Prompt(
        id=existing.id,
        title=update_data.get('title', existing.title),
        content=update_data.get('content', existing.content),
        description=update_data.get('description', existing.description),
        collection_id=update_data.get('collection_id', existing.collection_id),
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by ID.
    
    Permanently removes the prompt from storage. This operation cannot be undone.
    
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
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
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
