"""Unit tests for storage layer."""

import pytest
from app.models import Prompt, Collection
from app.storage import Storage


@pytest.fixture
def storage():
    """Create a fresh storage instance for each test."""
    return Storage()


@pytest.fixture
def sample_prompt():
    """Create a sample prompt."""
    return Prompt(
        title="Test Prompt",
        content="Test content",
        description="Test description"
    )


@pytest.fixture
def sample_collection():
    """Create a sample collection."""
    return Collection(
        name="Test Collection",
        description="Test description"
    )


class TestPromptOperations:
    """Test prompt CRUD operations."""
    
    def test_create_prompt(self, storage, sample_prompt):
        """Test creating a prompt."""
        result = storage.create_prompt(sample_prompt)
        assert result == sample_prompt
        assert result.id == sample_prompt.id
    
    def test_get_prompt_exists(self, storage, sample_prompt):
        """Test getting an existing prompt."""
        storage.create_prompt(sample_prompt)
        result = storage.get_prompt(sample_prompt.id)
        assert result is not None
        assert result.id == sample_prompt.id
        assert result.title == sample_prompt.title
    
    def test_get_prompt_not_exists(self, storage):
        """Test getting a non-existent prompt returns None."""
        result = storage.get_prompt("non-existent-id")
        assert result is None
    
    def test_get_all_prompts_empty(self, storage):
        """Test getting all prompts from empty storage."""
        result = storage.get_all_prompts()
        assert result == []
        assert len(result) == 0
    
    def test_get_all_prompts_with_data(self, storage, sample_prompt):
        """Test getting all prompts with data."""
        prompt1 = Prompt(title="Prompt 1", content="Content 1")
        prompt2 = Prompt(title="Prompt 2", content="Content 2")
        storage.create_prompt(prompt1)
        storage.create_prompt(prompt2)
        
        result = storage.get_all_prompts()
        assert len(result) == 2
        assert prompt1 in result
        assert prompt2 in result
    
    def test_update_prompt_exists(self, storage, sample_prompt):
        """Test updating an existing prompt."""
        storage.create_prompt(sample_prompt)
        
        updated_prompt = Prompt(
            id=sample_prompt.id,
            title="Updated Title",
            content="Updated content",
            created_at=sample_prompt.created_at,
            updated_at=sample_prompt.updated_at
        )
        
        result = storage.update_prompt(sample_prompt.id, updated_prompt)
        assert result is not None
        assert result.title == "Updated Title"
        assert result.content == "Updated content"
    
    def test_update_prompt_not_exists(self, storage, sample_prompt):
        """Test updating a non-existent prompt returns None."""
        result = storage.update_prompt("non-existent-id", sample_prompt)
        assert result is None
    
    def test_delete_prompt_exists(self, storage, sample_prompt):
        """Test deleting an existing prompt."""
        storage.create_prompt(sample_prompt)
        result = storage.delete_prompt(sample_prompt.id)
        assert result is True
        assert storage.get_prompt(sample_prompt.id) is None
    
    def test_delete_prompt_not_exists(self, storage):
        """Test deleting a non-existent prompt returns False."""
        result = storage.delete_prompt("non-existent-id")
        assert result is False


class TestCollectionOperations:
    """Test collection CRUD operations."""
    
    def test_create_collection(self, storage, sample_collection):
        """Test creating a collection."""
        result = storage.create_collection(sample_collection)
        assert result == sample_collection
        assert result.id == sample_collection.id
    
    def test_get_collection_exists(self, storage, sample_collection):
        """Test getting an existing collection."""
        storage.create_collection(sample_collection)
        result = storage.get_collection(sample_collection.id)
        assert result is not None
        assert result.id == sample_collection.id
        assert result.name == sample_collection.name
    
    def test_get_collection_not_exists(self, storage):
        """Test getting a non-existent collection returns None."""
        result = storage.get_collection("non-existent-id")
        assert result is None
    
    def test_get_all_collections_empty(self, storage):
        """Test getting all collections from empty storage."""
        result = storage.get_all_collections()
        assert result == []
        assert len(result) == 0
    
    def test_get_all_collections_with_data(self, storage):
        """Test getting all collections with data."""
        col1 = Collection(name="Collection 1")
        col2 = Collection(name="Collection 2")
        storage.create_collection(col1)
        storage.create_collection(col2)
        
        result = storage.get_all_collections()
        assert len(result) == 2
        assert col1 in result
        assert col2 in result
    
    def test_delete_collection_exists(self, storage, sample_collection):
        """Test deleting an existing collection."""
        storage.create_collection(sample_collection)
        result = storage.delete_collection(sample_collection.id)
        assert result is True
        assert storage.get_collection(sample_collection.id) is None
    
    def test_delete_collection_not_exists(self, storage):
        """Test deleting a non-existent collection returns False."""
        result = storage.delete_collection("non-existent-id")
        assert result is False


class TestPromptCollectionRelationship:
    """Test prompt-collection relationship operations."""
    
    def test_get_prompts_by_collection_empty(self, storage, sample_collection):
        """Test getting prompts for collection with no prompts."""
        storage.create_collection(sample_collection)
        result = storage.get_prompts_by_collection(sample_collection.id)
        assert result == []
    
    def test_get_prompts_by_collection_with_prompts(self, storage, sample_collection):
        """Test getting prompts for collection with prompts."""
        storage.create_collection(sample_collection)
        
        prompt1 = Prompt(
            title="Prompt 1",
            content="Content 1",
            collection_id=sample_collection.id
        )
        prompt2 = Prompt(
            title="Prompt 2",
            content="Content 2",
            collection_id=sample_collection.id
        )
        prompt3 = Prompt(
            title="Prompt 3",
            content="Content 3",
            collection_id="other-collection"
        )
        
        storage.create_prompt(prompt1)
        storage.create_prompt(prompt2)
        storage.create_prompt(prompt3)
        
        result = storage.get_prompts_by_collection(sample_collection.id)
        assert len(result) == 2
        assert prompt1 in result
        assert prompt2 in result
        assert prompt3 not in result
    
    def test_get_prompts_by_nonexistent_collection(self, storage):
        """Test getting prompts for non-existent collection."""
        result = storage.get_prompts_by_collection("non-existent-id")
        assert result == []


class TestStorageUtility:
    """Test storage utility methods."""
    
    def test_clear_empty_storage(self, storage):
        """Test clearing empty storage."""
        storage.clear()
        assert storage.get_all_prompts() == []
        assert storage.get_all_collections() == []
    
    def test_clear_with_data(self, storage, sample_prompt, sample_collection):
        """Test clearing storage with data."""
        storage.create_prompt(sample_prompt)
        storage.create_collection(sample_collection)
        
        assert len(storage.get_all_prompts()) == 1
        assert len(storage.get_all_collections()) == 1
        
        storage.clear()
        
        assert storage.get_all_prompts() == []
        assert storage.get_all_collections() == []


class TestStorageIsolation:
    """Test that storage instances are isolated."""
    
    def test_multiple_storage_instances_isolated(self):
        """Test that multiple storage instances don't share data."""
        storage1 = Storage()
        storage2 = Storage()
        
        prompt = Prompt(title="Test", content="Content")
        storage1.create_prompt(prompt)
        
        assert len(storage1.get_all_prompts()) == 1
        assert len(storage2.get_all_prompts()) == 0
