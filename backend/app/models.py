"""Pydantic models for PromptLab.

This module defines all data models used in the PromptLab API using Pydantic.
Models provide automatic validation, serialization, and documentation.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier using UUID4.
    
    Returns:
        str: A unique identifier string in UUID4 format.
        
    Examples:
        >>> id = generate_id()
        >>> len(id)
        36
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC timestamp.
    
    Returns:
        datetime: Current UTC datetime object.
        
    Examples:
        >>> timestamp = get_current_time()
        >>> isinstance(timestamp, datetime)
        True
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for prompt data with common fields.
    
    This model contains the core fields shared across prompt creation,
    updates, and responses. It enforces validation rules for all prompt data.
    
    Attributes:
        title (str): The prompt title (1-200 characters).
        content (str): The actual prompt text with optional template variables.
        description (Optional[str]): Optional description of the prompt's purpose (max 500 chars).
        collection_id (Optional[str]): Optional ID linking this prompt to a collection.
        tags (List[str]): List of tags for categorization (max 10 tags).
    """
    title: str = Field(..., min_length=1, max_length=200, description="Prompt title")
    content: str = Field(..., min_length=1, description="Prompt content with optional {{variables}}")
    description: Optional[str] = Field(None, max_length=500, description="Optional prompt description")
    collection_id: Optional[str] = Field(None, description="ID of the collection this prompt belongs to")
    tags: List[str] = Field(default_factory=list, max_items=10, description="Tags for categorization")


class PromptCreate(PromptBase):
    """Model for creating a new prompt.
    
    Inherits all fields from PromptBase. Used for POST /prompts endpoint.
    The ID and timestamps will be auto-generated upon creation.
    
    Examples:
        >>> prompt_data = PromptCreate(
        ...     title="Code Review",
        ...     content="Review this code: {{code}}",
        ...     description="AI code review prompt"
        ... )
    """
    pass


class PromptUpdate(PromptBase):
    """Model for full prompt updates.
    
    Inherits all fields from PromptBase. Used for PUT /prompts/{id} endpoint.
    All fields are required for a full update.
    
    Examples:
        >>> update_data = PromptUpdate(
        ...     title="Updated Title",
        ...     content="Updated content",
        ...     description="Updated description",
        ...     collection_id=None
        ... )
    """
    pass


