## 2025-12-14 - Path Traversal in Habitat Creation
**Vulnerability:** Path traversal vulnerability in `ExperimentalHabitat.spawn_experiment`.
**Learning:** `os.path.join` with user-controlled input allows creating directories outside the intended root if the input contains `../`.
**Prevention:** Always normalize paths with `os.path.abspath` and verify they start with the intended root using `os.path.commonpath` or `startswith` before performing file operations.
