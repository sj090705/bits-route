# graph_data.py
# Sparse Weighted Undirected Graph
# Nodes : 36 verified campus locations (GPS coordinates)
# Edges : 76 walkable path segments with Haversine-verified distances

# All edge weights are in METRES.
# All coordinates are (latitude, longitude) in decimal degrees.

COORDINATES = {
    "Clock Tower": (28.36412,  75.58704),
    "Meera Bhawan": (28.357125, 75.585593),
    "Ram Bhawan": (28.36230,  75.58636),
    "Budh Bhawan":(28.360722, 75.586769),
    "Krishna Bhawan":(28.362567, 75.588079),
    "Gandhi Bhawan":(28.361026, 75.588324),
    "Shankar Bhawan": (28.359770, 75.588494),
    "Vyas Bhawan":(28.358299, 75.588800),
    "Saraswati Temple":(28.358129, 75.587979),
    "Bhagirath Bhawan":(28.361138, 75.589277),
    "Vishwakarma Bhawan": (28.362687, 75.589040),
    "CVR Bhawan":(28.361886, 75.590986),
    "Malviya Bhawan": (28.361601, 75.585337),
    "Srinivasa Bhawan": (28.365601, 75.587347),
    "PIEDS":(28.36616,  75.58771),
    "Library":(28.365336, 75.588434),
    "Rana Pratap Bhawan":(28.362947, 75.590724),
    "Ashok Bhawan":(28.361389, 75.590938),
    "Lecture Theatre Complex":(28.365110, 75.589873),
    "FD1":(28.364287, 75.588781),
    "FD2": (28.363570, 75.587770),
    "FD3":(28.363390, 75.586383),
    "Food Ministry":(28.36489,  75.58826),
    "New Workshop": (28.365325, 75.587931),
    "All Night Canteen":(28.360141, 75.589384),
    "SAC":(28.360670, 75.585770),
    "Akshay Supermarket": (28.357148, 75.589956),
    "Cnot":(28.356218, 75.591457),
    "Looters":(28.361335, 75.585653),
    "BET-TACT": (28.362791, 75.585486),
    "Birla Balika Vidyapeeth":(28.359555, 75.586984),
    "Birla Shishu Vihar": (28.35738,  75.58727),
    "NAB": (28.36225,  75.58728),
    "Main Gate": (28.361022, 75.592976),
    "Vfast":(28.360911, 75.592074),
}

