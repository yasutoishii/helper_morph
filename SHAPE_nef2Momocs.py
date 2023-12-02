#!/usr/bin/env python

import pandas as pd
import argparse
import re

psr  = argparse.ArgumentParser(
    prog="SHAPE_nef2Momocs.py",
    usage='SHAPE_nef2Momocs.py -i NEF_FILE -o OUTPUT_CSV',
    description="This program reformat a nef file outputed by SHAPE to Momocs formats."
)

psr.add_argument('-i', '--input', help='.nef file: The EFA result file from SHAPE', required = True)
psr.add_argument('-o', '--output', help='Output csv file', required = True)

args        = psr.parse_args()
INPUT_FILE  = args.input
OUTPUT_FILE = args.output

with open(INPUT_FILE) as f:
    nef_dat = f.read().splitlines()
nef_dat = nef_dat[2:]

sample_names = [i for i in nef_dat if not i[0] == ' ']
if len(sample_names) == 0:
    print('Error: No sample name was detected !')
    print('Check: The sample names must not be started with a space')
    exit()

### Get No of coefficients ###
n_coeff = nef_dat.index(sample_names[1]) - nef_dat.index(sample_names[0]) - 1 

### Create a data frame to output ###
res_df = pd.DataFrame(
    columns = (
        ['ID'] +
        ['A{0}'.format(i) for i in range(1, n_coeff+1)] +
        ['B{0}'.format(i) for i in range(1, n_coeff+1)] +
        ['C{0}'.format(i) for i in range(1, n_coeff+1)] +
        ['D{0}'.format(i) for i in range(1, n_coeff+1)]
    )
)

coeff_oneindiv = dict()
for i in range(len(sample_names)):
    coeff_oneindiv = dict()

    for j in range(n_coeff+1):
        if j == 0:
            coeff_oneindiv['ID'] = [sample_names[i]]
        else:
            coeff_oneindiv_onedim = nef_dat[i*(n_coeff+1)+j].split()   ### Coeff: a[j], b[j], c[j], d[j] ###
            coeff_oneindiv_onedim = [float(k) for k in coeff_oneindiv_onedim]
            coeff_oneindiv['A{0}'.format(j)] = [coeff_oneindiv_onedim[0]]
            coeff_oneindiv['B{0}'.format(j)] = [coeff_oneindiv_onedim[1]]
            coeff_oneindiv['C{0}'.format(j)] = [coeff_oneindiv_onedim[2]]
            coeff_oneindiv['D{0}'.format(j)] = [coeff_oneindiv_onedim[3]]
    res_df = pd.concat([
        res_df,
        pd.DataFrame(coeff_oneindiv)
    ])

res_df.to_csv(
    OUTPUT_FILE,
    columns = None,
    index   = None
)