export const meta = {
  name: 'klipt-produce',
  description: 'Produce Klipt example pieces under different model/skill/pipeline configurations',
  phases: [{ title: 'Produce' }],
}
// Config matrix: A sonnet bare · B sonnet+klipt-craft · C opus bare · D opus+klipt-craft
// E opus director → sonnet maker+klipt-craft · F sonnet maker+klipt-craft → opus critic → sonnet reviser+klipt-craft
// G opus + taste-express · H sonnet + taste-express
// args: { items: [{ id, config, kind?, lang?, <brief fields>?, start?: 'maker'|'critic'|'reviser', partial?: bool }] }
//   brief fields inline, or read by the agent from bench/briefs/<id>.json when absent.
//   start: resume a multi-stage pipeline at that stage (earlier stages' files are already in the piece folder).
const SONNET = 'claude-sonnet-5-5', OPUS = 'claude-opus-5-5'
const RESULT = { type: 'object', properties: {
  id: { type: 'string' }, status: { type: 'string', enum: ['done', 'failed'] },
  deliverables: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } },
  required: ['id', 'status', 'notes'] }

function briefBlock(it) {
  if (!it.brief) return `The full client brief is in bench/briefs/${it.id}.json (brand, sector, kind, format, duration or slides, brief, optional angle = content angle / format to use). Read it first.\nCopy language: ${it.lang === 'en' ? 'English (natural, native-level marketing copy)' : 'French'}.`
  const lines = [`Brand: ${it.brand}`, `Sector: ${it.sector}`, `Deliverable: ${it.kind}, format ${it.format}` +
    (it.duration ? `, duration ${it.duration}` : '') + (it.slides ? `, ${it.slides} slides` : ''),
    `Brief: ${it.brief}`]
  if (it.angle) lines.push(`Content angle / format to use: ${it.angle}`)
  lines.push(`Copy language: ${it.lang === 'en' ? 'English (natural, native-level marketing copy)' : 'French'}.`)
  return lines.join('\n')
}
const head = (role, it) => `ROLE: ${role} | PIECE_ID: ${it.id}\nWorking directory: /home/user/video-klipt. Your piece folder: pieces/${it.id}/ (create it if missing). Do not open any other folder under pieces/.\n\n`
const PARTIAL = `\n\nNote: a previous attempt at this step was interrupted by a machine restart. Files already in your piece folder may be partial or stale: reuse what is good, fix or redo the rest, and make sure every final deliverable is complete and freshly rendered.`

const TE = `
2. Use the taste-express skill. SKILL_DIR = /home/user/video-klipt/skills/taste-express. Read SKILL_DIR/SKILL.md and follow its process (creative cell: run SKILL_DIR/scripts/draw.py, write design-card.md in YOUR piece folder; the kit; three-voice critique; SKILL_DIR/scripts/remember.py at the end).
   Adaptations to this environment: there is NO internet, so instead of Google Fonts / the Phosphor CDN use the local fonts and Lucide icons listed in the render contract. SKILL_DIR/scripts/render.py works for quick still previews, but the final deliverables must follow docs/RENDER_CONTRACT.md (index.html in the piece folder, rendered with tools/render.mjs). A kit carousel strip (\`<main class="carousel">\` with \`<section class="slide">\` children) is compatible with the stills renderer. For a video, apply the creative cell and the craft floors, then build the animation as the contract describes. The brief's facts are the user's facts.`

function makerPrompt(it, { skill, direction, te }) {
  return head('maker', it) +
`You are a senior designer / motion designer producing ONE piece for Klipt's public example library (Klipt makes social content for all kinds of businesses). It must be good enough that the brand would post it as is.

1. Read docs/RENDER_CONTRACT.md (mandatory technical rules and commands).` + (te ? TE : '') +
(skill ? `\n2. Read skills/klipt-craft/SKILL.md and follow its craft process.` : '') +
(direction ? `\n3. An art director prepared pieces/${it.id}/direction.md — read it and implement it faithfully (you may refine details that don't work once rendered).` : '') + `

BRIEF
${briefBlock(it)}

Build it, render the FINAL output (video or stills), check the result visually (open the sheet/frames) and fix problems, then write meta.json as specified in the contract. Clean up previews/scratch frames.
Return: id, status, deliverables (file paths), notes (one or two sentences on the concept and any issue).` + (it.partial ? PARTIAL : '')
}

