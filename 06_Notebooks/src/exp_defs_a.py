"""Experiments 1–5: search, games and CSPs."""

EXP1 = dict(num=1, slug="BFS_DFS_WaterJug_8Puzzle", co="CO204.1",
title="Uninformed Search — BFS and DFS",
aim="Implement Breadth-First Search and Depth-First Search to solve the Water-Jug problem and the 8-puzzle, and compare nodes expanded, path length and memory.",
theory="""**State space.** A problem is defined by an initial state, actions, a transition model, a goal test and path cost.
**BFS** expands the shallowest node first using a FIFO queue — complete and optimal for unit costs, but needs $O(b^d)$ memory.
**DFS** expands the deepest node first using a LIFO stack — needs only $O(bm)$ memory but is neither complete (in infinite spaces) nor optimal.
**Water-Jug (4 L, 3 L):** state $(x,y)$; actions fill, empty and pour; goal $x=2$.""",
algorithm=["Put the start node in the frontier (queue for BFS / stack for DFS) and mark it reached.",
"Pop a node; if it satisfies the goal test, reconstruct the path through parent links.",
"Otherwise generate successors; push every successor not yet reached and record its parent.",
"Repeat until the goal is found or the frontier is empty."],
cells=[
("md", "### 1. Water-Jug problem formulation"),
("code", r'''from collections import deque

CAP = (4, 3)            # jug capacities
START, GOAL_X = (0, 0), 2

def successors(s):
    x, y = s; A, B = CAP
    moves = {
        "Fill 4L":  (A, y), "Fill 3L": (x, B),
        "Empty 4L": (0, y), "Empty 3L": (x, 0),
        "Pour 4→3": (x - min(x, B - y), y + min(x, B - y)),
        "Pour 3→4": (x + min(y, A - x), y - min(y, A - x)),
    }
    return [(a, n) for a, n in moves.items() if n != s]

def is_goal(s): return s[0] == GOAL_X
print("Successors of (0,0):", successors((0, 0)))'''),
("md", "### 2. Generic BFS and DFS with statistics"),
("code", r'''def search(start, succ, goal, strategy="BFS", limit=10**6):
    frontier = deque([start]); parent = {start: (None, None)}
    order, max_frontier = [], 1
    while frontier:
        s = frontier.popleft() if strategy == "BFS" else frontier.pop()
        order.append(s)
        if goal(s):
            path, acts = [s], []
            while parent[path[-1]][0] is not None:
                p, a = parent[path[-1]]; acts.append(a); path.append(p)
            return path[::-1], acts[::-1], order, max_frontier
        for a, n in succ(s):
            if n not in parent:
                parent[n] = (s, a); frontier.append(n)
        max_frontier = max(max_frontier, len(frontier))
        if len(order) > limit: break
    return None, None, order, max_frontier

for strat in ("BFS", "DFS"):
    path, acts, order, mf = search(START, successors, is_goal, strat)
    print(f"\n{strat}: path length = {len(path)-1}, nodes expanded = {len(order)}, max frontier = {mf}")
    for s, a in zip(path, ["Start"] + acts):
        print(f"   {a:<9} → {s}")'''),
("md", "### 3. Animated BFS over the Water-Jug state space"),
("code", r'''import networkx as nx
G = nx.DiGraph()
for x in range(5):
    for y in range(4):
        for a, n in successors((x, y)): G.add_edge((x, y), n)
reach = nx.descendants(G, START) | {START}
H = G.subgraph(reach)
pos = {n: (n[0] * 1.4, n[1] * 1.2) for n in H.nodes}
_, _, bfs_order, _ = search(START, successors, is_goal, "BFS")

fig, ax = plt.subplots(figsize=(7.5, 5))
def frame(k):
    ax.clear(); seen = set(bfs_order[:k + 1])
    cols = [GOLD if n == bfs_order[k] else (TEAL if n in seen else MIST) for n in H.nodes]
    nx.draw_networkx_edges(H, pos, ax=ax, edge_color="#C8D0DC", arrows=True, arrowsize=8, width=0.8)
    nx.draw_networkx_nodes(H, pos, ax=ax, node_color=cols, edgecolors=NAVY, node_size=900)
    nx.draw_networkx_labels(H, pos, ax=ax, labels={n: f"{n[0]},{n[1]}" for n in H.nodes}, font_size=9, font_family="serif")
    ax.set_title(f"BFS step {k+1}: expanding {bfs_order[k]}", color=NAVY); ax.axis("off")
anim = animation.FuncAnimation(fig, frame, frames=len(bfs_order))
gif = save_gif(anim, "exp01_bfs_waterjug.gif", fps=1.5)
display(Image(filename=gif))'''),
("md", "### 4. 8-puzzle with BFS and (depth-limited) DFS"),
("code", r'''GOAL8 = (1, 2, 3, 4, 5, 6, 7, 8, 0)
def succ8(s):
    i = s.index(0); r, c = divmod(i, 3); out = []
    for a, dr, dc in (("Up", -1, 0), ("Down", 1, 0), ("Left", 0, -1), ("Right", 0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr * 3 + nc; t = list(s); t[i], t[j] = t[j], t[i]; out.append((a, tuple(t)))
    return out
rng8 = np.random.default_rng(11); start8, prev = GOAL8, None
for _ in range(9):                     # scramble the goal with 9 random non-reversing moves
    opts = [n for a, n in succ8(start8) if n != prev]; prev, start8 = start8, opts[rng8.integers(len(opts))]
print("Start state:", start8)
p, a, o, mf = search(start8, succ8, lambda s: s == GOAL8, "BFS")
print("BFS  : moves =", a, "| expanded =", len(o), "| max frontier =", mf)
p2, a2, o2, mf2 = search(start8, succ8, lambda s: s == GOAL8, "DFS", limit=20000)
print("DFS  :", "gave up after" if p2 is None else f"path length {len(p2)-1},", f"{len(o2):,} expansions (DFS wanders deep — not optimal)")

def show(s, ax, title):
    ax.imshow(np.zeros((3, 3)), cmap="Greys", vmin=0, vmax=1)
    for k, v in enumerate(s):
        r, c = divmod(k, 3)
        ax.add_patch(plt.Rectangle((c - .45, r - .45), .9, .9, color=NAVY if v else "white", ec=GOLD, lw=2))
        if v: ax.text(c, r, v, ha="center", va="center", color=GOLD, fontsize=20, weight="bold")
    ax.set_title(title, fontsize=11); ax.axis("off")
fig, axs = plt.subplots(1, len(p), figsize=(2.1 * len(p), 2.4))
for ax, s, t in zip(axs, p, ["Start"] + a): show(s, ax, t)
plt.tight_layout(); plt.savefig(f"{FIG}/exp01_8puzzle_path.png", dpi=130); plt.show()'''),
("md", "### 5. Comparison"),
("code", r'''import pandas as pd
rows = []
for strat in ("BFS", "DFS"):
    pth, _, od, mfr = search(START, successors, is_goal, strat)
    rows.append([strat, len(pth) - 1, len(od), mfr])
df = pd.DataFrame(rows, columns=["Strategy", "Path length", "Nodes expanded", "Max frontier"])
print(df.to_string(index=False))
ax = df.set_index("Strategy")[["Path length", "Nodes expanded", "Max frontier"]].plot.bar(color=[NAVY, GOLD, TEAL], figsize=(6, 3.5), rot=0)
ax.set_title("Water-Jug: BFS vs DFS"); plt.tight_layout(); plt.savefig(f"{FIG}/exp01_compare.png", dpi=130); plt.show()'''),
],
conclusion="Both strategies solved the Water-Jug problem in 6 moves, but only BFS guarantees the shortest solution. On the scrambled 8-puzzle BFS found the optimal path while DFS wandered thousands of nodes deep without returning a short solution. BFS suits shallow solutions; DFS suits tight memory.",
viva=["Why is BFS optimal only when all step costs are equal?", "What is the space complexity of DFS and why is it smaller than BFS?",
"How do you detect that an 8-puzzle state is unsolvable?", "What is the difference between tree search and graph search?",
"Why does the Water-Jug state graph contain cycles?"])

