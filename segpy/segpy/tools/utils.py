
def str_list(x):
    return str(x)


#################
################  clean_unique

def uniq_unsort(x):
    indexes = np.unique(x, return_index=True)[1]
    return ([x[index] for index in sorted(indexes)])

def gen_unique(x):
    xset = list(uniq_unsort(x))
    res0='|'.join(xset)
    return(res0)

def run_unique(x):
    res=x.apply(gen_unique)
    return(res)

def eval2(x):
    if x != x:
        return (x)
    else:
        return (eval(x))
    

#################
################  clean_seg_calculate_mean_mode

def floatB(aa):
    try:
        res=float(aa)
    except ValueError as err:
        res=np.NaN
    return(res)

def con_float(x):
    res0=[floatB(s) for s in x]
    return(np.nanmean(res0))

def check_is_numberic(x):
    ab=x[1:10].tolist()
    merged = list(itertools.chain(*ab))
    ac=list(filter(None, merged))
    while len(ac)<1:
        ad0=10
        ab=x[(1+ad0):(10+ad0)].tolist()
        merged = list(itertools.chain(*ab))
        ac=list(filter(None, merged))
    return(all(ele.isdigit() for ele in ac))

def cal_mode_mean(x):
    if check_is_numberic(x):
        res=x.apply(con_float)
    else:
        res=x.apply(mode)
    return(res)
