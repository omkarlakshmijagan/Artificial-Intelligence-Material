"""Experiment 3: Hill Climbing and Greedy Best-First Search
Aim: Implement steepest-ascent hill climbing (with random restarts) for the 8-queens problem and Greedy Best-First Search for a route problem; study local maxima and success rates.
26UAMPC204 Artificial Intelligence Lab, Sanjivani University
"""

# ---- Course style (navy & gold, Times) -------------------------------------
import os, warnings
warnings.filterwarnings("ignore")
import numpy as np
import matplotlib
matplotlib.use("Agg")  # figures/GIFs are saved to assets/
import matplotlib.pyplot as plt
from matplotlib import animation
display = Image = lambda *a, **k: None

NAVY, NAVY2, GOLD, GOLDL = "#0B1F4B", "#1F3A7A", "#C9A227", "#F6EBC8"
TEAL, CRIMSON, LEAF, MIST, SLATE = "#0E7C86", "#A4243B", "#2E7D32", "#EEF2F8", "#4A5568"
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "axes.edgecolor": SLATE, "axes.titleweight": "bold", "axes.titlecolor": NAVY,
    "axes.titlesize": 14, "axes.labelcolor": NAVY, "figure.dpi": 110,
    "axes.spines.top": False, "axes.spines.right": False,
})
FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "figures");    os.makedirs(FIG, exist_ok=True)
ANI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "animations"); os.makedirs(ANI, exist_ok=True)

def save_gif(anim, name, fps=2):
    path = os.path.join(ANI, name)
    anim.save(path, writer=animation.PillowWriter(fps=fps))
    plt.close("all")
    return path
print("Environment ready  ✓  numpy", np.__version__, "| matplotlib", matplotlib.__version__)


rng = np.random.default_rng(42)
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
print(f"Steepest-ascent success rate on 8-queens: {wins/500:.1%} (textbook ≈ 14%)   mean steps = {np.mean(steps):.1f}")

def restart_hc(n=8):
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
print('animation saved:', gif)

hs = [attacks(t) for t in trace]
plt.figure(figsize=(6, 3.2)); plt.plot(hs, "-o", color=NAVY, mfc=GOLD, ms=8)
plt.xlabel("step"); plt.ylabel("attacking pairs h"); plt.title("Hill climbing descends h to 0 (successful run)")
plt.tight_layout(); plt.savefig(f"{FIG}/exp03_hc_curve.png", dpi=130); plt.show()

roads = {("Arad","Zerind"):75,("Arad","Sibiu"):140,("Arad","Timisoara"):118,("Zerind","Oradea"):71,("Oradea","Sibiu"):151,
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
print("A*               :", " → ".join(ap), f"= {ac} km   (expanded {len(ao)})")
