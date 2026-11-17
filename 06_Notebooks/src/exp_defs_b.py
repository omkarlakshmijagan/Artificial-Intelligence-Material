"""Experiments 6–10: logic, probability, learning and expert systems."""

EXP6 = dict(num=6, slug="Logic_Facts_Rules_Inference", co="CO204.3",
title="Facts, Rules and Logical Inference",
aim="Represent facts and rules in a knowledge base (Prolog-style, in Python) and answer queries using forward chaining and backward chaining, including a propositional truth-table entailment checker.",
theory="""A **knowledge base** stores facts (ground atoms) and rules (Horn clauses $p_1\\wedge\\dots\\wedge p_n\\Rightarrow q$).
**Forward chaining** fires rules whose premises are satisfied until no new facts appear (data-driven).
**Backward chaining** starts from the query and recursively proves the rule premises (goal-driven, as in Prolog).
**Model checking** decides $KB\\models\\alpha$ by enumerating all truth assignments.""",
algorithm=["Store facts as tuples, e.g. ('parent', 'ram', 'sita'); rules as (head, [body literals]) with variables starting with '?'.",
"Forward chaining: repeatedly unify rule bodies with known facts and add instantiated heads.",
"Backward chaining: to prove a goal, unify it with a fact or a rule head and prove the body recursively.",
"Print the derived facts, query answers and proof traces."],
cells=[
("code", r'''import itertools
FACTS = {("parent","dashrath","ram"), ("parent","dashrath","bharat"), ("parent","ram","luv"), ("parent","ram","kush"),
         ("parent","kaushalya","ram"), ("male","dashrath"), ("male","ram"), ("male","bharat"), ("male","luv"), ("male","kush"),
         ("female","kaushalya"), ("female","sita"), ("parent","sita","luv"), ("parent","sita","kush")}
RULES = [
  (("father","?x","?y"),      [("parent","?x","?y"), ("male","?x")]),
  (("mother","?x","?y"),      [("parent","?x","?y"), ("female","?x")]),
  (("grandparent","?x","?z"), [("parent","?x","?y"), ("parent","?y","?z")]),
  (("sibling","?x","?y"),     [("parent","?p","?x"), ("parent","?p","?y"), ("neq","?x","?y")]),
  (("uncle","?u","?c"),       [("parent","?p","?c"), ("sibling","?u","?p"), ("male","?u")]),
]
def is_var(t): return isinstance(t, str) and t.startswith("?")
def walk(t, th):
    while is_var(t) and t in th: t = th[t]
    return t
def subst(lit, th): return tuple(walk(t, th) for t in lit)
def match(pat, fact, th):
    if len(pat) != len(fact): return None
    th = dict(th)
    for p, f in zip(pat, fact):
        p = th.get(p, p)
        if is_var(p): th[p] = f
        elif p != f: return None
    return th
print(f"KB: {len(FACTS)} facts, {len(RULES)} rules")'''),
("md", "### Forward chaining (data-driven)"),
("code", r'''def forward_chain(facts, rules, verbose=True):
    facts = set(facts); rnd = 0; history = []
    while True:
        rnd += 1; new = set()
        for head, body in rules:
            def sat(i, th):
                if i == len(body): yield th; return
                lit = subst(body[i], th)
                if lit[0] == "neq":
                    if lit[1] != lit[2]: yield from sat(i + 1, th)
                    return
                for f in facts:
                    t2 = match(lit, f, th)
                    if t2 is not None: yield from sat(i + 1, t2)
            for th in sat(0, {}):
                h = subst(head, th)
                if h not in facts: new.add(h)
        if not new: break
        history.append((rnd, sorted(new))); facts |= new
        if verbose: print(f"Round {rnd}: +{len(new)} facts →", ", ".join(f"{p}({', '.join(a)})" for p, *a in sorted(new)))
    return facts, history
ALL, hist = forward_chain(FACTS, RULES)
print("\nGrandparents of luv:", sorted(f[1] for f in ALL if f[0] == "grandparent" and f[2] == "luv"))
print("Uncle of luv       :", sorted(f[1] for f in ALL if f[0] == "uncle" and f[2] == "luv"))'''),
("md", "### Backward chaining (goal-driven, Prolog style) with proof trace"),
("code", r'''counter = itertools.count()
def rename(rule):
    k = next(counter); ren = lambda l: tuple(f"{t}_{k}" if is_var(t) else t for t in l)
    return ren(rule[0]), [ren(b) for b in rule[1]]
def bc(goals, th, depth=0, trace=None):
    if not goals: yield th; return
    g = subst(goals[0], th); rest = goals[1:]
    if g[0] == "neq":
        if g[1] != g[2]: yield from bc(rest, th, depth, trace)
        return
    for f in sorted(FACTS):
        t2 = match(g, f, th)
        if t2 is not None:
            if trace is not None: trace.append("  " * depth + f"✓ fact {f[0]}({', '.join(f[1:])})")
            yield from bc(rest, t2, depth, trace)
    for rule in RULES:
        head, body = rename(rule)
        # unify the renamed rule head with the goal
        t2 = dict(th); ok = True
        for a, b in zip(head, g):
            a, b = walk(a, t2), walk(b, t2)
            if a == b: continue
            if is_var(a): t2[a] = b
            elif is_var(b): t2[b] = a
            else: ok = False; break
        if ok and len(head) == len(g):
            if trace is not None: trace.append("  " * depth + f"→ try rule {rule[0][0]} for {g[0]}({', '.join(g[1:])})")
            yield from bc(body + rest, t2, depth + 1, trace)
def ask(q):
    tr = []; sols = []
    for th in bc([q], {}, 0, tr):
        sols.append(subst(q, th)); break
    return sols, tr
for q in [("grandparent","dashrath","kush"), ("uncle","bharat","luv"), ("mother","sita","kush"), ("father","bharat","luv")]:
    s, tr = ask(q)
    print(f"?- {q[0]}({', '.join(q[1:])}).  →  {'YES' if s else 'NO'}")
s, tr = ask(("uncle","bharat","luv")); print("\nProof trace for uncle(bharat, luv):"); print("\n".join(tr[:14]))'''),
("md", "### Propositional entailment by truth-table model checking"),
("code", r'''import pandas as pd
syms = ["P", "Q", "R"]
KB    = lambda m: (not m["P"] or m["Q"]) and (not m["Q"] or m["R"]) and m["P"]   # P⇒Q, Q⇒R, P
alpha = lambda m: m["R"]
rows = []
for vals in itertools.product([False, True], repeat=3):
    m = dict(zip(syms, vals)); rows.append({**{k: "T" if v else "F" for k, v in m.items()}, "KB": "T" if KB(m) else "F", "alpha": "T" if alpha(m) else "F"})
df = pd.DataFrame(rows); df.columns = ["P", "Q", "R", "KB", "α = R"]; print(df.to_string(index=False))
entails = all(alpha(dict(zip(syms, v))) for v in itertools.product([False, True], repeat=3) if KB(dict(zip(syms, v))))
print("\nKB ⊨ R ?", entails)'''),
("code", r'''import networkx as nx
G = nx.DiGraph(); base = [f for f in FACTS if f[0] == "parent"]
for f in base: G.add_edge(f[1], f[2], kind="parent")
for f in ALL:
    if f[0] in ("grandparent", "uncle"): G.add_edge(f[1], f[2], kind=f[0])
pos = {"dashrath": (0.5, 2), "kaushalya": (2, 2), "ram": (1.2, 1), "bharat": (-0.6, 1), "sita": (2.8, 1), "luv": (0.6, 0), "kush": (2.2, 0)}
fig, ax = plt.subplots(figsize=(7, 5))
def drawkb(k):
    ax.clear(); kinds = ["parent"] + (["grandparent"] if k >= 1 else []) + (["uncle"] if k >= 2 else [])
    cmap = {"parent": SLATE, "grandparent": GOLD, "uncle": CRIMSON}
    es = [(u, v) for u, v, d in G.edges(data=True) if d["kind"] in kinds]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=NAVY, node_size=1400)
    nx.draw_networkx_labels(G, pos, ax=ax, font_color="white", font_family="serif", font_size=9)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=es, edge_color=[cmap[G[u][v]["kind"]] for u, v in es], width=2.2, arrowsize=14,
                           connectionstyle="arc3,rad=0.15", node_size=1400)
    ax.set_xlim(-1.2, 3.4); ax.set_ylim(-0.5, 2.5)
    ax.set_title(["Base facts: parent", "Forward chaining adds grandparent (gold)", "…then uncle (crimson)"][min(k, 2)]); ax.axis("off")
gif = save_gif(animation.FuncAnimation(fig, drawkb, frames=4), "exp06_forward_chaining.gif", fps=0.8)
display(Image(filename=gif))'''),
],
conclusion="Forward chaining derived all father, mother, grandparent, sibling and uncle relations in a few rounds; backward chaining answered individual queries with an explicit proof trace; model checking confirmed that {P⇒Q, Q⇒R, P} entails R.",
viva=["Differentiate forward and backward chaining.", "What is a Horn clause and why is it important for chaining?",
"How does Prolog implement backward chaining?", "What is the complexity of truth-table model checking?",
"Why did we need the 'neq' built-in in the sibling rule?"])

