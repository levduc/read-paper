#!/bin/sh
# Serve one paper folder on this machine only, so the deck works with KaTeX and fonts.
# usage: tools/serve.sh [folder] [port] [address]   (defaults: . 8028 127.0.0.1)
# Papers under review are confidential: never bind to 0.0.0.0.
dir="${1:-.}"; port="${2:-8028}"; addr="${3:-127.0.0.1}"
case "$addr" in 0.0.0.0|::|'') echo "refusing to serve on all interfaces ($addr)" >&2; exit 2;; esac
cd "$dir" || exit 1
echo "serving $(pwd) at http://$addr:$port/deck/"
exec python3 -m http.server "$port" --bind "$addr"
