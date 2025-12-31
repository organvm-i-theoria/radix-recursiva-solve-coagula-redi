#!/usr/bin/env python3
"""
TEST_HABITAT_SYSTEM.py

Unit tests for the Experimental Habitat System.
Tests core functionality including:
- Habitat creation and initialization
- Experiment spawning and execution
- Nested habitat creation
- Graduation and composting workflows
- Containment boundaries
- Error handling

Run with: python3 test_habitat_system.py
Or with pytest: pytest test_habitat_system.py -v
"""

import unittest
import tempfile
import os
import shutil
from experimental_habitat_implementation import (
    ExperimentalHabitat,
    ExperimentalSystem,
    RecursiveMythEngine,
    ContainmentBoundary
)


class TestContainmentBoundary(unittest.TestCase):
    """Test ContainmentBoundary class"""

    def test_boundary_creation(self):
        """Test creating a containment boundary"""
        boundary = ContainmentBoundary("test_boundary", level=3)
        self.assertEqual(boundary.name, "test_boundary")
        self.assertEqual(boundary.level, 3)
        self.assertIsNone(boundary.parent)
        self.assertTrue(boundary.active)

    def test_boundary_nesting(self):
        """Test nested boundary creation"""
        parent = ContainmentBoundary("parent", level=1)
        child = ContainmentBoundary("child", level=2, parent=parent)

        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.children)

    def test_boundary_path(self):
        """Test full path generation"""
        parent = ContainmentBoundary("parent", level=1)
        child = ContainmentBoundary("child", level=2, parent=parent)
        grandchild = ContainmentBoundary("grandchild", level=3, parent=child)

        self.assertEqual(parent.get_full_path(), "parent")
        self.assertEqual(child.get_full_path(), "parent/child")
        self.assertEqual(grandchild.get_full_path(), "parent/child/grandchild")

    def test_breach_detection(self):
        """Test breach detection (placeholder)"""
        boundary = ContainmentBoundary("test", level=1)
        self.assertFalse(boundary.breach_detected())


class TestExperimentalSystem(unittest.TestCase):
    """Test ExperimentalSystem class"""

    def test_experiment_creation(self):
        """Test creating an experimental system"""
        exp = ExperimentalSystem("test_exp", "Test hypothesis")
        self.assertEqual(exp.name, "test_exp")
        self.assertEqual(exp.hypothesis, "Test hypothesis")
        self.assertEqual(exp.status, "spawning")
        self.assertEqual(len(exp.failures), 0)

    def test_experiment_run_success(self):
        """Test running a successful experiment"""
        exp = ExperimentalSystem("test_exp", "Test hypothesis")
        result = exp.run()

        self.assertEqual(exp.status, "completed")
        self.assertTrue(result["success"])
        self.assertEqual(len(exp.failures), 0)

    def test_experiment_run_failure(self):
        """Test experiment failure handling"""
        class FailingExperiment(ExperimentalSystem):
            def _execute_experiment(self):
                raise ValueError("Test failure")

        exp = FailingExperiment("failing_exp", "Will fail")

        with self.assertRaises(ValueError):
            exp.run()

        self.assertEqual(exp.status, "failed")
        self.assertEqual(len(exp.failures), 1)
        self.assertIn("Test failure", exp.failures[0]["error"])


class TestRecursiveMythEngine(unittest.TestCase):
    """Test RecursiveMythEngine class"""

    def test_myth_engine_creation(self):
        """Test creating myth engine"""
        engine = RecursiveMythEngine()
        self.assertEqual(engine.name, "recursive_myth_engine")
        self.assertEqual(engine.depth, 0)
        self.assertEqual(engine.max_depth, 3)

    def test_myth_generation(self):
        """Test recursive myth generation"""
        engine = RecursiveMythEngine()
        engine.max_depth = 2
        result = engine.run()

        self.assertEqual(engine.status, "completed")
        self.assertIn("myth", result)
        self.assertEqual(result["depth"], 2)
        self.assertIn("nested", result)

    def test_myth_depth_limit(self):
        """Test recursion depth limiting"""
        engine = RecursiveMythEngine()
        engine.max_depth = 5
        result = engine.run()

        self.assertEqual(result["depth"], 5)


