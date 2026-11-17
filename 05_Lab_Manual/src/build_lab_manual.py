"""Build the Lab Manual (LaTeX) from the experiment definitions and executed notebook outputs.
Run from repo root:  python 05_Lab_Manual/src/build_lab_manual.py
Animations: GIF frames are embedded with the LaTeX `animate` package (play in Adobe Acrobat Reader);
other viewers show the first frame.
"""
import os, sys, json, re, glob
from PIL import Image, ImageSequence
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "06_Notebooks", "src"))
from exp_defs_a import EXP1, EXP2, EXP3, EXP4, EXP5
from exp_defs_b import EXP6, EXP7, EXP8, EXP9, EXP10
EXPS = [EXP1, EXP2, EXP3, EXP4, EXP5, EXP6, EXP7, EXP8, EXP9, EXP10]
LM = os.path.join(ROOT, "05_Lab_Manual")
FR = os.path.join(LM, "frames")

SYM = {"α": r"$\alpha$", "β": r"$\beta$", "θ": r"$\theta$", "≥": r"$\ge$", "≤": r"$\le$", "→": r"$\to$", "⇒": r"$\Rightarrow$",
       "¬": r"$\neg$", "∨": r"$\vee$", "∧": r"$\wedge$", "⊨": r"$\models$", "−": "--", "–": "--", "—": "---", "×": r"$\times$",
       "≈": r"$\approx$", "□": r"$\square$", "’": "'", "…": r"\dots{}"}
def tex(s):
    out, parts = [], re.split(r"(\$[^$]+\$)", s)          # keep inline math untouched
    for i, p in enumerate(parts):
        if i % 2:
            out.append(p); continue
        p = p.replace("\\", "\\textbackslash{}") if False else p
        for a, b in (("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_")):
            p = p.replace(a, b)
        p = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", p)
        p = re.sub(r"(?<![\w*])\*(?!\s)(.+?)\*(?!\w)", r"\\emph{\1}", p)
        for a, b in SYM.items():
            p = p.replace(a, b)
        out.append(p)
    return "".join(out).replace("\n", "\n\n")

CLEAN = {"👤": "User:", "🤖": "Bot:", "✓": "[ok]", "♛": "Q", "⟹": "=>", "⊨": "|=", "∀": "forall ", "∃": "exists ",
         "→": "->", "⇒": "=>", "¬": "~", "∨": "|", "∧": "&", "□": "[]", "α": "alpha", "θ": "theta", "≈": "~=", "≥": ">=",
         "≤": "<=", "—": "--", "–": "-", "·": ".", "°": " deg", "…": "...", "’": "'", "×": "x", "−": "-", "•": "*"}
NONASCII = set()
def clean_code(s):
    for a, b in CLEAN.items():
        s = s.replace(a, b)
    NONASCII.update(ch for ch in s if ord(ch) > 127)
    return "".join(ch if ord(ch) < 128 else "?" for ch in s)

def gif_frames(name, maxf=14):
    path = os.path.join(ROOT, "assets", "animations", name)
    im = Image.open(path); frames = [f.copy().convert("RGB") for f in ImageSequence.Iterator(im)]
    step = max(1, len(frames) // maxf); sel = frames[::step][:maxf]
    if sel[-1] is not frames[-1]: sel.append(frames[-1])
    d = os.path.join(FR, name[:-4]); os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, "*.png")): os.remove(f)
    for i, f in enumerate(sel):
        f.thumbnail((900, 900)); f.save(os.path.join(d, f"f-{i}.png"))
    return d, len(sel)

