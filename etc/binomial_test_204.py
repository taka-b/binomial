# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 11:08:32 2020

@author: Takashi
"""

# from binomial_test_151.py

import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
from scipy.stats import binom
import math

# matplotlib の設定を調整   
plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定
plt.rcParams["figure.figsize"] = [12, 6]
plt.rcParams['font.size'] = 22 #フォントサイズを設定 default : 12
plt.rcParams['xtick.labelsize'] = 15 # 横軸のフォントサイズ
plt.rcParams['ytick.labelsize'] = 15

# 確率
p = 0.2

# 試行回数
TryNum = [3, 30, 100]
plotColor = ["r", "g", "b", "m"]

# 試行回数中の発生回数 (配列)  
variables = [np.arange(N+1) for N in TryNum]

# 二項分布の確率を取得
pmf_binom = [binom.pmf(k, N, p) for k, N in zip(variables, TryNum)]

# 自己情報量の計算
info_Shannon = [[-math.log2(p) for p in pmf_binom[i]] for i in range(len(pmf_binom))]
for ir, n in zip(info_Shannon, TryNum):
   # print(f" n = {n}, mini-info. = {min(ir)}, max-info = {max(ir)}")
   print(f" n = {n}, information = {ir}") 

# 確率×情報量　＝　情報の期待値成分
probability_expected = [[-p*math.log2(p) for p in pmf_binom[i]] for i in range(len(pmf_binom))]

# シャノンのエントロピー
entropy_Shannon = [sum([-p*math.log2(p) for p in pmf_binom[i]]) for i in range(len(pmf_binom))]


# 確率分布の表示
def plot_double(k, xAxis, ax_Left, ax_L_title, ax_Right, ax_R_title, N, p, c, viewNum = (0, "")):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(k, ax_Left, 'o', color=c, ms=10, label=f"{ax_L_title}: n={N}, p={p}")
    ax2 = ax1.twinx()
    ax2.vlines(k, 0, ax_Right, colors=c, lw=5, alpha=0.4, label=f"{ax_R_title}")
    if viewNum[0] == 0:
        pass
    else:
        plt.text(max(k)/2, max(ax_Left)/2, f"{viewNum[1]} = {viewNum[0]:.6f}", fontsize="large")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc='upper center')
    ax1.set_xlabel(xAxis)
    ax1.set_ylabel(ax_L_title)
    ax2.set_ylabel(ax_R_title)
    ax1.set_ylim([0, max(ax_Left)*1.2])
    ax2.set_ylim([0, max(ax_Right)*1.2])
    plt.title(f"{ax_L_title} and {ax_R_title}", fontsize=24)
    plt.show()
    
def plot_double_03(xAxis, ax_Left, ax_Right, title_info, viewNum = (0, "")):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(xAxis["xData"], ax_Left["L_data"],
             'o', color=ax_Left["color"], ms=10,
             label=f"{ax_Left['title']}")
    ax2 = ax1.twinx()
    ax2.vlines(xAxis["xData"], 0, ax_Right["R_data"], 
               colors=ax_Right["color"], lw=5, alpha=0.4, label=f"{ax_Right['title']}")
    if viewNum[0] == 0:
        pass
    else:
        plt.text(max(xAxis["xData"])/2, max(ax_Left["L_data"])/2,
                 f"{viewNum[1]} = {viewNum[0]:.6f}", fontsize="large")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc='upper center')
    ax1.set_xlabel(xAxis["title"])
    ax1.set_ylabel(ax_Left['title'])
    ax2.set_ylabel(ax_Right['title'])
    ax1.set_ylim([0, max(ax_Left["L_data"])*1.2])
    ax2.set_ylim([0, max(ax_Right["R_data"])*1.2])
    plt.title(f"{title_info['title']}", fontsize=24)
    plt.show()

    
def plot_single(k, xAxis, ax_Left, ax_L_title, N, p, c, viewNum = (0, "")):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.vlines(k, 0, ax_Left, color=c, label=f"n={N}, p={p}")
    if viewNum[0] == 0:
        pass
    else:    
        plt.text(max(k)/2, max(ax_Left)/2, f"{viewNum[1]} = {viewNum[0]:.6f}", fontsize="large")
    h1, l1 = ax1.get_legend_handles_labels()
    ax1.legend(h1, l1, loc='best')
    ax1.set_xlabel(xAxis)
    ax1.set_ylabel(ax_L_title)
    ax1.set_ylim([0, max(ax_Left)*1.2])
    plt.title(f"{ax_L_title}", fontsize=24)
    plt.show()
    
def plot_single_02(pd2d):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.vlines(pd2d.xData, 0, pd2d.yData, color=pd2d.color)
    plt.text(pd2d.max_x*0.25, pd2d.max_y*1.1, f"{pd2d.text} = {pd2d.textValue:.6f}", fontsize="large")
    h1, l1 = ax1.get_legend_handles_labels()
    ax1.legend(h1, l1, loc='best')
    ax1.set_xlabel(pd2d.xLabel)
    ax1.set_ylabel(pd2d.yLabel)
    ax1.set_ylim([0, pd2d.max_y*1.3])
    plt.title(f"{pd2d.title}", fontsize=24)
    plt.show()


class plotData_2D:
    def __init__(self, xData, xLabel, yData, yLabel, title="", color="k", text ="", v=None):
        self.xData = xData
        self.xLabel = xLabel
        self.yData = yData
        self.yLabel = yLabel
        self.title = title
        self.color = color
        self.xNum = len(self.xData)
        self.min_x = -min(self.xData)
        self.max_x = max(self.xData)
        self.min_y = -min(self.yData)
        self.max_y = max(self.yData)
        self.text = text
        self.textValue = v 
        
        
allPlotData = []
for i in range(len(TryNum)):
    
    pd2d = plotData_2D(variables[i], 'successes', 
                       pmf_binom[i], "probability", 
                       "Binomial", "b", "max_of probability", max(pmf_binom[i]))
    allPlotData.append(pd2d)
    

for pd2d in allPlotData:
    plot_single_02(pd2d)

    
# 情報量の表示_03
for i in range(len(TryNum)):
    plot_double_03({"xData": variables[i], 'title': 'successes: $\it{X}$'},
                   {"L_data": info_Shannon[i], 'title': "Information on reaction", "color": "r"},
                   {"R_data": pmf_binom[i], 'title': "probability", "color": "b"},
                   {'title': f"Information on reaction: n={TryNum[i]}, p={p}"} ) 
  
# シャノンのエントロピー        
for i in range(len(TryNum)):
    plot_double(variables[i], 'successes', 
                pmf_binom[i], "probability",
                probability_expected[i], "Entropy component", 
                TryNum[i], p, plotColor[i],  (entropy_Shannon[i], "RE")) 

# 
# 試行回数
TryNum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 100]
plotColor = ["g", "m"]

# 試行回数中の発生回数 (配列)  
variables = [np.arange(N+1) for N in TryNum]

# 二項分布の確率を取得
pmf_binom = [binom.pmf(k, N, p) for k, N in zip(variables, TryNum)]

# 自己情報量の計算, 最大値＆最小値
info_max = []
info_min = []
info_Shannon = [[-math.log2(p) for p in pmf_binom[i]] for i in range(len(pmf_binom))]
for ir, n in zip(info_Shannon, TryNum):
   print(f" n = {n}, mini-info. = {min(ir)}, max-info = {max(ir)}") 
   info_max.append(max(ir))
   info_min.append(min(ir))
   
plt.title("Information on Reaction", {"fontsize":25})
plt.xlabel("n: trial number", {"fontsize":15})
plt.ylabel("Information on reaction", {"fontsize":15})
plt.plot(TryNum, info_max,  label='maximun', marker="*")
plt.plot(TryNum, info_min,  label='minimum', marker=".")
plt.yscale("log", base = 10)
# plt.xscale("log", base = 10)
plt.legend()
plt.show()
   

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(TryNum, info_max, '*', color="g", ms=12, linestyle="-", label="maximun information")
ax2 = ax1.twinx()
ax2.plot(TryNum, info_min, ".", color="b", ms=12, linestyle="-", label="minimun information")
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='lower right')
ax1.set_xlabel("n: trial number")
ax1.set_xscale("log", base = 10)
ax1.set_ylabel("maximun information")
ax2.set_ylabel("minimun information")
ax1.set_yscale("log", base = 10)
ax2.set_yscale("log", base = 10)
ax1.set_ylim([0.1, 2.0e3])
ax2.set_ylim([0.1, 5e1])
plt.title("Information on Reaction", fontsize=24)
plt.show()










    
