"""Tests for prompt version tracking system.

This module tests the version tracking functionality including version models,
automatic version creation, version retrieval, revert, and compare operations.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from fastapi.testclient import TestClient

from app.models import Prompt, PromptVersion


class TestPromptVersionModel:
    """Tests for PromptVersion model."""
    
    def test_create_version_valid(self):
        """Test creating a valid prompt version."""
        version = PromptVersion(
            prompt_id="prompt-123",
            version=1,
            title="Test Prompt",
            content="Test content"
        )
        assert version.prompt_id == "prompt-123"
        assert version.version == 1
        assert version.title == "Test Prompt"
        assert version.content == "Test content"
        assert isinstance(version.created_at, datetime)
        assert version.id is not None
    
    def test_version_with_optional_fields(self):
        """Test version with description and collection_id."""
        version = PromptVersion(
            prompt_id="prompt-123",
            version=2,
            title="Test",
            content="Content",
            description="Test description",
            collection_id="col-123"
        )
        assert version.description == "Test description"
        assert version.collection_id == "col-123"
    
    def test_version_required_fields(self):
        """Test that required fields are enforced."""
        with pytest.raises(ValidationError):
            PromptVersion(version=1, title="Test", content="Content")  # Missing prompt_id
        
        with pytest.raises(ValidationError):
            PromptVersion(prompt_id="p-123", title="Test", content="Content")  # Missing version
    
    def test_version_number_positive(self):
        """Test that version number must be positive."""
        with pytest.raises(ValidationError):
            PromptVersion(
                prompt_id="p-123",
                version=0,  # Invalid
                title="Test",
                content="Content"
            )
        
        with pytest.raises(ValidationError):
            PromptVersion(
                prompt_id="p-123",
                version=-1,  # Invalid
                title="Test",
                content="Content"
            )


class TestPromptWithVersionFields:
    """Tests for Prompt model with version fields."""
    
    def test_prompt_has_version_fields(self):
        """Test that Prompt model has version and version_count fields."""
        prompt = Prompt(
            title="Test",
            content="Content"
        )
        assert hasattr(prompt, 'version')
        assert hasattr(prompt, 'version_count')
    
    def test_prompt_default_version(self):
        """Test that new prompts start at version 1."""
        prompt = Prompt(
            title="Test",
            content="Content"
        )
        assert prompt.version == 1
        assert prompt.version_count == 1
    
    def test_prompt_with_custom_version(self):
        """Test creating prompt with specific version."""
        prompt = Prompt(
            title="Test",
            content="Content",
            version=3,
            version_count=3
        )
        assert prompt.version == 3
        assert prompt.version_count == 3


class TestVersionStorage:
    """Tests for version storage operations."""
    
    def test_create_version(self, storage):
        """Test creating a version in storage."""
        version = PromptVersion(
            prompt_id="p-123",
            version=1,
            title="Test",
            content="Content"
        )
        result = storage.create_version(version)
        
        assert result.id == version.id
        assert result.prompt_id == "p-123"
        assert result.version == 1
    
    def test_get_versions_empty(self, storage):
        """Test getting versions for prompt with no versions."""
        versions = storage.get_versions("nonexistent")
        assert versions == []
    
    def test_get_versions_sorted(self, storage):
        """Test versions are returned sorted by version number (newest first)."""
        # Create versions out of order
        v1 = PromptVersion(prompt_id="p-123", version=1, title="V1", content="C1")
        v3 = PromptVersion(prompt_id="p-123", version=3, title="V3", content="C3")
        v2 = PromptVersion(prompt_id="p-123", version=2, title="V2", content="C2")
        
        storage.create_version(v1)
        storage.create_version(v3)
        storage.create_version(v2)
        
        versions = storage.get_versions("p-123")
        assert len(versions) == 3
        assert versions[0].version == 3  # Newest first
        assert versions[1].version == 2
        assert versions[2].version == 1
    
    def test_get_specific_version(self, storage):
        """Test getting a specific version by number."""
        v1 = PromptVersion(prompt_id="p-123", version=1, title="V1", content="C1")
        v2 = PromptVersion(prompt_id="p-123", version=2, title="V2", content="C2")
        
        storage.create_version(v1)
        storage.create_version(v2)
        
        version = storage.get_version("p-123", 2)
        assert version is not None
        assert version.version == 2
        assert version.title == "V2"
    
    def test_get_nonexistent_version(self, storage):
        """Test getting a version that doesn't exist."""
        version = storage.get_version("p-123", 99)
        assert version is None
    
    def test_get_version_count(self, storage):
        """Test getting version count for a prompt."""
        v1 = PromptVersion(prompt_id="p-123", version=1, title="V1", content="C1")
        v2 = PromptVersion(prompt_id="p-123", version=2, title="V2", content="C2")
        
        storage.create_version(v1)
        storage.create_version(v2)
        
        count = storage.get_version_count("p-123")
        assert count == 2
    
    def test_get_version_count_empty(self, storage):
        """Test version count for prompt with no versions."""
        count = storage.get_version_count("nonexistent")
        assert count == 0
    
    def test_delete_versions_for_prompt(self, storage):
        """Test deleting all versions for a prompt."""
        v1 = PromptVersion(prompt_id="p-123", version=1, title="V1", content="C1")
        v2 = PromptVersion(prompt_id="p-123", version=2, title="V2", content="C2")
        
        storage.create_version(v1)
        storage.create_version(v2)
        
        storage.delete_versions_for_prompt("p-123")
        
        versions = storage.get_versions("p-123")
        assert versions == []