def experiment(e):
    name = f"Exp{e['num']:02d}_{e['slug']}"
    outs = json.load(open(os.path.join(ROOT, "06_Notebooks", "outputs", name + ".json")))[1:]
    codes = [c for k, c in e["cells"] if k == "code"]
    L = [r"\newpage", rf"\section*{{Experiment {e['num']}: {tex(e['title'])}}}",
         rf"\noindent\co{{{e['co']}}}\ \btl{{L3 Apply}}\ \btl{{L4 Analyse}}\hfill\textbf{{\color{{navy}}Date:}}\ \rule{{3cm}}{{0.4pt}}\quad\textbf{{\color{{navy}}Sign:}}\ \rule{{3cm}}{{0.4pt}}\par\medskip",
         rf"\begin{{keypoint}}[Aim]{tex(e['aim'])}\end{{keypoint}}",
         r"\subsection*{Theory}", tex(e["theory"]),
         r"\subsection*{Algorithm}", r"\begin{algo}[Procedure]\begin{enumerate}"]
    L += [rf"\item {tex(s)}" for s in e["algorithm"]]
    L += [r"\end{enumerate}\end{algo}", r"\subsection*{Program (Python 3)}",
          rf"{{\small\color{{slate}}Notebook: \texttt{{06\_Notebooks/{name.replace('_', chr(92)+'_')}.ipynb}}\\ Script: \texttt{{06\_Notebooks/python/{name.replace('_', chr(92)+'_')}.py}}}}"]
    for i, c in enumerate(codes):
        L += [r"\begin{lstlisting}[style=py]", clean_code(c), r"\end{lstlisting}"]
        o = outs[i] if i < len(outs) else ""
        if o.strip():
            o = "\n".join(l[:105] for l in clean_code(o).strip().splitlines()[:40])
            L += [r"\noindent{\small\bfseries\color{gold!70!black}Output}", r"\begin{lstlisting}[style=out]", o, r"\end{lstlisting}"]
    figs = sorted(glob.glob(os.path.join(ROOT, "assets", "figures", f"exp{e['num']:02d}_*.png")))
    gifs = sorted(glob.glob(os.path.join(ROOT, "assets", "animations", f"exp{e['num']:02d}_*.gif")))
    if figs or gifs:
        L.append(r"\subsection*{Output Figures and Animation}")
    for g in gifs:
        d, n = gif_frames(os.path.basename(g))
        rel = os.path.relpath(d, LM).replace("\\", "/")
        L += [r"\begin{center}",
              rf"\animategraphics[controls,loop,autoplay,width=0.62\linewidth]{{2}}{{{rel}/f-}}{{0}}{{{n-1}}}\\",
              rf"{{\small\color{{slate}}\textbf{{Animation}} ({n} frames; plays in Adobe Acrobat Reader). GIF: \texttt{{assets/animations/{os.path.basename(g).replace('_', chr(92)+'_')}}}}}",
              r"\end{center}"]
    for f in figs:
        rel = os.path.relpath(f, LM).replace("\\", "/")
        L += [r"\begin{center}", rf"\includegraphics[width=0.78\linewidth,height=0.32\textheight,keepaspectratio]{{{rel}}}", r"\end{center}"]
    L += [r"\subsection*{Result}", rf"\begin{{outcome}}[Result \& Conclusion]{tex(e['conclusion'])}\end{{outcome}}",
          r"\subsection*{Viva-Voce Questions}", r"\begin{enumerate}"] + [rf"\item {tex(q)}" for q in e["viva"]] + [r"\end{enumerate}"]
    return "\n".join(L)

