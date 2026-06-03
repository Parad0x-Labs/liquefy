# Parad0x Labs — Canonical Stack Map

**Single source of truth.** Every Parad0x repo's README carries a *"How this fits the Parad0x stack"* section. The table below is **identical in every repo**. When you add, rename, or re-describe a repo, edit it **here first**, then copy the block verbatim into each README. Only the **You are here** line differs per repo.

## The rule

Each repo's section must answer three things:

1. **Why it's here** — what this repo does that nothing else in the stack does.
2. **Why it fits** — which sibling repo(s) it builds on or feeds (the *"You are here"* parenthetical).
3. **What it gives back** — the benefit it returns to the ecosystem (its table row).

Format: one `**You are here: <emoji> <Layer> (<sibling note>)**` line — unique per repo — immediately followed by the shared table.

## Canonical table (shipped repos)

| Layer | Repo | Does |
|---|---|---|
| 💸 Payments | [dna-x402](https://github.com/Parad0x-Labs/dna-x402) | x402 rail: quote → pay → verify → receipt → anchor |
| 🛠️ Build | [dna-x402-builders](https://github.com/Parad0x-Labs/dna-x402-builders) | Hosted kit: turn any API/bot into a paid agent |
| 🕶️ Privacy | [Dark-Null-Protocol](https://github.com/Parad0x-Labs/Dark-Null-Protocol) | Groth16 privacy settlement, published proofs |
| 🗜️ Data | [liquefy](https://github.com/Parad0x-Labs/liquefy) | Columnar compression that beats Zstd |
| 🛡️ Audit | [liquefy-openclaw-integration](https://github.com/Parad0x-Labs/liquefy-openclaw-integration) | Flight recorder: 24 engines + Solana-anchored audit trails |
| 🎬 Media | [nebula-media](https://github.com/Parad0x-Labs/nebula-media) | Proof-carrying media compression — scene-aware + on-chain receipts |
| 🧠 Local AI | [nulla-local](https://github.com/Parad0x-Labs/nulla-local) | Local-first agent runtime — your machine, your memory |

## "You are here" line — per repo

Paste the matching line above the table in each repo's README:

- **dna-x402** → `**You are here: 💸 Payments (the rail every other layer settles on).**`
- **dna-x402-builders** → `**You are here: 🛠️ Build (the on-ramp that turns any API into a 💸 Payments endpoint).**`
- **Dark-Null-Protocol** → `**You are here: 🕶️ Privacy (the zero-knowledge sibling of 💸 Payments).**`
- **liquefy** → `**You are here: 🗜️ Data (the compression engine the 🛡️ Audit and 🎬 Media layers are built on).**`
- **liquefy-openclaw-integration** → `**You are here: 🛡️ Audit (the forensics sibling of 🗜️ Liquefy).**`
- **nebula-media** → `**You are here: 🎬 Media (Liquefy's codec idea, applied to scenes instead of logs).**`
- **nulla-local** → `**You are here: 🧠 Local AI (the runtime that consumes every layer above).**`

## Planned layers

Do **not** add these to live READMEs until the repo is published (a dead link breaks the "every link works" rule):

| Layer | Repo | Does |
|---|---|---|
| 🗄️ Memory | `liquefy-memory` *(unreleased)* | MCP agent memory — 800× compressed, filter-search without decompress, x402-metered |

---

© 2026 [Parad0x Labs](https://github.com/Parad0x-Labs) — MIT
