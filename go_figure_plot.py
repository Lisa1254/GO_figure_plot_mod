#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 12:00:51 2022

@author: lhoeg
"""

#Adapt Go-Figure plotting to include size legend, and full GO term names

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import matplotlib.patches
from textwrap import wrap

#Set path for input and output files
path = r'/Users/lhoeg/Documents/GO_Fig_test/'

#Import numeric data from Go-figure output file
filename = r'COL_GO_fig_results_data.tsv'
df = pd.read_csv(path+filename, sep="\t")

#Import cluster file to have access to full GO term labels without truncating
names_file = r'COL_GO_fig_results_clusters.tsv'
df_names = pd.read_csv(path+names_file, sep="\t")

#COLOUR

#Choose colour palette
cmap = ListedColormap(sns.color_palette('plasma'))
#Choose dataframe column to use for colour. Using same as defined in original run of Go-figure
colour_criterium = df['colour']
#Set up colour-space using normalized colour data, and colour mapping
norm = plt.Normalize(colour_criterium.min(), colour_criterium.max())
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

#SIZE

#Set size range of marker points. Using default from Go-figure, 'medium'
size_range = (400,4000)

#FIGURE
#Using 21(26) as max labels since that was the input to Go-figure. This might need adjusting later.
max_labels = 26

#Set up figure space for main plot, and size legend plot
fig, axs = plt.subplots(1, 2, figsize=(8, 4), gridspec_kw=dict(width_ratios=[4, 1]))

#Construct main figure
ax1 = sns.scatterplot(x='x',y='y',size='size',sizes=size_range,hue='colour',palette=cmap,edgecolor='black',data=df.iloc[::-1],alpha=0.5,linewidth=1, ax=axs[0])

#Set axis labels
xlabel = "Semantic space X"
ylabel = "Semantic space Y"
ax1.set_xlabel(xlabel)
ax1.set_ylabel(ylabel)

#Label clusters
#Using default opacity of 1
opacity=1
#This relies on the max_labels that I'm not sure I'm importing fully correct
if len(df.index) >= max_labels:
    for line in range(0,max_labels):
        ax1.text(df.x[line], df.y[line], df.dotCount[line], horizontalalignment='center', verticalalignment='center', size='small', color='black', alpha=opacity)
else:
    for line in range(0,len(df.index)):
        ax1.text(df.x[line], df.y[line], df.dotCount[line], horizontalalignment='center', verticalalignment='center', size='small', color='black', alpha=opacity)

#SIZE FIGURE

#Determine sizes and labels for size legend figure
#Get all sizes
all_sizes = []
for line in range(0,len(df.index)):
    new_size = df.members[line].count(",") + 1
    all_sizes.append(new_size)
#Determine 4 labels
s_lab_min = min(all_sizes)
s_lab_max = max(all_sizes)
s_lab_1_3 = int((s_lab_max - s_lab_min + 1) / 3)
s_lab_2_3 = s_lab_1_3 * 2
#Determine middle size values from size range.
s_ran_1_3 = int((size_range[1]-size_range[0])/3+size_range[0])
s_ran_2_3 = int(2*(size_range[1]-size_range[0])/3+size_range[0])

#Plot size legend figure
ax2 = plt.scatter(x=np.repeat(1,4), y=(0,0.85,2.05,3.5), s=(size_range[0],s_ran_1_3,s_ran_2_3,size_range[1]), color='w', alpha=0.5, linewidth=1, edgecolor='black')
#Set axis parameters
ax2.axes.xaxis.set_visible(False)
ax2.axes.yaxis.set_ticklabels([])
ax2.axes.yaxis.set_ticks([])
ax2.axes.set_ylim(-0.5,4.5)
y2_label = "GO Terms per cluster"
axs[1].set_ylabel(y2_label)
#Add size label to each point
axs[1].text(1, 0, str(s_lab_min), horizontalalignment='center', verticalalignment='center', size='small', color='black')
axs[1].text(1, 0.85, str(s_lab_1_3), horizontalalignment='center', verticalalignment='center', size='small', color='black')
axs[1].text(1, 2.05, str(s_lab_2_3), horizontalalignment='center', verticalalignment='center', size='small', color='black')
axs[1].text(1, 3.5, str(s_lab_max), horizontalalignment='center', verticalalignment='center', size='small', color='black')

#COLORBAR LEGEND

#Choose either default ticks:
colorbar = ax1.figure.colorbar(sm,alpha=0.5)
#Or rounded to integer ticks
#kwargs = {'format': '%.0f'}
#colorbar = ax1.figure.colorbar(sm,alpha=0.5,**kwargs)
#Remaining colorbar parameters
colorbar.ax.tick_params(size=0)
#Add label to colour bar
colorbar.set_label('log10 pvalue (Representative)')


#LABEL LEGEND

#Set number of columns for cluster label legend
colnumber = 2
#Using legend position left for alignment
legend_position = 'left'
#Default font size is 'medium'
font_size = 'medium'

# Get full names from cluster file
df_names_sub = df_names[df_names['Cluster representative'] == df_names['Cluster member']]
full_names = []
for line in range(0,len(df.index)):
    test = df.representative[line]
    found_test = np.where(df_names_sub == test)[0][0]
    found_desc = str(line+1)+". "+df_names_sub.iloc[found_test,2]
    full_names.append(found_desc)
#Use text wrap at 50 character limit
labels_wrap = [ '\n'.join(wrap(l, 50)) for l in full_names]

#Set up empty space for labels in legend
empty_handle = matplotlib.patches.Rectangle((0,0), 1, 1, fill=False, edgecolor='none',visible=False)
#Use of max_labels again here, not sure if I'll be keeping/or fixing
handle_list = [empty_handle]*max_labels

#Add legend to figure
legend_ax = ax1.legend(handle_list,labels_wrap,bbox_to_anchor=(-0.2, -0.15),loc='upper '+legend_position.lower(),handlelength=0, handletextpad=0, ncol=colnumber, frameon=False, fontsize=font_size)
#Ensure rectangle handle for plotting legend is not visible
for item in legend_ax.legendHandles:
    item.set_visible(False)
    

#SAVE

dpi = 400
#Saving as pdf, can also do png
fig.savefig(path+'COL_test_image.pdf',dpi=dpi,bbox_extra_artists=(legend_ax,),bbox_inches='tight')

#









