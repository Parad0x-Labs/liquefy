# Proof Pack — Value-Lossless Verification (SHA-256)

Reference samples and cryptographic proofs to validate the Liquefy Conduction Engine on your local machine.

Pinned Docker image: `nullaai/liquefy-decoder-public@sha256:b7a0499f38d192e7333c760fcf8e429abcff83e58610259841f2ffb525c02935`

## Directory Structure

- `samples/raw/` — Original uncompressed log samples.
- `samples/compressed/` — Production `.null` archives.
- `samples/restored/` — Value-lossless restorations produced by the public SDK (SHA-256-verified against the originals; for these line-oriented samples the recovered bytes also match exactly).

---

## Verify (no decompress needed)

Run the built-in integrity check directly against the `.null` archive:

```bash
./liquefy verify proof-pack/samples/compressed/sample_nginx.null
```

Expected output:

```
OK  proof-pack/samples/compressed/sample_nginx.null
    embedded-sha256: d3f754f3d64a8c7071aacc263cdf3519d3ec28ebbb0a6ebe2217e2cab278aad8
    status: PASS
```

---

## Full Decompression + Diff

Decompress the archive, then confirm the restored file matches the original by SHA-256 (recovery is value-lossless; for these line-oriented samples the bytes also match exactly):

```bash
./liquefy decompress proof-pack/samples/compressed/sample_nginx.null proof-pack/samples/restored/sample_nginx.log
```

Verify the SHA-256 of the restored file:

```bash
sha256sum proof-pack/samples/restored/sample_nginx.log
```

Expected:

```
5380290fb0a6967b0a4d66e5b201bf0d76492bed33fff6b0fe0a3966c37a1ce4  proof-pack/samples/restored/sample_nginx.log
```

Diff against the original:

```bash
diff proof-pack/samples/raw/sample_nginx.log proof-pack/samples/restored/sample_nginx.log
```

Expected: no output (no output = bytes match for this sample; in general recovery is value-lossless and SHA-256-verified).

---

## Hash Reference

| File | SHA-256 |
|------|---------|
| `samples/raw/sample_nginx.log` | `5380290fb0a6967b0a4d66e5b201bf0d76492bed33fff6b0fe0a3966c37a1ce4` |
| `samples/compressed/sample_nginx.null` | `d3f754f3d64a8c7071aacc263cdf3519d3ec28ebbb0a6ebe2217e2cab278aad8` |
| Docker image (`nullaai/liquefy-decoder-public`) | `sha256:b7a0499f38d192e7333c760fcf8e429abcff83e58610259841f2ffb525c02935` |

---

Requires Docker. On Windows use WSL or Git Bash.
