# Segpy outputs
As output, Segpy computes variant counts for affected and unaffected individuals, both within and outside of families, by categorizing wild-type individuals, heterozygous carriers, and homozygous carriers at specific loci. These counts are organized into a comprehensive data frame, with each row representing a single variant and labeled with the Sample IDs of the corresponding carriers. 

Step 3 of the Segpy pipeline produces two output files, depending on the parsing parameter used:

1. **finalseg_cleaned_general.csv**: produced using the `--parser general` tag to remove uncessary characters, such as `"`, `[, ]`, etc.
2. **finalseg_cleaned_unique.csv**: produced using the `--parser unique` tag to eliminate duplicated variant entries resulting from VEP annotations.

Regardless of the parsing parameters used, the output file includes separate columns for the user-selected VEP annotations and distinct columns detailing the variant counts across individuals in the study, categorized by their disease status and family status (if applicable). 

The final output files will vary depending on the selected analysis track:

- [Single-family](#single-family) 
- [Multi-family](#multi-family)
- [Case-control](#case-control)

- - - -
### Single-family
| Column title   |      Description      |  
|----------|:-------------|
|affected_WT| # of affected individuals that are homozygous for the wildtype allele |
|affected_nocall| # of affected individuals with no variant call |
|affected_heterozygous| # of affected individuals that are heterozygous for the variant |
|affected_homozygous| # of affected individuals that are homozygous for the variant |
|unaffected_WT| # of unaffected individuals that are homozygous for the wildtype allele |
|unaffected_nocall| # of unaffected individuals with no variant call |
|unaffected_heterozygous| # of unaffected individuals that are heterozygous for the variant |
|unaffected_homozygous| # of unaffected individuals that are homozygous for the variant |
|affected_WT_ID| Sample ID of affected individuals that are homozygous for the wildtype allele |
|affected_nocall_ID| Sample ID of affected individuals with no variant call |
|affected_heterozygous_ID| Sample ID of affected individuals that are heterozygous for the variant |
|affected_homozygous_ID| Sample ID of affected individuals that are homozygous for the variant |
|unaffected_WT_ID| Sample ID of unaffected individuals that are homozygous for the wildtype allele |
|unaffected_nocall_ID| Sample ID of unaffected individuals with no variant call |
|unaffected_heterozygous_ID| Sample ID of unaffected individuals that are heterozygous for the variant |
|unaffected_homozygous_ID| Sample ID of unaffected individuals that are homozygous for the variant |
|affected_AF| Allele frequency among affected individuals |
|unaffected_AF| Allele frequency among unaffected individuals |

- - - -
### Multi-family

**NOTE:** For the multi-family analysis, each family will have a separate row for each variant that is observed in any individual within that family.

| Column title   |      Description      |  
|----------|:-------------|
|family_affected_WT| # of affected individuals within the family that are homozygous for the wildtype allele |
|family_affected_nocall| # of affected individuals within the family with no variant call |
|family_affected_heterozygous|  # of affected individuals within the family that are heterozygous for the variant |
|family_affected_homozygous| # of affected individuals within the family that are homozygous for the variant |
|family_unaffected_WT| # of unaffected individuals within the family that are homozygous for the wildtype allele |
|family_unaffected_nocall| # of unaffected individuals within the family with no variant call |
|family_unaffected_heterozygous|  # of unaffected individuals within the family that are heterozygous for the variant |
|family_unaffected_homozygous| # of unaffected individuals within the family that are homozygous for the variant |
|total_affected_WT| # of affected individuals across all families that are homozygous for the wildtype allele | 
|total_affected_nocall| # of affected individuals across all families with no variant call |
|total_affected_heterozygous| # of affected individuals across all families that are heterozygous for the variant |
|total_affected_homozygous| # of affected individuals across all families that are homozygous for the variant |
|total_unaffected_WT| # of unaffected individuals across all families that are homozygous for the wildtype allele | 
|total_unaffected_nocall| # of unaffected individuals across all families with no variant call |
|total_unaffected_heterozygous| # of unaffected individuals across all families that are heterozygous for the variant |
|total_unaffected_homozygous| # of unaffected individuals across all families that are homozygous for the variant |
|family_affected_WT_ID| Sample ID of affected individuals within the family that are homozygous for the wildtype allele | 
|family_affected_nocall_ID| Sample ID of affected individuals within the family with no variant call |
|family_affected_heterozygous_ID| Sample ID of affected individuals within the family that are heterozygous for the variant |
|family_affected_homozygous_ID| Sample ID of affected individuals within the family that are homozygous for the variant |
|family_unaffected_WT_ID| Sample ID of unaffected individuals within the family that are homozygous for the wildtype allele | 
|family_unaffected_nocall_ID| Sample ID of unaffected individuals within the family with no variant call |
|family_unaffected_heterozygous_ID| Sample ID of unaffected individuals within the family that are heterozygous for the variant |
|family_unaffected_homozygous_ID| Sample ID of unaffected individuals within the family that are homozygous for the variant |
|affected_AF| Allele frequency among affected individuals |
|unaffected_AF| Allele frequency among unaffected individuals |

- - - -
### Case-control
| Column title   |      Description      |  
|----------|:-------------|
|case_WT| # of cases that are homozygous for the wildtype allele |
|case_nocall| # of cases with no variant call |
|case_heterozygous| # of cases that are heterozygous for the variant |
|case_homozygous| # of cases that are homozygous for the variant |
|control_WT| # of controls that are homozygous for the wildtype allele |
|control_nocall| # of controls with no variant call |
|control_heterozygous| # of controls that are heterozygous for the variant |
|control_homozygous| # of controls that are homozygous for the variant |
|case_WT_ID| Sample ID of cases that are homozygous for the wildtype allele |
|case_nocall_ID| Sample ID of cases with no variant call |
|case_heterozygous_ID| Sample ID of cases that are heterozygous for the variant |
|case_homozygous_ID| Sample ID of cases that are homozygous for the variant |
|control_WT_ID| Sample ID of controls that are homozygous for the wildtype allele |
|control_nocall_ID| Sample ID of controls with no variant call |
|control_heterozygous_ID| Sample ID of controls that are heterozygous for the variant |
|control_homozygous_ID| Sample ID of controls that are homozygous for the variant |
|case_AF| Allele frequency among cases |
|control_AF| Allele frequency among controls |
