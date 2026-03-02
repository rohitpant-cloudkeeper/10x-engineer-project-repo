"""Unit tests for Pydantic models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    generate_id, get_current_time
)


class TestHelperFunctions:
    """Test helper functions."""
    
    def test_generate_id_returns_string(self):
        """Test that generate_id returns a string."""
        id = generate_id()
        assert isinstance(id, str)
        assert len(id) == 36  # UUID4 format
    
    def test_generate_id_is_unique(self):
        """Test that generate_id returns unique IDs."""
        id1 = generate_id()
        id2 = generate_id()
        assert id1 != id2
    
    def test_get_current_time_returns_datetime(self):
        """Test that get_current_time returns datetime."""
        time = get_current_time()
        assert isinstance(time, datetime)


class TestPromptBase:
    """Test PromptBase model validation."""
    
    def test_valid_prompt_base(self):
        """Test creating valid PromptBase."""
        data = {
            "title": "Test Prompt",
            "content": "Test content",
            "description": "Test description",
            "collection_id": "test-id"
        }
        prompt = PromptCreate(**data)
        assert prompt.title == "Test Prompt"
        assert prompt.content == "Test content"
        assert prompt.description == "Test description"
        assert prompt.collection_id == "test-id"
    
    def test_prompt_base_without_optional_fields(self):
        """Test PromptBase without optional fields."""
        data = {
            "title": "Test Prompt",
            "content": "Test content"
        }
        prompt = PromptCreate(**data)
        assert prompt.title == "Test Prompt"
        assert prompt.content == "Test content"
        assert prompt.description is None
        assert prompt.collection_id is None
    
    def test_prompt_base_title_required(self):
        """Test that title is required."""
        data = {
            "content": "Test content"
        }
        with pytest.raises(ValidationError) as exc_info:
            PromptCreate(**data)
        assert "title" in str(exc_info.value)
    
    def test_prompt_base_content_required(self):
        """Test that content is required."""
        data = {
            "title": "Test Prompt"
        }
        with pytest.raises(ValidationError) as exc_info:
            PromptCreate(**data)
        assert "content" in str(exc_info.value)
    
    def test_prompt_base_title_min_length(self):
        """Test title minimum length validation."""
        data = {
            "title": "",
            "content": "Test content"
        }
        with pytest.raises(ValidationError) as exc_info:
            PromptCreate(**data)
        assert "title" in str(exc_info.value)
    
    def test_prompt_base_title_max_length(self):
        """Test title maximum length validation."""
        data = {
            "title": "x" * 201,  # Exceeds 200 char limit
            "content": "Test content"
        }
        with pytest.raises(ValidationError) as exc_info:
            PromptCreate(**data)
        assert "title" in str(exc_info.value)
    
    def test_prompt_base_content_min_length(self):
        """Test content minimum length validation."""
        data = {
            "title": "Test",
            "content": ""
        }
        with pytest.raises(ValidationError) as exc_info:
            PromptCreate(**data)
        assert "content" in str(exc_info.value)
    
    def test_prompt_base_description_max_length(self):
        """Test description maximum length validation."""
        data = {
            "title": "Test",
            "content": "Content",
            "description": "x" * 501  # Exceeds 500 char limit
        }
        with pytest.raises(ValidationError) as exc_info:
            PromptCreate(**data)
        assert "description" in str(exc_info.value)


class TestPromptCreate:
    """Test PromptCreate model."""
    
    def test_prompt_create_inherits_from_base(self):
        """Test that PromptCreate has all base fields."""
        data = {
            "title": "Test",
            "content": "Content"
        }
        prompt = PromptCreate(**data)
        assert hasattr(prompt, 'title')
        assert hasattr(prompt, 'content')
        assert hasattr(prompt, 'description')
        assert hasattr(prompt, 'collection_id')


class TestPromptUpdate:
    """Test PromptUpdate model."""
    
    def test_prompt_update_requires_all_fields(self):
        """Test that PromptUpdate requires all fields."""
        data = {
            "title": "Updated",
            "content": "Updated content",
            "description": "Updated desc",
            "collection_id": None
        }
        prompt = PromptUpdate(**data)
        assert prompt.title == "Updated"
        assert prompt.content == "Updated content"


class TestPromptPatch:
    """Test PromptPatch model for partial updates."""
    
    def test_prompt_patch_all_fields_optional(self):
        """Test that all fields are optional in PromptPatch."""
        data = {}
        prompt = PromptPatch(**data)
        assert prompt.title is None
        assert prompt.content is None
        assert prompt.description is None
        assert prompt.collection_id is None
    
    def test_prompt_patch_with_only_title(self):
        """Test PromptPatch with only title."""
        data = {"title": "New Title"}
        prompt = PromptPatch(**data)
        assert prompt.title == "New Title"
        assert prompt.content is None
    
    def test_prompt_patch_with_multiple_fields(self):
        """Test PromptPatch with multiple fields."""
        data = {
            "title": "New Title",
            "description": "New Description"
        }
        prompt = PromptPatch(**data)
        assert prompt.title == "New Title"
        assert prompt.description == "New Description"
        assert prompt.content is None
    
    def test_prompt_patch_validates_constraints(self):
        """Test that PromptPatch still validates field constraints."""
        data = {"title": "x" * 201}  # Exceeds max length
        with pytest.raises(ValidationError):
            PromptPatch(**data)


class TestPrompt:
    """Test full Prompt model."""
    
    def test_prompt_auto_generates_id(self):
        """Test that Prompt auto-generates ID."""
        data = {
            "title": "Test",
            "content": "Content"
        }
        prompt = Prompt(**data)
        assert prompt.id is not None
        assert isinstance(prompt.id, str)
        assert len(prompt.id) == 36
    
    def test_prompt_auto_generates_timestamps(self):
        """Test that Prompt auto-generates timestamps."""
        data = {
            "title": "Test",
            "content": "Content"
        }
        prompt = Prompt(**data)
        assert prompt.created_at is not None
        assert prompt.updated_at is not None
        assert isinstance(prompt.created_at, datetime)
        assert isinstance(prompt.updated_at, datetime)
    
    def test_prompt_serialization(self):
        """Test that Prompt can be serialized."""
        data = {
            "title": "Test",
            "content": "Content"
        }
        prompt = Prompt(**data)
        serialized = prompt.model_dump()
        assert serialized['title'] == "Test"
        assert serialized['content'] == "Content"
        assert 'id' in serialized
        assert 'created_at' in serialized
        assert 'updated_at' in serialized


class TestCollectionBase:
    """Test CollectionBase model validation."""
    
    def test_valid_collection_base(self):
        """Test creating valid CollectionBase."""
        data = {
            "name": "Test Collection",
            "description": "Test description"
        }
        collection = CollectionCreate(**data)
        assert collection.name == "Test Collection"
        assert collection.description == "Test description"
    
    def test_collection_base_without_description(self):
        """Test CollectionBase without description."""
        data = {"name": "Test Collection"}
        collection = CollectionCreate(**data)
        assert collection.name == "Test Collection"
        assert collection.description is None
    
    def test_collection_base_name_required(self):
        """Test that name is required."""
        data = {"description": "Test"}
        with pytest.raises(ValidationError) as exc_info:
            CollectionCreate(**data)
        assert "name" in str(exc_info.value)
    
    def test_collection_base_name_min_length(self):
        """Test name minimum length validation."""
        data = {"name": ""}
        with pytest.raises(ValidationError):
            CollectionCreate(**data)
    
    def test_collection_base_name_max_length(self):
        """Test name maximum length validation."""
        data = {"name": "x" * 101}  # Exceeds 100 char limit
        with pytest.raises(ValidationError):
            CollectionCreate(**data)
    
    def test_collection_base_description_max_length(self):
        """Test description maximum length validation."""
        data = {
            "name": "Test",
            "description": "x" * 501  # Exceeds 500 char limit
        }
        with pytest.raises(ValidationError):
            CollectionCreate(**data)


class TestCollection:
    """Test full Collection model."""
    
    def test_collection_auto_generates_id(self):
        """Test that Collection auto-generates ID."""
        data = {"name": "Test Collection"}
        collection = Collection(**data)
        assert collection.id is not None
        assert isinstance(collection.id, str)
        assert len(collection.id) == 36
    
    def test_collection_auto_generates_timestamp(self):
        """Test that Collection auto-generates created_at."""
        data = {"name": "Test Collection"}
        collection = Collection(**data)
        assert collection.created_at is not None
        assert isinstance(collection.created_at, datetime)
    
    def test_collection_serialization(self):
        """Test that Collection can be serialized."""
        data = {"name": "Test Collection"}
        collection = Collection(**data)
        serialized = collection.model_dump()
        assert serialized['name'] == "Test Collection"
        assert 'id' in serialized
        assert 'created_at' in serialized


class TestResponseModels:
    """Test response models."""
    
    def test_prompt_list(self):
        """Test PromptList model."""
        prompt = Prompt(title="Test", content="Content")
        prompt_list = PromptList(prompts=[prompt], total=1)
        assert len(prompt_list.prompts) == 1
        assert prompt_list.total == 1
    
    def test_prompt_list_empty(self):
        """Test PromptList with empty list."""
        prompt_list = PromptList(prompts=[], total=0)
        assert len(prompt_list.prompts) == 0
        assert prompt_list.total == 0
    
    def test_collection_list(self):
        """Test CollectionList model."""
        collection = Collection(name="Test")
        collection_list = CollectionList(collections=[collection], total=1)
        assert len(collection_list.collections) == 1
        assert collection_list.total == 1
    
    def test_collection_list_empty(self):
        """Test CollectionList with empty list."""
        collection_list = CollectionList(collections=[], total=0)
        assert len(collection_list.collections) == 0
        assert collection_list.total == 0
    
    def test_health_response(self):
        """Test HealthResponse model."""
        health = HealthResponse(status="healthy", version="1.0.0")
        assert health.status == "healthy"
        assert health.version == "1.0.0"
