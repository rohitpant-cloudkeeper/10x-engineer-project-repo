"""Unit tests for utility functions."""

import pytest
from datetime import datetime, timedelta
from app.models import Prompt
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables
)


@pytest.fixture
def sample_prompts():
    """Create sample prompts with different timestamps."""
    now = datetime.utcnow()
    
    prompt1 = Prompt(
        title="First Prompt",
        content="Content 1",
        description="Description 1",
        collection_id="col-1"
    )
    prompt1.created_at = now - timedelta(days=2)
    
    prompt2 = Prompt(
        title="Second Prompt",
        content="Content 2",
        description="Description 2",
        collection_id="col-1"
    )
    prompt2.created_at = now - timedelta(days=1)
    
    prompt3 = Prompt(
        title="Third Prompt",
        content="Content 3",
        description="Description 3",
        collection_id="col-2"
    )
    prompt3.created_at = now
    
    return [prompt1, prompt2, prompt3]


class TestSortPromptsByDate:
    """Test sort_prompts_by_date function."""
    
    def test_sort_descending_default(self, sample_prompts):
        """Test sorting by date descending (newest first) - default."""
        result = sort_prompts_by_date(sample_prompts)
        assert result[0].title == "Third Prompt"
        assert result[1].title == "Second Prompt"
        assert result[2].title == "First Prompt"
    
    def test_sort_descending_explicit(self, sample_prompts):
        """Test sorting by date descending explicitly."""
        result = sort_prompts_by_date(sample_prompts, descending=True)
        assert result[0].title == "Third Prompt"
        assert result[1].title == "Second Prompt"
        assert result[2].title == "First Prompt"
    
    def test_sort_ascending(self, sample_prompts):
        """Test sorting by date ascending (oldest first)."""
        result = sort_prompts_by_date(sample_prompts, descending=False)
        assert result[0].title == "First Prompt"
        assert result[1].title == "Second Prompt"
        assert result[2].title == "Third Prompt"
    
    def test_sort_empty_list(self):
        """Test sorting empty list."""
        result = sort_prompts_by_date([])
        assert result == []
    
    def test_sort_single_prompt(self):
        """Test sorting single prompt."""
        prompt = Prompt(title="Test", content="Content")
        result = sort_prompts_by_date([prompt])
        assert len(result) == 1
        assert result[0] == prompt
    
    def test_sort_does_not_modify_original(self, sample_prompts):
        """Test that sorting doesn't modify original list."""
        original_order = [p.title for p in sample_prompts]
        sort_prompts_by_date(sample_prompts)
        current_order = [p.title for p in sample_prompts]
        assert original_order == current_order


class TestFilterPromptsByCollection:
    """Test filter_prompts_by_collection function."""
    
    def test_filter_by_collection(self, sample_prompts):
        """Test filtering prompts by collection ID."""
        result = filter_prompts_by_collection(sample_prompts, "col-1")
        assert len(result) == 2
        assert all(p.collection_id == "col-1" for p in result)
    
    def test_filter_by_different_collection(self, sample_prompts):
        """Test filtering by different collection."""
        result = filter_prompts_by_collection(sample_prompts, "col-2")
        assert len(result) == 1
        assert result[0].collection_id == "col-2"
    
    def test_filter_by_nonexistent_collection(self, sample_prompts):
        """Test filtering by non-existent collection returns empty list."""
        result = filter_prompts_by_collection(sample_prompts, "non-existent")
        assert result == []
    
    def test_filter_empty_list(self):
        """Test filtering empty list."""
        result = filter_prompts_by_collection([], "col-1")
        assert result == []
    
    def test_filter_prompts_without_collection(self):
        """Test filtering prompts without collection_id."""
        prompts = [
            Prompt(title="P1", content="C1", collection_id=None),
            Prompt(title="P2", content="C2", collection_id="col-1")
        ]
        result = filter_prompts_by_collection(prompts, "col-1")
        assert len(result) == 1
        assert result[0].title == "P2"


