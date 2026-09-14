#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "usage: $0 INPUT_MD [OUTPUT_PDF]" >&2
  exit 1
fi

input_md="$1"
if [[ ! -f "$input_md" ]]; then
  echo "input file not found: $input_md" >&2
  exit 1
fi

if [[ $# -eq 2 ]]; then
  output_pdf="$2"
else
  input_dir="$(dirname "$input_md")"
  input_base="$(basename "$input_md" .md)"
  output_pdf="$input_dir/pdf/$input_base.pdf"
fi

mkdir -p "$(dirname "$output_pdf")"

pandoc "$input_md" \
  -o "$output_pdf" \
  --pdf-engine=xelatex \
  -V papersize:a4 \
  -V fontsize:11pt \
  -V geometry:margin=20mm \
  -V mainfont='Times New Roman' \
  -V monofont='Menlo'
