"""Add slide transitions and staged entrance animations to the generated decks.

Shapes are named  anim{step}_{part}  by build.js. Every step fades/zooms in
automatically after the previous one (no clicks needed); parts of one step
appear together. Each slide also gets a Fade transition (cover gets Push).
Usage: python animate.py deck1.pptx [deck2.pptx ...]
"""
import re, sys, zipfile, shutil, os, tempfile

EFFECTS = {  # presetID, filter for <p:animEffect>
    "fade": (10, "fade"),
    "wipe": (22, "wipe(left)"),
    "zoom": (53, "fade"),
}

def shape_ids(xml):
    """Return {step: [spid,...]} from cNvPr name="animK_x"."""
    steps = {}
    for m in re.finditer(r'<p:cNvPr id="(\d+)" name="anim(\d+)_[a-z]"', xml):
        steps.setdefault(int(m.group(2)), []).append(m.group(1))
    return dict(sorted(steps.items()))

def effect_xml(ids, spid, node_type, dur, kind):
    preset, filt = EFFECTS[kind]
    a, b, c = next(ids), next(ids), next(ids)
    scale = ""
    if kind == "zoom":
        d1, d2 = next(ids), next(ids)
        scale = (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{d1}" dur="{dur}" fill="hold"/>'
                 f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_w</p:attrName></p:attrNameLst></p:cBhvr>'
                 f'<p:tavLst><p:tav tm="0"><p:val><p:strVal val="#ppt_w*0.70"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="#ppt_w"/></p:val></p:tav></p:tavLst></p:anim>'
                 f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{d2}" dur="{dur}" fill="hold"/>'
                 f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_h</p:attrName></p:attrNameLst></p:cBhvr>'
                 f'<p:tavLst><p:tav tm="0"><p:val><p:strVal val="#ppt_h*0.70"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="#ppt_h"/></p:val></p:tav></p:tavLst></p:anim>')
    return (f'<p:par><p:cTn id="{a}" presetID="{preset}" presetClass="entr" presetSubtype="{8 if kind=="wipe" else (16 if kind=="zoom" else 0)}" fill="hold" nodeType="{node_type}">'
            f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:set><p:cBhvr><p:cTn id="{b}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
            f'<p:to><p:strVal val="visible"/></p:to></p:set>'
            f'<p:animEffect transition="in" filter="{filt}"><p:cBhvr><p:cTn id="{c}" dur="{dur}"/>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>{scale}'
            f'</p:childTnLst></p:cTn></p:par>')

def timing_xml(steps, kind="fade", dur=450, gap=150):
    ids = iter(range(3, 10_000))
    groups, t = [], 0
    for k, (step, spids) in enumerate(steps.items()):
        gid = next(ids)
        inner = "".join(effect_xml(ids, sp, "afterEffect" if j == 0 else "withEffect", dur, kind)
                        for j, sp in enumerate(spids))
        groups.append(f'<p:par><p:cTn id="{gid}" fill="hold"><p:stCondLst><p:cond delay="{t}"/></p:stCondLst>'
                      f'<p:childTnLst>{inner}</p:childTnLst></p:cTn></p:par>')
        t += dur + gap
    click = next(ids)
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            f'<p:par><p:cTn id="{click}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
            '<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
            + "".join(groups) +
            '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
            '</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')

def process(path):
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(path) as z:
        z.extractall(tmp)
        names = z.namelist()
    sdir = os.path.join(tmp, "ppt", "slides")
    n_anim = 0
    for f in sorted(os.listdir(sdir)):
        if not f.endswith(".xml"):
            continue
        p = os.path.join(sdir, f)
        xml = open(p, encoding="utf-8").read()
        xml = re.sub(r"<p:transition.*?</p:transition>|<p:transition[^>]*/>", "", xml, flags=re.S)
        xml = re.sub(r"<p:timing>.*?</p:timing>", "", xml, flags=re.S)
        num = int(re.findall(r"\d+", f)[0])
        trans = '<p:transition spd="slow"><p:push dir="u"/></p:transition>' if num == 1 else \
                '<p:transition spd="med"><p:fade/></p:transition>'
        steps = shape_ids(xml)
        kind = "zoom" if num % 3 == 0 else ("wipe" if num % 3 == 1 and num > 1 else "fade")
        add = trans + (timing_xml(steps, kind) if steps else "")
        if steps:
            n_anim += 1
        xml = xml.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + add, 1) if "</p:clrMapOvr>" in xml \
            else xml.replace("</p:cSld>", "</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>" + add, 1)
        open(p, "w", encoding="utf-8").write(xml)
    out = path + ".tmp"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.write(os.path.join(tmp, n), n)
    shutil.move(out, path)
    shutil.rmtree(tmp)
    print(f"{os.path.basename(path)}: animated {n_anim} slides")

if __name__ == "__main__":
    for d in sys.argv[1:]:
        process(d)
