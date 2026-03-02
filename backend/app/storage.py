"""Storage layer for PromptLab.

This module provides in-memory storage for prompts, collections, tags, and versions.
Uses a modular design with separate storage classes for each entity type.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection, Tag, PromptVersion


class PromptStorage:
    """Storage manager for prompts and their versions.
    
    Handles CRUD operations for prompts and version history tracking.
    
    Attributes:
        _prompts (Dict[str, Prompt]): Dictionary mapping prompt IDs to Prompt objects.
        _versions (Dict[str, List[PromptVersion]]): Dictionary mapping prompt IDs to version lists.
    """
    
    def __init__(self):
        """Initialize empty prompt storage."""
        self._prompts: Dict[str, Prompt] = {}
        self._versions: Dict[str, List[PromptVersion]] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a new prompt."""
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID."""
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all stored prompts."""
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt."""
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its ID."""
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts belonging to a specific collection."""
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    def get_prompts_by_tag(self, tag_name: str) -> List[Prompt]:
        """Get all prompts with a specific tag."""
        return [p for p in self._prompts.values() if tag_name in p.tags]
    
    def get_prompts_by_tags(self, tag_names: List[str]) -> List[Prompt]:
        """Get prompts that have ALL specified tags (AND logic)."""
        if not tag_names:
            return list(self._prompts.values())
        
        return [
            p for p in self._prompts.values()
            if all(tag in p.tags for tag in tag_names)
        ]
    
    # ============== Version Operations ==============
    
    def create_version(self, version: PromptVersion) -> PromptVersion:
        """Store a new prompt version."""
        if version.prompt_id not in self._versions:
            self._versions[version.prompt_id] = []
        self._versions[version.prompt_id].append(version)
        return version
    
    def get_versions(self, prompt_id: str) -> List[PromptVersion]:
        """Get all versions for a prompt, sorted by version number (newest first)."""
        if prompt_id not in self._versions:
            return []
        versions = self._versions[prompt_id]
        return sorted(versions, key=lambda v: v.version, reverse=True)
    
    def get_version(self, prompt_id: str, version: int) -> Optional[PromptVersion]:
        """Get a specific version by number."""
        if prompt_id not in self._versions:
            return None
        for v in self._versions[prompt_id]:
            if v.version == version:
                return v
        return None
    
    def get_version_count(self, prompt_id: str) -> int:
        """Get total version count for a prompt."""
        if prompt_id not in self._versions:
            return 0
        return len(self._versions[prompt_id])
    
    def delete_versions_for_prompt(self, prompt_id: str):
        """Delete all versions for a prompt."""
        if prompt_id in self._versions:
            del self._versions[prompt_id]
    
    def clear(self):
        """Clear all prompt and version data."""
        self._prompts.clear()
        self._versions.clear()


class CollectionStorage:
    """Storage manager for collections.
    
    Handles CRUD operations for prompt collections.
    
    Attributes:
        _collections (Dict[str, Collection]): Dictionary mapping collection IDs to Collection objects.
    """
    
    def __init__(self):
        """Initialize empty collection storage."""
        self._collections: Dict[str, Collection] = {}
    
    def create_collection(self, collection: Collection) -> Collection:
        """Store a new collection."""
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID."""
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all stored collections."""
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its ID."""
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def clear(self):
        """Clear all collection data."""
        self._collections.clear()


class TagStorage:
    """Storage manager for tags.
    
    Handles CRUD operations for tags and usage tracking.
    
    Attributes:
        _tags (Dict[str, Tag]): Dictionary mapping tag names to Tag objects.
    """
    
    def __init__(self):
        """Initialize empty tag storage."""
        self._tags: Dict[str, Tag] = {}
    
    def get_all_tags(self) -> List[Tag]:
        """Get all tags sorted alphabetically."""
        tags = list(self._tags.values())
        return sorted(tags, key=lambda t: t.name)
    
    def get_tag(self, tag_name: str) -> Optional[Tag]:
        """Get a specific tag by name."""
        return self._tags.get(tag_name)
    
    def create_or_update_tag(self, tag_name: str) -> Tag:
        """Create tag if new, or increment usage count if exists."""
        if tag_name in self._tags:
            self._tags[tag_name].usage_count += 1
        else:
            self._tags[tag_name] = Tag(name=tag_name, usage_count=1)
        return self._tags[tag_name]
    
    def update_tag_usage(self, tag_name: str, delta: int):
        """Update tag usage count by delta (+1 or -1)."""
        if tag_name in self._tags:
            self._tags[tag_name].usage_count += delta
            # Remove tag if usage drops to 0
            if self._tags[tag_name].usage_count <= 0:
                del self._tags[tag_name]
    
    def clear(self):
        """Clear all tag data."""
        self._tags.clear()


