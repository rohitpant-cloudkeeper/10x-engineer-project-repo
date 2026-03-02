#!/usr/bin/env python3
"""Mutation testing for version tracking feature.

This script tests the quality of version tracking tests by introducing
intentional bugs (mutations) and verifying that tests catch them.
"""

import sys
import subprocess
from typing import List, Tuple


class Mutation:
    """Represents a single mutation to test."""
    
    def __init__(self, name: str, file: str, original: str, mutated: str):
        """Initialize mutation.
        
        Args:
            name: Description of the mutation.
            file: File path to mutate.
            original: Original code to replace.
            mutated: Mutated code to insert.
        """
        self.name = name
        self.file = file
        self.original = original
        self.mutated = mutated


# Define mutations for version tracking feature
MUTATIONS: List[Mutation] = [
    # Mutation 1: Version doesn't increment
    Mutation(
        name="Version number doesn't increment on update",
        file="app/api.py",
        original="version=existing.version + 1,",
        mutated="version=existing.version,  # MUTATION: Don't increment"
    ),
    
    # Mutation 2: Version count doesn't increment
    Mutation(
        name="Version count doesn't increment on update",
        file="app/api.py",
        original="version_count=existing.version_count + 1,",
        mutated="version_count=existing.version_count,  # MUTATION: Don't increment"
    ),
    
    # Mutation 3: Version not created on update
    Mutation(
        name="Version not created after update",
        file="app/api.py",
        original="    # Create new version\n    create_prompt_version(updated_prompt)",
        mutated="    # MUTATION: Don't create version\n    pass  # create_prompt_version(updated_prompt)"
    ),
    
    # Mutation 4: Versions not sorted correctly
    Mutation(
        name="Versions not sorted by version number",
        file="app/storage.py",
        original="return sorted(versions, key=lambda v: v.version, reverse=True)",
        mutated="return sorted(versions, key=lambda v: v.version, reverse=False)  # MUTATION: Wrong order"
    ),
    
    # Mutation 5: Version validation allows zero
    Mutation(
        name="Version number validation allows zero",
        file="app/models.py",
        original='version: int = Field(..., gt=0, description="Version number (must be positive)")',
        mutated='version: int = Field(..., ge=0, description="Version number (must be positive)")  # MUTATION: Allow zero'
    ),
    
    # Mutation 6: Revert doesn't check current version
    Mutation(
        name="Revert allows reverting to current version",
        file="app/api.py",
        original="    if version == existing.version:",
        mutated="    if version == existing.version + 999:  # MUTATION: Never true"
    ),
    
    # Mutation 7: Compare doesn't detect content changes
    Mutation(
        name="Compare doesn't detect content changes",
        file="app/api.py",
        original='"content": "changed" if v1.content != v2.content else "unchanged",',
        mutated='"content": "unchanged",  # MUTATION: Always unchanged'
    ),
    
    # Mutation 8: Compare doesn't detect title changes
    Mutation(
        name="Compare doesn't detect title changes",
        file="app/api.py",
        original='"title": "changed" if v1.title != v2.title else "unchanged",',
        mutated='"title": "unchanged",  # MUTATION: Always unchanged'
    ),
    
    # Mutation 9: Versions not deleted on prompt delete
    Mutation(
        name="Versions not deleted when prompt deleted",
        file="app/api.py",
        original="    # Delete all versions\n    storage.delete_versions_for_prompt(prompt_id)",
        mutated="    # MUTATION: Don't delete versions\n    pass  # storage.delete_versions_for_prompt(prompt_id)"
    ),
    
    # Mutation 10: Pagination offset not applied
    Mutation(
        name="Pagination offset not applied correctly",
        file="app/api.py",
        original="    versions = all_versions[offset:offset + limit]",
        mutated="    versions = all_versions[:limit]  # MUTATION: Ignore offset"
    ),
    
    # Mutation 11: Revert doesn't increment version
    Mutation(
        name="Revert doesn't create new version number",
        file="app/api.py",
        original="        version=existing.version + 1,\n        version_count=existing.version_count + 1,",
        mutated="        version=existing.version,  # MUTATION: Don't increment\n        version_count=existing.version_count,"
    ),
    
    # Mutation 12: Initial version not created
    Mutation(
        name="Initial version not created on prompt creation",
        file="app/api.py",
        original="    # Create initial version\n    create_prompt_version(created_prompt)",
        mutated="    # MUTATION: Don't create initial version\n    pass  # create_prompt_version(created_prompt)"
    ),
]


