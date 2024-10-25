# Segpy outputs
The Segpy pipeline computes the counts of affected and non-affected individuals, both in and out of families, based on reference allele, alternate allele, homozygous alternate allele, and no variant call. These counts are assembled into a comprehensive dataframe, where each row represents a single variant, which can be optionally annotated with Variant Effect Predictor (VEP) to facilitate downstream statistical analyses.

Step 3 of the Segpy pipeline produces two output files, depending on the parsing parameter used:

1. **finalseg_cleaned_general.csv**: produced using the `--parser general` tag to remove uncessary characters, such as `"`, `[, ]`, etc.
2. **finalseg_cleaned_unique.csv**: produced using the `--parser unique` tag to eliminate duplicated variant entries resulting from VEP annotations.

Regardless of the parsing parameters used, the output file includes separate columns for the user-selected VEP annotations and distinct columns detailing the variant counts across individuals in the study, categorized by their disease and family status:


| Column title   |      Description      |  
|----------|:-------------|
|**Family - Affected** | | 
|fam_aff_wild | Family - Affecteds: wildtype | 
|fam_aff_ncl | Family - Affecteds: no call | 
|fam_aff_vrt | Family - Affecteds: with variant | 
|fam_aff_homv | Family - Affecteds: homozygous for ALT allele | 
|**Family - Non-affected** | | 
|fam_naf_wild | Family - non-affecteds: wildtype | 
|fam_naf_ncl | Family - non-affecteds: no call | 
|fam_naf_vrt | Family - non-affecteds: with variant | 
|fam_naf_homv | Family - non-affecteds: homozygous for ALT allele | 
|**Non-Family - Affected** | | 
|nfm_aff_wild | Non-family - Affecteds: wildtype | 
|nfm_aff_ncl | Non-family - Affecteds: no call | 
|nfm_aff_vrt | Non-family - Affecteds: with variant | 
|nfm_aff_homv | Non-family - Affecteds: homozygous for ALT allele | 
|**Non-Family - Non-affected** | | 
|nfm_naf_wild | Non-family - non-affecteds: wildtype | 
|nfm_naf_ncl | Non-family - non-affecteds: no call | 
|nfm_naf_vrt | Non-family - non-affecteds: with variant | 
|nfm_naf_homv | Non-family - non-affecteds: homozygous for ALT allele | 


