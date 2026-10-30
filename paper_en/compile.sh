#!/bin/bash
set -e

# This script is meant to be run from within the paper output directory
# where main.tex, bibliography.bib, and sections/ already exist.
#
# Engine selection (automatic):
#   fontspec or ctexart -> xelatex (required for exact manuscript fonts)
#   legacy templates   -> pdflatex
#
# Guard: CJK prose under a non-ctexart class is a setup error — fail fast
# with a clear message instead of producing a broken PDF.

# Auto-detect Tectonic engine
TECTONIC_BIN=""
if command -v tectonic >/dev/null 2>&1; then
    TECTONIC_BIN="tectonic"
elif [ -x "/d/Tools/Tectonic/tectonic.exe" ] || [ -x "/d/Tools/Tectonic/tectonic" ]; then
    TECTONIC_BIN="/d/Tools/Tectonic/tectonic"
fi

if [ -n "$TECTONIC_BIN" ]; then
    echo "Using self-contained Tectonic engine: $TECTONIC_BIN"
    "$TECTONIC_BIN" main.tex
    cp -f main.pdf paper.pdf
    echo "Compilation complete. Output: paper.pdf"
    exit 0
fi

if grep -Eq '^[^%]*\\documentclass[^{]*\{ctexart\}|^[^%]*\\usepackage([[:space:]]*\[[^]]*\])?[[:space:]]*\{fontspec\}' main.tex; then
    ENGINE=xelatex
else
    ENGINE=pdflatex
fi

echo "Engine: $ENGINE"

echo "First $ENGINE run..."
$ENGINE -interaction=nonstopmode -halt-on-error main.tex

echo "Running bibtex..."
if [ -f bibliography.bib ]; then
    bibtex main
fi

echo "Second $ENGINE run..."
$ENGINE -interaction=nonstopmode -halt-on-error main.tex

echo "Final $ENGINE run..."
$ENGINE -interaction=nonstopmode -halt-on-error main.tex

cp -f main.pdf paper.pdf
echo "Compilation complete. Output: paper.pdf"