def apply_mutation(mutation: Mutation) -> bool:
    """Apply a mutation to a file.
    
    Args:
        mutation: The mutation to apply.
        
    Returns:
        bool: True if mutation was applied successfully.
    """
    try:
        with open(mutation.file, 'r') as f:
            content = f.read()
        
        if mutation.original not in content:
            print(f"  ⚠️  Original code not found in {mutation.file}")
            return False
        
        mutated_content = content.replace(mutation.original, mutation.mutated, 1)
        
        with open(mutation.file, 'w') as f:
            f.write(mutated_content)
        
        return True
    except Exception as e:
        print(f"  ❌ Error applying mutation: {e}")
        return False


def revert_mutation(mutation: Mutation) -> bool:
    """Revert a mutation from a file.
    
    Args:
        mutation: The mutation to revert.
        
    Returns:
        bool: True if mutation was reverted successfully.
    """
    try:
        with open(mutation.file, 'r') as f:
            content = f.read()
        
        original_content = content.replace(mutation.mutated, mutation.original, 1)
        
        with open(mutation.file, 'w') as f:
            f.write(original_content)
        
        return True
    except Exception as e:
        print(f"  ❌ Error reverting mutation: {e}")
        return False


def run_tests() -> bool:
    """Run the test suite.
    
    Returns:
        bool: True if all tests pass, False otherwise.
    """
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/test_versions.py", "-v", "--tb=no", "-q"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("  ⏱️  Tests timed out")
        return False
    except Exception as e:
        print(f"  ❌ Error running tests: {e}")
        return False


def test_mutation(mutation: Mutation) -> Tuple[bool, str]:
    """Test a single mutation.
    
    Args:
        mutation: The mutation to test.
        
    Returns:
        Tuple of (killed, status_message).
    """
    print(f"\n🧬 Testing: {mutation.name}")
    
    # Apply mutation
    if not apply_mutation(mutation):
        return False, "Failed to apply mutation"
    
    # Run tests
    print("  🧪 Running tests...")
    tests_pass = run_tests()
    
    # Revert mutation
    revert_mutation(mutation)
    
    if tests_pass:
        print("  ❌ SURVIVED - Tests still pass with this bug!")
        return False, "SURVIVED"
    else:
        print("  ✅ KILLED - Tests caught this bug!")
        return True, "KILLED"


def main():
    """Run mutation testing."""
    print("=" * 70)
    print("🧬 MUTATION TESTING FOR VERSION TRACKING FEATURE")
    print("=" * 70)
    print(f"\nTesting {len(MUTATIONS)} mutations...\n")
    
    # First, verify tests pass without mutations
    print("🔍 Verifying baseline tests pass...")
    if not run_tests():
        print("❌ Baseline tests are failing! Fix tests before running mutations.")
        sys.exit(1)
    print("✅ Baseline tests pass\n")
    
    # Test each mutation
    results = []
    for i, mutation in enumerate(MUTATIONS, 1):
        print(f"\n[{i}/{len(MUTATIONS)}]", end=" ")
        killed, status = test_mutation(mutation)
        results.append((mutation.name, killed, status))
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 MUTATION TESTING RESULTS")
    print("=" * 70)
    
    killed_count = sum(1 for _, killed, _ in results if killed)
    total_count = len(results)
    survival_rate = ((total_count - killed_count) / total_count * 100) if total_count > 0 else 0
    kill_rate = (killed_count / total_count * 100) if total_count > 0 else 0
    
    print(f"\nTotal Mutations: {total_count}")
    print(f"Killed: {killed_count} ({kill_rate:.1f}%)")
    print(f"Survived: {total_count - killed_count} ({survival_rate:.1f}%)")
    
    print("\n📋 Detailed Results:")
    print("-" * 70)
    for name, killed, status in results:
        icon = "✅" if killed else "❌"
        print(f"{icon} {status:8} - {name}")
    
    print("\n" + "=" * 70)
    
    if kill_rate >= 90:
        print("🎉 EXCELLENT! Your tests are very strong (≥90% kill rate)")
        return 0
    elif kill_rate >= 80:
        print("👍 GOOD! Your tests are strong (≥80% kill rate)")
        return 0
    elif kill_rate >= 70:
        print("⚠️  FAIR. Consider adding more tests (≥70% kill rate)")
        return 1
    else:
        print("❌ WEAK. Your tests need significant improvement (<70% kill rate)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
