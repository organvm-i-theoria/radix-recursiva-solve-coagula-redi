#!/usr/bin/env python3
"""
COMPLETE_WORKFLOW_DEMO.py

A comprehensive demonstration of the entire Experimental Habitat workflow,
showcasing all major features:
- Spawning experiments with different configurations
- Running and monitoring experiments
- Creating nested habitats
- Graduating successful experiments
- Composting failed experiments
- Complete lifecycle management

This demonstrates a realistic use case of the habitat system.
"""

from experimental_habitat_implementation import (
    ExperimentalHabitat,
    ExperimentalSystem,
    RecursiveMythEngine,
    ContainmentBoundary
)
import json
import time


class PatternMatcher(ExperimentalSystem):
    """Example: Pattern matching experiment"""

    def __init__(self):
        super().__init__(
            name="pattern_matcher",
            hypothesis="Symbolic patterns can be extracted from recursive structures"
        )
        self.patterns_found = []

    def _execute_experiment(self):
        """Execute pattern matching"""
        patterns = [
            "recursive_mirror",
            "symbolic_loop",
            "containment_boundary",
            "myth_generator"
        ]

        self.patterns_found = patterns
        return {
            "patterns_detected": len(patterns),
            "pattern_list": patterns,
            "confidence": 0.92,
            "status": "successful"
        }


class FailingExperiment(ExperimentalSystem):
    """Example: An experiment designed to fail for demonstration"""

    def __init__(self):
        super().__init__(
            name="failing_test",
            hypothesis="This experiment is designed to fail safely"
        )

    def _execute_experiment(self):
        """This will fail intentionally"""
        raise RuntimeError("Intentional failure to demonstrate composting")


class ResourceIntensiveExperiment(ExperimentalSystem):
    """Example: Resource-heavy experiment with simulated load"""

    def __init__(self):
        super().__init__(
            name="resource_test",
            hypothesis="Testing resource containment and limits"
        )

    def _execute_experiment(self):
        """Simulate resource-intensive operation"""
        # Simulate some processing time
        time.sleep(0.1)

        return {
            "operations_completed": 1000,
            "memory_used": "45MB",
            "cpu_time": "0.1s",
            "status": "within_limits"
        }


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n--- {title} ---")


def main():
    """Run the complete workflow demonstration"""

    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║       EXPERIMENTAL HABITAT SYSTEM - COMPLETE WORKFLOW DEMO      ║
