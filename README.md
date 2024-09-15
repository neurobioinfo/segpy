# Segpy: A pipline for segregation analysis


[![](https://img.shields.io/badge/Documentation-segpy-blue)](https://neurobioinfo.github.io/segpy/site/) 

-------------

This repository includes the pipeline for segregation analysis, which can be used to run the segregation on PC or HPC. 

## Contents
-  [Introduction](#introduction)
-  [Installation](#installation)
-  [How to run](#how-to-run)

---

## Introduction
Segregation analysis is a process to explore the genetic variant in a sample of seguence data. This pipeline counts the number of affecteds and nonaffecteds with variant, with homozygous variant, with no variant, and with no call. It gets those counts both in-family and globally. Also we also get the breakdown of not just variants, but also the breakdown of alleles in each. To achive the segregation, one needs a pedigree file with six columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex`{1:male; 2:female, 0:unknown}, and `phenotype`={1: control (unaffected), 2: proband(affected), -9:missing}. And the genetic data must be in the `vcf` format.

Please refer to the [documentation](https://neurobioinfo.github.io/segpy/site/) for an explanation and of how and why to use segpy's pipeline.

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
