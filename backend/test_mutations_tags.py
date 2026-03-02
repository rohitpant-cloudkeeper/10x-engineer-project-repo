#!/usr/bin/env python3
"""
Mutation testing script for tagging system.

This script introduces intentional bugs (mutations) into the tagging code
and verifies that our test suite catches them.
"""

import subprocess
import sys
from typing import List, Tuple


class MutationTest:
    """Represents a single mutation test."""
    
    def __init__(self, name: str, file_path: str, original: str, mutated: str, description: str):
        self.name = name
        self.file_path = file_path
        self.original = original
        self.mutated = mutated
        self.description = description
        self.passed = False
        self.output = ""


def read_file(path: str) -> str:
    """Read file content."""
    with open(path, 'r') as f:
        return f.read()


def write_file(path: str, content: str):
    """Write content to file."""
    with open(path, 'w') as f:
        f.write(content)


def run_tests() -> Tuple[bool, str]:
    """Run pytest and return (success, output)."""
    try:
        result = subprocess.run(
            ['python', '-m', 'pytest', 'tests/test_tags.py', '-v', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Tests timed out"
    except Exception as e:
        return False, str(e)


def apply_mutation(mutation: MutationTest) -> bool:
    """Apply a mutation to the code. Returns True if mutation was applied."""
    content = read_file(mutation.file_path)
    if mutation.original not in content:
        return False
    mutated_content = content.replace(mutation.original, mutation.mutated, 1)
    write_file(mutation.file_path, mutated_content)
    return True


def revert_mutation(mutation: MutationTest):
    """Revert a mutation."""
    content = read_file(mutation.file_path)
    reverted_content = content.replace(mutation.mutated, mutation.original, 1)
    write_file(mutation.file_path, reverted_content)


def create_mutations() -> List[MutationTest]:
    """Create list of mutations to test."""
    return [
        # Mutation 1: Tag normalization - remove lowercase conversion
        MutationTest(
            name="Mutation 1: Skip lowercase conversion",
            file_path="app/utils.py",
            original="    tag = tag.lower().strip()",
            mutated="    tag = tag.strip()  # BUG: removed .lower()",
            description="Remove lowercase conversion in normalize_tag"
        ),
        
        # Mutation 2: Tag normalization - don't replace spaces
        MutationTest(
            name="Mutation 2: Skip space replacement",
            file_path="app/utils.py",
            original="    tag = tag.replace(\" \", \"-\")",
            mutated="    tag = tag  # BUG: removed space replacement",
            description="Skip space-to-hyphen replacement"
        ),
        
        # Mutation 3: Tag validation - wrong pattern
        MutationTest(
            name="Mutation 3: Wrong validation pattern",
            file_path="app/utils.py",
            original="    if not re.match(r'^[a-z0-9-]+$', tag):",
            mutated="    if not re.match(r'^[a-zA-Z0-9-]+$', tag):  # BUG: allows uppercase",
            description="Allow uppercase in validation (should fail)"
        ),
        
        # Mutation 4: Tag usage count - don't increment
        MutationTest(
            name="Mutation 4: Skip usage count increment",
            file_path="app/storage.py",
            original="        if tag_name in self._tags:\n            self._tags[tag_name].usage_count += 1",
            mutated="        if tag_name in self._tags:\n            pass  # BUG: don't increment usage",
            description="Don't increment tag usage count"
        ),
        
        # Mutation 5: Tag filtering - use OR instead of AND
        MutationTest(
            name="Mutation 5: Use OR logic instead of AND",
            file_path="app/storage.py",
            original="            if all(tag in p.tags for tag in tag_names)",
            mutated="            if any(tag in p.tags for tag in tag_names)  # BUG: OR instead of AND",
            description="Use OR logic instead of AND for tag filtering"
        ),
        
        # Mutation 6: Tag creation - don't set usage count
        MutationTest(
            name="Mutation 6: Wrong initial usage count",
            file_path="app/storage.py",
            original="            self._tags[tag_name] = Tag(name=tag_name, usage_count=1)",
            mutated="            self._tags[tag_name] = Tag(name=tag_name, usage_count=0)  # BUG: wrong count",
            description="Set initial usage count to 0 instead of 1"
        ),
        
        # Mutation 7: Delete prompt - don't decrement tag usage
        MutationTest(
            name="Mutation 7: Skip tag usage decrement on delete",
            file_path="app/api.py",
            original="    # Decrement usage count for all tags\n    for tag in prompt.tags:\n        storage.update_tag_usage(tag, -1)",
            mutated="    # BUG: Skip tag usage decrement\n    pass",
            description="Don't decrement tag usage when deleting prompt"
        ),
        
        # Mutation 8: Normalize tags - don't remove duplicates
        MutationTest(
            name="Mutation 8: Keep duplicate tags",
            file_path="app/utils.py",
            original="    return list(set(normalized))",
            mutated="    return normalized  # BUG: don't remove duplicates",
            description="Don't remove duplicate tags"
        ),
        
        # Mutation 9: Tag length validation - wrong max length
        MutationTest(
            name="Mutation 9: Wrong max tag length",
            file_path="app/utils.py",
            original="    if len(tag) < 1 or len(tag) > 30:",
            mutated="    if len(tag) < 1 or len(tag) > 50:  # BUG: wrong max length",
            description="Allow tags longer than 30 characters"
        ),
        
        # Mutation 10: Update prompt tags - don't update old tags
        MutationTest(
            name="Mutation 10: Skip old tag removal",
            file_path="app/api.py",
            original="        # Remove old tags\n        for tag in existing.tags:\n            storage.update_tag_usage(tag, -1)",
            mutated="        # BUG: Skip old tag removal\n        pass",
            description="Don't decrement usage for old tags when updating"
        ),
        
        # Mutation 11: Tag sorting - don't sort alphabetically
        MutationTest(
            name="Mutation 11: Skip tag sorting",
            file_path="app/storage.py",
            original="        return sorted(tags, key=lambda t: t.name)",
            mutated="        return tags  # BUG: don't sort",
            description="Return unsorted tags"
        ),
        
        # Mutation 12: Popular tags - sort ascending instead of descending
        MutationTest(
            name="Mutation 12: Wrong sort order for popular tags",
            file_path="app/api.py",
            original="    tags = sorted(tags, key=lambda t: t.usage_count, reverse=True)",
            mutated="    tags = sorted(tags, key=lambda t: t.usage_count, reverse=False)  # BUG: ascending",
            description="Sort popular tags in ascending order"
        ),
    ]


def run_mutation_tests():
    """Run all mutation tests."""
    mutations = create_mutations()
    
    print("=" * 80)
    print("MUTATION TESTING FOR TAGGING SYSTEM")
    print("=" * 80)
    print(f"\nTotal mutations to test: {len(mutations)}\n")
    
    # First, verify tests pass without mutations
    print("Step 1: Verifying tests pass without mutations...")
    success, output = run_tests()
    if not success:
        print("❌ FAILED: Tests don't pass without mutations!")
        print("\nTest output:")
        print(output)
        return False
    print("✅ All tests pass without mutations\n")
    
    # Run each mutation
    results = []
    for i, mutation in enumerate(mutations, 1):
        print(f"\n{'=' * 80}")
        print(f"MUTATION {i}/{len(mutations)}: {mutation.name}")
        print(f"{'=' * 80}")
        print(f"Description: {mutation.description}")
        print(f"File: {mutation.file_path}")
        print(f"\nOriginal code:")
        print(f"  {mutation.original[:100]}...")
        print(f"\nMutated code:")
        print(f"  {mutation.mutated[:100]}...")
        
        # Apply mutation
        if not apply_mutation(mutation):
            print(f"\n⚠️  WARNING: Could not apply mutation (code not found)")
            continue
        
        print(f"\n🔬 Running tests with mutation applied...")
        
        # Run tests
        success, output = run_tests()
        mutation.passed = not success  # Mutation test passes if tests FAIL
        mutation.output = output
        
        # Revert mutation
        revert_mutation(mutation)
        
        # Report result
        if mutation.passed:
            print(f"✅ MUTATION KILLED: Tests caught the bug!")
            results.append((mutation.name, "KILLED", "Tests failed as expected"))
        else:
            print(f"❌ MUTATION SURVIVED: Tests didn't catch the bug!")
            print(f"\nThis means our tests are not strong enough to detect this bug.")
            results.append((mutation.name, "SURVIVED", "Tests passed despite bug"))
        
        # Show relevant test output
        if not mutation.passed:
            print(f"\nTest output (first 500 chars):")
            print(output[:500])
    
    # Summary
    print(f"\n\n{'=' * 80}")
    print("MUTATION TESTING SUMMARY")
    print(f"{'=' * 80}\n")
    
    killed = sum(1 for _, status, _ in results if status == "KILLED")
    survived = sum(1 for _, status, _ in results if status == "SURVIVED")
    
    print(f"Total mutations: {len(results)}")
    print(f"Mutations killed: {killed} ({killed/len(results)*100:.1f}%)")
    print(f"Mutations survived: {survived} ({survived/len(results)*100:.1f}%)")
    print()
    
    # Detailed results
    print("\nDetailed Results:")
    print("-" * 80)
    for name, status, note in results:
        emoji = "✅" if status == "KILLED" else "❌"
        print(f"{emoji} {name}: {status}")
        if status == "SURVIVED":
            print(f"   → {note}")
    
    print("\n" + "=" * 80)
    
    if survived > 0:
        print(f"\n⚠️  WARNING: {survived} mutation(s) survived!")
        print("This indicates weak test coverage for those scenarios.")
        print("Consider adding more specific tests to catch these bugs.")
        return False
    else:
        print("\n🎉 SUCCESS: All mutations were killed!")
        print("Your test suite is strong and catches all introduced bugs.")
        return True


if __name__ == "__main__":
    try:
        success = run_mutation_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nMutation testing interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during mutation testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