# EDGES
# Each tuple: ("Node A", "Node B", distance_in_metres)
# Graph is UNDIRECTED — every edge is traversable in both directions.
# Distances are Haversine-verified straight-line values between GPS coords
EDGES = [
    ("Clock Tower", "FD2", 94.03),
    ("Clock Tower", "FD3", 103.54),

    ("Meera Bhawan", "Birla Shishu Vihar", 166.53),
    ("Birla Shishu Vihar", "Birla Balika Vidyapeeth", 243.46),

    ("Ram Bhawan", "Budh Bhawan", 179.97),
    ("Ram Bhawan", "Krishna Bhawan", 170.80),
    ("Ram Bhawan", "Malviya Bhawan", 126.73),
    ("Ram Bhawan", "FD3", 121.22),
    ("Ram Bhawan", "NAB", 90.19),
    ("Ram Bhawan", "Looters", 127.67),
    ("Ram Bhawan", "BET-TACT", 101.46),

    ("Budh Bhawan", "Gandhi Bhawan", 155.86),
    ("Budh Bhawan", "SAC", 97.92),
    ("Budh Bhawan", "Looters", 128.73),
    ("Budh Bhawan", "Birla Balika Vidyapeeth", 131.46),
    ("Budh Bhawan", "NAB", 177.11),
    ("Budh Bhawan", "Shankar Bhawan", 199.24),

    ("Krishna Bhawan", "Gandhi Bhawan", 173.02),
    ("Krishna Bhawan", "Vishwakarma Bhawan", 94.97),
    ("Krishna Bhawan", "FD1", 203.22),
    ("Krishna Bhawan", "FD2", 115.55),
    ("Krishna Bhawan", "NAB", 85.76),

    ("Gandhi Bhawan", "Shankar Bhawan", 140.65),
    ("Gandhi Bhawan", "Bhagirath Bhawan", 94.08),
    ("Gandhi Bhawan", "Vishwakarma Bhawan", 197.54),
    ("Gandhi Bhawan", "All Night Canteen", 142.97),
    ("Gandhi Bhawan", "Birla Balika Vidyapeeth", 209.63),
    ("Gandhi Bhawan", "NAB", 170.17),

    ("Shankar Bhawan", "Vyas Bhawan", 166.29),
    ("Shankar Bhawan", "All Night Canteen", 96.36),
    ("Shankar Bhawan", "Birla Balika Vidyapeeth", 149.67),

    ("Vyas Bhawan", "Saraswati Temple", 82.53),
    ("Vyas Bhawan", "Akshay Supermarket", 170.81),
    ("Vyas Bhawan", "All Night Canteen", 212.64),

    ("Saraswati Temple", "Birla Balika Vidyapeeth", 186.07),
    ("Saraswati Temple", "Birla Shishu Vihar", 108.40),

    ("Bhagirath Bhawan", "Vishwakarma Bhawan", 173.80),
    ("Bhagirath Bhawan", "CVR Bhawan", 186.76),
    ("Bhagirath Bhawan", "Rana Pratap Bhawan", 245.98),
    ("Bhagirath Bhawan", "Ashok Bhawan", 164.90),
    ("Bhagirath Bhawan", "All Night Canteen", 111.35),

    ("Vishwakarma Bhawan", "CVR Bhawan", 210.21),
    ("Vishwakarma Bhawan", "Rana Pratap Bhawan", 167.29),
    ("Vishwakarma Bhawan", "Ashok Bhawan", 235.20),
    ("Vishwakarma Bhawan", "FD1", 179.71),
    ("Vishwakarma Bhawan", "FD2", 158.37),

    ("CVR Bhawan", "Rana Pratap Bhawan", 120.73),
    ("CVR Bhawan", "Ashok Bhawan", 55.46),  # shortest edge

    ("Library", "Lecture Theatre Complex", 143.02),
    ("Library", "FD1", 121.48),
    ("Library", "Food Ministry", 52.43),  # 2nd shortest edge
    ("Library", "PIEDS", 115.82),

    ("Rana Pratap Bhawan", "Lecture Theatre Complex", 254.52),
    ("Rana Pratap Bhawan", "FD1", 241.55),
    ("Rana Pratap Bhawan", "FD2", 297.22),

    ("Malviya Bhawan", "FD3", 223.71),
    ("Malviya Bhawan", "Looters", 42.79),
    ("Malviya Bhawan", "BET-TACT", 133.12),

    ("Srinivasa Bhawan", "PIEDS", 71.59),
    ("Srinivasa Bhawan", "Library", 110.36),
    ("Srinivasa Bhawan", "New Workshop", 64.86),

    ("PIEDS", "Library", 115.82),
    ("PIEDS", "New Workshop", 95.33),

    ("FD3", "BET-TACT", 110.18),

    ("Food Ministry", "New Workshop", 58.10),

    ("Ashok Bhawan", "All Night Canteen", 205.86),

    ("Lecture Theatre Complex", "Food Ministry", 159.71),
    ("Lecture Theatre Complex", "New Workshop", 191.51),

    ("FD1", "FD2", 127.05),
    ("FD1", "Food Ministry", 84.23),
    ("FD1", "New Workshop", 142.26),
    ("FD1", "Lecture Theatre Complex", 140.68),

    ("FD2", "Food Ministry", 154.41),
    ("FD2", "NAB", 154.41),

    ("All Night Canteen", "SAC", 358.49),
    ("All Night Canteen", "Birla Balika Vidyapeeth", 243.71),
    ("All Night Canteen", "Vfast", 276.79),
    ("All Night Canteen", "Akshay Supermarket", 337.48),

    ("Akshay Supermarket", "Cnot", 179.63),

    ("Main Gate", "Vfast", 89.12),
    ("Vfast", "Ashok Bhawan", 123.21),
    ("Vfast", "Cnot", 525.32),
    ("Vfast", "SAC", 617.42),
    ("Ashok Bhawan", "Cnot", 577.23),
    ("SAC", "Looters", 74.83),
]

"""Congestion schedule for L3 
 Format: { time_slot_index: {node_name: k_factor} }
 Time slot index = floor(minutes_since_midnight / 15)
 Slot 0  = 00:00–00:14,  Slot 31 = 07:45–07:59,
 Slot 35 = 08:45–08:59, etc.
 Only non-1.0 slots are listed.  All others default to k = 1.0.
Helper: convert "HH:MM" to slot index"""

def _slot(hhmm: str) -> int:
    h, m = map(int, hhmm.split(":"))
    return (h * 60 + m) // 15

# Zone member lists (used to expand slot entries)
_Z1 = ["LTC", "FD1", "Library", "Food Ministry", "Srinivasa Bhawan","New Workshop", "Vishwakarma Bhawan", "PIEDS", "Lecture Theatre Complex"]
_Z1_ACADEMIC = ["Lecture Theatre Complex", "FD1", "Srinivasa Bhawan", "Vishwakarma Bhawan"]
_Z1_FULL = ["Lecture Theatre Complex", "FD1", "Food Ministry","Srinivasa Bhawan", "Vishwakarma Bhawan","New Workshop", "Library"]

_Z2 = ["NAB", "Clock Tower", "FD2", "FD3", "Krishna Bhawan", "Gandhi Bhawan", "Ram Bhawan", "Budh Bhawan"]

_Z3 = ["Meera Bhawan", "Birla Shishu Vihar","Birla Balika Vidyapeeth", "Saraswati Temple"]

_Z4_EVE = ["Shankar Bhawan", "All Night Canteen", "Akshay Supermarket"]
_Z4_NIGHT = ["All Night Canteen"]

