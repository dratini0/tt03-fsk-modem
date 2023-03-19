#!/bin/sh

set -eux

. ./env

# Install python deps
if ! which cocotb-config; then
    pip install -qr requirements.txt
fi

# Run tests
cd src
make
