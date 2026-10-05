#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

# Start the Ubuntu Bash shell within the COMET Toolchain Docker container.

set -euo pipefail

# Define the default Docker image to be used.
IMAGE="${COMET_IMAGE:-comet-toolchain:v1.0.0}"

docker run -it --rm \
    -u "$(id -u):$(id -g)" \
    -v "$PWD:/app" \
    -w /app \
    -v "$PWD/mechanical/prints/profiles/prusaslicer:/opt/prusaslicer-config:ro" \
    -e HOME=/tmp/comet-home \
    -e XDG_CACHE_HOME=/tmp/comet-home/.cache \
    -e XDG_CONFIG_HOME=/tmp/comet-home/.config \
    -e XDG_DATA_HOME=/tmp/comet-home/.local/share \
    -e XDG_RUNTIME_DIR="/tmp/runtime-$(id -u)" \
    -e NO_AT_BRIDGE=1 \
    -e PRUSASLICER_DATADIR="/opt/prusaslicer-config" \
    "$IMAGE" \
    bash