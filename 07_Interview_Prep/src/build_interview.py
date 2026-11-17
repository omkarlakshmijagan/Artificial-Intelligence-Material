"""Build the Interview & Industry-Skills section.
Outputs
  07_Interview_Prep/AI_Interview_Skills_Handbook.tex / .md
  07_Interview_Prep/Interview_Coding_Solutions.ipynb (executed) and .py
  01_Unit_Notes/latex/unitN_industry.tex   (inserted at the end of every unit's notes)
  02_PPT/src/industry.json                 (two extra slides per unit deck)
Run from repo root: python 07_Interview_Prep/src/build_interview.py
"""
import os, sys, json, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "06_Notebooks", "src"))
from interview_data import SKILLS, Q, TRACKS
from coding_problems import PROBLEMS
OUT = os.path.join(ROOT, "07_Interview_Prep")
TITLES = {"I": "Introduction to AI and Intelligent Agents", "II": "Problem Solving by Search",
          "III": "Knowledge Representation and Reasoning", "IV": "Planning and Reasoning under Uncertainty",
          "V": "Learning, Expert Systems and Applications of AI"}
CO = {"I": "CO204.1", "II": "CO204.2", "III": "CO204.3", "IV": "CO204.4", "V": "CO204.5"}
ROUND_COL = {"Concept": "teal", "Coding": "navyL", "Design": "crimson", "Scenario": "leaf"}
DIFF_COL = {"Easy": "leaf", "Medium": "gold!85!black", "Hard": "crimson"}

SYM = {"α": r"$\alpha$", "β": r"$\beta$", "θ": r"$\theta$", "≥": r"$\ge$", "≤": r"$\le$", "→": r"$\to$", "⇒": r"$\Rightarrow$",
       "¬": r"$\neg$", "∨": r"$\vee$", "∧": r"$\wedge$", "⊨": r"$\models$", "−": "--", "–": "--", "—": "---", "×": r"$\times$",
       "≈": r"$\approx$", "√": r"$\surd$", "Σ": r"$\Sigma$", "²": r"$^2$", "∀": r"$\forall$", "∃": r"$\exists$", "≠": r"$\ne$",
       "μ": r"$\mu$", "η": r"$\eta$", "°": r"$^\circ$", "₁": r"$_1$", "₂": r"$_2$", "ŷ": r"$\hat y$", "∞": r"$\infty$", "…": r"\dots{}",
       "’": "'", "′": r"$'$", "Ã¯": "i", "ï": r"\"{i}"}
def tex(s):
    s = s.replace("e^(ΔE/T)", "\x01e^{\\Delta E/T}\x02")
    s = re.sub(r"(\w)\^\(([^)]*)\)", lambda m: "\x01" + m.group(1) + "^{" + m.group(2).replace("·", "\\cdot ") + "}\x02", s)
    s = re.sub(r"(\w)\^(\w)", lambda m: "\x01" + m.group(1) + "^{" + m.group(2) + "}\x02", s)
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_")):
        s = re.sub(r"(?<![\x01-\x02])" + re.escape(a), b.replace("\\", "\\\\"), s) if False else s.replace(a, b) if a != "\\" else s
    parts = re.split(r"(\x01[^\x02]*\x02)", s); out = []
    for p in parts:
        if p.startswith("\x01"):
            out.append("$" + p[1:-1] + "$"); continue
        for a, b in SYM.items():
            p = p.replace(a, b)
        out.append(p.replace("·", r"$\cdot$").replace("Δ", r"$\Delta$"))
    return "".join(out)

# ---------------------------------------------------------------- handbook (LaTeX)
def qa_box(u, i, q):
    rnd, diff, track, question, ans = q
    return rf"""\begin{{tcolorbox}}[enhanced,breakable,colback=white,colframe={ROUND_COL[rnd]},arc=2mm,boxrule=0.8pt,left=3mm,right=3mm,
 title={{\textbf{{Q{u}.{i:02d}}}\quad {tex(question)}}},fonttitle=\color{{white}}\small,colbacktitle={ROUND_COL[rnd]}]
\colorbox{{{ROUND_COL[rnd]}!15}}{{\scriptsize\bfseries\color{{{ROUND_COL[rnd]}}} {rnd.upper()}}}\
\colorbox{{{DIFF_COL[diff]}!15}}{{\scriptsize\bfseries\color{{{DIFF_COL[diff]}}} {diff.upper()}}}\
\colorbox{{navy!8}}{{\scriptsize\bfseries\color{{navy}} {tex(track)}}}\par\smallskip
\textbf{{\color{{navy}}Model answer.}} {tex(ans)}
\end{{tcolorbox}}"""

