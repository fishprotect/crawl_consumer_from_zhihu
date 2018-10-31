import argparse
par = argparse.ArgumentParser()
par.add_argument('-url',required = True)
par.add_argument('-ar') 

try:
    Arg = par.parse_args().url
    
except:
    Arg = 'none'