EXP2 = dict(num=2, slug="AStar_8Puzzle_Route", co="CO204.2",
title="A* Search with Admissible Heuristics",
aim="Implement A* search with admissible heuristics for the 8-puzzle (misplaced tiles, Manhattan distance) and for a grid shortest-route problem, and compare with uniform-cost search.",
theory="""A* expands the node with the smallest $f(n)=g(n)+h(n)$. If $h$ is **admissible** ($h\\le h^*$) tree-A* is optimal; if $h$ is **consistent** graph-A* is optimal.
For the 8-puzzle, $h_1$ = misplaced tiles and $h_2$ = Manhattan distance; $h_2$ dominates $h_1$, so it expands fewer nodes. With $h=0$, A* reduces to uniform-cost search.""",
algorithm=["Insert start with g = 0 and f = h(start) into a priority queue.",
"Pop the node with the lowest f; if it is the goal, return the path.",
"For each successor compute g' = g + step cost; if g' improves the best known g, record parent and push with f = g' + h.",
"Repeat until goal popped or queue empty."],
cells=[
("code", r'''import heapq, itertools, time
GOAL8 = (1, 2, 3, 4, 5, 6, 7, 8, 0)
def succ8(s):
    i = s.index(0); r, c = divmod(i, 3)
    for a, dr, dc in (("Up", -1, 0), ("Down", 1, 0), ("Left", 0, -1), ("Right", 0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr * 3 + nc; t = list(s); t[i], t[j] = t[j], t[i]; yield a, tuple(t), 1

def h0(s): return 0
def h1(s): return sum(1 for k, v in enumerate(s) if v and v != GOAL8[k])
def h2(s):
    d = 0
    for k, v in enumerate(s):
        if v: gr, gc = divmod(v - 1, 3); r, c = divmod(k, 3); d += abs(r - gr) + abs(c - gc)
    return d

def astar(start, succ, goal, h):
    tie = itertools.count(); frontier = [(h(start), next(tie), start)]
    g = {start: 0}; parent = {start: None}; expanded = 0
    while frontier:
        f, _, s = heapq.heappop(frontier)
        if f > g[s] + h(s): continue
        expanded += 1
        if goal(s):
            path = [s]
            while parent[path[-1]]: path.append(parent[path[-1]][0])
            return path[::-1], g[s], expanded
        for a, n, c in succ(s):
            ng = g[s] + c
            if ng < g.get(n, float("inf")):
                g[n] = ng; parent[n] = (s, a); heapq.heappush(frontier, (ng + h(n), next(tie), n))
    return None, None, expanded

start = (7, 2, 4, 5, 0, 6, 8, 3, 1)   # Russell & Norvig Fig. 3.25 start state
print("h1(start) =", h1(start), "  h2(start) =", h2(start))'''),
("code", r'''import pandas as pd
res = []
for name, h in (("UCS (h=0)", h0), ("A* h1 misplaced", h1), ("A* h2 Manhattan", h2)):
    t = time.time(); path, cost, exp = astar(start, succ8, lambda s: s == GOAL8, h)
    res.append([name, cost, exp, round(time.time() - t, 2)])
df = pd.DataFrame(res, columns=["Algorithm", "Solution cost", "Nodes expanded", "Time (s)"])
print(df.to_string(index=False))
fig, ax = plt.subplots(figsize=(6.5, 3.5))
ax.barh(df["Algorithm"], df["Nodes expanded"], color=[SLATE, GOLD, NAVY]); ax.set_xscale("log")
for i, v in enumerate(df["Nodes expanded"]): ax.text(v, i, f"  {v:,}", va="center", color=NAVY)
ax.set_title("Nodes expanded (log scale) — better heuristic, less work"); ax.invert_yaxis()
plt.tight_layout(); plt.savefig(f"{FIG}/exp02_heuristics.png", dpi=130); plt.show()'''),
("md", "### Shortest route on a grid map with obstacles — animated A*"),
("code", r'''rng = np.random.default_rng(7)
N = 20; grid = (rng.random((N, N)) < 0.25).astype(int)
S, T = (0, 0), (N - 1, N - 1); grid[S] = grid[T] = 0
def gsucc(p):
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        r, c = p[0] + dr, p[1] + dc
        if 0 <= r < N and 0 <= c < N and not grid[r, c]: yield "m", (r, c), 1
def manh(p): return abs(p[0] - T[0]) + abs(p[1] - T[1])

def astar_trace(h):
    tie = itertools.count(); fr = [(h(S), next(tie), S)]; g = {S: 0}; par = {S: None}; closed = []
    while fr:
        f, _, s = heapq.heappop(fr)
        if s in closed: continue
        closed.append(s)
        if s == T: break
        for _, n, c in gsucc(s):
            if g[s] + c < g.get(n, 1e9): g[n] = g[s] + c; par[n] = s; heapq.heappush(fr, (g[n] + h(n), next(tie), n))
    path = [T]
    while par.get(path[-1]): path.append(par[path[-1]])
    return closed, path[::-1]
closed_a, path_a = astar_trace(manh)
closed_u, path_u = astar_trace(lambda p: 0)
print(f"A*  : expanded {len(closed_a)} cells, path length {len(path_a)-1}")
print(f"UCS : expanded {len(closed_u)} cells, path length {len(path_u)-1}")

fig, ax = plt.subplots(figsize=(5.5, 5.5))
step = max(1, len(closed_a) // 30)
frames = list(range(0, len(closed_a), step)) + [len(closed_a)] * 4
def draw(k):
    ax.clear(); img = np.ones((N, N, 3))
    img[grid == 1] = matplotlib.colors.to_rgb(NAVY)
    for (r, c) in closed_a[:k]: img[r, c] = matplotlib.colors.to_rgb(GOLDL)
    if k >= len(closed_a):
        for (r, c) in path_a: img[r, c] = matplotlib.colors.to_rgb(GOLD)
    img[S] = matplotlib.colors.to_rgb(LEAF); img[T] = matplotlib.colors.to_rgb(CRIMSON)
    ax.imshow(img); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"A* (Manhattan): {min(k, len(closed_a))} cells expanded")
gif = save_gif(animation.FuncAnimation(fig, draw, frames=frames), "exp02_astar_grid.gif", fps=4)
display(Image(filename=gif))'''),
],
conclusion="All three searches return the optimal 20-move 8-puzzle solution, but A* with Manhattan distance expands orders of magnitude fewer nodes than UCS. On the grid, A* explores far fewer cells than UCS while returning a path of the same optimal length.",
viva=["Prove that the Manhattan distance heuristic is admissible.", "What is meant by one heuristic dominating another?",
"When does A* become uniform-cost search?", "What happens to A* if the heuristic overestimates?",
"Define consistency and explain why it implies admissibility."])