def skills_block(u, compact=False):
    s = SKILLS[u]
    items = "\n".join(rf"\item {tex(x)}" for x in s["skills"])
    return rf"""\begin{{tcolorbox}}[enhanced,colback=navy,colframe=gold,boxrule=1.2pt,arc=2mm,coltext=white,
 title={{\textbf{{Top industry skills you gain in Unit {u}}}}},fonttitle=\color{{navy}},colbacktitle=gold]
\begin{{itemize}}\setlength\itemsep{{1pt}}
{items}
\end{{itemize}}
\end{{tcolorbox}}
\begin{{tabularx}}{{\linewidth}}{{>{{\bfseries\color{{navy}}}}p{{3.4cm}}X}}
Tools to master & {tex(', '.join(s['tools']))}\\
Job roles & {tex(', '.join(s['roles']))}\\
Portfolio output & {tex(s['portfolio'])}\\
\end{{tabularx}}"""

def handbook():
    L = [r"\documentclass[11pt]{article}", r"\usepackage{../common/ai204}", r"\renewcommand{\doctitle}{Interview \& Industry Skills}",
         r"\begin{document}",
         r"\aicover{Interview \& Industry-Skills Handbook}{75 unit-wise interview questions with model answers \textbullet\ 10 solved coding problems \textbullet\ skill map}{Concept \textbullet\ Coding \textbullet\ System \& ML Design \textbullet\ Scenario \& Ethics}",
         r"\section*{How to use this handbook}",
         r"This handbook prepares you for the technical interview loops used by AI product companies, AI research labs, start-ups and IT-services / global capability centres (GCCs). The questions are \textbf{practice questions written for this course}, modelled on the topics and formats commonly discussed for such interviews; they are not verbatim questions from any specific company.",
         r"\begin{center}\begin{tabular}{>{\bfseries}l p{11cm}}",
         r"\rowcolor{navy}\textcolor{gold}{Round}&\textcolor{gold}{\textbf{What the interviewer checks}}\\",
         r"\textcolor{teal}{Concept}&Clear definitions, trade-offs and the ability to explain to a non-expert.\\",
         r"\rowcolor{ivory}\textcolor{navyL}{Coding}&Correct, efficient, tested code; complexity analysis; edge cases.\\",
         r"\textcolor{crimson}{Design}&Turning a fuzzy requirement into a system: data, algorithms, scale, metrics, failure modes.\\",
         r"\rowcolor{ivory}\textcolor{leaf}{Scenario}&Judgement in real situations: debugging, product trade-offs, ethics and safety.\\",
         r"\end{tabular}\end{center}",
         r"\begin{keypoint}[Answering framework]",
         r"\textbf{Clarify} the question and constraints $\rightarrow$ \textbf{State} a simple baseline $\rightarrow$ \textbf{Improve} it with the right AI technique $\rightarrow$ \textbf{Analyse} complexity, metrics and risks $\rightarrow$ \textbf{Summarise} in one sentence. For behavioural questions use STAR (Situation, Task, Action, Result).",
         r"\end{keypoint}",
         r"\section*{Skill map: what this course makes you job-ready for}",
         r"\begin{center}\small\begin{tabularx}{\linewidth}{c >{\raggedright}p{4cm} X}",
         r"\rowcolor{navy}\textcolor{gold}{\textbf{Unit}}&\textcolor{gold}{\textbf{Core skill}}&\textcolor{gold}{\textbf{Job roles}}\\"]
    for k, u in enumerate(SKILLS):
        L.append((r"\rowcolor{ivory}" if k % 2 else "") + rf"{u}&{tex(SKILLS[u]['skills'][0])}\tabularnewline")
        L[-1] = (r"\rowcolor{ivory}" if k % 2 else "") + rf"{u}&{tex(SKILLS[u]['skills'][0])}&{tex(', '.join(SKILLS[u]['roles']))}\\"
    L += [r"\end{tabularx}\end{center}",
          r"\section*{A 4-week interview-preparation plan}",
          r"\begin{tabularx}{\linewidth}{>{\bfseries\color{navy}}l X}\toprule",
          r"Week 1&Units I--II concept questions; code BFS, DFS, UCS and A* from memory; 2 grid/graph problems daily.\\",
          r"Week 2&Units III--IV; implement unification and Naïve Bayes from scratch; practise Bayes' rule numericals aloud.\\",
          r"Week 3&Unit V; build one end-to-end ML project with a model card; practise two design questions per day.\\",
          r"Week 4&Mock interviews in pairs using this handbook; polish GitHub portfolio and resume bullets with numbers.\\\bottomrule",
          r"\end{tabularx}", r"\newpage"]
    for u in Q:
        L.append(rf"\unitbanner{{{u}}}{{{tex(TITLES[u])}}}{{15 Questions \textbullet\ {CO[u]}}}")
        L.append(skills_block(u))
        for rnd in ("Concept", "Coding", "Design", "Scenario"):
            L.append(rf"\subsection*{{\color{{{ROUND_COL[rnd]}}}{rnd} round}}")
            for i, q in enumerate(Q[u], 1):
                if q[0] == rnd: L.append(qa_box(u, i, q))
        L.append(r"\newpage")
    L += [r"\section*{Solved Coding Problems}",
          r"All ten solutions are executed with tests in \texttt{07\_Interview\_Prep/Interview\_Coding\_Solutions.ipynb}.",
          ]
    outs = json.load(open(os.path.join(OUT, "outputs.json"))) if os.path.exists(os.path.join(OUT, "outputs.json")) else [""] * len(PROBLEMS)
    for k, (u, title, prompt, code) in enumerate(PROBLEMS, 1):
        clean = code.replace("✓", "[ok]").replace("→", "->").replace("⊨", "|=").replace("·", ".").replace("−", "-")
        out = outs[k - 1].replace("✓", "[ok]").replace("→", "->").replace("⊨", "|=").replace("·", ".")
        L += [rf"\subsection*{{C{k:02d}. {tex(title)} \hfill\co{{Unit {u}}}}}", rf"\textit{{{tex(prompt)}}}",
              r"\begin{lstlisting}[style=py]", clean, r"\end{lstlisting}"]
        if out.strip():
            L += [r"\noindent{\small\bfseries\color{gold!70!black}Output}", r"\begin{lstlisting}[style=out]", out.strip(), r"\end{lstlisting}"]
    L += [r"\section*{Final checklist before an AI interview}",
          r"\begin{itemize}\item Can you code BFS, Dijkstra/UCS and A* in 15 minutes each, with complexity?",
          r"\item Can you explain admissible vs consistent heuristics with an example?",
          r"\item Can you compute a Bayes' rule posterior and explain the base-rate effect?",
          r"\item Can you compute entropy and information gain by hand?",
          r"\item Can you explain precision, recall, overfitting and how you would monitor a deployed model?",
          r"\item Do you have two GitHub projects with a README, results and a responsible-AI note?\end{itemize}",
          r"\end{document}"]
    return "\n".join(L)

