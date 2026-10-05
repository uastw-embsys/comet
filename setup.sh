#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

set -euo pipefail

# Resolve paths regardless of where the script is called from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}"

# Set up the project's Docker image, which includes all the necessary tools.
${REPO_ROOT}/docker/build_image.sh

# Update the sources and generate the exports/artifacts.
${REPO_ROOT}/update_project.sh