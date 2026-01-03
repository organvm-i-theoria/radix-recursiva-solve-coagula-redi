# Experimental Habitat System

> A safe, isolated containment system for experimental code - "hat on a hat on a"

## Overview

The **Experimental Habitat System** provides a robust framework for safely executing experimental code in nested, isolated environments. Each "habitat" acts as a containment boundary, allowing you to run experimental systems with progressive isolation levels, monitor their execution, and either graduate successful patterns to production or safely compost failures for learning.

### Key Concepts

- **Habitat**: An isolated execution environment for experiments
- **Experiment**: A testable system with a hypothesis
- **Containment Boundary**: Isolation layer protecting the host system
- **Nesting**: Creating habitats within habitats for deeper isolation
- **Graduation**: Promoting successful experiments to the Code Forge
- **Composting**: Safely containing failures and extracting lessons

## Features

✅ **Multi-layer Containment** - Progressive isolation levels for risk management
✅ **Nested Habitats** - Create experiments within experiments ("hat on a hat")
✅ **Safe Execution** - Experiments run in controlled, monitored environments
✅ **Pattern Graduation** - Successful patterns can be promoted to production
✅ **Failure Composting** - Failed experiments safely contained with lesson extraction
✅ **Resource Management** - Configure CPU, memory, and time limits
✅ **Complete Lifecycle** - From spawning to cleanup, fully managed

## Installation

No external dependencies required! The system uses only Python standard library.

### Requirements

- Python 3.7 or higher
- Standard library modules: `json`, `os`, `tempfile`, `logging`, `argparse`, `cmd`

### Setup

```bash
# Clone or download the repository
git clone <repository-url>
cd solve-et-coagula

# Verify installation
python3 simple_habitat_demo.py
```

## Quick Start

### 1. Simple Demo

Run the basic demonstration:

```bash
python3 simple_habitat_demo.py
```

This demonstrates:
- Creating a habitat
- Spawning experiments
- Nested habitat creation
- Running experiments
- Graduation workflow

### 2. Complete Workflow

Run the comprehensive demonstration:

```bash
python3 complete_workflow_demo.py
```

This shows:
- Multiple experiment types
- Resource management
- Failure handling
- Status monitoring
- Complete lifecycle

### 3. Interactive Shell

Launch the interactive habitat manager:

```bash
python3 interactive_habitat.py
```

Available commands:
- `spawn <name>` - Create new experiment
- `run <name>` - Execute experiment
- `status [name]` - Check status
- `graduate <name>` - Promote to Code Forge
- `compost <name> <reason>` - Safely contain failure
- `nest <parent> <child>` - Create nested habitat
- `list` - Show all habitats
- `help` - Show all commands

Example session:

```
(habitat) spawn test1 --hypothesis "Testing pattern recognition"
(habitat) run test1
(habitat) status test1
(habitat) graduate test1
(habitat) quit
```

## Usage Examples

### Basic Experiment

```python
from experimental_habitat_implementation import ExperimentalHabitat, ExperimentalSystem

# Create habitat
habitat = ExperimentalHabitat("my_lab", isolation_level=3)

# Define experiment
class MyExperiment(ExperimentalSystem):
    def _execute_experiment(self):
        # Your experimental code here
        return {"result": "success"}

# Spawn and run
exp = MyExperiment("my_test", "Testing hypothesis")
containment_rules = {
    'resources': {'cpu': '50%', 'memory': '512M'},
    'time_limit': 60
}

habitat.spawn_experiment(exp, containment_rules)
result = habitat.run_experiment("my_test")

# Graduate or compost
if result["result"] == "success":
    habitat.graduate_to_forge("my_test")
else:
    habitat.contain_failure("my_test", "Test failed")

# Cleanup
habitat.cleanup()
```

### Nested Habitats

```python
# Create main habitat
main_habitat = ExperimentalHabitat("main_lab", isolation_level=1)

# Spawn parent experiment
parent = ExperimentalSystem("parent_exp", "Parent hypothesis")
main_habitat.spawn_experiment(parent, {'resources': {}})

# Create nested habitat
nested_habitat = main_habitat.nest_habitat("parent_exp", "sub_lab")

# Spawn child experiment in nested habitat
child = ExperimentalSystem("child_exp", "Child hypothesis")
nested_habitat.spawn_experiment(child, {'resources': {}})

# Run both
main_habitat.run_experiment("parent_exp")
nested_habitat.run_experiment("child_exp")

# Cleanup both
nested_habitat.cleanup()
main_habitat.cleanup()
```

### Resource Containment

```python
# Define strict resource limits
strict_containment = {
    'resources': {
        'cpu': '25%',
        'memory': '256M'
    },
    'network_isolation': True,
    'time_limit': 30,
    'recursive_depth_limit': 3
}

habitat.spawn_experiment(experiment, strict_containment)
```

## Architecture

### Components

1. **ContainmentBoundary**
   - Manages isolation layers
   - Tracks boundary hierarchy
   - Detects potential breaches

2. **ExperimentalSystem**
   - Base class for all experiments
   - Defines experiment lifecycle
   - Handles execution and errors

