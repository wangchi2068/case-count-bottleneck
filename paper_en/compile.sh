#!/bin/bash
set -e

# Build paper_en. Both manuscripts require XeLaTeX (fontspec + unicode-math);
# pdflatex fails by design inside main.tex. Prefer a self-contained Tectonic
# binary when one is available, and fall back to a local XeLaTeX + BibTeX toolchain.

# Tectonic: explicit override via $TECTONIC, then PATH, then a common local install.
TECTONIC_BIN=""
if [ -n "${TECTONIC:-}" ] && [ -x "${TECTONIC}" ]; then
    TECTONIC_BIN="${TECTONIC}"
elif command -v tectonic >/dev/null 2>&1; then
    TECTONIC_BIN="$(command -v tectonic)"
elif [ -x "/d/Tools/Tectonic/tectonic" ]; then
    TECTONIC_BIN="/d/Tools/Tectonic/tectonic"
elif [ -x "/d/Tools/Tectonic/tectonic.exe" ]; then
    TECTONIC_BIN="/d/Tools/Tectonic/tectonic.exe"
fi

if [ -n "$TECTONIC_BIN" ]; then
    echo "Engine: Tectonic ($TECTONIC_BIN)"
    "$TECTONIC_BIN" main.tex
    cp -f main.pdf paper.pdf
    echo "Compilation complete. Output: paper.pdf"
    exit 0
fi

if ! command -v xelatex >/dev/null 2>&1; then
    echo "ERROR: neither Tectonic nor XeLaTeX was found." >&2
    echo "Install Tectonic (https://tectonic-typesetting.github.io) or a TeX distribution" >&2
    echo "that provides xelatex and bibtex, then rerun this script." >&2
    exit 4
fi

echo "Engine: XeLaTeX"

echo "First xelatex run..."
xelatex -interaction=nonstopmode -halt-on-error main.tex

echo "Running bibtex..."
if [ -f bibliography.bib ]; then
    bibtex main
fi

echo "Second xelatex run..."
xelatex -interaction=nonstopmode -halt-on-error main.tex

echo "Final xelatex run..."
xelatex -interaction=nonstopmode -halt-on-error main.tex

cp -f main.pdf paper.pdf
echo "Compilation complete. Output: paper.pdf"
