#!/usr/bin/env bash
# Install OpenRadioss linux64 release binaries into $OPENRADIOSS_HOME (default ~/.cache/openradioss).
# Idempotent: skips download if starter+engine already present. TLS verification stays on.
# Usage: source <(tools/openradioss/setup.sh --env)   # prints env exports after install
set -euo pipefail
HOME_DIR="${OPENRADIOSS_HOME:-$HOME/.cache/openradioss}"
REPO="OpenRadioss/OpenRadioss"
mkdir -p "$HOME_DIR"

find_bin() { find "$HOME_DIR" -type f -name "$1" 2>/dev/null | head -1; }

if [ -z "$(find_bin 'starter_linux64_gf*')" ] || [ -z "$(find_bin 'engine_linux64_gf*')" ]; then
  echo "[openradioss] resolving latest release of $REPO" >&2
  URL=$(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" \
        | python3 -c 'import json,sys;a=json.load(sys.stdin)["assets"];print(next(x["browser_download_url"] for x in a if "linux64" in x["name"] and x["name"].endswith(".zip")))')
  echo "[openradioss] downloading $URL" >&2
  curl -fSL --retry 3 -o "$HOME_DIR/openradioss.zip" "$URL"
  (cd "$HOME_DIR" && python3 -m zipfile -e openradioss.zip . && rm -f openradioss.zip)
  find "$HOME_DIR" -path '*exec*' -type f -exec chmod +x {} +
fi

ROOT=$(dirname "$(dirname "$(find_bin 'starter_linux64_gf*')")")
ENVS="export OPENRADIOSS_PATH=$ROOT
export RAD_CFG_PATH=$ROOT/hm_cfg_files
export RAD_H3D_PATH=$ROOT/extlib/h3d/lib/linux64
export LD_LIBRARY_PATH=$ROOT/extlib/hm_reader/linux64:$ROOT/extlib/h3d/lib/linux64:\${LD_LIBRARY_PATH:-}
export OMP_STACKSIZE=400m"
if [ "${1:-}" = "--env" ]; then echo "$ENVS"; exit 0; fi
eval "$ENVS"
"$(find_bin 'starter_linux64_gf')" -version >/dev/null 2>&1 && echo "[openradioss] starter OK" || echo "[openradioss] starter FAILED"
"$(find_bin 'engine_linux64_gf')" -version >/dev/null 2>&1 && echo "[openradioss] engine OK" || echo "[openradioss] engine FAILED"
echo "$ENVS"
