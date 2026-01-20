## 2025-12-14 - Path Traversal in Habitat Creation
**Vulnerability:** Path traversal vulnerability in `ExperimentalHabitat.spawn_experiment`.
**Learning:** `os.path.join` with user-controlled input allows creating directories outside the intended root if the input contains `../`, `..\`, absolute paths (`/`, `C:\`), or other traversal patterns.
**Prevention:** 
1. Normalize path separators (convert `\` to `/`) to handle cross-platform attacks
2. Check for parent directory references (`..`) anywhere in the path
3. Check for absolute path indicators (leading `/` or `\`)
4. Check for Windows drive letters (`:` in position 1)
5. Use `os.path.abspath` and verify with `os.path.commonpath` that resulting path is within intended root
6. Handle `ValueError` from `commonpath` when paths are on different drives
**Fixed:** 2026-01-03 - Enhanced multi-layer validation prevents all known path traversal vectors

## 2025-12-16 - Path Traversal in Experiment Names
**Vulnerability:** Path traversal vulnerability in `spawn_experiment` and `nest_habitat` allowing creation of files outside the temporary directory using names like `../pwned`.
**Learning:** `os.path.join` does not sanitize input paths. Input validation is critical for file operations, especially when user input is used as part of a file path.
**Prevention:** Strictly validate all inputs used in file system operations. Use a strict allowlist (alphanumeric + safe chars) rather than trying to sanitize (blocklist).
## 2025-12-15 - Path Traversal in Experiment Names
**Vulnerability:** The `spawn_experiment` function in `experimental_habitat_implementation.py` used `experiment.name` directly in `os.path.join(self.temp_dir, experiment.name)`. This allowed creating directories outside the temporary habitat directory by providing an absolute path or path using `..`.
**Learning:** `os.path.join` does not prevent path traversal if one of the components is an absolute path. It simply returns the absolute path. Even with `os.makedirs`, this can be exploited to write to arbitrary locations where the user has permissions.
**Prevention:** Always validate user-supplied names that are used for filesystem operations. Ensure they do not contain path separators or resolve to a path outside the intended directory. Using `os.path.basename` or strict character whitelisting is recommended.

## 2026-01-18 - Over-Strict Validation Breaking Functionality
**Vulnerability:** Strict regex validation `^[a-zA-Z0-9_-]+$` in `spawn_experiment` blocked legitimate nested paths (e.g., `nested/safe/path`) and dots (`test.experiment`), causing operational failures.
**Learning:** Security controls that are too restrictive will be bypassed or cause denial of service. Input validation must align with business requirements (e.g. nested paths).
**Prevention:** Use a balanced validation approach: allow necessary characters (like `/` and `.`) for functionality, but explicitly block dangerous patterns (`..`, absolute paths) and verify containment (via `commonpath`) to maintain security. Precision is key.
