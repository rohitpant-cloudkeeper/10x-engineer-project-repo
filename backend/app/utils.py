"""Utility functions for PromptLab.

This module provides helper functions for common operations like sorting,
filtering, and searching prompts. These functions are used by the API layer
to process data before returning responses.
"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.
    
    Args:
        prompts: List of Prompt objects to sort.
        descending: If True, sort newest first. If False, sort oldest first.
                   Defaults to True (newest first).
    
    Returns:
        List[Prompt]: A new sorted list of Prompt objects. Original list is not modified.
        
    Examples:
        >>> prompts = [prompt1, prompt2, prompt3]
        >>> sorted_prompts = sort_prompts_by_date(prompts, descending=True)
        >>> sorted_prompts[0].created_at > sorted_prompts[1].created_at
        True
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts to only those belonging to a specific collection.
    
    Args:
        prompts: List of Prompt objects to filter.
        collection_id: The collection ID to filter by.
        
    Returns:
        List[Prompt]: A new list containing only prompts with matching collection_id.
        
    Examples:
        >>> all_prompts = storage.get_all_prompts()
        >>> dev_prompts = filter_prompts_by_collection(all_prompts, "dev-123")
        >>> all(p.collection_id == "dev-123" for p in dev_prompts)
        True
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description.
    
    Performs case-insensitive substring matching against prompt titles
    and descriptions. Returns prompts where the query appears in either field.
    
    Args:
        prompts: List of Prompt objects to search.
        query: Search string to look for (case-insensitive).
        
    Returns:
        List[Prompt]: A new list containing only prompts matching the search query.
        
    Examples:
        >>> prompts = storage.get_all_prompts()
        >>> results = search_prompts(prompts, "code review")
        >>> all("code review" in p.title.lower() or 
        ...     "code review" in (p.description or "").lower() 
        ...     for p in results)
        True
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Check if prompt content is valid.
    
    A valid prompt must:
    - Not be empty or only whitespace
    - Be at least 10 characters long (after stripping whitespace)
    
    Args:
        content: The prompt content string to validate.
        
    Returns:
        bool: True if content is valid, False otherwise.
        
    Examples:
        >>> validate_prompt_content("This is a valid prompt")
        True
        >>> validate_prompt_content("   ")
        False
        >>> validate_prompt_content("short")
        False
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Variables are defined using double curly braces: {{variable_name}}
    This function finds all such variables in the content.
    
    Args:
        content: The prompt content string to parse.
        
    Returns:
        List[str]: List of variable names found (without the braces).
            Returns empty list if no variables found.
        
    Examples:
        >>> content = "Hello {{name}}, your {{item}} is ready!"
        >>> extract_variables(content)
        ['name', 'item']
        >>> extract_variables("No variables here")
        []
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
