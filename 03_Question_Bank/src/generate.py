"""Generate Question Bank and Projects handbook (LaTeX + Markdown).
Run from repo root:  python 03_Question_Bank/src/generate.py
"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "03_Question_Bank", "src"))
sys.path.insert(0, os.path.join(ROOT, "04_Projects", "src"))
from qb_data import UNITS, BTL_NAMES
from projects_data import PROJECTS

BTL_COL = {"L1": "teal", "L2": "navyL", "L3": "leaf", "L4": "gold!85!black", "L5": "crimson", "L6": "navy"}

def tex_escape(s):
    rep = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}
    for a, b in rep.items():
        s = s.replace(a, b)
    return s

UNIC = {"⇒": r"$\Rightarrow$", "⇔": r"$\Leftrightarrow$", "¬": r"$\neg$", "∨": r"$\vee$", "∧": r"$\wedge$",
        "∀": r"$\forall$", "∃": r"$\exists$", "×": r"$\times$", "≥": r"$\ge$", "≤": r"$\le$", "–": "--", "—": "---",
        "η": r"$\eta$", "°": r"$^\circ$", "→": r"$\to$", "…": r"\dots{}", "ï": r"\"{i}", "≡": r"$\equiv$"}
def tex(s):
    s = tex_escape(s)
    for a, b in UNIC.items():
        s = s.replace(a, b)
    return s

# ------------------------------------------------------------------ QB
def qb_tex():
    L = [r"\documentclass[11pt]{article}", r"\usepackage{../common/ai204}",
         r"\renewcommand{\doctitle}{BTL Question Bank}", r"\begin{document}",
         r"\aicover{Question Bank}{30 questions per unit \textbullet\ 150 questions mapped to Bloom's Taxonomy (L1--L6) and Course Outcomes}{Remember \textbullet\ Understand \textbullet\ Apply \textbullet\ Analyse \textbullet\ Evaluate \textbullet\ Create}",
         r"\section*{How to use this Question Bank}",
         r"Every unit has exactly \textbf{30 questions}: five at each Bloom's Taxonomy Level (BTL). Marks guide: L1 = 2 marks, L2--L3 = 5 marks, L4--L6 = 10 marks. Use L1--L3 for CIA-I/quiz, L3--L5 for CIA-II and end-semester, L6 for assignments and open-book tasks.",
         r"\begin{center}\begin{tabular}{cllp{8cm}}",
         r"\rowcolor{navy}\color{gold}\textbf{Level}&\color{gold}\textbf{Name}&\color{gold}\textbf{Marks}&\color{gold}\textbf{Typical verbs}\\"]
    verbs = {"L1": "define, list, state, name, recall", "L2": "explain, describe, discuss, summarise",
             "L3": "apply, compute, solve, trace, formulate", "L4": "analyse, compare, differentiate, examine",
             "L5": "evaluate, justify, assess, critique, judge", "L6": "design, develop, propose, construct, create"}
    for k, (lv, nm) in enumerate(BTL_NAMES.items()):
        mk = "2" if lv == "L1" else ("5" if lv in ("L2", "L3") else "10")
        L.append((r"\rowcolor{ivory}" if k % 2 else "") + rf"\btl{{{lv}}}&{nm}&{mk}&{verbs[lv]}\\")
    L += [r"\end{tabular}\end{center}"]
    # distribution chart
    L += [r"\begin{center}\begin{tikzpicture}[x=1.7cm,y=0.18cm]",
          r"\draw[slate,->](0,0)--(6.6,0); \draw[slate,->](0,0)--(0,30) node[above,font=\small]{questions};"]
    for i, lv in enumerate(BTL_NAMES):
        L.append(rf"\fill[{BTL_COL[lv]}] ({i+0.2},0) rectangle ({i+0.8},25); \node[font=\small\bfseries] at ({i+0.5},26.8){{25}}; \node[below,font=\small] at ({i+0.5},0){{{lv}}};")
    L += [r"\end{tikzpicture}\\{\small\color{slate}Course-wide distribution: 25 questions at each BTL level (150 total).}\end{center}", r"\newpage"]
    for u, (title, co, qs) in UNITS.items():
        L.append(rf"\unitbanner{{{u}}}{{{tex(title)}}}{{30 Questions \textbullet\ {co}}}")
        L += [r"\begin{longtable}{>{\bfseries\color{navy}}p{0.8cm}p{11.6cm}ccc}",
              r"\rowcolor{navy}\color{gold}Q.&\color{gold}Question&\color{gold}BTL&\color{gold}CO&\color{gold}M\\\endhead"]
        for i, (lv, mk, q) in enumerate(qs, 1):
            row = rf"{i}&{tex(q)}&\btl{{{lv}}}&\co{{{co}}}&{mk}\\"
            L.append((r"\rowcolor{ivory}" if i % 2 == 0 else "") + row)
            if i % 5 == 0 and i < 30:
                L.append(r"\arrayrulecolor{gold}\midrule\arrayrulecolor{black}")
        L += [r"\end{longtable}", r"\newpage"]
    L.append(r"\end{document}")
    return "\n".join(L)

def qb_md():
    L = ["# 26UAMPC204 Artificial Intelligence — BTL Question Bank", "",
         "30 questions per unit (5 per Bloom's level). Marks: L1 = 2, L2–L3 = 5, L4–L6 = 10.", ""]
    for u, (title, co, qs) in UNITS.items():
        L += [f"## Unit {u}: {title} ({co})", "", "| # | Question | BTL | Marks |", "|---|---|---|---|"]
        for i, (lv, mk, q) in enumerate(qs, 1):
            L.append(f"| {i} | {q} | {lv} – {BTL_NAMES[lv]} | {mk} |")
        L.append("")
    return "\n".join(L)

# ------------------------------------------------------------------ Projects
def proj_tex():
    L = [r"\documentclass[11pt]{article}", r"\usepackage{../common/ai204}",
         r"\renewcommand{\doctitle}{Project Portfolio}", r"\begin{document}",
         r"\aicover{Project Portfolio}{50 unit-aligned mini and major projects \textbullet\ 10 per unit}{Problem \textbullet\ Tools \textbullet\ Deliverables \textbullet\ CO \& BTL mapping \textbullet\ Rubric}",
         r"\section*{Project Guidelines}",
         r"\begin{itemize}\item \textbf{Mini projects} (individual, 2 weeks): one algorithm, one dataset/simulation, a short report.",
         r"\item \textbf{Major projects} (teams of 3--4, 6 weeks): working system, demo video, GitHub repository, IEEE-format report.",
         r"\item Every project must include a \emph{README}, a requirements file, reproducible notebooks and a responsible-AI note.\end{itemize}",
         r"\begin{center}\begin{tabular}{lp{9cm}c}\rowcolor{navy}\color{gold}\textbf{Criterion}&\color{gold}\textbf{Description}&\color{gold}\textbf{Marks}\\",
         r"Problem formulation&Clear PEAS / state space / model specification&15\\",
         r"\rowcolor{ivory}Algorithm \& implementation&Correct, efficient, well-structured code&30\\",
         r"Experiments \& analysis&Baselines, metrics, plots and interpretation&25\\",
         r"\rowcolor{ivory}Presentation \& demo&Demo, viva, clarity of explanation&15\\",
         r"Documentation \& ethics&README, report, responsible-AI reflection&15\\\midrule",
         r"\textbf{Total}&&\textbf{100}\\\end{tabular}\end{center}\newpage"]
    titles = {u: UNITS[u][0] for u in UNITS}
    for u, plist in PROJECTS.items():
        co = UNITS[u][1]
        L.append(rf"\unitbanner{{{u}}}{{Projects: {tex(titles[u])}}}{{10 Projects \textbullet\ {co}}}")
        for i, (t, lvl, prob, tools, deliv) in enumerate(plist, 1):
            col = "crimson" if lvl == "Major" else "teal"
            btl = "L6" if lvl == "Major" else "L3/L4"
            L.append(rf"""\begin{{tcolorbox}}[enhanced,breakable,colback=white,colframe={col},arc=2mm,boxrule=0.9pt,
  title={{\textbf{{P{u}.{i:02d}\quad {tex(t)}}}\hfill \colorbox{{white}}{{\textcolor{{{col}}}{{\scriptsize\bfseries {lvl.upper()}}}}}}},fonttitle=\color{{white}},colbacktitle={col}]
