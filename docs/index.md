# Welcome to Segpy's documentation!

## Introduction
Segpy is a streamlined, user-friendly pipeline designed for variant segregation analysis, allowing investigators to compute allelic counts at variant sites across study subjects. The  pipeline can be applied to both pedigree-based family cohorts — those involving single or multi-family trios, quartets, or extended families — and population-based case-control cohorts. Considering the scale of modern datasets and the computational power required for their analysis, the Segpy pipeline was designed for seamless integration with the user's high-performance computing (HPC) clusters using the [SLURM](https://slurm.schedmd.com/) Workload Manager (Segpy SLURM); however, users may also run the pipleine directly from their Linux workstation or any PC with Bash and Singularity installed (Segpy Local). 

As input, users must provide a single VCF file describing the genetic variants of all study subjects and a pedigree file describing the familial relationships among those individuals (if applicable) and their disease status. As output, Segpy computes variant carrier counts for affected and unaffected individuals, both within and outside of families, by categorizing wild-type individuals, heterozygous carriers, and homozygous carriers at specific loci. These counts are organized into a comprehensive data frame, with each row representing a single variant and labeled with the Sample IDs of the corresponding carriers to facilitate donwstream analysis. 

To meet the requirements of various study designs, Segpy integrates the ability to analyze pedigree-based and population-based datasets by providing three distinct, yet highly comparable analysis tracks: <br>

1) Single-family <br>
2) Multi-family <br>
3) Case-control <br>

We provide comprehensive tutorials for running these analysis tracks in subsequent sections of this documentation. 

Each analysis tracks consists of four dstinct steps shown in **Figure 1**. In brief, Step 0 establishes a working directory for the analyis and deposits a modifiable text file to adjust the analytical parameters. In Step 1, the user-provided VCF file is converted to the [Hail MatrixTable](https://hail.is/docs/0.2/overview/matrix_table.html) format. In Step 2, variant segregation is performed based on the sample information defined in the user-provided pedigree file using the MatrixTable. In Step 3, the carrier counts data frame produced in Step 2 is parsed based on user specifications to reduce the computational burden of downstream analyses. 

 <p align="center">
 <img src="https://github.com/user-attachments/assets/d7879700-3bba-4d53-a775-8556e3c3f6d3" width="300" height="100">
 </p>

**Figure 1. Segpy pipeline workflow.**

A containerized version of the Segpy pipeline is publicly available from [Zenodo](https://zenodo.org/records/14503733), which includes the code, libraries, and dependicies required for running the analyses. 

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