class PromptPatch(BaseModel):
    """Model for partial prompt updates.
    
    All fields are optional, allowing clients to update only specific fields.
    Used for PATCH /prompts/{id} endpoint.
    
    Attributes:
        title (Optional[str]): Optional new title (1-200 characters if provided).
        content (Optional[str]): Optional new content (min 1 character if provided).
        description (Optional[str]): Optional new description (max 500 chars if provided).
        collection_id (Optional[str]): Optional new collection ID.
        tags (Optional[List[str]]): Optional new tags list (max 10 tags if provided).
        
    Examples:
        >>> patch_data = PromptPatch(title="New Title Only")
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Optional new title")
    content: Optional[str] = Field(None, min_length=1, description="Optional new content")
    description: Optional[str] = Field(None, max_length=500, description="Optional new description")
    collection_id: Optional[str] = Field(None, description="Optional new collection ID")
    tags: Optional[List[str]] = Field(None, max_items=10, description="Optional new tags")
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Optional new title")
    content: Optional[str] = Field(None, min_length=1, description="Optional new content")
    description: Optional[str] = Field(None, max_length=500, description="Optional new description")
    collection_id: Optional[str] = Field(None, description="Optional new collection ID")


class Prompt(PromptBase):
    """Complete prompt model with metadata.
    
    Represents a full prompt object as stored and returned by the API.
    Includes auto-generated ID and timestamps in addition to base fields.
    
    Attributes:
        id (str): Unique identifier (auto-generated UUID4).
        version (int): Current version number.
        version_count (int): Total number of versions.
        created_at (datetime): Timestamp when prompt was created (auto-generated).
        updated_at (datetime): Timestamp when prompt was last updated (auto-generated).
        
    Examples:
        >>> prompt = Prompt(
        ...     title="My Prompt",
        ...     content="Prompt text"
        ... )
        >>> assert prompt.id is not None
        >>> assert prompt.created_at is not None
    """
    id: str = Field(default_factory=generate_id, description="Unique prompt identifier")
    version: int = Field(default=1, description="Current version number")
    version_count: int = Field(default=1, description="Total number of versions")
    created_at: datetime = Field(default_factory=get_current_time, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=get_current_time, description="Last update timestamp")

    class Config:
        from_attributes = True


# ============== Tag Models ==============

class Tag(BaseModel):
    """A tag for categorizing prompts.
    
    Tags provide a flexible way to categorize prompts with multiple labels.
    Each tag tracks its usage count across all prompts.
    
    Attributes:
        name (str): Tag name (lowercase, alphanumeric and hyphens only, 1-30 chars).
        usage_count (int): Number of prompts using this tag.
        created_at (datetime): When tag was first used.
        
    Examples:
        >>> tag = Tag(name="python", usage_count=5)
        >>> assert tag.name == "python"
    """
    name: str = Field(..., min_length=1, max_length=30, pattern="^[a-z0-9-]+$", description="Tag name")
    usage_count: int = Field(default=0, ge=0, description="Number of prompts using this tag")
    created_at: datetime = Field(default_factory=get_current_time, description="Creation timestamp")


class TagList(BaseModel):
    """Response model for listing tags.
    
    Used by GET /tags endpoint to return multiple tags with metadata.
    
    Attributes:
        tags (List[Tag]): List of tag objects.
        total (int): Total count of tags returned.
        
    Examples:
        >>> response = TagList(tags=[tag1, tag2], total=2)
    """
    tags: List[Tag] = Field(..., description="List of tags")
    total: int = Field(..., description="Total number of tags")


# ============== Version Models ==============

class PromptVersion(BaseModel):
    """A historical version of a prompt.
    
    Stores the complete state of a prompt at a specific point in time.
    Versions are created automatically when prompts are updated.
    
    Attributes:
        id (str): Unique version identifier (auto-generated UUID4).
        prompt_id (str): ID of the parent prompt.
        version (int): Version number (1, 2, 3, ...).
        title (str): Prompt title at this version.
        content (str): Prompt content at this version.
        description (Optional[str]): Prompt description at this version.
        collection_id (Optional[str]): Collection ID at this version.
        tags (List[str]): Tags at this version.
        created_at (datetime): When this version was created.
        created_by (Optional[str]): User who created this version (future).
        
    Examples:
        >>> version = PromptVersion(
        ...     prompt_id="prompt-123",
        ...     version=1,
        ...     title="Test",
        ...     content="Content"
        ... )
    """
    id: str = Field(default_factory=generate_id, description="Unique version identifier")
    prompt_id: str = Field(..., description="Parent prompt ID")
    version: int = Field(..., gt=0, description="Version number (must be positive)")
    title: str = Field(..., min_length=1, max_length=200, description="Prompt title")
    content: str = Field(..., min_length=1, description="Prompt content")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")
    collection_id: Optional[str] = Field(None, description="Collection ID")
    tags: List[str] = Field(default_factory=list, max_items=10, description="Tags")
    created_at: datetime = Field(default_factory=get_current_time, description="Creation timestamp")
    created_by: Optional[str] = Field(None, description="User who created this version")


class PromptVersionList(BaseModel):
    """Response model for listing prompt versions.
    
    Used by GET /prompts/{id}/versions endpoint.
    
    Attributes:
        versions (List[PromptVersion]): List of version objects.
        total (int): Total count of versions.
        prompt_id (str): ID of the parent prompt.
        
    Examples:
        >>> response = PromptVersionList(
        ...     versions=[v1, v2],
        ...     total=2,
        ...     prompt_id="prompt-123"
        ... )
    """
    versions: List[PromptVersion] = Field(..., description="List of versions")
    total: int = Field(..., description="Total number of versions")
    prompt_id: str = Field(..., description="Parent prompt ID")


class VersionComparison(BaseModel):
    """Response model for comparing two versions.
    
    Used by GET /prompts/{id}/versions/compare endpoint.
    
    Attributes:
        prompt_id (str): ID of the parent prompt.
        from_version (PromptVersion): First version to compare.
        to_version (PromptVersion): Second version to compare.
        changes (dict): Dictionary showing which fields changed.
        
    Examples:
        >>> comparison = VersionComparison(
        ...     prompt_id="prompt-123",
        ...     from_version=v1,
        ...     to_version=v2,
        ...     changes={"title": "changed", "content": "unchanged"}
        ... )
    """
    prompt_id: str = Field(..., description="Parent prompt ID")
    from_version: PromptVersion = Field(..., description="First version")
    to_version: PromptVersion = Field(..., description="Second version")
    changes: dict = Field(..., description="Fields that changed")


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for collection data with common fields.
    
    Collections are used to organize prompts into logical groups.
    
    Attributes:
        name (str): The collection name (1-100 characters).
        description (Optional[str]): Optional description of the collection's purpose (max 500 chars).
    """
    name: str = Field(..., min_length=1, max_length=100, description="Collection name")
    description: Optional[str] = Field(None, max_length=500, description="Optional collection description")


