"""In-memory storage for PromptLab.

This module provides simple in-memory storage for prompts and collections.
Data is stored in Python dictionaries and persists only during the application
runtime. In a production environment, this would be replaced with a database
like PostgreSQL, MongoDB, or SQLite.

Note:
    All data is lost when the application restarts. This is suitable for
    development and testing but not for production use.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection, Tag, PromptVersion


class Storage:
    """In-memory storage manager for prompts, collections, and tags.
    
    Provides CRUD operations for prompts, collections, and tags using Python
    dictionaries as the underlying storage mechanism. Thread-safe for
    single-threaded applications but not suitable for concurrent access.
    
    Attributes:
        _prompts (Dict[str, Prompt]): Dictionary mapping prompt IDs to Prompt objects.
        _collections (Dict[str, Collection]): Dictionary mapping collection IDs to Collection objects.
        _tags (Dict[str, Tag]): Dictionary mapping tag names to Tag objects.
        
    Examples:
        >>> storage = Storage()
        >>> prompt = Prompt(title="Test", content="Content")
        >>> storage.create_prompt(prompt)
        >>> retrieved = storage.get_prompt(prompt.id)
    """
    
    def __init__(self):
        """Initialize empty storage dictionaries."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._tags: Dict[str, Tag] = {}
        self._versions: Dict[str, List[PromptVersion]] = {}  # prompt_id -> list of versions
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a new prompt.
        
        Args:
            prompt: The Prompt object to store.
            
        Returns:
            Prompt: The stored Prompt object (same as input).
            
        Examples:
            >>> prompt = Prompt(title="My Prompt", content="Content")
            >>> stored = storage.create_prompt(prompt)
            >>> stored.id == prompt.id
            True
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID.
        
        Args:
            prompt_id: The unique identifier of the prompt.
            
        Returns:
            Optional[Prompt]: The Prompt object if found, None otherwise.
            
        Examples:
            >>> prompt = storage.get_prompt("abc123")
            >>> if prompt:
            ...     print(prompt.title)
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all stored prompts.
        
        Returns:
            List[Prompt]: List of all Prompt objects in storage.
            
        Examples:
            >>> prompts = storage.get_all_prompts()
            >>> len(prompts)
            5
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt.
        
        Args:
            prompt_id: The ID of the prompt to update.
            prompt: The new Prompt object with updated data.
            
        Returns:
            Optional[Prompt]: The updated Prompt object if found, None if prompt doesn't exist.
            
        Examples:
            >>> updated = storage.update_prompt("abc123", new_prompt)
            >>> if updated:
            ...     print("Update successful")
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its ID.
        
        Args:
            prompt_id: The unique identifier of the prompt to delete.
            
        Returns:
            bool: True if prompt was deleted, False if prompt didn't exist.
            
        Examples:
            >>> success = storage.delete_prompt("abc123")
            >>> if success:
            ...     print("Deleted successfully")
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Store a new collection.
        
        Args:
            collection: The Collection object to store.
            
        Returns:
            Collection: The stored Collection object (same as input).
            
        Examples:
            >>> collection = Collection(name="Development")
            >>> stored = storage.create_collection(collection)
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID.
        
        Args:
            collection_id: The unique identifier of the collection.
            
        Returns:
            Optional[Collection]: The Collection object if found, None otherwise.
            
        Examples:
            >>> collection = storage.get_collection("xyz789")
            >>> if collection:
            ...     print(collection.name)
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all stored collections.
        
        Returns:
            List[Collection]: List of all Collection objects in storage.
            
        Examples:
            >>> collections = storage.get_all_collections()
            >>> for col in collections:
            ...     print(col.name)
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its ID.
        
        Args:
            collection_id: The unique identifier of the collection to delete.
            
        Returns:
            bool: True if collection was deleted, False if collection didn't exist.
            
        Note:
            This does not automatically delete prompts in the collection.
            The API layer handles orphaned prompts separately.
            
        Examples:
            >>> success = storage.delete_collection("xyz789")
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts belonging to a specific collection.
        
        Args:
            collection_id: The unique identifier of the collection.
            
        Returns:
            List[Prompt]: List of Prompt objects that belong to the specified collection.
                Returns empty list if no prompts found.
            
        Examples:
            >>> prompts = storage.get_prompts_by_collection("xyz789")
            >>> print(f"Found {len(prompts)} prompts in collection")
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clear all stored data.
        
        Removes all prompts and collections from storage. Primarily used
        for testing purposes.
        
        Warning:
            This operation cannot be undone. All data will be lost.
            
        Examples:
            >>> storage.clear()
            >>> len(storage.get_all_prompts())
            0
        """
        self._prompts.clear()
        self._collections.clear()
        self._tags.clear()
        self._versions.clear()
    
    # ============== Version Operations ==============
    
    def create_version(self, version: PromptVersion) -> PromptVersion:
        """Store a new prompt version.
        
        Args:
            version: The PromptVersion object to store.
            
        Returns:
            PromptVersion: The stored version object.
            
        Examples:
            >>> version = PromptVersion(prompt_id="p-123", version=1, title="Test", content="Content")
            >>> stored = storage.create_version(version)
        """
        if version.prompt_id not in self._versions:
            self._versions[version.prompt_id] = []
        self._versions[version.prompt_id].append(version)
        return version
    
    def get_versions(self, prompt_id: str) -> List[PromptVersion]:
        """Get all versions for a prompt, sorted by version number (newest first).
        
        Args:
            prompt_id: The unique identifier of the prompt.
            
        Returns:
            List[PromptVersion]: List of versions sorted by version number descending.
            
        Examples:
            >>> versions = storage.get_versions("p-123")
            >>> print(f"Found {len(versions)} versions")
        """
        if prompt_id not in self._versions:
            return []
        versions = self._versions[prompt_id]
        return sorted(versions, key=lambda v: v.version, reverse=True)
    
    def get_version(self, prompt_id: str, version: int) -> Optional[PromptVersion]:
        """Get a specific version by number.
        
        Args:
            prompt_id: The unique identifier of the prompt.
            version: The version number to retrieve.
            
        Returns:
            Optional[PromptVersion]: The version object if found, None otherwise.
            
        Examples:
            >>> version = storage.get_version("p-123", 2)
            >>> if version:
            ...     print(f"Version {version.version}: {version.title}")
        """
        if prompt_id not in self._versions:
            return None
        for v in self._versions[prompt_id]:
            if v.version == version:
                return v
        return None
    
    def get_version_count(self, prompt_id: str) -> int:
        """Get total version count for a prompt.
        
        Args:
            prompt_id: The unique identifier of the prompt.
            
        Returns:
            int: Number of versions for this prompt.
            
        Examples:
            >>> count = storage.get_version_count("p-123")
            >>> print(f"Prompt has {count} versions")
        """
        if prompt_id not in self._versions:
            return 0
        return len(self._versions[prompt_id])
    
    def delete_versions_for_prompt(self, prompt_id: str):
        """Delete all versions for a prompt.
        
        Args:
            prompt_id: The unique identifier of the prompt.
            
        Examples:
            >>> storage.delete_versions_for_prompt("p-123")
        """
        if prompt_id in self._versions:
            del self._versions[prompt_id]
    
    # ============== Tag Operations ==============
    
    def get_all_tags(self) -> List[Tag]:
        """Get all tags sorted alphabetically.
        
        Returns:
            List[Tag]: List of all Tag objects sorted by name.
            
        Examples:
            >>> tags = storage.get_all_tags()
            >>> print(f"Found {len(tags)} tags")
        """
        tags = list(self._tags.values())
        return sorted(tags, key=lambda t: t.name)
    
    def get_tag(self, tag_name: str) -> Optional[Tag]:
        """Get a specific tag by name.
        
        Args:
            tag_name: The tag name to retrieve.
            
        Returns:
            Optional[Tag]: The Tag object if found, None otherwise.
            
        Examples:
            >>> tag = storage.get_tag("python")
            >>> if tag:
            ...     print(f"Tag usage: {tag.usage_count}")
        """
        return self._tags.get(tag_name)
    
    def create_or_update_tag(self, tag_name: str) -> Tag:
        """Create tag if new, or increment usage count if exists.
        
        Args:
            tag_name: The tag name to create or update.
            
        Returns:
            Tag: The created or updated Tag object.
            
        Examples:
            >>> tag = storage.create_or_update_tag("python")
            >>> assert tag.usage_count == 1
        """
        if tag_name in self._tags:
            self._tags[tag_name].usage_count += 1
        else:
            self._tags[tag_name] = Tag(name=tag_name, usage_count=1)
        return self._tags[tag_name]
    
    def update_tag_usage(self, tag_name: str, delta: int):
        """Update tag usage count by delta (+1 or -1).
        
        Args:
            tag_name: The tag name to update.
            delta: The change in usage count (typically +1 or -1).
            
        Examples:
            >>> storage.update_tag_usage("python", 1)  # Increment
            >>> storage.update_tag_usage("python", -1)  # Decrement
        """
        if tag_name in self._tags:
            self._tags[tag_name].usage_count += delta
            # Remove tag if usage drops to 0
            if self._tags[tag_name].usage_count <= 0:
                del self._tags[tag_name]
    
    def get_prompts_by_tag(self, tag_name: str) -> List[Prompt]:
        """Get all prompts with a specific tag.
        
        Args:
            tag_name: The tag name to filter by.
            
        Returns:
            List[Prompt]: List of prompts containing the specified tag.
            
        Examples:
            >>> prompts = storage.get_prompts_by_tag("python")
            >>> print(f"Found {len(prompts)} Python prompts")
        """
        return [p for p in self._prompts.values() if tag_name in p.tags]
    
    def get_prompts_by_tags(self, tag_names: List[str]) -> List[Prompt]:
        """Get prompts that have ALL specified tags (AND logic).
        
        Args:
            tag_names: List of tag names (all must be present).
            
        Returns:
            List[Prompt]: List of prompts containing all specified tags.
            
        Examples:
            >>> prompts = storage.get_prompts_by_tags(["python", "testing"])
            >>> # Returns only prompts with BOTH tags
        """
        if not tag_names:
            return list(self._prompts.values())
        
        return [
            p for p in self._prompts.values()
            if all(tag in p.tags for tag in tag_names)
        ]


# Global storage instance
storage = Storage()