EXP7 = dict(num=7, slug="Unification_Resolution_FOL", co="CO204.3",
title="Unification and Resolution in First-Order Logic",
aim="Implement the unification algorithm (with occurs check) and a resolution refutation prover for first-order clauses; prove classic textbook theorems.",
theory="""**Unification** finds the most general substitution $\\theta$ such that $p\\theta=q\\theta$. The **occurs check** rejects bindings like $x/f(x)$.
**Resolution:** from clauses $(\\ell_1\\vee\\alpha)$ and $(\\neg\\ell_2\\vee\\beta)$ with $\\textsc{Unify}(\\ell_1,\\ell_2)=\\theta$ derive $(\\alpha\\vee\\beta)\\theta$.
To prove $KB\\models q$: add $\\neg q$ to the clause set and derive the empty clause $\\square$.""",
algorithm=["Represent terms as nested tuples: variables are lowercase strings starting with '?'; f(x) is ('f', x).",
"UNIFY(x, y, θ): if equal return θ; if x is a variable bind it (with occurs check); if compound unify arguments pairwise.",
"Convert KB and negated goal into clauses (sets of literals).",
"Repeatedly resolve pairs of clauses; stop when the empty clause appears (proof) or no new clauses (no proof)."],
cells=[
("code", r'''def is_var(t): return isinstance(t, str) and t.startswith("?")
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
for a, b in tests: print(f"UNIFY({show(a):<22}, {show(b):<26}) = {show_th(unify(a, b))}")'''),
("md", "### Resolution refutation prover"),
("code", r'''import itertools
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
print("Proved!" if ok else "Not proved")'''),
("code", r'''# Example 2 — Colonel West (Russell & Norvig 9.3)
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
print("Final step:", f"[{cs(r[1])}] + [{cs(r[2])}] ⟹ {cs(r[0])}")'''),
("code", r'''# Visualise the Socrates refutation as a proof tree
fig, ax = plt.subplots(figsize=(7.5, 4)); ax.axis("off")
boxes = {"C1": (0.15, 0.85, "¬Man(x) ∨ Mortal(x)"), "C3": (0.62, 0.85, "¬Mortal(Socrates)  [negated goal]"),
         "R1": (0.38, 0.5, "¬Man(Socrates)   θ={x/Socrates}"), "C2": (0.85, 0.5, "Man(Socrates)"), "R2": (0.6, 0.12, "□  (empty clause)")}
for k, (x, y, t) in boxes.items():
    ax.text(x, y, t, ha="center", va="center", fontsize=12, color="white" if k.startswith("R") else NAVY,
            bbox=dict(boxstyle="round,pad=0.5", fc=NAVY if k.startswith("R") else GOLDL, ec=GOLD, lw=2))
for a, b in (("C1","R1"),("C3","R1"),("R1","R2"),("C2","R2")):
    ax.annotate("", xy=boxes[b][:2], xytext=boxes[a][:2], arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2, shrinkA=18, shrinkB=18))
ax.set_title("Resolution refutation proof of Mortal(Socrates)")
plt.savefig(f"{FIG}/exp07_resolution_tree.png", dpi=130, bbox_inches="tight"); plt.show()'''),
],
conclusion="The unifier returned the expected MGUs, correctly failed on the clash requiring standardising apart, and the occurs check blocked x/f(x). The resolution prover derived the empty clause for both Mortal(Socrates) and Criminal(West).",
viva=["What is a most general unifier?", "Why is the occurs check needed?", "Why must variables be standardised apart before resolution?",
"What is Skolemisation?", "Why is resolution called refutation-complete?"])

