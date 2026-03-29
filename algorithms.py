#algorithms.py
import heapq
from collections import deque
from typing import Callable
from dataclasses import dataclass, field
from campus_graph import CampusGraph

@dataclass
class SearchResult:
    algorithm: str
    source: str
    goal:str
    path:list
    cost:float 
    nodes_expanded: int # nodes popped from frontier
    nodes_generated: int # nodes added to frontier
    frontier_log:list = field(default_factory=list)
    found:bool = True


def bfs(graph: CampusGraph, source: str, goal: str) -> SearchResult:
    frontier = deque([(source, [source])])
    visited = {source} # explored set prevents cycles

    nodes_expanded = 0
    nodes_generated = 1 # source is the first generated node
    frontier_log= []

    while frontier:
        node, path = frontier.popleft()
        nodes_expanded += 1

        frontier_log.append({
            "step": nodes_expanded,
            "node": node,
            "g": len(path) - 1, # number of hops so far
            "h":0.0,
            "f": float(len(path) - 1), })

        if node == goal:
            cost = _path_cost(graph, path)
            return SearchResult(algorithm="BFS", source=source, goal=goal,
                path=path, cost=cost, nodes_expanded=nodes_expanded, nodes_generated=nodes_generated, frontier_log=frontier_log,)

        for neighbour, _ in graph.neighbours(node):
            if neighbour not in visited:
                visited.add(neighbour)
                frontier.append((neighbour, path + [neighbour]))
                nodes_generated += 1

    return SearchResult( algorithm="BFS", source=source, goal=goal,path=[], cost=float("inf"),
        nodes_expanded=nodes_expanded,nodes_generated=nodes_generated, frontier_log=frontier_log,found=False, )

def ucs(graph: CampusGraph, source: str, goal: str) -> SearchResult:
 entries: (cumulative_cost, tie_breaker, node, path)
    counter   = 0
    heap      = [(0.0, counter, source, [source])]
    visited   = set()

    nodes_expanded  = 0
    nodes_generated = 1
    frontier_log    = []

    while heap:
        g, _, node, path = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)
        nodes_expanded += 1
        frontier_log.append({
            "step": nodes_expanded,
            "node": node,
            "g": round(g, 2),
            "h": 0.0,
            "f": round(g, 2),
        })

        if node == goal:
            return SearchResult(algorithm="UCS", source=source, goal=goal,path=path, cost=g,
                nodes_expanded=nodes_expanded, nodes_generated=nodes_generated, frontier_log=frontier_log, )

        for neighbour, weight in graph.neighbours(node):
            if neighbour not in visited:
                counter += 1
                heapq.heappush(heap, (g + weight, counter, neighbour, path + [neighbour]))
                nodes_generated += 1

    return SearchResult( algorithm="UCS", source=source, goal=goal, path=[], cost=float("inf"),
        nodes_expanded=nodes_expanded, nodes_generated=nodes_generated, frontier_log=frontier_log, found=False, )

def greedy(graph: CampusGraph, source: str, goal: str, heuristic: str = "haversine") -> SearchResult:
    h_fn = _get_heuristic(graph, heuristic)
    counter  = 0
    heap     = [(h_fn(source, goal), counter, source, [source])]
    visited  = set()
    nodes_expanded  = 0
    nodes_generated = 1
    frontier_log    = []

    while heap:
        h_val, _, node, path = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)
        nodes_expanded += 1

        g_val = _path_cost(graph, path)   # actual cost 
        frontier_log.append({
            "step": nodes_expanded,
            "node": node,
            "g": round(g_val, 2),
            "h": round(h_val, 2),
            "f": round(h_val, 2),   # f = h only for Greedy
        })

        if node == goal:
            return SearchResult(f"Greedy ({heuristic})", source=source, goal=goal, path=path, cost=g_val,
                nodes_expanded=nodes_expanded, nodes_generated=nodes_generated, frontier_log=frontier_log,
            )

        for neighbour, _ in graph.neighbours(node):
            if neighbour not in visited:
                h_nb = h_fn(neighbour, goal)
                counter += 1
                heapq.heappush(heap, (h_nb, counter,  neighbour, path + [neighbour]))
                nodes_generated += 1

    return SearchResult( algorithm=f"Greedy ({heuristic})", source=source, goal=goal, path=[], cost=float("inf"),
        nodes_expanded=nodes_expanded, nodes_generated=nodes_generated, frontier_log=frontier_log, found=False,
    )


