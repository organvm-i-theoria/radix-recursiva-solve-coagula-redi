#!/usr/bin/env python3
"""
Test script to verify the path traversal vulnerability fix in experimental_habitat_implementation.py
"""

import sys
from experimental_habitat_implementation import ExperimentalHabitat, ExperimentalSystem

def test_path_traversal_prevention():
    """Test that malicious experiment names are rejected"""
    
    print("🔒 Testing Path Traversal Vulnerability Fix")
    print("=" * 60)
    
    # Create a test habitat
    habitat = ExperimentalHabitat("security_test_lab", isolation_level=3)
    
    # Test cases for path traversal attempts
    malicious_names = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32",
        "../escape",
        "../../parent",
        "name/../traversal",
        "name/../../traverse",
        "./current",
        "name with spaces",
        "name/with/slashes",
        "name\\with\\backslashes",
        "name;with;semicolons",
        "name|with|pipes",
        "name&with&ampersands",
        "name$with$dollars",
        "name`with`backticks",
        "name(with)parens",
        "name[with]brackets",
        "name{with}braces",
        "name<with>angles",
        "name'with'quotes",
        'name"with"doublequotes',
        "name\nwith\nnewlines",
        "name\twith\ttabs",
    ]
    
    # Valid names that should be accepted
    valid_names = [
        "valid_name",
        "valid-name-123",
        "ValidName123",
        "test_experiment_1",
        "MyExperiment-v2",
    ]
    
    print("\n✅ Testing VALID experiment names:")
    print("-" * 60)
    for name in valid_names:
        try:
            experiment = ExperimentalSystem(name, "Test hypothesis")
            result = habitat.spawn_experiment(experiment, {'resources': {}})
            print(f"  ✓ '{name}' - ACCEPTED (as expected)")
        except ValueError as e:
            print(f"  ✗ '{name}' - REJECTED (unexpected!): {e}")
            return False
    
    print("\n🚫 Testing MALICIOUS experiment names (should all be rejected):")
    print("-" * 60)
    rejected_count = 0
    for name in malicious_names:
        try:
            experiment = ExperimentalSystem(name, "Malicious hypothesis")
            result = habitat.spawn_experiment(experiment, {'resources': {}})
            print(f"  ✗ '{name}' - ACCEPTED (VULNERABILITY!)")
            return False
        except ValueError as e:
            print(f"  ✓ '{name}' - REJECTED (as expected)")
            rejected_count += 1
    
    # Cleanup
    habitat.cleanup()
    
    print("\n" + "=" * 60)
    print(f"✅ All {len(valid_names)} valid names were accepted")
    print(f"✅ All {rejected_count}/{len(malicious_names)} malicious names were rejected")
    print("✅ Path traversal vulnerability fix is working correctly!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_path_traversal_prevention()
    sys.exit(0 if success else 1)
