#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

# Host X11, software OpenGL
# Run FreeCAD with GUI inside the COMET Docker container.

xhost +si:localuser:$(id -un)

docker run -it --rm \
    -u $(id -u):$(id -g) \
    -v ${XAUTHORITY:-$HOME/.Xauthority}:${XAUTHORITY:-$HOME/.Xauthority}:ro \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -v $PWD:/app \
    -e HOME=/app/.devcontainer-state/home \
    -e XDG_CACHE_HOME=/app/.devcontainer-state/home/.cache \
    -e XDG_CONFIG_HOME=/app/.devcontainer-state/home/.config \
    -e XDG_DATA_HOME=/app/.devcontainer-state/home/.local/share \
    -e DISPLAY=$DISPLAY \
    -e XAUTHORITY=${XAUTHORITY:-$HOME/.Xauthority} \
    -e QT_X11_NO_MITSHM=1 \
    -e XDG_RUNTIME_DIR=/tmp/runtime-$(id -u) \
    -e LIBGL_ALWAYS_SOFTWARE=1 \
    -e MESA_LOADER_DRIVER_OVERRIDE=llvmpipe \
    -e NO_AT_BRIDGE=1 \
    -w /app \
    comet:v1.0.0 \
    bash -lc 'mkdir -p "$XDG_RUNTIME_DIR" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$XDG_DATA_HOME" && chmod 700 "$XDG_RUNTIME_DIR" && dbus-run-session -- /prusaslicer-source/PrusaSlicer-version_2.9.6/build/src/prusa-slicer'
    #FreeCAD

xhost -si:localuser:$(id -un)