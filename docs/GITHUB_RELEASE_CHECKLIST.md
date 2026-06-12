# GitHub release checklist

- [ ] Replace example sample metadata with real project metadata.
- [ ] Confirm all FASTQ paths in `metadata/units.tsv` exist.
- [ ] Edit database paths in `config/config.yaml`.
- [ ] Run `snakemake --lint`.
- [ ] Run a dry run: `snakemake -n`.
- [ ] Test one small sample locally.
- [ ] Confirm `.gitignore` excludes raw data, results and databases.
- [ ] Add a repository description and topics: metagenomics, soil, snakemake, microbiome, MAGs.
- [ ] Add a workflow diagram to the README if desired.
- [ ] Create first release: `v0.1.0`.
