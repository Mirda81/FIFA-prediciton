from scipy.stats import skew, kurtosis
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def des_object(df, varname):
    table = vcounts = df[varname].value_counts()
    vcounts_len = len(vcounts)
    std = round(float(df[[varname,'SalePrice']].groupby(varname).agg(['mean']).std()),0)
   
    print("")
    print("*********************************")

    plt.figure(figsize=(16,5))
    sns.set_style("whitegrid")
    plt.subplot(121)
    plt.axis([0, 10, 0, 10])
    i = 7.5
    plt.text(0, 8.5, f"there is: {vcounts_len} different values", horizontalalignment='left', fontsize=12 )
    for row in range(np.min([len(table),10])):
      text = table.index[row] + ": " + str(table.iloc[row])      
      plt.text(0, i, text, horizontalalignment='left', fontsize=12 )
      i-=0.5
    plt.text(0, i-0.5, f"std: {std}", horizontalalignment='left', fontsize=12 )
   
    plt.text(0, 9, '-------------------------------------------------------', horizontalalignment='left', fontsize=12 )
    plt.title(varname + "| type:" + str(df[varname].dtype),loc='left', weight = 'bold')
    plt.axis('off')  
    plt.subplot(122)    
    g = sns.boxenplot(x = varname, y='SalePrice', data = df,showfliers = False)
    sns.pointplot(x = varname, y='SalePrice', data = df,linestyles='--', scale=0.4, 
              color='k', capsize=0)
    g.set_title(varname)
    plt.xlabel('')
    plt.xticks(rotation=90)      
    plt.tight_layout()
    plt.show()
    print("*********************************")
    print("")
    
def des_numeric(df, varname):
    print("*********************************")    
    table = pd.DataFrame(df[varname].describe().round(2))
    skw = skew(df[varname], axis=0, bias=True)
    kts = kurtosis(df[varname], axis=0, bias=True)    
  
    
    sns.set_style("whitegrid")
    plt.figure(figsize=(16,5))
    plt.subplot(131)
    plt.axis([0, 10, 0, 10])
    i = 8.5
    for row in range(len(table)):
      text = table.index[row] + ": " + str(table.iloc[row,0])      
      plt.text(0, i, text, horizontalalignment='left', fontsize=12 )
      i-=0.5
    
    
    plt.text(0, 9, '-------------------------------------------------------', horizontalalignment='left', fontsize=12 )
    plt.text(0, i, f"NA values: {df[varname].isna().sum()}", horizontalalignment='left', fontsize=12 )
    plt.text(0, i-0.5, f"unique values: {df[varname].nunique()}", horizontalalignment='left', fontsize=12 )
    plt.text(0, i-1.5, f"skew: {round(skw,2)}", horizontalalignment='left', fontsize=12 )
    plt.text(0, i-2, f"kurtosis: {round(kts,2)}", horizontalalignment='left', fontsize=12 )

    plt.title(varname + "| type:" + str(df[varname].dtype),loc='left', weight = 'bold')
    plt.axis('off')

    plt.subplot(132)
    g= sns.histplot(data=df[varname],alpha=1, discrete=True)
    g.set_title('Histogram')
    plt.subplot(133)
    g1 = sns.boxplot(data=df[varname], palette=['#7FFF00'])
    g1.set_title('Boxplot')
    plt.xticks([])
    plt.tight_layout()
    plt.show()
    
def des_df(df):
    for c in df.columns:
        if df[c].dtype == object:
            des_object(df,c)
        else:
            des_numeric(df,c)



from scipy.stats import poisson
def get_goals_proba(lam):
    return [poisson.pmf(i, lam) for i in range(0,6)] + [1 - poisson.cdf(5, lam)]

def get_goal_line_proba(p1_avg_goals, p2_avg_goals):
    p1=get_goals_proba(p1_avg_goals)
    p2=get_goals_proba(p2_avg_goals)
    
    p_total_gt15 = sum(p1[i]*sum(p2[j] for j in range(len(p2)) if i+j > 1) for i in range(len(p1)))
    p_total_gt25 = sum(p1[i]*sum(p2[j] for j in range(len(p2)) if i+j > 2) for i in range(len(p1)))
    p_total_gt35 = sum(p1[i]*sum(p2[j] for j in range(len(p2)) if i+j > 3) for i in range(len(p1)))
    p_total_gt45 = sum(p1[i]*sum(p2[j] for j in range(len(p2)) if i+j > 4) for i in range(len(p1)))
    p_total_gt55 = sum(p1[i]*sum(p2[j] for j in range(len(p2)) if i+j > 5) for i in range(len(p1)))
    
    return {'over 1.5': p_total_gt15,'over 2.5': p_total_gt25, 'over 3.5': p_total_gt35, 'over 4.5': p_total_gt45, 'over 5.5': p_total_gt55 }
def get_win_proba(p1_avg_goals, p2_avg_goals):
    p1=get_goals_proba(p1_avg_goals)
    p2=get_goals_proba(p2_avg_goals)
    win_p1 = sum(p1[i] * sum(p2[j] for j in range(i)) for i in range(len(p1)))
    win_p2 = sum(p2[i] * sum(p1[j] for j in range(i)) for i in range(len(p2)))
    tie_p = 1-win_p1-win_p2
    return f"{round(win_p1*100,2)} - {round(tie_p*100,2)} - {round(win_p2*100,2)}"







