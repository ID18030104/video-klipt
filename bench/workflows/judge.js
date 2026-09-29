export const meta = {
  name: 'klipt-judge',
  description: 'Blind-judge Klipt pieces (Opus and/or Sonnet judges) and rank head-to-head variants',
  phases: [{ title: 'Judge' }, { title: 'Rank' }],
}
// args: { pieces: [{id, kind, lang}], groups?: [[id,...]], judges?: ['opus'|'sonnet'] }
// Judges read the client brief from bench/briefs/<id>.json and only look at rendered outputs.
const ALL_JUDGES = [{ key: 'opus', model: 'claude-opus-5-5' }, { key: 'sonnet', model: 'claude-sonnet-5-5' }]
const JUDGES = args.judges ? ALL_JUDGES.filter(j => args.judges.includes(j.key)) : ALL_JUDGES
const S = { type: 'integer', minimum: 1, maximum: 10 }
const SCORE = { type: 'object', properties: {
  id: { type: 'string' },
  brand_fit: S, art_direction: S, typography: S, composition: S, copy_quality: S,
  storytelling: S, technical_polish: S, originality: S, overall: S,
  client_ready: { type: 'boolean' },
  defects: { type: 'array', items: { type: 'string' } },
  verdict: { type: 'string' } },
  required: ['id', 'brand_fit', 'art_direction', 'typography', 'composition', 'copy_quality', 'storytelling', 'technical_polish', 'originality', 'overall', 'client_ready', 'defects', 'verdict'] }
const RANK = { type: 'object', properties: {
  ranking: { type: 'array', items: { type: 'string' } }, rationale: { type: 'string' } }, required: ['ranking', 'rationale'] }

function briefText(it) {
  if (!it.brief) return `Read the client brief in bench/briefs/${it.id}.json (brand, sector, kind, format, duration or slides, brief, optional requested angle, lang = expected copy language).`
  return `Brand: ${it.brand} (${it.sector})\nDeliverable: ${it.kind}, ${it.format}${it.duration ? ', ' + it.duration : ''}${it.slides ? ', ' + it.slides + ' slides' : ''}\nBrief: ${it.brief}${it.angle ? '\nRequested angle: ' + it.angle : ''}\nExpected copy language: ${it.lang === 'en' ? 'English' : 'French'}`
}
function judgePrompt(it) {
  const isVideo = it.kind === 'video'
  return `ROLE: judge | PIECE_ID: ${it.id}
You are an independent, demanding jury member (senior creative director) evaluating a social-media piece made for a client of Klipt, a content agency. You know nothing about how it was made; judge ONLY the delivered output. Working directory: /home/user/video-klipt.

CLIENT BRIEF
${briefText(it)}

WHAT TO LOOK AT (apart from the brief file, only these; do not read index.html, bench/ files other than the brief, or any other file; do not open other pieces):
${isVideo
  ? `- pieces/${it.id}/sheet.jpg (12 frames evenly spaced across the video) and pieces/${it.id}/poster.jpg
- You may render up to 4 extra frames to check motion/legibility: node tools/render.mjs frame pieces/${it.id} <seconds> /tmp/j-${it.id}-<seconds>.png (then view it). Check the first second (hook) and the end card.`
  : `- every image in pieces/${it.id}/slides/ (view each one at full size), and pieces/${it.id}/sheet.jpg for the sequence.`}

Score 1–10 (10 = best-in-class agency work, 7 = solid professional, 5 = passable template, 3 = amateur): brand_fit (right register for this brand and audience), art_direction (distinctive, coherent visual concept), typography, composition (hierarchy, layout, spacing, safe zones), copy_quality (copy in the expected language — relevance, punch, spelling, grammar, typographic conventions of that language), storytelling (${isVideo ? 'hook, beats, pacing, end card' : 'narrative flow across slides / single-glance clarity'}), technical_polish (no clipping, overlap, broken rendering, illegible text), originality, overall.
client_ready: would the brand post it as is? defects: list every concrete defect you see (typos, clipped text, overlaps, empty frames…). verdict: 2 sentences. Be calibrated and severe; do not inflate.`
}
function rankPrompt(group) {
  const it = group[0]
  return `ROLE: ranker | PIECE_ID: ${group.map(g => g.id).join(',')}
You are an independent jury chair. Several agencies answered the SAME client brief. Rank their deliverables from best to worst, judging only the visual output (apart from the brief file, do not read code or other files). Working directory: /home/user/video-klipt.

CLIENT BRIEF
${briefText(it)}

Candidates (look at each one's sheet.jpg${it.kind === 'video' ? ' and poster.jpg' : ' and slides/*.png'}; do not read code or other files):
${group.map(g => `- pieces/${g.id}/`).join('\n')}

Return ranking (candidate ids, best first) and a rationale explaining the ranking (what separates the top from the bottom).`
}

const pieces = args.pieces
phase('Judge')
const scores = await parallel(pieces.flatMap(it => JUDGES.map(j => () =>
  agent(judgePrompt(it), { phase: 'Judge', model: j.model, schema: SCORE, label: `judge·${j.key}·${it.id}` })
    .then(r => r && ({ ...r, id: it.id, judge: j.key })))))
phase('Rank')
const groups = args.groups || []
const ranks = await parallel(groups.map(g => () =>
  agent(rankPrompt(g.map(id => pieces.find(p => p.id === id))), { phase: 'Rank', model: 'claude-opus-5-5', schema: RANK, label: `rank·${g[0]}` })
    .then(r => r && ({ ...r, group: g }))))
return { scores: scores.filter(Boolean), ranks: ranks.filter(Boolean) }