_EXT = ["Bhagirath Bhawan", "Rana Pratap Bhawan","Ashok Bhawan", "CVR Bhawan", "SAC", "Malviya Bhawan", "Looters Truck", "Vfast"]

def _make_slot_entry(nodes, k):
    #Return {node: k} dict for a list of nodes.
    return {n: k for n in nodes}

# Build congestion schedule as {slot_index: {node: k}}
CONGESTION_SCHEDULE: dict[int, dict[str, float]] = {}

def _add_slots(start_hhmm, end_hhmm, nodes, k):
    # Mark every 15-min slot in [start_hhmm, end_hhmm) with congestion k for the given node list.
    s = _slot(start_hhmm)
    e = _slot(end_hhmm)
    entry = _make_slot_entry(nodes, k)
    for idx in range(s, e):
        if idx not in CONGESTION_SCHEDULE:
            CONGESTION_SCHEDULE[idx] = {}
        CONGESTION_SCHEDULE[idx].update(entry)

# 07:45–08:00  morning rush  (Z1 food + Z2 + Z3)
_add_slots("07:45", "08:00", ["FD1", "Food Ministry", "New Workshop","Srinivasa Bhawan", "Vishwakarma Bhawan","Malviya Bhawan"], 2.0)
_add_slots("07:45", "08:00", _Z2 + _Z3, 2.0)

# Classchange rushes (Z1 academic + Z2 + Z3, k=2.5)
for start, end in [("08:45", "09:00"), ("09:45", "10:00"), ("11:45", "12:00"), ("12:45", "13:00"),("14:45", "15:00"), ("15:45", "16:00"), ("16:45", "17:00"), ("17:45", "18:00")]:
    _add_slots(start, end, _Z1_ACADEMIC + ["FD1"], 2.5)
    _add_slots(start, end, _Z2, 2.5)
    _add_slots(start, end, _Z3, 2.0)

_add_slots("10:45", "11:00", ["Lecture Theatre Complex", "FD1","New Workshop", "Vishwakarma Bhawan"], 2.5)
_add_slots("10:45", "11:00", _Z2, 2.5)

# Full Z1 (including FM) for 11:45–, 12:45–, 16:45–, 17:45–
for start, end in [("11:45", "12:00"), ("12:45", "13:00"), ("16:45", "17:00"), ("17:45", "18:00")]:
    _add_slots(start, end, ["Food Ministry"], 2.5)

# 13:45–14:00  postlunch hostel return
_add_slots("13:45", "14:00", ["FD2", "FD3", "NAB"], 1.4)
_add_slots("13:45", "14:00", _Z3, 2.0)
_add_slots("13:45", "14:00", ["Shankar Bhawan"], 1.3)

# Extended Bhawans — same class-change + morning windows
for start, end in [("07:45", "08:00"), ("08:45", "09:00"),("09:45", "10:00"), ("11:45", "12:00"),("12:45", "13:00"), ("13:45", "14:00"), ("14:45", "15:00"), ("15:45", "16:00"),("16:45", "17:00"), ("17:45", "18:00")]:
    _add_slots(start, end, ["Bhagirath Bhawan", "Rana Pratap Bhawan","Ashok Bhawan", "CVR Bhawan"], 2.0)

# 16:45–17:00 and 17:45–18:00  evening rush Z4 + extras
for start, end in [("16:45", "17:00"), ("17:45", "18:00")]:
    _add_slots(start, end, ["Shankar Bhawan", "All Night Canteen","Akshay Supermarket", "SAC","Vfast", "Looters"], 2.0)

# 18:00–19:00  ANC + SAC + Vfast
_add_slots("18:00", "19:00", ["All Night Canteen", "SAC", "Vfast","Looters"], 2.0)

# 20:00–02:00  night canteen light rush
_add_slots("20:00", "02:00", ["All Night Canteen", "Food Ministry", "Looters"], 1.4)

# 21:00–23:00  Cnot light rush  (node not in main edge list — stored anyway)
_add_slots("21:00", "23:00", ["Cnot"], 1.3)


# GRAPH STATISTICS
def _compute_stats():
    from collections import defaultdict
    deg = defaultdict(int)
    for u, v, _ in EDGES:
        deg[u] += 1
        deg[v] += 1
    n = len(COORDINATES)
    e = len(EDGES)
    weights = [w for _, _, w in EDGES]
    isolated = [node for node in COORDINATES if deg[node] == 0]
    return {
        "nodes": n,
        "edges": e,
        "density_pct": round(e / (n * (n - 1) / 2) * 100, 2),
        "min_weight_m": min(weights),
        "max_weight_m": max(weights),
        "avg_weight_m": round(sum(weights) / len(weights), 2),
        "avg_degree": round(2 * e / n, 2),
        "max_degree": max(deg.values()),
        "max_degree_nodes": [k for k, v in deg.items() if v == max(deg.values())],
        "min_degree": min(deg.values()),
        "min_degree_nodes": [k for k, v in deg.items() if v == min(deg.values())],
        "isolated_nodes": isolated,
    }

GRAPH_STATS = _compute_stats()
