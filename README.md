# Segpy: A pipline for segregation analysis
This repository includes module and pipeline for segregation analysis, which can be used to run the segregation on PC or HPC. 

## Contents
-  [Segregation Analysis](#segregation-Analysis)
-  [How to run](#how-to-run)
-  [Installation](#installation)


## Segregation Analysis
Segregation analysis is a process to explore the genetic variant in a sample of seguence data. This pipeline counts the number of affecteds and nonaffecteds with variant, with homozygous variant, with no variant, and with no call. It gets those counts both in-family and globally. Also we also get the breakdown of not just variants, but also the breakdown of alleles in each. To achive the segregation, one needs a pedigree file with six columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex`{1:male; 2:female, 0:unknown}, and `phenotype`={1: control (unaffected), 2: proband(affected), -9:missing}. And the genetic data must be in the `vcf` format.

Please refer to the [documentation](https://neurobioinfo.github.io/segpy/site/) for an explanation and of how and why to use segpy's pipeline.

## How to run
The segregation can do done using the [`segpy` module](https://neurobioinfo.github.io/segpy/site/tutorial/segoy), if you have access to HPC, you can automate it using [`segpy.slurm`](https://neurobioinfo.github.io/segpy/site/tutorial/segpy_slurm). 

## Installation
`segpy` is a python module developed on Python 3.10.2 to run the segregation analysis, the module can be easily downloaded using `pip`:  
```
pip install 'git+https://github.com/neurobioinfo/segpy#subdirectory=segpy'
```

The segregation can do done using the segpy module, if you have access to HPC, you can automate it using segpy.slurm
The `segpy.slurm` is written in the bash, so it can be used with any slurm system. To download  `segpy.slurm`, run the below comments 
```
wget https://github.com/neurobioinfo/segpy/releases/download/v0.2.1/segpy.slurm.zip
unzip segpy.slurm.zip 
```

To obtain a brief guidance of the pipeline, execute the following code.
```
bash ./segpy.slurm/launch_segpy.sh -h
```


### Contributing
This is an early version, any contribute or suggestion is appreciated, you can directly contact with [Saeid Amiri](https://github.com/saeidamiri1) or [Dan Spiegelman](https://github.com/danspiegelman).

### Citation
Amiri, S., Spiegelman, D., & Farhan, S. (2023). segpy: A pipeline for segregation analysis (Version 0.2.0) [Computer software]. https://github.com/neurobioinfo/segpy

### Changelog
Every release is documented on the [GitHub Releases page](https://github.com/neurobioinfo/segpy/releases).

### License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/neurobioinfo/segpy/blob/main/LICENSE) file for details

## Acknowledgement
The pipeline is done as a project by Neuro Bioinformatics Core, it is developed by [Saeid Amiri](https://github.com/saeidamiri1) with associate of Dan Spiegelman and Sali Farhan. 


**[⬆ back to top](#contents)**
