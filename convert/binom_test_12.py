#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 16:10:13 2023

@author: takashi
"""

# https://python.atelierkobato.com/binomial/

import numpy as np
from scipy.stats import binom
import math
import time



# サイコロを10回振って、1の目が3回出る確率

N = 10
p = 0.5

for i in range(0, len(str(N))):
    m = (1e1)**i
    p3 = binom.pmf(m, N, p)
    print(f"m = {m}: ", "{:.20f}".format(p3))


m = np.arange(0, N+1, 1)
print("m: ", m)
p4 = binom.pmf(m, N, p)
print("p4: ", p4)

def _calcEntropy():
    entropy_Shannon = 0
    for p in p4:
        try:
            entropy_Shannon += -p*math.log2(p)
        except:
            pass
    return entropy_Shannon

def _calcEntropy_03(m, N, pl):
    entropies = []
    for p in pl:
        p4 = binom.pmf(m, N, p)
        entro = 0
        for pi in p4:
            try:
                entro += -pi*math.log2(pi)
            except:
                pass
        entropies.append(entro)
    return entropies


start = time.time()

entropy_Shannon = _calcEntropy()

elapsed_time = time.time() - start
print ("elapsed_time: {0}".format(elapsed_time) + "[sec]")
print("entropy_Shannon: ", entropy_Shannon)



# https://qiita.com/y_itoh/items/cf1229bebc4839041fd5

import scipy as sp

# 可視化ライブラリのインポート
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定

# 確率分布を取得
pmf_binom = sp.stats.binom.pmf(n=N, p=p, k=m)
print("pmf_binom: \n", pmf_binom)

# 可視化
plt.plot(m, pmf_binom, label='pmf')
plt.xticks(m)
plt.legend()
plt.grid()
plt.show()

Ns = [1, 10, 100]
pl = np.arange(0, 1.01, 0.01)
pl2 = np.arange(0, 1.1, 0.1)
print(f"pl: {pl}")
sh_ens_1 = _calcEntropy_03(np.arange(0, Ns[0]+1, 1), Ns[0], pl)
sh_ens_2 = _calcEntropy_03(np.arange(0, Ns[1]+1, 1), Ns[1], pl)
sh_ens_3 = _calcEntropy_03(np.arange(0, Ns[2]+1, 1), Ns[2], pl)

# print(f"sh_en: {sh_ens}")
# plt.legend(fontsize=12)
plt.plot(pl, sh_ens_3 , label=f'(a) max trials number, n = {Ns[2]}')  
plt.plot(pl, sh_ens_2 , label=f'(b) max trials number, n = {Ns[1]}')
plt.plot(pl, sh_ens_1 , label=f'(c) max trials number, n = {Ns[0]}')
 

plt.xlabel("probability of success; p")
plt.ylabel("Reaction Entropy")
plt.xticks(pl2)
plt.legend(loc=(0.31, 0.63), fontsize=10)
plt.grid()  
plt.show()

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
print(repr(now))
date = now.strftime('%x %X')
date = date.replace("/", ".")
date = date.replace(":", "_")


# plt.legend(fontsize=12)
plt.plot(pl, sh_ens_3 , label=f'(a) max trials number, n = {Ns[2]}')  
plt.plot(pl, sh_ens_2 , label=f'(b) max trials number, n = {Ns[1]}')
plt.plot(pl, sh_ens_1 , label=f'(c) max trials number, n = {Ns[0]}')
 

plt.xlabel("probability of success; p")
plt.ylabel("Reaction Entropy")
plt.xticks(pl2)
plt.legend(loc=(0.31, 0.63), fontsize=10)
plt.grid()  

plt.savefig(f"RE_{date}.png", format="png", dpi=300)





