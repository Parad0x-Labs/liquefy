# Offline Licensing

Parad0x Labs uses a "Zero-Network" licensing model for enterprise decoders. This ensures that the appliance can operate in air-gapped or high-security environments without ever "calling home."

## Licensing Scope

Licenses apply to:
- Compression
- Orchestration
- Performance features
- Enterprise operational guarantees

Licenses do NOT apply to:
- Decode-only recovery
- Integrity verification
- Offline data restoration

Parad0x Labs does not restrict access to existing data.

## License File Format

The license is a simple JSON file, typically named `liquefy.lic`. It is mounted into the container at `/license/liquefy.lic`.

### Example Format (Reference Only)

```json
{
  "license_id": "LIC-12345-ABCD",
  "issued_to": "Enterprise Client Name",
  "expires_utc": "2027-01-01T00:00:00Z",
  "features": ["decode", "verify", "search"],
  "max_bytes_per_month": 1000000000000,
  "signature": "BASE64_HMAC_OR_ED25519_SIGNATURE_HERE"
}
```

## Verification Mechanism

1. **Embedded Public Key:** The decoder binary contains an embedded public key.
2. **Cryptographic Validation:** Upon startup, the decoder validates the JSON structure and the cryptographic signature.
3. **No Network Required:** Validation is purely mathematical and happens locally within the "Blackbox."

## Deployment

In a Docker environment, the license is provided via a read-only volume mount:

```bash
docker run -v $(pwd)/liquefy.lic:/license/liquefy.lic:ro ...
```

To check your license status:
```bash
liquefy-decoder license status
```

