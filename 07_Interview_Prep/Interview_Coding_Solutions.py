"""26UAMPC204 Artificial Intelligence — 10 solved coding interview problems (2 per unit)."""

# ======================================================================
# C01 (Unit I): 8-puzzle solvability check
# Given a 3×3 8-puzzle state as a tuple (0 = blank), return True if it can reach 1-2-3/4-5-6/7-8-_ . Target: O(n²) or better.
# ======================================================================
def solvable(state):
    tiles = [t for t in state if t != 0]
    inversions = sum(1 for i in range(len(tiles)) for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j])
    return inversions % 2 == 0          # 3x3 board: solvable iff inversions are even

tests = {(1,2,3,4,5,6,7,8,0): True, (1,2,3,4,5,6,8,7,0): False, (1,8,2,0,4,3,7,6,5): True, (8,1,2,0,4,3,7,6,5): False}
for s, exp in tests.items():
    assert solvable(s) == exp
    print(s, "→ solvable" if solvable(s) else "→ NOT solvable")
print("All tests passed ✓")

# ======================================================================
# C02 (Unit I): Water-Jug: minimum steps
# Jugs of capacity a and b litres; return the minimum number of operations to measure exactly t litres in either jug, or −1.
# ======================================================================
from collections import deque
def min_steps(a, b, t):
    start = (0, 0); dist = {start: 0}; q = deque([start])
    while q:
        x, y = q.popleft()
        if x == t or y == t: return dist[(x, y)]
        for n in ((a, y), (x, b), (0, y), (x, 0),
                  (x - min(x, b - y), y + min(x, b - y)), (x + min(y, a - x), y - min(y, a - x))):
            if n not in dist: dist[n] = dist[(x, y)] + 1; q.append(n)
    return -1
for a, b, t in ((4, 3, 2), (5, 3, 4), (6, 4, 1)):
    print(f"jugs ({a},{b}), target {t}: {min_steps(a, b, t)} steps")
assert min_steps(4, 3, 2) == 4 and min_steps(6, 4, 1) == -1
print("All tests passed ✓")

# ======================================================================
# C03 (Unit II): Shortest path in a grid with obstacles
# Grid of 0 (free) and 1 (wall). Return the length of the shortest 4-directional path from top-left to bottom-right, or −1.
# ======================================================================
from collections import deque
def shortest_path(grid):
    R, C = len(grid), len(grid[0])
    if grid[0][0] or grid[R-1][C-1]: return -1
    q, seen = deque([(0, 0, 0)]), {(0, 0)}
    while q:
        r, c, d = q.popleft()
        if (r, c) == (R - 1, C - 1): return d
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and not grid[nr][nc] and (nr, nc) not in seen:
                seen.add((nr, nc)); q.append((nr, nc, d + 1))
    return -1
g = [[0,0,0,0],[1,1,0,1],[0,0,0,0],[0,1,1,0]]
print("Shortest path length:", shortest_path(g))
assert shortest_path(g) == 6 and shortest_path([[0,1],[1,0]]) == -1
print("All tests passed ✓   Complexity: O(R·C) time and space")

# ======================================================================
# C04 (Unit II): Count N-Queens solutions with bitmasks
# Return the number of ways to place N non-attacking queens. Must handle N = 12 quickly.
# ======================================================================
import time
def n_queens(n):
    full = (1 << n) - 1
    def solve(cols, d1, d2):
        if cols == full: return 1
        count, free = 0, full & ~(cols | d1 | d2)
        while free:
            bit = free & -free; free -= bit
            count += solve(cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1)
        return count
    return solve(0, 0, 0)
for n in (4, 6, 8, 10, 12):
    t = time.time(); print(f"N={n:>2}: {n_queens(n):>6} solutions  ({time.time()-t:.3f}s)")
assert n_queens(8) == 92
print("All tests passed ✓")

# ======================================================================
# C05 (Unit III): Propositional entailment by model checking
# Given a KB and a query as Python functions over a model, decide whether KB ⊨ query and return a counter-model if not.
# ======================================================================
import itertools
def entails(symbols, kb, query):
    for vals in itertools.product([False, True], repeat=len(symbols)):
        m = dict(zip(symbols, vals))
        if kb(m) and not query(m): return False, m
    return True, None
S = ["Rain", "Sprinkler", "Wet"]
KB = lambda m: (not m["Rain"] or m["Wet"]) and (not m["Sprinkler"] or m["Wet"]) and (m["Rain"] or m["Sprinkler"])
print("KB ⊨ Wet ?  ", entails(S, KB, lambda m: m["Wet"]))
print("KB ⊨ Rain ? ", entails(S, KB, lambda m: m["Rain"]))
assert entails(S, KB, lambda m: m["Wet"])[0] and not entails(S, KB, lambda m: m["Rain"])[0]
print("All tests passed ✓")

# ======================================================================
# C06 (Unit III): Unification with occurs check
# Implement unify(x, y) for terms written as nested tuples; variables start with '?'. Return the substitution or None.
# ======================================================================
def is_var(t): return isinstance(t, str) and t.startswith("?")
def walk(t, s):
    while is_var(t) and t in s: t = s[t]
    return t
