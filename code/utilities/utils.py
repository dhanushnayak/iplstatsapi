def convert_to_over(x):
    o = int(x/6)
    b = x%6
    over = f'{o}.{b}'
    return float(over)


def nan_check(x):
    if isinstance(x,dict):
        d={}
        for i,j in x.items(): 
            if ((j>0)==False):d[i]=0
            else: d[i]=j
        print("Done",d)
        return d
    else:
        if ((x>0) == False): return 0
        else: return x