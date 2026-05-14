# The Torchbearer

**Student Name:** Rachel Rogers
**Student ID:** 133560411
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis
- **Why a single shortest-path run from S is not enough:**
  _Running Dijkstra once from S can find the cheapest path to each location on its own, but it
can’t figure out the best order to visit multiple relic chambers. For example, going to R1 before
R2 might cost less overall than going to R2 before R1, and a single run doesn’t compare those 
possibilities._

- **What decision remains after all inter-location costs are known:**
  _Even after we know the cheapest travel cost between every important location, we still have
to decide the best order to collect the relics before finally heading to the exit._

- **Why this requires a search over orders (one sentence):**
  _Since the total fuel cost changes depending on the order the relics are visited, the engine has 
to check different possible orders to find the cheapest overall route._


---

## Part 2: Precomputation Design

### Part 2a: Source Selection
| Source Node Type | Why it is a source |
|---|---|
| _Spawn (entrance) S_ | _The Torchbearer departs from here, so we need the cheapest cost from S to every relic and to the exit._ |
| _Each relic chamber Ri_ | _After picking up a relic, the Torchbearer travels from that relic to another relic or to the exit, so we need distances from every relic too._ |

### Part 2b: Distance Storage
| Property | Your answer                                                                                                     |
|---|-----------------------------------------------------------------------------------------------------------------|
| Data structure name | Nested dictionary (dict[node, dict[node, float]])                                                               |
| What the keys represent | A source node (spawn or a relic) that Dijkstra was run from                                                     |
| What the values represent | A dictionary mapping every graph node to its minimum travel cost from that source                               |
| Lookup time complexity | O(1) average                                                                                                    |
| Why O(1) lookup is possible | Python dictionaries use hash tables, so values can usually be found instantly using their key without searching |

### Part 2c: Precomputation Complexity
- **Number of Dijkstra runs:** _k + 1 (one per relic, plus one from spawn)_
- **Cost per run:** _O(m log n), where m = |E| and n = |V|_
- **Total complexity:** _O((k + 1) · m log n)_
- **Justification (one line):** _We run Dijkstra once for every k + 1 source node. Each run processes the whole graph and uses heap operations that take O(log n) time._

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means
- **For nodes already finalized (in S):**
  _dist[v] is the actual shortest distance from the source to v. Once a node is
finalized, its value is guaranteed to be correct and will never change, because 
no future path can produce a smaller distance._

- **For nodes not yet finalized (not in S):**
  _dist[u] is the cheapest distance found so far from the source to u using only
finalized nodes as intermediate steps. It may not be the true shortest distance 
yet, but it is the best estimate currently known and could still improve later._

### Part 3b: Why Each Phase Holds
- **Initialization : why the invariant holds before iteration 1:**
- _At the start, S is empty, dist[source] = 0, and all other nodes are set to inf._
- _The source is correct because the distance from the source to itself is 0, and no
other paths have been discovered yet._

- **Maintenance : why finalizing the min-dist node is always correct:**
- _The algorithm picks the non-finalized node u with the smallest tentative distance
and marks it as finalized._
- _Because all edge weights are nonnegative, any other path to u would have to go through
a node that is already the same distance or farther away, so there’s no way to find a
cheaper route later._

- **Termination : what the invariant guarantees when the algorithm ends:**
- _When the heap becomes empty, every reachable node has been finalized._
- _This means dist[v] contains the true shortest-path distance from the source to every
reachable node. Any node still marked as float('inf') was unreachable._

### Part 3c: Why This Matters for the Route Planner
_If any distance in the table were incorrect, the planner could choose a relic order that
only appears optimal, either missing the true cheapest route or selecting a path that
actually costs more fuel._

---

## Part 4: Search Design

### Why Greedy Fails
- **The failure mode:** _A greedy approach always goes to the closest unvisited relic next.
The problem is that picking the cheapest next step doesn’t guarantee the cheapest full route.
A good-looking first move can lead to very expensive later moves._

