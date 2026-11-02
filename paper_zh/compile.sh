#!/bin/bash
set -e

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
    cp -f main.pdf paper_elsarticle.pdf
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
cp -f main.pdf paper_elsarticle.pdf
echo "Compilation complete. Output: paper.pdf"
