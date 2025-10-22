# Segpy: a streamlined, user-friendly pipline for variant segregation analysis


[![](https://img.shields.io/badge/container-red)](https://zenodo.org/records/14503733/files/segpy.pip.zip?download=1) [![](https://img.shields.io/badge/Documentation-segpy-blue)](https://neurobioinfo.github.io/segpy/site/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14503733.svg)](https://doi.org/10.5281/zenodo.14503733)


-------------
## Contents
-  [Introduction](#introduction)
-  [Installation](#installation)
-  [Running Segpy](#running-segpy)
-  [Contributing](#contributing)
-  [Running Segpy](#running-segpy)
-  [Changelog](#changelog)
-  [License](#license)
-  [Acknowledgement](#acknowledgement)

---

## Introduction
Segpy is a streamlined, user-friendly pipeline designed for variant segregation analysis, allowing investigators to compute allelic carrier counts at variant sites across study subjects. The  pipeline can be applied to both pedigree-based family cohorts — those involving single or multi-family trios, quartets, or extended families — and population-based case-control cohorts. Considering the scale of modern datasets and the computational power required for their analysis, the Segpy pipeline was designed for seamless integration with the users’ high-performance computing (HPC) clusters using the [SLURM](https://slurm.schedmd.com/) Workload Manager (Segpy SLURM); however, users may also run the pipleine directly from their Linux workstation or any PC with Bash and Singularity installed (Segpy Local).

As input, users must provide a single VCF file describing the genetic variants of all study subjects and a pedigree file describing the familial relationships among those individuals (if applicable) and their disease status. As output, Segpy computes variant carrier counts for affected and unaffected individuals, both within and outside of families, by categorizing wild-type individuals, heterozygous carriers, and homozygous carriers at specific loci. These counts are organized into a comprehensive data frame, with each row representing a single variant and labeled with the Sample IDs of the corresponding carriers to facilitate donwstream analysis. 

To meet the requirements of various study designs, Segpy integrates the ability to analyze pedigree-based and population-based datasets by providing three distinct, yet highly comparable analysis tracks: <br>

1) Single-family <br>
2) Multi-family <br>
3) Case-control <br>

Each analysis tracks consists of four dstinct steps shown in **Figure 1**. In brief, Step 0 establishes a working directory for the analyis and deposits a modifiable text file to adjust the analytical parameters. In Step 1, the user-provided VCF file is converted to the [Hail MatrixTable](https://hail.is/docs/0.2/overview/matrix_table.html) format. In Step 2, variant segregation is performed based on the sample information defined in the user-provided pedigree file using the MatrixTable. In Step 3, the carrier counts data frame produced in Step 2 is parsed based on user specifications to reduce the computational burden of downstream analyses. 

 <p align="center">
 <img src="https://github.com/user-attachments/assets/d7879700-3bba-4d53-a775-8556e3c3f6d3" width="300" height="400">
 </p>

**Figure 1. Segpy pipeline workflow.**

A containerized version of the Segpy pipeline is publicly available from [Zenodo](https://zenodo.org/records/14503733), which includes the code, libraries, and dependicies required for running the analyses.

Below, we provide a quick start guide for Segpy. Please refer to Segpy's [documentation](https://neurobioinfo.github.io/segpy/site/) for comprehensive tutorials. 

---

## Installation

The following code can be used to download `segpy.pip`, which includes the code, libraries, and dependicies required for running the analyses:

```
# Download the Segpy container
curl "https://zenodo.org/records/14503733/files/segpy.pip.zip?download=1" --output segpy.pip.zip

# Unzip the Segpy container
unzip segpy.pip.zip
```

In addition to `segpy.pip`, users must install Apptainer/Singularity onto their HPC or local system. If you are using an HPC system, Apptainer is likely already installed, and you will simply need to load the module using the following code:

```
# Load Apptainer
module apptainer/1.2.4
```

To ensure that `segpy.pip` is downloaded properly, run the following command:

```
bash /path/to/segpy.pip/launch_segpy.sh -h
```

Which should return the folllowing:

```
------------------------------------ 
segregation pipeline version 0.0.6 is loaded

------------------- 
Usage:  segpy.pip/launch_segpy.sh [arguments]
        mandatory arguments:
                -d  (--dir)      = Working directory (where all the outputs will be printed) (give full path) 
                -s  (--steps)      = Specify what steps, e.g., 2 to run just step 2, 1-3 (run steps 1 through 3). 'ALL' to run all steps.
                                steps:
                                0: initial setup
                                1: create hail matrix
                                2: run segregation
                                3: final cleanup and formatting

        optional arguments:
                -h  (--help)      = Get the program options and exit.
                --jobmode  = The default for the pipeline is local. If you want to run the pipeline on slurm system, use slurm as the argument. 
                --analysis_mode  = The default for the pipeline is analysing single or multiple family. If you want to run the pipeline on case-control, use case-control as  the argumnet. 
                --parser             = 'general': to general parsing, 'unique': drop multiplicities 
                -v  (--vcf)      = VCF file (mandatory for steps 1-3)
                -p  (--ped)      = PED file (mandatory for steps 1-3)
                -c  (--config)      = config file [CURRENT: "/scratch/fiorini9/segpy.pip/configs/segpy.config.ini"]
                -V  (--verbose)      = verbose output 

 ------------------- 
 For a comprehensive help, visit  https://neurobioinfo.github.io/segpy/latest/ for documentation. 
```

After successfully downloading `segpy.pip` we can proceed with the segregation analysis. 

---

## Running Segpy 
Prior to initiating the pipeline, users must provide the paths to:

1. The directory containing `segpy.pip` (PIPELINE_HOME)
2. The directory designated for the pipeline's outputs (PWD)
3. The VCF file (VCF)
4. The pedigree file (PED)

Use the following code to define these paths:

```
# Define necessary paths
export PIPELINE_HOME=path/to/segpy.pip
PWD=path/to/outfolder
VCF=path/to/VCF.vcf
PED=path/to/pedigree.ped
```

To initiate the Segpy pipeline for your local workstation, use the following code:

```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 0 \
--analysis_mode single_family
```

Where `analysis_mode` is one of `single_family`, `multiple_family`, or `case-control` depending on the study design. 

To initiate the Segpy pipeline for your HPC cluster, include the `--job_mode` tag as shown in the following code:

```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 0 \
--jobmode slurm
--analysis_mode single_family
```

Upon initiating Segpy, the entire pipeline can be run using the following code:

```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 1-3 \
--vcf $VCF \
--ped $PED \
--parser general
```

Where `parser` is one of `general` or `unique`, depending on the user's preferred method for filtering the final output dataframe.

---

### Contributing
Any contributions or suggestions for the Segpy pipeline are welcomed. For direct contact, please reach out to The Neuro Bioinformatics Core at [neurobioinfo@mcgill.ca](mailto:neurobioinfo@mcgill.ca).

If you encounter any [issue](https://github.com/neurobioinfo/segpy/issues), please report them on the GitHub repository.

---

### Changelog
Every release is documented on the [GitHub Releases page](https://github.com/neurobioinfo/segpy/releases).

---

### License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/neurobioinfo/segpy/blob/main/LICENSE) file for details

---

### Acknowledgement
The pipeline is done as part of MNI projects, it is written by [Saeid Amiri](https://github.com/saeidamiri1) in association with [Dan Spiegelman](https://github.com/danspiegelman), [Michael Fiorini](https://github.com/mfiorini9), Allison Dilliott, and Sali Farhan at Neuro Bioinformatics Core. Copyright belongs [MNI BIOINFO CORE](https://github.com/neurobioinfo). 


**[⬆ back to top](#contents)**
