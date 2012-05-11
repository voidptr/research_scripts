import numpy as np
from DataTable import *
import pdb
import gzip as gz

class AvidaData:

   def __init__(self, file):
      type = {\
         'id':   'int',\
         'src': 'string',\
         'src_args': 'string',\
         'parent_id': 'int',\
         'parents': 'int',\
         'parent_dist': 'int',\
         'num_cpus': 'int',\
         'num_units': 'int',\
         'total_units': 'int',\
         'total_cpus': 'int',\
         'length': 'int',\
         'merit': 'float',\
         'gest_time': 'float',\
         'fitness': 'float',\
         'gen_born': 'int',\
         'update_born': 'int',\
         'update_dead': 'int',\
         'update_deactivated': 'int',\
         'depth': 'int',\
         'hw_type': 'int',\
         'inst_set': 'string',\
         'sequence': 'string',\
         'cells': 'string',\
         'gest_offset': 'string',\
         'lineage': 'string',\
         'phen_entropy': 'float',\
         'phen_max_fitness': 'float',\
         'task.0':'float',\
         'task.1':'float',\
         'task.2':'float',\
         'task.3':'float',\
         'task.4':'float',\
         'task.5':'float',\
         'task.6':'float',\
         'task.7':'float',\
         'task.8':'float',\
         'alignment':'string'
      }
      order = []
      fid = gz.open(file, 'rb')
      try:
         fid.readline() # Skip first header line
         format = fid.readline().strip() # Read format line
         for f in format.split(' '):
            if (f[0] == '#'):
               continue
            order.append(f)
         self.dt = DataTable(file, order, type)      
      finally:
         fid.close()
      
   def __getitem__(self,descr):
      return self.dt[descr]           
  
   def table(self):
      return self.dt.table()

   def columns(self):
      return self.dt.columns()

   def rows(self):
      return self.dt.rows()
      
   def rearrange(self,ndx):
      for k,v in self.dt.col.items():
         self.dt.col[k] = v[ndx]
      return

