## Frequently asked questions

- [What is finalseg.csv](#what-is-finalseg.csv)

# What is finalseg.csv
The output  of `finalseg.csv` can be categorized to  1) locus and alleles, 2) CSQ, 3) Global- Non-Affected 4) Global-Affected,  5) Family, 6) Family-Affected 7) Family - Non-affected.  If you do not want to have CSQ in the output file, choose `CSQ=False`. 
##### locus and alleles
locus: chromosome <br/>
alleles:  a variant form of a gene
##### CSQ
VEP put all the requested information in infront CSQ.  
##### Global - Non-Affected- is dropt
glb_naf_wild:  Global - Non-Affecteds, wildtype<br/>
glb_naf_ncl:     Global - Non-Affecteds, no call  <br/>   
glb_naf_vrt:     Global - Non-Affecteds, with variant    <br/>
glb_naf_homv:    Global - Non-Affecteds, homozygous for ALT allele<br/>
glb_naf_altaf:   Global - Non-Affecteds, ALT allele frequency   <br/>
##### Global - Affected - is dropt
glb_aff_wild: Global - Affecteds, wildtype <br/>
glb_aff_ncl:     Global - Affecteds, no call    <br/> 
glb_aff_vrt:     Global - Affecteds, with variant  <br/>
glb_aff_homv:    Global - Affecteds, homozygous for ALT allele<br/>
glb_aff_altaf:   Global - Affecteds, ALT allele frequency   <br/>
##### Family- Is dropt
{famid}_wild: Family - Affecteds: wildtype <br/>
{famid}_ncl: Family - Affecteds: no call<br/>
{famid}_vrt: Family - Affecteds: with variant<br/>
{famid}_homv: Family - Affecteds: homozygous for ALT allele<br/>
##### Family - Affected
{famid}_aff_wild: Family - Affecteds: wildtype <br/>
{famid}_aff_ncl: Family - Affecteds: no call<br/>
{famid}_aff_vrt: Family - Affecteds: with variant<br/>
{famid}_aff_homv: Family - Affecteds: homozygous for ALT allele<br/>
##### Family - Nonaffected   
{famid}_wild_naf: Family - Nonaffecteds: wildtype <br/>
{famid}_ncl_naf: Family - Nonaffecteds: no call<br/>
{famid}_vrt_naf: Family - Nonaffecteds: with variant<br/>
{famid}_homv_naf: Family - Nonaffecteds: homozygous for ALT allele<br/>