function directorPrompt(it) {
  return head('director', it) +
`You are an award-winning art director at Klipt. You do NOT write code: you write the creative direction that a designer/developer will implement as an HTML/JS composition rendered to video or images.

Read docs/RENDER_CONTRACT.md (to know what the medium can and cannot do: no photos, everything is built with type, shapes, SVG, canvas, three.js, UI mock-ups…) and skills/klipt-craft/SKILL.md.

BRIEF
${briefBlock(it)}

Write pieces/${it.id}/direction.md containing: audience insight and the one message; concept (the idea, why it fits this brand); art direction (palette with hex, fonts from the available list with sizes, graphic language, textures, logo idea); the COMPLETE final copy (exact strings, proofread, correct typography for the copy language); a precise storyboard with timecodes and transitions (video) or slide-by-slide layouts (carousel/post); motion notes; technical approach hints. Be specific enough that two different developers would produce nearly the same piece.
Return: id, status, deliverables, notes.`
}

function criticPrompt(it) {
  return head('critic', it) +
`You are an exacting creative director at Klipt reviewing a piece before it goes into the public example library. You do NOT edit the piece.

Read skills/klipt-craft/SKILL.md (the quality bar). Brief of the piece:
${briefBlock(it)}

Inspect pieces/${it.id}/: sheet.jpg, poster.jpg or slides/*.png, and index.html. For videos, render 3–5 extra frames at key moments with \`node tools/render.mjs frame pieces/${it.id} <t> /tmp/${it.id}-<t>.png\` and look at them.
Write pieces/${it.id}/critique.md: a verdict (1–10) and the 5–8 highest-impact fixes, prioritized, each concrete and actionable (exact values, strings, timings, positions). Include any typo, clipping, overflow, legibility or timing problem.
Return: id, status, deliverables, notes (verdict + top issue).`
}

function reviserPrompt(it) {
  return head('reviser', it) +
`You are a senior designer / motion designer at Klipt. A piece in pieces/${it.id}/ was reviewed by the creative director.

1. Read docs/RENDER_CONTRACT.md and skills/klipt-craft/SKILL.md.
2. Read pieces/${it.id}/critique.md and pieces/${it.id}/index.html.
3. Apply the fixes (use judgment: all high-priority ones), re-render the FINAL output, check it visually, update meta.json. Clean up previews/scratch frames.

Original brief:
${briefBlock(it)}
Return: id, status, deliverables, notes.` + (it.partial ? PARTIAL : '')
}

async function runItem(it) {
  const o = { phase: 'Produce', schema: RESULT }
  const L = s => `${it.id}·${it.config}·${s}`
  const from = it.start || 'first'
  switch (it.config) {
    case 'A': return [await agent(makerPrompt(it, {}), { ...o, model: SONNET, label: L('maker') })]
    case 'B': return [await agent(makerPrompt(it, { skill: true }), { ...o, model: SONNET, label: L('maker') })]
    case 'C': return [await agent(makerPrompt(it, {}), { ...o, model: OPUS, label: L('maker') })]
    case 'D': return [await agent(makerPrompt(it, { skill: true }), { ...o, model: OPUS, label: L('maker') })]
    case 'G': return [await agent(makerPrompt(it, { te: true }), { ...o, model: OPUS, label: L('maker') })]
    case 'H': return [await agent(makerPrompt(it, { te: true }), { ...o, model: SONNET, label: L('maker') })]
    case 'E': {
      const d = from === 'first' ? await agent(directorPrompt(it), { ...o, model: OPUS, label: L('director') }) : null
      const m = await agent(makerPrompt(it, { skill: true, direction: true }), { ...o, model: SONNET, label: L('maker') })
      return [d, m]
    }
    case 'F': {
      const m = ['first', 'maker'].includes(from) ? await agent(makerPrompt(it, { skill: true }), { ...o, model: SONNET, label: L('maker') }) : null
      const c = from !== 'reviser' ? await agent(criticPrompt(it), { ...o, model: OPUS, label: L('critic') }) : null
      const r = await agent(reviserPrompt(it), { ...o, model: SONNET, label: L('reviser') })
      return [m, c, r]
    }
  }
}

phase('Produce')
const ITEMS = args.items.map(x => ({ ...(args.brief || {}), ...x }))
const results = await parallel(ITEMS.map(it => () => runItem(it).catch(e => [{ id: it.id, status: 'failed', notes: String(e) }])))
return results.map((r, i) => ({ id: ITEMS[i].id, config: ITEMS[i].config, stages: r }))
