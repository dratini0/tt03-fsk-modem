#!/bin/sh

set -eux

export OPENLANE_TAG=2023.02.14
export OPENLANE_IMAGE_NAME=efabless/openlane:4cd0986b3ae550cdf7a6d0fba4e0657012f635d8-amd64
export OPENLANE_ROOT=$(pwd)/OpenLane
export PDK_ROOT=$(pwd)/PDK
export PDK=sky130A

# Check support tools exist
TT=$(pwd)/tt-support-tools
if [ ! -d "$TT" ]; then
    echo "Cloning TT support tools repo..."
    git clone https://github.com/tinytapeout/tt-support-tools $TT
fi

# Create and activate python venv
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
. .venv/bin/activate

# Install python deps
pip install -qr $TT/requirements.txt

# Check openlane exists
if [ ! -d "$OPENLANE_ROOT" ]; then
   git clone --depth=1 --branch $OPENLANE_TAG https://github.com/The-OpenROAD-Project/OpenLane.git $OPENLANE_ROOT
fi

# Build openlane
(cd OpenLane && make)

# Fetch the Verilog from Wokwi API
$TT/tt_tool.py --create-user-config

# Run OpenLane to build the GDS
$TT/tt_tool.py --harden

# Yosys warnings
$TT/tt_tool.py --print-warnings

# Print some routing stats
$TT/tt_tool.py --print-stats

# Print some cell stats
$TT/tt_tool.py --print-cell-category

# create png
$TT/tt_tool.py --create-png
