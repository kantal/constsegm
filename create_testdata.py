#!/usr/bin/env python3.8
#-*- coding:utf-8 -*-

"""Creating test data"""

import numpy as np
import sys

fn_data="test_data.csv" if len(sys.argv)==1 else sys.argv[1]

np.random.seed(33)
rnd= np.random.random
ay1= [np.full(4, 6), rnd(4)+6.5, [7,7,7], np.arange(8,9, 0.2), np.full(3,10)]
ay2= [np.full(6, 2), [5,6,6,6,6],     np.arange(4,6, 0.5), np.full(4,7)]
ay1= np.concatenate(ay1)
ay2= np.concatenate(ay2)
#ay2= np.random.random(len(ay1))

tstart= np.datetime64("2020-01-08T12:00")
tstop= tstart + len(ay1)*np.timedelta64(10,"m")
tim= np.arange(tstart,tstop,10, dtype='datetime64[m]').astype("U")

with open(fn_data,"w") as ff:

    ff.write("Time;Data1;Data2\n")  # header
    for r in zip(tim, ay1, ay2):

        ff.write(r[0]+";")
        ff.write( ";".join([str(v) for v in r[1:]]) )
        ff.write("\n")
