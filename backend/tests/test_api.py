"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data
    
    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0
    
    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)
        
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1
    
    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
    
    def test_get_prompt_not_found(self, client: TestClient):
        """Test that getting a non-existent prompt returns 404.
        
        NOTE: This test currently FAILS due to Bug #1!
        The API returns 500 instead of 404.
        """
        response = client.get("/prompts/nonexistent-id")
        # This should be 404, but there's a bug...
        assert response.status_code == 404  # Will fail until bug is fixed
    
    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/prompts/{prompt_id}")
        # Note: This might fail due to Bug #1
        assert get_response.status_code in [404, 500]  # 404 after fix
    
    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Update it
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description"
        }
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp would change
        
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        
        # NOTE: This assertion will fail due to Bug #2!
        # The updated_at should be different from original
        # assert data["updated_at"] != original_updated_at  # Uncomment after fix
    
    def test_sorting_order(self, client: TestClient):
        """Test that prompts are sorted newest first.
        
        NOTE: This test might fail due to Bug #3!
        """
        import time
        
        # Create prompts with delay
        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}
        
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)
        
        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        
        # Newest (Second) should be first
        assert prompts[0]["title"] == "Second"  # Will fail until Bug #3 fixed


class TestCollections:
    """Tests for collection endpoints."""
    
    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data
    
    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
    
    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test deleting a collection that has prompts.
        
        NOTE: Bug #4 - prompts become orphaned after collection deletion.
        This test documents the current (buggy) behavior.
        After fixing, update the test to verify correct behavior.
        """
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Delete collection
        client.delete(f"/collections/{collection_id}")
        
        # After fix: prompts should have collection_id set to None
        prompts = client.get("/prompts").json()["prompts"]
        assert len(prompts) == 1
        assert prompts[0]["collection_id"] is None  # Fixed: no longer orphaned
    
    def test_delete_collection_not_found(self, client: TestClient):
        """Test deleting a non-existent collection returns 404."""
        response = client.delete("/collections/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Collection not found"


class TestPromptPatch:
    """Tests for PATCH /prompts/{id} endpoint."""
    
    def test_patch_prompt_title_only(self, client: TestClient, sample_prompt_data):
        """Test partial update of only the title."""
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_content = create_response.json()["content"]
        
        # Patch only the title
        patch_data = {"title": "Patched Title"}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched Title"
        assert data["content"] == original_content  # Unchanged
    
    def test_patch_prompt_multiple_fields(self, client: TestClient, sample_prompt_data):
        """Test partial update of multiple fields."""
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_content = create_response.json()["content"]
        
        # Patch title and description
        patch_data = {
            "title": "New Title",
            "description": "New description"
        }
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["description"] == "New description"
        assert data["content"] == original_content  # Unchanged
    
    def test_patch_prompt_not_found(self, client: TestClient):
        """Test patching a non-existent prompt returns 404."""
        patch_data = {"title": "New Title"}
        response = client.patch("/prompts/nonexistent-id", json=patch_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"
    
    def test_patch_prompt_with_collection(self, client: TestClient, sample_prompt_data, sample_collection_data):
        """Test patching prompt with valid collection_id."""
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Patch with collection_id
        patch_data = {"collection_id": collection_id}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        assert response.json()["collection_id"] == collection_id
    
    def test_patch_prompt_invalid_collection(self, client: TestClient, sample_prompt_data):
        """Test patching prompt with invalid collection_id returns 400."""
        # Create prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Patch with invalid collection_id
        patch_data = {"collection_id": "nonexistent-collection"}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Collection not found"
    
    def test_patch_prompt_updates_timestamp(self, client: TestClient, sample_prompt_data):
        """Test that PATCH updates the updated_at timestamp."""
        import time
        
        # Create prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        time.sleep(0.1)
        
        # Patch the prompt
        patch_data = {"title": "Updated Title"}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        assert response.json()["updated_at"] != original_updated_at


class TestPromptValidation:
    """Tests for prompt validation and error cases."""
    
    def test_create_prompt_invalid_collection(self, client: TestClient, sample_prompt_data):
        """Test creating prompt with invalid collection_id returns 400."""
        prompt_data = {**sample_prompt_data, "collection_id": "nonexistent-collection"}
        response = client.post("/prompts", json=prompt_data)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Collection not found"
    
    def test_create_prompt_missing_required_fields(self, client: TestClient):
        """Test creating prompt without required fields returns 422."""
        # Missing title and content
        response = client.post("/prompts", json={})
        assert response.status_code == 422
    
    def test_update_prompt_not_found(self, client: TestClient, sample_prompt_data):
        """Test updating non-existent prompt returns 404."""
        update_data = {
            "title": "Updated",
            "content": "Updated content",
            "description": "Updated description"
        }
        response = client.put("/prompts/nonexistent-id", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"
    
    def test_update_prompt_invalid_collection(self, client: TestClient, sample_prompt_data):
        """Test updating prompt with invalid collection_id returns 400."""
        # Create prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Update with invalid collection
        update_data = {
            "title": "Updated",
            "content": "Updated content",
            "description": "Updated description",
            "collection_id": "nonexistent-collection"
        }
        response = client.put(f"/prompts/{prompt_id}", json=update_data)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Collection not found"
    
    def test_delete_prompt_not_found(self, client: TestClient):
        """Test deleting non-existent prompt returns 404."""
        response = client.delete("/prompts/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"


class TestPromptFiltering:
    """Tests for prompt filtering and search functionality."""
    
    def test_filter_by_collection(self, client: TestClient, sample_prompt_data, sample_collection_data):
        """Test filtering prompts by collection_id."""
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompts - one in collection, one without
        prompt_in_collection = {**sample_prompt_data, "collection_id": collection_id}
        client.post("/prompts", json=prompt_in_collection)
        
        prompt_without_collection = {
            "title": "Standalone Prompt",
            "content": "Content without collection"
        }
        client.post("/prompts", json=prompt_without_collection)
        
        # Filter by collection
        response = client.get(f"/prompts?collection_id={collection_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["collection_id"] == collection_id
    
    def test_search_prompts(self, client: TestClient):
        """Test searching prompts by title and description."""
        # Create prompts with different titles
        prompt1 = {
            "title": "Code Review Prompt",
            "content": "Review this code",
            "description": "For reviewing code"
        }
        prompt2 = {
            "title": "Documentation Generator",
            "content": "Generate docs",
            "description": "Creates documentation"
        }
        client.post("/prompts", json=prompt1)
        client.post("/prompts", json=prompt2)
        
        # Search for "code"
        response = client.get("/prompts?search=code")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert "Code Review" in data["prompts"][0]["title"]
    
    def test_filter_and_search_combined(self, client: TestClient, sample_collection_data):
        """Test combining collection filter and search."""
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompts
        prompt1 = {
            "title": "Code Review",
            "content": "Review code",
            "collection_id": collection_id
        }
        prompt2 = {
            "title": "Code Generator",
            "content": "Generate code",
            "collection_id": collection_id
        }
        prompt3 = {
            "title": "Code Formatter",
            "content": "Format code"
        }
        client.post("/prompts", json=prompt1)
        client.post("/prompts", json=prompt2)
        client.post("/prompts", json=prompt3)
        
        # Filter by collection and search
        response = client.get(f"/prompts?collection_id={collection_id}&search=review")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Code Review"
