#!/bin/sh
set -eu

# Fail-closed command gate for Liquefy Decoder Appliance
# Only explicitly allowed commands may execute.
# Any deviation results in immediate termination.

CMD="${1:-}"

case "$CMD" in
  version)
    exec /app/liquefy-decoder version
    ;;
  decompress)
    shift
    exec /app/liquefy-decoder decompress "$@"
    ;;
  verify)
    shift
    exec /app/liquefy-decoder verify "$@"
    ;;
  license)
    shift
    exec /app/liquefy-decoder license "$@"
    ;;
  *)
    echo "ERROR: Unsupported command."
    echo "Allowed commands: version | decompress | verify | license"
    exit 64
    ;;
esac