class CollectionCreate(CollectionBase):
    """Model for creating a new collection.
    
    Inherits all fields from CollectionBase. Used for POST /collections endpoint.
    The ID and timestamp will be auto-generated upon creation.
    
    Examples:
        >>> collection_data = CollectionCreate(
        ...     name="Development",
        ...     description="Prompts for development tasks"
        ... )
    """
    pass


class Collection(CollectionBase):
    """Complete collection model with metadata.
    
    Represents a full collection object as stored and returned by the API.
    Includes auto-generated ID and timestamp in addition to base fields.
    
    Attributes:
        id (str): Unique identifier (auto-generated UUID4).
        created_at (datetime): Timestamp when collection was created (auto-generated).
        
    Examples:
        >>> collection = Collection(name="My Collection")
        >>> assert collection.id is not None
        >>> assert collection.created_at is not None
    """
    id: str = Field(default_factory=generate_id, description="Unique collection identifier")
    created_at: datetime = Field(default_factory=get_current_time, description="Creation timestamp")

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Response model for listing prompts.
    
    Used by GET /prompts endpoint to return multiple prompts with metadata.
    
    Attributes:
        prompts (List[Prompt]): List of prompt objects.
        total (int): Total count of prompts returned.
        
    Examples:
        >>> response = PromptList(prompts=[prompt1, prompt2], total=2)
    """
    prompts: List[Prompt] = Field(..., description="List of prompts")
    total: int = Field(..., description="Total number of prompts")


class CollectionList(BaseModel):
    """Response model for listing collections.
    
    Used by GET /collections endpoint to return multiple collections with metadata.
    
    Attributes:
        collections (List[Collection]): List of collection objects.
        total (int): Total count of collections returned.
        
    Examples:
        >>> response = CollectionList(collections=[col1, col2], total=2)
    """
    collections: List[Collection] = Field(..., description="List of collections")
    total: int = Field(..., description="Total number of collections")


class HealthResponse(BaseModel):
    """Response model for health check endpoint.
    
    Used by GET /health endpoint to return API status and version.
    
    Attributes:
        status (str): Health status of the API (e.g., "healthy").
        version (str): Current API version string.
        
    Examples:
        >>> response = HealthResponse(status="healthy", version="0.1.0")
    """
    status: str = Field(..., description="API health status")
    version: str = Field(..., description="API version")
