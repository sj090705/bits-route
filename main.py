import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from campus_graph import CampusGraph
from algorithms import bfs, ucs, greedy, astar, td_astar
from visualisation import (draw_graph, plot_comparison, plot_empirical_vs_theory,draw_multistop,)
from empirical_validation import run_valid, THEORY

OUT = "outputs"
os.makedirs(OUT, exist_ok=True)

def p(t=""): print(t)
def bar(title): print(f"\n{'='*(len(title)+4)}\n  {title}\n{'='*(len(title)+4)}")
def div(): print("  " + "-"*60)

def pick_node(graph, prompt):
    nodes = sorted(graph.nodes)
    p("\n  Locations:")
    for i, n in enumerate(nodes, 1):
        p(f"    {i:>3}.  {n}")

    while True:
        raw = input(f"\n  {prompt} (number or name): ").strip()
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(nodes):
                p(f"  > {nodes[idx]}")
                return nodes[idx]
            p(f"  Enter 1-{len(nodes)}")
            continue

        # exact match 
        exact = next((n for n in nodes if n.lower() == raw.lower()), None)
        if exact:
            p(f"  > {exact}")
            return exact

        #  substring match 
        hits = [n for n in nodes if raw.lower() in n.lower()]
        if len(hits) == 1:
            p(f"  > {hits[0]}")
            return hits[0]
        elif len(hits) > 1:
            p(f"  Ambiguous -- matches: {', '.join(hits)}")
        else:
            p(f"  No match for '{raw}'. Try again.")

def pick_time():
    while True:
        raw = input("\n  Departure time HH:MM [Enter = 09:00]: ").strip()
        if raw == "":
            p("  > 09:00")
            return "09:00"
        if re.fullmatch(r"\d{2}:\d{2}", raw):
            hh, mm = int(raw[:2]), int(raw[3:])
            if 0 <= hh <= 23 and 0 <= mm <= 59:
                p(f"  > {raw}")
                return raw
        p("  Use format HH:MM, e.g. 08:30")

def advance_time(hhmm, metres, speed_mpm=80.0):
    hh, mm = int(hhmm[:2]), int(hhmm[3:])
    total_min = int(hh * 60 + mm + metres / speed_mpm)  
    return f"{(total_min // 60) % 24:02d}:{total_min % 60:02d}"

def run_leg(graph, src, dst, dep_time):
    return td_astar(graph, src, dst, departure_hhmm=dep_time)

def run_route(graph, stops, dep_time):
    legs, full_path, total_cost, total_hops, times = [], [], 0.0, 0, []
    t = dep_time

    for i in range(len(stops) - 1):
        src, dst = stops[i], stops[i + 1]
        times.append(t)
        res = run_leg(graph, src, dst, t)
        legs.append(res)

        if res.path:
            full_path += res.path if not full_path else res.path[1:]
            total_cost += res.cost
            total_hops += len(res.path) - 1
            t = advance_time(t, res.cost)
        else:
            p(f"  No path found: {src} -> {dst}")

    return {"legs": legs, "times": times, "stops": stops, "full_path": full_path, "total_cost": total_cost,"total_hops": total_hops}

def print_results(route):
    p()
    for i, (leg, dep) in enumerate(zip(route["legs"], route["times"])):
        src, dst = route["stops"][i], route["stops"][i + 1]
        if not leg.path:
            continue
        arr = advance_time(dep, leg.cost)
        p(f"  Leg {i+1}: {src}  ->  {dst}")
        p(f"    Depart {dep}  |  Arrive ~{arr}  |  "
          f"{leg.cost:.1f} m  |  {len(leg.path)-1} hops  |  "
          f"{leg.nodes_expanded} nodes expanded")
        p(f"    Path : {' -> '.join(leg.path)}")
        div()

    if len(route["legs"]) > 1:
        p(f"  TOTAL  {route['total_cost']:.1f} m  over {route['total_hops']} hops")
        p(f"  Full path: {' -> '.join(route['full_path'])}")