def markdown():
    L = ["# 26UAMPC204 Artificial Intelligence — Interview & Industry-Skills Handbook", "",
         "> Practice questions written for this course, modelled on topics and formats commonly discussed for AI/ML and software-engineering interviews at product companies, AI labs, start-ups and IT-services / GCC firms. They are not verbatim questions from any specific company.", ""]
    for u in Q:
        s = SKILLS[u]
        L += [f"## Unit {u}: {TITLES[u]} ({CO[u]})", "", "### 🚀 Top industry skills you gain", ""]
        L += [f"- {x}" for x in s["skills"]]
        L += ["", f"**Tools:** {', '.join(s['tools'])}  ", f"**Job roles:** {', '.join(s['roles'])}  ", f"**Portfolio output:** {s['portfolio']}", "",
              "### 🎯 Interview questions with model answers", ""]
        for i, (rnd, diff, track, q, a) in enumerate(Q[u], 1):
            L += [f"<details><summary><b>Q{u}.{i:02d}</b> [{rnd} · {diff} · {track}] {q}</summary>", "", a, "", "</details>", ""]
    L += ["## 💻 Solved coding problems", "", "See [Interview_Coding_Solutions.ipynb](Interview_Coding_Solutions.ipynb) for executed solutions with tests.", ""]
    for k, (u, title, prompt, _) in enumerate(PROBLEMS, 1):
        L.append(f"{k}. **{title}** (Unit {u}) — {prompt}")
    return "\n".join(L) + "\n"

