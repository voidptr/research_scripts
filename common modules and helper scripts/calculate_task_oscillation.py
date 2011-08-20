## calculate task oscillation

import math
import numpy as np

## collect the amplitudes from the raw data.
def calculate_task_amplitudes(samples, task_names, updates_list, start_update, stop_update, cycle_length):

    ## calculate the amplitudes for each sample
    amplitudes_by_sample_and_task = []
    for sample in samples:
        amplitudes_by_sample_and_task.append({})
        for task_name in sample.keys():
    
            amplitudes_by_sample_and_task[-1][task_name] = [] ## the amplitudes will go here.

            task = sample[task_name]
        
            last_cycle = -1
            max_val = -1
            min_val = -1
            for sample_index in range(0, len(task)):
                cycle = (updates_list[sample_index] - start_update) / cycle_length
                incycle_sample_number = (updates_list[sample_index] - start_update) % cycle_length

               # print task[sample_index]

                if cycle > last_cycle:  ## we're now in a new cycle
                    if max_val != -1 and min_val != -1: # and we've something to show from the previous go-round
                       # amplitudes_by_task[-1].append( (max_val, min_val, max_val - min_val) ) ## store the amplitude (tuple)
                        amplitudes_by_sample_and_task[-1][task_name].append( max_val - min_val ) ## store the amplitude

                    max_val = task[sample_index] ## reset the max and min to the first value.
                    min_val = task[sample_index] 
                else:
                    if max_val < task[sample_index]:
                        max_val = task[sample_index]

                    if min_val > task[sample_index]:
                        min_val = task[sample_index]        
        
                last_cycle = cycle;

    return amplitudes_by_sample_and_task

## calculate general stats from the values collected.
def calculate_stats_by_task_and_sample( amplitudes_by_sample_and_task, task_names ):

    sample_stats = [] ## the individual replicates

    for sample in amplitudes_by_sample_and_task:
        sample_stats.append({}) ## push a new {} (with keys of the task name) onto the end of the array

        for task_name in task_names:
            sample_stats[-1][ task_name ] = {} ## for the stats with their names. This is dumb and should be an object, but I'll fix it later.

            sample_stats[-1][ task_name ][ 'median' ] =  np.median ( sample[ task_name ] )
            sample_stats[-1][ task_name ][ 'mean' ] = np.mean ( sample[ task_name ] )
            sample_stats[-1][ task_name ][ 'std' ] = np.std ( sample[ task_name ] )
            sample_stats[-1][ task_name ][ 'ste' ] = np.std ( sample[ task_name ] ) / math.sqrt( len (sample[task_name]) )
            sample_stats[-1][ task_name ][ 'variance' ] = np.var ( sample[ task_name ] )

    return ( sample_stats )


## this method aggregates the above piecemeal methods -- dunno if this is actually useful.
def calculate_oscillation_stats_by_task(samples, task_names, updates_list, start_update, stop_update, cycle_length):
    
    ## calculate the amplitudes for each sample
    amplitudes_by_sample_and_task = calculate_task_amplitudes(samples, task_names, updates_list, start_update, stop_update, cycle_length)


    ## now, calculate the stats for each sample. These are within sample statistics.
    stats_by_sample_and_task = calculate_oscillation_stats_by_task_and_sample( amplitudes_by_sample_and_task, task_names )
   
    ## finally, calculate the mean median amplitude, by taking the median of all the samples' median amplitudes.
    mean_amplitudes_by_task = {}
    median_amplitudes_by_task = {}
    std_mean_amplitudes_by_task = {}
    ste_mean_amplitudes_by_task = {}
    variance_amplitudes_by_task = {}

    for task_name in task_names:
        median_amplitudes = []
        #for sample in median_amplitudes_by_sample_and_task:
        for sample in stats_by_sample_and_task['median']:
            median_amplitudes.append( sample[ task_name ] )

        mean_amplitudes_by_task[ task_name ] = np.mean( median_amplitudes )
        median_amplitudes_by_task[ task_name ] = np.median( median_amplitudes )
        std_mean_amplitudes_by_task[ task_name ] = np.std( median_amplitudes )
        ste_mean_amplitudes_by_task[ task_name ] = np.std( median_amplitudes ) / math.sqrt( len( median_amplitudes) )
        variance_amplitudes_by_task[ task_name ] = np.var( median_amplitudes )

    stats = {}
    stats['mean'] = mean_amplitudes_by_task
    stats['median'] = median_amplitudes_by_task
    stats['std'] = std_mean_amplitudes_by_task
    stats['ste'] = ste_mean_amplitudes_by_task
    stats['variance'] = variance_amplitudes_by_task

    return (stats)



