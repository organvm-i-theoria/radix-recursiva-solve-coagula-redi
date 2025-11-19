#!/usr/bin/env python3
"""
INTERACTIVE_HABITAT.py

Interactive shell for the Experimental Habitat system.
This provides a REPL-style interface for managing experiments within
a persistent habitat session.

Usage:
    python3 interactive_habitat.py
"""

import cmd
import json
import sys
from experimental_habitat_implementation import ExperimentalHabitat, ExperimentalSystem, RecursiveMythEngine


class InteractiveHabitat(cmd.Cmd):
    """Interactive shell for habitat management"""

    intro = '''
🧪 EXPERIMENTAL HABITAT - Interactive Shell
============================================
Type 'help' or '?' to list commands.
Type 'quit' or 'exit' to leave the shell.
'''
    prompt = '(habitat) '

    def __init__(self):
        super().__init__()
        self.habitats = {}
        self.current_habitat = None
        # Create default habitat
        self._create_default_habitat()

    def _create_default_habitat(self):
        """Create the default main habitat"""
        main_habitat = ExperimentalHabitat("main_lab", isolation_level=3)
        self.habitats["main"] = main_habitat
        self.current_habitat = "main"
        print(f"✅ Created default habitat: main_lab")

    def do_spawn(self, arg):
        """Spawn a new experiment
        Usage: spawn <name> [--type <type>] [--hypothesis <hypothesis>]
        Example: spawn test1 --hypothesis "Testing pattern recognition"
        """
        args = arg.split()
        if not args:
            print("❌ Error: Experiment name required")
            return

        name = args[0]
        exp_type = "recursive_myth"
        hypothesis = "Default experimental hypothesis"

        # Parse optional arguments
        i = 1
        while i < len(args):
            if args[i] == "--type" and i + 1 < len(args):
                exp_type = args[i + 1]
                i += 2
            elif args[i] == "--hypothesis" and i + 1 < len(args):
                # Join remaining args as hypothesis
                hypothesis = " ".join(args[i + 1:])
                break
            else:
                i += 1

        habitat = self.habitats[self.current_habitat]

        # Create experiment
        if exp_type == "recursive_myth":
            experiment = RecursiveMythEngine()
            experiment.name = name
            experiment.hypothesis = hypothesis
        else:
            experiment = ExperimentalSystem(name, hypothesis)

        # Spawn in habitat
        containment_rules = {
            'resources': {'cpu': '50%', 'memory': '512M'},
            'network_isolation': True,
            'time_limit': 1800,
            'recursive_depth_limit': 5
        }

        habitat.spawn_experiment(experiment, containment_rules)
        print(f"🧪 Spawned experiment '{name}' in habitat '{habitat.name}'")
        print(f"   Hypothesis: {hypothesis}")
        print(f"   Boundary: {experiment.boundary.get_full_path()}")

    def do_run(self, arg):
        """Run an experiment
        Usage: run <experiment_name>
        Example: run test1
        """
        if not arg:
            print("❌ Error: Experiment name required")
            return

        habitat = self.habitats[self.current_habitat]

        try:
            result = habitat.run_experiment(arg)
            print(f"✅ Experiment '{arg}' completed successfully")
            print("Result summary:")
            if isinstance(result, dict):
                for key, value in result.items():
                    if key != "nested":
                        print(f"   {key}: {value}")
        except Exception as e:
            print(f"❌ Experiment failed: {e}")

    def do_status(self, arg):
        """Get status of habitat or experiment
        Usage: status [experiment_name]
        Example: status
                 status test1
        """
        habitat = self.habitats[self.current_habitat]

        if arg:
            # Get experiment status
            if arg in habitat.active_experiments:
                exp_data = habitat.active_experiments[arg]
                experiment = exp_data['experiment']
                print(f"📊 Status for experiment '{arg}':")
                print(f"   Status: {experiment.status}")
                print(f"   Hypothesis: {experiment.hypothesis}")
                print(f"   Created: {experiment.created}")
                print(f"   Workspace: {exp_data.get('workspace')}")
            elif arg in habitat.graduated_patterns:
                print(f"🎓 Experiment '{arg}' has graduated to Code Forge")
            elif arg in habitat.failed_experiments:
                print(f"💀 Experiment '{arg}' has been composted")
            else:
                print(f"❓ Experiment '{arg}' not found")
        else:
            # Get habitat status
            status = habitat.get_habitat_status()
            print(f"🏠 Status for habitat '{self.current_habitat}':")
            print(json.dumps(status, indent=2))

    def do_graduate(self, arg):
        """Graduate an experiment to Code Forge
        Usage: graduate <experiment_name>
        Example: graduate test1
        """
        if not arg:
            print("❌ Error: Experiment name required")
            return

        habitat = self.habitats[self.current_habitat]

        try:
            forge_package = habitat.graduate_to_forge(arg)
            print(f"🎓 Experiment '{arg}' successfully graduated!")
            print("Forge package contents:")
            print(f"   Code patterns: {forge_package['code_patterns']}")
            print(f"   Symbolic mappings: {forge_package['symbolic_mappings']}")
            print(f"   Integration hooks: {forge_package['integration_hooks']}")
        except Exception as e:
            print(f"❌ Failed to graduate: {e}")

    def do_compost(self, arg):
        """Compost a failed experiment
        Usage: compost <experiment_name> <reason>
        Example: compost test1 "Resource limits exceeded"
        """
        args = arg.split(maxsplit=1)
        if len(args) < 2:
            print("❌ Error: Experiment name and reason required")
            return

        name, reason = args
        habitat = self.habitats[self.current_habitat]

        try:
            lessons = habitat.contain_failure(name, reason)
            print(f"♻️  Experiment '{name}' safely composted")
            print("Lessons learned:")
            for lesson_type, lesson_data in lessons.items():
                print(f"   {lesson_type}: {lesson_data}")
        except Exception as e:
            print(f"❌ Failed to compost: {e}")

    def do_nest(self, arg):
        """Create a nested habitat
        Usage: nest <parent_experiment> <child_name>
        Example: nest test1 sub_lab
        """
        args = arg.split()
        if len(args) < 2:
            print("❌ Error: Parent experiment and child name required")
            return

        parent_exp, child_name = args[0], args[1]
        parent_habitat = self.habitats[self.current_habitat]

        try:
            nested_habitat = parent_habitat.nest_habitat(parent_exp, child_name)
            habitat_key = f"{self.current_habitat}_{child_name}"
            self.habitats[habitat_key] = nested_habitat

            print(f"🪆 Created nested habitat '{child_name}'")
            print(f"   Nesting depth: {nested_habitat.nesting_depth}")
            print(f"   Isolation level: {nested_habitat.isolation_level}")
            print(f"   Access key: {habitat_key}")
        except Exception as e:
            print(f"❌ Failed to create nested habitat: {e}")

    def do_switch(self, arg):
        """Switch to a different habitat
        Usage: switch <habitat_key>
        Example: switch main
                 switch main_sub_lab
        """
        if not arg:
            print("❌ Error: Habitat key required")
            return

        if arg in self.habitats:
            self.current_habitat = arg
            print(f"✅ Switched to habitat: {arg}")
        else:
            print(f"❌ Habitat '{arg}' not found")
            print(f"Available habitats: {', '.join(self.habitats.keys())}")

    def do_list(self, arg):
        """List all habitats
        Usage: list
        """
        print("🏠 Active Habitats:")
        print("=" * 50)

        for key, habitat in self.habitats.items():
            status = habitat.get_habitat_status()
            current = " (current)" if key == self.current_habitat else ""
            print(f"📍 {key}{current}")
            print(f"   Name: {habitat.name}")
            print(f"   Isolation Level: {status['isolation_level']}")
            print(f"   Nesting Depth: {status['nesting_depth']}")
            print(f"   Active Experiments: {status['active_experiments']}")
            print(f"   Graduated Patterns: {status['graduated_patterns']}")
            print()

    def do_cleanup(self, arg):
        """Cleanup all habitats
        Usage: cleanup
        """
        print("🧹 Cleaning up all habitats...")

        for key, habitat in self.habitats.items():
            try:
                habitat.cleanup()
                print(f"✅ Cleaned up habitat '{key}'")
            except Exception as e:
                print(f"❌ Failed to cleanup habitat '{key}': {e}")

        print("🎉 Cleanup complete!")

    def do_quit(self, arg):
        """Exit the interactive shell
        Usage: quit
        """
        print("👋 Cleaning up and exiting...")
        for habitat in self.habitats.values():
            try:
                habitat.cleanup()
            except:
                pass
        return True

    def do_exit(self, arg):
        """Exit the interactive shell
        Usage: exit
        """
        return self.do_quit(arg)

    def do_EOF(self, arg):
        """Handle EOF (Ctrl+D)"""
        print()
        return self.do_quit(arg)


def main():
    """Run the interactive habitat shell"""
    try:
        InteractiveHabitat().cmdloop()
    except KeyboardInterrupt:
        print("\n👋 Interrupted. Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
