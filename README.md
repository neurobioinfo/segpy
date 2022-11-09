# Segregation: A repository for segregation analysis

This repository includes module and pipeline for segregation analysis. 

## Contents

- [Workflow](#workflow)
- [Segregation Analysis](#segregation-Analysis)
- [scrnabox.svn](#scrnaboxsvn)
- [References](#references)

## Workflow


---

## Segregation Analysis
Segregation is a process to explore the genetic variant in a sample of seguence data. This pipeline counts the number of affecteds and nonaffecteds with variant, with homozygous variant, with no variant, and with no call. It gets those counts both in-family and globally. Also we also get the breakdown of not just variants, but also the breakdown of alleles in each. To achive the segregation, one needs a pedigree file with six columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex`{1:male; 2:female, 0:unknown}, and `phenotype`={1: control (unaffected), 2: proband(affected), -9:missing}. And the genetic data must be in the `vcf` format.

## seganalyis
`seganalyis` is a python module developed to run segregation, 

## segrun.svn
`segrun.svn` is a pipeline (shield) developed to run step 1 to step 3 under HPC system, the pipeline has been using under [Beluga](https://docs.alliancecan.ca/wiki/B%C3%A9luga), the detail of how to use it is discussed in [segrun.svn](https://github.com/neurobioinfo/scrnabox/tree/main/scrnabox.svn)
![hashtag](https://raw.githubusercontent.com/neurobioinfo/segregation/main/segregation.png)

## References

## Contributing
This is an early version, any contribute or suggestion is appreciated, you can directly contact with [Saeid Amiri](https://github.com/saeidamiri1) or [Dan Spiegelman](https://github.com/danspiegelman).

## Citation

## Changelog

Every release is documented on the [GitHub Releases page](https://github.com/neurobioinfo/segregation/releases).

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/neurobioinfo/segregation/blob/main/LICENSE) file for details

## Acknowledgement

The pipeline is done as a project by Neuro Bioinformatics Core, it is written by [Saeid Amiri](https://github.com/saeidamiri1) with associate of Dan Spiegelman

## Todo

- Add nba to pipeline
  **[⬆ back to top](#contents)**
