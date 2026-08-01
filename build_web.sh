#!/usr/bin/env bash
# Build the web (WebAssembly) version of the game into build/web/.
#
#   pip install pygbag
#   ./build_web.sh
#
# The result in build/web/ is a plain static site: index.html, favicon.png and
# towerdefense.apk (the game + assets). It is committed to the repo so Vercel
# can serve it without a build step - re-run this script and commit whenever
# you change the game.
#
# To try it locally before deploying:
#   python3 -m pygbag --template web/default.tmpl --icon favicon.png .
#   -> open http://localhost:8000
set -euo pipefail

cd "$(dirname "$0")"

python3 -m pygbag \
    --build \
    --title "Tower Defense" \
    --app_name towerdefense \
    --width 1020 \
    --height 720 \
    --template web/default.tmpl \
    --icon favicon.png \
    .

# Both archives are kept on purpose: the loader in index.html downloads the
# .tar.gz on a normal host (Vercel) and the .apk only on itch.io.

echo
echo "Done. Static site in build/web/:"
ls -la build/web
