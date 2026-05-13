# The Torchbearer

**Student Name:** Rachel Rogers
**Student ID:** 133560411
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting. 

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

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

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| _Spawn (entrance) S_ | _The Torchbearer departs from here, so we need the cheapest cost from S to every relic and to the exit._ |
| _Each relic chamber Ri_ | _After picking up a relic, the Torchbearer travels from that relic to another relic or to the exit, so we need distances from every relic too._ |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer                                                                                                     |
|---|-----------------------------------------------------------------------------------------------------------------|
| Data structure name | Nested dictionary (dict[node, dict[node, float]])                                                               |
| What the keys represent | A source node (spawn or a relic) that Dijkstra was run from                                                     |
| What the values represent | A dictionary mapping every graph node to its minimum travel cost from that source                               |
| Lookup time complexity | O(1) average                                                                                                    |
| Why O(1) lookup is possible | Python dictionaries use hash tables, so values can usually be found instantly using their key without searching |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** _k + 1 (one per relic, plus one from spawn)_
- **Cost per run:** _O(m log n), where m = |E| and n = |V|_
- **Total complexity:** _O((k + 1) · m log n)_
- **Justification (one line):** _We run Dijkstra once for every k + 1 source node. Each run processes the whole graph and uses heap operations that take O(log n) time._

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  _dist[v] is the actual shortest distance from the source to v. Once a node is
finalized, its value is guaranteed to be correct and will never change, because 
no future path can produce a smaller distance._

- **For nodes not yet finalized (not in S):**
  _dist[u] is the cheapest distance found so far from the source to u using only
finalized nodes as intermediate steps. It may not be the true shortest distance 
yet, but it is the best estimate currently known and could still improve later._

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

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

> One sentence connecting correct distances to correct routing decisions.

_If any distance in the table were incorrect, the planner could choose a relic order that
only appears optimal, either missing the true cheapest route or selecting a path that
actually costs more fuel._

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

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

> One bullet. Must use the word "order."

- _The algorithm has to try different possible orders of visiting the relics because the total
cost depends on the full route, not just one step at a time, so it has to compare different
sequences to find the cheapest one._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
