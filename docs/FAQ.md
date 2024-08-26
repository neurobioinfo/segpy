## Frequently asked questions

- [finalseg.csv](#what-is-finalseg.csv)

# finalseg.csv
The output of `finalseg.csv` is the unpruned result from step 2.

# finalseg_cleaned_general.csv
The output of `finalseg_cleaned_general.csv` is the pruned result store under step 3. The file can be categorized to  1) locus and alleles, 2) CSQ, 3) Family, 4) Family-Affected, 5) Family, 6) Family-Affected. If you do not want to have CSQ in the output file, choose `CSQ=False`. 

##### locus and alleles
locus: chromosome <br/>
alleles:  a variant form of a gene
##### CSQ
VEP put all the requested information in infront CSQ.  
##### Family - Affected
fam_aff_wild: Family - Affecteds: wildtype <br/>
fam_aff_ncl: Family - Affecteds: no call<br/>
fam_aff_vrt: Family - Affecteds: with variant<br/>
famid_aff_homv: Family - Affecteds: homozygous for ALT allele<br/>
##### Family - Nonaffected   
fam_naf_wild: Family - Affecteds: wildtype <br/>
fam_naf_ncl: Family - Affecteds: no call<br/>
fam_naf_vrt: Family - Affecteds: with variant<br/>
fam_naf_homv: Family - Affecteds: homozygous for ALT allele<br/>
##### NonFamily - Affected
nfm_aff_wild: Family - Affecteds: wildtype <br/>
nfm_aff_ncl: Family - Affecteds: no call<br/>
nfm_aff_vrt: Family - Affecteds: with variant<br/>
nfm_aff_homv: Family - Affecteds: homozygous for ALT allele<br/>
##### NonFamily - Nonaffected   
nfm_naf_wild: Family - Affecteds: wildtype <br/>
nfm_naf_ncl: Family - Affecteds: no call<br/>
nfm_naf_vrt: Family - Affecteds: with variant<br/>
nfm_naf_homv: Family - Affecteds: homozygous for ALT allele<br/>
