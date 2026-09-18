#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

# Setup project's docker image which includes all tools needed.

cd docker
. build_image.sh
cd ..
