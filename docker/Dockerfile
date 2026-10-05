# syntax=docker/dockerfile:1
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

# --------------------------------------------------------------------
# Define used versions
# --------------------------------------------------------------------

ARG UBUNTU_VERSION=noble
ARG FREECAD_VERSION=1.1.3
ARG PRUSASLICER_VERSION=2.9.6

# --------------------------------------------------------------------
# Common build base
# --------------------------------------------------------------------

# Pull base image.
FROM ubuntu:${UBUNTU_VERSION} AS build-base

# Set the maintainer information for this Dockerfile
LABEL maintainer="Christoph Boehm<christoph.boehm@technikum-wien.at>"

# Set the default shell to bash for RUN commands
# This ensures all RUN commands use bash instead of sh
SHELL ["/bin/bash", "-c"]

## Get common tools
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        file \
        git \
        nano \
        pkg-config \
        sudo \
        wget \
        x11-apps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------
# FreeCAD builder
# Install FreeCAD: https://wiki.freecad.org/Compile_on_Linux#
# Additional Sources:
# - https://servercake.in/guides/package-management/building-from-source
# --------------------------------------------------------------------
FROM build-base AS freecad-builder

ARG FREECAD_VERSION

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        doxygen \
        libboost-date-time-dev \
        libboost-dev \
        libboost-filesystem-dev \
        libboost-graph-dev \
        libboost-iostreams-dev \
        libboost-program-options-dev \
        libboost-python-dev \
        libboost-regex-dev \
        libboost-serialization-dev \
        libboost-thread-dev \
        libcoin-dev \
        libeigen3-dev \
        libgl1-mesa-dri \
        libglu1-mesa-dev \
        libglx-mesa0 \
        libgtkglext1-dev \
        libkdtree++-dev \
        libkml-dev \
        libmedc-dev \
        libocct-data-exchange-dev \
        libocct-draw-dev \
        libocct-foundation-dev \
        libocct-modeling-algorithms-dev \
        libocct-modeling-data-dev \
        libocct-ocaf-dev \
        libocct-visualization-dev \
        libopencv-dev \
        libproj-dev \
        libpyside2-dev \
        libqt5svg5-dev \
        libshiboken2-dev \
        libvtk9-dev \
        libvtk9-qt-dev \
        libvtk-dicom-dev \
        libx11-dev \
        libx11-xcb1 \
        libxcb-glx0 \
        libxerces-c-dev \
        libxmu-dev \
        libxmuu-dev \
        libxrandr2 \
        libxrender1 \
        libyaml-cpp-dev \
        libzipios++-dev \
        netgen \
        netgen-headers \
        pyside2-tools \
        python3-dev \
        python3-matplotlib \
        python3-pivy \
        python3-ply \
        python3-pyside2.qtnetwork \
        python3-pyside2.qtsvg \
        python3-pyside2.qtuitools \
        python3-yaml \
        qtchooser \
        qttools5-dev \
        qtwayland5 \
        shiboken2 \
        swig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

## Switch to /tmp as working directory
WORKDIR /tmp

## Get FreeCAD source
RUN wget -O freecad-source.tar.gz \
    "https://github.com/FreeCAD/FreeCAD/releases/download/${FREECAD_VERSION}/freecad_source_${FREECAD_VERSION}.tar.gz" \
    && mkdir -p freecad-source \
    && tar -xvzf freecad-source.tar.gz -C freecad-source \
    && rm freecad-source.tar.gz

## Configure Build
RUN cmake -S freecad-source -B freecad-build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/opt/freecad \
    -DBUILD_TEST=OFF

## Build from Source
RUN cmake --build freecad-build --parallel "$(nproc --ignore=2)"

## Install into stage folder for Run-Time install later
RUN DESTDIR=/stage cmake --install freecad-build --strip

