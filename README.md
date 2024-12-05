# Segpy: A pipline for segregation analysis


[![](https://img.shields.io/badge/Documentation-segpy-blue)](https://neurobioinfo.github.io/segpy/site/) 

-------------
## Contents
-  [Introduction](#introduction)
-  [Installation](#installation)
-  [How to run](#how-to-run)

---

## Introduction
Segpy is a streamlined, user-friendly pipeline designed for variant segregation analysis, allowing investigators to compute allelic carrier counts at variant sites across study subjects. The  pipeline can be applied to both pedigree-based family cohorts — those involving single or multi-family trios, quartets, or extended families — and population-based case-control cohorts. As input, users must provide a single VCF file describing the genetic variants of all study subjects and a pedigree file describing the familial relationships among those individuals (if applicable) and their disease status. As output, Segpy computes variant carrier counts for affected and unaffected individuals, both within and outside of families, by categorizing wild-type individuals, heterozygous carriers, and homozygous carriers at specific loci. These counts are organized into a comprehensive data frame, with each row representing a single variant and labeled with the Sample IDs of the corresponding carriers to facilitate donwstream analysis. Considering the scale of modern datasets and the computational power required for their analysis, the Segpy pipeline was designed for seamless integration with the users’ high-performance computing clusters using the [SLURM](https://slurm.schedmd.com/) Workload Manager (Segpy SLURM); however, users may also run the pipleine directly from their local linux workstation (Segpy Local). 

To meet the requirements of various study designs, Segpy integrates the ability to analyze pedigree-based and population-based datasets by providing three distinct, yet highly comparable analysis tracks: <br>

1) Single-family <br>
2) Multi-family <br>
3) Case-control <br>

Each analysis tracks consists of four dstinct steps shown in **Figure 1**. In brief, Step 0 establishes a working directory for the analyis and deposits a modifiable text file to adjust the analytical parameters. In Step 1, the user-provided VCF file is converted to the [Hail MatrixTable](https://hail.is/docs/0.2/overview/matrix_table.html) format. In Step 2, variant segregation is performed based on the sample information defined in the user-provided pedigree file using the MatrixTable. In Step 3, the carrier counts data frame produced in Step 2 is parsed based on user specifications to reduce the computational burden of downstream analyses. 

 <p align="center">
 <img src="https://github.com/user-attachments/assets/d7879700-3bba-4d53-a775-8556e3c3f6d3" width="300" height="450">
 </p>

**Figure 1. Segpy pipeline workflow.**

A containerized version of the Segpy pipeline is publicly available from <span style="background-color: yellow;">Zenodo</span>, which includes the code, libraries, and dependicies required for running the analyses.

Please refer to Segpy's [documentation](https://neurobioinfo.github.io/segpy/site/) for comprehensive tutorials. 

## Installation
The pipeline is containerized and can be run using Apptainer\Singularity, eliminating the need to install modules within the pipeline. It is compatible with both High-Performance Computing (HPC) systems and standard Linux workstations, look at  [`segpy` installation](https://neurobioinfo.github.io/segpy/latest/installation/) for details. 


## How to run
If you have access to HPC, you can automate it using [`segpy via slurm`](https://neurobioinfo.github.io/segpy/latest/segpy_slurm/), 
or on a Linux workstation[`segpy via local`](https://neurobioinfo.github.io/segpy/latest/segpy_local/). 

NOTE: vcf input files must have no more than one ALT allele per line. If your vcf file has multiallelic positions, they can be split using [bcftools](https://github.com/samtools/bcftools): `bcftools norm -m- [input.vcf]`

### Contributing
This is an early version, any contribute or suggestion is appreciated, you can directly contact with [Saeid Amiri](https://github.com/saeidamiri1) or [Dan Spiegelman](https://github.com/danspiegelman).

### Citation
Amiri, S., Spiegelman, D., & Farhan, S. (2024). segpy: A pipeline for segregation analysis (Version 0.3.0) [Computer software]. https://github.com/neurobioinfo/segpy

### Changelog
Every release is documented on the [GitHub Releases page](https://github.com/neurobioinfo/segpy/releases).

### License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/neurobioinfo/segpy/blob/main/LICENSE) file for details

## Acknowledgement
The pipeline is done as a project by Neuro Bioinformatics Core, it is developed by [Saeid Amiri](https://github.com/saeidamiri1) with associate of Sali Farhan. 


**[⬆ back to top](#contents)**
