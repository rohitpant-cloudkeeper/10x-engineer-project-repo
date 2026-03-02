"""Test fixtures for PromptLab"""

import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.storage import storage as global_storage, Storage


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


@pytest.fixture
def storage():
    """Create a fresh storage instance for each test."""
    return Storage()


@pytest.fixture(autouse=True)
def clear_storage():
    """Clear global storage before each test."""
    global_storage.clear()
    yield
    global_storage.clear()


@pytest.fixture
def sample_prompt_data():
    """Sample prompt data for testing."""
    return {
        "title": "Code Review Prompt",
        "content": "Review the following code and provide feedback:\n\n{{code}}",
        "description": "A prompt for AI code review"
    }


@pytest.fixture
def sample_collection_data():
    """Sample collection data for testing."""
    return {
        "name": "Development",
        "description": "Prompts for development tasks"
    }
