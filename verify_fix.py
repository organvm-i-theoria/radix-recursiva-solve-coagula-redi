#!/usr/bin/env python3
"""
VERIFY_FIX.py

Verification script for the path traversal security fix in ExperimentalHabitat.
This script tests various path traversal attack vectors to ensure they are properly blocked.
"""

import os
import sys
import tempfile
from experimental_habitat_implementation import ExperimentalHabitat, ExperimentalSystem


class TestExperiment(ExperimentalSystem):
    """Simple test experiment for verification"""
    
    def __init__(self, name: str):
        super().__init__(name, "Test hypothesis")
    
    def _execute_experiment(self):
        return {"status": "completed", "message": "Test experiment ran successfully"}


def test_path_traversal_prevention():
    """Test that path traversal attacks are properly prevented"""
    
    print("🛡️ VERIFYING PATH TRAVERSAL SECURITY FIX")
    print("=" * 70)
    print()
    
    # Test cases: (name, should_be_blocked, description)
    test_cases = [
        # Valid experiment names (should NOT be blocked)
        ("safe_experiment", False, "Normal experiment name"),
        ("exp_123", False, "Alphanumeric with underscore"),
        ("nested/safe/path", False, "Nested path without traversal"),
        ("my-experiment", False, "Hyphenated name"),
        ("test.experiment", False, "Name with dot (not parent ref)"),
        
        # Path traversal attempts (SHOULD be blocked)
        ("../../../etc/passwd", True, "Unix-style upward traversal"),
        ("..\\..\\..\\windows\\system32", True, "Windows-style upward traversal"),
        ("../escape", True, "Single parent directory escape"),
        ("experiment/../../../etc", True, "Traversal in middle of path"),
        ("../../..", True, "Multiple parent references"),
        ("..\\..\\escape", True, "Mixed Windows traversal"),
        ("/etc/passwd", True, "Absolute Unix path"),
        ("C:\\Windows\\System32", True, "Absolute Windows path"),
        ("/absolute/path", True, "Absolute path attempt"),
        ("experiment/../../escape", True, "Nested with parent escape"),
    ]
    
    total_tests = len(test_cases)
    passed_tests = 0
    failed_tests = 0
    
    for experiment_name, should_be_blocked, description in test_cases:
        print(f"📝 Testing: {description}")
        print(f"   Input: '{experiment_name}'")
        
        # Create temporary habitat for testing
        habitat = ExperimentalHabitat(f"test_habitat_{passed_tests + failed_tests}", isolation_level=3)
        
        try:
            # Try to spawn experiment with potentially malicious name
            test_exp = TestExperiment(experiment_name)
            containment_rules = {
                'resources': {'cpu': '10%', 'memory': '64M'},
                'network_isolation': True
            }
            
            exp_data = habitat.spawn_experiment(test_exp, containment_rules)
            
            # If we get here, the experiment was allowed
            if should_be_blocked:
                print(f"   ❌ FAIL: Malicious path was NOT blocked!")
                print(f"   Created at: {exp_data['workspace']}")
                failed_tests += 1
            else:
                print(f"   ✅ PASS: Valid experiment name accepted")
                passed_tests += 1
                
        except ValueError as e:
            # ValueError indicates the security check caught the attempt
            if should_be_blocked:
                print(f"   ✅ PASS: Malicious path blocked correctly")
                print(f"   Error: {str(e)}")
                passed_tests += 1
            else:
                print(f"   ❌ FAIL: Valid experiment name was incorrectly blocked!")
                print(f"   Error: {str(e)}")
                failed_tests += 1
                
        except Exception as e:
            print(f"   ⚠️  UNEXPECTED ERROR: {type(e).__name__}: {e}")
            failed_tests += 1
            
        finally:
            # Cleanup
            try:
                habitat.cleanup()
            except:
                pass
        
        print()
    
    # Print summary
    print("=" * 70)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print()
    
    if failed_tests == 0:
        print("🎉 SUCCESS: All security tests passed!")
        print("✅ Path traversal vulnerability is properly mitigated.")
        return 0
    else:
        print("⚠️  FAILURE: Some security tests failed!")
        print("❌ Path traversal vulnerability may still exist.")
        return 1


def test_workspace_isolation():
    """Test that experiment workspaces are properly isolated"""
    
    print("🔒 VERIFYING WORKSPACE ISOLATION")
    print("=" * 70)
    print()
    
    habitat = ExperimentalHabitat("isolation_test", isolation_level=3)
    
    try:
        # Create two experiments
        exp1 = TestExperiment("experiment_1")
        exp2 = TestExperiment("experiment_2")
        
        containment = {'resources': {'cpu': '10%', 'memory': '64M'}}
        
        exp1_data = habitat.spawn_experiment(exp1, containment)
        exp2_data = habitat.spawn_experiment(exp2, containment)
        
        workspace1 = exp1_data['workspace']
        workspace2 = exp2_data['workspace']
        
        print(f"✅ Experiment 1 workspace: {workspace1}")
        print(f"✅ Experiment 2 workspace: {workspace2}")
        print()
        
        # Verify workspaces are different
        if workspace1 != workspace2:
            print("✅ PASS: Experiments have separate workspaces")
        else:
            print("❌ FAIL: Experiments share the same workspace")
            return 1
        
        # Verify both are within habitat temp directory
        if workspace1.startswith(habitat.temp_dir) and workspace2.startswith(habitat.temp_dir):
            print("✅ PASS: All workspaces are within habitat boundary")
        else:
            print("❌ FAIL: Some workspaces are outside habitat boundary")
            return 1
        
        # Verify workspaces exist
        if os.path.exists(workspace1) and os.path.exists(workspace2):
            print("✅ PASS: All workspaces exist on filesystem")
        else:
            print("❌ FAIL: Some workspaces don't exist")
            return 1
        
        print()
        print("🎉 SUCCESS: Workspace isolation verified!")
        return 0
        
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {e}")
        return 1
        
    finally:
        habitat.cleanup()


def main():
    """Run all verification tests"""
    
    print("🔐 EXPERIMENTAL HABITAT SECURITY VERIFICATION")
    print("=" * 70)
    print("Verifying path traversal fix in spawn_experiment method")
    print()
    
    try:
        # Run path traversal tests
        result1 = test_path_traversal_prevention()
        print()
        
        # Run workspace isolation tests
        result2 = test_workspace_isolation()
        print()
        
        # Overall result
        if result1 == 0 and result2 == 0:
            print("=" * 70)
            print("🎉 ALL VERIFICATION TESTS PASSED!")
            print("=" * 70)
            print("✅ The path traversal vulnerability has been successfully fixed.")
            print("✅ Workspace isolation is properly implemented.")
            print("✅ ExperimentalHabitat is secure for production use.")
            return 0
        else:
            print("=" * 70)
            print("⚠️  SOME VERIFICATION TESTS FAILED!")
            print("=" * 70)
            print("❌ Security issues remain. Do not use in production.")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Verification interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Verification failed with unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