EXP3 = dict(num=3, slug="HillClimbing_BestFirst", co="CO204.2",
title="Hill Climbing and Greedy Best-First Search",
aim="Implement steepest-ascent hill climbing (with random restarts) for the 8-queens problem and Greedy Best-First Search for a route problem; study local maxima and success rates.",
theory="""**Hill climbing** keeps one current state and moves to the best neighbour while it improves the objective. It can get stuck at **local maxima**, **plateaux** and **ridges**; **random restarts** make it complete with probability approaching 1.
**Greedy Best-First Search** expands the node with the lowest $h(n)$ — fast, but not optimal.
For 8-queens, the objective counts attacking pairs $h$ (goal $h=0$).""",
algorithm=["Start from a random complete state.", "Evaluate all neighbours (move one queen within its column).",
"If the best neighbour is not better than the current state, stop (local optimum).", "Otherwise move to it and repeat; on failure, restart from a new random state."],
cells=[
("code", r'''rng = np.random.default_rng(42)
def attacks(s):
    n = len(s); return sum(1 for i in range(n) for j in range(i + 1, n) if s[i] == s[j] or abs(s[i] - s[j]) == j - i)
def hill_climb(n=8, max_steps=100):
    s = list(rng.integers(0, n, n)); trace = [s[:]]
    for _ in range(max_steps):
        cur = attacks(s); best, best_s = cur, None
        for col in range(n):
            for row in range(n):
                if row != s[col]:
                    t = s[:]; t[col] = row; v = attacks(t)
                    if v < best: best, best_s = v, t
        if best_s is None: break
        s = best_s; trace.append(s[:])
    return s, attacks(s), trace

wins, steps = 0, []
for trial in range(500):
    s, h, tr = hill_climb()
    wins += (h == 0); steps.append(len(tr) - 1)
print(f"Steepest-ascent success rate on 8-queens: {wins/500:.1%} (textbook ≈ 14%)   mean steps = {np.mean(steps):.1f}")'''),
("code", r'''def restart_hc(n=8):
    restarts = 0
    while True:
        s, h, tr = hill_climb(n)
        if h == 0: return s, restarts, tr
        restarts += 1
sol, r, trace = restart_hc()
sol = [int(v) for v in sol]; trace = [[int(v) for v in t] for t in trace]
print("Solution:", sol, "found after", r, "random restarts;  attacking pairs =", attacks(sol))

def board(ax, s, title):
    n = len(s)
    ax.imshow([[(i + j) % 2 for j in range(n)] for i in range(n)], cmap=matplotlib.colors.ListedColormap([MIST, "#C8D0DC"]))
    for c, r in enumerate(s): ax.text(c, r, "♛", ha="center", va="center", fontsize=24, fontfamily="DejaVu Sans", color=NAVY if attacks(s) else LEAF)
    ax.set_title(title); ax.set_xticks([]); ax.set_yticks([])
fig, ax = plt.subplots(figsize=(4.5, 4.8))
gif = save_gif(animation.FuncAnimation(fig, lambda k: (ax.clear(), board(ax, trace[min(k, len(trace)-1)], f"Step {min(k, len(trace)-1)}: h = {attacks(trace[min(k, len(trace)-1)])}")),
                frames=len(trace) + 3), "exp03_hill_climbing_queens.gif", fps=1.5)
display(Image(filename=gif))'''),
("code", r'''hs = [attacks(t) for t in trace]
plt.figure(figsize=(6, 3.2)); plt.plot(hs, "-o", color=NAVY, mfc=GOLD, ms=8)
plt.xlabel("step"); plt.ylabel("attacking pairs h"); plt.title("Hill climbing descends h to 0 (successful run)")
plt.tight_layout(); plt.savefig(f"{FIG}/exp03_hc_curve.png", dpi=130); plt.show()'''),
("md", "### Greedy Best-First Search on the Romania map (straight-line-distance heuristic)"),
("code", r'''roads = {("Arad","Zerind"):75,("Arad","Sibiu"):140,("Arad","Timisoara"):118,("Zerind","Oradea"):71,("Oradea","Sibiu"):151,
 ("Timisoara","Lugoj"):111,("Lugoj","Mehadia"):70,("Mehadia","Drobeta"):75,("Drobeta","Craiova"):120,("Craiova","Rimnicu"):146,
 ("Craiova","Pitesti"):138,("Sibiu","Fagaras"):99,("Sibiu","Rimnicu"):80,("Rimnicu","Pitesti"):97,("Fagaras","Bucharest"):211,
 ("Pitesti","Bucharest"):101,("Bucharest","Giurgiu"):90,("Bucharest","Urziceni"):85}
G = {}
for (a, b), d in roads.items(): G.setdefault(a, {})[b] = d; G.setdefault(b, {})[a] = d
SLD = {"Arad":366,"Bucharest":0,"Craiova":160,"Drobeta":242,"Fagaras":176,"Giurgiu":77,"Lugoj":244,"Mehadia":241,
       "Oradea":380,"Pitesti":100,"Rimnicu":193,"Sibiu":253,"Timisoara":329,"Urziceni":80,"Zerind":374}
def best_first(start, goal, f):
    import heapq
    fr = [(f(start, 0), start, 0, [start])]; seen = set(); order = []
    while fr:
        _, n, g, path = heapq.heappop(fr)
        if n in seen: continue
        seen.add(n); order.append(n)
        if n == goal: return path, g, order
        for m, d in G[n].items(): heapq.heappush(fr, (f(m, g + d), m, g + d, path + [m]))
gp, gc, go = best_first("Arad", "Bucharest", lambda n, g: SLD[n])
ap, ac, ao = best_first("Arad", "Bucharest", lambda n, g: g + SLD[n])
print("Greedy best-first:", " → ".join(gp), f"= {gc} km   (expanded {len(go)})")
print("A*               :", " → ".join(ap), f"= {ac} km   (expanded {len(ao)})")'''),
],
conclusion="Plain steepest-ascent hill climbing solves only about one in seven 8-queens instances because it halts at local minima of h; random restarts always reach a solution. Greedy best-first reaches Bucharest quickly (450 km) but A* finds the optimal 418 km route.",
viva=["Why does hill climbing get stuck? Name three landscape features responsible.", "How does random-restart hill climbing achieve completeness?",
"Why is greedy best-first search not optimal? Give the Romania counter-example.", "What is the difference between hill climbing and simulated annealing?",
"What objective function did you use for 8-queens, and what is its maximum value?"])

