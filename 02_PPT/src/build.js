// Build animated unit decks for 26UAMPC204 Artificial Intelligence
// node build.js  → ../Unit_N_AI_26UAMPC204.pptx  (animations added afterwards by animate.py)
const pptxgen = require("pptxgenjs");
const path = require("path");
const units = require("./units.js");
const INDUSTRY = require("./industry.json");
// Optional: set PPTX_SKILL to a folder containing scripts/apply_theme.js to write theme colours into the deck.
let applyTheme = async () => {};
try { if (process.env.PPTX_SKILL) applyTheme = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js").applyTheme; } catch (e) {}

const NAVY = "0B1F4B", NAVY2 = "1F3A7A", GOLD = "C9A227", GOLDL = "F6EBC8", TEAL = "0E7C86",
      TEALL = "DDF1F2", CRIM = "A4243B", LEAF = "2E7D32", INK = "1A202C", SLATE = "4A5568", MIST = "EEF2F8", WHITE = "FFFFFF";
const FONT = "Times New Roman";
const ACC = [NAVY2, TEAL, GOLD, CRIM, LEAF, "6B46C1", "C05621", "2B6CB0"];

const THEME = { name: "AI204 Navy Gold", headFontFace: FONT, bodyFontFace: FONT,
  colors: { dk1: INK, lt1: WHITE, dk2: NAVY, lt2: MIST, accent1: NAVY2, accent2: GOLD, accent3: TEAL,
            accent4: CRIM, accent5: LEAF, accent6: "6B46C1", hlink: TEAL, folHlink: "6B46C1" } };

const W = 13.333, H = 7.5;
const LOGO = path.join(__dirname, "..", "..", "assets", "logo.png");

async function buildUnit(u, idx) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.author = "Dr. S. Satyanarayana";
  pres.company = "Sanjivani University";
  pres.title = `26UAMPC204 Unit ${u.num}: ${u.title}`;
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };

  const footer = `26UAMPC204 Artificial Intelligence  •  Unit ${u.num}  •  ${u.co}`;
  pres.defineSlideMaster({ title: "CONTENT", background: { color: WHITE },
    objects: [
      { text: { text: footer, options: { x: 0.6, y: 7.0, w: 8, h: 0.3, fontFace: FONT, fontSize: 10, color: SLATE, isTextBox: true, margin: 0 } } },
      { text: { text: "Sanjivani University  •  Dept. of AI & DS", options: { x: 7.9, y: 7.0, w: 4.2, h: 0.3, fontFace: FONT, fontSize: 10, color: SLATE, align: "right", isTextBox: true, margin: 0 } } },
      { image: { path: LOGO, x: 12.0, y: 0.3, w: 0.85, h: 0.85, altText: "Sanjivani University logo" } },
      { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 11.2, h: 0.9, fontFace: FONT, fontSize: 34, bold: true, color: NAVY, valign: "middle", margin: 0 }, text: "" } } ],
    slideNumber: { x: 12.3, y: 6.98, w: 0.5, h: 0.32, fontFace: FONT, fontSize: 10, color: NAVY, bold: true, align: "right" } });
  pres.defineSlideMaster({ title: "DARK", background: { color: NAVY },
    objects: [
      { rect: { x: 11.93, y: 0.43, w: 0.99, h: 0.99, fill: { color: WHITE }, line: { color: GOLD, width: 1.5 } } },
      { image: { path: LOGO, x: 12.0, y: 0.5, w: 0.85, h: 0.85, altText: "Sanjivani University logo" } },
      { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 0.5, w: 10.8, h: 1.0, fontFace: FONT, fontSize: 36, bold: true, color: GOLD, valign: "middle", margin: 0 }, text: "" } } ],
    slideNumber: { x: 12.3, y: 6.98, w: 0.5, h: 0.32, fontFace: FONT, fontSize: 10, color: GOLD, align: "right" } });

  pres.defineSlideMaster({ title: "COVER", background: { color: NAVY }, objects: [] });
  // ---------- Cover ----------
  pres.addSection({ title: "Opening" });
  let s = pres.addSlide({ masterName: "COVER", sectionTitle: "Opening" });
  for (let i = 0; i < 7; i++) s.addShape(pres.shapes.OVAL, { x: 9.2 - i * 0.25, y: -2.2 - i * 0.25, w: 6 + i * 0.5, h: 6 + i * 0.5, fill: { color: NAVY, transparency: 100 }, line: { color: GOLD, width: 0.75, transparency: 55 + i * 5 } });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.72, y: 0.52, w: 1.46, h: 1.46, rectRadius: 0.08, fill: { color: WHITE }, line: { color: GOLD, width: 2 } });
  s.addImage({ path: LOGO, x: 0.8, y: 0.6, w: 1.3, h: 1.3, altText: "Sanjivani University logo" });
  s.addText([{ text: "SANJIVANI UNIVERSITY", options: { fontSize: 24, bold: true, color: WHITE, breakLine: true } },
             { text: "Department of Artificial Intelligence & Data Science", options: { fontSize: 15, color: GOLD } }],
    { x: 2.45, y: 0.75, w: 8, h: 1.0, fontFace: FONT, isTextBox: true, margin: 0, valign: "middle" });
  s.addText(`26UAMPC204  •  ARTIFICIAL INTELLIGENCE  •  UNIT ${u.num}`, { x: 0.8, y: 2.55, w: 11, h: 0.45, fontFace: FONT, fontSize: 16, bold: true, color: GOLD, charSpacing: 2, isTextBox: true, margin: 0, objectName: "anim1_a" });
  s.addText(u.title, { x: 0.8, y: 3.05, w: 11.5, h: 1.7, fontFace: FONT, fontSize: 46, bold: true, color: WHITE, valign: "top", isTextBox: true, margin: 0, objectName: "anim2_a" });
  s.addText(u.tagline, { x: 0.8, y: 4.85, w: 11, h: 0.5, fontFace: FONT, fontSize: 20, italic: true, color: "D9E2F3", isTextBox: true, margin: 0, objectName: "anim3_a" });
  s.addText([{ text: "Dr. S. Satyanarayana, Ph.D., PDF (AI)", options: { fontSize: 16, bold: true, color: WHITE, breakLine: true } },
             { text: "Professor & Advisor, AI & Data Science  •  Academic Year 2026–27", options: { fontSize: 13, color: GOLD } }],
    { x: 0.8, y: 6.15, w: 9, h: 0.8, fontFace: FONT, isTextBox: true, margin: 0 });
  s.addText(u.co, { x: 10.6, y: 6.3, w: 1.9, h: 0.5, fontFace: FONT, fontSize: 14, bold: true, color: NAVY, align: "center", valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, fill: { color: GOLD }, isTextBox: true });
  s.addNotes(`Unit ${u.num} opener. ${u.title}. Outcome ${u.co}.`);

  pres.addSection({ title: "Core concepts" });
  u.slides.forEach((sd, k) => {
    const dark = sd.type === "summary";
    const sl = pres.addSlide({ masterName: dark ? "DARK" : "CONTENT", sectionTitle: dark ? "Core concepts" : "Core concepts" });
    sl.addText(dark ? "Key takeaways" : sd.title, { placeholder: "title" });
    RENDER[sd.type](pres, sl, sd);
    sl.addNotes(notesFor(sd));
  });

  // ---------- Industry readiness ----------
  const ind = INDUSTRY[u.num];
  if (ind) {
    pres.addSection({ title: "Industry readiness" });
    let k1 = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Industry readiness" });
    k1.addText("Top industry skills you gain", { placeholder: "title" });
    ind.skills.forEach((t, i) => {
      const x = 0.6 + (i % 3) * 4.1, y = 1.5 + Math.floor(i / 3) * 1.85, col = ACC[i % ACC.length];
      k1.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 3.85, h: 1.6, rectRadius: 0.1, fill: { color: MIST }, line: { color: "D5DCE8" }, objectName: `anim${i + 1}_a` });
      k1.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.5, w: 0.6, h: 0.6, fill: { color: col }, line: { color: col }, objectName: `anim${i + 1}_b` });
      k1.addText("✓", { x: x + 0.2, y: y + 0.5, w: 0.6, h: 0.6, fontFace: FONT, fontSize: 18, bold: true, color: WHITE, align: "center", valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_c` });
      k1.addText(t, { x: x + 0.95, y, w: 2.75, h: 1.6, fontFace: FONT, fontSize: 15, color: INK, valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_d` });
    });
    k1.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 5.35, w: 12.1, h: 1.4, rectRadius: 0.1, fill: { color: NAVY }, line: { color: GOLD, width: 1.5 }, objectName: "anim7_a" });
    k1.addText([{ text: "Job roles  ", options: { bold: true, color: GOLD } }, { text: ind.roles.join("  •  "), options: { color: WHITE, breakLine: true } },
                { text: "Tools  ", options: { bold: true, color: GOLD } }, { text: ind.tools.join("  •  "), options: { color: WHITE } }],
      { x: 0.9, y: 5.4, w: 11.6, h: 1.3, fontFace: FONT, fontSize: 15, valign: "middle", paraSpaceAfter: 6, isTextBox: true, margin: 0, objectName: "anim7_b" });
    k1.addNotes("Skills, tools and job roles this unit prepares you for. Portfolio output: " + ind.portfolio);

    let k2 = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Industry readiness" });
    k2.addText("Interview corner: top AI company style", { placeholder: "title" });
    const RC = { Concept: TEAL, Coding: NAVY2, Design: CRIM, Scenario: LEAF };
    ind.interview.forEach(([rnd, diff, track, q], i) => {
      const y = 1.55 + i * 1.62, col = RC[rnd] || NAVY2;
      k2.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y, w: 12.1, h: 1.42, rectRadius: 0.1, fill: { color: i % 2 ? MIST : WHITE }, line: { color: col, width: 1.25 }, objectName: `anim${i + 1}_a` });
      k2.addText(rnd.toUpperCase(), { x: 0.85, y: y + 0.2, w: 1.6, h: 0.42, fontFace: FONT, fontSize: 12, bold: true, color: WHITE, align: "center", valign: "middle",
        shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, fill: { color: col }, isTextBox: true, margin: 0, objectName: `anim${i + 1}_b` });
      k2.addText(`${diff} • ${track}`, { x: 0.85, y: y + 0.75, w: 1.6, h: 0.5, fontFace: FONT, fontSize: 10, color: SLATE, align: "center", valign: "top", isTextBox: true, margin: 0, objectName: `anim${i + 1}_c` });
      k2.addText(q, { x: 2.7, y, w: 9.8, h: 1.42, fontFace: FONT, fontSize: 17, color: INK, valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_d` });
    });
    k2.addText("Practice questions in common interview formats. Model answers: 07_Interview_Prep handbook.", { x: 0.6, y: 6.45, w: 12.1, h: 0.35, fontFace: FONT, fontSize: 12, italic: true, color: TEAL, isTextBox: true, margin: 0 });
    k2.addNotes("Interview corner. " + ind.interview.map(q => q[3]).join(" "));
  }

  // ---------- Closing ----------
  s = pres.addSlide({ masterName: "DARK", sectionTitle: ind ? "Industry readiness" : "Core concepts" });
  s.addText("Further reading", { placeholder: "title" });
  const refs = ["Russell & Norvig, Artificial Intelligence: A Modern Approach, 4th ed., Pearson (2021)",
                "Rich, Knight & Nair, Artificial Intelligence, 3rd ed., McGraw Hill (2017)",
                "NPTEL: An Introduction to AI — Prof. Mausam, IIT Delhi",
                "Course repository: github.com/drssnaiml1-cell/26UAMPC204-Artificial-Intelligence"];
  refs.forEach((r, i) => {
    s.addShape(pres.shapes.OVAL, { x: 0.9, y: 1.9 + i * 1.05, w: 0.6, h: 0.6, fill: { color: GOLD }, line: { color: GOLD }, objectName: `anim${i + 1}_a` });
    s.addText(String(i + 1), { x: 0.9, y: 1.9 + i * 1.05, w: 0.6, h: 0.6, fontFace: FONT, fontSize: 18, bold: true, color: NAVY, align: "center", valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_b` });
    s.addText(r, { x: 1.8, y: 1.9 + i * 1.05, w: 10.6, h: 0.6, fontFace: FONT, fontSize: 18, color: WHITE, valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_c` });
  });
  s.addText("Lab: see 06_Notebooks — every experiment runs end to end with outputs.", { x: 0.9, y: 6.3, w: 11.5, h: 0.5, fontFace: FONT, fontSize: 15, italic: true, color: GOLD, isTextBox: true, margin: 0 });
  s.addNotes("References and pointers to the lab notebooks.");

  const out = path.join(__dirname, "..", `Unit_${idx + 1}_AI_26UAMPC204.pptx`);
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("wrote", out);
}

function notesFor(sd) {
  const t = sd.items ? sd.items.map(x => Array.isArray(x) ? x.join(": ") : x).join(". ")
          : sd.bullets ? sd.bullets.join(". ") : sd.steps ? sd.steps.map(x => x.join(": ")).join(". ") : sd.caption || "";
  return `${sd.title || "Summary"}. ${t}`;
}

const RENDER = {
  agenda(pres, s, sd) {
    const n = sd.items.length, colW = 5.8;
    sd.items.forEach((it, i) => {
      const c = i < Math.ceil(n / 2) ? 0 : 1, r = c === 0 ? i : i - Math.ceil(n / 2);
      const x = 0.7 + c * 6.2, y = 1.6 + r * 1.25;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: colW, h: 1.0, rectRadius: 0.08, fill: { color: i % 2 ? MIST : GOLDL }, line: { color: i % 2 ? MIST : GOLDL }, objectName: `anim${i + 1}_a` });
      s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.17, w: 0.66, h: 0.66, fill: { color: NAVY }, line: { color: NAVY }, objectName: `anim${i + 1}_b` });
      s.addText(String(i + 1).padStart(2, "0"), { x: x + 0.2, y: y + 0.17, w: 0.66, h: 0.66, fontFace: FONT, fontSize: 16, bold: true, color: GOLD, align: "center", valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_c` });
      s.addText(it, { x: x + 1.05, y, w: colW - 1.2, h: 1.0, fontFace: FONT, fontSize: 20, color: INK, valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_d` });
    });
  },
  cards(pres, s, sd) {
    const cols = sd.cols || 3, n = sd.items.length, rows = Math.ceil(n / cols);
    const gx = 0.3, gy = 0.3, x0 = 0.6, y0 = 1.55, totW = 12.1, totH = 5.2;
    const cw = (totW - gx * (cols - 1)) / cols, ch = (totH - gy * (rows - 1)) / rows;
    sd.items.forEach(([h, b], i) => {
      const x = x0 + (i % cols) * (cw + gx), y = y0 + Math.floor(i / cols) * (ch + gy), col = ACC[i % ACC.length];
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h: ch, rectRadius: 0.1, fill: { color: MIST }, line: { color: "D5DCE8", width: 0.75 },
        shadow: { type: "outer", color: "8A94A6", blur: 6, offset: 2, angle: 90, opacity: 0.25 }, objectName: `anim${i + 1}_a` });
      s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: y + 0.25, w: 0.6, h: 0.6, fill: { color: col }, line: { color: col }, objectName: `anim${i + 1}_b` });
      s.addText(String(i + 1), { x: x + 0.25, y: y + 0.25, w: 0.6, h: 0.6, fontFace: FONT, fontSize: 16, bold: true, color: WHITE, align: "center", valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_c` });
      const big = rows === 1 || (cols <= 2);
      s.addText(h, { x: x + 1.0, y: y + 0.2, w: cw - 1.2, h: 0.7, fontFace: FONT, fontSize: cols >= 4 ? 17 : 20, bold: true, color: NAVY, valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_d` });
      s.addText(b, { x: x + 0.25, y: y + 1.0, w: cw - 0.5, h: ch - 1.15, fontFace: FONT, fontSize: cols >= 4 ? 16 : (big ? 20 : 18), color: INK, valign: "top", isTextBox: true, margin: 0, objectName: `anim${i + 1}_e` });
    });
  },
  twocol(pres, s, sd) {
    s.addText(sd.bullets.map((b, i) => ({ text: b, options: { bullet: { code: "25B8" }, breakLine: i < sd.bullets.length - 1 } })),
      { x: 0.6, y: 1.6, w: 7.2, h: 5.1, fontFace: FONT, fontSize: 23, color: INK, valign: "top", paraSpaceAfter: 22, isTextBox: true, margin: 0, objectName: "anim1_a" });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.2, y: 1.6, w: 4.5, h: 4.9, rectRadius: 0.12, fill: { color: NAVY }, line: { color: GOLD, width: 2 },
      shadow: { type: "outer", color: "1A202C", blur: 8, offset: 3, angle: 90, opacity: 0.3 }, objectName: "anim2_a" });
    s.addText(sd.box[0], { x: 8.55, y: 1.85, w: 3.8, h: 0.6, fontFace: FONT, fontSize: 22, bold: true, color: GOLD, isTextBox: true, margin: 0, objectName: "anim2_b" });
    s.addText(sd.box[1], { x: 8.55, y: 2.55, w: 3.8, h: 3.7, fontFace: FONT, fontSize: 21, color: WHITE, valign: "top", isTextBox: true, margin: 0, objectName: "anim2_c" });
  },
  table(pres, s, sd) {
    const nc = sd.head.length;
    const rows = [sd.head.map(h => ({ text: h, options: { bold: true, color: GOLD, fill: { color: NAVY }, fontSize: 16 } }))]
      .concat(sd.rows.map((r, i) => r.map((c, j) => ({ text: c, options: { fill: { color: i % 2 ? WHITE : MIST }, bold: j === 0, color: j === 0 ? NAVY : INK } }))));
    const fs = sd.rows.length > 6 ? 14 : 16;
    s.addTable(rows, { x: 0.6, y: 1.55, w: 12.1, fontFace: FONT, fontSize: fs, border: { type: "solid", pt: 0.5, color: "C8D0DC" }, valign: "middle",
      rowH: Math.min(0.62, 4.9 / (sd.rows.length + 1)), margin: 0.08, objectName: "anim1_a" });
    if (sd.note) s.addText(sd.note, { x: 0.6, y: 6.45, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 14, italic: true, color: TEAL, isTextBox: true, margin: 0, objectName: "anim2_a" });
  },
  flow(pres, s, sd) {
    const n = sd.steps.length, gap = 0.35, w = (12.1 - gap * (n - 1)) / n, y = 2.2, h = 3.6;
    sd.steps.forEach(([hd, tx], i) => {
      const x = 0.6 + i * (w + gap), col = ACC[i % ACC.length];
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: i % 2 ? MIST : GOLDL }, line: { color: col, width: 1.5 }, objectName: `anim${i + 1}_a` });
      s.addShape(pres.shapes.OVAL, { x: x + w / 2 - 0.4, y: y - 0.4, w: 0.8, h: 0.8, fill: { color: col }, line: { color: WHITE, width: 2 }, objectName: `anim${i + 1}_b` });
      s.addText(String(i + 1), { x: x + w / 2 - 0.4, y: y - 0.4, w: 0.8, h: 0.8, fontFace: FONT, fontSize: 20, bold: true, color: WHITE, align: "center", valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_c` });
      s.addText(hd, { x: x + 0.12, y: y + 0.55, w: w - 0.24, h: 0.9, fontFace: FONT, fontSize: n > 5 ? 17 : 20, bold: true, color: NAVY, align: "center", valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_d` });
      s.addText(tx, { x: x + 0.15, y: y + 1.5, w: w - 0.3, h: h - 1.7, fontFace: FONT, fontSize: n > 5 ? 16 : 18, color: INK, align: "center", valign: "top", isTextBox: true, margin: 0, objectName: `anim${i + 1}_e` });
      if (i < n - 1) s.addShape(pres.shapes.CHEVRON, { x: x + w + 0.06, y: y + h / 2 - 0.2, w: 0.24, h: 0.4, fill: { color: GOLD }, line: { color: GOLD }, objectName: `anim${i + 1}_f` });
    });
  },
  stats(pres, s, sd) {
    const n = sd.items.length, gap = 0.4, w = (12.1 - gap * (n - 1)) / n;
    sd.items.forEach(([v, l, d], i) => {
      const x = 0.6 + i * (w + gap), col = [NAVY, TEAL, CRIM][i % 3];
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.9, w, h: 4.2, rectRadius: 0.12, fill: { color: MIST }, line: { color: "D5DCE8" }, objectName: `anim${i + 1}_a` });
      s.addText(v, { x, y: 2.2, w, h: 1.6, fontFace: FONT, fontSize: 66, bold: true, color: col, align: "center", valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_b` });
      s.addText(l, { x, y: 3.9, w, h: 0.6, fontFace: FONT, fontSize: 22, bold: true, color: NAVY, align: "center", isTextBox: true, margin: 0, objectName: `anim${i + 1}_c` });
      s.addText(d, { x: x + 0.3, y: 4.55, w: w - 0.6, h: 1.2, fontFace: FONT, fontSize: 16, color: SLATE, align: "center", valign: "top", isTextBox: true, margin: 0, objectName: `anim${i + 1}_d` });
    });
  },
  chart(pres, s, sd) {
    const data = sd.series.map(([name, values]) => ({ name, labels: sd.labels, values }));
    const opts = { x: 0.6, y: 1.5, w: 8.6, h: 5.2, chartColors: [NAVY2, GOLD, CRIM, TEAL],
      catAxisLabelColor: SLATE, valAxisLabelColor: SLATE, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 12, valAxisLabelFontSize: 12,
      valGridLine: { color: "E2E8F0", size: 0.5 }, catGridLine: { style: "none" },
      showCatAxisTitle: true, catAxisTitle: sd.xTitle, showValAxisTitle: true, valAxisTitle: sd.yTitle,
      catAxisTitleColor: NAVY, valAxisTitleColor: NAVY, catAxisTitleFontFace: "+mn-lt", valAxisTitleFontFace: "+mn-lt", catAxisTitleFontSize: 13, valAxisTitleFontSize: 13,
      showLegend: sd.series.length > 1, legendPos: "t", legendFontFace: "+mn-lt", legendFontSize: 13, legendColor: INK, objectName: "anim1_a" };
    if (sd.ctype === "line") { opts.lineSize = 3; opts.lineDataSymbol = "circle"; opts.lineDataSymbolSize = 7; opts.valAxisMinVal = 0; opts.valAxisMaxVal = 1; }
    else { opts.showValue = true; opts.dataLabelPosition = "outEnd"; opts.dataLabelFontFace = "+mn-lt"; opts.dataLabelFontSize = 13; opts.dataLabelColor = NAVY; opts.dataLabelFormatCode = "0.000"; opts.chartColors = [NAVY2, TEAL, GOLD, CRIM]; opts.barGapWidthPct = 60; }
    s.addChart(sd.ctype === "line" ? pres.charts.LINE : pres.charts.BAR, data, opts);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 9.5, y: 1.8, w: 3.2, h: 4.4, rectRadius: 0.12, fill: { color: NAVY }, line: { color: GOLD, width: 2 }, objectName: "anim2_a" });
    s.addText("Takeaway", { x: 9.8, y: 2.05, w: 2.6, h: 0.5, fontFace: FONT, fontSize: 20, bold: true, color: GOLD, isTextBox: true, margin: 0, objectName: "anim2_b" });
    s.addText(sd.caption, { x: 9.8, y: 2.7, w: 2.6, h: 3.3, fontFace: FONT, fontSize: 19, color: WHITE, valign: "top", isTextBox: true, margin: 0, objectName: "anim2_c" });
  },
  quiz(pres, s, sd) {
    sd.items.forEach((q, i) => {
      const y = 1.65 + i * 1.65;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y, w: 12.1, h: 1.35, rectRadius: 0.1, fill: { color: i % 2 ? MIST : TEALL }, line: { color: i % 2 ? MIST : TEALL }, objectName: `anim${i + 1}_a` });
      s.addText(`Q${i + 1}`, { x: 0.85, y: y + 0.27, w: 0.8, h: 0.8, fontFace: FONT, fontSize: 20, bold: true, color: WHITE, align: "center", valign: "middle", shape: pres.shapes.OVAL, fill: { color: TEAL }, isTextBox: true, margin: 0, objectName: `anim${i + 1}_b` });
      s.addText(q, { x: 1.95, y, w: 10.5, h: 1.35, fontFace: FONT, fontSize: 19, color: INK, valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_c` });
    });
  },
  summary(pres, s, sd) {
    sd.items.forEach((t, i) => {
      const x = 0.8 + (i % 2) * 6.0, y = 1.9 + Math.floor(i / 2) * 2.3;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 5.6, h: 1.9, rectRadius: 0.12, fill: { color: NAVY2 }, line: { color: GOLD, width: 1.25 }, objectName: `anim${i + 1}_a` });
      s.addText(String(i + 1), { x: x + 0.3, y: y + 0.55, w: 0.8, h: 0.8, fontFace: FONT, fontSize: 24, bold: true, color: NAVY, align: "center", valign: "middle", shape: pres.shapes.OVAL, fill: { color: GOLD }, isTextBox: true, margin: 0, objectName: `anim${i + 1}_b` });
      s.addText(t, { x: x + 1.35, y, w: 4.0, h: 1.9, fontFace: FONT, fontSize: 19, color: WHITE, valign: "middle", isTextBox: true, margin: 0, objectName: `anim${i + 1}_c` });
    });
  }
};

(async () => { for (let i = 0; i < units.length; i++) await buildUnit(units[i], i); })();
