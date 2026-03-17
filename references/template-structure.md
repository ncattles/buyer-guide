# Template Structure Reference — v4

This file contains the complete, working docx-js reference script for the Buyer's Guide PDF. Every value here is canonical. Use this as a direct copy-paste foundation — do not reinterpret or simplify.

**The layout specs in SKILL.md and this file are in sync. If they ever conflict, SKILL.md wins.**

---

## Full Working Reference Script

```javascript
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber, PageBreak, ExternalHyperlink, LevelFormat,
  UnderlineType
} = require('docx');
const fs = require('fs');

// ── Page Layout ──────────────────────────────────────────────────────────────
const PAGE_W    = 12240;  // US Letter 8.5in
const PAGE_H    = 15840;  // US Letter 11in
const MARGIN    = 1080;   // 0.75in — NOT 1in
const CONTENT_W = 10080;  // PAGE_W - (MARGIN * 2) — all tables must sum to this

// ── Color Palette ─────────────────────────────────────────────────────────────
const C = {
  NAVY:        '1B2A4A',  // Section headings, title bar, header row fill
  BLUE:        '2E75B6',  // Accent borders, links, section heading underline
  BLUE_LIGHT:  'D6E8F7',
  GREEN:       '2E8B57',  // Checkmarks, strengths, rating >= 8.0, verdict #1
  GREEN_LIGHT: 'E2F4EB',
  GOLD:        'DAA520',  // Rating 7.0-7.9, verdict #3
  GOLD_LIGHT:  'FFF8DC',
  RED:         'CC3333',  // Weaknesses, rating < 7.0, avoid cards
  ALT_ROW:     'F0F4FA',  // Even table rows
  WHITE:       'FFFFFF',  // Odd table rows
  LIGHT_BG:    'EAF2FB',  // Checklist, links table, rec cards background
  GRAY_TEXT:   '555555',  // Checklist description text
  WARN_BG:     'FFF3CD',  // Avoid card background
  WARN_BORDER: 'E6A817',  // Avoid card border
  PURPLE:      '5E4B8B',  // Verdict #4 (budget pick)
};

// Rating color: >= 8.0 → GREEN, >= 7.0 → GOLD, < 7.0 → RED
const ratingColor = r => parseFloat(r) >= 8.0 ? C.GREEN : parseFloat(r) >= 7.0 ? C.GOLD : C.RED;

// ── Border Presets ────────────────────────────────────────────────────────────
const noBorder    = { style: BorderStyle.NONE,   size: 0, color: 'FFFFFF' };
const noBorders   = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
const thinBorder  = { style: BorderStyle.SINGLE, size: 4, color: 'CCCCCC' };
const thinBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const navyBorder  = { style: BorderStyle.SINGLE, size: 6, color: C.NAVY };
const navyBorders = { top: navyBorder, bottom: navyBorder, left: navyBorder, right: navyBorder };

// ── Helper Functions ──────────────────────────────────────────────────────────
const run  = (text, opts = {}) => new TextRun({ text, font: 'Arial', ...opts });
const bold = (text, opts = {}) => run(text, { bold: true, ...opts });
const para = (children, opts = {}) => new Paragraph({
  children: Array.isArray(children) ? children : [children], ...opts
});
const spacer = (before = 80, after = 80) => para([run('')], { spacing: { before, after } });
const link = (text, url) => new ExternalHyperlink({
  link: url,
  children: [new TextRun({ text, font: 'Arial', size: 18, color: C.BLUE,
    underline: { type: UnderlineType.SINGLE } })],
});

// ── Section Heading ───────────────────────────────────────────────────────────
function sectionHead(text) {
  return para([bold(text, { color: C.NAVY, size: 26 })], {
    spacing: { before: 240, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: C.BLUE, space: 4 } },
  });
}

// ── Banner ────────────────────────────────────────────────────────────────────
// meta format: 'Budget: [formatted]  |  Month YYYY  |  [User's confirmed location]'
// Budget formatting: 'Under $500' / '~$500' / '$400–600' / '$500 (flexible)'
// Location must come from what the user confirmed in Step 1 — NEVER hardcode a city.
function makeBanner(title, subtitle, meta) {
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [new TableRow({ children: [
      new TableCell({
        borders: noBorders,
        shading: { fill: C.NAVY, type: ShadingType.CLEAR },
        margins: { top: 260, bottom: 260, left: 360, right: 360 },
        width: { size: CONTENT_W, type: WidthType.DXA },
        children: [
          para([bold(title, { color: C.WHITE, size: 52, allCaps: true })],
            { alignment: AlignmentType.CENTER }),
          para([run(subtitle, { color: 'BBCCDD', size: 22 })],
            { alignment: AlignmentType.CENTER, spacing: { before: 80, after: 40 } }),
          para([run(meta, { color: 'AABBCC', size: 18 })],
            { alignment: AlignmentType.CENTER }),
        ],
      }),
    ]})],
  });
}

// ── Requirements Checklist ────────────────────────────────────────────────────
// reqs = [{ title, desc }, ...]
// Always include:
//   { title: 'Region', desc: 'All products verified available in [location] and priced in [currency].' }
// Include any confirmed existing hardware the recommended products must interact with.
function makeRequirements(reqs) {
  const rows = reqs.map(({ title, desc }) =>
    new TableRow({ children: [
      new TableCell({
        borders: noBorders,
        shading: { fill: C.LIGHT_BG, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 160, right: 80 },
        width: { size: 500, type: WidthType.DXA },
        verticalAlign: VerticalAlign.CENTER,
        children: [para([bold('✓', { color: C.GREEN, size: 24 })],
          { alignment: AlignmentType.CENTER })],
      }),
      new TableCell({
        borders: noBorders,
        shading: { fill: C.LIGHT_BG, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 160 },
        width: { size: CONTENT_W - 500, type: WidthType.DXA },
        children: [
          para([bold(title, { color: C.NAVY, size: 20 })],
            { spacing: { before: 0, after: 40 } }),
          para([run(desc, { size: 18, color: C.GRAY_TEXT })]),
        ],
      }),
    ]})
  );
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [500, CONTENT_W - 500],
    borders: { insideH: { style: BorderStyle.SINGLE, size: 4, color: 'C5D9EF' } },
    rows,
  });
}

// ── Glossary Table ────────────────────────────────────────────────────────────
// terms = [{ term, def }, ...]
function makeGlossary(terms) {
  const rows = terms.map(({ term, def }, i) =>
    new TableRow({ children: [
      new TableCell({
        borders: thinBorders,
        shading: { fill: i % 2 === 0 ? C.ALT_ROW : C.WHITE, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        width: { size: 2200, type: WidthType.DXA },
        children: [para([bold(term, { color: C.NAVY, size: 18 })])],
      }),
      new TableCell({
        borders: thinBorders,
        shading: { fill: i % 2 === 0 ? C.ALT_ROW : C.WHITE, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        width: { size: CONTENT_W - 2200, type: WidthType.DXA },
        children: [para([run(def, { size: 18 })])],
      }),
    ]})
  );
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [2200, CONTENT_W - 2200],
    rows,
  });
}

// ── Rankings Table ────────────────────────────────────────────────────────────
// headers = string[]
// colWidths = number[] — must sum to CONTENT_W (10080)
// rows = string[][] — last column assumed to be rating
// Over-budget stretch picks: append ' ⚠' to product name in column 1
// Tiebreaker order when ratings are equal: price → availability → community sentiment
function makeRankingsTable(headers, colWidths, rows) {
  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map((h, i) => new TableCell({
      borders: navyBorders,
      shading: { fill: C.NAVY, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      width: { size: colWidths[i], type: WidthType.DXA },
      verticalAlign: VerticalAlign.CENTER,
      children: [para([bold(h, { color: C.WHITE, size: 18 })],
        { alignment: AlignmentType.CENTER })],
    })),
  });

  const dataRows = rows.map((row, ri) => {
    const rc = ratingColor(row[row.length - 1]);
    return new TableRow({
      children: row.map((val, ci) => new TableCell({
        borders: thinBorders,
        shading: { fill: ri % 2 === 0 ? C.WHITE : C.ALT_ROW, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        width: { size: colWidths[ci], type: WidthType.DXA },
        verticalAlign: VerticalAlign.CENTER,
        children: [para([
          ci === row.length - 1
            ? bold(val, { color: rc, size: 19 })
            : ci === 0 || ci === 2
              ? bold(val, { size: 19 })
              : run(val, { size: 18 }),
        ], { alignment: ci === 0 || ci === 2 || ci === row.length - 1
          ? AlignmentType.CENTER : AlignmentType.LEFT })],
      })),
    });
  });

  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [headerRow, ...dataRows],
  });
}

// ── Product Card ──────────────────────────────────────────────────────────────
// verdictColor: C.GREEN (#1), C.BLUE (#2), C.GOLD (#3), C.PURPLE (#4)
// Over-budget: verdict = 'BEST OVERALL (OVER BUDGET)', verdictColor = rank color
// specs = [['Label', 'Value'], ...]
//
// MANDATORY spec rows:
//   ['Price History', 'Typically $X–Y; currently at [historic high / average / near low]']
//   Populate from CamelCamelCamel data. Never omit this row.
//
// Conditional specs — document condition inline:
//   ['Wireless Output', '15W Qi2 (pass-through only) / 7.5W standalone']
//
// Regional spec variants — note inline if user's regional model differs:
//   ['Panel Type', 'IPS (EU model: VA — check local listing)']
//
// weaknesses string must include (as applicable):
//   - Community complaints confirmed by 3+ distinct sources
//   - Conditional specs that materially change real-world performance
//   - "Exceeds stated budget of $X by Y%" if over budget
//   - "Consider waiting — [reason]" if at historic price high or successor imminent/announced
//   - Regional spec differences that are materially worse than the global model
function makeProductCard({
  rank, name, verdict, verdictColor, price, rating,
  specs, strengths, weaknesses,
  productUrl, productLabel, priceUrl, priceLabel
}) {
  const rc = ratingColor(rating);

  const titleBar = new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [700, CONTENT_W - 700 - 1800, 1800],
    rows: [new TableRow({ children: [
      new TableCell({
        borders: noBorders, shading: { fill: C.NAVY, type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 120, right: 80 },
        width: { size: 700, type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
        children: [para([bold(`#${rank}`, { color: C.WHITE, size: 40 })],
          { alignment: AlignmentType.CENTER })],
      }),
      new TableCell({
        borders: noBorders, shading: { fill: C.NAVY, type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 160, right: 80 },
        width: { size: CONTENT_W - 700 - 1800, type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
        children: [para([bold(name, { color: C.WHITE, size: 26 })])],
      }),
      new TableCell({
        borders: noBorders, shading: { fill: verdictColor, type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 120, right: 160 },
        width: { size: 1800, type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
        children: [para([bold(verdict, { color: C.WHITE, size: 18 })],
          { alignment: AlignmentType.CENTER })],
      }),
    ]})],
  });

  const priceBar = new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W / 2, CONTENT_W / 2],
    rows: [new TableRow({ children: [
      new TableCell({
        borders: noBorders, shading: { fill: C.ALT_ROW, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 180, right: 80 },
        width: { size: CONTENT_W / 2, type: WidthType.DXA },
        children: [para([bold('Price: ', { size: 20 }), bold(price, { size: 26, color: C.NAVY })])],
      }),
      new TableCell({
        borders: noBorders, shading: { fill: C.ALT_ROW, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 180, right: 80 },
        width: { size: CONTENT_W / 2, type: WidthType.DXA },
        children: [para([bold('Rating: ', { size: 20 }), bold(`${rating} / 10`, { size: 24, color: rc })])],
      }),
    ]})],
  });

  const specRows = specs.map(([label, value], i) =>
    new TableRow({ children: [
      new TableCell({
        borders: thinBorders,
        shading: { fill: i % 2 === 0 ? C.ALT_ROW : C.WHITE, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        width: { size: 2100, type: WidthType.DXA },
        children: [para([bold(label, { size: 18, color: C.NAVY })])],
      }),
      new TableCell({
        borders: thinBorders,
        shading: { fill: i % 2 === 0 ? C.ALT_ROW : C.WHITE, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        width: { size: CONTENT_W - 2100, type: WidthType.DXA },
        children: [para([run(value, { size: 18 })])],
      }),
    ]})
  );
  const specTable = new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [2100, CONTENT_W - 2100],
    rows: specRows,
  });

  const linkTable = new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W / 2, CONTENT_W / 2],
    rows: [new TableRow({ children: [
      new TableCell({
        borders: noBorders, shading: { fill: C.LIGHT_BG, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 160, right: 80 },
        width: { size: CONTENT_W / 2, type: WidthType.DXA },
        children: [
          para([bold('Product Link', { size: 18, color: C.NAVY })], { spacing: { before: 0, after: 40 } }),
          para([link(productLabel, productUrl)]),
        ],
      }),
      new TableCell({
        borders: noBorders, shading: { fill: C.LIGHT_BG, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 160, right: 80 },
        width: { size: CONTENT_W / 2, type: WidthType.DXA },
        children: [
          para([bold('Price Verified At', { size: 18, color: C.NAVY })], { spacing: { before: 0, after: 40 } }),
          para([link(priceLabel, priceUrl)]),
        ],
      }),
    ]})],
  });

  return [
    spacer(80, 0),
    titleBar,
    priceBar,
    spacer(60, 0),
    specTable,
    spacer(80, 0),
    para([bold('Strengths', { color: C.GREEN, size: 20 })], { spacing: { before: 0, after: 60 } }),
    para([run(strengths, { size: 19 })], { spacing: { before: 0, after: 100 } }),
    para([bold('Weaknesses', { color: C.RED, size: 20 })], { spacing: { before: 0, after: 60 } }),
    para([run(weaknesses, { size: 19 })], { spacing: { before: 0, after: 100 } }),
    linkTable,
    spacer(80, 0),
  ];
}