EXP4 = dict(num=4, slug="Minimax_AlphaBeta_TicTacToe", co="CO204.2",
title="Game Playing — Minimax with Alpha–Beta Pruning",
aim="Implement an unbeatable Tic-Tac-Toe player using Minimax and Alpha–Beta pruning, and measure how many nodes pruning saves.",
theory="""In a two-player zero-sum game, **Minimax** backs up utilities: MAX takes the maximum and MIN the minimum of child values.
**Alpha–Beta** keeps $\\alpha$ (best value for MAX) and $\\beta$ (best value for MIN) and prunes a subtree as soon as $\\alpha\\ge\\beta$. It returns exactly the same decision as Minimax; with perfect ordering, time drops from $O(b^m)$ to $O(b^{m/2})$.""",
algorithm=["If the state is terminal, return its utility (+1 X wins, −1 O wins, 0 draw).",
"MAX node: for each move, v = max(v, MIN-VALUE(child, α, β)); if v ≥ β prune; α = max(α, v).",
"MIN node: for each move, v = min(v, MAX-VALUE(child, α, β)); if v ≤ α prune; β = min(β, v).",
"At the root choose the move with the best backed-up value."],
cells=[
("code", r'''import math
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def winner(b):
    for i, j, k in LINES:
        if b[i] != " " and b[i] == b[j] == b[k]: return b[i]
    return "D" if " " not in b else None
def moves(b): return [i for i, v in enumerate(b) if v == " "]
def play(b, i, p): t = list(b); t[i] = p; return "".join(t)
def utility(w): return {"X": 1, "O": -1, "D": 0}[w]

counter = {"n": 0}
def minimax(b, player):
    counter["n"] += 1; w = winner(b)
    if w: return utility(w), None
    best = (-math.inf, None) if player == "X" else (math.inf, None)
    for m in moves(b):
        v, _ = minimax(play(b, m, player), "O" if player == "X" else "X")
        if (player == "X" and v > best[0]) or (player == "O" and v < best[0]): best = (v, m)
    return best

def alphabeta(b, player, a=-math.inf, be=math.inf):
    counter["n"] += 1; w = winner(b)
    if w: return utility(w), None
    best_m = None
    if player == "X":
        v = -math.inf
        for m in moves(b):
            val, _ = alphabeta(play(b, m, "X"), "O", a, be)
            if val > v: v, best_m = val, m
            a = max(a, v)
            if a >= be: break
    else:
        v = math.inf
        for m in moves(b):
            val, _ = alphabeta(play(b, m, "O"), "X", a, be)
            if val < v: v, best_m = val, m
            be = min(be, v)
            if a >= be: break
    return v, best_m

empty = " " * 9
counter["n"] = 0; v1, m1 = minimax(empty, "X"); n1 = counter["n"]
counter["n"] = 0; v2, m2 = alphabeta(empty, "X"); n2 = counter["n"]
print(f"Minimax    : value {v1}, best first move {m1}, nodes = {n1:,}")
print(f"Alpha-Beta : value {v2}, best first move {m2}, nodes = {n2:,}")
print(f"Pruning saved {100*(1-n2/n1):.1f}% of the nodes — same decision, value 0 means perfect play is a draw.")'''),
("code", r'''fig, ax = plt.subplots(figsize=(6, 3.4))
ax.bar(["Minimax", "Alpha–Beta"], [n1, n2], color=[SLATE, GOLD], edgecolor=NAVY)
for i, v in enumerate([n1, n2]): ax.text(i, v, f"{v:,}", ha="center", va="bottom", color=NAVY, weight="bold")
ax.set_ylabel("nodes generated"); ax.set_title("Tic-Tac-Toe from the empty board")
plt.tight_layout(); plt.savefig(f"{FIG}/exp04_nodes.png", dpi=130); plt.show()'''),
("md", "### Self-play: two perfect players (animated)"),
("code", r'''b, p, history = empty, "X", [empty]
while not winner(b):
    _, m = alphabeta(b, p); b = play(b, m, p); history.append(b); p = "O" if p == "X" else "X"
print("Final board:"); [print(" " + " | ".join(b[r*3:r*3+3])) for r in range(3)]
print("Result:", {"D": "Draw", "X": "X wins", "O": "O wins"}[winner(b)])

fig, ax = plt.subplots(figsize=(4, 4.3))
def drawb(k):
    s = history[min(k, len(history) - 1)]; ax.clear(); ax.set_xlim(0, 3); ax.set_ylim(0, 3); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 3, 3, color=NAVY))
    for t in (1, 2): ax.plot([t, t], [0, 3], color=GOLD, lw=3); ax.plot([0, 3], [t, t], color=GOLD, lw=3)
    for i, v in enumerate(s):
        if v != " ": ax.text(i % 3 + .5, 2.5 - i // 3, v, ha="center", va="center", fontsize=40, weight="bold", color="white" if v == "X" else GOLD)
    ax.set_title(f"Move {min(k, len(history)-1)}")
gif = save_gif(animation.FuncAnimation(fig, drawb, frames=len(history) + 2), "exp04_tictactoe_selfplay.gif", fps=1)
display(Image(filename=gif))'''),
],
conclusion="Minimax and Alpha–Beta choose the same optimal move and agree that perfect play leads to a draw, but Alpha–Beta generates only a small fraction of the nodes. Self-play between two optimal players ends in a draw.",
viva=["What are α and β and when is a branch pruned?", "Does alpha–beta pruning ever change the Minimax decision? Why?",
"How does move ordering affect the effectiveness of pruning?", "Why is full Minimax infeasible for chess?",
"What is an evaluation function and when is it used?"])

