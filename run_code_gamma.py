'''
Sweep through different recovery rates (gamma)
'''
import os
from datetime import datetime
# os.system('py main.py 100 5 0.1 0.2 0.0001 0.999 -f sample_data run')
N = 100000
T = 500
i = 0   # counter

while i < 21:
    argument = 'py main.py {} {} 0 0.14 {} 0 0.000005 -m --1 *b=0.15,0.000005 *p=0.62,0.38 --7 *b=0.024,0.052,0.214,0.178,0.126,0.143,0.136,0.071,0.026,0.010 *d=0,0,0,0,0,0.018,0.073,0.255,0.364,0.291 --8 *b=0.0001,0.0002 *d=0.000001,0.0000005 -f {}_gamma{}_{} run'.format(N, T, i*5/100, datetime.today().strftime('%Y%m%d'), i*5, '01')
    print(argument)
    os.system(argument)
    i += 1
# 'py main.py {} {} {} 0.8 0.2 0.01 -f data_alpha{}_{} run'