def save_visuals(graph, route, dep_time):
    safe  = dep_time.replace(":", "")
    stops = route["stops"]
    fname_png = f"{OUT}/user_route_{safe}.png"
    if len(route["legs"]) == 1:
        draw_graph(graph, route["legs"][0],title=f"TD-A*: {stops[0]} -> {stops[-1]}  [dep {dep_time}]",save_path=fname_png)
    else:
        draw_multistop(graph, route, title=f"TD-A* Multi-Stop Route  ({len(stops)} stops, dep {dep_time})", save_path=fname_png)
    p(f"  PNG -> {fname_png}")

def interactive(graph):
    nodes = sorted(graph.nodes)
    p("\n  Step 1 - Start location")
    start = pick_node(graph, "Start")

    p("\n  Step 2 - Intermediate stops (press Enter to skip)")
    waypoints = []
    while True:
        raw = input(f"  Add stop {len(waypoints)+1} (or Enter to choose desination): ").strip()
        if raw == "":
            break
        node = None
        if raw.isdigit():
            idx = int(raw) - 1
            node = nodes[idx] if 0 <= idx < len(nodes) else None
        else:
            node = next((n for n in nodes if n.lower() == raw.lower()), None)
            if node is None:
                hits = [n for n in nodes if raw.lower() in n.lower()]
                if len(hits) == 1:
                    node = hits[0]
                elif len(hits) > 1:
                    p(f"  Ambiguous: {', '.join(hits)}")
                    continue
        if node is None:
            p(f"  '{raw}' not found")
            continue
        if node in [start] + waypoints:
            p(f"  {node} is already in the route")
            continue
        waypoints.append(node)
        p(f"  > Added: {node}")

    p("\n  Step 3 - Destination")
    while True:
        dest = pick_node(graph, "Destination")
        if dest not in [start] + waypoints:
            break
        p(" Already in route. Choose a different destination.")

    stops = [start] + waypoints + [dest]
    dep_time = pick_time()

    p()
    div()
    p(f"  Route      : {'  ->  '.join(stops)}")
    p(f"  Departure  : {dep_time}")
    p(f"  Algorithm  : TD-A* (Haversine, time-dependent weights)")
    div()
    if input("  Run? [Y/N]: ").strip().lower() == "n":
        return

    route = run_route(graph, stops, dep_time)
    user_benchmark(graph, stops, dep_time)
    bar("RESULTS")
    print_results(route)
    save_visuals(graph, route, dep_time)

    if input("\n  Plan another route? [Y/N]: ").strip().lower() == "y":
        interactive(graph)

def user_benchmark(graph, stops, dep_time):
    bar("USER ROUTE BENCHMARK")
    SRC, DST = stops[0], stops[-1]
    r_bfs = bfs(graph, SRC, DST)
    r_ucs = ucs(graph, SRC, DST)
    r_gr_h  = greedy(graph, SRC, DST, "haversine")
    r_gr_e  = greedy(graph, SRC, DST, "euclidean")
    r_ah_h  = astar(graph, SRC, DST, "haversine")
    r_ah_e  = astar(graph, SRC, DST, "euclidean")
    r_td  = td_astar(graph, SRC, DST, departure_hhmm=dep_time)
    results = [r_bfs, r_ucs, r_gr_h, r_gr_e, r_ah_h, r_ah_e, r_td]
    for r in results:
        p(f"  {r.algorithm:<25} exp={r.nodes_expanded:>3}  "
          f"cost={r.cost:>8.1f} m  hops={len(r.path)-1}")

    plot_comparison(results, save_path=f"{OUT}/comparison_user.png")
    emp = run_valid(results)
    plot_empirical_vs_theory(
        emp,
        {a: THEORY[a] for a in emp}, save_path=f"{OUT}/empirical_vs_theory_user.png"
    )
    
def main():
    graph = CampusGraph()

    p("\n" + "="*62)
    p("  INTERACTIVE ROUTING  (TD-A* with time-dependent weights)")
    p("="*62)
    interactive(graph)
    p("\n  Goodbye.")

if __name__ == "__main__":
    main()