EXP5 = dict(num=5, slug="CSP_NQueens_MapColour_Sudoku", co="CO204.2",
title="Constraint Satisfaction — N-Queens, Map Colouring and Sudoku",
aim="Solve CSPs (N-Queens, map colouring of Australia and Sudoku) using backtracking search enhanced with MRV, forward checking and AC-3.",
theory="""A CSP is $\\langle X,D,C\\rangle$. **Backtracking** assigns one variable at a time and undoes an assignment when a variable has no legal value.
Heuristics: **MRV** (choose the variable with fewest legal values), **LCV**, **forward checking**. **AC-3** enforces arc consistency by deleting unsupported values.""",
algorithm=["If the assignment is complete, return it.", "Select an unassigned variable (MRV).",
"For each value consistent with the assignment: assign it, run forward checking/AC-3, recurse.",
"If recursion fails, undo the assignment and try the next value; if none remain, backtrack."],
cells=[
("code", r'''def nqueens(n):
    sol, trace, calls = [], [], [0]
    def ok(col, row):
        return all(r != row and abs(r - row) != col - c for c, r in enumerate(sol))
    def bt(col):
        calls[0] += 1
        if col == n: return True
        for row in range(n):
            if ok(col, row):
                sol.append(row); trace.append(sol[:])
                if bt(col + 1): return True
                sol.pop(); trace.append(sol[:])
        return False
    bt(0); return sol, trace, calls[0]
sol, trace, calls = nqueens(8)
print("8-Queens solution (row of queen in each column):", sol, "| recursive calls:", calls, "| board states:", len(trace))
for n in (4, 6, 8, 10, 12):
    s, t, c = nqueens(n); print(f"  n={n:>2}: first solution {s}  calls={c}")'''),
("code", r'''fig, ax = plt.subplots(figsize=(4.5, 4.8))
keep = trace[::max(1, len(trace)//40)] + [trace[-1]] * 4
def drawq(k):
    s = keep[k]; ax.clear(); n = 8
    ax.imshow([[(i + j) % 2 for j in range(n)] for i in range(n)], cmap=matplotlib.colors.ListedColormap([MIST, "#C8D0DC"]))
    for c, r in enumerate(s): ax.text(c, r, "♛", ha="center", va="center", fontsize=24, fontfamily="DejaVu Sans", color=LEAF if len(s) == 8 else NAVY)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title(f"Backtracking: {len(s)} queens placed")
gif = save_gif(animation.FuncAnimation(fig, drawq, frames=len(keep)), "exp05_nqueens_backtracking.gif", fps=4)
display(Image(filename=gif))'''),
("md", "### Map colouring of Australia — backtracking + MRV + forward checking"),
("code", r'''NB = {"WA":["NT","SA"],"NT":["WA","SA","Q"],"SA":["WA","NT","Q","NSW","V"],"Q":["NT","SA","NSW"],"NSW":["Q","SA","V"],"V":["SA","NSW"],"T":[]}
COLS = ["red", "green", "blue"]
def colour(assign, domains, log):
    if len(assign) == len(NB): return assign
    var = min((v for v in NB if v not in assign), key=lambda v: (len(domains[v]), -len(NB[v])))   # MRV + degree
    for val in domains[var]:
        new_d = {k: list(d) for k, d in domains.items()}; new_d[var] = [val]; ok = True
        for nb in NB[var]:
            if nb not in assign and val in new_d[nb]:
                new_d[nb].remove(val); ok &= bool(new_d[nb])   # forward checking
        if ok:
            log.append(f"{var} = {val}"); r = colour({**assign, var: val}, new_d, log)
            if r: return r
            log.append(f"backtrack on {var}")
    return None
log = []; res = colour({}, {v: COLS[:] for v in NB}, log)
print("Assignment order:", " → ".join(log)); print("Solution:", res)'''),
("code", r'''import networkx as nx
pos = {"WA":(0,1.2),"NT":(1.3,2),"SA":(1.6,0.9),"Q":(2.8,2),"NSW":(3,0.8),"V":(2.5,-0.2),"T":(2.7,-1.2)}
Gm = nx.Graph([(a, b) for a in NB for b in NB[a]]); Gm.add_node("T")
pal = {"red": CRIMSON, "green": LEAF, "blue": NAVY2}
plt.figure(figsize=(5.5, 4.2))
nx.draw(Gm, pos, with_labels=True, node_color=[pal[res[n]] for n in Gm.nodes], node_size=1700, font_color="white",
        font_weight="bold", font_family="serif", edge_color=GOLD, width=2.5)
plt.title("Australia map colouring — constraint graph"); plt.savefig(f"{FIG}/exp05_map_colouring.png", dpi=130, bbox_inches="tight"); plt.show()'''),
("md", "### Sudoku with AC-3 + backtracking"),
("code", r'''PUZ = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
cells = [(r, c) for r in range(9) for c in range(9)]
peers = {x: {y for y in cells if y != x and (y[0] == x[0] or y[1] == x[1] or (y[0]//3, y[1]//3) == (x[0]//3, x[1]//3))} for x in cells}
def ac3(D):
    q = [(x, y) for x in cells for y in peers[x]]
    while q:
        x, y = q.pop()
        if len(D[y]) == 1 and D[y][0] in D[x]:
            D[x] = [v for v in D[x] if v != D[y][0]]
            if not D[x]: return False
            q.extend((z, x) for z in peers[x] if z != y)
    return True
def solve(D, stats):
    if not ac3(D): return None
    if all(len(d) == 1 for d in D.values()): return D
    x = min((c for c in cells if len(D[c]) > 1), key=lambda c: len(D[c]))
    for v in D[x]:
        stats[0] += 1; E = {k: list(d) for k, d in D.items()}; E[x] = [v]
        r = solve(E, stats)
        if r: return r
    return None
D0 = {(r, c): [int(PUZ[r*9+c])] if PUZ[r*9+c] != "0" else list(range(1, 10)) for r, c in cells}
D1 = {k: list(v) for k, v in D0.items()}; ac3(D1)
print("Unknown cells before AC-3:", sum(len(v) > 1 for v in D0.values()), "| after AC-3 alone:", sum(len(v) > 1 for v in D1.values()))
stats = [0]; S = solve(D0, stats); print("Guesses needed by backtracking:", stats[0])
fig, ax = plt.subplots(figsize=(4.6, 4.6)); ax.set_xlim(0, 9); ax.set_ylim(0, 9); ax.axis("off")
for (r, c), v in S.items():
    given = PUZ[r*9+c] != "0"
    ax.add_patch(plt.Rectangle((c, 8 - r), 1, 1, color=GOLDL if given else "white", ec="#C8D0DC"))
    ax.text(c + .5, 8.5 - r, v[0], ha="center", va="center", fontsize=15, color=NAVY if given else TEAL, weight="bold" if given else "normal")
for t in range(0, 10, 3): ax.plot([t, t], [0, 9], color=NAVY, lw=2.5); ax.plot([0, 9], [t, t], color=NAVY, lw=2.5)
ax.set_title("Sudoku solved (givens shaded)")
HARD = "800000000003600000070090200050007000000045700000100030001000068008500010090000400"   # 'world's hardest' (Inkala)
Dh = {(r, c): [int(HARD[r*9+c])] if HARD[r*9+c] != "0" else list(range(1, 10)) for r, c in cells}
Dh1 = {k: list(v) for k, v in Dh.items()}; ac3(Dh1)
st2 = [0]; Sh = solve(Dh, st2)
print(f"Hard puzzle: unknown after AC-3 = {sum(len(v) > 1 for v in Dh1.values())}, backtracking guesses = {st2[0]}")
print("Hard puzzle first row solved:", [Sh[(0, c)][0] for c in range(9)]); plt.savefig(f"{FIG}/exp05_sudoku.png", dpi=130, bbox_inches="tight"); plt.show()'''),
],
conclusion="Backtracking finds the first 8-queens solution in about a hundred recursive calls; MRV with forward checking colours Australia without any backtracking; AC-3 alone solves an easy Sudoku, while the 'hardest' Sudoku additionally needs backtracking guesses guided by MRV.",
viva=["Define a CSP with its three components for map colouring.", "What is the MRV heuristic and why is it called fail-first?",
"Differentiate forward checking from arc consistency.", "What is the complexity of AC-3?",
"Why is Tasmania irrelevant in the Australia map-colouring problem?"])
