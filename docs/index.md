# Welcome to segpy's documentation!
Segpy is a comprehensive pipeline designed for segregation analysis. This documentation provides a step-by-step tutorial on executing segregation analysis in a High-Performance Computing (HPC) environment utilizing the Slurm workload manager system (https://slurm.schedmd.com/), or on a Linux workstation. Segregation analysis is a crucial process for exploring genetic variants within a sample of sequence data. This pipeline facilitates the counting of affected and non-affected individuals with variants, including homozygous variants, those with no variants, and those with no calls. These counts are computed both within families and globally. Additionally, the pipeline offers a detailed breakdown not only of variants but also of alleles in each case. To execute segregation analysis successfully, it is imperative to have a pedigree file with six columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex`{1:male; 2:female, 0:unknown}, and `phenotype`={1: control (unaffected), 2: proband(affected), -9:missing}. The genetic data must be provided in the vcf format.

For guidance on how to use segpy's pipeline, consult the tutorial.

## Contents
- [Installation](installation.md)
- [Tutorial:]()
    - [segpy local](segpy_local.md)
    - [segpy slurm](segpy_slurm.md)
- [FAQ](FAQ.md)
- [Reference](reference.md)
