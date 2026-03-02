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
from app.models import Prompt, Collection


class Storage:
    """In-memory storage manager for prompts and collections.
    
    Provides CRUD operations for prompts and collections using Python
    dictionaries as the underlying storage mechanism. Thread-safe for
    single-threaded applications but not suitable for concurrent access.
    
    Attributes:
        _prompts (Dict[str, Prompt]): Dictionary mapping prompt IDs to Prompt objects.
        _collections (Dict[str, Collection]): Dictionary mapping collection IDs to Collection objects.
        
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


# Global storage instance
storage = Storage()
