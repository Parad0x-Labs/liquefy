# liquefy

Columnar compression that beats Zstd on structured data. Built-in search. AES-256-GCM. MIT.

Format-aware columnar compression. 226x on JSON logs, 876x on payment receipts. Lossless and searchable without full decompression. Used in DNA x402 for AI agent payment receipt compression on Solana.

### How this fits the Parad0x stack

Parad0x Labs builds Web0 on Solana — money and agents that settle themselves. **You are here: 🗜️ Data.**

| Layer | Repo | Does |
|---|---|---|
| 💸 Payments | [dna-x402](https://github.com/Parad0x-Labs/dna-x402) | x402 rail: quote → pay → verify → receipt → anchor |
| 🛠️ Build | [dna-x402-builders](https://github.com/Parad0x-Labs/dna-x402-builders) | Hosted kit: turn any API/bot into a paid agent |
| 🕶️ Privacy | [Dark-Null-Protocol](https://github.com/Parad0x-Labs/Dark-Null-Protocol) | Groth16 privacy settlement, published proofs |
| 🗜️ Data | [liquefy](https://github.com/Parad0x-Labs/liquefy) (this repo) | Columnar compression that beats Zstd + audit trails |
| 🎬 Media | [nebula-media](https://github.com/Parad0x-Labs/nebula-media) | Perceptual video re-encoding, VMAF quality proofs |
| 🧠 Local AI | [nulla-local](https://github.com/Parad0x-Labs/nulla-local) | Local-first agent runtime — your machine, your memory |

**See it live**: [parad0xlabs.com](https://parad0xlabs.com)

---

Full documentation, benchmarks, and proof-pack are in this repository.

```python
pip install liquefy
from liquefy import compress_records
blob = compress_records(receipts)          # 876x on x402 receipts
commitment = sha256(blob).digest()         # 32 bytes — ready to anchor on Solana
```

**License:** MIT — © 2026 Parad0x Labs
