#!/usr/bin/python

################################
# Analysis script
#
# last updated 3/30/12
################################

#############
## There are a series of stages and actions. The levels go as follows:
## STAGE 4 -- PHYSICAL MODULARITY
## C.1 -> aggregated a single column - (fluct task unity mean) of every B.1 file into a single line in C.1; One file per treatment, 30 lines per file, 600 columns per line
## C.2 -> aggregated a single column - (backbone task unity mean) of every B.2 file into a single line in C.2; One file per treatment, 30 lines per file, 600 columns per line
## C.3 -> aggregated a single column - (fluct task scatter mean) of every B.3 file into a single line in C.3; One file per treatment, 30 lines per file, 600 columns per line
## C.4 -> aggregated a single column - (backbone task scatter mean) of every B.4 file into a single line in C.4; One file per treatment, 30 lines per file, 600 columns per line
## STAGE 5 -- TASKS COUNT
## D.1 -> aggregated the content of a single column in the task file (T.1) into a line in D.1; One file per treatment, 30 lines per file, 600 columns per line
## STAGE 7 -- FUNCTIONAL MODULARITY (like stage 4 but for functional modularity only)
## F.1 -> aggregated a single column - (functional modularity mean) of every E.1 file into a single line in F.1; One file per treatment, 30 lines per file, 600 columns per line


import glob
import os
from optparse import OptionParser
import sys

