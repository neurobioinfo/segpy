# Welcome to scrnabox's documentation!
segpy is a pipeline for segraegation analysis, this documrentation includes a tutorial for the segregation analysis using the segpy module in python or an HPC environment ([slurm work load manager system](https://slurm.schedmd.com/)).  Segregation analysis is a process to explore the genetic variant in a sample of seguence data. This pipeline counts the number of affecteds and nonaffecteds with variant, with homozygous variant, with no variant, and with no call. It gets those counts both in-family and globally. Also we also get the breakdown of not just variants, but also the breakdown of alleles in each. To achive the segregation, one needs a pedigree file with six columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex`{1:male; 2:female, 0:unknown}, and `phenotype`={1: control (unaffected), 2: proband(affected), -9:missing}. And the genetic data must be in the `vcf` format.


For an explanation and of how and why to use segpy's pipeline, look at tutorial. 

## Contents
- [Installation](installation.md)
- [Tutorial:]()
    - [segpy](segpy.md)
    - [segpy.slurm](segpy_slurm.md)
- [FAQ](FAQ.md)
- [Reference](reference.md)
