"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Rachel Rogers
Student ID:   133560411

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq

# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
    return (
        "Why a single shortest-path run from S is not enough: "
        "Running Dijkstra once from S can find the cheapest path to each location on its own, but it "
        "can’t figure out the best order to visit multiple relic chambers. For example, going to R1 before "
        "R2 might cost less overall than going to R2 before R1, and a single run doesn’t compare those "
        "possibilities.\n\n"

        "What decision remains after all inter-location costs are known: "
        "Even after we know the cheapest travel cost between every important location, we still have "
        "to decide the best order to collect the relics before finally heading to the exit. \n\n"

        "Why this requires a search over orders: "
        "Since the total fuel cost changes depending on the order the relics are visited, the engine has "
        "to check different possible orders to find the cheapest overall route."
    )

# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Return the list of nodes from which Dijkstra must be run.

    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    The exit_node is never a departure point (the journey ends there),
    so it is not included as a source.
    Duplicates removed using dict.fromkeys.
    """
    candidates = [spawn] + list(relics)
    # dict.fromkeys removes duplicates (preserves insertion order)
    return list(dict.fromkeys(candidates))


def run_dijkstra(graph, source):
    """
    Compute single-source shortest-path distances using a min-heap.

    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    Standard min-heap Dijkstra. Each heap entry is (tentative_cost, node).
    A node is "finalized" the first time it is popped from the heap,
    because all edge weights are nonnegative (so no later path can be
    cheaper than the one that reached it with the minimum tentative cost).
    Heap entries for already-finalized nodes are skipped.
    """
    # Initialize every node to infinity; source costs zero to reach itself.
    dist = {node: float('inf') for node in graph}
    dist[source] = 0

    # Min-heap: (cost, node)
    heap = [(0, source)]

    while heap:
        cost_u, u = heapq.heappop(heap)

        # Skip stale entries: a cheaper path to u was already finalized.
        if cost_u > dist[u]:
            continue

        # Relax all outgoing edges from u.
        for v, edge_cost in graph[u]:
            new_cost = dist[u] + edge_cost
            if new_cost < dist[v]:
                dist[v] = new_cost
                heapq.heappush(heap, (new_cost, v))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Build the complete distance table used by the route-search engine.

    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    Runs one Dijkstra per source node returned by select_sources and
    stores the full distance dictionary keyed by that source.
    Total cost: O((k+1) * (m log n)) where k = |relics|.
    """
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    for src in sources:
        dist_table[src] = run_dijkstra(graph, src)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """

    return (
        "Part 3a: What the Invariant Means"
        "For nodes already finalized (in S): "
        "dist[v] is the actual shortest distance from the source to v. Once a node is "
        "finalized, its value is guaranteed to be correct and will never change, because "
        "no future path can produce a smaller distance.\n\n"
        
        "For nodes not yet finalized (not in S): "
        "dist[u] is the cheapest distance found so far from the source to u using only "
        "finalized nodes as intermediate steps. It may not be the true shortest distance "
        "yet, but it is the best estimate currently known and could still improve later.\n\n"
        
        "Part 3b: Why Each Phase Holds "
        "Initialization : why the invariant holds before iteration 1: "
        "- At the start, S is empty, dist[source] = 0, and all other nodes are set to inf. "
        "- The source is correct because the distance from the source to itself is 0, and no "
        "other paths have been discovered yet.\n\n"

        "Maintenance: why finalizing the min-dist node is always correct: "
        "- The algorithm picks the non-finalized node u with the smallest tentative distance "
        "and marks it as finalized."
        "- Because all edge weights are nonnegative, any other path to u would have to go through "
        "a node that is already the same distance or farther away, so there’s no way to find a "
        "cheaper route later.\n\n"

        "Termination: what the invariant guarantees when the algorithm ends: "
        "- When the heap becomes empty, every reachable node has been finalized. "
        "- This means dist[v] contains the true shortest-path distance from the source to every "
        "reachable node. Any node still marked as float('inf') was unreachable.\n\n"

        "Part 3c: Why This Matters for the Route Planner "
        "If any distance in the table were incorrect, the planner could choose a relic order that "
        "only appears optimal, either missing the true cheapest route or selecting a path that "
        "actually costs more fuel."
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """
    return (
        "- The failure mode: A greedy approach always goes to the closest unvisited relic next. "
        "The problem is that picking the cheapest next step doesn’t guarantee the cheapest full route. "
        "A good-looking first move can lead to very expensive later moves.\n\n"
        
        "- Counter-example setup: Using the example with B, C, and D: the distances are "
        "S -> B=1, S -> C=2, S -> D=2; B -> C=100, B -> D=1, B -> T=1; C -> B=1, C -> T=1; D -> B=1, D -> C=1.\n\n"
        
        "- What greedy picks: Greedy starts at S and picks B first since it’s closest (cost 1). "
        "From B it then goes to D (1), then to C (1), and finally to T (1), for a total cost of 4. But "
        "if we change the setup so B->C is very expensive (100), greedy still starts with B and ends up "
        "getting stuck paying that large cost later, making the route much worse.\n\n"
        
        "- What optimal picks: A better route is S->C->B->D->T, which avoids that expensive "
        "connection and gives a lower total cost.\n\n"
        
        "- Why greedy loses: Greedy fails because it only looks at the next cheapest step and "
        "ignores how that choice affects the rest of the journey, and it can’t undo bad early "
        "decisions.\n\n"

### What the Algorithm Must Explore
        "- The algorithm has to try different possible orders of visiting the relics because the total "
        "cost depends on the full route, not just one step at a time, so it has to compare different "
        "sequences to find the cheapest one."
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Find the minimum-fuel route from spawn through all relics to exit_node.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    State representation (see README Part 5a):
      current_loc — node the Torchbearer is currently at
      relics_remaining — set of relic nodes not yet collected
      relics_visited_order — list recording the order relics were collected
      cost_so_far — total fuel burned to reach current_loc
    """
    # best[0] = best fuel cost found so far, best[1] = corresponding relic order
    # A mutable list lets _explore update it without a return value
    best = [float('inf'), []]

    # relics_remaining is a set: O(1) membership test, O(1) add/remove,
    # and O(1) discard for backtracking (see README Part 5b)
    relics_remaining = set(relics)

    _explore(
        dist_table=dist_table,
        current_loc=spawn,
        relics_remaining=relics_remaining,
        relics_visited_order=[],
        cost_so_far=0.0,
        exit_node=exit_node,
        best=best,
    )

    return (best[0], best[1])

def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : set
        - Relic nodes not yet collected (chosen data structure: set)
        - See README Part 5b for complexity
    relics_visited_order : list[node]
        - Relics collected so far, in order they were visited
    cost_so_far : float
        - Total fuel burned to reach current_loc along the current path
    exit_node : node
    best : list
        - best[0] = best fuel cost found so far (float)
        - best[1] = relic visitation order for that best cost (list)

    Returns
    -------
    None
        Updates best in place.
    """

    # Base case
    if not relics_remaining:
        cost_to_exit = dist_table[current_loc][exit_node]
        total_cost = cost_so_far + cost_to_exit
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = list(relics_visited_order)  # snapshot the current order
        return

    """
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    # Pruning: best-so-far + lower-bound check (Part 6).
    # Lower bound: the cheapest this branch can possibly finish is
    # cost_so_far, plus the minimum cost to reach any remaining relic from
    # current_loc, plus the minimum cost from any remaining relic to the exit.
    # Since these values come from shortest-path distances, the estimate
    # can never be higher than the true remaining cost.
    min_to_next = min(dist_table[current_loc][r] for r in relics_remaining)
    min_to_exit = min(dist_table[r][exit_node] for r in relics_remaining)
    lower_bound = cost_so_far + min_to_next + min_to_exit

    # Pruning Safety: We prune only when the lower bound on the total cost
    # of this branch is >= best[0]. Because the lower bound never overestimates
    # the true remaining cost (all values come from exact shortest-path
    # distances), any route that could beat best[0] would produce a lower
    # bound strictly less than best[0] and would not be pruned. So the
    # optimal solution is never discarded.
    if lower_bound >= best[0]:
        return

    # Recursive case
    for next_relic in list(relics_remaining):
        travel_cost = dist_table[current_loc][next_relic]

        # If next_relic is unreachable from current_loc, skip branch
        if travel_cost == float('inf'):
            continue

        # recurse
        relics_remaining.remove(next_relic)  # mark collected
        relics_visited_order.append(next_relic)  # record order

        _explore(
            dist_table=dist_table,
            current_loc=next_relic,
            relics_remaining=relics_remaining,
            relics_visited_order=relics_visited_order,
            cost_so_far=cost_so_far + travel_cost,
            exit_node=exit_node,
            best=best,
        )

        # backtrack
        relics_visited_order.pop()  # unmark order
        relics_remaining.add(next_relic)  # unmark collected

# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        Weighted directed graph as an adjacency list.
    spawn : node
        Starting location (dungeon entrance).
    relics : list[node]
        Relic chambers that must each be visited at least once.
    exit_node : node
        The route must end here (dungeon exit).

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """

    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)

# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
