# Development Log – The Torchbearer

**Student Name:** Rachel Rogers
**Student ID:** 133560411

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – [05/11/2026]: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

_I will start with Part 2, because run_dijkstra seems to be the foundation for
everything. If I get that right, I can trust the distance table when building
the search. I think the trickiest part will be Part 5 and Part 6, specifically getting
the recursive explore function with backtracking and pruning to work, and getting the state
management (with unmarking relics on the backtrack) right. For testing, I will use the
provided four test cases to start, and then make my own graphs with known optimal routes to
check edge cases._

---

## Entry 2 – [05/12/2026]: Wrong Assumption in Part 2

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

_When I first implemented select_sources, I only included the relic nodes as Dijkstra sources
because I thought the only distances that mattered were between relics. This was a mistake since
the Torchbearer actually starts at the spawn node, not at a relic. This means the first part of
every route is spawn -> first relic, and without running Dijkstra from spawn, those distances
were missing from the table. The fix was to add spawn to the list of source nodes before
removing duplicates._

---

## Entry 3 – [Date]: [Short description]

_Your entry here._

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time. 

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|-----------------|
| Part 1: Problem Analysis | 1               |
| Part 2: Precomputation Design | 2.5             |
| Part 3: Algorithm Correctness | 0.75            |
| Part 4: Search Design |                 |
| Part 5: State and Search Space |                 |
| Part 6: Pruning |                 |
| Part 7: Implementation |                 |
| README and DEVLOG writing |                 |
| **Total** | 4.25            |