#!/bin/sh
# Run the entry program the way the grader does: copy POST.json into out/.
set -e
mkdir -p out
MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
