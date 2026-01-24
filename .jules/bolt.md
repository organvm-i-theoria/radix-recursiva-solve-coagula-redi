## 2025-05-05 - ContainmentBoundary Path Caching
**Learning:** Caching recursive properties in a mutable tree structure requires careful invalidation logic. Initially, I implemented simple caching in `__init__`, but this broke correctness when properties changed.
**Action:** Always verify if cached data depends on mutable properties. If so, use property setters to invalidate or update the cache, and propagate changes to dependent children if necessary. For read-heavy, write-rare structures, O(subtree) updates for O(1) reads is a good trade-off.
## 2025-12-15 - Optimizing Deep Recursive Access
**Learning:** In deep tree structures where parent nodes are immutable, caching the full path at initialization transforms $O(depth)$ access into $O(1)$. This is critical for performance when path lookups are frequent (e.g., status reporting).
**Action:** Always check if a recursive property can be computed at construction time. For existing objects or backward compatibility, implement a fallback that uses the original recursive logic if the cached value is missing.
## 2026-01-21 - Text Sanitization Overhead
**Learning:** Manual character-by-character loops in Python for text sanitization (e.g., in `sanitize_for_terminal`) are significantly slower than C-optimized methods like `str.translate`. For high-volume UI rendering or logging, this overhead becomes noticeable.
**Action:** Use `str.translate` with pre-computed translation tables for filtering or mapping characters instead of manual iteration.