class Storage:
    """Unified storage facade for all entity types.
    
    Provides a single interface to access prompt, collection, tag, and version storage.
    Uses composition to delegate operations to specialized storage classes.
    
    This facade pattern maintains backward compatibility while providing better
    separation of concerns internally.
    
    Attributes:
        prompts (PromptStorage): Storage for prompts and versions.
        collections (CollectionStorage): Storage for collections.
        tags (TagStorage): Storage for tags.
        
    Examples:
        >>> storage = Storage()
        >>> prompt = Prompt(title="Test", content="Content")
        >>> storage.create_prompt(prompt)
        >>> retrieved = storage.get_prompt(prompt.id)
    """
    
    def __init__(self):
        """Initialize storage with all sub-storages."""
        self.prompts = PromptStorage()
        self.collections = CollectionStorage()
        self.tags = TagStorage()
    
    # ============== Prompt Operations (Delegated) ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a new prompt."""
        return self.prompts.create_prompt(prompt)
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID."""
        return self.prompts.get_prompt(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all stored prompts."""
        return self.prompts.get_all_prompts()
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt."""
        return self.prompts.update_prompt(prompt_id, prompt)
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its ID."""
        return self.prompts.delete_prompt(prompt_id)
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts belonging to a specific collection."""
        return self.prompts.get_prompts_by_collection(collection_id)
    
    # ============== Collection Operations (Delegated) ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Store a new collection."""
        return self.collections.create_collection(collection)
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID."""
        return self.collections.get_collection(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all stored collections."""
        return self.collections.get_all_collections()
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its ID."""
        return self.collections.delete_collection(collection_id)
    
    # ============== Version Operations (Delegated) ==============
    
    def create_version(self, version: PromptVersion) -> PromptVersion:
        """Store a new prompt version."""
        return self.prompts.create_version(version)
    
    def get_versions(self, prompt_id: str) -> List[PromptVersion]:
        """Get all versions for a prompt, sorted by version number (newest first)."""
        return self.prompts.get_versions(prompt_id)
    
    def get_version(self, prompt_id: str, version: int) -> Optional[PromptVersion]:
        """Get a specific version by number."""
        return self.prompts.get_version(prompt_id, version)
    
    def get_version_count(self, prompt_id: str) -> int:
        """Get total version count for a prompt."""
        return self.prompts.get_version_count(prompt_id)
    
    def delete_versions_for_prompt(self, prompt_id: str):
        """Delete all versions for a prompt."""
        return self.prompts.delete_versions_for_prompt(prompt_id)
    
    # ============== Tag Operations (Delegated) ==============
    
    def get_all_tags(self) -> List[Tag]:
        """Get all tags sorted alphabetically."""
        return self.tags.get_all_tags()
    
    def get_tag(self, tag_name: str) -> Optional[Tag]:
        """Get a specific tag by name."""
        return self.tags.get_tag(tag_name)
    
    def create_or_update_tag(self, tag_name: str) -> Tag:
        """Create tag if new, or increment usage count if exists."""
        return self.tags.create_or_update_tag(tag_name)
    
    def update_tag_usage(self, tag_name: str, delta: int):
        """Update tag usage count by delta (+1 or -1)."""
        return self.tags.update_tag_usage(tag_name, delta)
    
    def get_prompts_by_tag(self, tag_name: str) -> List[Prompt]:
        """Get all prompts with a specific tag."""
        return self.prompts.get_prompts_by_tag(tag_name)
    
    def get_prompts_by_tags(self, tag_names: List[str]) -> List[Prompt]:
        """Get prompts that have ALL specified tags (AND logic)."""
        return self.prompts.get_prompts_by_tags(tag_names)
    
    # ============== Utility ==============
    
    def clear(self):
        """Clear all stored data.
        
        Removes all prompts, collections, tags, and versions from storage.
        Primarily used for testing purposes.
        
        Warning:
            This operation cannot be undone. All data will be lost.
        """
        self.prompts.clear()
        self.collections.clear()
        self.tags.clear()


# Global storage instance
storage = Storage()
