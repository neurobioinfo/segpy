# Segpy: A pipline for segregation analysis


[![](https://img.shields.io/badge/Documentation-segpy-blue)](https://neurobioinfo.github.io/segpy/site/) 

-------------

This repository includes module and pipeline for segregation analysis, which can be used to run the segregation on PC or HPC. 

## Contents
-  [Introduction](#introduction)
-  [Installation](#installation)
-  [How to run](#how-to-run)

---

## Introduction
Segregation analysis is a process to explore the genetic variant in a sample of seguence data. This pipeline counts the number of affecteds and nonaffecteds with variant, with homozygous variant, with no variant, and with no call. It gets those counts both in-family and globally. Also we also get the breakdown of not just variants, but also the breakdown of alleles in each. To achive the segregation, one needs a pedigree file with six columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex`{1:male; 2:female, 0:unknown}, and `phenotype`={1: control (unaffected), 2: proband(affected), -9:missing}. And the genetic data must be in the `vcf` format.

Please refer to the [documentation](https://neurobioinfo.github.io/segpy/site/) for an explanation and of how and why to use segpy's pipeline.

## Installation
`segpy` is a Python module specifically designed for segregation analysis, developed on Python 3.10.2, the module can be easily downloaded using `pip` package manager:  

```
pip install 'git+https://github.com/neurobioinfo/segpy#subdirectory=segpy'
```

Segregation analysis can be conducted utilizing the segpy scheduler, `segpy.pip`. If you have access to an HPC or Linux workstation, you can automate the process using `segpy.pip`. The scheduler script is written in Bash, making it compatible with systems such as Slurm or a Linux workstation.

```
wget https://github.com/neurobioinfo/segpy/releases/download/v0.2.2/segpy.pip.zip
unzip segpy.pip.zip 
```

To obtain a brief guidance of the pipeline, execute the following code.
```
bash ./segpy.pip/launch_segpy.sh -h
```

## How to run
Segregation analysis can be performed directly in Python using the [`segpy` module](https://neurobioinfo.github.io/segpy/site/tutorial/segpy_module), if you have access to HPC, you can automate it using [`segpy via slurm`](https://neurobioinfo.github.io/segpy/site/tutorial/segpy_slurm), 
or on a Linux workstation[`segpy via local`](https://neurobioinfo.github.io/segpy/site/tutorial/segpy_local). 

NOTE: vcf input files must have no more than one ALT allele per line. If your vcf file has multiallelic positions, they can be split using [bcftools](https://github.com/samtools/bcftools): `bcftools norm -m- [input.vcf]`

### Contributing
This is an early version, any contribute or suggestion is appreciated, you can directly contact with [Saeid Amiri](https://github.com/saeidamiri1) or [Dan Spiegelman](https://github.com/danspiegelman).


### Citation
Amiri, S., Spiegelman, D., & Farhan, S. (2024). segpy: A pipeline for segregation analysis (Version 0.2.0) [Computer software]. https://github.com/neurobioinfo/segpy

### Changelog
Every release is documented on the [GitHub Releases page](https://github.com/neurobioinfo/segpy/releases).

### License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/neurobioinfo/segpy/blob/main/LICENSE) file for details

## Acknowledgement
The pipeline is done as a project by Neuro Bioinformatics Core, it is developed by [Saeid Amiri](https://github.com/saeidamiri1) with associate of Dan Spiegelman and Sali Farhan. 


**[⬆ back to top](#contents)**
