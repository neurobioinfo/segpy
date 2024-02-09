import os 
import pandas as pd 
import numpy as np
from statistics import mode
from pyspark.sql.functions import udf
from pyspark.sql.functions import col
from pyspark import SparkContext, SQLContext
sc = SparkContext.getOrCreate()
spark = SQLContext(sc)
##################################

def clean(outfolder,method='general'):
    if method=='general':
        clean_general(outfolder)
    elif method=='unique':
        clean_unique(outfolder)

##########
def clean_general(outfolder):
    finalseg='finalseg.csv'
    finalseg_modified='finalseg_modified_general.csv'
    cmd_cp=f'cd {outfolder}; cp {finalseg} {finalseg_modified}'
    os.system(cmd_cp)
    cmd_prune=f'cd {outfolder}; sed -i {finalseg_modified} -e "s/\\"//g" -e  "s/\[//g" -e "s/\]//g" -e " s/\, /\|/g" -e "s/\,/\|/g" -e "s/\t/,/g" '
    os.system(cmd_prune)

def clean_unique(outfolder):
    """
    outfolder: the folder that you want to save your output 
    header_need: the header that you want. 
    """
    finalseg='finalseg.csv'
    finalseg_modified_mode='finalseg_modified_uniq.csv'
    final_name=f'{outfolder}/{finalseg}'        
    final=pd.read_csv(final_name, sep='\t',index_col=False)
    columns_all=final.columns.to_list()
    columns_csq = [col for col in columns_all if 'csq' in col]
    udf_s = udf(lambda x: list(set(eval(x))))
    f_rddcsq = spark.createDataFrame(final.loc[:,columns_csq])
    f_rddcsq=f_rddcsq.select(*(udf_s(col(c)).alias(c) for c in columns_csq))
    f_rddcsq_pd=f_rddcsq.toPandas()
    for i in columns_csq:
        final[i]=f_rddcsq_pd[i]
    final_name=f'{outfolder}/{finalseg_modified_mode}'
    final.to_csv(final_name,index=False,sep='\t')
    cmd_prune=f"cd {outfolder}; sed -i {finalseg_modified_mode} -e 's/,/\|/g' -e 's/\"//g' -e 's/\t/,/g' -e 's/\[//g' -e 's/\]//g' -e 's/ //g' "
    os.system(cmd_prune)

##########################################################################################
########## Archive 
from segpy.tools.utils import uniq_unsort,gen_unique,run_unique,eval2

def clean_unique_archive(outfolder):
    """
    outfolder: the folder that you want to save your output 
    header_need: the header that you want. 
    """
    finalseg='finalseg.csv'
    finalseg_modified_mode='finalseg_modified_mode.csv'
    # header_fin_name=f'{outfolder}/header.txt'    
    # header_fin=pd.read_csv(header_fin_name, sep='\t',index_col=False,header=None)
    # header_need_name=f'{header_need}'            
    # header_need=pd.read_csv(header_need_name, sep='\t',index_col=False,header=None)
    final_name=f'{outfolder}/{finalseg}'        
    final=pd.read_csv(final_name, sep='\t',index_col=False)
    # header_fin=list(final.columns)   
    # list2=[header_fin.index(i) for i in header_need.iloc[0,:].tolist()]
    # list2=list(set(list2))
    # final2=final.iloc[:,list2]
    for i in list(np.where(final.dtypes=='object')[0]):
        if i==0: continue 
        try: 
            final.iloc[:,i] = final.iloc[:,i].apply(eval2)
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):    
            pass
        final.iloc[:,i]=run_unique(final.iloc[:,i])
    final_name=f'{outfolder}/{finalseg_modified_mode}'        
    final.to_csv(final_name,index=False)
    cmd_prune=f'cd {outfolder}; sed -i {finalseg_modified_mode} -e "s/,|/,/g" -e "s/|,/,/g"'
    os.system(cmd_prune)


##########
# the following function calculate the mean and mode 
from segpy.tools.utils import floatB,con_float,check_is_numberic,cal_mode_mean

def clean_seg_calculate_mean_mode_archive(outfolder, header_need, header_to_modify):
    header_fin_name=f'{outfolder}/header.txt'    
    header_fin=pd.read_csv(header_fin_name, sep='\t',index_col=False,header=None)
    header_need_name=f'{outfolder}/{header_need}'            
    header_need=pd.read_csv(header_need_name, sep='\t',index_col=False,header=None)
    header_abs_name=f'{outfolder}/{header_to_modify}'    
    header_abs=pd.read_csv(header_abs_name, sep='\t',index_col=False,header=None)
    final_name=f'{outfolder}/finalseg.csv'        
    final=pd.read_csv(final_name, sep='\t',index_col=False)
    list1=[header_fin.iloc[0,:].tolist().index(i) for i in header_abs.iloc[0,:].tolist()]
    list2=[header_fin.iloc[0,:].tolist().index(i) for i in header_need.iloc[0,:].tolist()]
    j_t=header_fin.shape[1]
    for i in list1:
        if i==0: next 
        if isinstance(final.iloc[:,i], object):
            final.iloc[:,i] = final.iloc[:,i].apply(eval)
        j_t=j_t+1
        new_col=final.columns[i]+'modified'
        final[new_col]=cal_mode_mean(final.iloc[:,i])
    new_list = [x+header_fin.shape[1] for x in range(0,len(list1))]
    listt=list2+new_list
    final2=final.iloc[:,listt]
    # final_name=f'{outfolder}finalseg_m.csv'
    # final.iloc[:,listt].to_csv(final_name,index=False)
    for i in range(1,final2.shape[1]):
        # if i==0: next 
        try: 
            final2.iloc[:,i] = final2.iloc[:,i].apply(eval)
        except :
            next
    final2_name=f'{outfolder}/finalseg_modified.csv'        
    final2.to_csv(final2_name,index=False)
    cmd_prune=f'cd {outfolder}; sed -i finalseg_modified.csv -e "s/\'//g"'
    os.system(cmd_prune)

##########
if __name__ == "__main__":
    clean()
