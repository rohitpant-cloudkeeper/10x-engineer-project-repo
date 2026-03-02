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
    """
    title: str = Field(..., min_length=1, max_length=200, description="Prompt title")
    content: str = Field(..., min_length=1, description="Prompt content with optional {{variables}}")
    description: Optional[str] = Field(None, max_length=500, description="Optional prompt description")
    collection_id: Optional[str] = Field(None, description="ID of the collection this prompt belongs to")


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
        
    Examples:
        >>> patch_data = PromptPatch(title="New Title Only")
    """
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
    created_at: datetime = Field(default_factory=get_current_time, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=get_current_time, description="Last update timestamp")

    class Config:
        from_attributes = True


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
