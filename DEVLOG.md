# Development Log – The Torchbearer

**Student Name:** Rachel Rogers
**Student ID:** 133560411

---

## Entry 1 – [05/11/2026]: Initial Plan
_I will start with Part 2, because run_dijkstra seems to be the foundation for
everything. If I get that right, I can trust the distance table when building
the search. I think the trickiest part will be Part 5 and Part 6, specifically getting
the recursive explore function with backtracking and pruning to work, and getting the state
management (with unmarking relics on the backtrack) right. For testing, I will use the
provided four test cases to start, and then make my own graphs with known optimal routes to
check edge cases._

---

## Entry 2 – [05/12/2026]: Wrong Assumption in Part 2
_When I first implemented select_sources, I only included the relic nodes as Dijkstra sources
because I thought the only distances that mattered were between relics. This was a mistake since
the Torchbearer actually starts at the spawn node, not at a relic. This means the first part of
every route is spawn -> first relic, and without running Dijkstra from spawn, those distances
were missing from the table. The fix was to add spawn to the list of source nodes before
removing duplicates._

---

## Entry 3 – [05/14/2026]: Wrong Assumption in Part 6
_My first version of the lower bound only used min_to_next, which is the cheapest cost from the
current location to any remaining relic. This made the estimate too weak, so the algorithm didn’t
prune many unnecessary branches. Later, when I tried to improve the bound by using the cost to
one specific relic instead of the minimum over all relics, I created a bigger problem: sometimes
that relic was not part of the best route, so the estimate became too high and could incorrectly
prune the optimal path. The fix was to always use the minimum cost over all remaining relics for
both min_to_next and min_to_exit, which guarantees the estimate never becomes larger than the true
remaining cost._

---

## Entry 4 – [05/14/2026]: Post-Implementation Reflection
_Given more time, there are two things I would improve. First, the lower bound in explore only
looks at the cheapest next relic and cheapest exit path. Using a stronger estimate that considers
all remaining relics together would allow the algorithm to prune more branches and run faster.
Second, the search currently checks relics in arbitrary set order, so it may not find good routes
early. Sorting relics by their distance from the current location would likely find better solutions
sooner and improve pruning._

---

## Final Entry – [05/14/2026]: Time Estimate
| Part | Estimated Hours |
|---|-----------------|
| Part 1: Problem Analysis | 1               |
| Part 2: Precomputation Design | 2.5             |
| Part 3: Algorithm Correctness | 0.75            |
| Part 4: Search Design | 0.5             |
| Part 5: State and Search Space | 0.75            |
| Part 6: Pruning | 2.5             |
| Part 7: Implementation | 0.5             |
| README and DEVLOG writing | 1               |
| **Total** | 9.5             |

_Note: I filled out the README and the torchbearer.py implementation simultaneously as I went. Sorry if I wasn't
intended to do it that way. For each part of the time estimate (Parts 1-6), I included the time I spent
on the README and torchbearer.py for that part._

_I used "Part 7: Implementation" as the amount of time I spent cleaning things up torchbearer.py (0.5 hr)
and the "README and DEVLOG writing" part is the time I spent writing the DEVLOG and cleaning up the README (1 hr).
I hope that makes sense._