
import read_intermediate_files as rif

data_structure = rif.read_intermediate_datafile('intermediate_file_format.txt')

print str(data_structure)

rif.output_to_intermediate_format( data_structure )