// ── What To Avoid Cards ───────────────────────────────────────────────────────
// avoids = [{ title, desc }, ...]
function makeAvoidCards(avoids) {
  const rows = avoids.map(({ title, desc }) =>
    new TableRow({ children: [
      new TableCell({
        borders: {
          top:    { style: BorderStyle.SINGLE, size: 6,  color: C.WARN_BORDER },
          bottom: { style: BorderStyle.SINGLE, size: 6,  color: C.WARN_BORDER },
          left:   { style: BorderStyle.SINGLE, size: 18, color: C.RED },
          right:  noBorder,
        },
        shading: { fill: C.WARN_BG, type: ShadingType.CLEAR },
        margins: { top: 100, bottom: 100, left: 160, right: 160 },
        width: { size: CONTENT_W, type: WidthType.DXA },
        children: [
          para([bold('AVOID: ' + title, { color: C.RED, size: 19 })], { spacing: { before: 0, after: 60 } }),
          para([run(desc, { size: 18 })]),
        ],
      }),
    ]})
  );
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    borders: { insideH: { style: BorderStyle.SINGLE, size: 4, color: C.WARN_BORDER } },
    rows,
  });
}

// ── Recommendations Cards ─────────────────────────────────────────────────────
// recs = [{ title, body, accentColor }, ...]
// accentColor matches verdictColor of the recommended product
//
// Dominant winner: first card should read "If you only read one recommendation: [product]. [Reason.]"
// Consider waiting: include in body — "If timing allows, consider waiting — [reason]."
// Announced successor: include a separate card — "Consider waiting for [product] — [timeframe]. [What it improves.]"
function makeRecCards(recs) {
  const rows = recs.map(({ title, body, accentColor }) =>
    new TableRow({ children: [
      new TableCell({
        borders: {
          top:    noBorder,
          bottom: { style: BorderStyle.SINGLE, size: 4, color: 'CCCCCC' },
          left:   { style: BorderStyle.SINGLE, size: 18, color: accentColor },
          right:  noBorder,
        },
        shading: { fill: C.LIGHT_BG, type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 200, right: 160 },
        width: { size: CONTENT_W, type: WidthType.DXA },
        children: [
          para([bold(title, { color: accentColor, size: 20 })], { spacing: { before: 0, after: 80 } }),
          para([run(body, { size: 19 })]),
        ],
      }),
    ]})
  );
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    borders: { insideH: noBorder },
    rows,
  });
}

