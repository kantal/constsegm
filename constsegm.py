#!/usr/bin/env python3.8
#-*- coding:utf-8 -*-

""" Simultaneously Constant or Almost Constant Segments Detection

Copyright (c) 2021, Antal Koós
License: MIT
"""
__version__= "0.9.1"

import pandas as pd, numpy as np
from matplotlib import pylab as plt
import sys, pathlib as pth

#--------
# Input:
#--------
if len(sys.argv) != 4:
    print(f"Use: $ {pth.Path(sys.argv[0]).name}  path/data_file.csv  eps1  eps2")
    sys.exit()

fn_data, eps1, eps2= sys.argv[1:]
eps1, eps2= float(eps1), float(eps2)

#----------------------
# DataFrame processing:
#----------------------
df= pd.read_csv(fn_data, parse_dates=["Time"], index_col=["Time"], sep=";")

col_d1, col_d2= df.columns[:2]
# The criteria:
crit= df[col_d1].diff().abs().le(eps1) & df[col_d2].diff().abs().le(eps2)
crit[0]= crit[1]

shcrit= crit.shift(-1, fill_value=False)
crit= crit|shcrit

s= (~crit).cumsum()

G= df[crit].groupby(s)

#------------
# To stdout:
#------------
for _key,grp in G:
        print(f"{grp.index[0]} - {grp.index[-1]}")

#-----------
# Plotting:
#-----------
cols= [col_d1, col_d2]
eps= [eps1, eps2]

ax= df[cols].plot()

leg= ax.legend(ax.lines, [f"{c} ({e})" for c,e in zip(cols,eps)])
leg.set_draggable(True)
ax.set_title(pth.Path(fn_data).name)

#vi= 2.5    # indicator line position
vi= min(df[cols].min()) - 0.5

for _key,grp in G:

        x1,x2= grp.index[0], grp.index[-1]
        ax.hlines(vi, x1, x2, color="darkgreen", ls="--", alpha=0.5)
        ax.axvline(x1, c="darkgreen", ls="--", alpha=0.8)
        ax.axvline(x2, c="darkgreen", ls="--", alpha=0.8)

ax.grid(axis="both", which="both")
plt.show()
