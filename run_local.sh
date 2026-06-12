#!/usr/bin/env bash
set -euo pipefail
snakemake --snakefile workflow/Snakefile --configfile config/config.yaml --use-conda --cores 16 --printshellcmds --rerun-incomplete
