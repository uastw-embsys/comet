#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

# Build the COMET Docker image.

DOCKER_BUILDKIT=1 docker build -t comet:v1.0.0 .

# DOCKER_BUILDKIT=1 docker build --progress=plain -t comet:v1.0.0 .