3. **ExperimentalHabitat**
   - Main container environment
   - Manages multiple experiments
   - Handles graduation and composting

4. **RecursiveMythEngine**
   - Example experimental system
   - Demonstrates recursive patterns
   - Shows depth limiting

### Isolation Levels

- **Level 1**: Basic isolation
- **Level 2**: Enhanced isolation
- **Level 3**: High isolation (default)
- **Level 4+**: Progressive nesting depth

Each nested habitat increments the isolation level automatically.

## Workflow

```
┌─────────────────┐
│ Create Habitat  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Spawn Experiment│◄──┐
└────────┬────────┘   │
         │            │ (Nesting)
         ▼            │
┌─────────────────┐   │
│ Run Experiment  │   │
└────────┬────────┘   │
         │            │
    ┌────┴────┐       │
    │         │       │
    ▼         ▼       │
┌─────┐   ┌──────┐   │
│Success│ │Failure│   │
└──┬──┘   └───┬──┘   │
   │          │       │
   ▼          ▼       │
┌──────┐  ┌────────┐ │
│Graduate│ │Compost │ │
└──┬───┘  └────┬───┘ │
   │           │      │
   ▼           ▼      │
┌──────────────────┐ │
│    Cleanup       │◄┘
└──────────────────┘
```

## Testing

Run the test suite:

```bash
python3 test_habitat_system.py
```

Expected output:
```
Ran 21 tests in 0.013s

OK
```

Tests cover:
- Containment boundary creation
- Experiment spawning and execution
- Nested habitat workflows
- Graduation and composting
- Error handling
- Resource management

## API Reference

### ExperimentalHabitat

#### Methods

- `spawn_experiment(experiment, containment_rules)` - Spawn new experiment
- `run_experiment(experiment_name)` - Execute spawned experiment
- `nest_habitat(parent_experiment, child_name)` - Create nested habitat
- `graduate_to_forge(experiment_name)` - Promote successful experiment
- `contain_failure(experiment_name, reason)` - Compost failed experiment
- `get_habitat_status()` - Get current status
- `cleanup()` - Clean up resources

### ExperimentalSystem

#### Methods

- `run()` - Execute the experiment
- `_execute_experiment()` - Override this in subclasses

#### Attributes

- `name` - Experiment name
- `hypothesis` - Experimental hypothesis
- `status` - Current status (spawning/running/completed/failed)
- `results` - Experiment results
- `failures` - List of failures
- `boundary` - Containment boundary

## Advanced Features

### Custom Experiments

Create custom experimental systems by subclassing `ExperimentalSystem`:

```python
class CustomExperiment(ExperimentalSystem):
    def __init__(self):
        super().__init__(
            name="custom_exp",
            hypothesis="My custom hypothesis"
        )
        # Add custom attributes

    def _execute_experiment(self):
        # Implement your experimental logic
        # This is where your code runs
        result = do_something_experimental()
        return {"custom_data": result}
```

### Monitoring

```python
# Get habitat status
status = habitat.get_habitat_status()
print(f"Active experiments: {status['active_experiments']}")
print(f"Graduated: {status['graduated_patterns']}")
print(f"Failed: {status['failed_experiments']}")

# Get experiment status
exp_data = habitat.active_experiments['my_exp']
print(f"Status: {exp_data['experiment'].status}")
print(f"Workspace: {exp_data['workspace']}")
```

### Pattern Extraction

When graduating experiments, the system extracts:

- **Code Patterns**: Reusable code structures
- **Symbolic Mappings**: Abstract pattern relationships
- **Integration Hooks**: Connection points for other systems

```python
forge_package = habitat.graduate_to_forge("my_exp")
patterns = forge_package['code_patterns']
symbols = forge_package['symbolic_mappings']
hooks = forge_package['integration_hooks']
```

## Best Practices

1. **Always Clean Up**: Use `habitat.cleanup()` or context managers
2. **Set Resource Limits**: Define appropriate containment rules
3. **Monitor Status**: Check experiment status regularly
4. **Handle Failures**: Always use try/except for experiment execution
5. **Graduate Incrementally**: Test patterns before promoting
6. **Use Nesting Wisely**: Don't nest too deeply (limit: 5 levels)
7. **Document Hypotheses**: Clear hypotheses aid in learning

## Troubleshooting

### Common Issues

**Experiment not found**
- Ensure experiment is spawned before running
- Check experiment name matches exactly

**Resource limit exceeded**
- Increase time_limit in containment rules
- Reduce recursive_depth_limit if applicable

**Cleanup errors**
- Check file permissions on temp directories
- Ensure no processes are holding resources

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

This system is part of the 4_S0VRC3 vault. See the main repository for contribution guidelines.

## License

See repository license file.

## Acknowledgments

Part of Anthony James Padavano's recursive creative system.

## Support

For issues, questions, or contributions:
1. Check the documentation
2. Run the demos and tests
3. Review the example code
4. Consult the main README

---

**Status**: ✅ Working Prototype
**Version**: 1.0.0
**Last Updated**: 2025-11-19
