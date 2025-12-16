## 2025-05-05 - ContainmentBoundary Path Caching
**Learning:** Caching recursive properties in a mutable tree structure requires careful invalidation logic. Initially, I implemented simple caching in `__init__`, but this broke correctness when properties changed.
**Action:** Always verify if cached data depends on mutable properties. If so, use property setters to invalidate or update the cache, and propagate changes to dependent children if necessary. For read-heavy, write-rare structures, O(subtree) updates for O(1) reads is a good trade-off.
