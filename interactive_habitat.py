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
from experimental_habitat_implementation import (
    ExperimentalHabitat,
    ExperimentalSystem,
    RecursiveMythEngine,
)
import habitat_ux

# Use shared colors
Colors = habitat_ux.Colors

_LABEL_ISOLATION_LEVEL = "Isolation Level"
_LABEL_NESTING_DEPTH = "Nesting Depth"


class InteractiveHabitat(cmd.Cmd):
    """Interactive shell for habitat management"""

    intro = ""  # Will be set in preloop to allow dynamic coloring
    prompt = f"{Colors.BOLD}(habitat){Colors.RESET} "

    def __init__(self):
        super().__init__()
        self.habitats = {}
        self.current_habitat = None
        # Create default habitat
        self._create_default_habitat()

    def preloop(self):
        """Print the header before the loop starts"""
        habitat_ux.print_header("EXPERIMENTAL HABITAT", "Interactive Shell")
        print(
            f"Type '{Colors.CYAN}help{Colors.RESET}' or '{Colors.CYAN}?{Colors.RESET}' to list commands."
        )
        print(
            f"Type '{Colors.CYAN}quit{Colors.RESET}' or '{Colors.CYAN}exit{Colors.RESET}' to leave the shell.\n"
        )

    def _create_default_habitat(self):
        """Create the default main habitat"""
        main_habitat = ExperimentalHabitat("main_lab", isolation_level=3)
        self.habitats["main"] = main_habitat
        self.current_habitat = "main"
        # We don't print here to avoid cluttering startup

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
        safe_name = habitat_ux.sanitize_for_terminal(name)
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
                hypothesis = " ".join(args[i + 1 :])
                break
            else:
                i += 1

        safe_hypothesis = habitat_ux.sanitize_for_terminal(hypothesis)

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
            "resources": {"cpu": "50%", "memory": "512M"},
            "network_isolation": True,
            "time_limit": 1800,
            "recursive_depth_limit": 5,
        }

        habitat.spawn_experiment(experiment, containment_rules)
        habitat_ux.print_card(
            f"Spawned Experiment: {safe_name}",
            {
                "Habitat": habitat.name,
                "Hypothesis": safe_hypothesis,
                "Boundary": experiment.boundary.get_full_path(),
            },
            icon="🧪",
        )
        print(
            f"{Colors.GREEN}🧪 Spawned experiment '{Colors.BOLD}{safe_name}{Colors.RESET}{Colors.GREEN}' in habitat '{habitat.name}'{Colors.RESET}"
        )

    def do_run(self, arg):
        """Run an experiment
        Usage: run <experiment_name>
        Example: run test1
        """
        if not arg:
            print(f"{Colors.RED}❌ Error: Experiment name required{Colors.RESET}")
            return

        safe_arg = habitat_ux.sanitize_for_terminal(arg)

        habitat = self.habitats[self.current_habitat]

        try:
            result = habitat.run_experiment(arg)
            print(
                f"{Colors.GREEN}✅ Experiment '{safe_arg}' completed successfully{Colors.RESET}"
            )

            display_result = {}
            if isinstance(result, dict):
                for key, value in result.items():
                    if key != "nested":
                        display_result[key] = value
            else:
                display_result["Result"] = result

            habitat_ux.print_card(f"Result: {safe_arg}", display_result, icon="✅")

        except Exception as e:
            safe_err = habitat_ux.sanitize_for_terminal(e)
            print(f"{Colors.RED}❌ Experiment failed: {safe_err}{Colors.RESET}")

    def do_status(self, arg):
        """Get status of habitat or experiment
        Usage: status [experiment_name]
        Example: status
                 status test1
        """
        habitat = self.habitats[self.current_habitat]

        if arg:
            safe_arg = habitat_ux.sanitize_for_terminal(arg)
            # Get experiment status
            if arg in habitat.active_experiments:
                exp_data = habitat.active_experiments[arg]
                experiment = exp_data["experiment"]

                habitat_ux.print_card(
                    f"Experiment: {safe_arg}",
                    {
                        "Status": experiment.status,
                        "Hypothesis": experiment.hypothesis,
                        "Created": experiment.created,
                        "Workspace": exp_data.get("workspace"),
                    },
                    icon="📊",
                )
            elif arg in habitat.graduated_patterns:
                print(
                    f"{Colors.GREEN}🎓 Experiment '{safe_arg}' has graduated to Code Forge{Colors.RESET}"
                )
            elif arg in habitat.failed_experiments:
                print(
                    f"{Colors.RED}💀 Experiment '{safe_arg}' has been composted{Colors.RESET}"
                )
            else:
                print(
                    f"{Colors.YELLOW}❓ Experiment '{safe_arg}' not found{Colors.RESET}"
                )
        else:
            # Get habitat status
            status = habitat.get_habitat_status()
            display_status = {
                "Habitat Name": habitat.name,
                _LABEL_ISOLATION_LEVEL: status["isolation_level"],
                _LABEL_NESTING_DEPTH: status["nesting_depth"],
                "Active Experiments": status["active_experiments"],
                "Graduated Patterns": status["graduated_patterns"],
                "Failed Experiments": status["failed_experiments"],
                "Workspace": status["workspace"],
            }
            habitat_ux.print_card(
                f"Habitat: {self.current_habitat}", display_status, icon="🏠"
            )

    def do_graduate(self, arg):
        """Graduate an experiment to Code Forge
        Usage: graduate <experiment_name>
        Example: graduate test1
        """
        if not arg:
            print(f"{Colors.RED}❌ Error: Experiment name required{Colors.RESET}")
            return

        safe_arg = habitat_ux.sanitize_for_terminal(arg)

        habitat = self.habitats[self.current_habitat]

        try:
            forge_package = habitat.graduate_to_forge(arg)
            print(
                f"{Colors.GREEN}🎓 Experiment '{safe_arg}' successfully graduated!{Colors.RESET}"
            )
            habitat_ux.print_card(
                f"Graduated: {safe_arg}",
                {
                    "Code patterns": forge_package["code_patterns"],
                    "Symbolic mappings": forge_package["symbolic_mappings"],
                    "Integration hooks": forge_package["integration_hooks"],
                },
                icon="🎓",
            )
        except Exception as e:
            safe_err = habitat_ux.sanitize_for_terminal(e)
            print(f"{Colors.RED}❌ Failed to graduate: {safe_err}{Colors.RESET}")

    def do_compost(self, arg):
        """Compost a failed experiment
        Usage: compost <experiment_name> <reason>
        Example: compost test1 "Resource limits exceeded"
        """
        args = arg.split(maxsplit=1)
        if len(args) < 2:
            print(
                f"{Colors.RED}❌ Error: Experiment name and reason required{Colors.RESET}"
            )
            return

        name, reason = args
        safe_name = habitat_ux.sanitize_for_terminal(name)
        habitat = self.habitats[self.current_habitat]

        try:
            lessons = habitat.contain_failure(name, reason)
            print(
                f"{Colors.YELLOW}♻️  Experiment '{safe_name}' safely composted{Colors.RESET}"
            )
            habitat_ux.print_card(f"Composted: {safe_name}", lessons, icon="♻️ ")
        except Exception as e:
            safe_err = habitat_ux.sanitize_for_terminal(e)
            print(f"{Colors.RED}❌ Failed to compost: {safe_err}{Colors.RESET}")

    def do_nest(self, arg):
        """Create a nested habitat
        Usage: nest <parent_experiment> <child_name>
        Example: nest test1 sub_lab
        """
        args = arg.split()
        if len(args) < 2:
            print(
                f"{Colors.RED}❌ Error: Parent experiment and child name required{Colors.RESET}"
            )
            return

        parent_exp, child_name = args[0], args[1]
        safe_parent_exp = habitat_ux.sanitize_for_terminal(parent_exp)
        safe_child_name = habitat_ux.sanitize_for_terminal(child_name)
        parent_habitat = self.habitats[self.current_habitat]

        try:
            nested_habitat = parent_habitat.nest_habitat(parent_exp, child_name)
            habitat_key = f"{self.current_habitat}_{child_name}"
            self.habitats[habitat_key] = nested_habitat

            print(
                f"{Colors.GREEN}🪆 Created nested habitat '{safe_child_name}'{Colors.RESET}"
            )
            habitat_ux.print_card(
                f"Nested Habitat: {safe_child_name}",
                {
                    "Parent Experiment": safe_parent_exp,
                    _LABEL_NESTING_DEPTH: nested_habitat.nesting_depth,
                    _LABEL_ISOLATION_LEVEL: nested_habitat.isolation_level,
                    "Access Key": habitat_key,
                },
                icon="🪆",
            )
        except Exception as e:
            safe_err = habitat_ux.sanitize_for_terminal(e)
            print(
                f"{Colors.RED}❌ Failed to create nested habitat: {safe_err}{Colors.RESET}"
            )

    def do_switch(self, arg):
        """Switch to a different habitat
        Usage: switch <habitat_key>
        Example: switch main
                 switch main_sub_lab
        """
        if not arg:
            print(f"{Colors.RED}❌ Error: Habitat key required{Colors.RESET}")
            return

        safe_arg = habitat_ux.sanitize_for_terminal(arg)

        if arg in self.habitats:
            self.current_habitat = arg
            print(f"{Colors.GREEN}✅ Switched to habitat: {safe_arg}{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Habitat '{safe_arg}' not found{Colors.RESET}")
            print(f"Available habitats: {', '.join(self.habitats.keys())}")

    def do_list(self, _arg):
        """List all habitats
        Usage: list
        """
        habitat_ux.print_header("Active Habitats")

        for key, habitat in self.habitats.items():
            status = habitat.get_habitat_status()
            current = " (current)" if key == self.current_habitat else ""

            display_status = {
                "Key": f"{key}{current}",
                "Name": habitat.name,
                _LABEL_ISOLATION_LEVEL: status["isolation_level"],
                _LABEL_NESTING_DEPTH: status["nesting_depth"],
                "Active Experiments": status["active_experiments"],
                "Graduated Patterns": status["graduated_patterns"],
            }
            habitat_ux.print_card(f"Habitat: {key}", display_status, icon="📍")

    def do_cleanup(self, _arg):
        """Cleanup all habitats
        Usage: cleanup
        """
        print(f"{Colors.BLUE}🧹 Cleaning up all habitats...{Colors.RESET}")

        for key, habitat in self.habitats.items():
            try:
                habitat.cleanup()
                print(f"{Colors.GREEN}✅ Cleaned up habitat '{key}'{Colors.RESET}")
            except Exception as e:
                print(
                    f"{Colors.RED}❌ Failed to cleanup habitat '{key}': {e}{Colors.RESET}"
                )

        print(f"{Colors.GREEN}🎉 Cleanup complete!{Colors.RESET}")

    def do_quit(self, _arg):
        """Exit the interactive shell
        Usage: quit
        """
        print(f"{Colors.BLUE}👋 Cleaning up and exiting...{Colors.RESET}")
        for habitat in self.habitats.values():
            try:
                habitat.cleanup()
            except Exception as e:
                # Ignore cleanup errors during exit, but log them for visibility
                print(
                    f"{Colors.RED}❌ Error during cleanup of habitat '{habitat.name}': {e}{Colors.RESET}"
                )
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
