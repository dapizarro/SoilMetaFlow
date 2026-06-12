#!/usr/bin/env bash
set -euo pipefail
snakemake --snakefile workflow/Snakefile --configfile config/config.yaml --profile profiles/slurm