EXP8 = dict(num=8, slug="Bayes_BayesianNetwork_Diagnosis", co="CO204.4",
title="Bayes' Theorem and a Bayesian Network for Diagnosis",
aim="Apply Bayes' theorem to a medical-test diagnosis problem and implement the Burglary–Alarm Bayesian network with exact inference by enumeration and approximate inference by sampling.",
theory="""**Bayes' theorem:** $P(H\\mid E)=\\dfrac{P(E\\mid H)P(H)}{P(E)}$.
A **Bayesian network** is a DAG with a CPT per node; the joint is $\\prod_i P(x_i\\mid parents(X_i))$.
**Enumeration:** $P(X\\mid e)=\\alpha\\sum_y P(X,e,y)$. **Rejection sampling** estimates the same posterior from random samples.""",
algorithm=["Encode priors and conditional probabilities.", "Compute the posterior with Bayes' rule and study how it varies with the prior.",
"Encode the Burglary network CPTs; compute the joint probability of a full assignment.",
"Compute P(Burglary | JohnCalls, MaryCalls) by enumeration and compare with rejection sampling."],
cells=[
("code", r'''def bayes(prior, sens, fpr):
    evidence = sens * prior + fpr * (1 - prior)
    return sens * prior / evidence, evidence
post, ev = bayes(prior=0.01, sens=0.90, fpr=0.05)
print(f"P(+) = {ev:.4f}")
print(f"P(Disease | +) = {post:.4f}  →  only {post:.1%} despite a 90%-sensitive test (base-rate effect)")
post2, _ = bayes(prior=post, sens=0.90, fpr=0.05)
print(f"After a second independent positive test: {post2:.1%}")'''),
("code", r'''priors = np.linspace(0.001, 0.5, 300)
plt.figure(figsize=(6.8, 3.8))
for sens, fpr, c in ((0.90, 0.05, NAVY), (0.99, 0.01, TEAL), (0.80, 0.10, CRIMSON)):
    plt.plot(priors, [bayes(p, sens, fpr)[0] for p in priors], color=c, lw=2.5, label=f"sens={sens}, FPR={fpr}")
plt.axvline(0.01, color=GOLD, ls="--"); plt.text(0.015, 0.05, "prevalence 1%", color=GOLD)
plt.xlabel("prior P(Disease)"); plt.ylabel("posterior P(Disease | +)"); plt.legend(frameon=False); plt.title("Posterior depends strongly on the prior")
plt.tight_layout(); plt.savefig(f"{FIG}/exp08_posterior_vs_prior.png", dpi=130); plt.show()'''),
("md", "### Burglary–Alarm Bayesian network"),
("code", r'''import itertools
P_B, P_E = 0.001, 0.002
P_A = {(True, True): 0.95, (True, False): 0.94, (False, True): 0.29, (False, False): 0.001}
P_J = {True: 0.90, False: 0.05}; P_M = {True: 0.70, False: 0.01}
def p(v, prob): return prob if v else 1 - prob
def joint(b, e, a, j, m):
    return p(b, P_B) * p(e, P_E) * p(a, P_A[(b, e)]) * p(j, P_J[a]) * p(m, P_M[a])
print(f"P(j, m, a, ¬b, ¬e) = {joint(False, False, True, True, True):.6f}")

def enumerate_query(var, evidence):
    names = ["B", "E", "A", "J", "M"]; dist = {}
    for val in (True, False):
        tot = 0.0
        for vals in itertools.product((True, False), repeat=5):
            asg = dict(zip(names, vals))
            if asg[var] != val or any(asg[k] != v for k, v in evidence.items()): continue
            tot += joint(*vals)
        dist[val] = tot
    z = sum(dist.values()); return {k: v / z for k, v in dist.items()}
for q, ev in (("B", {"J": True, "M": True}), ("E", {"J": True, "M": True}), ("A", {"J": True, "M": True}), ("B", {"J": True, "M": False})):
    r = enumerate_query(q, ev); print(f"P({q}=T | {', '.join(f'{k}={v}' for k, v in ev.items())}) = {r[True]:.4f}")'''),
("code", r'''rng = np.random.default_rng(0)
def prior_sample():
    b = rng.random() < P_B; e = rng.random() < P_E; a = rng.random() < P_A[(b, e)]
    return b, e, a, rng.random() < P_J[a], rng.random() < P_M[a]
def likelihood_weighting(n):
    wsum = {True: 0.0, False: 0.0}; est = []
    for i in range(1, n + 1):
        b = rng.random() < P_B; e = rng.random() < P_E; a = rng.random() < P_A[(b, e)]
        w = P_J[a] * P_M[a]; wsum[b] += w
        if i % 500 == 0: est.append(wsum[True] / (wsum[True] + wsum[False]))
    return est
exact = enumerate_query("B", {"J": True, "M": True})[True]
est = likelihood_weighting(100_000)
print(f"Exact P(B | j, m) = {exact:.4f};  likelihood weighting (100k samples) ≈ {est[-1]:.4f}")
fig, ax = plt.subplots(figsize=(6.8, 3.6)); xs = np.arange(1, len(est) + 1) * 500
line, = ax.plot([], [], color=NAVY, lw=2); ax.axhline(exact, color=GOLD, ls="--", lw=2, label=f"exact = {exact:.3f}")
ax.set_xlim(0, xs[-1]); ax.set_ylim(0, 0.8); ax.set_xlabel("samples"); ax.set_ylabel("estimate"); ax.legend(frameon=False)
def upd(k):
    line.set_data(xs[:k + 1], est[:k + 1]); ax.set_title(f"Likelihood weighting converges — {xs[k]:,} samples"); return line,
gif = save_gif(animation.FuncAnimation(fig, upd, frames=range(0, len(est), 5)), "exp08_sampling_convergence.gif", fps=6)
display(Image(filename=gif))'''),
("code", r'''import networkx as nx
G = nx.DiGraph([("Burglary","Alarm"),("Earthquake","Alarm"),("Alarm","JohnCalls"),("Alarm","MaryCalls")])
pos = {"Burglary":(0,1),"Earthquake":(2,1),"Alarm":(1,0.5),"JohnCalls":(0,0),"MaryCalls":(2,0)}
plt.figure(figsize=(6, 3.6))
nx.draw(G, pos, with_labels=True, node_color=[GOLDL, GOLDL, NAVY, MIST, MIST], node_size=3800, edgecolors=NAVY,
        font_color="black", font_family="serif", font_size=10, arrowsize=18, edge_color=TEAL, width=2)
plt.title("Bayesian network structure"); plt.savefig(f"{FIG}/exp08_bayesnet.png", dpi=130, bbox_inches="tight"); plt.show()'''),
],
conclusion="A positive result from a 90%-sensitive test with 1% prevalence gives only a 15.4% chance of disease. In the alarm network, P(Burglary | JohnCalls, MaryCalls) = 0.284 by exact enumeration, and likelihood weighting converges to the same value.",
viva=["State Bayes' theorem and name each term.", "Explain the base-rate fallacy with the medical test example.",
"Why is a Bayesian network more compact than the full joint distribution?", "What is the complexity of inference by enumeration?",
"How does likelihood weighting differ from rejection sampling?"])