# --------------------------------------------------------------------
# PrusaSlicer builder
# Build from Source: https://github.com/prusa3d/PrusaSlicer/blob/version_2.9.6/doc/How%20to%20build%20-%20Linux%20et%20al.md
# --------------------------------------------------------------------
FROM build-base AS prusaslicer-builder

ARG PRUSASLICER_VERSION

## Set Environment
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        autoconf \
        automake \
        doxygen \
        graphviz \
        libdbus-1-dev \
        libglu1-mesa-dev \
        libgtk-3-dev \
        libhidapi-dev \
        libtool \
        libusb-1.0-0-dev \
        libwebkit2gtk-4.1-dev \
        m4 \
        texinfo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

## Get PrusaSlicer source
# strip-components=1 do get rid of sub-folders
RUN wget -O prusaslicer-source.tar.gz \
    "https://github.com/prusa3d/PrusaSlicer/archive/refs/tags/version_${PRUSASLICER_VERSION}.tar.gz" \
    && mkdir -p prusaslicer-source \
    && tar -xvzf prusaslicer-source.tar.gz -C prusaslicer-source --strip-components=1\
    && rm prusaslicer-source.tar.gz

## Configure PrusaSlicer dependencies
RUN cmake -S prusaslicer-source/deps -B prusaslicer-source/deps/build -DDEP_WX_GTK3=ON

## Build PrusaSlicer dependencies
RUN cmake --build prusaslicer-source/deps/build --parallel "$(nproc --ignore=2)"

## Configure PrusaSlicer
RUN cmake -S prusaslicer-source -B prusaslicer-build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/opt/prusaslicer \
    -DSLIC3R_STATIC=1 \
    -DSLIC3R_GTK=3 \
    -DSLIC3R_PCH=OFF \
    -DCMAKE_PREFIX_PATH=$(pwd)/prusaslicer-source/deps/build/destdir/usr/local

## Build PrusaSlicer
RUN cmake --build prusaslicer-build --parallel "$(nproc --ignore=2)"

## Stage/Install PrusaSlicer
RUN DESTDIR=/stage cmake --install prusaslicer-build --strip

# --------------------------------------------------------------------
# Runtime image
# --------------------------------------------------------------------
FROM ubuntu:${UBUNTU_VERSION} AS runtime

LABEL maintainer="Christoph Boehm <christoph.boehm@technikum-wien.at>"

SHELL ["/bin/bash", "-c"]


RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        locales \
        dbus \
        dbus-x11 \
        dbus-user-session \
        dconf-service \
        xdg-utils \
        shared-mime-info \
        librsvg2-common \
        libgdk-pixbuf2.0-bin \
        adwaita-icon-theme \
        hicolor-icon-theme \
        fonts-dejavu-core \
        fontconfig \
        libgl1 \
        libgl1-mesa-dri \
        libglu1-mesa \
        libegl1 \
        libglx-mesa0 \
        libx11-6 \
        libx11-xcb1 \
        libxcb-glx0 \
        libxext6 \
        libxrender1 \
        libxi6 \
        libxrandr2 \
        libxinerama1 \
        libxcursor1 \
        libxdamage1 \
        libxfixes3 \
        libxxf86vm1 \
        libxmu6 \
        libxmuu1 \
        libgtk-3-0 \
        libgtkglext1 \
        libwebkit2gtk-4.1-0 \
        libdbus-1-3 \
        libnotify4 \
        libsecret-1-0 \
        libqt5printsupport5 \
        libyaml-cpp0.8 \
        libxerces-c3.2t64 \
        libboost-program-options1.83.0 \
        libhidapi-hidraw0 \
        libqt5concurrent5 \
        libvtk9.1t64 \
        libvtk9.1t64-qt \
        libmedc11t64 \
        libboost-thread1.83.0 \
        python3 \
        python3-matplotlib \
        python3-pivy \
        python3-ply \
        python3-pyside2.qtnetwork \
        python3-pyside2.qtsvg \
        python3-pyside2.qtuitools \
        python3-yaml \
        qtwayland5 \
        netgen \
        && sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen \
        && locale-gen en_US.UTF-8 \
        && update-locale LANG=en_US.UTF-8 \
        && update-ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only installed applications.
