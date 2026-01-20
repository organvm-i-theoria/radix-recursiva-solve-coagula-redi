# Security Fix: Path Traversal Vulnerability in Experiment Spawning

## Summary

Fixed a **path traversal vulnerability** in the `ExperimentalHabitat.spawn_experiment()` method that could allow malicious experiment names to escape the containment boundary and create directories outside the intended temporary workspace.

## Vulnerability Details

### Issue
The original implementation of `spawn_experiment()` used unsanitized user input (experiment names) directly in filesystem operations without validation:

```python
# VULNERABLE CODE (before fix)
exp_dir = os.path.join(self.temp_dir, experiment.name)
os.makedirs(exp_dir, exist_ok=True)
```

### Attack Vectors
An attacker could potentially:
- Use path traversal sequences like `../../../etc/passwd` to escape the temp directory
- Create directories in system locations
- Overwrite or access files outside the intended containment boundary
- Bypass the isolation mechanisms of the experimental habitat

### Example Exploit Attempts
```python
# These malicious names would have worked before the fix:
malicious_experiment = ExperimentalSystem("../../../tmp/malicious", "Bad hypothesis")
malicious_experiment = ExperimentalSystem("../../escape", "Evil hypothesis")
malicious_experiment = ExperimentalSystem("name/../traversal", "Sneaky hypothesis")
```

## The Fix

### Implementation
Added strict input validation using a whitelist approach at line 134-136 of `experimental_habitat_implementation.py`:

```python
# Validate experiment name to prevent path traversal
if not re.match(r'^[a-zA-Z0-9_-]+$', experiment.name):
    raise ValueError(f"Invalid experiment name '{experiment.name}'. Name must contain only alphanumeric characters, underscores, and hyphens.")
```

### Security Strategy

1. **Whitelist Approach**: Only allow safe characters (alphanumeric, underscore, hyphen)
2. **Fail-Safe**: Reject any experiment name that doesn't match the pattern
3. **Clear Error Messages**: Inform users why their experiment name was rejected
4. **Defense in Depth**: Validation happens BEFORE any filesystem operations

### What's Allowed
- ✅ Alphanumeric characters: `a-z`, `A-Z`, `0-9`
- ✅ Underscores: `_`
- ✅ Hyphens: `-`

Examples of valid names:
- `recursive_myth_engine`
- `test-experiment-123`
- `MyExperiment_v2`

### What's Blocked
- ❌ Path traversal sequences: `..`, `/`, `\`
- ❌ Special characters: `;`, `|`, `&`, `$`, `` ` ``, etc.
- ❌ Whitespace: spaces, tabs, newlines
- ❌ Quotes: `'`, `"`
- ❌ Any other non-alphanumeric characters

## Testing

### Automated Tests
A comprehensive test suite (`test_path_traversal_fix.py`) verifies:
- ✅ Valid experiment names are accepted
- ✅ All 23+ malicious patterns are rejected
- ✅ Error messages are clear and informative

### Test Results
```
✅ All 5 valid names were accepted
✅ All 23/23 malicious names were rejected
✅ Path traversal vulnerability fix is working correctly!
```

## Security Impact

### Before Fix
- **Severity**: HIGH
- **Impact**: Arbitrary directory creation, potential file system escape
- **Exploitability**: Easy (requires only passing a crafted experiment name)
- **Scope**: Any code calling `spawn_experiment()` with user-controlled names

### After Fix
- **Status**: MITIGATED
- **Protection**: Input validation blocks all path traversal attempts
- **Side Effects**: None (legitimate experiment names still work)
- **Performance**: Negligible (single regex match per spawn)

## Recommendations

### For Developers
1. **Always validate user input** before using it in filesystem operations
2. **Use whitelist validation** rather than trying to blacklist dangerous patterns
3. **Implement defense in depth** - validation at multiple layers
4. **Write security tests** for any code that accepts user input

### For Users
- Use only alphanumeric characters, underscores, and hyphens in experiment names
- Avoid special characters and path separators
- The system will clearly indicate if an experiment name is invalid

## Related Security Considerations

### Additional Protections Already in Place
1. **Temporary Directory Isolation**: Experiments run in isolated temp directories
2. **Containment Boundaries**: Each experiment has its own containment boundary
3. **Resource Limits**: Configurable resource constraints per experiment
4. **Cleanup Mechanisms**: Automatic cleanup of experiment workspaces

### Future Enhancements
Consider adding:
- Experiment name length limits (e.g., max 255 characters)
- Rate limiting on experiment spawning
- Audit logging of all experiment creation attempts
- Additional filesystem sandboxing (e.g., using chroot or containers)

## References

- OWASP Path Traversal: https://owasp.org/www-community/attacks/Path_Traversal
- CWE-22: Improper Limitation of a Pathname to a Restricted Directory
- File: `experimental_habitat_implementation.py`, lines 134-136
- Test: `test_path_traversal_fix.py`

## Commit Information

- **Fix Commit**: a86fb6ed646ff1bc2494c59d06dbe1225dbbd3b7
- **Title**: Shield: Fix path traversal vulnerability in experiment spawning
- **Date**: Mon Dec 15 15:40:49 2025