- **Counter-example setup:** _Using the example with B, C, and D: the distances are
S -> B=1, S -> C=2, S -> D=2; B -> C=100, B -> D=1, B -> T=1; C -> B=1, C -> T=1; D -> B=1, D -> C=1._
- **What greedy picks:** _Greedy starts at S and picks B first since it’s closest (cost 1).
From B it then goes to D (1), then to C (1), and finally to T (1), for a total cost of 4. But
if we change the setup so B->C is very expensive (100), greedy still starts with B and ends up
getting stuck paying that large cost later, making the route much worse._
- **What optimal picks:** _A better route is S->C->B->D->T, which avoids that expensive
connection and gives a lower total cost._
- **Why greedy loses:** _Greedy fails because it only looks at the next cheapest step and
ignores how that choice affects the rest of the journey, and it can’t undo bad early
decisions._

### What the Algorithm Must Explore
- _The algorithm has to try different possible orders of visiting the relics because the total
cost depends on the full route, not just one step at a time, so it has to compare different
sequences to find the cheapest one._

---

## Part 5: State and Search Space

### Part 5a: State Representation
| Component | Variable name in code | Data type           | Description           |
|---|-----------------------|---------------------|-----------------------|
| Current location | current_loc           | node (any hashable) | The dungeon node the Torchbearer is currently standing at  |
| Relics already collected | relics_remaining      | set                 | The set of relic nodes not yet visited; a relic is collected when removed from this set                      |
| Fuel cost so far | cost_so_far           | float               | Total fuel burned along the current path from spawn to current_loc                      |

### Part 5b: Data Structure for Visited Relics
| Property | Your answer                   |
|---|-------------------------------|
| Data structure chosen | set (Python built-in hash set) |
| Operation: check if relic already collected | Time complexity: O(1) average |
| Operation: mark a relic as collected | Time complexity: O(1) average |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) average |
| Why this structure fits | All three operations needed during recursive search (check, mark, unmark) are O(1);sets also make it easy to loop through remaining relics and check when none are left.                              |

### Part 5c: Worst-Case Search Space
- **Worst-case number of orders considered:** _k! (k factorial), where k = |M| = number of relic chambers._
- **Why:** _Without pruning, the algorithm tries every permutation of the k relics. There are k choices for the first relic, k−1 for the second, and so on, giving k x (k−1) x … x 1 = k! distinct orderings in the worst case._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking
- **What is tracked:** _best[0] stores the lowest total fuel cost found so far for a complete route from the spawn, through all relics, to the exit. best[1] stores the relic order for that best route. They are updated whenever the algorithm finds a cheaper complete solution.._
- **When it is used:** _At the start of each recursive call, the algorithm compares the current branch’s lower-bound estimate against best[0]._
- **What it allows the algorithm to skip:** _If the branch’s estimated minimum possible cost is already greater than or equal to best[0], the algorithm stops exploring that branch because it cannot lead to a better solution._

### Part 6b: Lower Bound Estimation
- **What information is available at the current state:** _The algorithm knows the fuel cost so far (cost_so_far), the current location, the remaining relics, and the precomputed shortest distances between important locations._
- **What the lower bound accounts for:** _The estimate includes the current cost so far, the cheapest cost to reach any remaining relic, and the cheapest cost from a remaining relic to the exit. This gives a minimum possible cost to finish the route._
- **Why it never overestimates:** _All values come from the shortest-path distance table, which contains true minimum costs. Since the algorithm always uses the minimum possible values, the estimate can be smaller than the real remaining cost, but never larger._

### Part 6c: Pruning Correctness
- _Pruning is safe because the lower bound never overestimates the true remaining cost, so if a branch could actually lead to a better solution, its estimate would also look better and the branch would not be pruned._
- _Consequently, the algorithm only removes branches that cannot possibly beat the current best solution, so the optimal route is never accidentally discarded._

---

## References
- _Kelania, A. (2025). Geeks For Geeks. https://www.geeksforgeeks.org/python/hash-set-in-python/. I used this to refresh my memory on hash sets in Python for part 5 to make sure I was using it right._