def occurs(v, t, s):
    t = walk(t, s)
    return t == v or (isinstance(t, tuple) and any(occurs(v, a, s) for a in t[1:]))
def unify(x, y, s=None):
    s = {} if s is None else s
    x, y = walk(x, s), walk(y, s)
    if x == y: return s
    if is_var(x): return None if occurs(x, y, s) else {**s, x: y}
    if is_var(y): return unify(y, x, s)
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y) and x[0] == y[0]:
        for a, b in zip(x[1:], y[1:]):
            s = unify(a, b, s)
            if s is None: return None
        return s
    return None
print(unify(("Knows", "John", "?x"), ("Knows", "?y", ("Mother", "?y"))))
print(unify(("P", "?x"), ("P", ("f", "?x"))))        # occurs check → None
assert unify(("P", "?x"), ("P", ("f", "?x"))) is None
print("All tests passed ✓")

# ======================================================================
# C07 (Unit IV): Naïve Bayes spam filter from scratch
# Train a multinomial Naïve Bayes classifier with Laplace smoothing on a tiny corpus and classify new messages.
# ======================================================================
import math
from collections import Counter
train = [("win cash prize now", "spam"), ("limited offer win free", "spam"), ("free cash claim now", "spam"),
         ("meeting at ten tomorrow", "ham"), ("lab report due tomorrow", "ham"), ("lunch at canteen today", "ham")]
classes = {"spam", "ham"}
prior = {c: sum(1 for _, y in train if y == c) / len(train) for c in classes}
counts = {c: Counter(w for x, y in train if y == c for w in x.split()) for c in classes}
vocab = {w for x, _ in train for w in x.split()}
def predict(msg):
    scores = {}
    for c in classes:
        total = sum(counts[c].values())
        scores[c] = math.log(prior[c]) + sum(math.log((counts[c][w] + 1) / (total + len(vocab))) for w in msg.split())
    return max(scores, key=scores.get), scores
for m in ("claim your free prize", "report meeting tomorrow"):
    label, sc = predict(m); print(f"{m!r:28} → {label}   (log-scores: {', '.join(f'{k}={v:.2f}' for k, v in sc.items())})")
assert predict("claim your free prize")[0] == "spam" and predict("report meeting tomorrow")[0] == "ham"
print("All tests passed ✓")

# ======================================================================
# C08 (Unit IV): Bayes' rule calculator with sequential evidence
# Write posterior(prior, sensitivity, false_positive_rate) and apply it twice for two independent positive tests.
# ======================================================================
def posterior(prior, sens, fpr):
    return sens * prior / (sens * prior + fpr * (1 - prior))
p1 = posterior(0.001, 0.99, 0.01); p2 = posterior(p1, 0.99, 0.01)
print(f"After 1 positive test: {p1:.3%}")
print(f"After 2 positive tests: {p2:.3%}")
assert abs(p1 - 0.0902) < 1e-3
print("All tests passed ✓   Lesson: low base rates dominate a single test")

# ======================================================================
# C09 (Unit V): Entropy and information gain
# Given labels and a candidate attribute, compute entropy and information gain from scratch; verify on Play Tennis (Outlook).
# ======================================================================
from collections import Counter
from math import log2
def entropy(labels):
    n = len(labels); return -sum(c / n * log2(c / n) for c in Counter(labels).values())
def info_gain(values, labels):
    n = len(labels); rem = 0.0
    for v in set(values):
        sub = [l for x, l in zip(values, labels) if x == v]; rem += len(sub) / n * entropy(sub)
    return entropy(labels) - rem
outlook = "S S O R R R O S S R S O O R".split()
play    = "N N Y Y Y N Y N Y Y Y Y Y N".split()
print(f"H(Play) = {entropy(play):.3f}   Gain(Outlook) = {info_gain(outlook, play):.3f}")
assert round(info_gain(outlook, play), 3) == 0.247
print("All tests passed ✓")

# ======================================================================
# C10 (Unit V): Intent classifier with a confidence fallback
# Build a small chatbot intent classifier (TF-IDF + logistic regression) that returns a fallback when confidence is low.
# ======================================================================
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
X = ["what are the fees", "fee structure please", "how much does it cost", "tuition amount",
     "am i eligible", "eligibility criteria", "minimum marks needed", "is jee required",
     "hostel facility", "is accommodation available", "where will i stay", "hostel rooms",
     "placement record", "which companies visit", "average salary package", "job opportunities"]
y = ["fees"] * 4 + ["eligibility"] * 4 + ["hostel"] * 4 + ["placement"] * 4
clf = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(C=20, max_iter=1000)).fit(X, y)
def answer(q, threshold=0.40):
    probs = clf.predict_proba([q])[0]; i = probs.argmax()
    label = str(clf.classes_[i]) if probs[i] >= threshold else "fallback"
    return label, round(float(probs[i]), 2)
for q in ("what is the fee", "do you have hostel rooms", "companies for placement", "tell me a joke"):
    print(f"{q!r:30} → {answer(q)}")
assert answer("what is the fee")[0] == "fees" and answer("tell me a joke")[0] == "fallback"
print("All tests passed ✓")
