
## read datafiles

def read_intermediate_datafile( filename ):

    root_data_structure = {}

    fd = open(filename)

    in_section = False
    section_name_assigned = False
    data_names_assigned = False
    section_name = ''
    data_names = ''

    for line in fd:
        line = line.strip() ## strip off the end of line crap
        if ( len(line) == 0 and in_section == False ) or (len(line) > 0 and line[0] == '#'): ## if the line is a comment or regular blank line
            continue ## do nothing

        elif len(line) == 0 and in_section == True: ## the end of the section! reset for the next one
            in_section = False
            section_name_assigned = False
            section_name = ''
            data_names_assigned = False
            data_names = ''            

        elif not section_name_assigned:
            section_name = line
            section_name_assigned = True
            assert( len(section_name) > 0 )            
            root_data_structure[section_name] = {}

        elif not data_names_assigned:
            data_names_assigned = True
            data_names = line
            assert( len(data_names) > 0 )
            in_section = True

        elif in_section:
            line = line.split(',') ## split up the line on commas
            root_data_structure[section_name][line[0]] = line[1:] ## shove the rest of the line in there

    fd.close()
    return root_data_structure

def output_to_intermediate_format( root_data_structure ):

    for section_name in root_data_structure.keys():
        print section_name
        print "key, values" ## for the rest of it, fuck 
        for key in root_data_structure[ section_name ].keys():
            print key + "," + ",".join( root_data_structure[ section_name ][ key ] )
        print ## blank line to delineate the end of the section