COPY --from=freecad-builder /stage/opt/freecad /opt/freecad
COPY --from=prusaslicer-builder /stage/opt/prusaslicer /opt/prusaslicer

# Application paths.
RUN echo "/opt/freecad/lib" > /etc/ld.so.conf.d/freecad.conf \
    && echo "/opt/prusaslicer/lib" > /etc/ld.so.conf.d/prusaslicer.conf \
    && ldconfig
ENV PATH="/usr/local/bin:/opt/freecad/bin:/opt/prusaslicer/bin:${PATH}"

# Optional, helps FreeCAD Python module lookup in some builds.
ENV PYTHONPATH="/opt/freecad/lib"

# Avoid AT-SPI warnings in minimal containers.
ENV NO_AT_BRIDGE=1

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_DIR=/etc/ssl/certs
ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Adding "PRUSASLICER_DATADIR" automatically to prusa-slicer call
RUN mv /opt/prusaslicer/bin/prusa-slicer /opt/prusaslicer/bin/prusa-slicer.real \
    && cat >/usr/local/bin/prusa-slicer <<'EOF' \
    && chmod +x /usr/local/bin/prusa-slicer
#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${PRUSASLICER_DATADIR:-}" ]]; then
    for arg in "$@"; do
        case "$arg" in
            --datadir|--datadir=*)
                exec /opt/prusaslicer/bin/prusa-slicer.real "$@"
                ;;
        esac
    done
    exec /opt/prusaslicer/bin/prusa-slicer.real --datadir "$PRUSASLICER_DATADIR" "$@"
else
    exec /opt/prusaslicer/bin/prusa-slicer.real "$@"
fi
EOF

# Small launcher that selects FreeCAD or PrusaSlicer in CMD of GUI mode.
RUN cat >/usr/local/bin/comet-toolchain-launch <<'EOF' \
 && chmod +x /usr/local/bin/comet-toolchain-launch
#!/usr/bin/env bash
set -euo pipefail

app="${1:-freecad}"
shift || true

mkdir -p \
    "${XDG_RUNTIME_DIR:-/tmp/runtime-$(id -u)}" \
    "${XDG_CONFIG_HOME:-$HOME/.config}" \
    "${XDG_CACHE_HOME:-$HOME/.cache}" \
    "${XDG_DATA_HOME:-$HOME/.local/share}"

chmod 700 "${XDG_RUNTIME_DIR:-/tmp/runtime-$(id -u)}" || true

case "${app}" in
    freecad)
        exec FreeCAD "$@"
        ;;

    freecadcmd)
        exec FreeCADCmd "$@"
        ;;

    prusaslicer)
        exec prusa-slicer "$@"
        ;;

    bash)
        exec "${app}" "$@"
        ;;

    *)
        echo "Unknown application: ${app}" >&2
        echo "Usage: comet-toolchain-launch [freecad|freecadcmd|prusaslicer|bash]" >&2
        exit 2
        ;;
esac
EOF

#"smoke tests", runtime linker check, paths, binaries, and Python calls
RUN set -e; \
    find /opt/freecad /opt/prusaslicer -type f -print0 \
    | xargs -0 file \
    | awk -F: '/ELF/ {print $1}' \
    | while read -r f; do ldd "$f" || true; done \
    | tee /tmp/ldd.log; \
    ! grep -q "not found" /tmp/ldd.log
RUN FreeCADCmd --version
RUN prusa-slicer --help >/dev/null
RUN python3 - <<'PY'
import subprocess
subprocess.run(["FreeCADCmd", "--version"], check=True)
subprocess.run(["prusa-slicer", "--help"], check=True)
PY

WORKDIR /app

ENTRYPOINT ["comet-toolchain-launch"]
CMD ["bash"]