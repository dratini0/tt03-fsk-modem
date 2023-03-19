#!/bin/sh

set -eux

. ./env

# Check support tools exist
TT=$(pwd)/tt-support-tools
if [ ! -d "$TT" ]; then
    echo "Cloning TT support tools repo..."
    git clone https://github.com/tinytapeout/tt-support-tools $TT
fi

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
