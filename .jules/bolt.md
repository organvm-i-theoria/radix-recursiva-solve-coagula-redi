## 2025-12-15 - Optimizing Deep Recursive Access
**Learning:** In deep tree structures where parent nodes are immutable, caching the full path at initialization transforms $O(depth)$ access into $O(1)$. This is critical for performance when path lookups are frequent (e.g., status reporting).
**Action:** Always check if a recursive property can be computed at construction time. For existing objects or backward compatibility, implement a fallback that uses the original recursive logic if the cached value is missing.