EXP9 = dict(num=9, slug="DecisionTree_Rules", co="CO204.5",
title="Decision-Tree Classifier and Rule Extraction",
aim="Build a decision tree (ID3 from scratch on the Play-Tennis data and scikit-learn CART on the Iris data), interpret the learned rules and study overfitting with depth.",
theory="""Entropy $H(S)=-\\sum_k p_k\\log_2p_k$; information gain $Gain(S,A)=H(S)-\\sum_v\\frac{|S_v|}{|S|}H(S_v)$.
ID3 chooses the attribute with the highest gain at each node and recurses until nodes are pure. CART uses the Gini index. Deep trees overfit; limit depth or prune.""",
algorithm=["Compute the entropy of the full dataset.", "Compute the information gain of every attribute; split on the best.",
"Recurse on each subset until pure or no attributes remain.", "Convert each root-to-leaf path into an IF–THEN rule; evaluate on test data."],
cells=[
("code", r'''import pandas as pd
from math import log2
data = pd.DataFrame([
 ["Sunny","Hot","High","Weak","No"],["Sunny","Hot","High","Strong","No"],["Overcast","Hot","High","Weak","Yes"],
 ["Rain","Mild","High","Weak","Yes"],["Rain","Cool","Normal","Weak","Yes"],["Rain","Cool","Normal","Strong","No"],
 ["Overcast","Cool","Normal","Strong","Yes"],["Sunny","Mild","High","Weak","No"],["Sunny","Cool","Normal","Weak","Yes"],
 ["Rain","Mild","Normal","Weak","Yes"],["Sunny","Mild","Normal","Strong","Yes"],["Overcast","Mild","High","Strong","Yes"],
 ["Overcast","Hot","Normal","Weak","Yes"],["Rain","Mild","High","Strong","No"]],
 columns=["Outlook","Temperature","Humidity","Wind","Play"])
def H(s):
    p = s.value_counts(normalize=True); return -sum(q * log2(q) for q in p if q > 0)
def gain(df, a, t="Play"):
    return H(df[t]) - sum(len(g) / len(df) * H(g[t]) for _, g in df.groupby(a))
print(f"H(S) = {H(data['Play']):.3f}")
gains = {a: gain(data, a) for a in data.columns[:-1]}
for a, g in sorted(gains.items(), key=lambda x: -x[1]): print(f"  Gain(S, {a:<11}) = {g:.3f}")'''),
("code", r'''def id3(df, attrs, t="Play"):
    if df[t].nunique() == 1: return df[t].iloc[0]
    if not attrs: return df[t].mode()[0]
    best = max(attrs, key=lambda a: gain(df, a))
    return {best: {v: id3(g, [a for a in attrs if a != best]) for v, g in df.groupby(best)}}
tree = id3(data, list(data.columns[:-1]))
def rules(node, cond=()):
    if not isinstance(node, dict): yield cond, node; return
    (a, branches), = node.items()
    for v, sub in branches.items(): yield from rules(sub, cond + ((a, v),))
print("Learned tree:", tree, "\n")
for c, out in rules(tree): print("IF " + " AND ".join(f"{a} = {v}" for a, v in c) + f"  THEN Play = {out}")
def predict(node, x):
    while isinstance(node, dict): (a, br), = node.items(); node = br[x[a]]
    return node
acc = np.mean([predict(tree, r) == r["Play"] for _, r in data.iterrows()]); print(f"\nTraining accuracy: {acc:.0%}")'''),
("code", r'''fig, ax = plt.subplots(figsize=(6.5, 3.4))
ks = sorted(gains, key=lambda k: -gains[k])
ax.bar(ks, [gains[k] for k in ks], color=[NAVY, TEAL, GOLD, CRIMSON])
for i, k in enumerate(ks): ax.text(i, gains[k] + 0.005, f"{gains[k]:.3f}", ha="center", color=NAVY, weight="bold")
ax.set_ylabel("information gain (bits)"); ax.set_title("Root selection: Outlook has the highest gain")
plt.tight_layout(); plt.savefig(f"{FIG}/exp09_gain.png", dpi=130); plt.show()'''),
("md", "### scikit-learn CART on the Iris dataset"),
("code", r'''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix
iris = load_iris(); X, y = iris.data, iris.target
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
clf = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Xtr, ytr)
print("Test accuracy:", round(accuracy_score(yte, clf.predict(Xte)), 3))
print("Confusion matrix:\n", confusion_matrix(yte, clf.predict(Xte)))
print("\nRules learned:\n" + export_text(clf, feature_names=list(iris.feature_names)))
plt.figure(figsize=(10, 5.5))
plot_tree(clf, feature_names=iris.feature_names, class_names=iris.target_names, filled=True, rounded=True, fontsize=9)
plt.title("CART decision tree (max_depth = 3)"); plt.savefig(f"{FIG}/exp09_iris_tree.png", dpi=130, bbox_inches="tight"); plt.show()'''),
("code", r'''depths = range(1, 11); tr_acc, te_acc = [], []
for d in depths:
    m = DecisionTreeClassifier(max_depth=d, random_state=0).fit(Xtr, ytr)
    tr_acc.append(m.score(Xtr, ytr)); te_acc.append(m.score(Xte, yte))
plt.figure(figsize=(6.5, 3.5)); plt.plot(depths, tr_acc, "-o", color=NAVY, label="train"); plt.plot(depths, te_acc, "-s", color=GOLD, label="test")
plt.xlabel("max depth"); plt.ylabel("accuracy"); plt.legend(frameon=False); plt.title("Depth vs accuracy — watch for overfitting")
plt.tight_layout(); plt.savefig(f"{FIG}/exp09_depth.png", dpi=130); plt.show()

X2 = X[:, 2:4]; xx, yy = np.meshgrid(np.linspace(0.5, 7.2, 300), np.linspace(0, 2.7, 300))
fig, ax = plt.subplots(figsize=(6, 4.4)); cm = matplotlib.colors.ListedColormap([GOLDL, "#BFE3E6", "#D9DEEA"])
def frm(k):
    d = k + 1; m = DecisionTreeClassifier(max_depth=d, random_state=0).fit(X2, y); ax.clear()
    ax.contourf(xx, yy, m.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape), cmap=cm)
    for c, col in zip(range(3), [GOLD, TEAL, NAVY]): ax.scatter(*X2[y == c].T, color=col, edgecolor="white", s=40, label=iris.target_names[c])
    ax.set_xlabel("petal length"); ax.set_ylabel("petal width"); ax.legend(frameon=False, loc="upper left")
    ax.set_title(f"Decision boundary, depth = {d}, train acc = {m.score(X2, y):.2f}")
gif = save_gif(animation.FuncAnimation(fig, frm, frames=6), "exp09_tree_boundary.gif", fps=1)
display(Image(filename=gif))'''),
],
conclusion="ID3 selected Outlook (gain 0.247) as the root and produced five readable rules with 100% training accuracy. CART on Iris reached high test accuracy at depth 3; deeper trees fit training data perfectly without improving test accuracy — a sign of overfitting.",
viva=["Define entropy and information gain.", "Why is Outlook chosen as the root for Play Tennis?",
"Compare Gini index and entropy.", "How does pruning reduce overfitting?",
"Why are decision trees considered interpretable models?"])

