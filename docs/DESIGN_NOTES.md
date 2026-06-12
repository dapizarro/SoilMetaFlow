# Design notes

The pipeline is intentionally modular. Soil metagenomes can be analysed at different depths depending on project goals and available computing resources.

## Minimal mode

QC + trimming + Kraken2/Bracken. Useful for fast screening and checking whether samples cluster by site, treatment or soil horizon.

## Standard mode

QC + taxonomy + assembly + gene prediction + eggNOG annotation. Useful for most ecological studies where functional potential is required.

## Genome-resolved mode

Standard mode + mapping + binning + MAG quality control + optional GTDB-Tk. Useful when dominant populations or novel lineages are biologically important.

## Notes for soil datasets

- Soil has high complexity; assemblies may be fragmented.
- Co-assembly can improve recovery of low-abundance genomes but may create chimeric bins if samples are too heterogeneous.
- Binning is more reliable when coverage varies across samples. This template currently performs per-sample binning; project-level co-binning can be added.
- Taxonomic profiles depend strongly on database completeness.
- Functional annotations should be interpreted as potential, not activity.
