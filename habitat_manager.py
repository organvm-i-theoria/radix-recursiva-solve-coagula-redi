#!/usr/bin/env python3
"""
HABITAT_MANAGER.py

Management interface for the Experimental Habitat system.
This script provides a command-line interface for spawning, managing,
and monitoring experimental systems within nested containment environments.

Usage:
    python3 habitat_manager.py spawn <experiment_name> --hypothesis "test hypothesis"
    python3 habitat_manager.py run <experiment_name>
    python3 habitat_manager.py status [experiment_name]
    python3 habitat_manager.py graduate <experiment_name>
    python3 habitat_manager.py compost <experiment_name> --reason "failure reason"
    python3 habitat_manager.py nest <parent_exp> <child_name>
    python3 habitat_manager.py list-habitats
    python3 habitat_manager.py cleanup
"""

import argparse
import json
import os
import sys
from typing import Any
import logging
from datetime import datetime
from experimental_habitat_implementation import ExperimentalHabitat, ExperimentalSystem, RecursiveMythEngine
import habitat_ux

# Configure logging to suppress INFO messages so they don't clutter CLI output
logging.getLogger().setLevel(logging.ERROR)

# Import Colors from habitat_ux to use shared definitions
Colors = habitat_ux.Colors

class HabitatManager:
    """Manager for experimental habitat operations"""
    
    def __init__(self, config_file: str = "habitat_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.habitats = {}
        self.initialize_habitats()
    
    def load_config(self) -> dict:
        """Load or create habitat configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            default_config = {
                "default_habitat": {
                    "name": "main_lab",
                    "isolation_level": 3,
                    "default_containment": {
                        "resources": {"cpu": "50%", "memory": "512M"},
                        "network_isolation": True,
                        "time_limit": 1800,
                        "recursive_depth_limit": 5
                    }
                },
                "experiment_types": {
                    "recursive_myth": "RecursiveMythEngine",
                    "pattern_test": "PatternTestSystem",
                    "symbolic_loop": "SymbolicLoopSystem"
                }
            }
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: dict = None):
        """Save habitat configuration"""
        if config is None:
            config = self.config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def initialize_habitats(self):
        """Initialize habitat instances"""
        default_config = self.config["default_habitat"]
        main_habitat = ExperimentalHabitat(
            name=default_config["name"],
            isolation_level=default_config["isolation_level"]
        )
        self.habitats["main"] = main_habitat
    
    def spawn_experiment(self, name: str, experiment_type: str = "recursive_myth", 
                        hypothesis: str = "Default experiment hypothesis", 
                        containment_rules: dict = None) -> dict:
        """Spawn a new experimental system"""
        
        if containment_rules is None:
            containment_rules = self.config["default_habitat"]["default_containment"]
        
        # Create experiment instance based on type
        if experiment_type == "recursive_myth":
            experiment = RecursiveMythEngine()
            experiment.name = name  # Override name
            experiment.hypothesis = hypothesis
        else:
            # Generic experimental system
            experiment = ExperimentalSystem(name, hypothesis)
        
        # Spawn in main habitat
        habitat = self.habitats["main"]
        exp_data = habitat.spawn_experiment(experiment, containment_rules)
        
        habitat_ux.print_card(
            f"Spawned Experiment: {name}",
            {
                "Habitat": habitat.name,
                "Hypothesis": hypothesis,
                "Containment Level": habitat.isolation_level,
                "Boundary": experiment.boundary.get_full_path()
            },
            icon="🧪",
            color=Colors.GREEN
        )
        print(f"{Colors.GREEN}🧪 Spawned experiment '{Colors.BOLD}{name}{Colors.RESET}{Colors.GREEN}' in habitat '{habitat.name}'{Colors.RESET}")
        print(f"   Hypothesis: {hypothesis}")
        print(f"   Containment Level: {habitat.isolation_level}")
        print(f"   Boundary: {experiment.boundary.get_full_path()}")
        
        return exp_data
    
    def run_experiment(self, name: str, habitat_name: str = "main") -> dict:
        """Run a spawned experiment"""
        habitat = self.habitats.get(habitat_name)
        if not habitat:
            raise ValueError(f"Habitat '{habitat_name}' not found")
        
        print(f"{Colors.BLUE}🚀 Running experiment '{name}' in habitat '{habitat_name}'...{Colors.RESET}")
        
        try:
            result = habitat.run_experiment(name)
            print(f"{Colors.GREEN}✅ Experiment '{name}' completed successfully{Colors.RESET}")
            print(f"{Colors.HEADER}Result summary:{Colors.RESET}")
            if isinstance(result, dict):
                for key, value in result.items():
                    if key != "nested":  # Don't print nested recursion
                        print(f"   {Colors.CYAN}{key}:{Colors.RESET} {value}")
            else:
                print(f"   {result}")
            return result
        except Exception as e:
            print(f"{Colors.RED}❌ Experiment '{name}' failed: {e}{Colors.RESET}")
            raise
    
    def _print_kv(self, key: str, value: Any, indent: int = 3):
        """Helper to print key-value pairs nicely aligned"""
        padding = " " * indent
        key_str = f"{key}:"
        print(f"{padding}{key_str:<25} {value}")

    def get_status(self, experiment_name: str = None, habitat_name: str = "main") -> dict:
        """Get habitat or experiment status"""
        habitat = self.habitats.get(habitat_name)
        if not habitat:
            raise ValueError(f"Habitat '{habitat_name}' not found")
        
        if experiment_name:
            # Get specific experiment status
            if experiment_name in habitat.active_experiments:
                exp_data = habitat.active_experiments[experiment_name]
                experiment = exp_data['experiment']
                status = {
                    'Status': experiment.status,
                    'Hypothesis': experiment.hypothesis,
                    'Created': experiment.created,
                    'Boundary': experiment.boundary.get_full_path() if experiment.boundary else None,
                    'Workspace': exp_data.get('workspace'),
                    'Containment Rules': exp_data.get('containment_rules')
                }
                habitat_ux.print_card(f"Experiment: {experiment_name}", status, icon="📊", color=Colors.BLUE)
                print(f"📊 Status for experiment '{experiment_name}':")
                self._print_kv("Status", status['status'])
                self._print_kv("Hypothesis", status['hypothesis'])
                self._print_kv("Created", status['created'])
                self._print_kv("Boundary", status['boundary'])
                self._print_kv("Workspace", status['workspace'])
                print(f"{Colors.HEADER}📊 Status for experiment '{Colors.BOLD}{experiment_name}{Colors.RESET}{Colors.HEADER}':{Colors.RESET}")
                for key, value in status.items():
                    if key == 'containment_rules' and isinstance(value, dict):
                        print(f"   {Colors.CYAN}{key.replace('_', ' ').title()}:{Colors.RESET}")
                        for k, v in value.items():
                            print(f"     - {k}: {v}")
                    else:
                        print(f"   {Colors.CYAN}{key.replace('_', ' ').title()}:{Colors.RESET} {value}")
                return status
            elif experiment_name in habitat.graduated_patterns:
                print(f"{Colors.GREEN}🎓 Experiment '{experiment_name}' has graduated to Code Forge{Colors.RESET}")
                return habitat.graduated_patterns[experiment_name]
            elif experiment_name in habitat.failed_experiments:
                print(f"{Colors.RED}💀 Experiment '{experiment_name}' has been composted{Colors.RESET}")
                return habitat.failed_experiments[experiment_name]
            else:
                print(f"{Colors.YELLOW}❓ Experiment '{experiment_name}' not found in habitat '{habitat_name}'{Colors.RESET}")
                return {}
        else:
            # Get habitat status
            status = habitat.get_habitat_status()
            # Clean up status keys for display
            display_status = {
                "Isolation Level": status['isolation_level'],
                "Nesting Depth": status['nesting_depth'],
                "Active Experiments": status['active_experiments'],
                "Graduated Patterns": status['graduated_patterns'],
                "Failed Experiments": status['failed_experiments'],
                "Workspace": status['workspace']
            }
            habitat_ux.print_card(f"Habitat: {habitat_name}", display_status, icon="🏠", color=Colors.BLUE)
            print(f"🏠 Status for habitat '{habitat_name}':")
            self._print_kv("Name", status['name'])
            self._print_kv("Isolation Level", status['isolation_level'])
            self._print_kv("Nesting Depth", status['nesting_depth'])
            self._print_kv("Active Experiments", status['active_experiments'])
            self._print_kv("Graduated Patterns", status['graduated_patterns'])
            self._print_kv("Failed Experiments", status['failed_experiments'])
            self._print_kv("Workspace", status['workspace'])
            print(f"{Colors.HEADER}🏠 Status for habitat '{Colors.BOLD}{habitat_name}{Colors.RESET}{Colors.HEADER}':{Colors.RESET}")
            for key, value in status.items():
                if key == 'containment_boundaries' and isinstance(value, list):
                     print(f"   {Colors.CYAN}{key.replace('_', ' ').title()}:{Colors.RESET} {len(value)} active")
                else:
                    print(f"   {Colors.CYAN}{key.replace('_', ' ').title()}:{Colors.RESET} {value}")
            return status
    
    def graduate_experiment(self, name: str, habitat_name: str = "main") -> dict:
        """Graduate an experiment to the Code Forge"""
        habitat = self.habitats.get(habitat_name)
        if not habitat:
            raise ValueError(f"Habitat '{habitat_name}' not found")
        
        print(f"{Colors.BLUE}🎓 Graduating experiment '{name}' to Code Forge...{Colors.RESET}")
        
        try:
            forge_package = habitat.graduate_to_forge(name)
            print(f"{Colors.GREEN}✅ Experiment '{name}' successfully graduated!{Colors.RESET}")
            print(f"{Colors.HEADER}Forge package contents:{Colors.RESET}")
            print(f"   {Colors.CYAN}Code patterns:{Colors.RESET} {forge_package['code_patterns']}")
            print(f"   {Colors.CYAN}Symbolic mappings:{Colors.RESET} {forge_package['symbolic_mappings']}")
            print(f"   {Colors.CYAN}Integration hooks:{Colors.RESET} {forge_package['integration_hooks']}")
            habitat_ux.print_card(
                f"Graduated: {name}",
                {
                    "Status": "Success",
                    "Code Patterns": forge_package['code_patterns'],
                    "Symbolic Mappings": forge_package['symbolic_mappings'],
                    "Integration Hooks": forge_package['integration_hooks']
                },
                icon="✅",
                color=Colors.GREEN
            )
            return forge_package
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to graduate experiment '{name}': {e}{Colors.RESET}")
            raise
    
    def compost_experiment(self, name: str, reason: str, habitat_name: str = "main") -> dict:
        """Compost a failed experiment"""
        habitat = self.habitats.get(habitat_name)
        if not habitat:
            raise ValueError(f"Habitat '{habitat_name}' not found")
        
        print(f"{Colors.YELLOW}♻️  Composting experiment '{name}' - Reason: {reason}{Colors.RESET}")
        
        try:
            lessons = habitat.contain_failure(name, reason)
            print(f"{Colors.GREEN}✅ Experiment '{name}' safely composted{Colors.RESET}")
            print(f"{Colors.HEADER}Lessons learned:{Colors.RESET}")
            for lesson_type, lesson_data in lessons.items():
                print(f"   {Colors.CYAN}{lesson_type}:{Colors.RESET} {lesson_data}")
            habitat_ux.print_card(
                f"Composted: {name}",
                lessons,
                icon="✅",
                color=Colors.YELLOW
            )
            return lessons
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to compost experiment '{name}': {e}{Colors.RESET}")
            raise
    
    def create_nested_habitat(self, parent_experiment: str, child_name: str, 
                            parent_habitat: str = "main") -> 'ExperimentalHabitat':
        """Create a nested habitat"""
        parent_hab = self.habitats.get(parent_habitat)
        if not parent_hab:
            raise ValueError(f"Parent habitat '{parent_habitat}' not found")
        
        print(f"{Colors.BLUE}🪆 Creating nested habitat '{child_name}' under experiment '{parent_experiment}'...{Colors.RESET}")
        
        try:
            nested_habitat = parent_hab.nest_habitat(parent_experiment, child_name)
            habitat_key = f"{parent_habitat}_{child_name}"
            self.habitats[habitat_key] = nested_habitat
            
            print(f"{Colors.GREEN}✅ Nested habitat '{child_name}' created successfully{Colors.RESET}")
            print(f"   {Colors.CYAN}Nesting depth:{Colors.RESET} {nested_habitat.nesting_depth}")
            print(f"   {Colors.CYAN}Isolation level:{Colors.RESET} {nested_habitat.isolation_level}")
            print(f"   {Colors.CYAN}Access key:{Colors.RESET} {habitat_key}")
            habitat_ux.print_card(
                f"Nested Habitat: {child_name}",
                {
                    "Parent Experiment": parent_experiment,
                    "Nesting Depth": nested_habitat.nesting_depth,
                    "Isolation Level": nested_habitat.isolation_level,
                    "Access Key": habitat_key
                },
                icon="✅",
                color=Colors.BLUE
            )
            
            return nested_habitat
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to create nested habitat: {e}{Colors.RESET}")
            raise
    
    def list_habitats(self):
        """List all active habitats"""
        print(f"{Colors.HEADER}🏠 Active Habitats:{Colors.RESET}")
        print("=" * 50)
        
        for key, habitat in self.habitats.items():
            status = habitat.get_habitat_status()
            print(f"{Colors.BOLD}📍 {key} ({habitat.name}){Colors.RESET}")
            print(f"   {Colors.CYAN}Isolation Level:{Colors.RESET} {status['isolation_level']}")
            print(f"   {Colors.CYAN}Nesting Depth:{Colors.RESET} {status['nesting_depth']}")
            print(f"   {Colors.CYAN}Active Experiments:{Colors.RESET} {status['active_experiments']}")
            print(f"   {Colors.CYAN}Graduated Patterns:{Colors.RESET} {status['graduated_patterns']}")
            print(f"   {Colors.CYAN}Failed Experiments:{Colors.RESET} {status['failed_experiments']}")
            print(f"   {Colors.CYAN}Workspace:{Colors.RESET} {status['workspace']}")
            print()
        habitat_ux.print_header("Active Habitats", color=Colors.HEADER)
        
        for key, habitat in self.habitats.items():
            status = habitat.get_habitat_status()
            display_status = {
                "Habitat Name": habitat.name,
                "Isolation Level": status['isolation_level'],
                "Nesting Depth": status['nesting_depth'],
                "Active Experiments": status['active_experiments'],
                "Graduated Patterns": status['graduated_patterns'],
                "Failed Experiments": status['failed_experiments'],
                "Workspace": status['workspace']
            }
            habitat_ux.print_card(f"Habitat: {key}", display_status, icon="📍", color=Colors.HEADER)
        print("🏠 Active Habitats:")
        print("=" * 60)
        print(f"{'KEY':<20} {'NAME':<20} {'LVL':<5} {'ACTIVE':<7} {'WORKSPACE'}")
        print("-" * 60)
        
        for key, habitat in self.habitats.items():
            status = habitat.get_habitat_status()
            workspace_short = status['workspace']
            if len(workspace_short) > 30:
                workspace_short = "..." + workspace_short[-27:]

            print(f"{key:<20} {status['name']:<20} {status['isolation_level']:<5} {status['active_experiments']:<7} {workspace_short}")
        print("=" * 60)
    
    def cleanup_all(self, force: bool = False):
        """Cleanup all habitats"""
        print(f"{Colors.BLUE}🧹 Cleaning up all habitats...{Colors.RESET}")
        if not force:
            response = input("⚠️  Are you sure you want to cleanup all habitats? This cannot be undone. [y/N] ")
            if response.lower() not in ['y', 'yes']:
                print("❌ Cleanup cancelled.")
                return

        print("🧹 Cleaning up all habitats...")
        
        for key, habitat in self.habitats.items():
            try:
                habitat.cleanup()
                print(f"{Colors.GREEN}✅ Cleaned up habitat '{key}'{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}❌ Failed to cleanup habitat '{key}': {e}{Colors.RESET}")
        
        print(f"{Colors.GREEN}🎉 Cleanup complete!{Colors.RESET}")

def main():
    """Main command-line interface"""
    parser = argparse.ArgumentParser(description="Experimental Habitat Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Spawn command
    spawn_parser = subparsers.add_parser('spawn', help='Spawn a new experiment')
    spawn_parser.add_argument('name', help='Experiment name')
    spawn_parser.add_argument('--type', default='recursive_myth', help='Experiment type')
    spawn_parser.add_argument('--hypothesis', default='Default experimental hypothesis', help='Experiment hypothesis')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run an experiment')
    run_parser.add_argument('name', help='Experiment name')
    run_parser.add_argument('--habitat', default='main', help='Habitat name')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Get status')
    status_parser.add_argument('name', nargs='?', help='Experiment name (optional)')
    status_parser.add_argument('--habitat', default='main', help='Habitat name')
    
    # Graduate command
    grad_parser = subparsers.add_parser('graduate', help='Graduate experiment to Code Forge')
    grad_parser.add_argument('name', help='Experiment name')
    grad_parser.add_argument('--habitat', default='main', help='Habitat name')
    
    # Compost command
    compost_parser = subparsers.add_parser('compost', help='Compost failed experiment')
    compost_parser.add_argument('name', help='Experiment name')
    compost_parser.add_argument('--reason', required=True, help='Failure reason')
    compost_parser.add_argument('--habitat', default='main', help='Habitat name')
    
    # Nest command
    nest_parser = subparsers.add_parser('nest', help='Create nested habitat')
    nest_parser.add_argument('parent_experiment', help='Parent experiment name')
    nest_parser.add_argument('child_name', help='Child habitat name')
    nest_parser.add_argument('--parent-habitat', default='main', help='Parent habitat name')
    
    # List command
    subparsers.add_parser('list-habitats', help='List all habitats')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Cleanup all habitats')
    cleanup_parser.add_argument('-f', '--force', action='store_true', help='Force cleanup without confirmation')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize manager
    manager = HabitatManager()
    
    try:
        if args.command == 'spawn':
            manager.spawn_experiment(args.name, args.type, args.hypothesis)
            
        elif args.command == 'run':
            manager.run_experiment(args.name, args.habitat)
            
        elif args.command == 'status':
            manager.get_status(args.name, args.habitat)
            
        elif args.command == 'graduate':
            manager.graduate_experiment(args.name, args.habitat)
            
        elif args.command == 'compost':
            manager.compost_experiment(args.name, args.reason, args.habitat)
            
        elif args.command == 'nest':
            manager.create_nested_habitat(args.parent_experiment, args.child_name, args.parent_habitat)
            
        elif args.command == 'list-habitats':
            manager.list_habitats()
            
        elif args.command == 'cleanup':
            manager.cleanup_all(args.force)
            
    except Exception as e:
        print(f"{Colors.RED}❌ Command failed: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()