EXP10 = dict(num=10, slug="ExpertSystem_Chatbot", co="CO204.5",
title="Rule-Based Expert System and a Basic Chatbot (Mini-Project)",
aim="Develop a rule-based expert system with certainty factors and an explanation facility for crop-disease advice, and a pattern-matching chatbot for college admission queries.",
theory="""An expert system has a **knowledge base** (IF–THEN rules), **working memory** (facts), an **inference engine** (match → conflict resolution → act) and an **explanation facility**.
Certainty factors combine as $CF(conclusion)=\\min(CF_{premises})\\times CF_{rule}$ and, for two rules supporting the same conclusion, $CF_1+CF_2(1-CF_1)$.
A **retrieval chatbot** matches user input to intents using patterns/keywords and returns a response.""",
algorithm=["Load rules and the user's observed facts with certainty values.", "Find all rules whose premises are in working memory (match).",
"Fire them, computing the conclusion CF; combine CFs for repeated conclusions; repeat until no change.",
"Report conclusions sorted by CF and answer WHY/HOW questions from the firing trace."],
cells=[
("code", r'''RULES = [
 ("R1", ["yellow_leaves", "leaf_spots"],          "fungal_infection",   0.7),
 ("R2", ["white_powder_on_leaves"],                "powdery_mildew",     0.9),
 ("R3", ["fungal_infection", "humid_weather"],     "leaf_blight",        0.8),
 ("R4", ["wilting", "dry_soil"],                   "water_stress",       0.85),
 ("R5", ["wilting", "brown_stem_base"],            "root_rot",           0.75),
 ("R6", ["holes_in_leaves", "larvae_seen"],        "pest_attack",        0.9),
 ("R7", ["leaf_blight"],                           "advise_fungicide",   0.9),
 ("R8", ["powdery_mildew"],                        "advise_sulphur_spray", 0.85),
 ("R9", ["water_stress"],                          "advise_irrigation",  0.95),
 ("R10",["pest_attack"],                           "advise_neem_oil",    0.8),
 ("R11",["root_rot"],                              "advise_drainage",    0.8),
 ("R12",["yellow_leaves", "stunted_growth"],       "nitrogen_deficiency",0.7),
 ("R13",["nitrogen_deficiency"],                   "advise_urea_dose",   0.8),
]
def infer(observed):
    wm = dict(observed); trace = []; changed = True
    while changed:
        changed = False
        for rid, prem, concl, cf in RULES:
            if all(p in wm for p in prem):
                new = round(min(wm[p] for p in prem) * cf, 3)
                old = wm.get(concl)
                comb = new if old is None else round(old + new * (1 - old), 3)
                if (rid, concl) not in [(t[0], t[2]) for t in trace]:
                    wm[concl] = comb; trace.append((rid, prem, concl, comb)); changed = True
    return wm, trace
def explain(concl, trace):
    for rid, prem, c, cf in trace:
        if c == concl: return f"{concl} (CF {cf}) because {rid}: " + " AND ".join(prem)
    return f"{concl} was observed directly."
case = {"yellow_leaves": 1.0, "leaf_spots": 0.9, "humid_weather": 0.8, "holes_in_leaves": 0.6, "larvae_seen": 0.7}
wm, trace = infer(case)
print("Observed:", case, "\n\nInference trace:")
for rid, prem, c, cf in trace: print(f"  {rid}: IF {' AND '.join(prem)} THEN {c}   → CF = {cf}")
print("\nAdvice (sorted by certainty):")
for k, v in sorted(wm.items(), key=lambda x: -x[1]):
    if k.startswith("advise"): print(f"  • {k.replace('advise_', '').replace('_', ' ').title():<16} CF = {v}")
print("\nHOW was leaf_blight concluded?  ", explain("leaf_blight", trace))'''),
("code", r'''import networkx as nx
G = nx.DiGraph()
for rid, prem, c, cf in trace:
    for p in prem: G.add_edge(p, c, label=rid)
layers = {}
def depth(n): return 0 if n in case else 1 + max(depth(p) for p in G.predecessors(n))
for n in G.nodes: layers.setdefault(depth(n), []).append(n)
pos = {n: (d * 3.0, -i * 1.2 + len(ns) * 0.6) for d, ns in layers.items() for i, n in enumerate(sorted(ns))}
order = [rid for rid, *_ in trace]
fig, ax = plt.subplots(figsize=(9, 4.8))
def fr(k):
    ax.clear(); fired = set(order[:k]); lit = set(case) | {c for rid, _, c, _ in trace if rid in fired}
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=[GOLD if G[u][v]["label"] in fired else "#C8D0DC" for u, v in G.edges], width=2.2, arrowsize=14)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=[(LEAF if n.startswith("advise") else NAVY) if n in lit else MIST for n in G.nodes], node_size=2600, edgecolors=NAVY)
    for group, fc in ((lit, "white"), (set(G.nodes) - lit, NAVY)):
        nx.draw_networkx_labels(G, pos, ax=ax, labels={n: n.replace("_", "\n") for n in G.nodes if n in group}, font_size=7.5,
                                font_family="serif", font_color=fc)
    ax.set_title(f"Rule firing: {', '.join(order[:k]) or 'initial facts'}"); ax.axis("off"); ax.margins(0.12)
gif = save_gif(animation.FuncAnimation(fig, fr, frames=len(order) + 3), "exp10_expert_system_firing.gif", fps=1)
display(Image(filename=gif))'''),
("md", "### Basic admission chatbot (pattern / keyword matching)"),
("code", r'''import re
INTENTS = [
 ("greet",    r"\b(hi|hello|hey|namaste)\b",                 "Hello! I am the Sanjivani AI&DS admission assistant. How can I help?"),
 ("fees",     r"\b(fee|fees|cost|tuition)\b",                "Fee details for B.Tech AI & DS are on the university admissions portal; scholarships are available for eligible students."),
 ("eligible", r"\b(eligib\w*|criteria|qualify|jee|mht.?cet)\b", "Eligibility: 10+2 with Physics & Mathematics and a valid MHT-CET / JEE Main score."),
 ("courses",  r"\b(course|subject|syllabus|curriculum)\b",   "The curriculum covers AI, ML, Deep Learning, Data Engineering and an industry internship."),
 ("hostel",   r"\b(hostel|accommodation|stay)\b",            "Separate hostels for boys and girls are available on campus."),
 ("placement",r"\b(placement\w*|jobs?|package|recruit\w*)\b",     "The Training & Placement cell runs aptitude training and campus drives every year."),
 ("contact",  r"\b(contact|phone|email|address)\b",          "Please visit the university website or the admissions office, Kopargaon."),
 ("bye",      r"\b(bye|thanks|thank you)\b",                 "Thank you! All the best for your admission."),
]
def reply(msg):
    m = msg.lower()
    for name, pat, ans in INTENTS:
        if re.search(pat, m): return name, ans
    return "fallback", "Sorry, I did not understand. You can ask about fees, eligibility, courses, hostel or placements."
for q in ["Hi there!", "What is the eligibility for AI and DS?", "How much are the fees?", "Is hostel available?",
          "Tell me about placements", "Can I study astrophysics?", "Thanks, bye"]:
    intent, ans = reply(q); print(f"👤 {q}\n🤖 [{intent}] {ans}\n")'''),
("code", r'''tests = [("hello", "greet"), ("fees structure?", "fees"), ("am I eligible with JEE", "eligible"), ("syllabus please", "courses"),
         ("where do I stay", "hostel"), ("average package", "placement"), ("email id", "contact"), ("thank you", "bye"), ("weather today", "fallback")]
acc = np.mean([reply(q)[0] == t for q, t in tests]); print(f"Intent accuracy on test prompts: {acc:.0%}")'''),
],
conclusion="The expert system chained symptom rules to diagnoses and advice, combined certainty factors and explained its reasoning; the chatbot correctly mapped all test prompts to intents, falling back gracefully for unknown queries.",
viva=["List the components of an expert system.", "How are certainty factors combined in MYCIN?",
"What is conflict resolution in a production system?", "What is the role of the explanation facility?",
"How would you improve the chatbot using machine learning?"])
