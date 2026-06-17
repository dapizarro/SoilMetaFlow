# SoilMetagenomeFlow

**Reproducible, scalable shotgun metagenomics pipeline for samples starting from raw paired-end FASTQ files.**

This repository is designed as a GitHub-ready template for metagenomics projects. It uses **Snakemake + Conda** and can run locally or on SLURM clusters. The workflow is modular, so it can be used for pilot datasets, full projects, or new metagenome collections with minimal changes.

---

## 1. Scientific rationale

Several components of this workflow derive from methodologies developed during research on symbiotic systems  and environmental metagenomics, including genome assembly, metagenomic binning, MAG reconstruction and functional annotation across diverse microbial and eukaryotic communities.

- Read-based taxonomy is fast and useful for sample comparison.
- Assembly-based gene prediction improves functional interpretation.
- Binning and MAG quality control allow genome-resolved ecological analysis.

---

## 2. Workflow overview

```text
Raw FASTQ
   │
   ├── FastQC / fastp / MultiQC
   │       └── read quality, trimming, adapter removal, QC report
   │
   ├── Kraken2 + Bracken
   │       └── taxonomic profiles from reads
   │
   ├── MEGAHIT assembly
   │       └── contigs per sample
   │
   ├── Prodigal meta mode
   │       └── gene and protein prediction
   │
   ├── eggNOG-mapper
   │       └── orthology, COGs, KEGG-like functions, GO terms
   │
   ├── Bowtie2 + samtools
   │       └── read mapping against contigs for coverage
   │
   ├── MetaBAT2
   │       └── genome binning
   │
   └── CheckM2 / optional GTDB-Tk
           └── MAG quality and taxonomy
```

---

## 3. Repository structure

```text
soil_metagenomics_pipeline/
├── README.md
├── LICENSE
├── environment.yaml
├── run_local.sh
├── run_slurm.sh
├── config/
│   └── config.yaml
├── metadata/
│   ├── samples.tsv
│   └── units.tsv
├── workflow/
│   ├── Snakefile
│   └── envs/
├── scripts/
│   └── summarize_fastp.py
├── profiles/
│   └── slurm/config.yaml
├── resources/
│   ├── db/
│   └── host/
├── docs/
├── tests/
└── results/
```

---

## 4. Input files

### `metadata/units.tsv`

This is the most important file. Each row corresponds to one sequencing unit or lane.

```tsv
sample_id	unit	fq1	fq2
SOIL01	L001	data/raw/SOIL01_L001_R1.fastq.gz	data/raw/SOIL01_L001_R2.fastq.gz
SOIL01	L002	data/raw/SOIL01_L002_R1.fastq.gz	data/raw/SOIL01_L002_R2.fastq.gz
SOIL02	L001	data/raw/SOIL02_L001_R1.fastq.gz	data/raw/SOIL02_L001_R2.fastq.gz
```

The pipeline automatically merges multiple units belonging to the same biological sample after trimming.

### `metadata/samples.tsv`

This table stores ecological or experimental metadata.

```tsv
sample_id	site	treatment	replicate	soil_layer	notes
SOIL01	SiteA	control	1	0-10cm	forest soil
SOIL02	SiteA	amended	1	0-10cm	compost amended soil
```

Keep this file clean because it will later be used for ecological statistics in R or Python.

---

## 5. Installation

Install Mambaforge or Miniforge, then create the base Snakemake environment:

```bash
mamba env create -f environment.yaml
mamba activate soil-metagenomics-pipeline
```

Snakemake will create the rule-specific environments automatically when executed with `--use-conda`.

---

## 6. Configuration

Edit `config/config.yaml` before running real data.

Key fields:

```yaml
samples: metadata/samples.tsv
units: metadata/units.tsv
outdir: results

databases:
  kraken2: resources/db/kraken2_standard
  bracken: resources/db/bracken
  eggnog: resources/db/eggnog
  gtdbtk: resources/db/gtdbtk
  checkm2: resources/db/checkm2/CheckM2_database/uniref100.KO.1.dmnd
```

Large databases should **not** be committed to GitHub. Keep them under `resources/db/` locally or document their paths in the config file.

---

## 7. Running locally

Dry run:

```bash
snakemake --snakefile workflow/Snakefile --configfile config/config.yaml --use-conda -n
```

Run:

```bash
bash run_local.sh
```

---

## 8. Running on SLURM

Edit `profiles/slurm/config.yaml` for your cluster partition, memory and runtime limits.

Then run:

```bash
bash run_slurm.sh
```

---

## 9. Main outputs

```text
results/
├── qc/
│   ├── fastqc/raw/
│   ├── fastp/
│   └── multiqc/multiqc_report.html
├── clean/
│   └── *.clean.fastq.gz
├── taxonomy/
│   ├── kraken2/*.report
│   └── bracken/*.bracken
├── assembly/
│   └── SAMPLE/final.contigs.fa
├── genes/
│   └── SAMPLE/proteins.faa, genes.fna, genes.gff
├── functional/
│   └── eggnog/*.annotations
├── mapping/
│   └── *.sorted.bam
├── binning/
│   └── metabat2/SAMPLE/bin*.fa
├── mags/
│   └── checkm2/SAMPLE/quality_report.tsv
└── summary/
    └── sample_qc_summary.tsv
```

---

## 10. Recommended downstream ecological analyses

Once the pipeline has generated taxonomic and functional tables, typical downstream analyses include:

- Alpha diversity: richness, Shannon diversity, evenness.
- Beta diversity: Bray-Curtis, Jaccard, Aitchison after compositional transformation.
- Ordination: PCoA, NMDS, PCA or dbRDA.
- Differential abundance: ANCOM-BC, ALDEx2, MaAsLin2 or DESeq2 with caution.
- Environmental modelling: PERMANOVA, mixed models, random forest, gradient analysis.
- MAG ecology: MAG abundance versus soil chemistry, vegetation, treatment or geography.
- Functional guilds: carbohydrate metabolism, nitrogen cycling, sulfur cycling, stress response, antibiotic resistance, biosynthetic gene clusters.

For soil metagenomics, avoid interpreting raw relative abundances as absolute biomass. Whenever possible, combine shotgun data with metabarcoding, soil chemistry, DNA yield, qPCR or spike-in controls.

---


## 11. Citation suggestion

If you use this pipeline in a poster, talk or manuscript, cite it as: https://doi.org/10.5281/zenodo.20700718

---

## 12. Roadmap

Planned optional modules:

- HUMAnN-based pathway profiling.
- AMR detection with AMRFinderPlus, RGI or DeepARG.
- Biosynthetic gene cluster detection with antiSMASH or GECCO.
- Co-assembly mode by site or treatment.
- RMarkdown report for ecological statistics.
- Example toy dataset for continuous integration.
