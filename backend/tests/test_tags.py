"""Tests for tagging system.

This module tests the tagging functionality including tag models,
validation, normalization, storage, and API endpoints.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from fastapi.testclient import TestClient

from app.models import Prompt, Tag, PromptCreate, PromptPatch


class TestTagModel:
    """Tests for Tag model."""
    
    def test_create_tag_valid(self):
        """Test creating a valid tag."""
        tag = Tag(name="python", usage_count=5)
        assert tag.name == "python"
        assert tag.usage_count == 5
        assert isinstance(tag.created_at, datetime)
    
    def test_tag_name_validation_length(self):
        """Test tag name length validation."""
        # Too short (empty)
        with pytest.raises(ValidationError):
            Tag(name="")
        
        # Too long (>30 chars)
        with pytest.raises(ValidationError):
            Tag(name="a" * 31)
        
        # Valid lengths
        Tag(name="a")  # Min length
        Tag(name="a" * 30)  # Max length
    
    def test_tag_name_validation_pattern(self):
        """Test tag name pattern validation (lowercase, alphanumeric, hyphens only)."""
        # Valid patterns
        Tag(name="python")
        Tag(name="code-review")
        Tag(name="python3")
        Tag(name="ai-ml-2024")
        
        # Invalid patterns (should fail)
        with pytest.raises(ValidationError):
            Tag(name="Python")  # Uppercase
        
        with pytest.raises(ValidationError):
            Tag(name="code review")  # Space
        
        with pytest.raises(ValidationError):
            Tag(name="ai/ml")  # Special char
        
        with pytest.raises(ValidationError):
            Tag(name="test@tag")  # Special char
    
    def test_tag_usage_count_default(self):
        """Test tag usage count defaults to 0."""
        tag = Tag(name="python")
        assert tag.usage_count == 0
    
    def test_tag_usage_count_non_negative(self):
        """Test tag usage count must be non-negative."""
        Tag(name="python", usage_count=0)  # Valid
        Tag(name="python", usage_count=10)  # Valid
        
        with pytest.raises(ValidationError):
            Tag(name="python", usage_count=-1)  # Invalid


class TestPromptWithTags:
    """Tests for Prompt model with tags field."""
    
    def test_create_prompt_with_tags(self):
        """Test creating a prompt with tags."""
        prompt = Prompt(
            title="Test Prompt",
            content="Test content",
            tags=["python", "code-review"]
        )
        assert prompt.tags == ["python", "code-review"]
    
    def test_create_prompt_without_tags(self):
        """Test creating a prompt without tags defaults to empty list."""
        prompt = Prompt(
            title="Test Prompt",
            content="Test content"
        )
        assert prompt.tags == []
    
    def test_prompt_tags_max_items(self):
        """Test prompt can have maximum 10 tags."""
        # 10 tags should work
        Prompt(
            title="Test",
            content="Content",
            tags=[f"tag{i}" for i in range(10)]
        )
        
        # 11 tags should fail
        with pytest.raises(ValidationError):
            Prompt(
                title="Test",
                content="Content",
                tags=[f"tag{i}" for i in range(11)]
            )
    
    def test_prompt_create_with_tags(self):
        """Test PromptCreate model with tags."""
        data = PromptCreate(
            title="Test",
            content="Content",
            tags=["python", "testing"]
        )
        assert data.tags == ["python", "testing"]
    
    def test_prompt_patch_with_tags(self):
        """Test PromptPatch model with optional tags."""
        # Patch with tags
        patch = PromptPatch(tags=["new-tag"])
        assert patch.tags == ["new-tag"]
        
        # Patch without tags
        patch = PromptPatch(title="New Title")
        assert patch.tags is None


class TestTagNormalization:
    """Tests for tag normalization utility."""
    
    def test_normalize_tag_lowercase(self):
        """Test tag normalization converts to lowercase."""
        from app.utils import normalize_tag
        assert normalize_tag("Python") == "python"
        assert normalize_tag("CODE-REVIEW") == "code-review"
    
    def test_normalize_tag_strip_whitespace(self):
        """Test tag normalization strips whitespace."""
        from app.utils import normalize_tag
        assert normalize_tag("  python  ") == "python"
        assert normalize_tag("\tpython\n") == "python"
    
    def test_normalize_tag_replace_spaces(self):
        """Test tag normalization replaces spaces with hyphens."""
        from app.utils import normalize_tag
        assert normalize_tag("code review") == "code-review"
        assert normalize_tag("ai ml") == "ai-ml"
    
    def test_normalize_tag_remove_invalid_chars(self):
        """Test tag normalization removes invalid characters."""
        from app.utils import normalize_tag
        assert normalize_tag("C++") == "c"
        assert normalize_tag("AI/ML") == "aiml"
        assert normalize_tag("test@tag") == "testtag"
    
    def test_normalize_tag_validation_error(self):
        """Test tag normalization raises error for invalid tags."""
        from app.utils import normalize_tag
        
        # Empty after normalization
        with pytest.raises(ValueError, match="Invalid tag format"):
            normalize_tag("@@@")
        
        # Too long
        with pytest.raises(ValueError, match="Tag length must be 1-30 characters"):
            normalize_tag("a" * 31)
    
    def test_normalize_tags_list(self):
        """Test normalizing a list of tags."""
        from app.utils import normalize_tags
        
        tags = ["Python", "Code Review", "AI/ML"]
        normalized = normalize_tags(tags)
        assert normalized == ["python", "code-review", "aiml"]
    
    def test_normalize_tags_remove_duplicates(self):
        """Test normalizing removes duplicate tags."""
        from app.utils import normalize_tags
        
        tags = ["Python", "python", "PYTHON"]
        normalized = normalize_tags(tags)
        assert normalized == ["python"]
    
    def test_normalize_tags_empty_list(self):
        """Test normalizing empty list."""
        from app.utils import normalize_tags
        
        assert normalize_tags([]) == []


class TestTagStorage:
    """Tests for tag storage operations."""
    
    def test_create_tag(self, storage):
        """Test creating a tag in storage."""
        tag = Tag(name="python", usage_count=1)
        result = storage.create_or_update_tag("python")
        
        assert result.name == "python"
        assert result.usage_count == 1
    
    def test_get_tag_exists(self, storage):
        """Test getting an existing tag."""
        storage.create_or_update_tag("python")
        tag = storage.get_tag("python")
        
        assert tag is not None
        assert tag.name == "python"
    
    def test_get_tag_not_exists(self, storage):
        """Test getting a non-existent tag returns None."""
        tag = storage.get_tag("nonexistent")
        assert tag is None
    
    def test_get_all_tags_empty(self, storage):
        """Test getting all tags from empty storage."""
        tags = storage.get_all_tags()
        assert tags == []
    
    def test_get_all_tags_sorted(self, storage):
        """Test tags are returned sorted alphabetically."""
        storage.create_or_update_tag("python")
        storage.create_or_update_tag("javascript")
        storage.create_or_update_tag("go")
        
        tags = storage.get_all_tags()
        tag_names = [t.name for t in tags]
        assert tag_names == ["go", "javascript", "python"]
    
    def test_update_tag_usage(self, storage):
        """Test updating tag usage count."""
        storage.create_or_update_tag("python")
        storage.update_tag_usage("python", 1)
        
        tag = storage.get_tag("python")
        assert tag.usage_count == 2
    
    def test_get_prompts_by_tag(self, storage):
        """Test getting prompts by a single tag."""
        prompt1 = Prompt(title="P1", content="C1", tags=["python"])
        prompt2 = Prompt(title="P2", content="C2", tags=["python", "testing"])
        prompt3 = Prompt(title="P3", content="C3", tags=["javascript"])
        
        storage.create_prompt(prompt1)
        storage.create_prompt(prompt2)
        storage.create_prompt(prompt3)
        
        results = storage.get_prompts_by_tag("python")
        assert len(results) == 2
        assert prompt1 in results
        assert prompt2 in results
    
    def test_get_prompts_by_tags_and_logic(self, storage):
        """Test getting prompts by multiple tags (AND logic)."""
        prompt1 = Prompt(title="P1", content="C1", tags=["python", "testing"])
        prompt2 = Prompt(title="P2", content="C2", tags=["python"])
        prompt3 = Prompt(title="P3", content="C3", tags=["python", "testing", "advanced"])
        
        storage.create_prompt(prompt1)
        storage.create_prompt(prompt2)
        storage.create_prompt(prompt3)
        
        # Both python AND testing
        results = storage.get_prompts_by_tags(["python", "testing"])
        assert len(results) == 2
        assert prompt1 in results
        assert prompt3 in results


class TestTagAPI:
    """Tests for tag API endpoints."""
    
    def test_create_prompt_with_tags(self, client: TestClient):
        """Test creating a prompt with tags via API."""
        data = {
            "title": "Python Code Review",
            "content": "Review this code",
            "tags": ["python", "code-review"]
        }
        response = client.post("/prompts", json=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["tags"] == ["python", "code-review"]
    
    def test_create_prompt_tags_normalized(self, client: TestClient):
        """Test tags are normalized when creating prompt."""
        data = {
            "title": "Test",
            "content": "Content",
            "tags": ["Python", "Code Review", "AI/ML"]
        }
        response = client.post("/prompts", json=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["tags"] == ["python", "code-review", "aiml"]
    
    def test_create_prompt_tags_deduplicated(self, client: TestClient):
        """Test duplicate tags are removed."""
        data = {
            "title": "Test",
            "content": "Content",
            "tags": ["python", "Python", "PYTHON"]
        }
        response = client.post("/prompts", json=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["tags"] == ["python"]
    
    def test_create_prompt_too_many_tags(self, client: TestClient):
        """Test creating prompt with more than 10 tags fails."""
        data = {
            "title": "Test",
            "content": "Content",
            "tags": [f"tag{i}" for i in range(11)]
        }
        response = client.post("/prompts", json=data)
        assert response.status_code == 422
    
    def test_patch_prompt_add_tags(self, client: TestClient, sample_prompt_data):
        """Test adding tags to existing prompt via PATCH."""
        # Create prompt without tags
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Add tags
        patch_data = {"tags": ["python", "testing"]}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        assert response.json()["tags"] == ["python", "testing"]
    
    def test_patch_prompt_remove_all_tags(self, client: TestClient):
        """Test removing all tags via PATCH."""
        # Create prompt with tags
        data = {
            "title": "Test",
            "content": "Content",
            "tags": ["python", "testing"]
        }
        create_response = client.post("/prompts", json=data)
        prompt_id = create_response.json()["id"]
        
        # Remove all tags
        patch_data = {"tags": []}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        assert response.json()["tags"] == []
    
    def test_filter_prompts_by_single_tag(self, client: TestClient):
        """Test filtering prompts by a single tag."""
        # Create prompts with different tags
        client.post("/prompts", json={
            "title": "P1",
            "content": "C1",
            "tags": ["python"]
        })
        client.post("/prompts", json={
            "title": "P2",
            "content": "C2",
            "tags": ["python", "testing"]
        })
        client.post("/prompts", json={
            "title": "P3",
            "content": "C3",
            "tags": ["javascript"]
        })
        
        # Filter by python tag
        response = client.get("/prompts?tags=python")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
    
    def test_filter_prompts_by_multiple_tags(self, client: TestClient):
        """Test filtering prompts by multiple tags (AND logic)."""
        # Create prompts
        client.post("/prompts", json={
            "title": "P1",
            "content": "C1",
            "tags": ["python", "testing"]
        })
        client.post("/prompts", json={
            "title": "P2",
            "content": "C2",
            "tags": ["python"]
        })
        client.post("/prompts", json={
            "title": "P3",
            "content": "C3",
            "tags": ["python", "testing", "advanced"]
        })
        
        # Filter by python AND testing
        response = client.get("/prompts?tags=python,testing")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
    
    def test_filter_by_nonexistent_tag(self, client: TestClient):
        """Test filtering by non-existent tag returns empty list."""
        response = client.get("/prompts?tags=nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["prompts"] == []
    
    def test_list_all_tags(self, client: TestClient):
        """Test GET /tags endpoint."""
        # Create prompts with tags
        client.post("/prompts", json={
            "title": "P1",
            "content": "C1",
            "tags": ["python", "testing"]
        })
        client.post("/prompts", json={
            "title": "P2",
            "content": "C2",
            "tags": ["python"]
        })
        
        response = client.get("/tags")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        
        # Check tags are sorted alphabetically
        tag_names = [t["name"] for t in data["tags"]]
        assert tag_names == ["python", "testing"]
        
        # Check usage counts
        python_tag = next(t for t in data["tags"] if t["name"] == "python")
        assert python_tag["usage_count"] == 2
    
    def test_list_tags_empty(self, client: TestClient):
        """Test GET /tags returns empty list when no tags exist."""
        response = client.get("/tags")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["tags"] == []
    
    def test_get_tag_details(self, client: TestClient):
        """Test GET /tags/{name} endpoint."""
        # Create prompts with tag
        client.post("/prompts", json={
            "title": "P1",
            "content": "C1",
            "tags": ["python"]
        })
        
        response = client.get("/tags/python")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "python"
        assert data["usage_count"] == 1
        assert "created_at" in data
    
    def test_get_tag_not_found(self, client: TestClient):
        """Test GET /tags/{name} returns 404 for non-existent tag."""
        response = client.get("/tags/nonexistent")
        assert response.status_code == 404
    
    def test_get_popular_tags(self, client: TestClient):
        """Test GET /tags/popular endpoint."""
        # Create prompts with various tags
        for i in range(5):
            client.post("/prompts", json={
                "title": f"P{i}",
                "content": f"C{i}",
                "tags": ["python"]
            })
        
        for i in range(3):
            client.post("/prompts", json={
                "title": f"P{i+5}",
                "content": f"C{i+5}",
                "tags": ["javascript"]
            })
        
        response = client.get("/tags/popular?limit=2")
        assert response.status_code == 200
        data = response.json()
        
        # Should return top 2 tags by usage
        assert len(data["tags"]) == 2
        assert data["tags"][0]["name"] == "python"
        assert data["tags"][0]["usage_count"] == 5
        assert data["tags"][1]["name"] == "javascript"
        assert data["tags"][1]["usage_count"] == 3
    
    def test_search_tags(self, client: TestClient):
        """Test searching tags by name."""
        # Create prompts with tags
        client.post("/prompts", json={
            "title": "P1",
            "content": "C1",
            "tags": ["python", "python3", "javascript"]
        })
        
        response = client.get("/tags?search=python")
        assert response.status_code == 200
        data = response.json()
        
        # Should return tags containing "python"
        tag_names = [t["name"] for t in data["tags"]]
        assert "python" in tag_names
        assert "python3" in tag_names
        assert "javascript" not in tag_names
    
    def test_combined_filters_tags_and_collection(self, client: TestClient, sample_collection_data):
        """Test combining tag filter with collection filter."""
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompts
        client.post("/prompts", json={
            "title": "P1",
            "content": "C1",
            "tags": ["python"],
            "collection_id": collection_id
        })
        client.post("/prompts", json={
            "title": "P2",
            "content": "C2",
            "tags": ["python"]
        })
        
        # Filter by tag AND collection
        response = client.get(f"/prompts?tags=python&collection_id={collection_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
    
    def test_combined_filters_tags_and_search(self, client: TestClient):
        """Test combining tag filter with search."""
        # Create prompts
        client.post("/prompts", json={
            "title": "Python Code Review",
            "content": "Review code",
            "tags": ["python"]
        })
        client.post("/prompts", json={
            "title": "Python Testing",
            "content": "Test code",
            "tags": ["python"]
        })
        client.post("/prompts", json={
            "title": "JavaScript Review",
            "content": "Review JS",
            "tags": ["javascript"]
        })
        
        # Filter by tag AND search
        response = client.get("/prompts?tags=python&search=review")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Python Code Review"
