# collect ALL STATS 

# Written in Python 2.7
# RCK
# 8-5-11

import sys
sys.path.append('../common modules and helper scripts')

from optparse import OptionParser
import read_intermediate_files as rif

# Set up options
usage = """usage: %prog [options] output_filename task_name_translation_file.txt data_file1 [ data_file2 ... ] 
"""
parser = OptionParser(usage)
## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 3:
    parser.error("incorrect number of arguments")

output_filename = args[0]

task_name_translation_file = args[1]

data_files = args[2:]

data_structure = {} ## keyed by backbone task

translation = {}
translation_file = open( task_name_translation_file )
for line in translation_file:
    line = line.strip()
    if (len(line) == 0):
        continue

    line = line.split()
    translation[line[0]] = line[1]

translation_file.close()

for file in data_files:
    file = file.strip()

    if len(file) == 0:
        continue

    filenamebits = file.split('_')
    ## interpret the filename, which should be in the following format: 33_Andn_Backbone__mann_whitney_u_stats__control_vs_punish_xor
    ##                                                                      1                                                11    12
    backbone_task = translation[ filenamebits[1] ]
    fluctuating_task = translation[ filenamebits[12] ] # should be the same as [-1]
    punish_or_nopunish = filenamebits[11] 

    if not backbone_task in data_structure.keys():
        data_structure[backbone_task] = {} ## keyed by the fluctuating task

    if not fluctuating_task in data_structure[backbone_task].keys():
        data_structure[backbone_task][fluctuating_task] = {} ## keyed by the punish/nopunish

    data = rif.read_intermediate_datafile(file)

    data_structure[backbone_task][fluctuating_task][ punish_or_nopunish ] = data

    
means = {}
pvalues = {}