class TestSearchPrompts:
    """Test search_prompts function."""
    
    def test_search_by_title(self):
        """Test searching prompts by title."""
        prompts = [
            Prompt(title="Python Code Review", content="Content 1"),
            Prompt(title="JavaScript Linter", content="Content 2"),
            Prompt(title="Python Debugger", content="Content 3")
        ]
        result = search_prompts(prompts, "python")
        assert len(result) == 2
        assert all("python" in p.title.lower() for p in result)
    
    def test_search_by_description(self):
        """Test searching prompts by description."""
        prompts = [
            Prompt(title="Prompt 1", content="C1", description="Python helper"),
            Prompt(title="Prompt 2", content="C2", description="JavaScript tool"),
            Prompt(title="Prompt 3", content="C3", description="Python utility")
        ]
        result = search_prompts(prompts, "python")
        assert len(result) == 2
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        prompts = [
            Prompt(title="PYTHON Code", content="Content"),
            Prompt(title="python script", content="Content"),
            Prompt(title="Python Tool", content="Content")
        ]
        result = search_prompts(prompts, "python")
        assert len(result) == 3
    
    def test_search_no_matches(self):
        """Test search with no matches returns empty list."""
        prompts = [
            Prompt(title="JavaScript", content="Content"),
            Prompt(title="Ruby", content="Content")
        ]
        result = search_prompts(prompts, "python")
        assert result == []
    
    def test_search_empty_list(self):
        """Test searching empty list."""
        result = search_prompts([], "python")
        assert result == []
    
    def test_search_empty_query(self):
        """Test search with empty query returns all prompts."""
        prompts = [
            Prompt(title="Prompt 1", content="Content 1"),
            Prompt(title="Prompt 2", content="Content 2")
        ]
        result = search_prompts(prompts, "")
        assert len(result) == 2
    
    def test_search_with_special_characters(self):
        """Test search with special characters."""
        prompts = [
            Prompt(title="C++ Programming", content="Content"),
            Prompt(title="C# Development", content="Content")
        ]
        result = search_prompts(prompts, "c++")
        assert len(result) == 1
        assert "C++" in result[0].title
    
    def test_search_prompts_without_description(self):
        """Test searching prompts that have no description."""
        prompts = [
            Prompt(title="Python Code", content="Content", description=None),
            Prompt(title="JavaScript", content="Content", description="Python tool")
        ]
        result = search_prompts(prompts, "python")
        assert len(result) == 2


class TestValidatePromptContent:
    """Test validate_prompt_content function."""
    
    def test_valid_content(self):
        """Test validation of valid content."""
        assert validate_prompt_content("This is valid content") is True
    
    def test_valid_content_exactly_10_chars(self):
        """Test content with exactly 10 characters."""
        assert validate_prompt_content("1234567890") is True
    
    def test_valid_content_with_whitespace(self):
        """Test valid content with leading/trailing whitespace."""
        assert validate_prompt_content("  Valid content  ") is True
    
    def test_invalid_empty_string(self):
        """Test that empty string is invalid."""
        assert validate_prompt_content("") is False
    
    def test_invalid_only_whitespace(self):
        """Test that only whitespace is invalid."""
        assert validate_prompt_content("   ") is False
        assert validate_prompt_content("\t\n") is False
    
    def test_invalid_too_short(self):
        """Test that content shorter than 10 chars is invalid."""
        assert validate_prompt_content("short") is False
        assert validate_prompt_content("123456789") is False
    
    def test_invalid_too_short_after_strip(self):
        """Test content that's too short after stripping whitespace."""
        assert validate_prompt_content("  short  ") is False
    
    def test_valid_multiline_content(self):
        """Test valid multiline content."""
        content = """This is a
        multiline content
        that is valid"""
        assert validate_prompt_content(content) is True


class TestExtractVariables:
    """Test extract_variables function."""
    
    def test_extract_single_variable(self):
        """Test extracting single variable."""
        content = "Hello {{name}}"
        result = extract_variables(content)
        assert result == ["name"]
    
    def test_extract_multiple_variables(self):
        """Test extracting multiple variables."""
        content = "Hello {{name}}, your {{item}} is ready!"
        result = extract_variables(content)
        assert result == ["name", "item"]
    
    def test_extract_no_variables(self):
        """Test content with no variables."""
        content = "This has no variables"
        result = extract_variables(content)
        assert result == []
    
    def test_extract_variables_with_underscores(self):
        """Test variables with underscores."""
        content = "User: {{user_name}}, ID: {{user_id}}"
        result = extract_variables(content)
        assert result == ["user_name", "user_id"]
    
    def test_extract_variables_with_numbers(self):
        """Test variables with numbers."""
        content = "Item {{item1}} and {{item2}}"
        result = extract_variables(content)
        assert result == ["item1", "item2"]
    
    def test_extract_duplicate_variables(self):
        """Test that duplicate variables are included."""
        content = "{{name}} and {{name}} again"
        result = extract_variables(content)
        assert result == ["name", "name"]
    
    def test_extract_variables_case_sensitive(self):
        """Test that variable extraction is case-sensitive."""
        content = "{{Name}} and {{name}}"
        result = extract_variables(content)
        assert result == ["Name", "name"]
    
    def test_extract_empty_string(self):
        """Test extracting from empty string."""
        result = extract_variables("")
        assert result == []
    
    def test_extract_malformed_variables(self):
        """Test that malformed variables are not extracted."""
        content = "{name} or {{name or name}}"
        result = extract_variables(content)
        assert result == []
    
    def test_extract_variables_with_spaces_not_matched(self):
        """Test that variables with spaces are not matched."""
        content = "{{ name }}"
        result = extract_variables(content)
        assert result == []
