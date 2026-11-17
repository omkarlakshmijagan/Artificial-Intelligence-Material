"""Assemble, execute and save the 10 lab notebooks (with outputs) + plain .py scripts.
Run:  python 06_Notebooks/src/build_notebooks.py [exp numbers...]
"""
import os, sys, json, nbformat
from nbclient import NotebookClient
HERE = os.path.dirname(os.path.abspath(__file__))
NB_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from nb_common import SETUP, header, box
from exp_defs_a import EXP1, EXP2, EXP3, EXP4, EXP5
from exp_defs_b import EXP6, EXP7, EXP8, EXP9, EXP10
EXPS = [EXP1, EXP2, EXP3, EXP4, EXP5, EXP6, EXP7, EXP8, EXP9, EXP10]

def build(e):
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    C = nb.cells
    C.append(nbformat.v4.new_markdown_cell(header(e["num"], e["title"], e["co"], e["aim"])))
    C.append(nbformat.v4.new_markdown_cell("## 📘 Theory\n\n" + e["theory"]))
    C.append(nbformat.v4.new_markdown_cell("## 🧭 Algorithm\n\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(e["algorithm"], 1))))
    C.append(nbformat.v4.new_markdown_cell("## ⚙️ Setup"))
    C.append(nbformat.v4.new_code_cell(SETUP))
    C.append(nbformat.v4.new_markdown_cell("## 💻 Implementation and Output"))
    for kind, src in e["cells"]:
        C.append(nbformat.v4.new_markdown_cell(src) if kind == "md" else nbformat.v4.new_code_cell(src))
    C.append(nbformat.v4.new_markdown_cell("## ✅ Result and Conclusion\n\n" + box("Conclusion", e["conclusion"], "#2E7D32", "#E3F2E4")))
    C.append(nbformat.v4.new_markdown_cell("## 🎤 Viva Questions\n\n" + "\n".join(f"{i}. {q}" for i, q in enumerate(e["viva"], 1))))
    name = f"Exp{e['num']:02d}_{e['slug']}"
    NotebookClient(nb, timeout=900, kernel_name="python3", resources={"metadata": {"path": NB_DIR}}).execute()
    nbformat.write(nb, os.path.join(NB_DIR, name + ".ipynb"))
    # plain python script
    py = [f'"""Experiment {e["num"]}: {e["title"]}\nAim: {e["aim"]}\n26UAMPC204 Artificial Intelligence Lab, Sanjivani University\n"""',
          SETUP.replace('matplotlib.use("Agg")', 'matplotlib.use("Agg")  # figures/GIFs are saved to assets/')
                .replace('os.path.join("..", "assets"', 'os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"')
                .replace("from IPython.display import Image, display", "display = Image = lambda *a, **k: None")]
    py += [src for kind, src in e["cells"] if kind == "code"]
    os.makedirs(os.path.join(NB_DIR, "python"), exist_ok=True)
    open(os.path.join(NB_DIR, "python", name + ".py"), "w").write("\n\n".join(py).replace("display(Image(filename=gif))", "print('animation saved:', gif)") + "\n")
    # dump text outputs for the lab manual
    outs = []
    for c in nb.cells:
        if c.cell_type == "code":
            txt = "".join(o.get("text", "") for o in c.get("outputs", []) if o.get("output_type") == "stream")
            errs = [o for o in c.get("outputs", []) if o.get("output_type") == "error"]
            if errs: raise RuntimeError(f"{name}: {errs[0]['ename']} {errs[0]['evalue']}")
            outs.append(txt)
    os.makedirs(os.path.join(NB_DIR, "outputs"), exist_ok=True)
    json.dump(outs, open(os.path.join(NB_DIR, "outputs", name + ".json"), "w"), indent=1, ensure_ascii=False)
    print("✓", name)

if __name__ == "__main__":
    sel = [int(a) for a in sys.argv[1:]] or range(1, 11)
    for e in EXPS:
        if e["num"] in sel:
            build(e)