for backbone_task in data_structure.keys(): ## loop through the backbone tasks
    means[ backbone_task ] = {}
    pvalues[ backbone_task ] = {}
    for fluctuating_task in data_structure[ backbone_task ].keys():

        for punish_or_nopunish in data_structure[ backbone_task ][ fluctuating_task ].keys():
            if len(data_structure[ backbone_task ][ fluctuating_task ][ punish_or_nopunish ].keys()) > 0:

                control_mean_of_backbone_task = float( data_structure[ backbone_task ][ fluctuating_task ][ punish_or_nopunish ][ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Control'][ backbone_task ][0] )
                treatment_mean_of_backbone_task = float( data_structure[ backbone_task ][ fluctuating_task ][ punish_or_nopunish ][ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Treatment'][ backbone_task ][0] )
                difference_in_backbone_mean_fluctuaction = abs( treatment_mean_of_backbone_task - control_mean_of_backbone_task )

                control_std = float( data_structure[ backbone_task ][ fluctuating_task ][ punish_or_nopunish ][ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Control'][ backbone_task ][2] )
                treatment_std = float( data_structure[ backbone_task ][ fluctuating_task ][ punish_or_nopunish ][ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Treatment'][ backbone_task ][2] )

                ## assign the outgoing mean difference
                means[ backbone_task ][ fluctuating_task ] = difference_in_backbone_mean_fluctuaction

                if 'Mann_Whitney_U_Statistics_By_Task' in data_structure[ backbone_task ][ fluctuating_task ][ punish_or_nopunish ].keys() and difference_in_backbone_mean_fluctuaction > control_std and difference_in_backbone_mean_fluctuaction > treatment_std:
                    pvalues[ backbone_task ][ fluctuating_task ] = float( data_structure[ backbone_task ][ fluctuating_task ][ punish_or_nopunish ][ 'Mann_Whitney_U_Statistics_By_Task' ][ backbone_task ][1] )
                else:
                    pvalues[ backbone_task ][ fluctuating_task ] = 1
            else:
                means[ backbone_task ][ fluctuating_task ] = 0
                pvalues[ backbone_task ][ fluctuating_task ] = 1

## plot the thing
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
##### extra imports for dates example. remove after conversion
import matplotlib.dates as dates
import datetime, random
import matplotlib.colors as mplc
import matplotlib.cm as cm

task_order = [ 'Echo', 'Not', 'Nand', 'And', 'OrNot', 'Or', 'AndNot', 'Nor', 'Xor', 'Equals' ]
task_order_reverse = ['Equals', 'Xor', 'Nor', 'AndNot', 'Or', 'OrNot', 'And', 'Nand', 'Not', 'Echo' ]


######## THINGY!
def format_value(x, array=None):
     return task_order[x] #use FuncFormatter to dump out the strings

def format_value_rev(x, array=None):
     return task_order_reverse[x] #use FuncFormatter to dump out the strings


#r_d = random_date()
#some_dates = [dates.date2num(r_d.next()) for i in range(0,20)]
########## END THINGY

xplacements = np.arange( 10 ) ## 10 bars

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', xticklabels=task_order )

#x_values = range(10) * 10 ## x
#y_values = range(10) * 10 ## y 
x_values = []
y_values = []
bar_heights = [] ## dz
colors = []
normalized_pvalues = []
hatching = []
for y_index in range(10): ## from front to back
    for x_index in range(10): ## from left to right

        if (x_index == y_index):
            continue

        backbone = task_order[ y_index ]
        fluct = task_order[ x_index ]

        if pvalues[ backbone ][ fluct ] == 1:
            continue


#        if pvalues[ backbone ][ fluct ] <= 0.05:
#            hatching.append('/')
#        else:
#            hatching.append('')

        
        
        #means[ backbone ][ fluct ]
        #print str(x_index) + "," + str(y_index) + backbone + fluct + str(means[ backbone ][ fluct ])

        x_values.append( x_index - .25 )
        y_values.append( y_index - .25 )
        bar_heights.append( means[ backbone ][ fluct ] )

        #if pvalues[ backbone ][ fluct ] <= 0.01:
        #    colors.append('red')
        #elif pvalues[ backbone ][ fluct ] <= 0.05:
        #    colors.append('lightpink')
        #else:
        #    colors.append('white')

        #print  pvalues[ backbone ][ fluct ]

        if pvalues[ backbone ][ fluct ] <= 0.05:
            #print "OK : " + str( pvalues[ backbone ][ fluct ] )
            normalized_pvalues.append( pvalues[ backbone ][ fluct ] )
        else:
            #print "BAD: " + str(  pvalues[ backbone ][ fluct ] )
            normalized_pvalues.append( pvalues[ backbone ][ fluct ] + .3)


z_values = [0] * len(bar_heights) ## z
widths = [.5] * len(bar_heights)  ## dx
depths = [.5] * len(bar_heights)  ## dy


colors = [ cm.RdYlBu( pval ) for pval in normalized_pvalues ]

ax.bar3d(x_values, y_values, z_values, widths, depths, bar_heights, color=colors )

m = cm.ScalarMappable(cmap=cm.RdYlBu)
m.set_array(normalized_pvalues)
cb = plt.colorbar(m, ticks=[0.4, 0.05, 0.01])
cb.ax.set_ylabel('P-Value')
cb.set_ticklabels(ticklabels=['0.1', '0.05', '0.01'])

##### SET THE TICKS
ax.w_xaxis.set_major_locator(ticker.FixedLocator(range(10))) # I want all the dates on my xaxis
ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_value))
#for tl in ax.w_xaxis.get_ticklabels(): # re-create what autofmt_xdate but with w_xaxis
#       tl.set_ha('left')
       #tl.set_rotation(40)     

ax.w_yaxis.set_major_locator(ticker.FixedLocator(range(10))) # I want all the dates on my xaxis
ax.w_yaxis.set_major_formatter(ticker.FuncFormatter(format_value))
#for tl in ax.w_yaxis.get_ticklabels(): # re-create what autofmt_xdate but with w_xaxis
#       tl.set_ha('right')
       #tl.set_rotation(340)
#### done setting the ticks

#ax.view_init(70,135)
#ax.dist = 15
#ax.elev = 90
ax.azim = 210
#print ax.azim


ax.set_xlabel('Fluctuating Tasks')
ax.set_ylabel('Backbone Tasks')
ax.set_zlabel('Mean Amplitude Difference between Treatment and Control')
plt.hot()

plt.savefig(output_filename)