class TestAutomaticVersionCreation:
    """Tests for automatic version creation on prompt updates."""
    
    def test_update_prompt_creates_version(self, client: TestClient):
        """Test that updating a prompt creates a new version."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "Original Title",
            "content": "Original content"
        })
        prompt_id = response.json()["id"]
        
        # Update prompt
        client.put(f"/prompts/{prompt_id}", json={
            "title": "Updated Title",
            "content": "Updated content"
        })
        
        # Check versions
        response = client.get(f"/prompts/{prompt_id}/versions")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2  # Original + update
        assert data["versions"][0]["version"] == 2
        assert data["versions"][0]["title"] == "Updated Title"
        assert data["versions"][1]["version"] == 1
        assert data["versions"][1]["title"] == "Original Title"
    
    def test_patch_prompt_creates_version(self, client: TestClient):
        """Test that patching a prompt creates a new version."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "Original",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        # Patch prompt
        client.patch(f"/prompts/{prompt_id}", json={
            "title": "Patched"
        })
        
        # Check versions
        response = client.get(f"/prompts/{prompt_id}/versions")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
    
    def test_version_increments_correctly(self, client: TestClient):
        """Test that version numbers increment sequentially."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        # Multiple updates
        for i in range(2, 6):
            client.put(f"/prompts/{prompt_id}", json={
                "title": f"V{i}",
                "content": "Content"
            })
        
        # Check versions
        response = client.get(f"/prompts/{prompt_id}/versions")
        data = response.json()
        assert data["total"] == 5
        
        # Verify sequential version numbers
        versions = data["versions"]
        for i, version in enumerate(versions):
            assert version["version"] == 5 - i  # Newest first
    
    def test_prompt_version_fields_updated(self, client: TestClient):
        """Test that prompt's version and version_count fields are updated."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        prompt = response.json()
        assert prompt["version"] == 1
        assert prompt["version_count"] == 1
        
        # Update prompt
        response = client.put(f"/prompts/{prompt_id}", json={
            "title": "Updated",
            "content": "Content"
        })
        prompt = response.json()
        assert prompt["version"] == 2
        assert prompt["version_count"] == 2