def astar(graph: CampusGraph, source: str, goal: str, heuristic: str = "haversine") -> SearchResult:
    h_fn = _get_heuristic(graph, heuristic)
    counter = 0
    start_h = h_fn(source, goal)
    heap = [(start_h, counter, 0.0, source, [source])]
    visited = {} 
    nodes_expanded  = 0
    nodes_generated = 1
    frontier_log    = []

    while heap:
        f, _, g, node, path = heapq.heappop(heap)

        if node in visited and visited[node] <= g:
            continue

        visited[node] = g
        nodes_expanded += 1
        h_val = h_fn(node, goal)
        frontier_log.append({
            "step": nodes_expanded,
            "node": node,
            "g": round(g, 2),
            "h": round(h_val, 2),
            "f": round(f, 2),
        })

        if node == goal:
            return SearchResult(algorithm=f"A* ({heuristic})", source=source, goal=goal, path=path, cost=g,
                nodes_expanded=nodes_expanded, nodes_generated=nodes_generated, frontier_log=frontier_log,
            )

        for neighbour, weight in graph.neighbours(node):
            g_new = g + weight
            if neighbour not in visited or visited[neighbour] > g_new:
                h_nb  = h_fn(neighbour, goal)
                f_new = g_new + h_nb
                counter += 1
                heapq.heappush(heap, (f_new, counter, g_new, neighbour, path + [neighbour]))
                nodes_generated += 1

    return SearchResult( algorithm=f"A* ({heuristic})", source=source, goal=goal, path=[], cost=float("inf"),
        nodes_expanded=nodes_expanded, nodes_generated=nodes_generated, frontier_log=frontier_log, found=False, )

def td_astar(graph: CampusGraph, source: str, goal: str,  departure_hhmm: str = "08:48",
             walking_speed_mps: float = 1.4) -> SearchResult:
  
    start_slot = graph.hhmm_to_slot(departure_hhmm)
    counter = 0
    h0 = graph.h_haversine(source, goal)
    heap = [(h0, counter, 0.0, source, start_slot, [source])]
    visited = {}   
    nodes_expanded  = 0
    nodes_generated = 1
    frontier_log    = []

    while heap:
        f, _, g, node, t_slot, path = heapq.heappop(heap)

        state = (node, t_slot)
        if state in visited and visited[state] <= g:
            continue

        visited[state] = g
        nodes_expanded += 1

        h_val = graph.h_haversine(node, goal)
        frontier_log.append({
            "step":   nodes_expanded,
            "node":   node,
            "t_slot": t_slot,
            "g": round(g, 2),
            "h": round(h_val, 2),
            "f": round(f, 2),
        })

        if node == goal:
            return SearchResult(algorithm=f"TD-A* (depart {departure_hhmm})",source=source, goal=goal, path=path, cost=g,
                nodes_expanded=nodes_expanded, nodes_generated=nodes_generated,  frontier_log=frontier_log,
            )

        for neighbour, _ in graph.neighbours(node):
            w   = graph.w_eff(node, neighbour, t_slot)
            g_new = g + w

            travel_slots = max(1, int(w / (walking_speed_mps * 15 * 60)))
            t_new = min(t_slot + travel_slots, 95)   

            new_state = (neighbour, t_new)
            if new_state not in visited or visited[new_state] > g_new:
                h_nb  = graph.h_haversine(neighbour, goal)
                f_new = g_new + h_nb
                counter += 1
                heapq.heappush(heap, (f_new, counter, g_new,neighbour, t_new, path + [neighbour]))
                nodes_generated += 1

    return SearchResult(algorithm=f"TD-A* (depart {departure_hhmm})",source=source, goal=goal,path=[], cost=float("inf"),
        nodes_expanded=nodes_expanded,nodes_generated=nodes_generated,frontier_log=frontier_log, found=False,)


def _get_heuristic(graph: CampusGraph,  name: str) -> Callable[[str, str], float]:
    if name == "haversine":
        return graph.h_haversine
    elif name == "euclidean":
        return graph.h_euclidean  
    else:
        raise ValueError(f"Unknown heuristic '{name}'. ")


def _path_cost(graph: CampusGraph, path: list[str]) -> float:
    return sum(
        next(w for nb, w in graph.neighbours(path[i]) if nb == path[i + 1])
        for i in range(len(path) - 1)
    )
