#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

# No X11 and GPU
# Run FreeCADCmd scripts inside the COMET Docker container.

# set -euo pipefail

SCRIPTS=("$@")

SCRIPT_COMMANDS=""
if [ "${#SCRIPTS[@]}" -eq 0 ]; then
    SCRIPT_COMMANDS+="FreeCADCmd"
else
    for script in "${SCRIPTS[@]}"; do
        SCRIPT_COMMANDS+="FreeCADCmd -c /app/$script; "
    done
    SCRIPT_COMMANDS=${SCRIPT_COMMANDS::-2}
fi

echo "USED COMMAND: cd /app; $SCRIPT_COMMANDS"

docker run -it --rm \
    -u $(id -u):$(id -g) \
    -v /etc/localtime:/etc/localtime:ro \
    -v $PWD:/app \
    -e HOME=/app/.devcontainer-state/home \
    -e XDG_CACHE_HOME=/app/.devcontainer-state/home/.cache \
    -e XDG_CONFIG_HOME=/app/.devcontainer-state/home/.config \
    -e XDG_DATA_HOME=/app/.devcontainer-state/home/.local/share \
    -e LIBGL_ALWAYS_SOFTWARE=1 \
    -e MESA_LOADER_DRIVER_OVERRIDE=llvmpipe \
    -w /app \
    comet:v1.0.0 \
    bash -c "cd /app; $SCRIPT_COMMANDS"