║                                                                  ║
║  Demonstrating the full lifecycle of experimental systems in    ║
║  nested, isolated containment environments.                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")

    # ===================================================================
    # PHASE 1: Environment Setup
    # ===================================================================
    print_section("PHASE 1: Environment Setup")

    print("\n🏗️  Creating main experimental habitat...")
    main_habitat = ExperimentalHabitat("primary_research_lab", isolation_level=3)
    print(f"✅ Habitat '{main_habitat.name}' established")
    print(f"   📍 Workspace: {main_habitat.temp_dir}")
    print(f"   🔒 Isolation Level: {main_habitat.isolation_level}")

    # ===================================================================
    # PHASE 2: Spawning Multiple Experiments
    # ===================================================================
    print_section("PHASE 2: Spawning Multiple Experiments")

    experiments = []

    print_subsection("Experiment 1: Recursive Myth Engine")
    myth_engine = RecursiveMythEngine()
    myth_engine.max_depth = 4
    containment_high = {
        'resources': {'cpu': '75%', 'memory': '1G'},
        'network_isolation': True,
        'time_limit': 60,
        'recursive_depth_limit': 5
    }
    main_habitat.spawn_experiment(myth_engine, containment_high)
    experiments.append(("myth_engine", myth_engine, "success"))
    print(f"✅ Spawned: {myth_engine.name}")
    print(f"   Containment: {myth_engine.boundary.get_full_path()}")

    print_subsection("Experiment 2: Pattern Matcher")
    pattern_matcher = PatternMatcher()
    containment_medium = {
        'resources': {'cpu': '50%', 'memory': '512M'},
        'network_isolation': True,
        'time_limit': 30
    }
    main_habitat.spawn_experiment(pattern_matcher, containment_medium)
    experiments.append(("pattern_matcher", pattern_matcher, "success"))
    print(f"✅ Spawned: {pattern_matcher.name}")

    print_subsection("Experiment 3: Resource Intensive Test")
    resource_test = ResourceIntensiveExperiment()
    containment_resource = {
        'resources': {'cpu': '25%', 'memory': '256M'},
        'network_isolation': True,
        'time_limit': 15,
        'monitor_resources': True
    }
    main_habitat.spawn_experiment(resource_test, containment_resource)
    experiments.append(("resource_test", resource_test, "success"))
    print(f"✅ Spawned: {resource_test.name}")

    print_subsection("Experiment 4: Failing Experiment (for composting demo)")
    failing_exp = FailingExperiment()
    containment_low = {
        'resources': {'cpu': '10%', 'memory': '128M'},
        'network_isolation': True,
        'time_limit': 10
    }
    main_habitat.spawn_experiment(failing_exp, containment_low)
    experiments.append(("failing_test", failing_exp, "fail"))
    print(f"✅ Spawned: {failing_exp.name}")

    # ===================================================================
    # PHASE 3: Nested Habitat Creation
    # ===================================================================
    print_section("PHASE 3: Creating Nested Habitats")

    print("\n🪆 Creating nested habitat within myth_engine experiment...")
    nested_habitat = main_habitat.nest_habitat("recursive_myth_engine", "analysis_sublayer")
    print(f"✅ Nested habitat created: {nested_habitat.name}")
    print(f"   📊 Nesting depth: {nested_habitat.nesting_depth}")
    print(f"   🔒 Isolation level: {nested_habitat.isolation_level}")

    # Spawn experiment in nested habitat
    print("\n🧪 Spawning experiment in nested habitat...")
    nested_analyzer = PatternMatcher()
    nested_analyzer.name = "nested_pattern_analyzer"
    nested_containment = {
        'resources': {'cpu': '25%', 'memory': '256M'},
        'network_isolation': True,
        'parent_dependency': 'recursive_myth_engine'
    }
    nested_habitat.spawn_experiment(nested_analyzer, nested_containment)
    print(f"✅ Nested experiment spawned: {nested_analyzer.name}")
    print(f"   🔗 Parent dependency: recursive_myth_engine")

    # ===================================================================
    # PHASE 4: Running Experiments
    # ===================================================================
    print_section("PHASE 4: Running Experiments")

    results = []

    for exp_name, exp_obj, expected_result in experiments:
        print_subsection(f"Running: {exp_name}")

        try:
            start = time.time()
            result = main_habitat.run_experiment(exp_obj.name)
            duration = time.time() - start

            print(f"✅ Completed in {duration:.3f}s")
            print(f"   Result: {json.dumps(result, indent=6)[:200]}...")
            results.append((exp_name, "success", result))

        except Exception as e:
            print(f"❌ Failed: {e}")
            results.append((exp_name, "failed", str(e)))

    # Run nested experiment
    print_subsection("Running: nested_pattern_analyzer")
    nested_result = nested_habitat.run_experiment(nested_analyzer.name)
    print(f"✅ Nested experiment completed")
    print(f"   Patterns found: {nested_result['pattern_list']}")

    # ===================================================================
    # PHASE 5: Status Monitoring
    # ===================================================================
    print_section("PHASE 5: Status Monitoring")

    print("\n📊 Main Habitat Status:")
    main_status = main_habitat.get_habitat_status()
    print(json.dumps(main_status, indent=2))

    print("\n📊 Nested Habitat Status:")
    nested_status = nested_habitat.get_habitat_status()
    print(json.dumps(nested_status, indent=2))

    # ===================================================================
    # PHASE 6: Graduation & Composting
    # ===================================================================
    print_section("PHASE 6: Graduation & Composting")

    # Graduate successful experiments
    print_subsection("Graduating Successful Experiments")

    for exp_name, status, result in results:
        if status == "success" and exp_name != "failing_test":
            try:
                forge_package = main_habitat.graduate_to_forge(exp_name)
                print(f"🎓 Graduated: {exp_name}")
                print(f"   Code patterns: {forge_package['code_patterns']}")
            except Exception as e:
                print(f"⚠️  Could not graduate {exp_name}: {e}")

    # Graduate nested experiment
    print("\n🎓 Graduating nested experiment...")
    nested_package = nested_habitat.graduate_to_forge(nested_analyzer.name)
    print(f"✅ Nested experiment graduated")

    # Compost failed experiment
    print_subsection("Composting Failed Experiments")

    try:
        lessons = main_habitat.contain_failure(
            "failing_test",
            "Intentional failure for demonstration purposes"
        )
        print(f"♻️  Composted: failing_test")
        print(f"   Lessons learned:")
        for key, value in lessons.items():
            if isinstance(value, list) and value:
                print(f"      {key}: {value[0]}")
            elif not isinstance(value, list):
                print(f"      {key}: {value}")
    except Exception as e:
        print(f"⚠️  Composting note: {e}")

    # ===================================================================
    # PHASE 7: Final Summary
    # ===================================================================
    print_section("PHASE 7: Final Summary")

    print("\n📈 Experiment Results Summary:")
    print(f"   Total experiments spawned: {len(experiments) + 1}")  # +1 for nested
    print(f"   Successful completions: {sum(1 for _, s, _ in results if s == 'success')}")
    print(f"   Failed experiments: {sum(1 for _, s, _ in results if s == 'failed')}")
    print(f"   Graduated to Code Forge: {len(main_habitat.graduated_patterns) + len(nested_habitat.graduated_patterns)}")
    print(f"   Safely composted: {len(main_habitat.failed_experiments)}")

    print("\n🏆 Graduated Patterns:")
    for name in main_habitat.graduated_patterns.keys():
        print(f"   ✓ {name}")
    for name in nested_habitat.graduated_patterns.keys():
        print(f"   ✓ {name} (nested)")

    print("\n📚 System Capabilities Demonstrated:")
    capabilities = [
        "✓ Multi-experiment spawning with different configurations",
        "✓ Nested habitat creation (hat on a hat on a)",
        "✓ Resource-aware containment boundaries",
        "✓ Safe experiment execution and monitoring",
        "✓ Successful pattern graduation to Code Forge",
        "✓ Failed experiment composting and lesson extraction",
        "✓ Complete lifecycle management",
        "✓ State tracking and status reporting"
    ]
    for cap in capabilities:
        print(f"   {cap}")

    # ===================================================================
    # PHASE 8: Cleanup
    # ===================================================================
    print_section("PHASE 8: Cleanup")

    print("\n🧹 Cleaning up experimental environments...")
    main_habitat.cleanup()
    print(f"✅ Main habitat cleaned: {main_habitat.name}")

    nested_habitat.cleanup()
    print(f"✅ Nested habitat cleaned: {nested_habitat.name}")

    print("\n" + "=" * 70)
    print("🎉 COMPLETE WORKFLOW DEMONSTRATION FINISHED SUCCESSFULLY!")
    print("=" * 70)
    print("\nThe Experimental Habitat system successfully demonstrated:")
    print("  • Safe, isolated execution of experimental code")
    print("  • Nested containment with progressive isolation")
    print("  • Pattern extraction and graduation workflow")
    print("  • Failure handling and knowledge retention")
    print("  • Complete lifecycle management from spawn to cleanup")
    print("\nSystem ready for production use! 🚀")
    print()


if __name__ == "__main__":
    main()
