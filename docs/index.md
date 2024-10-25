# Welcome to Segpy's documentation!
Segpy is a comprehensive pipeline to facilitate variant segregation analysis. Segregation analysis investigates how genetic variants are passed down through generations in a family in order to identify genetic traits that contribute to disease. In general, segregation analysis comprises a three-step process: <br>

1. **Family pedigree construction**: A detailed family tree is created to visualize relationships and inheritance patterns among family members.
2. **Genotyping**: Family members are genotyped to identify the presence or absence of specific variants.
3. **Data Analysis**: Statistical methods are applied to analyze how the variants segregate with the phenotype within the family. This often involves comparing the genotype of affected individuals to that of unaffected individuals.

While Segpy was originally designed for segregation analysis, it can also be used to analyze **case-control cohorts**. We provide comprehensive tutorials for each application case in the **Tutorial** section of this documentation. Regardless of the application case, Segpy computes the counts of affected and non-affected individuals, both in and out of families, based on reference allele, alternate allele, homozygous alternate allele, and no variant call. These counts are assembled into a comprehensive dataframe, where each row represents a single variant, which can be optionally annotated with [Variant Effect Predictor](https://useast.ensembl.org/info/docs/tools/vep/index.html) (VEP) to facilitate downstream statistical analyses.

The Segpy pipeline comprises four sequential steps shown in **Figure 1**. As input, users must provide a VCF file, which can be optionally annotated with VEP, and a pedigree file. The VCF file is then converted to the Hail MatrixTable format, the variants are segregated, and the counts data frame is parsed to only retain informative ouputs.

 <p align="center">
 <img src="https://github.com/user-attachments/assets/9beb08d2-49cd-41fc-a419-3caca8329c6d" width="450" height="100">
 </p>

**Figure 1. Segpy pipeline workflow.**

A containerized version of the Segpy pipeline is publicly available from **Zenodo**, which includes the code, libraries, and dependicies required for running the analyses. Segpy is configured to seamlessly integrate with High-Performance Computing (HPC) systems utilizing the [SLURM](https://slurm.schedmd.com/) workload manager (Segpy SLURM), but can also be run locally on linux workstations (Segpy Local).

In this documentation, we provide a step-by-step tutorial and explanation of the Segpy pipeline. We also provide a quick-start tutorial using a simulated dataset.

 - - - -

## Contents
- Tutorial:
    - [Installation](installation.md) 
    - [Segpy SLURM](segpy_slurm.md)
    - [Segpy Local](segpy_local.md)
    - [Configuration parameters](reference.md) 
    - [Output files](output.md) 
    - [FAQ](FAQ.md)           
- About:
    - [License](LICENSE.md)
    - [Changelog](changelog.md)
    - [Contributing](contributing.md)
    - [Acknowledgement](Acknowledgement.md)