# ---------------------------------------------------------------- unit notes inserts
def notes_insert(u):
    idx = list(enumerate(Q[u], 1))
    picks = [p for p in idx if p[1][0] in ("Concept", "Coding")][:3] + [p for p in idx if p[1][0] in ("Design", "Scenario")][:2]
    L = [r"\section{Industry Readiness: Skills \& Interview Corner}", skills_block(u),
         r"\subsection*{Interview corner --- top AI company style questions}",
         r"{\small\color{slate}Practice questions modelled on common AI/ML interview formats; full set of 15 with model answers in \texttt{07\_Interview\_Prep}.}"]
    for i, q in picks:
        L.append(qa_box(u, i, q))
    return "\n".join(L)

# ---------------------------------------------------------------- PPT data
def ppt_json():
    d = {}
    for u in Q:
        s = SKILLS[u]
        picks = [Q[u][0], [q for q in Q[u] if q[0] == "Coding"][0], [q for q in Q[u] if q[0] == "Design"][0]]
        d[u] = {"skills": s["skills"][:6], "roles": s["roles"], "tools": s["tools"], "portfolio": s["portfolio"],
                "interview": [[q[0], q[1], q[2], q[3]] for q in picks]}
    return d

# ---------------------------------------------------------------- notebook
def notebook():
    import nbformat
    from nbclient import NotebookClient
    from nb_common import box
    nb = nbformat.v4.new_notebook(); nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    LOGO = "https://raw.githubusercontent.com/drssnaiml1-cell/26UAMPC204-Artificial-Intelligence/main/assets/logo.png"
    nb.cells.append(nbformat.v4.new_markdown_cell(f'''<div style="background:#0B1F4B;padding:22px 26px;border-radius:12px;border:3px solid #C9A227;font-family:'Times New Roman',serif">
<img src="{LOGO}" alt="Sanjivani University" width="92" style="float:right;background:#FFFFFF;border:2px solid #C9A227;border-radius:8px;padding:3px;margin-left:14px">
<div style="color:#C9A227;font-size:14px;letter-spacing:2px;font-weight:bold">26UAMPC204 · ARTIFICIAL INTELLIGENCE · INTERVIEW PREP</div>
<div style="color:#FFFFFF;font-size:30px;font-weight:bold;margin-top:6px">10 Solved Coding Interview Problems</div>
<div style="color:#F6EBC8;font-size:15px;margin-top:8px">Two per unit · each solution is tested with <code>assert</code> · state complexity aloud in the interview</div>
<div style="clear:both"></div></div>'''))
    for k, (u, title, prompt, code) in enumerate(PROBLEMS, 1):
        nb.cells.append(nbformat.v4.new_markdown_cell(f"## C{k:02d} · {title}  <span style='color:#C9A227'>(Unit {u})</span>\n\n" +
                                                      box("Problem", prompt, "#1F3A7A", "#EEF2F8")))
        nb.cells.append(nbformat.v4.new_code_cell(code))
    NotebookClient(nb, timeout=300, kernel_name="python3", resources={"metadata": {"path": OUT}}).execute()
    nbformat.write(nb, os.path.join(OUT, "Interview_Coding_Solutions.ipynb"))
    outs = ["".join(o.get("text", "") for o in c.get("outputs", []) if o.get("output_type") == "stream")
            for c in nb.cells if c.cell_type == "code"]
    json.dump(outs, open(os.path.join(OUT, "outputs.json"), "w"), indent=1, ensure_ascii=False)
    py = ['"""26UAMPC204 Artificial Intelligence — 10 solved coding interview problems (2 per unit)."""']
    for k, (u, title, prompt, code) in enumerate(PROBLEMS, 1):
        py.append(f"# {'=' * 70}\n# C{k:02d} (Unit {u}): {title}\n# {prompt}\n# {'=' * 70}\n{code}")
    open(os.path.join(OUT, "Interview_Coding_Solutions.py"), "w").write("\n\n".join(py) + "\n")
    print("✓ coding notebook executed")

if __name__ == "__main__":
    notebook()
    open(os.path.join(OUT, "AI_Interview_Skills_Handbook.tex"), "w").write(handbook())
    open(os.path.join(OUT, "AI_Interview_Skills_Handbook.md"), "w").write(markdown())
    open(os.path.join(OUT, "README.md"), "w").write(markdown())
    for k, u in enumerate(Q, 1):
        open(os.path.join(ROOT, "01_Unit_Notes", "latex", f"unit{k}_industry.tex"), "w").write(notes_insert(u))
    json.dump(ppt_json(), open(os.path.join(ROOT, "02_PPT", "src", "industry.json"), "w"), indent=1, ensure_ascii=False)
    print("✓ handbook, markdown, notes inserts and PPT data written")
