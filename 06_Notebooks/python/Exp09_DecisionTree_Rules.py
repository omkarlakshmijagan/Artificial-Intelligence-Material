"""Experiment 9: Decision-Tree Classifier and Rule Extraction
Aim: Build a decision tree (ID3 from scratch on the Play-Tennis data and scikit-learn CART on the Iris data), interpret the learned rules and study overfitting with depth.
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


import pandas as pd
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
for a, g in sorted(gains.items(), key=lambda x: -x[1]): print(f"  Gain(S, {a:<11}) = {g:.3f}")

def id3(df, attrs, t="Play"):
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
acc = np.mean([predict(tree, r) == r["Play"] for _, r in data.iterrows()]); print(f"\nTraining accuracy: {acc:.0%}")

fig, ax = plt.subplots(figsize=(6.5, 3.4))
ks = sorted(gains, key=lambda k: -gains[k])
ax.bar(ks, [gains[k] for k in ks], color=[NAVY, TEAL, GOLD, CRIMSON])
for i, k in enumerate(ks): ax.text(i, gains[k] + 0.005, f"{gains[k]:.3f}", ha="center", color=NAVY, weight="bold")
ax.set_ylabel("information gain (bits)"); ax.set_title("Root selection: Outlook has the highest gain")
plt.tight_layout(); plt.savefig(f"{FIG}/exp09_gain.png", dpi=130); plt.show()

from sklearn.datasets import load_iris
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
plt.title("CART decision tree (max_depth = 3)"); plt.savefig(f"{FIG}/exp09_iris_tree.png", dpi=130, bbox_inches="tight"); plt.show()

depths = range(1, 11); tr_acc, te_acc = [], []
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
print('animation saved:', gif)
