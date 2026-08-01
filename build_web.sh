#!/usr/bin/env bash
# Build the web (WebAssembly) version of the game into build/web/.
#
#   pip install pygbag
#   ./build_web.sh
#
# Requires internet: pygbag downloads the HTML template matching its own
# version from https://pygame-web.github.io/cdn/<version>/ (and caches it in
# build/web-cache/). Do NOT pass --template with a hand-picked file - a
# template from a different version than the runtime gives a blank page.
#
# The result in build/web/ is a plain static site. It is committed to the repo
# so Vercel can serve it without a build step - re-run this script and commit
# whenever you change the game.
#
# To try it locally before deploying:
#   cd build/web && python3 -m http.server 8000   -> http://127.0.0.1:8000
# Use 127.0.0.1, not localhost: on "http://localhost:8*" the runtime switches to
# a dev mode that looks for pygame-ce under /cdn/ on your own server.
set -euo pipefail

cd "$(dirname "$0")"

python3 -m pygbag \
    --build \
    --title "Tower Defense" \
    --app_name towerdefense \
    --width 1020 \
    --height 720 \
    --icon favicon.png \
    .

# Both archives are kept on purpose: the loader in index.html downloads the
# .tar.gz on a normal host (Vercel) and the .apk only on itch.io.

echo
echo "Done. Static site in build/web/:"
ls -la build/web