class TestExperimentalHabitat(unittest.TestCase):
    """Test ExperimentalHabitat class"""

    def setUp(self):
        """Set up test habitat"""
        self.habitat = ExperimentalHabitat("test_lab", isolation_level=2)

    def tearDown(self):
        """Clean up test habitat"""
        self.habitat.cleanup()

    def test_habitat_creation(self):
        """Test habitat initialization"""
        self.assertEqual(self.habitat.name, "test_lab")
        self.assertEqual(self.habitat.isolation_level, 2)
        self.assertEqual(self.habitat.nesting_depth, 0)
        self.assertTrue(os.path.exists(self.habitat.temp_dir))

    def test_spawn_experiment(self):
        """Test spawning an experiment"""
        exp = ExperimentalSystem("test_exp", "Test hypothesis")
        containment = {
            'resources': {'cpu': '50%', 'memory': '512M'},
            'network_isolation': True
        }

        exp_data = self.habitat.spawn_experiment(exp, containment)

        self.assertIn("test_exp", self.habitat.active_experiments)
        self.assertEqual(exp_data["status"], "spawned")
        self.assertIsNotNone(exp.boundary)
        self.assertTrue(os.path.exists(exp_data["workspace"]))

    def test_run_experiment(self):
        """Test running a spawned experiment"""
        exp = ExperimentalSystem("test_exp", "Test hypothesis")
        containment = {'resources': {}}

        self.habitat.spawn_experiment(exp, containment)
        result = self.habitat.run_experiment("test_exp")

        self.assertTrue(result["success"])
        exp_data = self.habitat.active_experiments["test_exp"]
        self.assertEqual(exp_data["status"], "completed")

    def test_run_nonexistent_experiment(self):
        """Test running an experiment that doesn't exist"""
        with self.assertRaises(ValueError):
            self.habitat.run_experiment("nonexistent")

    def test_nest_habitat(self):
        """Test creating nested habitat"""
        # First spawn parent experiment
        parent_exp = ExperimentalSystem("parent_exp", "Parent")
        self.habitat.spawn_experiment(parent_exp, {'resources': {}})

        # Create nested habitat
        nested = self.habitat.nest_habitat("parent_exp", "sub_lab")

        self.assertEqual(nested.nesting_depth, 1)
        self.assertEqual(nested.isolation_level, 3)  # +1 from parent
        self.assertIn("nested_sub_lab", nested.name)

    def test_graduate_experiment(self):
        """Test graduating successful experiment"""
        exp = ExperimentalSystem("test_exp", "Test hypothesis")
        self.habitat.spawn_experiment(exp, {'resources': {}})
        self.habitat.run_experiment("test_exp")

        forge_package = self.habitat.graduate_to_forge("test_exp")

        self.assertIn("test_exp", self.habitat.graduated_patterns)
        self.assertNotIn("test_exp", self.habitat.active_experiments)
        self.assertIn("code_patterns", forge_package)
        self.assertIn("symbolic_mappings", forge_package)
        self.assertIn("integration_hooks", forge_package)

    def test_contain_failure(self):
        """Test composting failed experiment"""
        class FailingExp(ExperimentalSystem):
            def _execute_experiment(self):
                raise RuntimeError("Intentional failure")

        exp = FailingExp("failing_exp", "Will fail")
        self.habitat.spawn_experiment(exp, {'resources': {}})

        try:
            self.habitat.run_experiment("failing_exp")
        except:
            pass

        lessons = self.habitat.contain_failure("failing_exp", "Test failure")

        self.assertIn("failing_exp", self.habitat.failed_experiments)
        self.assertNotIn("failing_exp", self.habitat.active_experiments)
        self.assertIn("what_failed", lessons)
        self.assertIn("wisdom_gained", lessons)

    def test_habitat_status(self):
        """Test getting habitat status"""
        status = self.habitat.get_habitat_status()

        self.assertEqual(status["name"], "test_lab")
        self.assertEqual(status["isolation_level"], 2)
        self.assertEqual(status["nesting_depth"], 0)
        self.assertEqual(status["active_experiments"], 0)
        self.assertIn("workspace", status)

    def test_habitat_cleanup(self):
        """Test habitat cleanup"""
        temp_dir = self.habitat.temp_dir
        self.assertTrue(os.path.exists(temp_dir))

        self.habitat.cleanup()
        self.assertFalse(os.path.exists(temp_dir))


class TestIntegrationWorkflow(unittest.TestCase):
    """Integration tests for complete workflows"""

    def test_full_lifecycle(self):
        """Test complete experiment lifecycle"""
        # Create habitat
        habitat = ExperimentalHabitat("integration_lab", isolation_level=2)

        try:
            # Spawn experiment
            exp = RecursiveMythEngine()
            exp.max_depth = 2
            habitat.spawn_experiment(exp, {'resources': {}})

            # Run experiment
            result = habitat.run_experiment(exp.name)
            self.assertIn("myth", result)

            # Graduate
            package = habitat.graduate_to_forge(exp.name)
            self.assertIsNotNone(package)

            # Verify final state
            status = habitat.get_habitat_status()
            self.assertEqual(status["active_experiments"], 0)
            self.assertEqual(status["graduated_patterns"], 1)

        finally:
            habitat.cleanup()

    def test_nested_workflow(self):
        """Test nested habitat workflow"""
        main_hab = ExperimentalHabitat("main_lab", isolation_level=1)

        try:
            # Spawn parent experiment
            parent = ExperimentalSystem("parent", "Parent experiment")
            main_hab.spawn_experiment(parent, {'resources': {}})

            # Create nested habitat
            nested_hab = main_hab.nest_habitat("parent", "nested_lab")

            # Spawn nested experiment
            child = ExperimentalSystem("child", "Child experiment")
            nested_hab.spawn_experiment(child, {'resources': {}})

            # Run both
            main_hab.run_experiment("parent")
            nested_hab.run_experiment("child")

            # Graduate both
            main_hab.graduate_to_forge("parent")
            nested_hab.graduate_to_forge("child")

            # Verify nesting
            self.assertEqual(nested_hab.nesting_depth, 1)
            self.assertEqual(nested_hab.isolation_level, 2)

            nested_hab.cleanup()

        finally:
            main_hab.cleanup()


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestContainmentBoundary))
    suite.addTests(loader.loadTestsFromTestCase(TestExperimentalSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestRecursiveMythEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestExperimentalHabitat))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWorkflow))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    import sys
    sys.exit(run_tests())
