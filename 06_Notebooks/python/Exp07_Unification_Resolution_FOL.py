"""Experiment 7: Unification and Resolution in First-Order Logic
Aim: Implement the unification algorithm (with occurs check) and a resolution refutation prover for first-order clauses; prove classic textbook theorems.
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


def is_var(t): return isinstance(t, str) and t.startswith("?")
def walk(t, th):
    while is_var(t) and t in th: t = th[t]
    return t
def occurs(v, t, th):
    t = walk(t, th)
    if t == v: return True
    return isinstance(t, tuple) and any(occurs(v, a, th) for a in t[1:])
def unify(x, y, th=None):
    if th is None: th = {}
    x, y = walk(x, th), walk(y, th)
    if x == y: return th
    if is_var(x): return None if occurs(x, y, th) else {**th, x: y}
    if is_var(y): return unify(y, x, th)
    if isinstance(x, tuple) and isinstance(y, tuple) and x[0] == y[0] and len(x) == len(y):
        for a, b in zip(x[1:], y[1:]):
            th = unify(a, b, th)
            if th is None: return None
        return th
    return None
def resolve_term(t, th):
    t = walk(t, th)
    return (t[0],) + tuple(resolve_term(a, th) for a in t[1:]) if isinstance(t, tuple) else t
def show(t):
    if isinstance(t, tuple): return f"{t[0]}({', '.join(show(a) for a in t[1:])})"
    return t.lstrip("?")
def show_th(th): return "{" + ", ".join(f"{k.lstrip('?')}/{show(resolve_term(v, th))}" for k, v in th.items()) + "}" if th is not None else "FAIL"

tests = [(("Knows","John","?x"), ("Knows","John","Jane")),
         (("Knows","John","?x"), ("Knows","?y","Bill")),
         (("Knows","John","?x"), ("Knows","?y",("Mother","?y"))),
         (("Knows","John","?x"), ("Knows","?x","Elizabeth")),
         (("P","?x",("f","?y")), ("P","a",("f",("g","?z")))),
         (("Q","?x"), ("Q",("f","?x")))]
for a, b in tests: print(f"UNIFY({show(a):<22}, {show(b):<26}) = {show_th(unify(a, b))}")

import itertools
def neg(l): return l[1] if l[0] == "not" else ("not", l)
def subst_lit(l, th): return ("not", resolve_term(l[1], th)) if l[0] == "not" else resolve_term(l, th)
cid = itertools.count()
def standardise(clause):
    k = next(cid); m = {}
    def rn(t):
        if is_var(t): m.setdefault(t, f"{t}{k}"); return m[t]
        return (t[0],) + tuple(rn(a) for a in t[1:]) if isinstance(t, tuple) else t
    return frozenset(("not", rn(l[1])) if l[0] == "not" else rn(l) for l in clause)
def resolvents(c1, c2):
    out = []
    for l1 in c1:
        for l2 in c2:
            if (l1[0] == "not") != (l2[0] == "not"):
                a, b = (l1[1], l2) if l1[0] == "not" else (l1, l2[1])
                th = unify(a, b)
                if th is not None:
                    new = frozenset(subst_lit(l, th) for l in (c1 - {l1}) | (c2 - {l2}))
                    out.append((new, th, l1, l2))
    return out
def prove(kb, goal, max_iter=2000):
    clauses = [standardise(c) for c in kb] + [standardise([neg(goal)])]
    names = {c: f"C{i+1}" for i, c in enumerate(clauses)}; steps = []; seen = set(clauses)
    for _ in range(max_iter):
        new = []
        for c1, c2 in itertools.combinations(list(seen), 2):
            for r, th, l1, l2 in resolvents(c1, c2):
                if r in seen or r in [n for n, *_ in new]: continue
                new.append((r, c1, c2, th))
                if not r:
                    steps.append((r, c1, c2, th)); return True, steps, names
        if not new: return False, steps, names
        for r, c1, c2, th in sorted(new, key=lambda x: len(x[0]))[:30]:
            seen.add(r); names[r] = f"C{len(names)+1}"; steps.append((r, c1, c2, th))
    return False, steps, names
def cs(c): return " ∨ ".join(("¬" + show(l[1])) if l[0] == "not" else show(l) for l in sorted(c, key=str)) or "□"

# Example 1 — Socrates
KB1 = [[("not", ("Man","?x")), ("Mortal","?x")], [("Man","Socrates")]]
ok, st, nm = prove(KB1, ("Mortal","Socrates"))
print("KB: ∀x Man(x) ⇒ Mortal(x);  Man(Socrates)   Goal: Mortal(Socrates)")
for r, c1, c2, th in st: print(f"   resolve [{cs(c1)}] with [{cs(c2)}]  ⟹  {cs(r)}")
print("Proved!" if ok else "Not proved")

# Example 2 — Colonel West (Russell & Norvig 9.3)
KB2 = [
 [("not",("American","?x")),("not",("Weapon","?y")),("not",("Sells","?x","?y","?z")),("not",("Hostile","?z")),("Criminal","?x")],
 [("not",("Missile","?x")),("not",("Owns","Nono","?x")),("Sells","West","?x","Nono")],
 [("not",("Missile","?x")),("Weapon","?x")],
 [("not",("Enemy","?x","America")),("Hostile","?x")],
 [("Owns","Nono","M1")],[("Missile","M1")],[("American","West")],[("Enemy","Nono","America")]]
ok, st, nm = prove(KB2, ("Criminal","West"))
print("Goal: Criminal(West) →", "PROVED ✓" if ok else "not proved", f"after generating {len(st)} resolvents")
chain = []
r = st[-1]
print("Final step:", f"[{cs(r[1])}] + [{cs(r[2])}] ⟹ {cs(r[0])}")

# Visualise the Socrates refutation as a proof tree
fig, ax = plt.subplots(figsize=(7.5, 4)); ax.axis("off")
boxes = {"C1": (0.15, 0.85, "¬Man(x) ∨ Mortal(x)"), "C3": (0.62, 0.85, "¬Mortal(Socrates)  [negated goal]"),
         "R1": (0.38, 0.5, "¬Man(Socrates)   θ={x/Socrates}"), "C2": (0.85, 0.5, "Man(Socrates)"), "R2": (0.6, 0.12, "□  (empty clause)")}
for k, (x, y, t) in boxes.items():
    ax.text(x, y, t, ha="center", va="center", fontsize=12, color="white" if k.startswith("R") else NAVY,
            bbox=dict(boxstyle="round,pad=0.5", fc=NAVY if k.startswith("R") else GOLDL, ec=GOLD, lw=2))
for a, b in (("C1","R1"),("C3","R1"),("R1","R2"),("C2","R2")):
    ax.annotate("", xy=boxes[b][:2], xytext=boxes[a][:2], arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2, shrinkA=18, shrinkB=18))
ax.set_title("Resolution refutation proof of Mortal(Socrates)")
plt.savefig(f"{FIG}/exp07_resolution_tree.png", dpi=130, bbox_inches="tight"); plt.show()