class TestVersionAPI:
    """Tests for version API endpoints."""
    
    def test_list_versions(self, client: TestClient):
        """Test GET /prompts/{id}/versions endpoint."""
        # Create and update prompt
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        client.put(f"/prompts/{prompt_id}", json={
            "title": "V2",
            "content": "Content"
        })
        
        # List versions
        response = client.get(f"/prompts/{prompt_id}/versions")
        assert response.status_code == 200
        data = response.json()
        
        assert "versions" in data
        assert "total" in data
        assert "prompt_id" in data
        assert data["prompt_id"] == prompt_id
        assert data["total"] == 2
        assert len(data["versions"]) == 2
    
    def test_list_versions_prompt_not_found(self, client: TestClient):
        """Test listing versions for non-existent prompt."""
        response = client.get("/prompts/nonexistent/versions")
        assert response.status_code == 404
    
    def test_get_specific_version(self, client: TestClient):
        """Test GET /prompts/{id}/versions/{version} endpoint."""
        # Create and update prompt
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content 1"
        })
        prompt_id = response.json()["id"]
        
        client.put(f"/prompts/{prompt_id}", json={
            "title": "V2",
            "content": "Content 2"
        })
        
        # Get version 1
        response = client.get(f"/prompts/{prompt_id}/versions/1")
        assert response.status_code == 200
        version = response.json()
        assert version["version"] == 1
        assert version["title"] == "V1"
        assert version["content"] == "Content 1"
    
    def test_get_version_not_found(self, client: TestClient):
        """Test getting non-existent version."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        # Try to get non-existent version
        response = client.get(f"/prompts/{prompt_id}/versions/99")
        assert response.status_code == 404
    
    def test_revert_to_version(self, client: TestClient):
        """Test POST /prompts/{id}/versions/{version}/revert endpoint."""
        # Create prompt and make updates
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content 1",
            "description": "Desc 1"
        })
        prompt_id = response.json()["id"]
        
        client.put(f"/prompts/{prompt_id}", json={
            "title": "V2",
            "content": "Content 2",
            "description": "Desc 2"
        })
        
        client.put(f"/prompts/{prompt_id}", json={
            "title": "V3",
            "content": "Content 3",
            "description": "Desc 3"
        })
        
        # Revert to version 1
        response = client.post(f"/prompts/{prompt_id}/versions/1/revert")
        assert response.status_code == 200
        prompt = response.json()
        
        # Check prompt has V1 content but is now V4
        assert prompt["title"] == "V1"
        assert prompt["content"] == "Content 1"
        assert prompt["description"] == "Desc 1"
        assert prompt["version"] == 4
        assert prompt["version_count"] == 4
    
    def test_revert_creates_new_version(self, client: TestClient):
        """Test that reverting creates a new version."""
        # Create and update prompt
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        client.put(f"/prompts/{prompt_id}", json={
            "title": "V2",
            "content": "Content"
        })
        
        # Revert to V1
        client.post(f"/prompts/{prompt_id}/versions/1/revert")
        
        # Check versions
        response = client.get(f"/prompts/{prompt_id}/versions")
        data = response.json()
        assert data["total"] == 3  # V1, V2, V3 (revert)
        assert data["versions"][0]["version"] == 3
        assert data["versions"][0]["title"] == "V1"  # Same as V1
    
    def test_revert_to_current_version(self, client: TestClient):
        """Test reverting to the current version returns error."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        # Try to revert to current version (1)
        response = client.post(f"/prompts/{prompt_id}/versions/1/revert")
        assert response.status_code == 400
        assert "already on this version" in response.json()["detail"].lower()
    
    def test_revert_version_not_found(self, client: TestClient):
        """Test reverting to non-existent version."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        # Try to revert to non-existent version
        response = client.post(f"/prompts/{prompt_id}/versions/99/revert")
        assert response.status_code == 404
    
    def test_compare_versions(self, client: TestClient):
        """Test GET /prompts/{id}/versions/compare endpoint."""
        # Create prompt with multiple versions
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content 1",
            "description": "Desc 1"
        })
        prompt_id = response.json()["id"]
        
        client.put(f"/prompts/{prompt_id}", json={
            "title": "V2",
            "content": "Content 2",
            "description": "Desc 1"  # Same
        })
        
        # Compare versions
        response = client.get(f"/prompts/{prompt_id}/versions/compare?from=1&to=2")
        assert response.status_code == 200
        data = response.json()
        
        assert data["prompt_id"] == prompt_id
        assert "from_version" in data
        assert "to_version" in data
        assert "changes" in data
        
        assert data["from_version"]["version"] == 1
        assert data["to_version"]["version"] == 2
        
        # Check changes detection
        changes = data["changes"]
        assert changes["title"] == "changed"
        assert changes["content"] == "changed"
        assert changes["description"] == "unchanged"
    
    def test_compare_same_version(self, client: TestClient):
        """Test comparing a version with itself."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        # Compare version 1 with itself
        response = client.get(f"/prompts/{prompt_id}/versions/compare?from=1&to=1")
        assert response.status_code == 200
        data = response.json()
        
        # All fields should be unchanged
        changes = data["changes"]
        assert all(v == "unchanged" for v in changes.values())
    
    def test_compare_nonexistent_version(self, client: TestClient):
        """Test comparing with non-existent version."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        # Try to compare with non-existent version
        response = client.get(f"/prompts/{prompt_id}/versions/compare?from=1&to=99")
        assert response.status_code == 404


class TestVersionCascadeDelete:
    """Tests for cascade deletion of versions."""
    
    def test_delete_prompt_deletes_versions(self, client: TestClient):
        """Test that deleting a prompt deletes all its versions."""
        # Create and update prompt
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        client.put(f"/prompts/{prompt_id}", json={
            "title": "Updated",
            "content": "Content"
        })
        
        # Verify versions exist
        response = client.get(f"/prompts/{prompt_id}/versions")
        assert response.status_code == 200
        assert response.json()["total"] == 2
        
        # Delete prompt
        client.delete(f"/prompts/{prompt_id}")
        
        # Verify versions are gone
        response = client.get(f"/prompts/{prompt_id}/versions")
        assert response.status_code == 404


class TestVersionPagination:
    """Tests for version list pagination."""
    
    def test_version_pagination_limit(self, client: TestClient):
        """Test limiting number of versions returned."""
        # Create prompt with many versions
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        # Create 10 more versions
        for i in range(2, 12):
            client.put(f"/prompts/{prompt_id}", json={
                "title": f"V{i}",
                "content": "Content"
            })
        
        # Get with limit
        response = client.get(f"/prompts/{prompt_id}/versions?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["versions"]) == 5
        assert data["total"] == 11  # Total count unchanged
    
    def test_version_pagination_offset(self, client: TestClient):
        """Test skipping versions with offset."""
        # Create prompt with versions
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        for i in range(2, 6):
            client.put(f"/prompts/{prompt_id}", json={
                "title": f"V{i}",
                "content": "Content"
            })
        
        # Get with offset
        response = client.get(f"/prompts/{prompt_id}/versions?offset=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["versions"]) == 3  # 5 total - 2 offset
        assert data["versions"][0]["version"] == 3  # Skipped 5 and 4



class TestVersionFieldsUpdated:
    """Tests to verify version fields are properly updated."""
    
    def test_update_increments_version_field(self, client: TestClient):
        """Test that PUT updates increment the version field."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        assert response.json()["version"] == 1
        
        # Update prompt
        response = client.put(f"/prompts/{prompt_id}", json={
            "title": "V2",
            "content": "Content"
        })
        assert response.status_code == 200
        assert response.json()["version"] == 2
        
        # Update again
        response = client.put(f"/prompts/{prompt_id}", json={
            "title": "V3",
            "content": "Content"
        })
        assert response.status_code == 200
        assert response.json()["version"] == 3
    
    def test_patch_increments_version_field(self, client: TestClient):
        """Test that PATCH updates increment the version field."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        assert response.json()["version"] == 1
        
        # Patch prompt
        response = client.patch(f"/prompts/{prompt_id}", json={
            "title": "V2"
        })
        assert response.status_code == 200
        assert response.json()["version"] == 2
    
    def test_update_increments_version_count_field(self, client: TestClient):
        """Test that PUT updates increment the version_count field."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        assert response.json()["version_count"] == 1
        
        # Update prompt
        response = client.put(f"/prompts/{prompt_id}", json={
            "title": "V2",
            "content": "Content"
        })
        assert response.status_code == 200
        assert response.json()["version_count"] == 2
        
        # Update again
        response = client.put(f"/prompts/{prompt_id}", json={
            "title": "V3",
            "content": "Content"
        })
        assert response.status_code == 200
        assert response.json()["version_count"] == 3
    
    def test_patch_increments_version_count_field(self, client: TestClient):
        """Test that PATCH updates increment the version_count field."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        assert response.json()["version_count"] == 1
        
        # Patch prompt
        response = client.patch(f"/prompts/{prompt_id}", json={
            "title": "V2"
        })
        assert response.status_code == 200
        assert response.json()["version_count"] == 2
    
    def test_revert_increments_version_field(self, client: TestClient):
        """Test that revert increments the version field."""
        # Create and update prompt
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        client.put(f"/prompts/{prompt_id}", json={
            "title": "V2",
            "content": "Content"
        })
        
        # Revert to V1
        response = client.post(f"/prompts/{prompt_id}/versions/1/revert")
        assert response.status_code == 200
        assert response.json()["version"] == 3  # Should be 3, not 1
    
    def test_revert_increments_version_count_field(self, client: TestClient):
        """Test that revert increments the version_count field."""
        # Create and update prompt
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        client.put(f"/prompts/{prompt_id}", json={
            "title": "V2",
            "content": "Content"
        })
        
        # Revert to V1
        response = client.post(f"/prompts/{prompt_id}/versions/1/revert")
        assert response.status_code == 200
        assert response.json()["version_count"] == 3  # Should be 3, not 1


class TestVersionCascadeDeleteVerification:
    """Tests to verify versions are actually deleted."""
    
    def test_versions_actually_deleted_on_prompt_delete(self, client: TestClient):
        """Test that versions are actually removed from storage when prompt deleted."""
        from app.storage import storage
        
        # Create and update prompt
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        client.put(f"/prompts/{prompt_id}", json={
            "title": "Updated",
            "content": "Content"
        })
        
        # Verify versions exist in storage
        versions_before = storage.get_versions(prompt_id)
        assert len(versions_before) == 2
        
        # Delete prompt
        client.delete(f"/prompts/{prompt_id}")
        
        # Verify versions are gone from storage
        versions_after = storage.get_versions(prompt_id)
        assert len(versions_after) == 0
