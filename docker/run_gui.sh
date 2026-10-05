#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

# Host X11 and OpenGL software. Run GUI-based tools inside the COMET Toolchain Docker container.

set -euo pipefail

# Define the default Docker image to be used.
IMAGE="${COMET_IMAGE:-comet-toolchain:v1.0.0}"

# Define the default application.
APP="${1:-freecad}"
shift || true

# Store the container's "state" inside the repository folder.
STATE_DIR="$PWD/.devcontainer-state/home"
mkdir -p \
    "$STATE_DIR/.cache" \
    "$STATE_DIR/.config" \
    "$STATE_DIR/.local/share"

# XAuth settings.
XAUTHORITY_HOST="${XAUTHORITY:-$HOME/.Xauthority}"
XAUTH_ARGS=()
if [[ -f "$XAUTHORITY_HOST" ]]; then
    XAUTH_ARGS+=(
        -v "$XAUTHORITY_HOST:/tmp/.docker.xauth:ro"
        -e "XAUTHORITY=/tmp/.docker.xauth"
    )
else
    echo "Warning: no Xauthority file found at location: $XAUTHORITY_HOST" >&2
    echo "Continuing with xhost-based X11 access only." >&2
fi

# Always reset xhost.
cleanup() {
    xhost -si:localuser:"$(id -un)" >/dev/null 2>&1 || true
}
trap cleanup EXIT

# Debug information for the GUI display.
if [[ -n "${DISPLAY:-}" ]]; then
    xhost +si:localuser:"$(id -un)"
else
    echo "Error: Environment variable DISPLAY is not set. Cannot start GUI applications." >&2
    exit 1
fi

docker run -it --rm \
    -u "$(id -u):$(id -g)" \
    -v "$PWD:/app" \
    -w /app \
    -v "$STATE_DIR:/home/comet" \
    -v "$PWD/mechanical/prints/profiles/prusaslicer:/opt/prusaslicer-config:ro" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    -v /etc/localtime:/etc/localtime:ro \
    "${XAUTH_ARGS[@]}" \
    -e HOME=/home/comet \
    -e XDG_CACHE_HOME=/home/comet/.cache \
    -e XDG_CONFIG_HOME=/home/comet/.config \
    -e XDG_DATA_HOME=/home/comet/.local/share \
    -e XDG_RUNTIME_DIR="/tmp/runtime-$(id -u)" \
    -e DISPLAY="${DISPLAY}" \
    -e QT_X11_NO_MITSHM=1 \
    -e LIBGL_ALWAYS_SOFTWARE="${LIBGL_ALWAYS_SOFTWARE:-1}" \
    -e MESA_LOADER_DRIVER_OVERRIDE="${MESA_LOADER_DRIVER_OVERRIDE:-llvmpipe}" \
    -e NO_AT_BRIDGE=1 \
    -e PRUSASLICER_DATADIR="/opt/prusaslicer-config" \
    "$IMAGE" \
    "$APP" "$@"