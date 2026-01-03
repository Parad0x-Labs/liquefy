# Liquefy Sealed Decoder Appliance
# Public Specification - Production Binary Not Included

# Use Google's distroless static image for maximum security
# This image contains only the minimal set of libraries needed to run a static binary
FROM gcr.io/distroless/static-debian12:nonroot

LABEL maintainer="hello@parad0xlabs.com"
LABEL description="Sealed Blackbox Decoder for Liquefy Archives"

WORKDIR /app

# The liquefy-decoder binary must be present in the build context.
# It is not included in the public repository to protect proprietary IP.
COPY --chown=nonroot:nonroot liquefy-decoder /app/liquefy-decoder
COPY --chown=nonroot:nonroot entrypoint.sh /app/entrypoint.sh

# Ensure the binary is executable
# Note: chmod is not available in distroless, binary must be executable in build context.

USER nonroot:nonroot

# The entrypoint proxies all commands to the decoder binary and prevents shell access.
ENTRYPOINT ["/app/entrypoint.sh"]

