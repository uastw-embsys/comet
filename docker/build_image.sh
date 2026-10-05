#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

set -euo pipefail

# Resolve paths regardless of where the script is called from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Docker image settings.
IMAGE="${COMET_IMAGE:-comet-toolchain:v1.0.0}"

# Try the GHCR.io image before building locally.
GHCR_IMAGE="${COMET_GHCR_IMAGE:-ghcr.io/uastw-embsys/comet-toolchain:v1.0.0}"

# Define the versions of the tools to be used.
UBUNTU_VERSION="${UBUNTU_VERSION:-noble}"
FREECAD_VERSION="${FREECAD_VERSION:-1.1.3}"
PRUSASLICER_VERSION="${PRUSASLICER_VERSION:-2.9.6}"

# 1. Check to see if the image already exists locally.
if docker image inspect "${IMAGE}" >/dev/null 2>&1; then
    echo "Using local Docker image: ${IMAGE}"
    exit 0
fi

# 2. Try pulling the image from GHCR.io.
echo "Local image not found: ${IMAGE}"
echo "Trying to pull image from GHCR: ${GHCR_IMAGE}"

if docker pull "${GHCR_IMAGE}"; then
    echo "Pulled GHCR image: ${GHCR_IMAGE}"

    # Tag the pulled image with the same name as the local image.
    if [[ "${GHCR_IMAGE}" != "${IMAGE}" ]]; then
        docker tag "${GHCR_IMAGE}" "${IMAGE}"
        echo "Tagged ${GHCR_IMAGE} as ${IMAGE}"
    fi

    exit 0
fi

# 3. Build the image as a last resort.
echo "GHCR image not available. Building Docker image locally: ${IMAGE}"

docker buildx build \
    --load \
    --target runtime \
    --file "${REPO_ROOT}/docker/Dockerfile" \
    --tag "${IMAGE}" \
    --build-arg "UBUNTU_VERSION=${UBUNTU_VERSION}" \
    --build-arg "FREECAD_VERSION=${FREECAD_VERSION}" \
    --build-arg "PRUSASLICER_VERSION=${PRUSASLICER_VERSION}" \
    "${REPO_ROOT}"