# Set up options
usage = """usage: %prog [options] action1 [action 2 ...]

Permitted actions
test_progress, sanitize, tasks, fitness, coalescent, aggregate_funct_mod, aggregate_phys_mod, aggregate_mutation_metrics
          
"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")

parser.add_option("-t","--treatment", dest = "treatment", help = "Run the command in screen")

parser.add_option("-u", "--update_only", action = "store_true", dest = "update_only",
                  default = False, help = "Update only")

parser.add_option("-s","--screen", dest = "screen", help = "Run the command in screen")

parser.add_option("-l","--script_location", dest = "location", help = "script directory location")

parser.add_option("-T","--test", dest = "test", help = "which test(s) to run")

parser.add_option("-e","--expected", dest = "expected", help = "expected counts (in line and values)")


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")

## actions
actions = args[0:]
acceptable_actions = ['test_progress', 'sanitize', 'tasks', 'fitness', 'coalescent', 'aggregate_funct_mod', 'aggregate_phys_mod', 'aggregate_mutation_metrics' ]

for action in actions:
    if not action in acceptable_actions:
        parser.error("unknown action: %s" % action)

## treatment
if not options.treatment:
    options.treatment = ""

## tests to run
test = ['all']
if options.test:
    test = options.test.split(',')

expected = 0
if options.expected:
    expected = int(options.expected)


if not options.location:
    options.location = os.path[0]

if not options.location:
    parser.error("script directory path is required")

## ############# SCRIPT PATHS ################ ##

extract_line_on_condition_path = "../../%s/common\ modules\ and\ helper\ scripts/extract_line_on_condition.py" % options.location
calculate_physical_modularity_path="../../%s/evolution_of_modularity_pipelines/calculate_physical_modularity.py" % options.location
convert_to_organisms_path="../../%s/evolution_of_modularity_pipelines/convert_to_organisms.py" % options.location
extract_single_column_to_csv_path="../../%s/common\ modules\ and\ helper\ scripts/extract_single_column_to_csv.py" % options.location
aggregate_file_path = "../../%s/common\ modules\ and\ helper\ scripts/aggregate_file.py" % options.location


analyze_path=sys.argv[0]

if "sanitize" in actions:
    files = glob.glob("*_??????")
    if not os.path.exists("empty_data_directories"):
        os.mkdir("empty_data_directories")
    for file in files:
        print file
        if not os.path.exists("%s/data/" % file):
            print "Is Empty. Moving %s" % file
            os.popen("mv %s empty_data_directories" % file)
        else:
            os.chdir("%s/data/" % file)
            print "Gunzipping all the files."
            os.popen("gunzip --recursive ./")
            os.chdir("../../")

if "test_progress" in actions:

    failed_lines = []

 

    print "Testing Collected Data."
    print "======================="

    files = glob.glob("*_??????")
    for file in files:
        if not os.path.exists("%s/data/" % file):
            print "%s/data/ not found" % file
            continue
        else:
            print "-------------------------------------------------------------------------------"
            print file
            print "-------------------------------------------------------------------------------"

        os.chdir("%s/data/" % file)


        if '0' in test or 'all' in test:
            ## test basic existence 
            print "TEST 0:"
            root_modularity_files = glob.glob("individual_modularity-*.dat*")
            root_ct = len(root_modularity_files)
            if root_ct == expected:
                print "  %s files found." % root_ct
                print "---------------------------------------------------------------- PASSED"
            else:
                print "  no files found."
                print "-------------------------------------------------------- FAILED"

           
        if '1' in test or 'all' in test:
            ## test two-task extraction
            print "TEST 1: extract_twotask"
            if not os.path.exists("two_task_only_individual_modularity"):
                print "  No two_task_only_individual_modularity/ found."
                print "-------------------------------------------------------- FAILED"
                failed_lines.append( "%s - Test 1 - missing dir" % file)

            else:
                os.chdir("two_task_only_individual_modularity")
                two_task_files = glob.glob("two_task_only__*.dat*")
                two_task_ct = len(two_task_files)
                if len(two_task_files) != expected:
                    print "  Wrong count. Expected: %s, found: %s" % (expected, len(two_task_files))
                    print "-------------------------------------------------------- FAILED" 
                    failed_lines.append( "%s - Test 1 - bad count" % file)
                else:
                    print "  File count aggrees. OK :D"
                    print "---------------------------------------------------------------- PASSED"

                if len(two_task_files) > 0 and two_task_files[0][-3:] == ".gz":
                    print "  Files not sanitized. run sanitize for speed."
                    print "----------------------------------------------- NOTE"
                os.chdir("../")

        if '2' in test or 'all' in test:
            ## test two-task extraction converted to organism
            print "TEST 2: convert_twotask_organism"
            if not os.path.exists("two_task_only_individual_modularity__organisms"):
                print "  No two_task_only_individual_modularity__organisms/ found."
                print "-------------------------------------------------------- FAILED"
                failed_lines.append( "%s - Test 2 - missing dir" % file)
            else:
                os.chdir("two_task_only_individual_modularity__organisms")
                two_task_files = glob.glob("*two_task_only__*.dat*")
                two_task_organisms_ct = len(two_task_files)

                if len(two_task_files) != expected:
                    print "  Wrong count. Expected: %s, found: %s" % (expected, len(two_task_files))
                    print "-------------------------------------------------------- FAILED"
                    failed_lines.append( "%s - Test 2 - bad count" % file)
                else:
                    print "  File count aggrees. OK :D"
                    print "---------------------------------------------------------------- PASSED"

                if len(two_task_files) > 0 and two_task_files[0][-3:] == ".gz":
                    print "  Files not sanitized. run sanitize for speed."
                    print "----------------------------------------------- NOTE"

                os.chdir("../")

        if '4' in test or 'all' in test:
            ## test calc_phys_mod converted to organism
            print "TEST 4: calc_phys_mod_organism"
            phys_mod_files_organisms_ct = 0
            if not os.path.exists("physical_modularity_stats__organisms"):
                print "  No physical_modularity_stats__organisms/ found."
                print "-------------------------------------------------------- FAILED"
                failed_lines.append( "%s - Test 4 - missing dir" % file)

            else:
                os.chdir("physical_modularity_stats__organisms")
                phys_mod_files = glob.glob("task_physical_modularity__*.dat*")
                phys_mod_files_organisms_ct = len(phys_mod_files)

                if len(phys_mod_files) != expected:
                    print "  Wrong count. Expected: %s found: %s" % (expected, len(phys_mod_files))
                    print "-------------------------------------------------------- FAILED"
                    failed_lines.append( "%s - Test 4 - bad count" % file)
                else:
                    print "  File count agrees. OK :D"
                    print "---------------------------------------------------------------- PASSED"

                if len(phys_mod_files) > 0 and phys_mod_files[0][-3:] == ".gz":
                    print "  Files not sanitized. run sanitize for speed."
                    print "----------------------------------------------- NOTE"
                
                os.chdir("../")

        if '6' in test or 'all' in test:
            ## test collect_phys_mod converted to organism
            print "TEST 6: collect_phys_mod_organism"
            collected_phys_mod_files = glob.glob("*__two_task_physical_modularity__stats__organisms.csv*")
            if len(collected_phys_mod_files) < 12:
                print "missing some collected physical modularity stats. %s out of 12" % len(collected_phys_mod_files)
                print "-------------------------------------------------------- FAILED"
                failed_lines.append( "%s - Test 6 - missing files" % file)


            for c_p_file in (collected_phys_mod_files):
                if os.path.getsize(c_p_file) == 0:
                    print "  %s is empty."
                    print "  ------------------------------------------------------ FAILED"
                else:
                    cmd = "cat"
                    if c_p_file[-3:] == ".gz":
                        cmd = "zcat -c -f"
                    lines = os.popen("%s %s | wc -l" % (cmd, c_p_file)).read()

                    print "  %s: has %s lines out of expected %s" % (c_p_file, int(lines), expected)
                    if int(lines) == expected:
                        print "  -------------------------------------------------------------- PASSED"
                    else:
                        print "  ------------------------------------------------------ FAILED"
                        failed_lines.append( "%s %s - Test 6 - bad count" % (file, c_p_file))


            if len(collected_phys_mod_files) > 0 and collected_phys_mod_files[0][-3:] == ".gz":
                print "  Files not sanitized. run sanitize for speed."
                print "----------------------------------------------- NOTE"

        if '8' in test or 'all' in test:
            ## collect funct_mod_organism
            print "TEST 8: collect_funct_mod_organism"
            collected_funct_mod_files = glob.glob("two_task_functional_modularity__stats__organisms.csv*")
            if len(collected_funct_mod_files) < 1:
                print "  missing collected functional modularity stats. 0/1"
                print "-------------------------------------------------------- FAILED"
                failed_lines.append( "%s - Test 8 - missing file" % file)

            for c_f_file in (collected_funct_mod_files):
                if os.path.getsize(c_f_file) == 0:
                    print "  %s is empty."
                    print "-------------------------------------------------------- FAILED"
                else:
                    cmd = "cat"
                    if c_p_file[-3:] == ".gz":
                        cmd = "zcat -c -f"

                    lines = os.popen("%s %s | wc -l" % (cmd, c_p_file)).read()
                    lines = lines.strip()
    
                    print "  %s: has %s lines out of expected %s" % (c_f_file, lines, expected)

                    if int(lines) == expected:
                        print "---------------------------------------------------------------- PASSED"
                    else:
                        print "-------------------------------------------------------- FAILED"
                        failed_lines.append( "%s %s - Test 8 - bad count" % (file, c_f_file))

            if len(collected_funct_mod_files) > 0 and collected_funct_mod_files[0][-3:] == ".gz":
                print "Files not sanitized. run sanitize for speed."
                print "----------------------------------------------- NOTE"

        ## done
        os.chdir("../../") ## done with the stuff in each directory
        print "Done with %s" % file
        print


    print "Testing Aggregate Data."
    print "======================="
    print "test actions: aggregate_phys_mod, aggregate_funct_mod, task, fitness"

    ## aggregated files
    aggregated_files = glob.glob("*.csv")
    print "Found %s aggregated files out of 45" % len(aggregated_files)

    for ag_file in (aggregated_files):
        if os.path.getsize(ag_file) == 0:
            print "%s is empty." % ag_file
        else:
            lines = os.popen("cat %s | wc -l" % ag_file).read()
            print "%s: has %s lines" % (ag_file, lines)

    print
    print "SUMMARY"
    print "======="
    for line in failed_lines:
        print line

    print
    print "DONE"


def aggregate_phys_mod( pattern, task, measure, condition ):
    files = glob.glob(pattern)
    print "  %s task - %s - %s - %s" % ( task, measure, condition, options.treatment )
    
    outfilename = "%s_%s__%s_task_%s.csv" % ( condition, options.treatment, task, measure )

    if options.update_only and os.path.exists(outfilename) and os.path.getsize(outfilename) > 0:
        print "Skipping %s" % outfilename
        return

    if os.path.exists(outfilename):
        os.unlink(outfilename)

    for file in files:
        if os.path.exists("%s/data" % file):
            os.chdir("%s/data/" % file)
            if not os.path.exists("%s_task_%s__two_task_physical_modularity__stats__organisms.csv" % ( task, measure ) ):
                print "Missing prerequisite: stage 3 - %s %s_task_%s__two_task_physical_modularity__stats__organisms.csv" % ( file, task, measure )
                return

            os.popen( "python %s --dimensionality 1 -s \",\" 1 %s_task_%s__two_task_physical_modularity__stats__organisms.csv >> ../../%s" % (
                extract_single_column_to_csv_path, task, measure, outfilename ) )
            os.chdir("../../")
        else:
            print "%s does not exist" % file    

if "aggregate_phys_mod" in actions: ## stage 4

    print "aggregate_phys_mod"
    if options.screen: ## we're in a screen!
        print "Screen is not a valid mode for this stage."
    else:
        primary = ["control*_??????", "noreward*_??????", "punish*_??????"]
        names = ["control", "noreward", "punish"]
        secondary = ["backbone", "fluct"]
        tertiary = ["unity", "scatter", "gapmean", "gapmedian", "gapvar", "gapstd"]

        for i in range(0, len(primary)):
            pattern = primary[i]
            name = names[i]
            for task in secondary:
                for measure in tertiary:
                    aggregate_phys_mod(pattern, task, measure, name)


def proc_aggregate_mut_file( pattern, measure, aggregation, condition, infile, outfile ):
    files = glob.glob(pattern)
    print "  %s - %s - %s" % ( measure, condition, options.treatment )

    if options.update_only and os.path.exists(outfile) and os.path.getsize(outfile) > 0:
        print "Skipping %s" % outfile
        return

    if os.path.exists(outfile):
        os.unlink(outfile)

    for file in files:
        if os.path.exists("%s/data/" % file):
            os.chdir("%s/data/" % file)
            os.popen( "python %s -s \",\" --header --%s %s >> ../../%s" % ( aggregate_file_path, aggregation, infile, outfile ) )
            os.chdir("../../")
        else:
            print "%s does not exist" % file    

if "aggregate_mutation_metrics" in actions: ## 
    print "aggregate_mutation_metrics"
    if options.screen: ## we're in a screen!
        print "Screen is not a valid mode for this stage."
    else:
        proc_aggregate_mut_file("control*_??????", "sum_dominant_lineage_mutation_metrics", "sum", "control", "mutation_metrics.csv*", "control_%s__sum_dominant_lineage_mutation_metrics.csv" % options.treatment)
        proc_aggregate_mut_file("noreward*_??????", "sum_dominant_lineage_mutation_metrics", "sum", "noreward", "mutation_metrics.csv*", "noreward_%s__sum_dominant_lineage_mutation_metrics.csv" % options.treatment)
        proc_aggregate_mut_file("punish*_??????", "sum_dominant_lineage_mutation_metrics", "sum", "punish", "mutation_metrics.csv*", "punish_%s__sum_dominant_lineage_mutation_metrics.csv" % options.treatment)

        proc_aggregate_mut_file("control*_??????", "mean_dominant_lineage_mutation_metrics", "mean", "control", "mutation_metrics.csv*", "control_%s__mean_dominant_lineage_mutation_metrics.csv" % options.treatment)
        proc_aggregate_mut_file("noreward*_??????", "mean_dominant_lineage_mutation_metrics", "mean", "noreward", "mutation_metrics.csv*", "noreward_%s__mean_dominant_lineage_mutation_metrics.csv" % options.treatment)
        proc_aggregate_mut_file("punish*_??????", "mean_dominant_lineage_mutation_metrics", "mean", "punish", "mutation_metrics.csv*", "punish_%s__mean_dominant_lineage_mutation_metrics.csv" % options.treatment)



def proc_aggregate_run_file( pattern, measure, column, condition, infile, outfile ):
    files = glob.glob(pattern)
    print "  %s - %s - %s" % ( measure, condition, options.treatment )

    if options.update_only and os.path.exists(outfile) and os.path.getsize(outfile) > 0:
        print "Skipping %s" % outfile
        return

    if os.path.exists(outfile):
        os.unlink(outfile)

    for file in files:
        if os.path.exists("%s/data/" % file):
            os.chdir("%s/data/" % file)
            if options.verbose:
                print "python %s --dimensionality 1 -s \" \" %s %s >> ../../%s" % ( extract_single_column_to_csv_path, column, infile, outfile )
            os.popen( "python %s --dimensionality 1 -s \" \" %s %s >> ../../%s" % ( extract_single_column_to_csv_path, column, infile, outfile ) )
            os.chdir("../../")
        else:
            print "%s does not exist" % file    

if "tasks" in actions: ## 
    print "tasks"
    if options.screen: ## we're in a screen!
        print "Screen is not a valid mode for this stage."
    else:
        proc_aggregate_run_file("control*_??????", "fluct_task_count", 3, "control", "tasks.dat*", "control_%s__fluct_task_count.csv" % options.treatment)
        proc_aggregate_run_file("noreward*_??????", "fluct_task_count", 3, "noreward", "tasks.dat*", "noreward_%s__fluct_task_count.csv" % options.treatment)
        proc_aggregate_run_file("punish*_??????", "fluct_task_count", 3, "punish", "tasks.dat*", "punish_%s__fluct_task_count.csv" % options.treatment)

if "fitness" in actions: ## 
    print "fitness"
    if options.screen: ## we're in a screen!
        print "Screen is not a valid mode for this stage."
    else:
        proc_aggregate_run_file("control*_??????", "fitness", 4, "control", "average.dat*", "control_%s__fitness.csv" % options.treatment)
        proc_aggregate_run_file("noreward*_??????", "fitness", 4, "noreward", "average.dat*", "noreward_%s__fitness.csv" % options.treatment)
        proc_aggregate_run_file("punish*_??????", "fitness", 4, "punish", "average.dat*", "punish_%s__fitness.csv" % options.treatment)

if "coalescent" in actions: ## 
    print "coalescent"
    if options.screen: ## we're in a screen!
        print "Screen is not a valid mode for this stage."
    else:
        proc_aggregate_run_file("control*_??????", "coalescent generations", 10, "control", "stats.dat*", "control_%s__coalescent.csv" % options.treatment)
        proc_aggregate_run_file("noreward*_??????", "coalescent generations", 10, "noreward", "stats.dat*", "noreward_%s__coalescent.csv" % options.treatment)
        proc_aggregate_run_file("punish*_??????", "coalescent generations", 10, "punish", "stats.dat*", "punish_%s__coalescent.csv" % options.treatment)


def aggregate_funct_mod( pattern, condition ):
    files = glob.glob(pattern)
    print "  %s - %s" % ( condition, options.treatment )

    outfilename = "%s_%s__functional_modularity.csv" % ( condition, options.treatment )

    if options.update_only and os.path.exists(outfilename) and os.path.getsize(outfilename) > 0:
        print "Skipping %s" % outfilename
        return

    if os.path.exists(outfilename):
        os.unlink(outfilename)

    for file in files:
        #print file
        if os.path.exists("%s/data/" % file):
            os.chdir("%s/data/" % file)
            if not os.path.exists("two_task_functional_modularity__stats__organisms.csv"):
                print "Missing prerequisite: collect_funct_mod: two_task_functional_modularity__stats__organisms.csv" % ( task, measure )
                return

            os.popen( "python %s --dimensionality 1 -s \",\" 1 two_task_functional_modularity__stats__organisms.csv >> ../../%s" %
                (extract_single_column_to_csv_path, outfilename ) )
            os.chdir("../../")
                
        else:
            print "%s does not exist" % file    

if "aggregate_funct_mod" in actions: ## stage 4

    print "aggregate_funct_mod"
    if options.screen: ## we're in a screen!
        print "Screen is not a valid mode for this stage."
    else:
        aggregate_funct_mod("control*_??????", "control")
        aggregate_funct_mod("noreward*_??????", "noreward")
        aggregate_funct_mod("punish*_??????", "punish")


