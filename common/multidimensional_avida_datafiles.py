## multidimensional avida data

import sys
import gzip

## each file is an quasi-independent entity, with its own data separated by tasks
def load_tasks_files_as_samples_by_file( inputfilenames, start_update=0, stop_update=sys.maxint ):
   
    # set up the data object
    samples = [] ## the array of samples
    task_names = [] ## the collection of task names
    update_list = [] ## the set of sampled updates

    first_file = True

    for inputfilename in inputfilenames:
        samples.append( {} ) ## append a sample dictionary.
        if inputfilename[-3:] == ".gz":
            fd = gzip.open(inputfilename)
        else:
            fd = open(inputfilename)  
 
        line_ct = 0
        for line in fd:
            line = line.strip() ## strip off the end of line crap
            if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
                if line_ct > 4 and len(line) > 0: ## there are names here!
                    line = line.split()
                    taskname = line[-1]
                    if first_file:
                        task_names.append( taskname )

                    samples[-1][taskname] = [] ## put an empty list under the task name to hold the samples.
                line_ct += 1
                continue

            line = line.split() ## break the line up on spaces
            ## the lines are split up into: update, task1, task2, task3, ...
            update = int(line[0])

            ## limit the selection of data if required
            if update >= start_update and update <= stop_update:
                update_list.append(update)
                for i in range(0, len(task_names)):
                    samples[-1][ task_names[i] ].append( int(line[i+1]) )

        fd.close()
        first_file = False

    return samples, task_names, update_list

def load_tasks_files_as_samples_by_update( inputfilenames, start_update=0, stop_update=sys.maxint ):
   
    # set up the data object
    tasks = {} ## the dictionary of tasks
    task_names = [] ## the collection of task names
    update_list = [] ## the set of sampled updates

    first_file = True ## if this is the first file of the dataset, do some stuff.
    
    for inputfilename in inputfilenames:
        if inputfilename[-3:] == ".gz":
            fd = gzip.open(inputfilename)
        else:
            fd = open(inputfilename)  
 
        header_line_ct = 0
        data_line_ct = 0
        for line in fd:
            line = line.strip() ## strip off the end of line crap
            if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
                if line_ct > 4 and len(line) > 0 and first_file: ## there are names here!
                    line = line.split()
                    taskname = line[-1]
                    task_names.append( taskname )
                    tasks[taskname] = [] ## create an empty list under the task name to hold the data for that task.
                header_line_ct += 1
                continue

            
            line = line.split() ## break the line up on spaces
            ## the lines are split up into: update, task1, task2, task3, ...
            update = int(line[0])
            if update >= start_update and update <= stop_update: ## if we're in the proper range, gather the data.
                if first_file:
                    update_list.append(update)
                    for taskname in task_names:
                        tasks[taskname].append([]) ## add a new samples array for this update, for each task.

                ## now go through and insert the sample at the end of the samples array for this task and this update.
                for i in range(0, len(task_names)):
                    tasks[ task_names[i] ][data_line_ct].append( int(line[i+1]) )

                data_line_ct += 1

        fd.close()
        first_file = False ## we're done with the first file of the dataset.

    return tasks, task_names, update_list