\textbf{{\color{{navy}}Problem:}} {tex(prob)}\\[2pt]
\textbf{{\color{{navy}}Tools / Data:}} {tex(tools)}\qquad \textbf{{\color{{navy}}Deliverables:}} {tex(deliv)}\\[2pt]
\co{{{co}}}\ \btl{{{btl}}}
\end{{tcolorbox}}""")
        L.append(r"\newpage")
    L.append(r"\end{document}")
    return "\n".join(L)

def proj_md():
    L = ["# 26UAMPC204 Artificial Intelligence — Project Portfolio (50 projects)", "",
         "Mini = individual, 2 weeks. Major = team of 3–4, 6 weeks. Rubric: formulation 15, implementation 30, experiments 25, demo 15, documentation & ethics 15.", ""]
    for u, plist in PROJECTS.items():
        L += [f"## Unit {u}: {UNITS[u][0]} ({UNITS[u][1]})", "", "| ID | Project | Type | Problem | Tools | Deliverables |", "|---|---|---|---|---|---|"]
        for i, (t, lvl, prob, tools, deliv) in enumerate(plist, 1):
            L.append(f"| P{u}.{i:02d} | **{t}** | {lvl} | {prob} | {tools} | {deliv} |")
        L.append("")
    return "\n".join(L)

import re
def fixhdr(t):
    return re.sub(r"\\color\{gold\}(\\textbf\{[^}]*\}|[A-Za-z.]+)", r"\\textcolor{gold}{\1}", t)

if __name__ == "__main__":
    open(os.path.join(ROOT, "03_Question_Bank", "AI_Question_Bank_BTL.tex"), "w").write(fixhdr(qb_tex()))
    open(os.path.join(ROOT, "03_Question_Bank", "AI_Question_Bank_BTL.md"), "w").write(qb_md())
    open(os.path.join(ROOT, "04_Projects", "AI_Projects_Portfolio.tex"), "w").write(fixhdr(proj_tex()))
    open(os.path.join(ROOT, "04_Projects", "AI_Projects_Portfolio.md"), "w").write(proj_md())
    print("generated QB and projects")