def main():
    rows = "\n".join((r"\rowcolor{ivory}" if e["num"] % 2 == 0 else "") +
                     rf"{e['num']}&{tex(e['title'])}&{e['co']}&\pageref{{exp{e['num']}}}&&\\" for e in EXPS)
    doc = [r"\documentclass[11pt]{article}", r"\usepackage{../common/ai204}", r"\usepackage{animate}",
           r"\renewcommand{\doctitle}{Laboratory Manual}", r"\begin{document}",
           r"\aicover{Laboratory Manual}{10 experiments \textbullet\ Python 3 \textbullet\ executed Jupyter notebooks with outputs \textbullet\ animated algorithm visualisations}{For DSY -- AI \& ML students \textbullet\ Integrated Theory + Practical (2-0-2)}",
           r"\section*{Certificate}",
           r"\begin{tcolorbox}[enhanced,colback=ivory,colframe=gold,boxrule=1.2pt,arc=3mm,left=8mm,right=8mm,top=6mm,bottom=6mm]",
           r"\large This is to certify that Mr./Ms.\ \rule{7cm}{0.4pt}\ Roll No.\ \rule{2.5cm}{0.4pt}\ of class \rule{3cm}{0.4pt}\ has satisfactorily completed the experiments in \textbf{26UAMPC204 Artificial Intelligence Laboratory} during the academic year 2026--27.\\[3cm]",
           r"\rule{4.5cm}{0.4pt}\hfill\rule{4.5cm}{0.4pt}\hfill\rule{4.5cm}{0.4pt}\\ Course Faculty\hfill Head of Department\hfill External Examiner",
           r"\end{tcolorbox}",
           r"\section*{Laboratory Instructions}",
           r"\begin{itemize}\item Install Python 3.10+ and run \texttt{pip install -r requirements.txt} from the repository root.",
           r"\item Open each notebook in Jupyter or VS Code, run all cells, and compare your output with the output printed in this manual.",
           r"\item Write the aim, algorithm, program, output and result in your journal; attach the printed figures.",
           r"\item Each experiment carries 10 marks: performance 4, journal 3, viva 3.",
           r"\item Animations play inside this PDF in Adobe Acrobat Reader; GIF versions are in \texttt{assets/animations}.\end{itemize}",
           r"\section*{Index of Experiments}",
           r"\begin{center}\begin{tabular}{c p{8.6cm} c c p{1.6cm} p{1.6cm}}",
           r"\rowcolor{navy}\textcolor{gold}{\textbf{No.}}&\textcolor{gold}{\textbf{Title}}&\textcolor{gold}{\textbf{CO}}&\textcolor{gold}{\textbf{Page}}&\textcolor{gold}{\textbf{Date}}&\textcolor{gold}{\textbf{Sign}}\\",
           rows, r"\end{tabular}\end{center}",
           r"\section*{Course Outcomes}",
           r"\begin{tabularx}{\linewidth}{>{\bfseries\color{navy}}l X}\toprule",
           r"CO204.1&Explain the foundations of AI and intelligent agents and formulate problems as state-space search.\\",
           r"CO204.2&Apply uninformed, informed, local and adversarial search, and constraint satisfaction.\\",
           r"CO204.3&Represent knowledge and perform inference in propositional and first-order logic.\\",
           r"CO204.4&Apply classical planning and reasoning under uncertainty (probability, Bayesian networks, fuzzy logic).\\",
           r"CO204.5&Illustrate learning, expert systems and applications of AI with awareness of ethical issues.\\\bottomrule",
           r"\end{tabularx}"]
    for e in EXPS:
        doc.append(experiment(e).replace(rf"\section{{Experiment {e['num']}:", rf"\section{{Experiment {e['num']}:", 1)
                   + "\n" + rf"\label{{exp{e['num']}}}")
    doc.append(r"\end{document}")
    txt = "\n".join(doc)
    # put the label right after each section heading (so \pageref points to the start)
    for e in EXPS:
        txt = txt.replace("\n" + rf"\label{{exp{e['num']}}}", "")
        txt = txt.replace(rf"\section{{Experiment {e['num']}: ", rf"\section{{Experiment {e['num']}: ", 1)
        head = rf"\section*{{Experiment {e['num']}: {tex(e['title'])}}}"
        txt = txt.replace(head, head + rf"\label{{exp{e['num']}}}", 1)
    open(os.path.join(LM, "AI_Lab_Manual_26UAMPC204.tex"), "w").write(txt)
    print("lab manual tex written; unmapped non-ASCII in code:", NONASCII)

if __name__ == "__main__":
    main()