// ── Header & Footer ───────────────────────────────────────────────────────────
function makeHeader(guideTitle, dateStr) {
  return new Header({ children: [
    para([
      bold(guideTitle, { color: C.NAVY, size: 16 }),
      run('\t', { size: 16 }),
      run(dateStr, { color: '888888', size: 16 }),
    ], {
      tabStops: [{ type: 'right', position: 9360 }],
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'CCCCCC', space: 4 } },
    }),
  ]});
}

function makeFooter(dateStr) {
  return new Footer({ children: [
    para([
      run(`Prices verified ${dateStr}. Verify before purchase.`, { color: '888888', size: 16, italics: true }),
      run('\t', { size: 16 }),
      run('Page ', { color: '888888', size: 16 }),
      new TextRun({ children: [PageNumber.CURRENT], font: 'Arial', size: 16, color: '888888' }),
    ], {
      tabStops: [{ type: 'right', position: 9360 }],
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'CCCCCC', space: 4 } },
    }),
  ]});
}

// ── Document Constructor ──────────────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [{
      reference: 'bullets',
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 480, hanging: 240 } } },
      }],
    }],
  },
  styles: { default: { document: { run: { font: 'Arial', size: 20 } } } },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_W, height: PAGE_H },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
      },
    },
    headers: { default: makeHeader('Guide Title Here', 'Month YYYY') },
    footers: { default: makeFooter('Month YYYY') },
    children: [
      // 1. Banner
      // Budget formatting: 'Under $500' / '~$500' / '$400–600' / '$500 (flexible)'
      // Location: user's confirmed answer from Step 1 — NEVER hardcode a city
      makeBanner('PRODUCT CATEGORY', 'Subtitle — use case and category detail', 'Budget: Under $XXX  |  Month YYYY  |  User Location'),

      // 2. Intro — if category has a dominant winner (≥1.0 rating gap), name it here
      spacer(160, 0),
      para([run('2–4 sentence intro. If one product leads by ≥1.0 rating points, name it and note the gap here.', { size: 20 })],
        { spacing: { before: 160, after: 120 } }),

      // 3. Requirements — always include Region and any confirmed existing hardware
      sectionHead('Your Requirements — Applied to This Guide'),
      makeRequirements([
        { title: 'Requirement 1', desc: 'How it was applied...' },
        { title: 'Region', desc: 'All products verified available in [location] and priced in [currency].' },
        // Existing hardware example:
        // { title: 'Compatible with', desc: 'OtterBox Defender Series Pro (iPhone 17 Pro Max) — MagSafe magnets confirmed built-in.' },
      ]),
      spacer(80, 0),

      // 4. Glossary
      sectionHead('Key Terms & Glossary'),
      makeGlossary([{ term: 'Term', def: 'Definition...' }]),
      spacer(80, 0),

      // 5. What To Look For
      sectionHead('What To Look For'),
      para([bold('Criterion — ', { color: C.NAVY, size: 19 }), run('Explanation...', { size: 19 })],
        { spacing: { before: 80, after: 60 }, bullet: { level: 0 } }),
      spacer(40, 0),

      para([new PageBreak()]),

      // 6. Rankings Table — append ' ⚠' to name for over-budget stretch picks
      sectionHead('Rankings at a Glance'),
      makeRankingsTable(
        ['#', 'Product', 'Price', 'Spec 1', 'Spec 2', 'Spec 3', 'Rating'],
        [360, 2760, 900, 1320, 1320, 1480, 1940],
        [
          ['1', 'Product A', '$XXX', 'value', 'value', 'value', '8.7 / 10'],
          // Over-budget example: ['2', 'Product B ⚠', '$XXX', 'value', 'value', 'value', '9.1 / 10'],
        ]
      ),
      spacer(60, 0),
      para([run('Prices verified [Month Year]. Verify before purchase.', { size: 16, color: '888888', italics: true })]),

      para([new PageBreak()]),

      // 7. Detailed Reviews
      sectionHead('Detailed Reviews'),
      ...makeProductCard({
        rank: 1, name: 'Product A', verdict: 'BEST OVERALL',
        verdictColor: C.GREEN, price: '$XXX', rating: '8.7',
        specs: [
          // MANDATORY — always include Price History row populated from CamelCamelCamel:
          ['Price History', 'Typically $X–Y; currently at [historic high / average / near low]'],
          ['Spec Label', 'Spec Value'],
          // Conditional spec example:
          // ['Wireless Output', '15W Qi2 (pass-through only) / 7.5W standalone'],
          // Regional variant example:
          // ['Panel Type', 'IPS (EU model: VA — verify local listing)'],
        ],
        strengths: 'Strengths paragraph...',
        weaknesses: 'Weaknesses paragraph...',
        // Over-budget example: 'Exceeds stated budget of $XXX by Y%. [other weaknesses...]'
        // Consider waiting example: '[weaknesses...] Consider waiting — currently at historic price high; typically $XX less during sales.'
        // Announced successor example: '[weaknesses...] Consider waiting — [SuccessorName] announced for [timeframe].'
        productUrl: 'https://manufacturer.com/product',
        productLabel: 'manufacturer.com — Product Page',
        priceUrl: 'https://amazon.com/dp/XXXXX',
        priceLabel: 'Amazon — $XXX (verified Month Year)',
      }),

      para([new PageBreak()]),

      // 8. What To Avoid
      sectionHead('What To Avoid'),
      para([run('Intro sentence...', { size: 19 })], { spacing: { before: 0, after: 120 } }),
      makeAvoidCards([{ title: 'Warning title', desc: 'Warning description...' }]),
      spacer(80, 0),

      para([new PageBreak()]),

      // 9. Final Recommendations
      // Dominant winner: first card = "If you only read one recommendation: [product]. [Reason.]"
      // Consider waiting: include in body of relevant product's card
      // Announced successor: add a separate card for it
      sectionHead('Final Recommendations'),
      makeRecCards([
        { title: 'Scenario title', body: 'Recommendation body... If timing allows, consider waiting — [reason].', accentColor: C.GREEN },
        // Announced successor card example:
        // { title: 'Consider Waiting — [SuccessorName]', body: 'Announced for [timeframe]. Improves [X, Y]. If you can wait, this may be the better buy.', accentColor: C.BLUE },
      ]),
      spacer(120, 0),

      // 10. Pro Tips
      sectionHead('Pro Tips for Your [Category] Setup'),
      para([run('Tip text...', { size: 19 })], { spacing: { before: 60, after: 60 }, bullet: { level: 0 } }),

      // 11. Disclaimer
      para([run('Prices and availability verified [DATE]. Prices change frequently — always verify the current price at the linked retailer before purchasing. Product links are direct retailer and manufacturer URLs with no affiliate tracking.',
        { size: 16, color: '888888', italics: true })],
        { spacing: { before: 120, after: 0 }, border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'CCCCCC', space: 8 } } }),
    ],
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('/home/claude/guide.docx', buf);
  console.log('DOCX written');
}).catch(err => { console.error(err); process.exit(1); });
```

---

## Post-Generation Commands

```bash
node guide.js
python /mnt/skills/public/docx/scripts/office/validate.py guide.docx
python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf guide.docx
cp guide.pdf /mnt/user-data/outputs/
```

---

## Rankings Table Column Width Examples

Column widths **must sum to CONTENT_W (10080)**. Adapt per category:

| Category | Columns | Example Widths |
|---|---|---|
| Desks | #, Product, Price, Size, Height Range, Capacity, Presets, Rating | 360, 2400, 900, 1100, 1320, 1000, 1060, 1940 |
| Monitors | #, Product, Price, Panel, Refresh, Coating, HDR, Rating | 360, 2400, 900, 1100, 1000, 1000, 1080, 2240 |
| Laptops | #, Product, Price, CPU, RAM, Battery, Display, Rating | 360, 2400, 900, 1200, 800, 900, 1120, 2400 |
| Headphones | #, Product, Price, Type, ANC, Battery, Driver, Rating | 360, 2400, 900, 900, 800, 900, 1080, 2740 |
| Power Banks | #, Product, Price, Wireless, USB-C Out, Capacity, Weight, Rating | 360, 2600, 1000, 1500, 1200, 1100, 860, 1460 |

Always verify your widths sum to exactly 10080 before running.

---

## Verdict Badge Colors by Rank

| Rank / Role | Color Constant | Hex | Notes |
|---|---|---|---|
| #1 Best Overall | `C.GREEN` | `2E8B57` | |
| #2 Best Features / Best Value | `C.BLUE` | `2E75B6` | |
| #3 Mid-Range / Biggest Surface | `C.GOLD` | `DAA520` | |
| #4 Best Budget | `C.PURPLE` | `5E4B8B` | |
| Stretch Pick (over budget) | Same color as rank | — | Append " (OVER BUDGET)" to verdict text |

Use the same color for that product's recommendation card `accentColor`.
