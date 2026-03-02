"""Additional tests to increase API coverage.

This module contains tests specifically designed to cover edge cases
and missing branches in the API layer.
"""

import pytest
from fastapi.testclient import TestClient


class TestPromptListFiltering:
    """Tests for combined filtering scenarios in list_prompts."""
    
    def test_list_prompts_with_tags_and_collection(self, client: TestClient):
        """Test filtering by both tags and collection."""
        # Create collection
        col_response = client.post("/collections", json={
            "name": "Test Collection"
        })
        col_id = col_response.json()["id"]
        
        # Create prompts with different combinations
        client.post("/prompts", json={
            "title": "Prompt 1",
            "content": "Content 1",
            "collection_id": col_id,
            "tags": ["python", "testing"]
        })
        
        client.post("/prompts", json={
            "title": "Prompt 2",
            "content": "Content 2",
            "collection_id": col_id,
            "tags": ["python"]
        })
        
        client.post("/prompts", json={
            "title": "Prompt 3",
            "content": "Content 3",
            "tags": ["python", "testing"]
        })
        
        # Filter by tags and collection
        response = client.get(f"/prompts?tags=python,testing&collection_id={col_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Prompt 1"
    
    def test_list_prompts_with_tags_and_search(self, client: TestClient):
        """Test filtering by both tags and search query."""
        # Create prompts
        client.post("/prompts", json={
            "title": "Python Testing Guide",
            "content": "Content 1",
            "tags": ["python", "testing"]
        })
        
        client.post("/prompts", json={
            "title": "Python Basics",
            "content": "Content 2",
            "tags": ["python"]
        })
        
        client.post("/prompts", json={
            "title": "Testing Guide",
            "content": "Content 3",
            "tags": ["testing"]
        })
        
        # Filter by tags and search
        response = client.get("/prompts?tags=python&search=testing")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Python Testing Guide"
    
    def test_list_prompts_all_filters_combined(self, client: TestClient):
        """Test filtering by tags, collection, and search together."""
        # Create collection
        col_response = client.post("/collections", json={
            "name": "Dev Collection"
        })
        col_id = col_response.json()["id"]
        
        # Create prompts
        client.post("/prompts", json={
            "title": "Python Testing Guide",
            "content": "Content 1",
            "collection_id": col_id,
            "tags": ["python", "testing"]
        })
        
        client.post("/prompts", json={
            "title": "Python Guide",
            "content": "Content 2",
            "collection_id": col_id,
            "tags": ["python"]
        })
        
        # Filter by all three
        response = client.get(f"/prompts?tags=python,testing&collection_id={col_id}&search=testing")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Python Testing Guide"


class TestUpdatePromptEdgeCases:
    """Tests for edge cases in prompt update operations."""
    
    def test_update_prompt_with_tags(self, client: TestClient):
        """Test updating prompt with tags."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "Original",
            "content": "Content",
            "tags": ["old-tag"]
        })
        prompt_id = response.json()["id"]
        
        # Update with new tags
        response = client.put(f"/prompts/{prompt_id}", json={
            "title": "Updated",
            "content": "Content",
            "tags": ["new-tag", "another-tag"]
        })
        assert response.status_code == 200
        
        # Verify old tag usage decreased
        old_tag = client.get("/tags/old-tag")
        assert old_tag.status_code == 404  # Should be deleted when usage = 0
        
        # Verify new tags created
        new_tag = client.get("/tags/new-tag")
        assert new_tag.status_code == 200
        assert new_tag.json()["usage_count"] == 1
    
    def test_update_prompt_remove_all_tags(self, client: TestClient):
        """Test updating prompt to remove all tags."""
        # Create prompt with tags
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content",
            "tags": ["tag1", "tag2"]
        })
        prompt_id = response.json()["id"]
        
        # Update to remove all tags
        response = client.put(f"/prompts/{prompt_id}", json={
            "title": "Test",
            "content": "Content",
            "tags": []
        })
        assert response.status_code == 200
        
        # Verify tags removed
        prompt = response.json()
        assert prompt["tags"] == []
        
        # Verify tag usage decreased
        tag1 = client.get("/tags/tag1")
        assert tag1.status_code == 404


class TestPatchPromptEdgeCases:
    """Tests for edge cases in patch operations."""
    
    def test_patch_prompt_with_empty_tags(self, client: TestClient):
        """Test patching prompt with empty tags list."""
        # Create prompt with tags
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content",
            "tags": ["tag1"]
        })
        prompt_id = response.json()["id"]
        
        # Patch with empty tags
        response = client.patch(f"/prompts/{prompt_id}", json={
            "tags": []
        })
        assert response.status_code == 200
        assert response.json()["tags"] == []


class TestVersionEdgeCases:
    """Tests for edge cases in version operations."""
    
    def test_revert_updates_tags_correctly(self, client: TestClient):
        """Test that reverting updates tag usage counts."""
        # Create prompt with tags
        response = client.post("/prompts", json={
            "title": "V1",
            "content": "Content",
            "tags": ["tag1"]
        })
        prompt_id = response.json()["id"]
        
        # Update with different tags
        client.put(f"/prompts/{prompt_id}", json={
            "title": "V2",
            "content": "Content",
            "tags": ["tag2"]
        })
        
        # Revert to V1
        response = client.post(f"/prompts/{prompt_id}/versions/1/revert")
        assert response.status_code == 200
        
        # Verify tags restored
        prompt = response.json()
        assert prompt["tags"] == ["tag1"]
        
        # Verify tag usage counts
        tag1 = client.get("/tags/tag1")
        assert tag1.status_code == 200
        assert tag1.json()["usage_count"] == 1
        
        tag2 = client.get("/tags/tag2")
        assert tag2.status_code == 404  # Should be deleted
    
    def test_compare_versions_with_tag_changes(self, client: TestClient):
        """Test comparing versions with tag changes."""
        # Create prompt
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content",
            "tags": ["tag1"]
        })
        prompt_id = response.json()["id"]
        
        # Update tags
        client.put(f"/prompts/{prompt_id}", json={
            "title": "Test",
            "content": "Content",
            "tags": ["tag2"]
        })
        
        # Compare versions
        response = client.get(f"/prompts/{prompt_id}/versions/compare?from=1&to=2")
        assert response.status_code == 200
        data = response.json()
        
        assert data["changes"]["tags"] == "changed"
        assert data["changes"]["title"] == "unchanged"
    
    def test_compare_versions_with_collection_changes(self, client: TestClient):
        """Test comparing versions with collection changes."""
        # Create collection
        col_response = client.post("/collections", json={
            "name": "Test Collection"
        })
        col_id = col_response.json()["id"]
        
        # Create prompt without collection
        response = client.post("/prompts", json={
            "title": "Test",
            "content": "Content"
        })
        prompt_id = response.json()["id"]
        
        # Update with collection
        client.put(f"/prompts/{prompt_id}", json={
            "title": "Test",
            "content": "Content",
            "collection_id": col_id
        })
        
        # Compare versions
        response = client.get(f"/prompts/{prompt_id}/versions/compare?from=1&to=2")
        assert response.status_code == 200
        data = response.json()
        
        assert data["changes"]["collection_id"] == "changed"


class TestTagEndpointEdgeCases:
    """Tests for edge cases in tag endpoints."""
    
    def test_get_popular_tags_with_custom_limit(self, client: TestClient):
        """Test getting popular tags with custom limit."""
        # Create prompts with different tags
        for i in range(5):
            client.post("/prompts", json={
                "title": f"Prompt {i}",
                "content": "Content",
                "tags": [f"tag{i}"]
            })
        
        # Get top 3 popular tags
        response = client.get("/tags/popular?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tags"]) <= 3
    
    def test_search_tags_case_insensitive(self, client: TestClient):
        """Test tag search is case insensitive."""
        # Create prompt with tag
        client.post("/prompts", json={
            "title": "Test",
            "content": "Content",
            "tags": ["python"]
        })
        
        # Search with uppercase
        response = client.get("/tags?search=PYTHON")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["tags"][0]["name"] == "python"
    
    def test_search_tags_partial_match(self, client: TestClient):
        """Test tag search with partial match."""
        # Create prompts with tags
        client.post("/prompts", json={
            "title": "Test 1",
            "content": "Content",
            "tags": ["python"]
        })
        
        client.post("/prompts", json={
            "title": "Test 2",
            "content": "Content",
            "tags": ["python-testing"]
        })
        
        # Search with partial match
        response = client.get("/tags?search=python")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
